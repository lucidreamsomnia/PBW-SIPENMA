from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class MataKuliah(Base):
	__tablename__ = "mata_kuliah"

	id_matakuliah = Column(Integer, primary_key=True, autoincrement=True)
	id_program_studi = Column(Integer, ForeignKey("program_studi.id_program_studi"), nullable=False)
	kode_mk = Column(String(20), unique=True, nullable=False, index=True)
	nama_matakuliah = Column(String(100), nullable=False)
	sks = Column(Integer, nullable=False)
	semester = Column(Integer, nullable=False)
	jenis_mk = Column(String(30), nullable=True)
	status_aktif = Column(Boolean, nullable=False, default=True)
	created_at = Column(DateTime, nullable=False, server_default=func.now())
	updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	program_studi = relationship("ProgramStudi", back_populates="matakuliah")
	kelas = relationship("Kelas", back_populates="matakuliah")
	komponen_nilai = relationship("KomponenNilai", back_populates="matakuliah")