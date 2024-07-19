# app/api/api_v1/api.py
from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users, bot, embedding

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bot.router, prefix="/bot", tags=["bot"])
api_router.include_router(embedding.router, prefix="/embedding", tags=["embedding"])

