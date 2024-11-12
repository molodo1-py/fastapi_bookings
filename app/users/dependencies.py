from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exc.exceptions import (
    IncorrectFormatTokenException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.dao import UsersDAO


def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token=token, key=settings.ACCESS_KEY, algorithms=settings.ACCESS_ALGORITHM
        )
    except JWTError:
        raise IncorrectFormatTokenException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(model_id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user