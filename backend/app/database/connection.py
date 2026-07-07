# backend/app/database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SESUAIKAN DENGAN XAMPP ANDA: mysql+pymysql://username:password@localhost:port/nama_database
# Default XAMPP biasanya username="root", password="", db="sipenma"
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/sipenma"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency untuk route FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()