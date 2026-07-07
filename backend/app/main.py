# backend/app/main.py
from fastapi import FastAPI
from backend.app.routes import nilai, whatsapp, statistik, mahasiswa, matakuliah

app = FastAPI(
    title="SIPENMA API - Sisi Dosen",
    description="Backend service untuk dosen dalam menginput nilai, statistik, dan mengirimkan notifikasi WhatsApp",
    version="2.0.0"
)

# Daftarkan semua route yang telah dibuat
app.include_router(nilai.router)
app.include_router(whatsapp.router)
app.include_router(statistik.router)
app.include_router(mahasiswa.router)
app.include_router(matakuliah.router)

@app.get("/")
def root():
    return {"message": "Selamat datang di API SIPENMA - Sisi Dosen aktif!"}