from uuid import UUID

from sqlalchemy import select

from core.models import Chat, ChatParticipant

from .base import BaseRepository


class RoleRepository(BaseRepository):
    async def is_admin(self, user_id: UUID, chat_id: UUID) -> bool:
        query = select(Chat).where(Chat.id == chat_id, Chat.admin_id == user_id)
        is_exists = await self.session.scalar(query)
        return bool(is_exists)

    async def is_member(self, user_id: UUID, chat_id: UUID) -> bool:
        query = select(ChatParticipant).where(
            ChatParticipant.user_id == user_id, ChatParticipant.chat_id == chat_id
        )
        is_exists = await self.session.scalar(query)
        return bool(is_exists)
