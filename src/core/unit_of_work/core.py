from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None]:
        if self._session.in_transaction():
            yield
            return

        async with self._session.begin():
            yield
