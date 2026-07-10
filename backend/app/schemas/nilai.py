from pydantic import BaseModel
from typing import Optional


class NilaiBase(BaseModel):
    id_krs: int
    tugas: float
    uts: float
    uas: float


class NilaiCreate(NilaiBase):
    pass


class NilaiUpdate(BaseModel):
    tugas: Optional[float] = None
    uts: Optional[float] = None
    uas: Optional[float] = None


class NilaiResponse(BaseModel):
    id_nilai: int
    id_krs: int
    nilai_akhir: float
    grade: str

    class Config:
        from_attributes = True