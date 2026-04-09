from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.games import router as games_router
from app.api.routes.health import router as health_router
from app.api.routes.search import router as search_router
from app.core.config import settings
from app.core.logging_config import configure_logging


configure_logging()

app = FastAPI(
    title="Cloud Native Game Discovery Platform",
    version="1.0.0",
    description="AI-powered cloud native game discovery backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(search_router)
app.include_router(games_router)


@app.get("/")
def root():
    return {
        "service": "cloud-native-game-discovery-platform",
        "status": "running",
        "version": "1.0.0",
        "project_name": settings.PROJECT_NAME,
    }
