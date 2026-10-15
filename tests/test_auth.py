import asyncio
import uuid
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.api.routes import auth as auth_routes
from app.core.config import Settings
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    test_settings = Settings(
        data_dir=tmp_path / "data",
        gemini_api_key=None,
        google_client_id="test-google-client-id",
    )
    application = create_app(test_settings)
    with TestClient(application) as test_client:
        yield test_client


def test_auth_registration_login_and_me(client: TestClient) -> None:
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json()["authenticated"] is False

    payload = {
        "email": "user@example.com",
        "password": "SecretPassword123",
        "full_name": "Tuhin Ahmed",
    }
    registered = client.post("/api/auth/register", json=payload)
    assert registered.status_code == 201
    user = registered.json()
    assert user["user"]["email"] == "user@example.com"
    assert user["user"]["full_name"] == "Tuhin Ahmed"
    token = user["token"]
    assert len(token) > 20

    assert client.post("/api/auth/register", json=payload).status_code == 400
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["authenticated"] is True
    assert me.json()["user"]["email"] == "user@example.com"

    login = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "SecretPassword123"},
    )
    assert login.status_code == 200
    assert login.json()["user"]["email"] == "user@example.com"
    assert client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "WrongPassword"},
    ).status_code == 401

    logout = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout.status_code == 200
    assert client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    ).json()["authenticated"] is False


def test_signup_aliases(client: TestClient) -> None:
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "signup_alias@example.com",
            "password": "Password123",
            "full_name": "Alias User",
        },
    )
    assert response.status_code == 201

    root_response = client.post(
        "/signup",
        json={
            "email": "root_signup@example.com",
            "password": "Password123",
            "full_name": "Root User",
        },
    )
    assert root_response.status_code == 201

    modern_tld = client.post(
        "/api/auth/register",
        json={
            "email": "reader+docs@example.technology",
            "password": "Password123",
            "full_name": "Reader",
        },
    )
    assert modern_tld.status_code == 201


def test_unknown_account_login_does_not_register_implicitly(client: TestClient) -> None:
    payload = {"email": "new@example.com", "password": "Password123"}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 404
    assert client.post(
        "/api/auth/register",
        json={**payload, "full_name": "New User"},
    ).status_code == 201


def test_google_signin_requires_verified_google_id_token(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        auth_routes,
        "_verify_google_credential",
        lambda credential, client_id: {
            "email": "researcher@gmail.com",
            "email_verified": True,
            "name": "Dr. Researcher",
        },
    )
    response = client.post(
        "/api/auth/google",
        json={"credential": "verified-google-id-token"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "researcher@gmail.com"
    assert data["user"]["full_name"] == "Dr. Researcher"

    monkeypatch.setattr(
        auth_routes,
        "_verify_google_credential",
        lambda credential, client_id: {
            "email": "forged@gmail.com",
            "email_verified": False,
            "name": "Forged",
        },
    )
    rejected = client.post(
        "/api/auth/google",
        json={"credential": "unverified-google-id-token"},
    )
    assert rejected.status_code == 401


def test_google_signin_fails_clearly_without_client_id(tmp_path) -> None:
    application = create_app(Settings(data_dir=tmp_path / "data", google_client_id=None))
    with TestClient(application) as client:
        response = client.post("/api/auth/google", json={"credential": "some-token"})
    assert response.status_code == 503
    assert "GOOGLE_CLIENT_ID" in response.json()["detail"]


def test_user_data_is_private_and_legacy_data_goes_to_first_account(
    client: TestClient,
) -> None:
    document_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()

    async def add_legacy_document() -> None:
        await client.app.state.database.add_document(
            {
                "id": document_id,
                "filename": "legacy.pdf",
                "title": "legacy",
                "page_count": 1,
                "chunk_count": 1,
                "created_at": now,
                "file_path": "legacy.pdf",
            }
        )

    asyncio.run(add_legacy_document())
    first = client.post(
        "/api/auth/register",
        json={
            "email": "first@example.com",
            "password": "Password123",
            "full_name": "First User",
        },
    ).json()
    second = client.post(
        "/api/auth/register",
        json={
            "email": "second@example.com",
            "password": "Password123",
            "full_name": "Second User",
        },
    ).json()

    created_chat = client.post(
        "/api/chats",
        json={"document_id": document_id},
        headers={"Authorization": f"Bearer {first['token']}"},
    )
    assert created_chat.status_code == 201
    chat_id = created_chat.json()["id"]

    first_docs = client.get(
        "/api/documents",
        headers={"Authorization": f"Bearer {first['token']}"},
    )
    second_docs = client.get(
        "/api/documents",
        headers={"Authorization": f"Bearer {second['token']}"},
    )
    assert [item["id"] for item in first_docs.json()["documents"]] == [document_id]
    assert second_docs.json()["documents"] == []
    second_chats = client.get(
        "/api/chats",
        headers={"Authorization": f"Bearer {second['token']}"},
    )
    assert second_chats.json()["conversations"] == []
    assert client.get(
        f"/api/chats/{chat_id}",
        headers={"Authorization": f"Bearer {second['token']}"},
    ).status_code == 404
    assert client.delete(
        f"/api/documents/{document_id}",
        headers={"Authorization": f"Bearer {second['token']}"},
    ).status_code == 404
    client.cookies.delete("documind_token")
    assert client.get("/api/documents").status_code == 401
    assert client.get("/api/chats").status_code == 401
