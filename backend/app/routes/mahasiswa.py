# backend/app/routes/mahasiswa.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.services import mahasiswa_service
from typing import Optional

router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa (Shared)"])

@router.get("/")
def get_mahasiswa_list(search: Optional[str] = None, db: Session = Depends(get_db)):
    if search:
        return mahasiswa_service.search_mahasiswa(db, search)
    return mahasiswa_service.get_all_mahasiswa(db)

@router.get("/{id}")
def get_mahasiswa_detail(id: int, db: Session = Depends(get_db)):
    mhs = mahasiswa_service.get_mahasiswa(db, id)
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    return mhs

# KETERANGAN: POST, PUT, DELETE dikerjakan oleh Admin (Tidak ditulis di sini sesuai instruksi)