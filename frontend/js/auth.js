let currentUser = null;

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    const username = localStorage.getItem('username');
    if (token && username) {
        currentUser = { username };
        afterLogin();
    }
});

async function doRegister() {
    const username = document.getElementById('reg-user').value.trim();
    const password = document.getElementById('reg-pass').value;
    if (!username || !password) { setMsg('register-msg', 'Please fill all fields.', 'error'); return; }

    setLoading('btn-register', true, 'Creating…');
    try {
        const res = await fetch(`${API}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            setMsg('register-msg', '✅ Account created! You can now log in.', 'success');
            setTimeout(() => switchTab('login'), 1200);
        } else {
            setMsg('register-msg', data.detail || 'Registration failed.', 'error');
        }
    } catch {
        setMsg('register-msg', 'Server unreachable.', 'error');
    } finally {
        setLoading('btn-register', false, 'Create Account');
    }
}

async function doLogin() {
    const username = document.getElementById('login-user').value.trim();
    const password = document.getElementById('login-pass').value;
    if (!username || !password) { setMsg('login-msg', 'Please fill all fields.', 'error'); return; }

    setLoading('btn-login', true, 'Logging in…');
    try {
        const res = await fetch(`${API}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('username', username);
            currentUser = { username };
            afterLogin();
        } else {
            setMsg('login-msg', data.detail || 'Login failed.', 'error');
        }
    } catch {
        setMsg('login-msg', 'Server unreachable.', 'error');
    } finally {
        setLoading('btn-login', false, 'Login');
    }
}

function afterLogin() {
    document.getElementById('nav-user-area').style.display = 'flex';
    document.getElementById('nav-username').textContent = currentUser.username;

    // Clear forms
    document.getElementById('login-pass').value = '';

    if (typeof loadProfileStats === 'function') loadProfileStats();
    if (typeof loadLeaderboard === 'function') loadLeaderboard();

    showScreen('lobby-screen');
}

function logout() {
    currentUser = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    if (typeof ws !== 'undefined' && ws) { ws.close(); ws = null; }
    if (typeof pollTimer !== 'undefined' && pollTimer) { clearInterval(pollTimer); pollTimer = null; }
    document.getElementById('nav-user-area').style.display = 'none';
    showScreen('auth-screen');
}
