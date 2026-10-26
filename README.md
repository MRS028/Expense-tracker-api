# Expense Tracker API

A production-ready **Personal Expense Tracker REST API** built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. Users can register, log in with JWT authentication, and manage their own income/expense records with full CRUD operations, filtering, and user ownership isolation.

This project was built as the **Mid Term assignment (Module 24)** for the Phitron AI-ML track.

---

## Live Demo

- **Base URL**: https://expense-tracker-api-1phr.onrender.com
- **Swagger UI**: https://expense-tracker-api-1phr.onrender.com/docs

---

## Features

- **JWT Authentication** — Register and login with secure password hashing (`bcrypt`)
- **Full CRUD** for income and expense transactions
- **User Ownership Isolation** — users can only access their own transactions
- **Advanced Filtering** — filter by type, category, and amount range
- **Pydantic Validation** — enforces positive amounts, valid types, and ISO date format
- **SQLAlchemy ORM** with PostgreSQL persistence
- **Pytest Test Suite** — 5 automated tests covering all core operations
- **Auto-generated Swagger UI** at `/docs`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL |
| Authentication | JWT (`python-jose`) + `bcrypt` |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Testing | Pytest + HTTPX |
| Deployment | Render |

---

## Project Structure

```
expense-tracker-api/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry point
│   ├── config.py                   # Environment variable loading
│   ├── database.py                 # SQLAlchemy engine + session
│   ├── models.py                   # User, Transaction ORM models
│   ├── schemas.py                  # Pydantic request/response schemas
│   ├── auth.py                     # JWT + password utilities
│   └── routers/
│       ├── __init__.py
│       ├── auth_router.py          # /auth/register, /auth/login
│       └── transaction_router.py   # /transactions CRUD + filter
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   └── test_transactions.py        # 5 core test cases
├── .env.example
├── .gitignore
├── pytest.ini
├── postman_collection.json
├── render.yaml
├── requirements.txt
└── README.md
```

---

## Quick Start (Local)

### 1. Clone the repo

```bash
git clone https://github.com/MRS028/expense-tracker-api.git
cd expense-tracker-api
```

### 2. Create virtual environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database

```bash
psql -U postgres -h localhost -c "CREATE DATABASE expense_db;"
```

### 5. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```env
SECRET_KEY=your-super-secret-key-change-me
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=expense_db
```

> **Note:** `SECRET_KEY` must be a strong random string. Generate one with:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 6. Run the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |

**Register body:**
```json
{
  "username": "rakib",
  "email": "rakib@example.com",
  "password": "mypassword123"
}
```

**Login** uses `application/x-www-form-urlencoded`:
```
username=rakib&password=mypassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Transactions

All transaction endpoints require `Authorization: Bearer <token>`.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/transactions/` | Create a new transaction |
| GET | `/transactions/` | List all transactions (own only) |
| GET | `/transactions/{id}` | Get a specific transaction |
| PUT | `/transactions/{id}` | Update a transaction |
| DELETE | `/transactions/{id}` | Delete a transaction |
| GET | `/transactions/filter` | Filter by type/category/amount |

**Create transaction body:**
```json
{
  "title": "Lunch",
  "amount": 250.50,
  "type": "expense",
  "category": "Food",
  "date": "2026-10-26"
}
```

**Validation rules:**
- `amount` must be **positive** (`> 0`)
- `type` must be `"income"` or `"expense"`
- `date` must be ISO format `YYYY-MM-DD`

### Filtering

```
GET /transactions/filter?type=expense&category=Food&minimum_amount=100&maximum_amount=5000
```

All query parameters are optional. Only the logged-in user's transactions are returned.

---

## Testing

Run the automated test suite:

```bash
pytest -v
```

Expected output:
```
tests/test_transactions.py::test_create_transaction PASSED
tests/test_transactions.py::test_get_all_transactions PASSED
tests/test_transactions.py::test_get_specific_transaction PASSED
tests/test_transactions.py::test_update_transaction PASSED
tests/test_transactions.py::test_delete_transaction PASSED

==================== 5 passed in 2.00s ====================
```

### Manual Testing with Postman

Import `postman_collection.json` into Postman. The collection includes:

- Health check
- Authentication (register + login with auto-token saving)
- All CRUD operations
- Filtering scenarios
- Negative tests (401, 404, 422)

Run the **Login** request first — the token is automatically saved to a collection variable and applied to all subsequent requests.

---

## Deployment on Render

This project includes `render.yaml` for one-click deployment.

### Steps

1. Push the project to GitHub (ensure `.env` is in `.gitignore`).
2. In Render dashboard: **New → Blueprint** → connect your repo.
3. Render reads `render.yaml` and automatically provisions:
   - PostgreSQL database
   - Web service with environment variables injected
4. Wait for the build to complete.
5. Verify at `https://your-app.onrender.com/docs`.

### Manual Setup (alternative)

| Setting | Value |
|---|---|
| Environment | Python 3.12 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Add these environment variables:
- `SECRET_KEY` (generate a random one)
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` (from Render PostgreSQL)

---

## Security Notes

- Passwords are hashed with **bcrypt** (never stored in plaintext).
- JWT tokens expire after **30 minutes**.
- All transaction queries include `WHERE owner_id = current_user.id` — users cannot access or modify other users' records.
- The `.env` file is **never committed** to Git (see `.gitignore`).
- On Render, all secrets are injected via environment variables.

---

## Author

- Name: Md. Rifat Sheikh
- GitHub: [@MRS028](https://github.com/MRS028)
- Email: rifat.seu.cse@gmail.com

---
