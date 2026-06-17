from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Sistem Informasi Nilai Mahasiswa API"
    }