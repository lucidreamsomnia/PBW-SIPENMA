from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Dosen(Base):
	__tablename__ = "dosen"

	id_dosen = Column(Integer, primary_key=True, autoincrement=True)
	id_user = Column(Integer, ForeignKey("user.id_user"), nullable=False, unique=True)
	id_program_studi = Column(Integer, ForeignKey("program_studi.id_program_studi"), nullable=False)
	nidn = Column(String(30), unique=True, nullable=False, index=True)
	nama_dosen = Column(String(100), nullable=False)
	gelar_depan = Column(String(50), nullable=True)
	gelar_belakang = Column(String(50), nullable=True)
	email = Column(String(100), nullable=True)
	no_telp = Column(String(20), nullable=True)
	alamat = Column(String(255), nullable=True)
	status_aktif = Column(Boolean, nullable=False, default=True)
	created_at = Column(DateTime, nullable=False, server_default=func.now())
	updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	user = relationship("User", back_populates="dosen_profile")
	program_studi = relationship("ProgramStudi", back_populates="dosens")
	kelas_ajar = relationship("Kelas", back_populates="dosen")