from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.research import router as research_router
from app.repositories.research_repository import (
    initialize_database,
)
from app.api.history import (
    router as history_router,
)
from app.config.logging_config import (
    configure_logging,
)

configure_logging()
from app.config.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
)


initialize_database()


app.include_router(
    health_router
)

app.include_router(
    research_router
)

app.include_router(
    history_router
)