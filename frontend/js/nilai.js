const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

const mahasiswaList = [
    { nim: '2021001', nama: 'Ahmad Fauzi' },
    { nim: '2021002', nama: 'Siti Nurhaliza' },
    { nim: '2021003', nama: 'Budi Santoso' },
    { nim: '2022001', nama: 'Dewi Lestari' },
    { nim: '2022002', nama: 'Rizky Ramadhan' },
];

const matkulList = [
    { kode: 'IF101', nama: 'Algoritma dan Pemrograman' },
    { kode: 'IF102', nama: 'Basis Data' },
    { kode: 'IF103', nama: 'Jaringan Komputer' },
    { kode: 'IF104', nama: 'Pengembangan Web' },
    { kode: 'IF105', nama: 'Pemrograman Mobile' },
];

function populateSelect(selectEl, data, valueKey, labelFn) {
    selectEl.innerHTML = '<option value="">-- Pilih --</option>' +
        data.map(d => `<option value="${d[valueKey]}">${labelFn(d)}</option>`).join('');
}

populateSelect(document.getElementById('selectMahasiswa'), mahasiswaList, 'nim', d => `${d.nim} - ${d.nama}`);
populateSelect(document.getElementById('selectMatkul'), matkulList, 'kode', d => `${d.kode} - ${d.nama}`);

document.getElementById('searchMahasiswa').addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    const filtered = mahasiswaList.filter(m => m.nim.includes(q) || m.nama.toLowerCase().includes(q));
    populateSelect(document.getElementById('selectMahasiswa'), filtered, 'nim', d => `${d.nim} - ${d.nama}`);
});

document.getElementById('searchMatkul').addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    const filtered = matkulList.filter(m => m.kode.toLowerCase().includes(q) || m.nama.toLowerCase().includes(q));
    populateSelect(document.getElementById('selectMatkul'), filtered, 'kode', d => `${d.kode} - ${d.nama}`);
});

document.getElementById('simpanBtn').addEventListener('click', async () => {
    const nim = document.getElementById('selectMahasiswa').value;
    const kode_mk = document.getElementById('selectMatkul').value;
    const tugas = parseFloat(document.getElementById('nilaiTugas').value);
    const uts   = parseFloat(document.getElementById('nilaiUTS').value);
    const uas   = parseFloat(document.getElementById('nilaiUAS').value);
    const alertBox = document.getElementById('alertBox');

    if (!nim || !kode_mk) {
        alertBox.innerHTML = `<div class="alert alert-warning py-2">Pilih mahasiswa dan mata kuliah terlebih dahulu.</div>`;
        return;
    }

    const nilai_akhir = (tugas * 0.3 + uts * 0.3 + uas * 0.4).toFixed(2);

    try {
        const res = await fetch('http://localhost:8000/nilai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ nim, kode_mk, tugas, uts, uas, nilai_akhir: parseFloat(nilai_akhir) })
        });

        if (res.ok) {
            alertBox.innerHTML = `<div class="alert alert-success py-2">Nilai berhasil disimpan! Nilai Akhir: <strong>${nilai_akhir}</strong></div>`;
            document.getElementById('nilaiTugas').value = 0;
            document.getElementById('nilaiUTS').value = 0;
            document.getElementById('nilaiUAS').value = 0;
        } else {
            const data = await res.json();
            alertBox.innerHTML = `<div class="alert alert-danger py-2">${data.detail || 'Gagal menyimpan nilai.'}</div>`;
        }
    } catch {
        // Demo mode: show calculated result without backend
        alertBox.innerHTML = `<div class="alert alert-info py-2">Demo: Nilai Akhir = <strong>${nilai_akhir}</strong> (backend belum terhubung)</div>`;
    }
});
