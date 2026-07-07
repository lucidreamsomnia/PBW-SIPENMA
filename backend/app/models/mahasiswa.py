from sqlalchemy import Column, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TIMESTAMP, YEAR
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base


class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    id_mahasiswa = Column(Integer, primary_key=True, autoincrement=True)
    nim = Column(String(20), nullable=False, unique=True)
    nama = Column(String(100), nullable=False)
    id_prodi = Column(
        Integer,
        ForeignKey("program_studi.id_prodi", onupdate="CASCADE"),
        nullable=False,
    )
    angkatan = Column(YEAR(4), nullable=False)
    jenis_kelamin = Column(ENUM("L", "P"), nullable=False)
    email = Column(String(100), nullable=True)
    no_hp = Column(String(20), nullable=True)
    alamat = Column(Text, nullable=True)
    status_mahasiswa = Column(
        ENUM("Aktif", "Cuti", "Lulus", "DO"),
        nullable=True,
        server_default=text("'Aktif'"),
    )
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    program_studi = relationship("ProgramStudi", back_populates="mahasiswa")
