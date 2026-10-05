from collections.abc import AsyncGenerator
from datetime import timedelta

from dishka import Provider, Scope, make_async_container, provide
from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import Config
from core.dto.common import CurrentUser
from core.security.password_hasher import PasswordHasher
from core.security.token_manager import InvalidTokenError, TokenExpiredError, TokenManager, UnauthorizedError
from core.unit_of_work import UnitOfWork

from chat.repositories.auth import UserRepository
from chat.services.auth import AuthService



class CustomProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config()  # type: ignore

    @provide(scope=Scope.APP)
    async def get_db_engine(self, config: Config) -> AsyncGenerator[AsyncEngine]:
        engine = create_async_engine(config.core.database_dsn.get_secret_value())
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_db_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_db_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_password_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.APP)
    def get_token_manager(self, config: Config) -> TokenManager:
        return TokenManager(
            config.chat.secret_key.get_secret_value(),
            timedelta(seconds=config.chat.jwt_access_ttl),
            timedelta(seconds=config.chat.jwt_refresh_ttl),
        )

    @provide(scope=Scope.REQUEST)
    async def get_auth_repo(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_uow(
        self,
        session: AsyncSession,
    ) -> UnitOfWork:
        return UnitOfWork(session)


    @provide(scope=Scope.REQUEST)
    async def get_auth_service(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_manager: TokenManager,
        uow: UnitOfWork,
    ) -> AuthService:
        return AuthService(user_repo, password_hasher, token_manager, uow)

    @provide(scope=Scope.REQUEST)
    async def get_current_user(self, request: Request, token_manager: TokenManager) -> CurrentUser:
        authorization = request.headers.get("Authorization")

        if authorization is None:
            raise UnauthorizedError

        scheme, _, token = authorization.partition(" ")

        if scheme.lower() != "bearer" or not token:
            raise UnauthorizedError

        try:
            payload = token_manager.decode_access_token(token)
        except (InvalidTokenError, TokenExpiredError) as exc:
            raise UnauthorizedError from exc

        return CurrentUser(id=payload.sub)


container = make_async_container(CustomProvider())
