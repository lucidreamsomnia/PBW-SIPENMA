from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from app.database.base import Base


class Role(Base):
	__tablename__ = "role"

	id_role = Column(Integer, primary_key=True, autoincrement=True)
	nama_role = Column(String(30), unique=True, nullable=False, index=True)
	deskripsi = Column(String(255), nullable=True)
	created_at = Column(DateTime, nullable=False, server_default=func.now())
	updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	users = relationship("User", back_populates="role")
