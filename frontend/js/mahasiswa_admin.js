const API_BASE = 'http://localhost:8000';
const PAGE_SIZE = 10;

const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

let currentPage = 1;
let mahasiswaData = [];
let optionsData = { program_studi: [], angkatan: [], status: [] };
let selectedDeleteId = null;

const mahasiswaModal = new bootstrap.Modal(document.getElementById('mahasiswaModal'));
const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));

function showAlert(type, message) {
    document.getElementById('alertBox').innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show py-2" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

function getQueryParams() {
    const params = new URLSearchParams({
        page: currentPage,
        limit: PAGE_SIZE
    });

    const search = document.getElementById('searchInput').value.trim();
    const idProdi = document.getElementById('filterProdi').value;
    const angkatan = document.getElementById('filterAngkatan').value;
    const status = document.getElementById('filterStatus').value;

    if (search) params.append('search', search);
    if (idProdi) params.append('id_prodi', idProdi);
    if (angkatan) params.append('angkatan', angkatan);
    if (status) params.append('status_mahasiswa', status);

    return params.toString();
}

async function apiRequest(url, options = {}) {
    const res = await fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        }
    });

    if (res.status === 204) return null;

    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.detail || 'Terjadi kesalahan pada server');
    }
    return data;
}

function renderTable(rows) {
    const table = document.getElementById('mahasiswaTable');
    table.innerHTML = rows.map(m => `
        <tr>
            <td>${m.nim}</td>
            <td>${m.nama}</td>
            <td>${m.nama_prodi || '-'}</td>
            <td>${m.angkatan}</td>
            <td>${m.email || '-'}</td>
            <td><span class="badge bg-primary">${m.status_mahasiswa || '-'}</span></td>
            <td class="text-end">
                <button class="btn btn-sm btn-light me-1" onclick="openEditModal(${m.id_mahasiswa})" title="Edit">
                    <i class="bi bi-pencil-square"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="openDeleteModal(${m.id_mahasiswa})" title="Hapus">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
    `).join('') || '<tr><td colspan="7" class="text-center text-muted py-3">Tidak ada data</td></tr>';
}

function renderPagination(totalPages) {
    let html = '';
    for (let i = 1; i <= totalPages; i++) {
        html += `<li class="page-item ${i === currentPage ? 'active' : ''}">
            <button class="page-link" onclick="goPage(${i})">${i}</button>
        </li>`;
    }
    document.getElementById('pagination').innerHTML = html;
}

async function loadMahasiswa() {
    try {
        const data = await apiRequest(`${API_BASE}/mahasiswa/page?${getQueryParams()}`);
        mahasiswaData = data.data;
        renderTable(data.data);
        renderPagination(data.total_pages);
    } catch (err) {
        renderTable([]);
        renderPagination(0);
        showAlert('danger', err.message);
    }
}

async function loadOptions() {
    const data = await apiRequest(`${API_BASE}/mahasiswa/options`);
    optionsData = data;

    document.getElementById('filterProdi').innerHTML = '<option value="">Semua Prodi</option>' +
        data.program_studi.map(p => `<option value="${p.id_prodi}">${p.nama_prodi}</option>`).join('');

    document.getElementById('filterAngkatan').innerHTML = '<option value="">Semua Angkatan</option>' +
        data.angkatan.map(a => `<option value="${a}">${a}</option>`).join('');

    document.getElementById('filterStatus').innerHTML = '<option value="">Semua Status</option>' +
        data.status.map(s => `<option value="${s}">${s}</option>`).join('');

    document.getElementById('inputProdi').innerHTML =
        data.program_studi.map(p => `<option value="${p.id_prodi}">${p.nama_prodi}</option>`).join('');
}

function resetForm() {
    document.getElementById('mahasiswaForm').reset();
    document.getElementById('inputId').value = '';
    document.getElementById('inputStatus').value = 'Aktif';
    document.getElementById('inputAngkatan').value = new Date().getFullYear();
}

