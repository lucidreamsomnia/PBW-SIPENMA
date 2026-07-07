from math import ceil
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.models.role import Role
from backend.app.models.user import User
from backend.app.schemas.pengguna import PenggunaCreate, PenggunaUpdate
from backend.app.utils.security import hash_password


def _base_query(db: Session):
	return db.query(User, Role).join(Role, User.id_role == Role.id_role)


def _serialize(row):
	user, role = row
	return {
		"id_user": user.id_user,
		"id_role": user.id_role,
		"username": user.username,
		"email": user.email,
		"status_aktif": bool(user.status_aktif),
		"nama_role": role.nama_role if role else None,
		"deskripsi_role": role.deskripsi if role else None,
		"created_at": user.created_at,
		"updated_at": user.updated_at,
	}


def _apply_filters(
	query,
	search: Optional[str] = None,
	id_role: Optional[int] = None,
	status_aktif: Optional[bool] = None,
):
	if search:
		pattern = f"%{search}%"
		query = query.filter(
			or_(
				User.username.like(pattern),
				User.email.like(pattern),
				Role.nama_role.like(pattern),
			)
		)
	if id_role:
		query = query.filter(User.id_role == id_role)
	if status_aktif is not None:
		query = query.filter(User.status_aktif == status_aktif)
	return query


def get_all_pengguna(
	db: Session,
	search: Optional[str] = None,
	id_role: Optional[int] = None,
	status_aktif: Optional[bool] = None,
):
	query = _apply_filters(
		_base_query(db),
		search=search,
		id_role=id_role,
		status_aktif=status_aktif,
	)
	rows = query.order_by(User.id_user.desc()).all()
	return [_serialize(row) for row in rows]


def get_pengguna_page(
	db: Session,
	search: Optional[str] = None,
	id_role: Optional[int] = None,
	status_aktif: Optional[bool] = None,
	page: int = 1,
	limit: int = 10,
):
	page = max(page, 1)
	limit = min(max(limit, 1), 100)
	query = _apply_filters(
		_base_query(db),
		search=search,
		id_role=id_role,
		status_aktif=status_aktif,
	)
	total = query.count()
	rows = (
		query.order_by(User.id_user.desc())
		.offset((page - 1) * limit)
		.limit(limit)
		.all()
	)

	return {
		"data": [_serialize(row) for row in rows],
		"total": total,
		"page": page,
		"limit": limit,
		"total_pages": ceil(total / limit) if total else 0,
	}


def get_pengguna(db: Session, pengguna_id: int):
	row = _base_query(db).filter(User.id_user == pengguna_id).first()
	return _serialize(row) if row else None


def get_options(db: Session):
	roles = db.query(Role).order_by(Role.nama_role).all()
	return {
		"roles": [
			{
				"id_role": item.id_role,
				"nama_role": item.nama_role,
				"deskripsi": item.deskripsi,
			}
			for item in roles
		],
		"status": [
			{"value": True, "label": "Aktif"},
			{"value": False, "label": "Nonaktif"},
		],
	}


def username_exists(db: Session, username: str, exclude_id: Optional[int] = None):
	query = db.query(User).filter(User.username == username)
	if exclude_id:
		query = query.filter(User.id_user != exclude_id)
	return query.first() is not None


def email_exists(db: Session, email: str, exclude_id: Optional[int] = None):
	query = db.query(User).filter(User.email == email)
	if exclude_id:
		query = query.filter(User.id_user != exclude_id)
	return query.first() is not None


def role_exists(db: Session, role_id: int):
	return db.query(Role).filter(Role.id_role == role_id).first() is not None


def create_pengguna(db: Session, data: PenggunaCreate):
	payload = data.model_dump()
	password = payload.pop("password")
	payload["password_hash"] = hash_password(password)
	pengguna = User(**payload)
	db.add(pengguna)
	db.commit()
	db.refresh(pengguna)
	return get_pengguna(db, pengguna.id_user)


def update_pengguna(db: Session, pengguna_id: int, data: PenggunaUpdate):
	pengguna = db.query(User).filter(User.id_user == pengguna_id).first()
	if not pengguna:
		return None

	updates = data.model_dump(exclude_unset=True)
	password = updates.pop("password", None)
	if password:
		updates["password_hash"] = hash_password(password)

	for field, value in updates.items():
		setattr(pengguna, field, value)

	db.commit()
	db.refresh(pengguna)
	return get_pengguna(db, pengguna.id_user)


def delete_pengguna(db: Session, pengguna_id: int):
	pengguna = db.query(User).filter(User.id_user == pengguna_id).first()
	if not pengguna:
		return False

	db.delete(pengguna)
	db.commit()
	return True