from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core.security.password_hasher import PasswordHasher
from core.security.token_manager import TokenManager
from chat.schemas.common import LoginRequestBody, LoginResponse, SignupRequestBody, SignupResponse

from ..services.auth import AuthService


router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@router.post("/signup")
async def signup(user: SignupRequestBody, auth_service: FromDishka[AuthService]) -> SignupResponse:
    token_pair = await auth_service.signup(user.login, user.nickname, user.password)
    return SignupResponse.model_validate(token_pair, from_attributes=True)


@router.post("/login")
async def login(user: LoginRequestBody, auth_service: FromDishka[AuthService]) -> LoginResponse:
    token_pair = await auth_service.login(user.login, user.password)
    return LoginResponse.model_validate(token_pair, from_attributes=True)