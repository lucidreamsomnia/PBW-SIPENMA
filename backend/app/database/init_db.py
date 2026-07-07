# backend/app/database/init_db.py
from backend.app.database.connection import engine, Base
import backend.app.database.base # Memastikan semua model ter-load

def init_db():
    print("Inisialisasi database dan pembuatan tabel...")
    Base.metadata.create_all(bind=engine)
    print("Tabel berhasil dibuat!")

if __name__ == "__main__":
    init_db()