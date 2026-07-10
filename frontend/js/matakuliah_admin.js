const API_BASE = 'http://127.0.0.1:8000';
const PAGE_SIZE = 10;

const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

let currentPage = 1;
let matkulData = [];
let selectedDeleteId = null;

const matkulModal = new bootstrap.Modal(document.getElementById('matkulModal'));
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
    const semester = document.getElementById('filterSemester').value;
    const status = document.getElementById('filterStatus').value;

    if (search) params.append('search', search);
    if (semester) params.append('semester', semester);
    if (status) params.append('status_mk', status);

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
    const table = document.getElementById('matkulTable');
    table.innerHTML = rows.map(m => `
        <tr>
            <td>${m.kode_mk}</td>
            <td>${m.nama_mk}</td>
            <td>${m.sks}</td>
            <td>${m.semester_rekomendasi || '-'}</td>
            <td><span class="badge bg-primary">${m.status_mk || '-'}</span></td>
            <td class="text-end">
                <button class="btn btn-sm btn-light me-1" onclick="openEditModal(${m.id_mk})" title="Edit">
                    <i class="bi bi-pencil-square"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="openDeleteModal(${m.id_mk})" title="Hapus">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
    `).join('') || '<tr><td colspan="6" class="text-center text-muted py-3">Tidak ada data</td></tr>';
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

async function loadMatkul() {
    try {
        const data = await apiRequest(`${API_BASE}/matakuliah/page?${getQueryParams()}`);
        matkulData = data.data;
        renderTable(data.data);
        renderPagination(data.total_pages);
    } catch (err) {
        renderTable([]);
        renderPagination(0);
        showAlert('danger', err.message);
    }
}

async function loadOptions() {
    const data = await apiRequest(`${API_BASE}/matakuliah/options`);

    document.getElementById('filterSemester').innerHTML = '<option value="">Semua Semester</option>' +
        data.semester.map(s => `<option value="${s}">Semester ${s}</option>`).join('');

    document.getElementById('filterStatus').innerHTML = '<option value="">Semua Status</option>' +
        data.status.map(s => `<option value="${s}">${s}</option>`).join('');
}

function resetForm() {
    document.getElementById('matkulForm').reset();
    document.getElementById('inputId').value = '';
    document.getElementById('inputSks').value = 3;
    document.getElementById('inputStatus').value = 'Aktif';
}

function openAddModal() {
    resetForm();
    document.getElementById('modalTitle').textContent = 'Tambah Mata Kuliah';
    matkulModal.show();
}

function openEditModal(id) {
    const m = matkulData.find(item => item.id_mk === id);
    if (!m) return;

    document.getElementById('modalTitle').textContent = 'Edit Mata Kuliah';
    document.getElementById('inputId').value = m.id_mk;
    document.getElementById('inputKode').value = m.kode_mk;
    document.getElementById('inputNama').value = m.nama_mk;
    document.getElementById('inputSks').value = m.sks;
    document.getElementById('inputSemester').value = m.semester_rekomendasi || '';
    document.getElementById('inputStatus').value = m.status_mk || 'Aktif';
    matkulModal.show();
}

function openDeleteModal(id) {
    const m = matkulData.find(item => item.id_mk === id);
    if (!m) return;

    selectedDeleteId = id;
    document.getElementById('deleteName').textContent = `${m.nama_mk} (${m.kode_mk})`;
    deleteModal.show();
}

function getFormPayload() {
    const semester = document.getElementById('inputSemester').value;

    return {
        kode_mk: document.getElementById('inputKode').value.trim(),
        nama_mk: document.getElementById('inputNama').value.trim(),
        sks: parseInt(document.getElementById('inputSks').value, 10),
        semester_rekomendasi: semester ? parseInt(semester, 10) : null,
        status_mk: document.getElementById('inputStatus').value
    };
}

async function saveMatkul(e) {
    e.preventDefault();
    const id = document.getElementById('inputId').value;
    const payload = getFormPayload();
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_BASE}/matakuliah/${id}` : `${API_BASE}/matakuliah/`;

    try {
        await apiRequest(url, {
            method,
            body: JSON.stringify(payload)
        });
        matkulModal.hide();
        showAlert('success', id ? 'Data mata kuliah berhasil diperbarui.' : 'Data mata kuliah berhasil ditambahkan.');
        await loadOptions();
        await loadMatkul();
    } catch (err) {
        showAlert('danger', err.message);
    }
}

async function deleteMatkul() {
    if (!selectedDeleteId) return;

    try {
        await apiRequest(`${API_BASE}/matakuliah/${selectedDeleteId}`, { method: 'DELETE' });
        deleteModal.hide();
        selectedDeleteId = null;
        showAlert('success', 'Data mata kuliah berhasil dihapus.');
        await loadOptions();
        await loadMatkul();
    } catch (err) {
        showAlert('danger', err.message);
    }
}

function goPage(page) {
    currentPage = page;
    loadMatkul();
}

function applyFilters() {
    currentPage = 1;
    loadMatkul();
}

document.getElementById('addBtn').addEventListener('click', openAddModal);
document.getElementById('matkulForm').addEventListener('submit', saveMatkul);
document.getElementById('confirmDeleteBtn').addEventListener('click', deleteMatkul);
document.getElementById('searchInput').addEventListener('input', applyFilters);
document.getElementById('filterSemester').addEventListener('change', applyFilters);
document.getElementById('filterStatus').addEventListener('change', applyFilters);

loadOptions()
    .then(loadMatkul)
    .catch(err => showAlert('danger', err.message));
