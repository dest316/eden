from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class InvitationLink(Base):
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chat.id", ondelete="CASCADE"), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    token: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index(
            "uq_active_invite_per_chat",
            "chat_id",
            unique=True,
            postgresql_where=revoked_at.is_(None),
        ),
        Index("ix_invitation_link_chat_id", "chat_id"),
    )
    __tablename__ = "invitation_link"
