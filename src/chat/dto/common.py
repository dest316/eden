from dataclasses import dataclass
from uuid import UUID

from .base import BaseDTO


@dataclass(frozen=True, slots=True)
class CurrentUser(BaseDTO):
    id: UUID
