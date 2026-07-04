const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

// Grade helper — 9-grade scale
function getGrade(n) {
    if (n >= 85)       return 'A';
    if (n >= 80)       return 'A-';
    if (n >= 75)       return 'B+';
    if (n >= 70)       return 'B';
    if (n >= 65)       return 'B-';
    if (n >= 60)       return 'C+';
    if (n >= 55)       return 'C';
    if (n >= 40)       return 'D';
    return 'E';
}

function getGradeBadge(n) {
    const g = getGrade(n);
    if (g === 'A')       return `<span class="badge bg-success">${g}</span>`;
    if (g === 'A-')      return `<span class="badge bg-success">${g}</span>`;
    if (g === 'B+')      return `<span class="badge bg-primary">${g}</span>`;
    if (g === 'B')       return `<span class="badge bg-primary">${g}</span>`;
    if (g === 'B-')      return `<span class="badge bg-primary">${g}</span>`;
    if (g === 'C+')      return `<span class="badge bg-warning text-dark">${g}</span>`;
    if (g === 'C')       return `<span class="badge bg-warning text-dark">${g}</span>`;
    if (g === 'D')       return `<span class="badge bg-danger">${g}</span>`;
    return `<span class="badge bg-secondary">${g}</span>`;
}

// 1. Distribusi Grade Mahasiswa — vertical bar, blue, 9 grades
new Chart(document.getElementById('gradeChart'), {
    type: 'bar',
    data: {
        labels: ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'E'],
        datasets: [{
            data: [130, 90, 115, 80, 50, 35, 30, 15, 10],
            backgroundColor: '#5b8dee',
            borderRadius: 4,
            barPercentage: 0.6
        }]
    },
    options: {
        plugins: { legend: { display: false } },
        scales: {
            y: { beginAtZero: true, max: 160, grid: { color: '#eee' } },
            x: { grid: { display: false } }
        }
    }
});

// 2. Tren Rata-rata Nilai per Semester — line, green
new Chart(document.getElementById('trendChart'), {
    type: 'line',
    data: {
        labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6'],
        datasets: [{
            data: [75, 77, 78, 80, 84, 82],
            borderColor: '#27ae60',
            backgroundColor: 'transparent',
            pointBackgroundColor: '#27ae60',
            pointRadius: 5,
            tension: 0.3
        }]
    },
    options: {
        plugins: { legend: { display: false } },
        scales: {
            y: { min: 70, max: 90, grid: { color: '#eee' } },
            x: { grid: { display: false } }
        }
    }
});

// 3. Jumlah Mahasiswa per Program Studi — horizontal bar, orange
new Chart(document.getElementById('prodiChart'), {
    type: 'bar',
    data: {
        labels: ['Teknik Informatika', 'Sistem Informasi', 'Teknik Komputer'],
        datasets: [{
            data: [160, 110, 70],
            backgroundColor: '#f5a623',
            borderRadius: 4,
            barPercentage: 0.5
        }]
    },
    options: {
        indexAxis: 'y',
        plugins: { legend: { display: false } },
        scales: {
            x: { beginAtZero: true, max: 160, grid: { color: '#eee' } },
            y: { grid: { display: false } }
        }
    }
});

// Ranking Table
const rankings = [
    { nim: '2021002', nama: 'Siti Nurhaliza', avg: 83.85 },
    { nim: '2021001', nama: 'Ahmad Fauzi',    avg: 86.75 },
    { nim: '2021003', nama: 'Budi Santoso',   avg: 85.00 },
    { nim: '2022002', nama: 'Rizky Ramadhan', avg: 82.50 },
    { nim: '2022001', nama: 'Dewi Lestari',   avg: 74.70 },
].sort((a, b) => b.avg - a.avg);

document.getElementById('rankingTable').innerHTML = rankings.map((r, i) => `
    <tr>
        <td><strong>#${i + 1}</strong></td>
        <td>${r.nim}</td>
        <td>${r.nama}</td>
        <td><strong>${r.avg.toFixed(2)}</strong></td>
        <td>${getGradeBadge(r.avg)}</td>
    </tr>
`).join('');
