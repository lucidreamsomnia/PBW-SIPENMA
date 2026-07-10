from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.database.connection import get_db

router = APIRouter(prefix="/krs", tags=["KRS"])


@router.get("/options")
def get_krs_options(db: Session = Depends(get_db)):
	query = text(
		"""
		SELECT
			k.id_krs,
			k.id_mahasiswa,
			k.id_kelas,
			m.nim,
			m.nama AS nama_mahasiswa,
			mk.id_mk,
			mk.kode_mk,
			mk.nama_mk,
			kls.nama_kelas
		FROM krs k
		INNER JOIN mahasiswa m ON k.id_mahasiswa = m.id_mahasiswa
		INNER JOIN kelas kls ON k.id_kelas = kls.id_kelas
		INNER JOIN mata_kuliah mk ON kls.id_mk = mk.id_mk
		ORDER BY m.nim, mk.kode_mk
		"""
	)

	rows = db.execute(query).mappings().all()
	return [dict(row) for row in rows]
