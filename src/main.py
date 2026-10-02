from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from core.bootstrap.provider import container


app = FastAPI()

setup_dishka(container=container, app=app)
