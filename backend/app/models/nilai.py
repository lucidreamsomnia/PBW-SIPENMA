# backend/app/models/nilai.py
from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from backend.app.database.connection import Base

class Nilai(Base):
    __tablename__ = "nilai"

    id_nilai = Column(Integer, primary_key=True, autoincrement=True)
    id_krs = Column(Integer, nullable=False)
    id_grade = Column(Integer, nullable=True)
    nilai_akhir = Column(Float, nullable=False)
    status_publish = Column(Boolean, default=False)