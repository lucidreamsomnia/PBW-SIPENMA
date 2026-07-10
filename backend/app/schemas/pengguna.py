from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class RoleOption(BaseModel):
	id_role: int
	nama_role: str
	deskripsi: Optional[str] = None


class PenggunaStatusOption(BaseModel):
	value: bool
	label: str


class PenggunaBase(BaseModel):
	id_role: int
	username: str = Field(..., min_length=1, max_length=50)
	email: str = Field(..., min_length=1, max_length=100)
	status_aktif: bool = True


class PenggunaCreate(PenggunaBase):
	password: str = Field(..., min_length=6, max_length=255)


class PenggunaUpdate(BaseModel):
	id_role: Optional[int] = None
	username: Optional[str] = Field(None, min_length=1, max_length=50)
	email: Optional[str] = Field(None, min_length=1, max_length=100)
	password: Optional[str] = Field(None, min_length=6, max_length=255)
	status_aktif: Optional[bool] = None


class PenggunaResponse(PenggunaBase):
	id_user: int
	nama_role: Optional[str] = None
	deskripsi_role: Optional[str] = None
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True


class PenggunaPageResponse(BaseModel):
	data: List[PenggunaResponse]
	total: int
	page: int
	limit: int
	total_pages: int


class PenggunaOptionsResponse(BaseModel):
	roles: List[RoleOption]
	status: List[PenggunaStatusOption]