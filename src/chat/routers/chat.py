from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from ..schemas.chat import Chat, CreateRequestBody, CreateResponse, GetUserChatsResponse
from ..services import ChatService

router = APIRouter(prefix="/chat", route_class=DishkaRoute)

@router.post("/")
async def create_chat(
    body: CreateRequestBody, chat_service: FromDishka[ChatService]
) -> CreateResponse:
    chat = await chat_service.create_chat(body.name)
    response = CreateResponse.model_validate(chat, from_attributes=True)
    return response


@router.get("/")
async def get_user_chats(chat_service: FromDishka[ChatService]) -> GetUserChatsResponse:
    chats = await chat_service.get_user_chats()
    response = GetUserChatsResponse(
        data=[Chat.model_validate(chat, from_attributes=True) for chat in chats]
    )
    return response
