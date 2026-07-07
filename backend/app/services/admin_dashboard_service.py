from sqlalchemy import text
from sqlalchemy.orm import Session


def _count_table(db: Session, table_name: str) -> int:
    return db.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar() or 0


def get_dashboard_data(db: Session):
    mahasiswa_status_rows = db.execute(
        text(
            """
            SELECT COALESCE(status_mahasiswa, 'Tidak diketahui') AS label, COUNT(*) AS total
            FROM mahasiswa
            GROUP BY status_mahasiswa
            ORDER BY total DESC
            """
        )
    ).mappings().all()

    pengguna_role_rows = db.execute(
        text(
            """
            SELECT r.nama_role AS label, COUNT(u.id_user) AS total
            FROM role r
            LEFT JOIN user u ON u.id_role = r.id_role
            GROUP BY r.id_role, r.nama_role
            ORDER BY r.id_role
            """
        )
    ).mappings().all()

    recent_rows = db.execute(
        text(
            """
            SELECT aktivitas, waktu
            FROM audit_log
            ORDER BY waktu DESC
            LIMIT 6
            """
        )
    ).mappings().all()

    return {
        "summary": {
            "total_mahasiswa": _count_table(db, "mahasiswa"),
            "total_matakuliah": _count_table(db, "mata_kuliah"),
            "total_pengguna": _count_table(db, "user"),
            "kelas_aktif": _count_table(db, "kelas"),
        },
        "mahasiswa_status": {
            "labels": [row["label"] for row in mahasiswa_status_rows],
            "values": [row["total"] for row in mahasiswa_status_rows],
        },
        "pengguna_role": {
            "labels": [row["label"] for row in pengguna_role_rows],
            "values": [row["total"] for row in pengguna_role_rows],
        },
        "recent_activities": [
            {"aktivitas": row["aktivitas"], "waktu": row["waktu"]}
            for row in recent_rows
        ],
    }
