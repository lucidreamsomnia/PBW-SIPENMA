from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, Text, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class DetailNilai(Base):
    __tablename__ = "detail_nilai"

    id_detail_nilai = Column(Integer, primary_key=True, autoincrement=True)
    id_nilai = Column(Integer, ForeignKey("nilai.id_nilai"), nullable=False)
    id_komponen_nilai = Column(Integer, ForeignKey("komponen_nilai.id_komponen_nilai"), nullable=False)
    skor = Column(Numeric(5, 2), nullable=False)
    catatan = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    nilai = relationship("Nilai", back_populates="detail_nilai")
    komponen_nilai = relationship("KomponenNilai", back_populates="detail_nilai")