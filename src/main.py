from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from chat.exception_handlers import register_exception_handlers
from chat.routers import auth_router, chat_router
from core.bootstrap.provider import container

app = FastAPI()
register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(chat_router)

setup_dishka(container=container, app=app)
