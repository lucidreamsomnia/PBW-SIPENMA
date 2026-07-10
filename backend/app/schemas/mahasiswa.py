from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class MahasiswaBase(BaseModel):
    nim: str = Field(..., min_length=1, max_length=20)
    nama: str = Field(..., min_length=1, max_length=100)
    id_prodi: int
    angkatan: int
    jenis_kelamin: str = Field(..., pattern="^(L|P)$")
    email: Optional[str] = Field(None, max_length=100)
    no_hp: Optional[str] = Field(None, max_length=20)
    alamat: Optional[str] = None
    status_mahasiswa: Optional[str] = Field("Aktif", pattern="^(Aktif|Cuti|Lulus|DO)$")


class MahasiswaCreate(MahasiswaBase):
    pass


class MahasiswaUpdate(BaseModel):
    nim: Optional[str] = Field(None, min_length=1, max_length=20)
    nama: Optional[str] = Field(None, min_length=1, max_length=100)
    id_prodi: Optional[int] = None
    angkatan: Optional[int] = None
    jenis_kelamin: Optional[str] = Field(None, pattern="^(L|P)$")
    email: Optional[str] = Field(None, max_length=100)
    no_hp: Optional[str] = Field(None, max_length=20)
    alamat: Optional[str] = None
    status_mahasiswa: Optional[str] = Field(None, pattern="^(Aktif|Cuti|Lulus|DO)$")


class MahasiswaResponse(MahasiswaBase):
    id_mahasiswa: int
    nama_prodi: Optional[str] = None
    fakultas: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MahasiswaPageResponse(BaseModel):
    data: List[MahasiswaResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class ProgramStudiOption(BaseModel):
    id_prodi: int
    nama_prodi: str
    fakultas: str


class MahasiswaOptionsResponse(BaseModel):
    program_studi: List[ProgramStudiOption]
    angkatan: List[int]
    status: List[str]
