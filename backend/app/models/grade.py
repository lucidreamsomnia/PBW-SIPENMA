from sqlalchemy import Column, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Grade(Base):
    __tablename__ = "grade"

    id_grade = Column(Integer, primary_key=True, autoincrement=True)
    kode_grade = Column(String(5), unique=True, nullable=False, index=True)
    nilai_min = Column(Numeric(5, 2), nullable=False)
    nilai_max = Column(Numeric(5, 2), nullable=False)
    bobot = Column(Numeric(5, 2), nullable=False)
    keterangan = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    nilai = relationship("Nilai", back_populates="grade")