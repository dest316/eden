from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chat.id"), primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )

    chat: Mapped["Chat"] = relationship("Chat", back_populates="memberships")
    user: Mapped["User"] = relationship("User", back_populates="memberships")
