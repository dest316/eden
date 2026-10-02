from enum import StrEnum


class SenderType(StrEnum):
    EDEN = "eden"
    USER = "user"


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
