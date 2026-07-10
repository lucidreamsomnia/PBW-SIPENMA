# backend/app/services/matakuliah_service.py
from math import ceil
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.models.matakuliah import MataKuliah
from backend.app.schemas.matakuliah import MataKuliahCreate, MataKuliahUpdate


def _serialize(matakuliah: MataKuliah):
    return {
        "id_mk": matakuliah.id_mk,
        "kode_mk": matakuliah.kode_mk,
        "nama_mk": matakuliah.nama_mk,
        "sks": int(matakuliah.sks),
        "semester_rekomendasi": (
            int(matakuliah.semester_rekomendasi)
            if matakuliah.semester_rekomendasi is not None
            else None
        ),
        "status_mk": matakuliah.status_mk,
        "created_at": matakuliah.created_at,
        "updated_at": matakuliah.updated_at,
    }


def _apply_filters(
    query,
    search: Optional[str] = None,
    semester: Optional[int] = None,
    status: Optional[str] = None,
):
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                MataKuliah.kode_mk.like(pattern),
                MataKuliah.nama_mk.like(pattern),
            )
        )
    if semester:
        query = query.filter(MataKuliah.semester_rekomendasi == semester)
    if status:
        query = query.filter(MataKuliah.status_mk == status)
    return query


def get_all_matakuliah(
    db: Session,
    search: Optional[str] = None,
    semester: Optional[int] = None,
    status: Optional[str] = None,
):
    query = _apply_filters(
        db.query(MataKuliah),
        search=search,
        semester=semester,
        status=status,
    )
    rows = query.order_by(MataKuliah.id_mk.desc()).all()
    return [_serialize(row) for row in rows]


def get_matakuliah_page(
    db: Session,
    search: Optional[str] = None,
    semester: Optional[int] = None,
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
):
    page = max(page, 1)
    limit = min(max(limit, 1), 100)
    query = _apply_filters(
        db.query(MataKuliah),
        search=search,
        semester=semester,
        status=status,
    )
    total = query.count()
    rows = (
        query.order_by(MataKuliah.id_mk.desc())
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


def get_matakuliah(db: Session, mk_id: int):
    matakuliah = db.query(MataKuliah).filter(MataKuliah.id_mk == mk_id).first()
    return _serialize(matakuliah) if matakuliah else None


def search_matakuliah(db: Session, query: str):
    return get_all_matakuliah(db, search=query)


def get_options(db: Session):
    semester_rows = (
        db.query(MataKuliah.semester_rekomendasi)
        .distinct()
        .order_by(MataKuliah.semester_rekomendasi)
        .all()
    )
    status_rows = (
        db.query(MataKuliah.status_mk)
        .distinct()
        .order_by(MataKuliah.status_mk)
        .all()
    )
    return {
        "semester": [int(row[0]) for row in semester_rows if row[0] is not None],
        "status": [row[0] for row in status_rows if row[0]],
    }


def kode_exists(db: Session, kode_mk: str, exclude_id: Optional[int] = None):
    query = db.query(MataKuliah).filter(MataKuliah.kode_mk == kode_mk)
    if exclude_id:
        query = query.filter(MataKuliah.id_mk != exclude_id)
    return query.first() is not None


def create_matakuliah(db: Session, data: MataKuliahCreate):
    matakuliah = MataKuliah(**data.model_dump())
    db.add(matakuliah)
    db.commit()
    db.refresh(matakuliah)
    return get_matakuliah(db, matakuliah.id_mk)


def update_matakuliah(db: Session, mk_id: int, data: MataKuliahUpdate):
    matakuliah = db.query(MataKuliah).filter(MataKuliah.id_mk == mk_id).first()
    if not matakuliah:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(matakuliah, field, value)

    db.commit()
    db.refresh(matakuliah)
    return get_matakuliah(db, matakuliah.id_mk)


def delete_matakuliah(db: Session, mk_id: int):
    matakuliah = db.query(MataKuliah).filter(MataKuliah.id_mk == mk_id).first()
    if not matakuliah:
        return False

    db.delete(matakuliah)
    db.commit()
    return True
