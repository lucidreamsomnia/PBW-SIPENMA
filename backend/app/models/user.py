from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from app.database.base import Base


class User(Base):
	__tablename__ = "user"

	id_user = Column(Integer, primary_key=True, autoincrement=True)
	id_role = Column(Integer, ForeignKey("role.id_role"), nullable=False)
	username = Column(String(50), unique=True, nullable=False, index=True)
	email = Column(String(100), unique=True, nullable=False, index=True)
	password_hash = Column(String(255), nullable=False)
	status_aktif = Column(Boolean, nullable=False, default=True)
	created_at = Column(DateTime, nullable=False, server_default=func.now())
	updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

	role = relationship("Role", back_populates="users")
	dosen_profile = relationship("Dosen", back_populates="user", uselist=False)
	mahasiswa_profile = relationship("Mahasiswa", back_populates="user", uselist=False)
	audit_logs = relationship("AuditLog", back_populates="user")
	notifikasi = relationship("Notifikasi", back_populates="user")
