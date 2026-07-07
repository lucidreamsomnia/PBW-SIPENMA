from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Nilai(Base):
    __tablename__ = "nilai"

    id_nilai = Column(Integer, primary_key=True, autoincrement=True)
    id_krs = Column(Integer, ForeignKey("krs.id_krs"), nullable=False, unique=True)
    id_grade = Column(Integer, ForeignKey("grade.id_grade"), nullable=False)
    nilai_akhir = Column(Numeric(5, 2), nullable=False)
    predikat = Column(String(20), nullable=True)
    catatan = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    krs = relationship("KRS", back_populates="nilai")
    grade = relationship("Grade", back_populates="nilai")
    detail_nilai = relationship("DetailNilai", back_populates="nilai")