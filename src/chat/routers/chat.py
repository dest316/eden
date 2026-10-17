from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from ..schemas import chat as chat_schemas
from ..services import ChatService, InvitationLinkService

router = APIRouter(prefix="/chat", route_class=DishkaRoute)

@router.post("/")
async def create_chat(
    body: chat_schemas.CreateRequestBody, chat_service: FromDishka[ChatService]
) -> chat_schemas.CreateResponse:
    chat = await chat_service.create_chat(body.name)
    response = chat_schemas.CreateResponse.model_validate(chat, from_attributes=True)
    return response


@router.get("/")
async def get_user_chats(chat_service: FromDishka[ChatService]) -> chat_schemas.GetUserChatsResponse:
    chats = await chat_service.get_user_chats()
    response = chat_schemas.GetUserChatsResponse(
        data=[chat_schemas.Chat.model_validate(chat, from_attributes=True) for chat in chats]
    )
    return response


@router.post("/issue_link")
async def issue_link(
    body: chat_schemas.IssueLinkRequestBody,
    invitation_link_service: FromDishka[InvitationLinkService],
) -> chat_schemas.IssueLinkResponse:
    link = await invitation_link_service.issue(body.chat_id)
    return chat_schemas.IssueLinkResponse.model_validate(link, from_attributes=True)


@router.post("/revoke_link")
async def revoke_link(
    body: chat_schemas.RevokeLinkRequestBody,
    invitation_link_service: FromDishka[InvitationLinkService],
) -> chat_schemas.RevokeLinkResponse:
    await invitation_link_service.revoke(body.chat_id)
    return chat_schemas.RevokeLinkResponse()


@router.post("/invite/{token}")
async def follow_link(
    token: str, invitation_link_service: FromDishka[InvitationLinkService]
) -> chat_schemas.FollowLinkResponse:
    chat_id = await invitation_link_service.follow(token)
    return chat_schemas.FollowLinkResponse(chat_id=chat_id)
