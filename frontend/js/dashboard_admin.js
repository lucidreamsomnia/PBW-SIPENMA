const API_BASE = 'http://127.0.0.1:8000';

const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

const fallbackData = {
    summary: {
        total_mahasiswa: 0,
        total_matakuliah: 0,
        total_pengguna: 0,
        kelas_aktif: 0
    },
    mahasiswa_status: {
        labels: ['Aktif'],
        values: [0]
    },
    pengguna_role: {
        labels: ['Admin', 'Dosen'],
        values: [0, 0]
    },
    recent_activities: []
};

let statusChart;
let roleChart;

function setText(id, value) {
    document.getElementById(id).textContent = value;
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

function renderSummary(summary) {
    setText('totalMahasiswa', summary.total_mahasiswa);
    setText('totalMatkul', summary.total_matakuliah);
    setText('totalPengguna', summary.total_pengguna);
    setText('kelasAktif', summary.kelas_aktif);
}

function renderCharts(data) {
    if (statusChart) statusChart.destroy();
    if (roleChart) roleChart.destroy();

    statusChart = new Chart(document.getElementById('statusMahasiswaChart'), {
        type: 'pie',
        data: {
            labels: data.mahasiswa_status.labels,
            datasets: [{
                data: data.mahasiswa_status.values,
                backgroundColor: ['#27ae60', '#f5a623', '#e74c3c', '#5b8dee'],
                borderWidth: 0
            }]
        },
        options: {
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });

    roleChart = new Chart(document.getElementById('penggunaRoleChart'), {
        type: 'bar',
        data: {
            labels: data.pengguna_role.labels,
            datasets: [{
                label: 'Total Pengguna',
                data: data.pengguna_role.values,
                backgroundColor: '#27ae60',
                borderRadius: 4
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: '#eee' } },
                x: { grid: { display: false } }
            },
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

function renderActivities(activities) {
    const table = document.getElementById('activityTable');

    table.innerHTML = activities.map(item => `
        <tr>
            <td>${item.aktivitas}</td>
            <td>${formatDate(item.waktu)}</td>
        </tr>
    `).join('') || '<tr><td colspan="2" class="text-center text-muted py-3">Belum ada aktivitas</td></tr>';
}

function renderDashboard(data) {
    renderSummary(data.summary);
    renderCharts(data);
    renderActivities(data.recent_activities);
}

async function loadDashboard() {
    try {
        const res = await fetch(`${API_BASE}/admin/dashboard/`);
        if (!res.ok) throw new Error('Gagal mengambil data dashboard');
        const data = await res.json();
        renderDashboard(data);
    } catch {
        renderDashboard(fallbackData);
    }
}

loadDashboard();
