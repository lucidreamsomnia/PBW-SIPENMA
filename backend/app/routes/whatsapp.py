# backend/app/routes/whatsapp.py
from fastapi import APIRouter
from backend.app.services import whatsapp_service
from pydantic import BaseModel

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp Notification (Dosen)"])

class WAData(BaseModel):
    phone_number: str
    message: str

@router.post("/send")
def send_notification(data: WAData):
    return whatsapp_service.send_whatsapp_notification(data.phone_number, data.message)