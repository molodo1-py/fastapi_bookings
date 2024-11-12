from fastapi import APIRouter, Depends, Response
from fastapi_versioning import version

from app.exc.exceptions import IncorrectEmailOrPassword, UserAlreadyExistException
from app.users.auth import authenticate_user, create_acces_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(prefix="/auth", tags=["Auth & Users"])


@router.post("/register")
@version(1)
async def register_user(user_data: SUserAuth) -> None:
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
@version(1)
async def login_user(response: Response, user_data: SUserAuth) -> dict:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_acces_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
@version(1)
async def logout_user(response: Response) -> None:
    response.delete_cookie(key="booking_access_token")


@router.get("/me")
@version(1)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user