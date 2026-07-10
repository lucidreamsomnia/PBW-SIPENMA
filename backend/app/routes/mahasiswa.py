# backend/app/routes/mahasiswa.py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.schemas.mahasiswa import (
    MahasiswaCreate,
    MahasiswaOptionsResponse,
    MahasiswaPageResponse,
    MahasiswaResponse,
    MahasiswaUpdate,
)
from backend.app.services import mahasiswa_service
from typing import List, Optional

router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa (Shared)"])

@router.get("/", response_model=List[MahasiswaResponse])
def get_mahasiswa_list(
    search: Optional[str] = None,
    id_prodi: Optional[int] = None,
    angkatan: Optional[int] = None,
    status_mahasiswa: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return mahasiswa_service.get_all_mahasiswa(
        db,
        search=search,
        id_prodi=id_prodi,
        angkatan=angkatan,
        status=status_mahasiswa,
    )


@router.get("/page", response_model=MahasiswaPageResponse)
def get_mahasiswa_page(
    search: Optional[str] = None,
    id_prodi: Optional[int] = None,
    angkatan: Optional[int] = None,
    status_mahasiswa: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return mahasiswa_service.get_mahasiswa_page(
        db,
        search=search,
        id_prodi=id_prodi,
        angkatan=angkatan,
        status=status_mahasiswa,
        page=page,
        limit=limit,
    )


@router.get("/options", response_model=MahasiswaOptionsResponse)
def get_mahasiswa_options(db: Session = Depends(get_db)):
    return mahasiswa_service.get_options(db)


@router.get("/{id}", response_model=MahasiswaResponse)
def get_mahasiswa_detail(id: int, db: Session = Depends(get_db)):
    mhs = mahasiswa_service.get_mahasiswa(db, id)
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return mhs


@router.post("/", response_model=MahasiswaResponse, status_code=status.HTTP_201_CREATED)
def create_mahasiswa(data: MahasiswaCreate, db: Session = Depends(get_db)):
    if mahasiswa_service.nim_exists(db, data.nim):
        raise HTTPException(status_code=400, detail="NIM sudah digunakan")
    if not mahasiswa_service.prodi_exists(db, data.id_prodi):
        raise HTTPException(status_code=400, detail="Program studi tidak ditemukan")
    return mahasiswa_service.create_mahasiswa(db, data)


@router.put("/{id}", response_model=MahasiswaResponse)
def update_mahasiswa(id: int, data: MahasiswaUpdate, db: Session = Depends(get_db)):
    if data.nim and mahasiswa_service.nim_exists(db, data.nim, exclude_id=id):
        raise HTTPException(status_code=400, detail="NIM sudah digunakan")
    if data.id_prodi and not mahasiswa_service.prodi_exists(db, data.id_prodi):
        raise HTTPException(status_code=400, detail="Program studi tidak ditemukan")

    updated = mahasiswa_service.update_mahasiswa(db, id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mahasiswa(id: int, db: Session = Depends(get_db)):
    try:
        deleted = mahasiswa_service.delete_mahasiswa(db, id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Mahasiswa tidak dapat dihapus karena masih digunakan oleh data lain",
        )

    if not deleted:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
