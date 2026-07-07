# backend/app/schemas/nilai.py
from pydantic import BaseModel
from typing import Optional

class NilaiBase(BaseModel):
    mahasiswa_id: int
    matakuliah_id: int
    tugas: float
    uts: float
    uas: float

class NilaiCreate(NilaiBase):
    pass

class NilaiUpdate(BaseModel):
    tugas: Optional[float] = None
    uts: Optional[float] = None
    uas: Optional[float] = None

class NilaiResponse(NilaiBase):
    id: int
    nilai_akhir: float
    grade: str

    class Config:
        from_attributes = True