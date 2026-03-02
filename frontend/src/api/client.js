const BASE = import.meta.env.VITE_API_URL || '';

function getToken() {
  return localStorage.getItem('access_token');
}

export async function register(email, password) {
  const res = await fetch(`${BASE}/auth_f/v1/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || 'Registration failed');
  return data;
}

export async function login(email, password) {
  const form = new URLSearchParams();
  form.set('username', email);
  form.set('password', password);
  const res = await fetch(`${BASE}/auth_f/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form.toString(),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || 'Login failed');
  return data;
}

export async function getMe() {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const res = await fetch(`${BASE}/auth_f/v1/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || 'Unauthorized');
  return data;
}

export async function listApiKeys() {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const res = await fetch(`${BASE}/api_f/v1/api-keys/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || 'Failed to list keys');
  return Array.isArray(data) ? data : [];
}

export async function createApiKey(name) {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const res = await fetch(`${BASE}/api_f/v1/api-keys/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ name }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || 'Failed to create key');
  return data;
}

export async function revokeApiKey(keyId) {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const res = await fetch(`${BASE}/api_f/v1/api-keys/${keyId}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || 'Failed to revoke key');
  }
}
