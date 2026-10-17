from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .base import BaseDTO


@dataclass(frozen=True)
class InvitationLinkDTO(BaseDTO):
    id: UUID
    chat_id: UUID
    created_by: UUID
    token: str  
    created_at: datetime
    revoked_at: datetime | None
