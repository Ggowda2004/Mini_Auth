import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { listApiKeys, createApiKey, revokeApiKey } from '../api/client';

export default function Dashboard() {
  const { user, signOut, refreshUser } = useAuth();
  const [keys, setKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [keyName, setKeyName] = useState('');
  const [creating, setCreating] = useState(false);
  const [createdKey, setCreatedKey] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const list = await listApiKeys();
        if (!cancelled) setKeys(list);
      } catch (e) {
        if (!cancelled) setError(e.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, []);

  async function handleCreateKey(e) {
    e.preventDefault();
    if (!keyName.trim() || keyName.length < 6) {
      setError('Name must be 6–50 characters');
      return;
    }
    setError('');
    setCreating(true);
    setCreatedKey(null);
    try {
      const result = await createApiKey(keyName.trim());
      setCreatedKey(result);
      setKeyName('');
      const list = await listApiKeys();
      setKeys(list);
    } catch (err) {
      setError(err.message || 'Failed to create key');
    } finally {
      setCreating(false);
    }
  }

  async function handleRevoke(keyId) {
    if (!confirm('Revoke this API key? It will stop working immediately.')) return;
    setError('');
    try {
      await revokeApiKey(keyId);
      setKeys((prev) => prev.filter((k) => k.id !== keyId));
    } catch (err) {
      setError(err.message || 'Failed to revoke key');
    }
  }

  return (
    <div className="page">
      <div className="card" style={{ maxWidth: 480 }}>
        <div className="dashboard-header">
          <h1>Dashboard</h1>
          <button type="button" className="btn btn-secondary" onClick={signOut} style={{ width: 'auto' }}>
            Sign out
          </button>
        </div>

        {user && (
          <div className="user-info">
            <strong>{user.email}</strong>
            {user.role && <span> · Admin</span>}
          </div>
        )}

        {error && <div className="error">{error}</div>}

        <section className="section">
          <h2>API keys</h2>
          <form onSubmit={handleCreateKey} className="create-key-form">
            <input
              type="text"
              placeholder="Key name (min 6 chars)"
              value={keyName}
              onChange={(e) => setKeyName(e.target.value)}
              minLength={6}
              maxLength={50}
            />
            <button type="submit" className="btn btn-primary" disabled={creating} style={{ width: 'auto' }}>
              {creating ? 'Creating…' : 'Create'}
            </button>
          </form>

          {createdKey && (
            <div className="key-created">
              <strong>Key created — copy it now; it won’t be shown again.</strong>
              <code style={{ display: 'block', marginTop: 4 }}>{createdKey.raw_key}</code>
            </div>
          )}

          {loading ? (
            <p style={{ color: '#6b7280', fontSize: '0.9rem' }}>Loading keys…</p>
          ) : keys.length === 0 ? (
            <p style={{ color: '#6b7280', fontSize: '0.9rem' }}>No API keys yet.</p>
          ) : (
            <ul className="api-key-list">
              {keys.map((k) => (
                <li key={k.id}>
                  <span>{k.name}</span>
                  {!k.revoked ? (
                    <button type="button" className="btn btn-danger" onClick={() => handleRevoke(k.id)}>
                      Revoke
                    </button>
                  ) : (
                    <span style={{ color: '#9ca3af', fontSize: '0.85rem' }}>Revoked</span>
                  )}
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}
