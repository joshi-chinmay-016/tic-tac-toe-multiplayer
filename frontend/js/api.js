const API = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000'
    : window.location.origin;

function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

async function apiFetch(endpoint, options = {}) {
    const headers = { ...getAuthHeaders(), ...options.headers };
    return fetch(`${API}${endpoint}`, { ...options, headers });
}
