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
