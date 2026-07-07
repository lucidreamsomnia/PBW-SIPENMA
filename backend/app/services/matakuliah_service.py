# backend/app/services/matakuliah_service.py
from sqlalchemy.orm import Session

def get_all_matakuliah(db: Session):
    return [{"id": 101, "nama_mk": "Pemrograman Berbasis Web", "sks": 3}, {"id": 102, "nama_mk": "Arsitektur Sistem", "sks": 2}]

def get_matakuliah(db: Session, mk_id: int):
    data = {101: {"id": 101, "nama_mk": "Pemrograman Berbasis Web", "sks": 3}, 102: {"id": 102, "nama_mk": "Arsitektur Sistem", "sks": 2}}
    return data.get(mk_id, None)

def search_matakuliah(db: Session, query: str):
    all_data = [{"id": 101, "nama_mk": "Pemrograman Berbasis Web", "sks": 3}, {"id": 102, "nama_mk": "Arsitektur Sistem", "sks": 2}]
    return [mk for mk in all_data if query.lower() in mk["nama_mk"].lower()]