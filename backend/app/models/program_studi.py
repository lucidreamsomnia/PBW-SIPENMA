from sqlalchemy import Column, Integer, String, text
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.orm import relationship

from backend.app.database.connection import Base


class ProgramStudi(Base):
    __tablename__ = "program_studi"

    id_prodi = Column(Integer, primary_key=True, autoincrement=True)
    nama_prodi = Column(String(100), nullable=False)
    fakultas = Column(String(100), nullable=False)
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

    mahasiswa = relationship("Mahasiswa", back_populates="program_studi")
