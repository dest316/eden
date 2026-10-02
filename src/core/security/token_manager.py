from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from core.types.common import TokenType


# Вынести в exceptions/
class TokenExpiredError(Exception):
    ...


class InvalidTokenError(Exception):
    ...


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class TokenPayload:
    sub: UUID
    type: TokenType
    issued_at: datetime
    expires_at: datetime


from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt


class TokenManager:
    ALGORITHM = "HS256"

    def __init__(
        self,
        secret: str,
        access_ttl: timedelta,
        refresh_ttl: timedelta,
    ) -> None:
        self._secret = secret
        self._access_ttl = access_ttl
        self._refresh_ttl = refresh_ttl

    def create_access_token(self, user_id: UUID) -> str:
        return self._create_token(
            user_id=user_id,
            token_type=TokenType.ACCESS,
            ttl=self._access_ttl,
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        return self._create_token(
            user_id=user_id,
            token_type=TokenType.REFRESH,
            ttl=self._refresh_ttl,
        )

    def decode_access_token(self, token: str) -> TokenPayload:
        return self._decode_token(
            token,
            expected_type=TokenType.ACCESS,
        )


    def decode_refresh_token(self, token: str) -> TokenPayload:
        return self._decode_token(
            token,
            expected_type=TokenType.REFRESH,
        )

    def _create_token(
        self,
        user_id: UUID,
        token_type: TokenType,
        ttl: timedelta,
    ) -> str:
        now = datetime.now(UTC)

        payload = {
            "sub": str(user_id),
            "type": token_type.value,
            "iat": now,
            "exp": now + ttl,
        }

        return jwt.encode(
            payload,
            self._secret,
            algorithm=self.ALGORITHM,
        )

    def _decode_token(
        self,
        token: str,
        expected_type: TokenType,
    ) -> TokenPayload:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[self.ALGORITHM],
                options={
                    "require": ["sub", "type", "iat", "exp"],
                },
            )
        except jwt.ExpiredSignatureError as exc:
            raise TokenExpiredError from exc
        except jwt.InvalidTokenError as exc:
            raise InvalidTokenError from exc

        if payload["type"] != expected_type:
            raise InvalidTokenError

        try:
            return TokenPayload(
                sub=UUID(payload["sub"]),
                type=TokenType(payload["type"]),
                issued_at=datetime.fromtimestamp(
                    payload["iat"],
                    tz=UTC,
                ),
                expires_at=datetime.fromtimestamp(
                    payload["exp"],
                    tz=UTC,
                ),
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise InvalidTokenError from exc