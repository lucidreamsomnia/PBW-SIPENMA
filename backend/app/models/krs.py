from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base


class KRS(Base):
    __tablename__ = "krs"

    id_krs = Column(Integer, primary_key=True, autoincrement=True)
    id_mahasiswa = Column(Integer, ForeignKey("mahasiswa.id_mahasiswa"), nullable=False)
    id_kelas = Column(Integer, ForeignKey("kelas.id_kelas"), nullable=False)
    id_tahun_ajaran = Column(Integer, ForeignKey("tahun_ajaran.id_tahun_ajaran"), nullable=False)
    tanggal_krs = Column(DateTime, nullable=False, server_default=func.now())
    status_krs = Column(String(30), nullable=False, default="DIAJUKAN")
    catatan = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    mahasiswa = relationship("Mahasiswa", back_populates="krs")
    kelas = relationship("Kelas", back_populates="krs")
    tahun_ajaran = relationship("TahunAjaran", back_populates="krs")
    nilai = relationship("Nilai", back_populates="krs", uselist=False)