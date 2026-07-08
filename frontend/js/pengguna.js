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
let penggunaData = [];
let selectedDeleteId = null;

const penggunaModal = new bootstrap.Modal(document.getElementById('penggunaModal'));
const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));

function showAlert(type, message) {
    document.getElementById('alertBox').innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show py-2" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

function formatDate(value) {
    if (!value) return '-';
    return new Date(value).toLocaleString('id-ID', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getQueryParams() {
    const params = new URLSearchParams({
        page: currentPage,
        limit: PAGE_SIZE
    });

    const search = document.getElementById('searchInput').value.trim();
    const idRole = document.getElementById('filterRole').value;
    const status = document.getElementById('filterStatus').value;

    if (search) params.append('search', search);
    if (idRole) params.append('id_role', idRole);
    if (status !== '') params.append('status_aktif', status);

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
    const table = document.getElementById('penggunaTable');
    table.innerHTML = rows.map(p => `
        <tr>
            <td>${p.username}</td>
            <td>${p.email}</td>
            <td>${p.nama_role || '-'}</td>
            <td>
                <span class="badge ${p.status_aktif ? 'bg-success' : 'bg-secondary'}">
                    ${p.status_aktif ? 'Aktif' : 'Nonaktif'}
                </span>
            </td>
            <td>${formatDate(p.created_at)}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-light me-1" onclick="openEditModal(${p.id_user})" title="Edit">
                    <i class="bi bi-pencil-square"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="openDeleteModal(${p.id_user})" title="Hapus">
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

async function loadPengguna() {
    try {
        const data = await apiRequest(`${API_BASE}/pengguna/page?${getQueryParams()}`);
        penggunaData = data.data;
        renderTable(data.data);
        renderPagination(data.total_pages);
    } catch (err) {
        renderTable([]);
        renderPagination(0);
        showAlert('danger', err.message);
    }
}

async function loadOptions() {
    const data = await apiRequest(`${API_BASE}/pengguna/options`);

    document.getElementById('filterRole').innerHTML = '<option value="">Semua Role</option>' +
        data.roles.map(role => `<option value="${role.id_role}">${role.nama_role}</option>`).join('');

    document.getElementById('filterStatus').innerHTML = '<option value="">Semua Status</option>' +
        data.status.map(item => `<option value="${item.value}">${item.label}</option>`).join('');

    document.getElementById('inputRole').innerHTML =
        '<option value="">Pilih Role</option>' +
        data.roles.map(role => `<option value="${role.id_role}">${role.nama_role}</option>`).join('');

    document.getElementById('inputStatus').innerHTML =
        data.status.map(item => `<option value="${item.value}">${item.label}</option>`).join('');
}

function resetForm() {
    document.getElementById('penggunaForm').reset();
    document.getElementById('inputId').value = '';
    document.getElementById('inputStatus').value = 'true';
    document.getElementById('inputPassword').value = '';
    document.getElementById('passwordHelp').textContent = 'Password wajib diisi saat membuat pengguna baru.';
}

function openAddModal() {
    resetForm();
    document.getElementById('modalTitle').textContent = 'Tambah Pengguna';
    penggunaModal.show();
}

function openEditModal(id) {
    const p = penggunaData.find(item => item.id_user === id);
    if (!p) return;

    document.getElementById('modalTitle').textContent = 'Edit Pengguna';
    document.getElementById('inputId').value = p.id_user;
    document.getElementById('inputUsername').value = p.username;
    document.getElementById('inputEmail').value = p.email;
    document.getElementById('inputRole').value = p.id_role;
    document.getElementById('inputStatus').value = String(p.status_aktif);
    document.getElementById('inputPassword').value = '';
    document.getElementById('passwordHelp').textContent = 'Kosongkan jika tidak ingin mengubah password.';
    penggunaModal.show();
}

function openDeleteModal(id) {
    const p = penggunaData.find(item => item.id_user === id);
    if (!p) return;

    selectedDeleteId = id;
    document.getElementById('deleteName').textContent = `${p.username} (${p.email})`;
    deleteModal.show();
}

function getFormPayload() {
    const password = document.getElementById('inputPassword').value.trim();

    return {
        username: document.getElementById('inputUsername').value.trim(),
        email: document.getElementById('inputEmail').value.trim(),
        id_role: parseInt(document.getElementById('inputRole').value, 10),
        status_aktif: document.getElementById('inputStatus').value === 'true',
        password: password || null
    };
}

async function savePengguna(e) {
    e.preventDefault();
    const id = document.getElementById('inputId').value;
    const payload = getFormPayload();

    if (!id && !payload.password) {
        showAlert('danger', 'Password wajib diisi saat membuat pengguna baru.');
        return;
    }

    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_BASE}/pengguna/${id}` : `${API_BASE}/pengguna/`;

    try {
        await apiRequest(url, {
            method,
            body: JSON.stringify(payload)
        });
        penggunaModal.hide();
        showAlert('success', id ? 'Data pengguna berhasil diperbarui.' : 'Data pengguna berhasil ditambahkan.');
        await loadOptions();
        await loadPengguna();
    } catch (err) {
        showAlert('danger', err.message);
    }
}

async function deletePengguna() {
    if (!selectedDeleteId) return;

    try {
        await apiRequest(`${API_BASE}/pengguna/${selectedDeleteId}`, { method: 'DELETE' });
        deleteModal.hide();
        selectedDeleteId = null;
        showAlert('success', 'Data pengguna berhasil dihapus.');
        await loadOptions();
        await loadPengguna();
    } catch (err) {
        showAlert('danger', err.message);
    }
}

function goPage(page) {
    currentPage = page;
    loadPengguna();
}

function applyFilters() {
    currentPage = 1;
    loadPengguna();
}

document.getElementById('addBtn').addEventListener('click', openAddModal);
document.getElementById('penggunaForm').addEventListener('submit', savePengguna);
document.getElementById('confirmDeleteBtn').addEventListener('click', deletePengguna);
document.getElementById('searchInput').addEventListener('input', applyFilters);
document.getElementById('filterRole').addEventListener('change', applyFilters);
document.getElementById('filterStatus').addEventListener('change', applyFilters);

loadOptions()
    .then(loadPengguna)
    .catch(err => showAlert('danger', err.message));