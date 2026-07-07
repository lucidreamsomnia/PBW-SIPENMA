from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class ProgramStudi(Base):
    __tablename__ = "program_studi"

    id_program_studi = Column(Integer, primary_key=True, autoincrement=True)
    kode_program_studi = Column(String(20), unique=True, nullable=False, index=True)
    nama_program_studi = Column(String(100), nullable=False)
    jenjang = Column(String(10), nullable=False)
    fakultas = Column(String(100), nullable=True)
    status_aktif = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    dosens = relationship("Dosen", back_populates="program_studi")
    mahasiswas = relationship("Mahasiswa", back_populates="program_studi")
    matakuliah = relationship("MataKuliah", back_populates="program_studi")