function openAddModal() {
    resetForm();
    document.getElementById('modalTitle').textContent = 'Tambah Mahasiswa';
    mahasiswaModal.show();
}

function openEditModal(id) {
    const m = mahasiswaData.find(item => item.id_mahasiswa === id);
    if (!m) return;

    document.getElementById('modalTitle').textContent = 'Edit Mahasiswa';
    document.getElementById('inputId').value = m.id_mahasiswa;
    document.getElementById('inputNim').value = m.nim;
    document.getElementById('inputNama').value = m.nama;
    document.getElementById('inputProdi').value = m.id_prodi;
    document.getElementById('inputAngkatan').value = m.angkatan;
    document.getElementById('inputJenisKelamin').value = m.jenis_kelamin;
    document.getElementById('inputEmail').value = m.email || '';
    document.getElementById('inputNoHp').value = m.no_hp || '';
    document.getElementById('inputStatus').value = m.status_mahasiswa || 'Aktif';
    document.getElementById('inputAlamat').value = m.alamat || '';
    mahasiswaModal.show();
}

function openDeleteModal(id) {
    const m = mahasiswaData.find(item => item.id_mahasiswa === id);
    if (!m) return;

    selectedDeleteId = id;
    document.getElementById('deleteName').textContent = `${m.nama} (${m.nim})`;
    deleteModal.show();
}

function getFormPayload() {
    const email = document.getElementById('inputEmail').value.trim();
    const noHp = document.getElementById('inputNoHp').value.trim();
    const alamat = document.getElementById('inputAlamat').value.trim();

    return {
        nim: document.getElementById('inputNim').value.trim(),
        nama: document.getElementById('inputNama').value.trim(),
        id_prodi: parseInt(document.getElementById('inputProdi').value, 10),
        angkatan: parseInt(document.getElementById('inputAngkatan').value, 10),
        jenis_kelamin: document.getElementById('inputJenisKelamin').value,
        email: email || null,
        no_hp: noHp || null,
        alamat: alamat || null,
        status_mahasiswa: document.getElementById('inputStatus').value
    };
}

async function saveMahasiswa(e) {
    e.preventDefault();
    const id = document.getElementById('inputId').value;
    const payload = getFormPayload();
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_BASE}/mahasiswa/${id}` : `${API_BASE}/mahasiswa/`;

    try {
        await apiRequest(url, {
            method,
            body: JSON.stringify(payload)
        });
        mahasiswaModal.hide();
        showAlert('success', id ? 'Data mahasiswa berhasil diperbarui.' : 'Data mahasiswa berhasil ditambahkan.');
        await loadOptions();
        await loadMahasiswa();
    } catch (err) {
        showAlert('danger', err.message);
    }
}

async function deleteMahasiswa() {
    if (!selectedDeleteId) return;

    try {
        await apiRequest(`${API_BASE}/mahasiswa/${selectedDeleteId}`, { method: 'DELETE' });
        deleteModal.hide();
        selectedDeleteId = null;
        showAlert('success', 'Data mahasiswa berhasil dihapus.');
        await loadOptions();
        await loadMahasiswa();
    } catch (err) {
        showAlert('danger', err.message);
    }
}

function goPage(page) {
    currentPage = page;
    loadMahasiswa();
}

function applyFilters() {
    currentPage = 1;
    loadMahasiswa();
}

document.getElementById('addBtn').addEventListener('click', openAddModal);
document.getElementById('mahasiswaForm').addEventListener('submit', saveMahasiswa);
document.getElementById('confirmDeleteBtn').addEventListener('click', deleteMahasiswa);
document.getElementById('searchInput').addEventListener('input', applyFilters);
document.getElementById('filterProdi').addEventListener('change', applyFilters);
document.getElementById('filterAngkatan').addEventListener('change', applyFilters);
document.getElementById('filterStatus').addEventListener('change', applyFilters);

loadOptions()
    .then(loadMahasiswa)
    .catch(err => showAlert('danger', err.message));
