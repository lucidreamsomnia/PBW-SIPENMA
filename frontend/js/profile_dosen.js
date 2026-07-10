const user = JSON.parse(localStorage.getItem('user') || '{}');
if (user.nama) document.getElementById('topbarName').textContent = user.nama;

document.getElementById('logoutBtn').addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    window.location.href = '../pages/login.html';
});

// Populate profile fields from localStorage
function loadProfile() {
    const u = JSON.parse(localStorage.getItem('user') || '{}');
    document.getElementById('profileName').textContent  = u.nama     || 'Dosen';
    document.getElementById('profileNIDN').textContent  = 'NIDN: ' + (u.nidn    || '-');
    document.getElementById('profileProdi').textContent = 'Prodi: ' + (u.prodi   || '-');
    document.getElementById('inputNama').value    = u.nama    || '';
    document.getElementById('inputNIDN').value    = u.nidn    || '';
    document.getElementById('inputEmail').value   = u.email   || '';
    document.getElementById('inputTelp').value    = u.telp    || '';
    document.getElementById('inputProdi').value   = u.prodi   || '';
    document.getElementById('inputJabatan').value = u.jabatan || '';
}

loadProfile();

// Edit Profile
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const alertEl = document.getElementById('profileAlert');
    const payload = {
        nama:    document.getElementById('inputNama').value.trim(),
        nidn:    document.getElementById('inputNIDN').value.trim(),
        email:   document.getElementById('inputEmail').value.trim(),
        telp:    document.getElementById('inputTelp').value.trim(),
        prodi:   document.getElementById('inputProdi').value.trim(),
        jabatan: document.getElementById('inputJabatan').value.trim(),
    };

    try {
        const res = await fetch('http://127.0.0.1:8000/dosen/profile', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            const updated = { ...JSON.parse(localStorage.getItem('user') || '{}'), ...payload };
            localStorage.setItem('user', JSON.stringify(updated));
            loadProfile();
            alertEl.innerHTML = `<div class="alert alert-success py-2">Profil berhasil diperbarui.</div>`;
        } else {
            const data = await res.json();
            alertEl.innerHTML = `<div class="alert alert-danger py-2">${data.detail || 'Gagal memperbarui profil.'}</div>`;
        }
    } catch {
        // Demo mode
        const updated = { ...JSON.parse(localStorage.getItem('user') || '{}'), ...payload };
        localStorage.setItem('user', JSON.stringify(updated));
        loadProfile();
        alertEl.innerHTML = `<div class="alert alert-info py-2">Demo: Profil diperbarui secara lokal.</div>`;
    }
});

// Change Password
document.getElementById('pwForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const alertEl = document.getElementById('pwAlert');
    const pwLama  = document.getElementById('pwLama').value;
    const pwBaru  = document.getElementById('pwBaru').value;
    const pwKonfirmasi = document.getElementById('pwKonfirmasi').value;

    if (pwBaru !== pwKonfirmasi) {
        alertEl.innerHTML = `<div class="alert alert-warning py-2">Password baru dan konfirmasi tidak cocok.</div>`;
        return;
    }
    if (pwBaru.length < 6) {
        alertEl.innerHTML = `<div class="alert alert-warning py-2">Password minimal 6 karakter.</div>`;
        return;
    }

    try {
        const res = await fetch('http://127.0.0.1:8000/auth/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({ old_password: pwLama, new_password: pwBaru })
        });

        if (res.ok) {
            alertEl.innerHTML = `<div class="alert alert-success py-2">Password berhasil diubah.</div>`;
            document.getElementById('pwForm').reset();
        } else {
            const data = await res.json();
            alertEl.innerHTML = `<div class="alert alert-danger py-2">${data.detail || 'Gagal mengubah password.'}</div>`;
        }
    } catch {
        alertEl.innerHTML = `<div class="alert alert-info py-2">Demo: Backend belum terhubung.</div>`;
    }
});
