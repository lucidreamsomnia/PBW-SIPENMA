from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.schemas.admin_dashboard import AdminDashboardResponse
from backend.app.services import admin_dashboard_service

router = APIRouter(prefix="/admin/dashboard", tags=["Dashboard (Admin)"])


@router.get("/", response_model=AdminDashboardResponse)
def read_admin_dashboard(db: Session = Depends(get_db)):
    return admin_dashboard_service.get_dashboard_data(db)
