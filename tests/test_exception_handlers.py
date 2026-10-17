import json

import pytest
from fastapi import FastAPI, HTTPException

from chat.exception_handlers import register_exception_handlers
from chat.exceptions.common import (
    EntityNotFoundError,
    ForbiddenError,
    LinkExpiredError,
    LoginAlreadyExistsError,
    UniqueConstraintError,
    WrongCredentialsError,
)
from core.security.token_manager import InvalidTokenError, TokenExpiredError, UnauthorizedError


async def request(app: FastAPI, path: str = "/") -> tuple[int, dict, dict]:
    """Exercise the ASGI app without a server or database."""
    messages = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    await app(
        {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": "GET",
            "scheme": "http",
            "path": path,
            "root_path": "",
            "query_string": b"",
            "headers": [],
        },
        receive,
        send,
    )
    start = next(message for message in messages if message["type"] == "http.response.start")
    body = b"".join(
        message.get("body", b"") for message in messages if message["type"] == "http.response.body"
    )
    return start["status"], dict(start["headers"]), json.loads(body)


def app_raising(exc: Exception) -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/")
    async def endpoint():
        raise exc

    return app


@pytest.mark.parametrize(
    "exception_type",
    [
        LoginAlreadyExistsError,
        EntityNotFoundError,
        WrongCredentialsError,
        LinkExpiredError,
        ForbiddenError,
        UnauthorizedError,
        InvalidTokenError,
        TokenExpiredError,
    ],
)
def test_application_starts_and_registers_handlers(exception_type):
    from main import app

    assert exception_type in app.exception_handlers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("exception_type", "expected_status", "expected_detail"),
    [
        (LoginAlreadyExistsError, 409, "Login already exists"),
        (EntityNotFoundError, 404, "Entity not found"),
        (WrongCredentialsError, 401, "Wrong username or password"),
        (LinkExpiredError, 410, "Invitation link has been revoked"),
        (ForbiddenError, 403, "Forbidden"),
        (UnauthorizedError, 401, "Authentication required"),
        (InvalidTokenError, 401, "Invalid authentication token"),
        (TokenExpiredError, 401, "Authentication token has expired"),
    ],
)
async def test_service_errors_have_explicit_http_responses(
    exception_type, expected_status, expected_detail
):
    status_code, headers, body = await request(
        app_raising(exception_type("Internal details should not be exposed"))
    )
    assert status_code == expected_status
    assert body == {"detail": expected_detail}
    assert headers[b"content-type"] == b"application/json"
    if expected_status == 401:
        assert headers[b"www-authenticate"] == b"Bearer"
    else:
        assert b"www-authenticate" not in headers


@pytest.mark.asyncio
async def test_exception_subclasses_use_the_registered_parent():
    class ChatNotFoundError(EntityNotFoundError):
        pass

    status_code, _, body = await request(app_raising(ChatNotFoundError()))
    assert status_code == 404
    assert body == {"detail": "Entity not found"}


@pytest.mark.asyncio
async def test_http_exceptions_keep_their_response_and_headers():
    status_code, headers, body = await request(
        app_raising(HTTPException(429, "Try later", headers={"Retry-After": "10"}))
    )
    assert status_code == 429
    assert body == {"detail": "Try later"}
    assert headers[b"retry-after"] == b"10"


@pytest.mark.asyncio
async def test_request_validation_still_returns_422():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/{number}")
    async def endpoint(number: int):
        return number

    status_code, _, body = await request(app, "/not-a-number")
    assert status_code == 422
    assert body["detail"][0]["loc"] == ["path", "number"]


@pytest.mark.asyncio
@pytest.mark.parametrize("exception_type", [RuntimeError, UniqueConstraintError])
async def test_unexpected_and_repository_errors_are_not_translated(exception_type):
    with pytest.raises(exception_type):
        await request(app_raising(exception_type("Unexpected failure")))
