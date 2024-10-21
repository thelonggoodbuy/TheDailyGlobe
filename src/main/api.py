from typing import TYPE_CHECKING

from fastapi import FastAPI
from src.presentation.routing.articles import router as articles_router
from src.presentation.routing.users import router as users_router
from src.main.config.settings import Settings
from dishka.integrations.fastapi import setup_dishka
from src.main.config.container import get_async_container
from src.infrastructure.database.engine import get_alchemy_engine
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordBearer


if TYPE_CHECKING:
    from dishka import AsyncContainer
    from sqlalchemy.ext.asyncio import AsyncEngine


def create_app() -> FastAPI:

    # from src.infrastructure.openapi.openapi import oauth2_scheme


    settings = Settings()
    
    alchemy_engine: AsyncEngine = get_alchemy_engine(db_settings=settings.db)

    app = FastAPI()
    # session middleware for authlib
    app.add_middleware(SessionMiddleware, secret_key="!secret")

    # Include the articles router
    app.include_router(articles_router)
    # include users router
    app.include_router(users_router)

    container: AsyncContainer = get_async_container(
        settings=settings,
        alchemy_engine=alchemy_engine,
    )
    setup_dishka(container, app)

    return app



app = create_app()


