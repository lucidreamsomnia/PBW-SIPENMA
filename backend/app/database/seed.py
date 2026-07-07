from datetime import date

from app.database.session import SessionLocal
from app.models import (
	Dosen,
	Grade,
	Mahasiswa,
	MataKuliah,
	ProgramStudi,
	Role,
	TahunAjaran,
	User,
)


def get_or_create(session, model, defaults=None, **filters):
	instance = session.query(model).filter_by(**filters).first()
	if instance is not None:
		return instance, False

	params = dict(defaults or {})
	params.update(filters)
	instance = model(**params)
	session.add(instance)
	session.flush()
	return instance, True


def seed_data() -> None:
	session = SessionLocal()
	try:
		admin_role, _ = get_or_create(session, Role, nama_role="ADMIN", defaults={"deskripsi": "Administrator sistem"})
		dosen_role, _ = get_or_create(session, Role, nama_role="DOSEN", defaults={"deskripsi": "Dosen pengajar"})
		mahasiswa_role, _ = get_or_create(session, Role, nama_role="MAHASISWA", defaults={"deskripsi": "Mahasiswa aktif"})

		admin_user, _ = get_or_create(
			session,
			User,
			username="admin",
			defaults={
				"id_role": admin_role.id_role,
				"email": "admin@sipenma.local",
				"password_hash": "admin123",
				"status_aktif": True,
			},
		)

		informatika, _ = get_or_create(
			session,
			ProgramStudi,
			kode_program_studi="IF",
			defaults={
				"nama_program_studi": "Informatika",
				"jenjang": "S1",
				"fakultas": "Fakultas Ilmu Komputer",
				"status_aktif": True,
			},
		)
		sistem_informasi, _ = get_or_create(
			session,
			ProgramStudi,
			kode_program_studi="SI",
			defaults={
				"nama_program_studi": "Sistem Informasi",
				"jenjang": "S1",
				"fakultas": "Fakultas Ilmu Komputer",
				"status_aktif": True,
			},
		)

		dosen_users = [
			{
				"username": "dosen.andi",
				"email": "andi@sipenma.local",
				"password_hash": "dosen123",
				"nidn": "1122334455",
				"nama_dosen": "Andi Pratama",
				"gelar_depan": "Dr.",
				"gelar_belakang": "M.Kom",
				"id_program_studi": informatika.id_program_studi,
			},
			{
				"username": "dosen.sari",
				"email": "sari@sipenma.local",
				"password_hash": "dosen123",
				"nidn": "2233445566",
				"nama_dosen": "Sari Wulandari",
				"gelar_depan": None,
				"gelar_belakang": "S.T., M.T.",
				"id_program_studi": sistem_informasi.id_program_studi,
			},
		]

		for dosen_data in dosen_users:
			user, _ = get_or_create(
				session,
				User,
				username=dosen_data["username"],
				defaults={
					"id_role": dosen_role.id_role,
					"email": dosen_data["email"],
					"password_hash": dosen_data["password_hash"],
					"status_aktif": True,
				},
			)
			get_or_create(
				session,
				Dosen,
				nidn=dosen_data["nidn"],
				defaults={
					"id_user": user.id_user,
					"id_program_studi": dosen_data["id_program_studi"],
					"nama_dosen": dosen_data["nama_dosen"],
					"gelar_depan": dosen_data["gelar_depan"],
					"gelar_belakang": dosen_data["gelar_belakang"],
					"email": dosen_data["email"],
					"status_aktif": True,
				},
			)

		mahasiswa_users = [
			{
				"username": "mhs.budi",
				"email": "budi@sipenma.local",
				"password_hash": "mhs123",
				"nim": "2310001",
				"nama_mahasiswa": "Budi Santoso",
				"angkatan": 2023,
				"jenis_kelamin": "Laki-laki",
				"tempat_lahir": "Bandung",
				"tanggal_lahir": date(2005, 1, 15),
				"id_program_studi": informatika.id_program_studi,
			},
			{
				"username": "mhs.nina",
				"email": "nina@sipenma.local",
				"password_hash": "mhs123",
				"nim": "2310002",
				"nama_mahasiswa": "Nina Aulia",
				"angkatan": 2023,
				"jenis_kelamin": "Perempuan",
				"tempat_lahir": "Jakarta",
				"tanggal_lahir": date(2005, 4, 21),
				"id_program_studi": sistem_informasi.id_program_studi,
			},
			{
				"username": "mhs.rizky",
				"email": "rizky@sipenma.local",
				"password_hash": "mhs123",
				"nim": "2310003",
				"nama_mahasiswa": "Rizky Hidayat",
				"angkatan": 2022,
				"jenis_kelamin": "Laki-laki",
				"tempat_lahir": "Surabaya",
				"tanggal_lahir": date(2004, 9, 9),
				"id_program_studi": informatika.id_program_studi,
			},
		]

		for mahasiswa_data in mahasiswa_users:
			user, _ = get_or_create(
				session,
				User,
				username=mahasiswa_data["username"],
				defaults={
					"id_role": mahasiswa_role.id_role,
					"email": mahasiswa_data["email"],
					"password_hash": mahasiswa_data["password_hash"],
					"status_aktif": True,
				},
			)
			get_or_create(
				session,
				Mahasiswa,
				nim=mahasiswa_data["nim"],
				defaults={
					"id_user": user.id_user,
					"id_program_studi": mahasiswa_data["id_program_studi"],
					"nama_mahasiswa": mahasiswa_data["nama_mahasiswa"],
					"angkatan": mahasiswa_data["angkatan"],
					"jenis_kelamin": mahasiswa_data["jenis_kelamin"],
					"tempat_lahir": mahasiswa_data["tempat_lahir"],
					"tanggal_lahir": mahasiswa_data["tanggal_lahir"],
					"email": mahasiswa_data["email"],
					"status_aktif": True,
				},
			)

		tahun_ajaran_2024, _ = get_or_create(
			session,
			TahunAjaran,
			tahun_ajaran="2024/2025",
			defaults={
				"semester": "Ganjil",
				"tanggal_mulai": date(2024, 8, 1),
				"tanggal_selesai": date(2025, 1, 31),
				"status_aktif": True,
			},
		)
		tahun_ajaran_2025, _ = get_or_create(
			session,
			TahunAjaran,
			tahun_ajaran="2025/2026",
			defaults={
				"semester": "Ganjil",
				"tanggal_mulai": date(2025, 8, 1),
				"tanggal_selesai": date(2026, 1, 31),
				"status_aktif": True,
			},
		)

		courses = [
			{
				"kode_mk": "IF101",
				"nama_matakuliah": "Pemrograman Dasar",
				"sks": 3,
				"semester": 1,
				"jenis_mk": "Wajib",
				"id_program_studi": informatika.id_program_studi,
			},
			{
				"kode_mk": "IF201",
				"nama_matakuliah": "Struktur Data",
				"sks": 3,
				"semester": 3,
				"jenis_mk": "Wajib",
				"id_program_studi": informatika.id_program_studi,
			},
			{
				"kode_mk": "SI101",
				"nama_matakuliah": "Pengantar Sistem Informasi",
				"sks": 3,
				"semester": 1,
				"jenis_mk": "Wajib",
				"id_program_studi": sistem_informasi.id_program_studi,
			},
			{
				"kode_mk": "SI202",
				"nama_matakuliah": "Analisis dan Perancangan Sistem",
				"sks": 3,
				"semester": 4,
				"jenis_mk": "Wajib",
				"id_program_studi": sistem_informasi.id_program_studi,
			},
		]

		for course_data in courses:
			get_or_create(
				session,
				MataKuliah,
				kode_mk=course_data["kode_mk"],
				defaults={
					"id_program_studi": course_data["id_program_studi"],
					"nama_matakuliah": course_data["nama_matakuliah"],
					"sks": course_data["sks"],
					"semester": course_data["semester"],
					"jenis_mk": course_data["jenis_mk"],
					"status_aktif": True,
				},
			)

		grades = [
			("A", 85, 100, 4.00, "Sangat Baik"),
			("AB", 80, 84, 3.50, "Baik Sekali"),
			("B", 70, 79, 3.00, "Baik"),
			("BC", 65, 69, 2.50, "Lebih dari Cukup"),
			("C", 60, 64, 2.00, "Cukup"),
			("D", 50, 59, 1.00, "Kurang"),
			("E", 0, 49, 0.00, "Sangat Kurang"),
		]

		for kode_grade, nilai_min, nilai_max, bobot, keterangan in grades:
			get_or_create(
				session,
				Grade,
				kode_grade=kode_grade,
				defaults={
					"nilai_min": nilai_min,
					"nilai_max": nilai_max,
					"bobot": bobot,
					"keterangan": keterangan,
				},
			)

		session.commit()
		print("Seed data inserted successfully.")
	except Exception:
		session.rollback()
		raise
	finally:
		session.close()


if __name__ == "__main__":
	seed_data()
