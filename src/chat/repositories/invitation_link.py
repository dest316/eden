from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select, update

from core.models import InvitationLink

from ..dto import InvitationLinkDTO
from .base import BaseRepository


class InvitationLinkRepository(BaseRepository):
    async def add(self, user_id: UUID, chat_id: UUID, token: str) -> InvitationLinkDTO:
        link = InvitationLink(created_by=user_id, chat_id=chat_id, token=token)
        self.session.add(link)
        await self.session.flush()
        return InvitationLinkDTO.from_orm_object(link)

    async def get_by(self, field: str, value: Any) -> list[InvitationLinkDTO]:
        query = select(InvitationLink).where(getattr(InvitationLink, field) == value)
        links = await self.session.scalars(query)
        return [InvitationLinkDTO.from_orm_object(link) for link in links]

    async def get_relevant(self, chat_id: UUID) -> InvitationLinkDTO | None:
        query = select(InvitationLink).where(
            InvitationLink.chat_id == chat_id, InvitationLink.revoked_at.is_(None)
        )
        link = (await self.session.execute(query)).scalar_one_or_none()
        return None if link is None else InvitationLinkDTO.from_orm_object(link)

    async def set_revoked(self, chat_id: UUID) -> bool:
        stmt = (
            update(InvitationLink)
            .values(revoked_at=datetime.now(tz=UTC))
            .where(InvitationLink.chat_id == chat_id, InvitationLink.revoked_at.is_(None))
            .returning(InvitationLink.chat_id)
        )
        return await self.session.scalar(stmt) is not None
