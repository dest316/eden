from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.common import SenderType

from .base import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class Message(Base):
    __tablename__ = "message"

    id: Mapped[UUID] = mapped_column(Uuid, default=uuid4, primary_key=True)

    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id"), nullable=False)
    sender_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id"), nullable=True)

    sender_type: Mapped[SenderType] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    reply_to_message_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("message.id"), nullable=True
    )
    persona_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    sender: Mapped["User | None"] = relationship("User")
