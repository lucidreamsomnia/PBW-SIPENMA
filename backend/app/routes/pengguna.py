from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.pengguna import (
	PenggunaCreate,
	PenggunaOptionsResponse,
	PenggunaPageResponse,
	PenggunaResponse,
	PenggunaUpdate,
)
from backend.app.services import pengguna_service

router = APIRouter(prefix="/pengguna", tags=["Pengguna (Admin)"])


@router.get("/", response_model=List[PenggunaResponse])
def get_pengguna_list(
	search: Optional[str] = None,
	id_role: Optional[int] = None,
	status_aktif: Optional[bool] = None,
	db: Session = Depends(get_db),
):
	return pengguna_service.get_all_pengguna(
		db,
		search=search,
		id_role=id_role,
		status_aktif=status_aktif,
	)


@router.get("/page", response_model=PenggunaPageResponse)
def get_pengguna_page(
	search: Optional[str] = None,
	id_role: Optional[int] = None,
	status_aktif: Optional[bool] = None,
	page: int = 1,
	limit: int = 10,
	db: Session = Depends(get_db),
):
	return pengguna_service.get_pengguna_page(
		db,
		search=search,
		id_role=id_role,
		status_aktif=status_aktif,
		page=page,
		limit=limit,
	)


@router.get("/options", response_model=PenggunaOptionsResponse)
def get_pengguna_options(db: Session = Depends(get_db)):
	return pengguna_service.get_options(db)


@router.get("/{id}", response_model=PenggunaResponse)
def get_pengguna_detail(id: int, db: Session = Depends(get_db)):
	pengguna = pengguna_service.get_pengguna(db, id)
	if not pengguna:
		raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
	return pengguna


@router.post("/", response_model=PenggunaResponse, status_code=status.HTTP_201_CREATED)
def create_pengguna(data: PenggunaCreate, db: Session = Depends(get_db)):
	if not pengguna_service.role_exists(db, data.id_role):
		raise HTTPException(status_code=400, detail="Role tidak ditemukan")
	if pengguna_service.username_exists(db, data.username):
		raise HTTPException(status_code=400, detail="Username sudah digunakan")
	if pengguna_service.email_exists(db, data.email):
		raise HTTPException(status_code=400, detail="Email sudah digunakan")
	return pengguna_service.create_pengguna(db, data)


@router.put("/{id}", response_model=PenggunaResponse)
def update_pengguna(id: int, data: PenggunaUpdate, db: Session = Depends(get_db)):
	if data.id_role and not pengguna_service.role_exists(db, data.id_role):
		raise HTTPException(status_code=400, detail="Role tidak ditemukan")
	if data.username and pengguna_service.username_exists(db, data.username, exclude_id=id):
		raise HTTPException(status_code=400, detail="Username sudah digunakan")
	if data.email and pengguna_service.email_exists(db, data.email, exclude_id=id):
		raise HTTPException(status_code=400, detail="Email sudah digunakan")

	updated = pengguna_service.update_pengguna(db, id, data)
	if not updated:
		raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
	return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pengguna(id: int, db: Session = Depends(get_db)):
	try:
		deleted = pengguna_service.delete_pengguna(db, id)
	except IntegrityError:
		db.rollback()
		raise HTTPException(
			status_code=409,
			detail="Pengguna tidak dapat dihapus karena masih digunakan oleh data lain",
		)

	if not deleted:
		raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
	return Response(status_code=status.HTTP_204_NO_CONTENT)