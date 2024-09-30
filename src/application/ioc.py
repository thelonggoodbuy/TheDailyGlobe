from dishka import Provider
from dishka import provide
from dishka import AnyOf
from dishka import Scope
from dishka import from_context


from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


from src.infrastructure.interfaces.uow import IDatabaseSession
from src.infrastructure.database.repositories.users import UserAlchemyRepository

from collections.abc import AsyncIterable


from src.application.interactors.articles import ArticleInteractor
from src.application.interactors.users import LoginRegularInteractor,\
                                            LoginGmailRequestToCloudInteractor,\
                                            LoginGmailResponseFromCloudInteractor

from src.infrastructure.database.repositories.users import IAlchemyRepository


from src.main.config.settings import Settings
from src.application.services.jwt_token_service import JWTTokenService
from src.application.interfaces.services import ITokenService




# TODO rename provider and make distinct provider for articles
class ArticleProvider(Provider):

    async_engine = from_context(provides=AsyncEngine, scope=Scope.APP)
    settings = from_context(provides=Settings, scope=Scope.APP)



    article_interactor = provide(
        source=ArticleInteractor,
        scope=Scope.REQUEST
    )

    login_regular_interactor = provide(
        source=LoginRegularInteractor,
        scope=Scope.REQUEST
    )

    login_gmail_request_to_cloud_interactor = provide(
        source=LoginGmailRequestToCloudInteractor,
        scope=Scope.REQUEST
    )

    login_gmail_response_from_cloud_interactor = provide(
        source=LoginGmailResponseFromCloudInteractor,
        scope=Scope.REQUEST
    )

    token_service = provide(
        source=JWTTokenService,
        scope=Scope.APP,
        provides=ITokenService,
    )


    user_repository = provide(
        source=UserAlchemyRepository,
        scope=Scope.REQUEST,
        provides=IAlchemyRepository
    )


    @provide(scope=Scope.APP)
    def get_alchemy_session_maker(
        self,
        async_engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        """Provide async session maker."""
        return async_sessionmaker(
            async_engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )
    
    @provide(scope=Scope.REQUEST)
    async def get_alchemy_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, IDatabaseSession]]:
        """Provide async session."""
        async with session_maker() as session:
            yield session
