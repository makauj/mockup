import os
from datetime import datetime

from fastapi.testclient import TestClient

# Ensure imports can build an engine during tests.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from backend.main import app, get_db  # noqa: E402
from backend.schemas import CollectionCreate  # noqa: E402


class _DummyDB:
    pass


def _override_get_db():
    yield _DummyDB()


app.dependency_overrides[get_db] = _override_get_db
client = TestClient(app)


def test_upload_requires_user_header() -> None:
    response = client.post(
        "/upload/",
        files={"file": ("rows.xlsx", b"dummy", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    assert response.status_code == 401


def test_upload_rejects_non_excel_extension() -> None:
    response = client.post(
        "/upload/",
        files={"file": ("rows.txt", b"dummy", "text/plain")},
        headers={"X-User": "tester"},
    )
    assert response.status_code == 400
    assert "Only .xlsx and .xls" in response.json()["detail"]


def test_upload_accepts_bearer_token(monkeypatch) -> None:
    now = datetime.utcnow()
    monkeypatch.setenv("API_BEARER_TOKEN", "secret-token")
    monkeypatch.setenv("API_BEARER_SUBJECT", "service-account")

    def _fake_parse_excel(_file):
        return [
            (
                CollectionCreate(ID=12, Name="Bearer", Email=None, Contact="555", Date=now.date()),
                True,
            )
        ]

    def _fake_create_collection(_db, _entry, _read_only, user):
        return {
            "record_id": 2,
            "ID": 12,
            "Name": "Bearer",
            "Email": None,
            "Contact": "555",
            "Date": now.date(),
            "read_only": True,
            "last_updated_by": user,
            "last_updated_at": now,
        }

    monkeypatch.setattr("backend.main.parse_excel", _fake_parse_excel)
    monkeypatch.setattr("backend.main.crud.create_collection", _fake_create_collection)

    response = client.post(
        "/upload/",
        files={"file": ("rows.xlsx", b"dummy", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers={"Authorization": "Bearer secret-token"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload[0]["last_updated_by"] == "service-account"


def test_upload_rejects_invalid_bearer_token(monkeypatch) -> None:
    monkeypatch.setenv("API_BEARER_TOKEN", "good-token")

    response = client.post(
        "/upload/",
        files={"file": ("rows.xlsx", b"dummy", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers={"Authorization": "Bearer bad-token"},
    )

    assert response.status_code == 401


def test_oauth2_token_endpoint_and_jwt_upload(monkeypatch) -> None:
    now = datetime.utcnow()
    monkeypatch.setenv("AUTH_USERNAME", "admin")
    monkeypatch.setenv("AUTH_PASSWORD", "secret")
    monkeypatch.setenv("JWT_SECRET_KEY", "jwt-secret")

    token_response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "secret"},
    )
    assert token_response.status_code == 200
    token_payload = token_response.json()
    assert token_payload["token_type"] == "bearer"
    access_token = token_payload["access_token"]

    def _fake_parse_excel(_file):
        return [
            (
                CollectionCreate(ID=20, Name="JWT", Email=None, Contact="999", Date=now.date()),
                True,
            )
        ]

    def _fake_create_collection(_db, _entry, _read_only, user):
        return {
            "record_id": 3,
            "ID": 20,
            "Name": "JWT",
            "Email": None,
            "Contact": "999",
            "Date": now.date(),
            "read_only": True,
            "last_updated_by": user,
            "last_updated_at": now,
        }

    monkeypatch.setattr("backend.main.parse_excel", _fake_parse_excel)
    monkeypatch.setattr("backend.main.crud.create_collection", _fake_create_collection)

    response = client.post(
        "/upload/",
        files={"file": ("rows.xlsx", b"dummy", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload[0]["last_updated_by"] == "admin"


def test_upload_accepts_valid_excel_with_mocks(monkeypatch) -> None:
    now = datetime.utcnow()

    def _fake_parse_excel(_file):
        return [
            (
                CollectionCreate(ID=10, Name="A", Email=None, Contact="555", Date=now.date()),
                True,
            )
        ]

    def _fake_create_collection(_db, _entry, _read_only, user):
        return {
            "record_id": 1,
            "ID": 10,
            "Name": "A",
            "Email": None,
            "Contact": "555",
            "Date": now.date(),
            "read_only": True,
            "last_updated_by": user,
            "last_updated_at": now,
        }

    monkeypatch.setattr("backend.main.parse_excel", _fake_parse_excel)
    monkeypatch.setattr("backend.main.crud.create_collection", _fake_create_collection)

    response = client.post(
        "/upload/",
        files={"file": ("rows.xlsx", b"dummy", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        headers={"X-User": "tester"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["ID"] == 10
    assert payload[0]["read_only"] is True
    assert payload[0]["last_updated_by"] == "tester"
