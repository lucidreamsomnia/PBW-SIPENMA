const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

const sampleData = [
    { nim: '2021001', nama: 'Ahmad Fauzi',    jurusan: 'Teknik Informatika', angkatan: 2021, email: 'ahmad@email.com' },
    { nim: '2021002', nama: 'Siti Nurhaliza', jurusan: 'Sistem Informasi',   angkatan: 2021, email: 'siti@email.com' },
    { nim: '2021003', nama: 'Budi Santoso',   jurusan: 'Teknik Informatika', angkatan: 2021, email: 'budi@email.com' },
    { nim: '2022001', nama: 'Dewi Lestari',   jurusan: 'Teknik Komputer',    angkatan: 2022, email: 'dewi@email.com' },
    { nim: '2022002', nama: 'Rizky Ramadhan', jurusan: 'Sistem Informasi',   angkatan: 2022, email: 'rizky@email.com' },
    { nim: '2022003', nama: 'Andi Pratama',   jurusan: 'Teknik Informatika', angkatan: 2022, email: 'andi@email.com' },
    { nim: '2023001', nama: 'Rina Wulandari', jurusan: 'Sistem Informasi',   angkatan: 2023, email: 'rina@email.com' },
    { nim: '2023002', nama: 'Fajar Nugroho',  jurusan: 'Teknik Komputer',    angkatan: 2023, email: 'fajar@email.com' },
];

const PAGE_SIZE = 5;
let currentPage = 1;
let filtered = [...sampleData];

function renderTable() {
    const start = (currentPage - 1) * PAGE_SIZE;
    const rows = filtered.slice(start, start + PAGE_SIZE);
    document.getElementById('mahasiswaTable').innerHTML = rows.map(m => `
        <tr>
            <td>${m.nim}</td>
            <td>${m.nama}</td>
            <td>${m.jurusan}</td>
            <td>${m.angkatan}</td>
            <td>${m.email}</td>
        </tr>
    `).join('') || '<tr><td colspan="5" class="text-center text-muted py-3">Tidak ada data</td></tr>';
}

function renderPagination() {
    const total = Math.ceil(filtered.length / PAGE_SIZE);
    let html = '';
    for (let i = 1; i <= total; i++) {
        html += `<li class="page-item ${i === currentPage ? 'active' : ''}">
            <button class="page-link" onclick="goPage(${i})">${i}</button>
        </li>`;
    }
    document.getElementById('pagination').innerHTML = html;
}

function goPage(p) {
    currentPage = p;
    renderTable();
    renderPagination();
}

document.getElementById('searchInput').addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    filtered = sampleData.filter(m =>
        m.nim.includes(q) || m.nama.toLowerCase().includes(q) || m.jurusan.toLowerCase().includes(q)
    );
    currentPage = 1;
    renderTable();
    renderPagination();
});

renderTable();
renderPagination();
