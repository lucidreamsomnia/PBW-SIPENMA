# backend/app/database/base.py
from backend.app.database.connection import Base
# Impor semua model di sini agar terdeteksi oleh Alembic / init_db
from backend.app.models.nilai import Nilai