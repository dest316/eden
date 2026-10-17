from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from core.security.token_manager import (
    InvalidTokenError,
    TokenExpiredError,
    UnauthorizedError,
)

from .exceptions.common import (
    EntityNotFoundError,
    ForbiddenError,
    LinkExpiredError,
    LoginAlreadyExistsError,
    WrongCredentialsError,
)

# HTTP policy lives here; services and repositories remain independent of HTTP.
ERROR_RESPONSES: dict[type[Exception], tuple[int, str]] = {
    LoginAlreadyExistsError: (status.HTTP_409_CONFLICT, "Login already exists"),
    EntityNotFoundError: (status.HTTP_404_NOT_FOUND, "Entity not found"),
    WrongCredentialsError: (status.HTTP_401_UNAUTHORIZED, "Wrong username or password"),
    LinkExpiredError: (status.HTTP_410_GONE, "Invitation link has been revoked"),
    ForbiddenError: (status.HTTP_403_FORBIDDEN, "Forbidden"),
    UnauthorizedError: (status.HTTP_401_UNAUTHORIZED, "Authentication required"),
    InvalidTokenError: (status.HTTP_401_UNAUTHORIZED, "Invalid authentication token"),
    TokenExpiredError: (status.HTTP_401_UNAUTHORIZED, "Authentication token has expired"),
}


async def service_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Match Starlette's nearest-ancestor lookup, including exception subclasses.
    exception_type = next(cls for cls in type(exc).__mro__ if cls in ERROR_RESPONSES)
    status_code, detail = ERROR_RESPONSES[exception_type]
    headers = (
        {"WWW-Authenticate": "Bearer"} if status_code == status.HTTP_401_UNAUTHORIZED else None
    )
    return JSONResponse(status_code=status_code, content={"detail": detail}, headers=headers)


def register_exception_handlers(app: FastAPI) -> None:
    for exception_type in ERROR_RESPONSES:
        app.add_exception_handler(exception_type, service_exception_handler)
