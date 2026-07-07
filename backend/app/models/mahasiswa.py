from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base


class Mahasiswa(Base):
	__tablename__ = "mahasiswa"

	id_mahasiswa = Column(Integer, primary_key=True, autoincrement=True)
	id_user = Column(Integer, ForeignKey("user.id_user"), nullable=False, unique=True)
	id_program_studi = Column(Integer, ForeignKey("program_studi.id_program_studi"), nullable=False)
	nim = Column(String(30), unique=True, nullable=False, index=True)
	nama_mahasiswa = Column(String(100), nullable=False)
	angkatan = Column(Integer, nullable=False)
	jenis_kelamin = Column(String(20), nullable=True)
	tempat_lahir = Column(String(100), nullable=True)
	tanggal_lahir = Column(Date, nullable=True)
	email = Column(String(100), nullable=True)
	no_telp = Column(String(20), nullable=True)
	alamat = Column(String(255), nullable=True)
	status_aktif = Column(Boolean, nullable=False, default=True)
	created_at = Column(DateTime, nullable=False, server_default=func.now())
	updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	user = relationship("User", back_populates="mahasiswa_profile")
	program_studi = relationship("ProgramStudi", back_populates="mahasiswas")
	krs = relationship("KRS", back_populates="mahasiswa")