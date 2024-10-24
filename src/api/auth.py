from fastapi import APIRouter, HTTPException, Response, Request

from src.services.auth import AuthSevice
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAdd):
    hashed_password = AuthSevice().hash_password(data.password)
    new_user_data = UserAdd(
        username=data.username,
        hashed_password=hashed_password,
        email=data.email
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(
            email=data.email)
        if user is None:
            raise HTTPException(
                status_code=401, detail="Нет такого пользователя")
        if not AuthSevice().verify_password(
                data.password, user.hashed_password):
            raise HTTPException(
                status_code=401, detail="Неверный пароль"
            )
        access_token = AuthSevice().create_access_token(
            data={"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token, "token_type": "bearer"}


@router.get("/only_auth")
async def only_auth(request: Request):
    access_token = request.cookies.get("access_token", None)
    return {"status": "OK", "access_token": access_token}
