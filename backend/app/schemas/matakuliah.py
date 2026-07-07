from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class MataKuliahBase(BaseModel):
    kode_mk: str = Field(..., min_length=1, max_length=20)
    nama_mk: str = Field(..., min_length=1, max_length=120)
    sks: int = Field(..., ge=1, le=9)
    semester_rekomendasi: Optional[int] = Field(None, ge=1, le=14)
    status_mk: Optional[str] = Field("Aktif", pattern="^(Aktif|Nonaktif)$")


class MataKuliahCreate(MataKuliahBase):
    pass


class MataKuliahUpdate(BaseModel):
    kode_mk: Optional[str] = Field(None, min_length=1, max_length=20)
    nama_mk: Optional[str] = Field(None, min_length=1, max_length=120)
    sks: Optional[int] = Field(None, ge=1, le=9)
    semester_rekomendasi: Optional[int] = Field(None, ge=1, le=14)
    status_mk: Optional[str] = Field(None, pattern="^(Aktif|Nonaktif)$")


class MataKuliahResponse(MataKuliahBase):
    id_mk: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MataKuliahPageResponse(BaseModel):
    data: List[MataKuliahResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class MataKuliahOptionsResponse(BaseModel):
    semester: List[int]
    status: List[str]
