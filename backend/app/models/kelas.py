from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base


class Kelas(Base):
    __tablename__ = "kelas"

    id_kelas = Column(Integer, primary_key=True, autoincrement=True)
    id_matakuliah = Column(Integer, ForeignKey("mata_kuliah.id_matakuliah"), nullable=False)
    id_dosen = Column(Integer, ForeignKey("dosen.id_dosen"), nullable=False)
    id_tahun_ajaran = Column(Integer, ForeignKey("tahun_ajaran.id_tahun_ajaran"), nullable=False)
    kode_kelas = Column(String(20), nullable=False, index=True)
    nama_kelas = Column(String(100), nullable=False)
    kapasitas = Column(Integer, nullable=True)
    jadwal_hari = Column(String(20), nullable=True)
    jadwal_jam = Column(String(20), nullable=True)
    ruangan = Column(String(50), nullable=True)
    status_aktif = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    matakuliah = relationship("MataKuliah", back_populates="kelas")
    dosen = relationship("Dosen", back_populates="kelas_ajar")
    tahun_ajaran = relationship("TahunAjaran", back_populates="kelas")
    krs = relationship("KRS", back_populates="kelas")