# backend/app/routes/matakuliah.py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.schemas.matakuliah import (
    MataKuliahCreate,
    MataKuliahOptionsResponse,
    MataKuliahPageResponse,
    MataKuliahResponse,
    MataKuliahUpdate,
)
from backend.app.services import matakuliah_service
from typing import List, Optional

router = APIRouter(prefix="/matakuliah", tags=["Matakuliah (Shared)"])

@router.get("/", response_model=List[MataKuliahResponse])
def get_matakuliah_list(
    search: Optional[str] = None,
    semester: Optional[int] = None,
    status_mk: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return matakuliah_service.get_all_matakuliah(
        db,
        search=search,
        semester=semester,
        status=status_mk,
    )


@router.get("/page", response_model=MataKuliahPageResponse)
def get_matakuliah_page(
    search: Optional[str] = None,
    semester: Optional[int] = None,
    status_mk: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return matakuliah_service.get_matakuliah_page(
        db,
        search=search,
        semester=semester,
        status=status_mk,
        page=page,
        limit=limit,
    )


@router.get("/options", response_model=MataKuliahOptionsResponse)
def get_matakuliah_options(db: Session = Depends(get_db)):
    return matakuliah_service.get_options(db)


@router.get("/{id}", response_model=MataKuliahResponse)
def get_matakuliah_detail(id: int, db: Session = Depends(get_db)):
    mk = matakuliah_service.get_matakuliah(db, id)
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah tidak ditemukan")
    return mk

@router.post("/", response_model=MataKuliahResponse, status_code=status.HTTP_201_CREATED)
def create_matakuliah(data: MataKuliahCreate, db: Session = Depends(get_db)):
    if matakuliah_service.kode_exists(db, data.kode_mk):
        raise HTTPException(status_code=400, detail="Kode mata kuliah sudah digunakan")
    return matakuliah_service.create_matakuliah(db, data)


@router.put("/{id}", response_model=MataKuliahResponse)
def update_matakuliah(id: int, data: MataKuliahUpdate, db: Session = Depends(get_db)):
    if data.kode_mk and matakuliah_service.kode_exists(db, data.kode_mk, exclude_id=id):
        raise HTTPException(status_code=400, detail="Kode mata kuliah sudah digunakan")

    updated = matakuliah_service.update_matakuliah(db, id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Matakuliah tidak ditemukan")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_matakuliah(id: int, db: Session = Depends(get_db)):
    try:
        deleted = matakuliah_service.delete_matakuliah(db, id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Mata kuliah tidak dapat dihapus karena masih digunakan oleh data lain",
        )

    if not deleted:
        raise HTTPException(status_code=404, detail="Matakuliah tidak ditemukan")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
