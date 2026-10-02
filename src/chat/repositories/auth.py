from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.models import User
from core.dto.common import UserDTO

from .base import BaseRepository
from ..exceptions.common import UniqueConstraintError


class UserRepository(BaseRepository):
    async def add(self, login: str, hashed_password: str, nickname: str) -> UUID:
        user = User(login=login, hashed_pass=hashed_password, visible_nickname=nickname)
        self.session.add(user)
        try:
            await self.session.flush()
        except IntegrityError as e:
            raise UniqueConstraintError from e

        return user.id

    async def get_by(self, field: str, value: Any) -> UserDTO | None:
        query = select(User).where(getattr(User, field) == value)
        user = (await self.session.execute(query)).scalar_one_or_none()
        if user is not None:
            return UserDTO.from_orm_object(user)
