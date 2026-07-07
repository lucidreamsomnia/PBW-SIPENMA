from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base


class TahunAjaran(Base):
    __tablename__ = "tahun_ajaran"

    id_tahun_ajaran = Column(Integer, primary_key=True, autoincrement=True)
    tahun_ajaran = Column(String(9), unique=True, nullable=False, index=True)
    semester = Column(String(20), nullable=False)
    tanggal_mulai = Column(Date, nullable=True)
    tanggal_selesai = Column(Date, nullable=True)
    status_aktif = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    kelas = relationship("Kelas", back_populates="tahun_ajaran")
    krs = relationship("KRS", back_populates="tahun_ajaran")