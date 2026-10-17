import secrets
from uuid import UUID

from core.unit_of_work.core import UnitOfWork
from core.unit_of_work.decorator import transactional

from ..dto import CurrentUser, InvitationLinkDTO
from ..exceptions.common import EntityNotFoundError, ForbiddenError, LinkExpiredError
from ..repositories import ChatRepository, InvitationLinkRepository, RoleRepository


class InvitationLinkService:
    def __init__(
        self,
        invitation_link_repo: InvitationLinkRepository,
        chat_repo: ChatRepository,
        role_repo: RoleRepository,
        current_user: CurrentUser,
        uow: UnitOfWork,
    ) -> None:
        self._invitation_link_repo = invitation_link_repo
        self._role_repo = role_repo
        self._chat_repo = chat_repo
        self._current_user_id = current_user.id
        self._uow = uow

    @transactional
    async def issue(self, chat_id: UUID) -> InvitationLinkDTO:
        if not (await self._role_repo.is_admin(self._current_user_id, chat_id)):
            raise ForbiddenError

        token = secrets.token_urlsafe(16)

        await self._invitation_link_repo.set_revoked(chat_id)
        link = await self._invitation_link_repo.add(
            user_id=self._current_user_id, chat_id=chat_id, token=token
        )
        return link

    @transactional
    async def follow(self, token: str) -> UUID:
        links = await self._invitation_link_repo.get_by("token", token)
        if not links:
            raise EntityNotFoundError
        link = links[0]
        if link.revoked_at is not None:
            raise LinkExpiredError

        await self._chat_repo.add_user(self._current_user_id, link.chat_id)
        return link.chat_id

    @transactional
    async def revoke(self, chat_id: UUID) -> None:
        if not (await self._role_repo.is_admin(self._current_user_id, chat_id)):
            raise ForbiddenError

        result = await self._invitation_link_repo.set_revoked(chat_id)
        if not result:
            raise EntityNotFoundError
