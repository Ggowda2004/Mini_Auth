# Mini Auth — Frontend (MVP)

Minimal React frontend for the Mini Auth backend (FastAPI + Postgres, Clerk-like auth).

## Setup

1. Copy env and install deps:

   ```bash
   cp .env.example .env
   npm install
   ```

2. In `.env`, set `VITE_API_URL` if the API is not on the same host (e.g. `http://localhost:8000`). Leave empty to use Vite’s proxy (recommended for dev).

3. Start the backend (from repo root):

   ```bash
   cd backend && uvicorn app.main:app --reload
   ```

4. Start the frontend:

   ```bash
   npm run dev
   ```

5. Open http://localhost:5173 — Register, Login, Dashboard (profile + API keys).

## MVP features

- **Register** — email + password (min 8 chars, one letter, one number)
- **Login** — email + password → JWT stored in `localStorage`
- **Dashboard** — current user info + create/list/revoke API keys
- **Protected routes** — unauthenticated users are redirected to `/login`
