from typing import TYPE_CHECKING


from fastapi import FastAPI
from src.presentation.routing.articles import router as articles_router
from src.presentation.routing.users import router as users_router
from src.presentation.routing.comments import router as comment_router
from src.presentation.routing.notifications import router as notifications_router
from src.presentation.routing.subscriptions import router as subscriptions_router


from src.main.config.settings import Settings
from dishka.integrations.fastapi import setup_dishka
from src.main.config.container import get_async_container
from src.infrastructure.database.engine import get_alchemy_engine
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from src.presentation.schemas.base_schemas import BaseResponseSchema

import firebase_admin
from firebase_admin import credentials



if TYPE_CHECKING:
    from dishka import AsyncContainer
    from sqlalchemy.ext.asyncio import AsyncEngine







def create_app() -> FastAPI:

    # from src.infrastructure.openapi.openapi import oauth2_scheme



    settings = Settings()
    
    alchemy_engine: AsyncEngine = get_alchemy_engine(db_settings=settings.db)

    app = FastAPI()


    if not firebase_admin._apps:
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(credential=cred, name="firebase_app")


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        error_messages_str = ""
        for error in exc.errors():
            error_dict = error['ctx']
            for key in error_dict.keys(): 
                error_messages_str += f"{key}: {error_dict[key]}"


        response = BaseResponseSchema(error=True, message=error_messages_str, data={})

        # return JSONResponse(response.model_dump(by_alias=True), status_code=400)
        return JSONResponse(response.model_dump(by_alias=True), status_code=400)


    # session middleware for authlib
    app.add_middleware(SessionMiddleware, secret_key="!secret")

    # Include the articles router
    app.include_router(articles_router)
    # include users router
    app.include_router(users_router)
    # include comment router
    app.include_router(comment_router)
    # include notification router
    app.include_router(notifications_router)
    # include subscription router
    app.include_router(subscriptions_router)


    container: AsyncContainer = get_async_container(
        settings=settings,
        alchemy_engine=alchemy_engine,
    )
    setup_dishka(container, app)

    return app



app = create_app()


