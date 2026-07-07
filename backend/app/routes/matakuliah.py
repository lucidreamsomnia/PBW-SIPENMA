# backend/app/routes/matakuliah.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.services import matakuliah_service
from typing import Optional

router = APIRouter(prefix="/matakuliah", tags=["Matakuliah (Shared)"])

@router.get("/")
def get_matakuliah_list(search: Optional[str] = None, db: Session = Depends(get_db)):
    if search:
        return matakuliah_service.search_matakuliah(db, search)
    return matakuliah_service.get_all_matakuliah(db)

@router.get("/{id}")
def get_matakuliah_detail(id: int, db: Session = Depends(get_db)):
    mk = matakuliah_service.get_matakuliah(db, id)
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah tidak ditemukan")
    return mk

# KETERANGAN: POST, PUT, DELETE dikerjakan oleh Admin (Tidak ditulis di sini sesuai instruksi)