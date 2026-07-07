from sqlalchemy import Column, Integer, String, text
from sqlalchemy.dialects.mysql import ENUM, TIMESTAMP, TINYINT

from backend.app.database.connection import Base


class MataKuliah(Base):
    __tablename__ = "mata_kuliah"

    id_mk = Column(Integer, primary_key=True, autoincrement=True)
    kode_mk = Column(String(20), nullable=False, unique=True)
    nama_mk = Column(String(120), nullable=False)
    sks = Column(TINYINT, nullable=False)
    semester_rekomendasi = Column(TINYINT, nullable=True)
    status_mk = Column(
        ENUM("Aktif", "Nonaktif"),
        nullable=True,
        server_default=text("'Aktif'"),
    )
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )
