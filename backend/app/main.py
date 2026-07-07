# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import nilai, whatsapp, statistik, mahasiswa, matakuliah, admin_dashboard, pengguna

app = FastAPI(
    title="SIPENMA API",
    description="Backend service untuk pengelolaan nilai mahasiswa",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daftarkan semua route yang telah dibuat
app.include_router(nilai.router)
app.include_router(whatsapp.router)
app.include_router(statistik.router)
app.include_router(mahasiswa.router)
app.include_router(matakuliah.router)
app.include_router(pengguna.router)
app.include_router(admin_dashboard.router)

@app.get("/")
def root():
    return {"message": "Selamat datang di API SIPENMA aktif!"}
