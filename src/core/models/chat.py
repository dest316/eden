from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .chat_participant import ChatParticipant
    from .message import Message


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[UUID] = mapped_column(Uuid, default=uuid4, primary_key=True)
    admin_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))

    admin: Mapped["User"] = relationship("User")
    memberships: Mapped[list["ChatParticipant"]] = relationship(back_populates="chat")
    messages: Mapped[list["Message"]] = relationship(back_populates="chat")
