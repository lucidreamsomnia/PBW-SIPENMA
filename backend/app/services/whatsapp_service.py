# backend/app/services/whatsapp_service.py
def send_whatsapp_notification(phone_number: str, message: str):
    # Logika integrasi API WhatsApp Gateway (misal: Fonnte/Wootils/dll)
    print(f"Mengirim pesan WA ke {phone_number}: {message}")
    return {"status": "success", "target": phone_number, "message": "Pesan terkirim (Simulasi)"}