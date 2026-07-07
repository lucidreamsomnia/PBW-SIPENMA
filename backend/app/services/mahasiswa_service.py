# backend/app/services/mahasiswa_service.py
from sqlalchemy.orm import Session

# Catatan: Menggunakan data dummy / silakan hubungkan dengan Model Mahasiswa milik Admin jika sudah ada
def get_all_mahasiswa(db: Session):
    return [{"id": 1, "nama": "Budi Santoso", "nim": "12345678"}, {"id": 2, "nama": "Siti Aminah", "nim": "87654321"}]

def get_mahasiswa(db: Session, mahasiswa_id: int):
    data = {1: {"id": 1, "nama": "Budi Santoso", "nim": "12345678"}, 2: {"id": 2, "nama": "Siti Aminah", "nim": "87654321"}}
    return data.get(mahasiswa_id, None)

def search_mahasiswa(db: Session, query: str):
    all_data = [{"id": 1, "nama": "Budi Santoso", "nim": "12345678"}, {"id": 2, "nama": "Siti Aminah", "nim": "87654321"}]
    return [m for m in all_data if query.lower() in m["nama"].lower() or query in m["nim"]]