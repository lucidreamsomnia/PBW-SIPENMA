# backend/app/routes/statistik.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.connection import get_db
from backend.app.services import statistik_service

router = APIRouter(prefix="/statistik", tags=["Statistik (Dosen)"])

@router.get("/")
def read_statistik(db: Session = Depends(get_db)):
    return statistik_service.get_statistik_nilai(db)