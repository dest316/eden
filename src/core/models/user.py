from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .chat_participant import ChatParticipant

class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(Uuid, default=uuid4, primary_key=True)
    login: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    hashed_pass: Mapped[str] = mapped_column(Text, nullable=False)
    visible_nickname: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))

    memberships: Mapped[list["ChatParticipant"]] = relationship(back_populates="user")
