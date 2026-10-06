from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .base import BaseDTO


@dataclass(frozen=True)
class UserDTO(BaseDTO):
    id: UUID
    login: str
    hashed_pass: str
    visible_nickname: str
    created_at: datetime
