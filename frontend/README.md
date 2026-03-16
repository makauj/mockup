# Collections Console Frontend

This folder contains the current static web app UI for the backend API.

## Current app capabilities

- API base URL configuration in the UI (default: `http://localhost:8000`).
- OAuth2 login flow using `POST /auth/token` (username/password form).
- JWT bearer auth for API requests after OAuth2 login.
- Backward-compatible legacy auth mode using `X-User` header.
- Excel import flow using `POST /upload/`.
- Collection query and filtering UI using `GET /collections/`.
- Collection update flow using `PUT /collections/{record_id}`.
- Built-in activity log panel showing request outcomes and response payloads.

## UI sections

1. API Configuration
1. OAuth2 Login
1. Legacy Header Login
1. Upload Excel
1. Query Collections
1. Update Collection
1. Activity Log

## Local run

From workspace root:

```powershell
c:/Users/john/Downloads/Repos/mockup/.venv/Scripts/python.exe -m http.server 5173 --directory frontend
```

Open:

- `http://localhost:5173`

## Backend prerequisites

- Backend server is running and reachable from the browser.
- CORS is enabled in backend (already configured in current backend app).
- Use one of the supported auth paths:
  - OAuth2 JWT
  - Requires `AUTH_USERNAME` and `AUTH_PASSWORD` (or `AUTH_PASSWORD_HASH`) in backend env
  - Requires `JWT_SECRET_KEY` in backend env
  - Legacy fallback
  - Set `X-User` in the frontend login panel

## Typical usage flow

1. Set API base URL.
1. Authenticate using OAuth2 login or set legacy `X-User`.
1. Upload an `.xlsx`/`.xls` file.
1. Load filtered collections and review results in table.
1. Update editable rows by record ID.

## Files in this frontend

- `index.html`: page structure and panels
- `styles.css`: visual styling and responsive layout
- `app.js`: API integration, auth handling, and UI behavior
