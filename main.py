from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.endpoints import auth, bot, embedding, users, agent
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup operations can be added here if needed

def create_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)

    # Set all CORS enabled origins
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(auth.router, prefix=settings.API_V1_STR)
    application.include_router(bot.router, prefix=f"{settings.API_V1_STR}/bot", tags=["bot"])
    application.include_router(agent.router, prefix=f"{settings.API_V1_STR}/agent", tags=["agent"])
    application.include_router(embedding.router, prefix=f"{settings.API_V1_STR}/embedding", tags=["embedding"])
    application.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

    return application

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)