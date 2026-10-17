from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from chat.dto import ChatDTO
from core.models import Chat, ChatParticipant

from .base import BaseRepository


class ChatRepository(BaseRepository):
    async def create(self, creator_id: UUID, name: str) -> ChatDTO:
        chat = Chat(name=name, admin_id=creator_id)
        chat_participant = ChatParticipant(chat=chat, user_id=creator_id)
        self.session.add_all((chat, chat_participant))
        await self.session.flush()
        return ChatDTO.from_orm_object(chat)

    async def add_user(self, user_id: UUID, chat_id: UUID) -> bool:
        stmt = (
            insert(ChatParticipant)
            .values(user_id=user_id, chat_id=chat_id)
            .on_conflict_do_nothing(
                index_elements=[ChatParticipant.chat_id, ChatParticipant.user_id]
            )
        ).returning(ChatParticipant)
        return bool(await self.session.scalar(stmt))

    async def get_by_user(self, user_id: UUID) -> list[ChatDTO]:
        query = select(Chat).join(ChatParticipant).where(ChatParticipant.user_id == user_id)
        chats = await self.session.scalars(query)
        return [ChatDTO.from_orm_object(chat) for chat in chats]

    async def get_by(self, field: str, value: Any) -> list[ChatDTO]:
        query = select(Chat).where(getattr(Chat, field) == value)
        chats = await self.session.scalars(query)
        return [ChatDTO.from_orm_object(chat) for chat in chats]
