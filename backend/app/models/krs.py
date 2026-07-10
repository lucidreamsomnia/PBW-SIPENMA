from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base


class KRS(Base):
    __tablename__ = "krs"

    id_krs = Column(Integer, primary_key=True, autoincrement=True)

    id_mahasiswa = Column(
        Integer,
        ForeignKey("mahasiswa.id_mahasiswa"),
        nullable=False
    )

    id_kelas = Column(
        Integer,
        ForeignKey("kelas.id_kelas"),
        nullable=False
    )

    mahasiswa = relationship("Mahasiswa", back_populates="krs")
    kelas = relationship("Kelas", back_populates="krs")
    nilai = relationship("Nilai", back_populates="krs", uselist=False)