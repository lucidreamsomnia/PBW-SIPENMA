# backend/app/services/nilai_service.py
from sqlalchemy.orm import Session
from backend.app.models.nilai import Nilai

def get_all_nilai(db: Session):
    # Mengambil data nilai yang diimpor dari file SQL di XAMPP
    return db.query(Nilai).all()

def get_nilai_by_krs(db: Session, id_krs: int):
    return db.query(Nilai).filter(Nilai.id_krs == id_krs).first()