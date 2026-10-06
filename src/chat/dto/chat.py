from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .base import BaseDTO


@dataclass(frozen=True)
class ChatDTO(BaseDTO):
    id: UUID
    admin_id: UUID
    name: str
    created_at: datetime
