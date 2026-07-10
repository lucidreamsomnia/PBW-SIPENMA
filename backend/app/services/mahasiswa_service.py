# backend/app/services/mahasiswa_service.py
from math import ceil
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.models.mahasiswa import Mahasiswa
from backend.app.models.program_studi import ProgramStudi
from backend.app.schemas.mahasiswa import MahasiswaCreate, MahasiswaUpdate


def _base_query(db: Session):
    return db.query(Mahasiswa, ProgramStudi).join(
        ProgramStudi,
        Mahasiswa.id_prodi == ProgramStudi.id_prodi,
    )


def _serialize(row):
    mahasiswa, prodi = row
    return {
        "id_mahasiswa": mahasiswa.id_mahasiswa,
        "nim": mahasiswa.nim,
        "nama": mahasiswa.nama,
        "id_prodi": mahasiswa.id_prodi,
        "nama_prodi": prodi.nama_prodi,
        "fakultas": prodi.fakultas,
        "angkatan": int(mahasiswa.angkatan),
        "jenis_kelamin": mahasiswa.jenis_kelamin,
        "email": mahasiswa.email,
        "no_hp": mahasiswa.no_hp,
        "alamat": mahasiswa.alamat,
        "status_mahasiswa": mahasiswa.status_mahasiswa,
        "created_at": mahasiswa.created_at,
        "updated_at": mahasiswa.updated_at,
    }


def _apply_filters(
    query,
    search: Optional[str] = None,
    id_prodi: Optional[int] = None,
    angkatan: Optional[int] = None,
    status: Optional[str] = None,
):
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Mahasiswa.nim.like(pattern),
                Mahasiswa.nama.like(pattern),
                Mahasiswa.email.like(pattern),
                ProgramStudi.nama_prodi.like(pattern),
            )
        )
    if id_prodi:
        query = query.filter(Mahasiswa.id_prodi == id_prodi)
    if angkatan:
        query = query.filter(Mahasiswa.angkatan == angkatan)
    if status:
        query = query.filter(Mahasiswa.status_mahasiswa == status)
    return query


def get_all_mahasiswa(
    db: Session,
    search: Optional[str] = None,
    id_prodi: Optional[int] = None,
    angkatan: Optional[int] = None,
    status: Optional[str] = None,
):
    query = _apply_filters(
        _base_query(db),
        search=search,
        id_prodi=id_prodi,
        angkatan=angkatan,
        status=status,
    )
    rows = query.order_by(Mahasiswa.id_mahasiswa.desc()).all()
    return [_serialize(row) for row in rows]


def get_mahasiswa_page(
    db: Session,
    search: Optional[str] = None,
    id_prodi: Optional[int] = None,
    angkatan: Optional[int] = None,
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
):
    page = max(page, 1)
    limit = min(max(limit, 1), 100)
    query = _apply_filters(
        _base_query(db),
        search=search,
        id_prodi=id_prodi,
        angkatan=angkatan,
        status=status,
    )
    total = query.count()
    rows = (
        query.order_by(Mahasiswa.id_mahasiswa.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "data": [_serialize(row) for row in rows],
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": ceil(total / limit) if total else 0,
    }


def get_mahasiswa(db: Session, mahasiswa_id: int):
    row = _base_query(db).filter(Mahasiswa.id_mahasiswa == mahasiswa_id).first()
    return _serialize(row) if row else None


def search_mahasiswa(db: Session, query: str):
    return get_all_mahasiswa(db, search=query)


def get_options(db: Session):
    prodi_rows = db.query(ProgramStudi).order_by(ProgramStudi.nama_prodi).all()
    angkatan_rows = (
        db.query(Mahasiswa.angkatan)
        .distinct()
        .order_by(Mahasiswa.angkatan.desc())
        .all()
    )
    status_rows = (
        db.query(Mahasiswa.status_mahasiswa)
        .distinct()
        .order_by(Mahasiswa.status_mahasiswa)
        .all()
    )

    return {
        "program_studi": [
            {
                "id_prodi": item.id_prodi,
                "nama_prodi": item.nama_prodi,
                "fakultas": item.fakultas,
            }
            for item in prodi_rows
        ],
        "angkatan": [int(row[0]) for row in angkatan_rows if row[0] is not None],
        "status": [row[0] for row in status_rows if row[0]],
    }


def nim_exists(db: Session, nim: str, exclude_id: Optional[int] = None):
    query = db.query(Mahasiswa).filter(Mahasiswa.nim == nim)
    if exclude_id:
        query = query.filter(Mahasiswa.id_mahasiswa != exclude_id)
    return query.first() is not None


def prodi_exists(db: Session, id_prodi: int):
    return db.query(ProgramStudi).filter(ProgramStudi.id_prodi == id_prodi).first() is not None


def create_mahasiswa(db: Session, data: MahasiswaCreate):
    mahasiswa = Mahasiswa(**data.model_dump())
    db.add(mahasiswa)
    db.commit()
    db.refresh(mahasiswa)
    return get_mahasiswa(db, mahasiswa.id_mahasiswa)


def update_mahasiswa(db: Session, mahasiswa_id: int, data: MahasiswaUpdate):
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id_mahasiswa == mahasiswa_id).first()
    if not mahasiswa:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(mahasiswa, field, value)

    db.commit()
    db.refresh(mahasiswa)
    return get_mahasiswa(db, mahasiswa.id_mahasiswa)


def delete_mahasiswa(db: Session, mahasiswa_id: int):
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.id_mahasiswa == mahasiswa_id).first()
    if not mahasiswa:
        return False

    db.delete(mahasiswa)
    db.commit()
    return True
