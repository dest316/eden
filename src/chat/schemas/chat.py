from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Chat(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    admin_id: UUID


class CreateRequestBody(BaseModel):
    name: str


class CreateResponse(BaseModel):
    chat: Chat


class GetUserChatsResponse(BaseModel):
    data: list[Chat]


class IssueLinkRequestBody(BaseModel):
    chat_id: UUID


class IssueLinkResponse(BaseModel):
    id: UUID
    chat_id: UUID
    created_by: UUID
    token: str
    created_at: datetime
    revoked_at: datetime | None


class RevokeLinkRequestBody(IssueLinkRequestBody):
    ...


class RevokeLinkResponse(BaseModel):
    status: str = Field(default="OK")


class FollowLinkResponse(BaseModel):
    chat_id: UUID
