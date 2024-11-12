import pytest
from httpx import AsyncClient
from pydantic import EmailStr


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "kotopes", 200),
        ("kot@pes.com", "kot0pes", 409),
        ("pes@kot.com", "pesokot", 200),
        ("abcde", "kotopes", 422),
    ],
)
async def test_register_user(
    email: EmailStr, password: str, status_code: int, ac: AsyncClient
):
    response = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test", 200),
        ("artem@example.com", "artem", 200),
        ("wrong@person.com", "pidoras", 401),
        ("person.com", "pidoras", 422),
    ],
)
async def test_login_user(
    email: EmailStr, password: str, status_code: int, ac: AsyncClient
):

    response = await ac.post("/auth/login", json={"email": email, "password": password})

    assert response.status_code == status_code