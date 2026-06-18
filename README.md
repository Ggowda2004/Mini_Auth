# Mini Auth

A small auth API built with **FastAPI** and **PostgreSQL** — user registration, JWT login, and API key management.

The **backend** is the main part of this project. The **frontend** is a basic React dashboard (AI-assisted) to test the API.

---

## What it does

- Register and log in users
- Issue JWT access tokens
- Create, list, and revoke API keys (`sk_live_...`)
- Protect routes with JWT or `x-api-key` header

---

## Tech stack

**Backend:** FastAPI, SQLAlchemy, PostgreSQL, Pydantic, JWT, bcrypt, SHA-256

**Frontend:** React, Vite

---

## Quick start

### 1. Create the database

```sql
CREATE DATABASE auth_db;
```

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Create `backend/.env`:

```env
JWT_SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/auth_db
```

Run:

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### 3. Frontend (optional)

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## Main endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /auth_f/v1/auth/register` | Register (JSON) |
| `POST /auth_f/v1/auth/login` | Login → JWT |
| `GET /auth_f/v1/auth/me` | Current user |
| `POST /api_f/v1/api-keys/` | Create API key |
| `GET /api_f/v1/api-keys/` | List API keys |
| `DELETE /api_f/v1/api-keys/{id}` | Revoke key |

Protected routes need `Authorization: Bearer <token>` or `x-api-key: <key>`.

---

## Project layout

```
backend/app/
  core/          config, security
  db/models/     User, APIKey, AuditLogs
  routes/        auth, api-keys
  services/      business logic
  schemas/       request validation

frontend/        React UI
```
