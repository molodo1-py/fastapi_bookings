import pytest
from pydantic import EmailStr

from app.users.dao import UsersDAO
from app.users.models import Users


@pytest.mark.parametrize(
    "user_id,email,exists",
    [(1, "test@test.com", True), (2, "artem@example.com", True), (1488, "....", False)],
)
async def test_find_user_by_id(user_id: int, email: EmailStr, exists: bool):
    user: Users = await UsersDAO.find_by_id(user_id)

    if exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
