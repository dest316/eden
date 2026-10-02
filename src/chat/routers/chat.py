from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter


router = APIRouter(prefix="/chat", route_class=DishkaRoute)
