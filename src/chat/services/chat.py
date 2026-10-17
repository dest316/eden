from chat.dto import ChatDTO, CurrentUser
from core.unit_of_work.decorator import UnitOfWork, transactional

from ..repositories import ChatRepository


class ChatService:
    def __init__(self, chat_repo: ChatRepository, current_user: CurrentUser, uow: UnitOfWork) -> None:
        self._chat_repo = chat_repo
        self._current_user_id = current_user.id
        self._uow = uow

    @transactional
    async def create_chat(self, name: str) -> ChatDTO:
        chat = await self._chat_repo.create(self._current_user_id, name)
        return chat

    @transactional
    async def get_user_chats(self) -> list[ChatDTO]:
        chats = await self._chat_repo.get_by_user(self._current_user_id)
        return chats
