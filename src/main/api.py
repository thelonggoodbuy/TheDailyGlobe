from typing import TYPE_CHECKING

from fastapi import FastAPI
from src.presentation.routing.articles import router as articles_router
from src.presentation.routing.users import router as users_router
from src.presentation.routing.comments import router as comment_router
from src.main.config.settings import Settings
from dishka.integrations.fastapi import setup_dishka
from src.main.config.container import get_async_container
from src.infrastructure.database.engine import get_alchemy_engine
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from src.presentation.schemas.base_schemas import BaseResponseSchema



if TYPE_CHECKING:
    from dishka import AsyncContainer
    from sqlalchemy.ext.asyncio import AsyncEngine







def create_app() -> FastAPI:

    # from src.infrastructure.openapi.openapi import oauth2_scheme


    settings = Settings()
    
    alchemy_engine: AsyncEngine = get_alchemy_engine(db_settings=settings.db)

    app = FastAPI()


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        print('***exc***')
        print(exc)
        print('*********')
        print(exc.body)
        print('*********')
        # print(exc.errors()[0]['ctx']['error'])
        # error_obj = exc.errors()[0]['ctx']['error']
        for error in exc.errors():
            print('--->error<---')
            print(error)
            print('-------------')

            error_obj = error['ctx']['error'].args[0] 

            print('this is error obj:')
            print(type(error_obj))
            print(error_obj)
            # print(error_obj.__dict__)
            print('*********')
            # return error_obj
            response = BaseResponseSchema(error=True, message=error_obj, data={})

            return JSONResponse(response.model_dump(by_alias=True), status_code=400)


    # session middleware for authlib
    app.add_middleware(SessionMiddleware, secret_key="!secret")

    # Include the articles router
    app.include_router(articles_router)
    # include users router
    app.include_router(users_router)
    # include comment router
    app.include_router(comment_router)


    container: AsyncContainer = get_async_container(
        settings=settings,
        alchemy_engine=alchemy_engine,
    )
    setup_dishka(container, app)

    return app



app = create_app()


