# backend/app/routes/nilai.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.schemas.nilai import NilaiCreate, NilaiUpdate, NilaiResponse
from backend.app.services import nilai_service
from typing import List

router = APIRouter(prefix="/nilai", tags=["Nilai (Dosen)"])

@router.get("/", response_model=List[NilaiResponse])
def read_all_nilai(db: Session = Depends(get_db)):
    return nilai_service.get_all_nilai(db)

@router.post("/", response_model=NilaiResponse)
def input_nilai(nilai_data: NilaiCreate, db: Session = Depends(get_db)):
    return nilai_service.create_nilai(db, nilai_data)

@router.put("/{nilai_id}", response_model=NilaiResponse)
def edit_nilai(nilai_id: int, nilai_data: NilaiUpdate, db: Session = Depends(get_db)):
    updated = nilai_service.update_nilai(db, nilai_id, nilai_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Data nilai tidak ditemukan")
    return updated