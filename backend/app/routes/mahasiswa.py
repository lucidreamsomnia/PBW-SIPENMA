# ==========================================================
# ADMIN SECTION
# (Dikerjakan oleh Bagian Admin)
# ==========================================================

@router.post("/")
def create_mahasiswa():
    ...

@router.put("/{id}")
def update_mahasiswa():
    ...

@router.delete("/{id}")
def delete_mahasiswa():
    ...



# ==========================================
# DOSEN SECTION
# ==========================================

@router.get("/")
def get_all_mahasiswa():
    ...

@router.get("/{id}")
def get_mahasiswa():
    ...