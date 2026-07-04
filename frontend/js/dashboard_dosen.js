// Set topbar name from localStorage
const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

// Logout
document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

// Pie Chart - Status Kelulusan
new Chart(document.getElementById('kelulusanChart'), {
    type: 'pie',
    data: {
        labels: ['Lulus: 89%', 'Tidak Lulus: 11%'],
        datasets: [{
            data: [89, 11],
            backgroundColor: ['#27ae60', '#e74c3c'],
            borderWidth: 0
        }]
    },
    options: {
        plugins: {
            legend: { position: 'bottom' }
        }
    }
});

// Bar Chart - Rata-rata Nilai per Mata Kuliah
new Chart(document.getElementById('matkulChart'), {
    type: 'bar',
    data: {
        labels: ['Algoritma', 'Basis Data', 'Jaringan', 'Web Dev', 'Mobile'],
        datasets: [{
            label: 'Rata-rata',
            data: [78, 75, 74, 84, 77],
            backgroundColor: '#27ae60',
            borderRadius: 4
        }]
    },
    options: {
        scales: {
            y: { min: 0, max: 100, grid: { color: '#eee' } },
            x: { grid: { display: false } }
        },
        plugins: { legend: { position: 'bottom' } }
    }
});
