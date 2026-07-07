# backend/app/services/statistik_service.py
from sqlalchemy.orm import Session
from backend.app.models.nilai import Nilai
from sqlalchemy import func

def get_statistik_nilai(db: Session):
    # Menghitung rata-rata nilai akhir, nilai tertinggi, dan nilai terendah
    stats = db.query(
        func.avg(Nilai.nilai_akhir).label("rata_rata"),
        func.max(Nilai.nilai_akhir).label("tertinggi"),
        func.min(Nilai.nilai_akhir).label("terendah")
    ).first()
    
    return {
        "rata_rata": round(stats.rata_rata, 2) if stats.rata_rata else 0,
        "tertinggi": stats.tertinggi if stats.tertinggi else 0,
        "terendah": stats.terendah if stats.terendah else 0
    }