from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

from .core import UnitOfWork

P = ParamSpec("P")
R = TypeVar("R")
S = TypeVar("S", bound="HasUnitOfWork")


class HasUnitOfWork(Protocol):
    _uow: UnitOfWork


def transactional(
    func: Callable[Concatenate[S, P], Awaitable[R]],
) -> Callable[Concatenate[S, P], Awaitable[R]]:
    @wraps(func)
    async def wrapper(
        self: S,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        async with self._uow.transaction():
            return await func(self, *args, **kwargs)

    return wrapper