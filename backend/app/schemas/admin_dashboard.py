from datetime import datetime
from typing import List

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_mahasiswa: int
    total_matakuliah: int
    total_pengguna: int
    kelas_aktif: int


class ChartData(BaseModel):
    labels: List[str]
    values: List[int]


class RecentActivity(BaseModel):
    aktivitas: str
    waktu: datetime


class AdminDashboardResponse(BaseModel):
    summary: DashboardSummary
    mahasiswa_status: ChartData
    pengguna_role: ChartData
    recent_activities: List[RecentActivity]
