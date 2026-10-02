from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from chat.routers.auth import router as auth_router

from core.bootstrap.provider import container


app = FastAPI()

app.include_router(auth_router)

setup_dishka(container=container, app=app)
