const API_BASE = 'http://127.0.0.1:8000';

const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

const state = {
    krsRows: [],
    mahasiswa: [],
    matakuliah: [],
};

function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function showAlert(type, message) {
    document.getElementById('alertBox').innerHTML = `
        <div class="alert alert-${type} py-2">${escapeHtml(message)}</div>
    `;
}

async function apiRequest(url, options = {}) {
    const res = await fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {}),
        },
    });

    if (res.status === 204) {
        return null;
    }

    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.detail || 'Terjadi kesalahan pada server');
    }

    return data;
}

function uniqueBy(items, keyFn) {
    const map = new Map();
    items.forEach((item) => {
        const key = keyFn(item);
        if (!map.has(key)) {
            map.set(key, item);
        }
    });
    return [...map.values()];
}

function renderMahasiswaOptions(items) {
    const select = document.getElementById('selectMahasiswa');
    const currentValue = select.value;
    select.innerHTML = '<option value="">-- Pilih Mahasiswa --</option>' +
        items.map((item) => (
            `<option value="${item.id_mahasiswa}">${item.nim} - ${item.nama_mahasiswa}</option>`
        )).join('');
    select.value = currentValue;
}

function renderMatkulOptions(items) {
    const select = document.getElementById('selectMatkul');
    const currentValue = select.value;

    select.innerHTML =
        '<option value="">-- Pilih Mata Kuliah --</option>' +
        items.map((item) => (
            `<option value="${item.id_mk}">${item.kode_mk} - ${item.nama_mk}</option>`
        )).join('');

    select.value = currentValue;
}

function applyFilters() {
    const searchMahasiswa = document.getElementById('searchMahasiswa').value.trim().toLowerCase();
    const searchMatkul = document.getElementById('searchMatkul').value.trim().toLowerCase();

    const filteredMahasiswa = state.mahasiswa.filter((item) => (
        !searchMahasiswa ||
        item.nim.toLowerCase().includes(searchMahasiswa) ||
        item.nama_mahasiswa.toLowerCase().includes(searchMahasiswa)
    ));

    const filteredMatkul = state.matakuliah.filter((item) => (
        !searchMatkul ||
        item.kode_mk.toLowerCase().includes(searchMatkul) ||
        item.nama_mk.toLowerCase().includes(searchMatkul)
    ));

    renderMahasiswaOptions(filteredMahasiswa);
    renderMatkulOptions(filteredMatkul);
}

async function loadKrsOptions() {
    const data = await apiRequest(`${API_BASE}/krs/options`);
    state.krsRows = data;
    state.mahasiswa = uniqueBy(data, (item) => item.id_mahasiswa);
    state.matakuliah = uniqueBy(data, (item) => item.id_mk);
    applyFilters();
}

function getSelectedKrs() {
    const idMahasiswa = parseInt(document.getElementById('selectMahasiswa').value, 10);
    const idMatakuliah = parseInt(document.getElementById('selectMatkul').value, 10);

    if (!idMahasiswa || !idMatakuliah) {
        return null;
    }

    return state.krsRows.find((item) => (
        item.id_mahasiswa === idMahasiswa && item.id_mk === idMatakuliah
    ));
}

document.getElementById('searchMahasiswa').addEventListener('input', applyFilters);
document.getElementById('searchMatkul').addEventListener('input', applyFilters);

document.getElementById('simpanBtn').addEventListener('click', async () => {
    const selectedKrs = getSelectedKrs();
    const tugas = parseFloat(document.getElementById('nilaiTugas').value);
    const uts = parseFloat(document.getElementById('nilaiUTS').value);
    const uas = parseFloat(document.getElementById('nilaiUAS').value);

    if (!selectedKrs) {
        showAlert('warning', 'Pilih mahasiswa dan mata kuliah terlebih dahulu.');
        return;
    }

    if ([tugas, uts, uas].some((value) => Number.isNaN(value))) {
        showAlert('warning', 'Nilai tugas, UTS, dan UAS harus diisi.');
        return;
    }

    try {
        await apiRequest(`${API_BASE}/nilai/`, {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
            body: JSON.stringify({
                id_krs: selectedKrs.id_krs,
                tugas,
                uts,
                uas,
            }),
        });

        showAlert('success', 'Nilai berhasil disimpan.');
        document.getElementById('nilaiTugas').value = 0;
        document.getElementById('nilaiUTS').value = 0;
        document.getElementById('nilaiUAS').value = 0;
    } catch (err) {
        showAlert('danger', err.message);
    }
});

loadKrsOptions().catch((err) => {
    showAlert('danger', err.message);
});
