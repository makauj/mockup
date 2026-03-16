# Collection System

This project imports collection data from Excel into a PostgreSQL-backed API, enforces read-only rules on completed rows, tracks audit fields, and includes a static frontend for authentication, upload, querying, and updates.

## Current state

- FastAPI backend under `backend/`
- Alembic migrations under `alembic/`
- Static frontend under `frontend/`
- OAuth2 password login with JWT support
- Backward-compatible `X-User` and static bearer-token auth fallback
- Excel import rules implemented for read-only vs editable rows
- Audit fields stored on writes (`last_updated_by`, `last_updated_at`)
- Database trigger-based read-only enforcement included in migrations

## Import rules

- Required Excel column: `ID`
- Supported import columns: `ID`, `Name`, `Contact`, `Date`
- Ignored import columns: `Email`, `collected`
- If `ID`, `Name`, and `Contact` are all present, the row is imported as read-only
- If only `ID` is present, or `ID` plus partial data is present, the row remains editable
- If `Date` is missing, the current date is used
- Multiple rows per `ID` are supported

## Project structure

```text
mockup/
├── alembic/
├── backend/
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── db.sql
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── schemas.py
│   ├── tests/
│   └── utils.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   ├── styles.css
│   └── README.md
├── alembic.ini
└── README.md
```

## Backend API

Current endpoints:

- `POST /auth/token`: OAuth2 password login, returns JWT bearer token
- `POST /upload/`: upload `.xlsx` or `.xls` workbook
- `GET /collections/`: list collections with optional `ID`, `read_only`, `skip`, `limit`
- `PUT /collections/{record_id}`: update editable collection rows

## Authentication

Supported auth modes during rollout:

1. OAuth2/JWT
2. Static bearer token fallback
3. Legacy `X-User` header fallback

Environment variables:

```powershell
$env:AUTH_USERNAME = "admin"
$env:AUTH_PASSWORD = "change-me"
$env:JWT_SECRET_KEY = "change-me-long-random-secret"
$env:JWT_ALGORITHM = "HS256"
$env:JWT_EXPIRE_MINUTES = "60"
```

Optional compatibility settings:

```powershell
$env:API_BEARER_TOKEN = "change-me"
$env:API_BEARER_SUBJECT = "service_account"
```

## Database configuration

The backend requires `DATABASE_URL`.

Example:

```powershell
$env:DATABASE_URL = "postgresql://username:password@localhost:5432/your_database"
```

Note: the schema expects the referenced foreign-key table to exist:

```sql
CREATE TABLE IF NOT EXISTS other_table (
    id INTEGER PRIMARY KEY
);
```

## Install backend dependencies

From workspace root:

```powershell
c:/Users/john/Downloads/Repos/mockup/.venv/Scripts/python.exe -m pip install -r backend/requirements.txt
```

## Run backend locally

With environment variables set:

```powershell
c:/Users/john/Downloads/Repos/mockup/.venv/Scripts/python.exe -m uvicorn backend.main:app --reload
```

Default API URL:

- `http://localhost:8000`

## Migration workflow

Alembic is configured at the workspace root.

Apply migrations:

```powershell
c:/Users/john/Downloads/Repos/mockup/.venv/Scripts/python.exe -m alembic upgrade head
```

Create a new migration:

```powershell
c:/Users/john/Downloads/Repos/mockup/.venv/Scripts/python.exe -m alembic revision -m "describe_change"
```

Auto-generate a migration from model changes:

```powershell
c:/Users/john/Downloads/Repos/mockup/.venv/Scripts/python.exe -m alembic revision --autogenerate -m "describe_change"
```

Current migration chain:

- `4e1d706724c5`: initial collections schema + triggers
- `2f2bc9c539fe`: defaults/nullability alignment + record_id index

## Frontend

The frontend is a static web app in `frontend/`.

Current capabilities:

- API base URL configuration
- OAuth2 login and JWT storage in memory
- Legacy `X-User` auth mode
- Excel upload UI
- Collection filter/query table
- Update form by `record_id`
- Activity log panel for request results

Run frontend locally:

```powershell
c:/Users/john/Downloads/Repos/mockup/.venv/Scripts/python.exe -m http.server 5173 --directory frontend
```

Open:

- `http://localhost:5173`

## Testing

Run backend tests:

```powershell
c:/Users/john/Downloads/Repos/mockup/.venv/Scripts/python.exe -m pytest backend/tests -q
```

Current automated coverage includes:

- Excel parsing behavior
- Upload validation
- Legacy auth fallback
- OAuth2 token issuance
- JWT-protected upload behavior

## CI

GitHub Actions migration safety workflow:

- `.github/workflows/migration-check.yml`

It validates:

1. `alembic upgrade head`
2. `alembic downgrade base`
3. `alembic upgrade head`

## Known local prerequisites

- PostgreSQL must be running and reachable before applying migrations
- Docker-based local DB startup was not possible in this environment because the Docker daemon was unavailable
- The foreign-key target table `other_table` must exist before applying the collections migration
