const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

const sampleData = [
    { nim: '2021001', nama: 'Ahmad Fauzi',    matkul: 'Algoritma dan Pemrograman', tugas: 85, uts: 80, uas: 88 },
    { nim: '2021001', nama: 'Ahmad Fauzi',    matkul: 'Basis Data',                tugas: 90, uts: 85, uas: 92 },
    { nim: '2021002', nama: 'Siti Nurhaliza', matkul: 'Algoritma dan Pemrograman', tugas: 92, uts: 88, uas: 90 },
    { nim: '2021002', nama: 'Siti Nurhaliza', matkul: 'Jaringan Komputer',         tugas: 78, uts: 75, uas: 80 },
    { nim: '2021003', nama: 'Budi Santoso',   matkul: 'Pengembangan Web',          tugas: 88, uts: 82, uas: 85 },
    { nim: '2022001', nama: 'Dewi Lestari',   matkul: 'Basis Data',                tugas: 75, uts: 70, uas: 78 },
    { nim: '2022002', nama: 'Rizky Ramadhan', matkul: 'Pemrograman Mobile',        tugas: 82, uts: 80, uas: 85 },
];

function calcNilaiAkhir(d) {
    return (d.tugas * 0.3 + d.uts * 0.3 + d.uas * 0.4).toFixed(2);
}

function getGrade(n) {
    if (n >= 85) return { g: 'A',  cls: 'grade-a' };
    if (n >= 80) return { g: 'A-', cls: 'grade-a' };
    if (n >= 75) return { g: 'B+', cls: 'grade-b' };
    if (n >= 70) return { g: 'B',  cls: 'grade-b' };
    if (n >= 65) return { g: 'B-', cls: 'grade-b' };
    if (n >= 60) return { g: 'C+', cls: 'grade-c' };
    if (n >= 55) return { g: 'C',  cls: 'grade-c' };
    if (n >= 40) return { g: 'D',  cls: 'grade-d' };
    return { g: 'E', cls: 'grade-d' };
}

// Populate filter
const matkulSet = [...new Set(sampleData.map(d => d.matkul))];
const filterEl = document.getElementById('filterMatkul');
matkulSet.forEach(m => {
    filterEl.innerHTML += `<option value="${m}">${m}</option>`;
});

let filtered = [...sampleData];

function renderTable() {
    const rows = filtered.map(d => {
        const na = parseFloat(calcNilaiAkhir(d));
        const { g, cls } = getGrade(na);
        return `<tr>
            <td>${d.nim}</td>
            <td>${d.nama}</td>
            <td>${d.matkul}</td>
            <td>${d.tugas}</td>
            <td>${d.uts}</td>
            <td>${d.uas}</td>
            <td><strong>${na.toFixed(2)}</strong></td>
            <td><span class="grade-badge ${cls}">${g}</span></td>
        </tr>`;
    }).join('') || '<tr><td colspan="8" class="text-center text-muted py-3">Tidak ada data</td></tr>';

    document.getElementById('rekapTable').innerHTML = rows;

    const values = filtered.map(d => parseFloat(calcNilaiAkhir(d)));
    document.getElementById('sumTotal').textContent = filtered.length;
    document.getElementById('sumRata').textContent  = values.length ? (values.reduce((a,b)=>a+b,0)/values.length).toFixed(2) : '0';
    document.getElementById('sumMax').textContent   = values.length ? Math.max(...values).toFixed(2) : '0';
    document.getElementById('sumMin').textContent   = values.length ? Math.min(...values).toFixed(2) : '0';
}

function applyFilters() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    const mk = document.getElementById('filterMatkul').value;
    filtered = sampleData.filter(d =>
        (!q || d.nim.includes(q) || d.nama.toLowerCase().includes(q)) &&
        (!mk || d.matkul === mk)
    );
    renderTable();
}

document.getElementById('searchInput').addEventListener('input', applyFilters);
document.getElementById('filterMatkul').addEventListener('change', applyFilters);

document.getElementById('exportBtn').addEventListener('click', () => {
    const header = 'NIM,Nama,Mata Kuliah,Tugas,UTS,UAS,Nilai Akhir,Grade\n';
    const rows = filtered.map(d => {
        const na = parseFloat(calcNilaiAkhir(d));
        const { g } = getGrade(na);
        return `${d.nim},${d.nama},${d.matkul},${d.tugas},${d.uts},${d.uas},${na.toFixed(2)},${g}`;
    }).join('\n');
    const blob = new Blob([header + rows], { type: 'text/csv' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'rekap_nilai.csv';
    a.click();
});

renderTable();
