const API_BASE = 'http://localhost:8000';

document.getElementById('togglePassword').addEventListener('click', () => {
    const pwd = document.getElementById('password');
    const icon = document.getElementById('eyeIcon');
    const isHidden = pwd.type === 'password';
    pwd.type = isHidden ? 'text' : 'password';
    icon.className = isHidden ? 'bi bi-eye-slash' : 'bi bi-eye';
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const alertBox = document.getElementById('alertBox');

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            alertBox.innerHTML = `<div class="alert alert-danger py-2">${data.detail || 'Login gagal.'}</div>`;
            return;
        }

        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('user', JSON.stringify(data.user));

        if (data.role === 'dosen') {
            window.location.href = 'dashboard_dosen.html';
        } else if (data.role === 'admin') {
            window.location.href = 'dashboard_admin.html';
        } else {
            alertBox.innerHTML = `<div class="alert alert-warning py-2">Role tidak dikenali.</div>`;
        }

    } catch {
        alertBox.innerHTML = `<div class="alert alert-danger py-2">Tidak dapat terhubung ke server.</div>`;
    }
});
