from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base


class KomponenNilai(Base):
    __tablename__ = "komponen_nilai"

    id_komponen_nilai = Column(Integer, primary_key=True, autoincrement=True)
    id_matakuliah = Column(Integer, ForeignKey("mata_kuliah.id_matakuliah"), nullable=False)
    nama_komponen = Column(String(100), nullable=False)
    bobot = Column(Numeric(5, 2), nullable=False)
    urutan = Column(Integer, nullable=False, default=1)
    status_aktif = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    matakuliah = relationship("MataKuliah", back_populates="komponen_nilai")
    detail_nilai = relationship("DetailNilai", back_populates="komponen_nilai")