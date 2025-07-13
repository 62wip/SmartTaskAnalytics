from httpx import AsyncClient
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    test_data = {
        "username": "testuser",
        "email": "unique@example.com",
        "password": "testpass",
    }

    response = await client.post("/auth/register", json=test_data)

    print("Response status:", response.status_code)
    print("Response body:", response.json())

    assert response.status_code == status.HTTP_201_CREATED

    dup_response = await client.post("/auth/register", json=test_data)
    assert dup_response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already" in dup_response.json()["detail"].lower()

    error_detail = dup_response.json()["detail"].lower()
    assert any(field in error_detail for field in ["email", "username"])


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    user_data = {
        "username": "logintest2",
        "email": "logintes2@example.com",
        "password": "password",
    }

    register_response = await client.post("/auth/register", json=user_data)
    assert register_response.status_code == status.HTTP_201_CREATED

    login_data = {"username": user_data["email"], "password": user_data["password"]}

    login_response = await client.post("/auth/login", data=login_data)
    assert login_response.status_code == status.HTTP_201_CREATED
    response_json = login_response.json()

    assert "access_token" in response_json
    assert "token_type" in response_json
    assert response_json["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    user_data = {
        "username": "logintest3",
        "email": "logintest3@example.com",
        "password": "correctpassword",
    }

    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    login_data = {"username": user_data["email"], "password": "wrongpassword"}

    login_response = await client.post("/auth/login", data=login_data)

    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid" in login_response.json()["detail"]


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    login_data = {"username": "noone@example.com", "password": "any_password"}

    login_response = await client.post("/auth/login", data=login_data)

    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid" in login_response.json()["detail"]


@pytest.mark.asyncio
async def test_me_success(client: AsyncClient):
    user_data = {
        "username": "meuser",
        "email": "meuser@example.com",
        "password": "securepass",
    }
    register_resp = await client.post("/auth/register", json=user_data)
    assert register_resp.status_code == status.HTTP_201_CREATED

    login_data = {"username": user_data["email"], "password": user_data["password"]}
    login_resp = await client.post("/auth/login", data=login_data)
    assert login_resp.status_code == status.HTTP_201_CREATED
    token = login_resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    me_resp = await client.get("/auth/me", headers=headers)

    assert me_resp.status_code == status.HTTP_200_OK
    me_json = me_resp.json()
    assert me_json["email"] == "meuser@example.com"
    assert me_json["username"] == "meuser"


@pytest.mark.asyncio
async def test_me_unauthorized(client: AsyncClient):
    me_resp = await client.get("/auth/me")

    assert me_resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert "not authenticated" in me_resp.json()["detail"].lower()
