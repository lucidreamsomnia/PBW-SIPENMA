# backend/app/services/nilai_service.py
from sqlalchemy.orm import Session

from backend.app.models.nilai import Nilai
from backend.app.models.krs import KRS
from backend.app.models.grade import Grade
from backend.app.schemas.nilai import NilaiCreate, NilaiUpdate

def hitung_nilai_akhir(tugas: float, uts: float, uas: float) -> float:
    return round(
        (tugas * 0.30) +
        (uts * 0.30) +
        (uas * 0.40),
        2
    )


def get_grade(db: Session, nilai_akhir: float):
    return (
        db.query(Grade)
        .filter(
            Grade.nilai_min <= nilai_akhir,
            Grade.nilai_max >= nilai_akhir,
        )
        .first()
    )

def get_all_nilai(db: Session):
    # Mengambil data nilai yang diimpor dari file SQL di XAMPP
    return db.query(Nilai).all()

def get_nilai_by_krs(db: Session, id_krs: int):
    return db.query(Nilai).filter(Nilai.id_krs == id_krs).first()

def create_nilai(db: Session, data: NilaiCreate):
    # Pastikan KRS ada
    krs = db.query(KRS).filter(KRS.id_krs == data.id_krs).first()
    print("KRS :", krs)
    
    if not krs:
        print("KRS tidak ditemukan")
        return None
    
    existing = db.query(Nilai).filter(
         Nilai.id_krs == data.id_krs
         ).first()
    
    print("Existing :", existing)
    
    if existing:
        print("Nilai sudah ada")
        return None
    
    nilai_akhir = hitung_nilai_akhir(
        data.tugas,
        data.uts,
        data.uas
    )
    
    print("Nilai akhir :", nilai_akhir)
    
    grade = get_grade(db, nilai_akhir)
    
    print("Grade :", grade)
    
    if not grade:
        print("Grade tidak ditemukan")
        return None

    nilai = Nilai(
        id_krs=data.id_krs,
        nilai_akhir=nilai_akhir,
        id_grade=grade.id_grade,
        status_publish=0,
    )

    db.add(nilai)
    db.commit()
    db.refresh(nilai)

    return {
        "id_nilai": nilai.id_nilai,
        "id_krs": nilai.id_krs,
        "nilai_akhir": float(nilai.nilai_akhir),
        "grade": grade.nama_grade,
    }