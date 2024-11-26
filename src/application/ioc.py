from dishka import Provider
from dishka import provide
from dishka import AnyOf
from dishka import Scope
from dishka import from_context


from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


from src.infrastructure.interfaces.uow import IDatabaseSession
from src.application.interfaces.gateways import IWriteFileStorageGateway


from src.infrastructure.database.repositories.users import UserAlchemyRepository
from src.infrastructure.database.repositories.articles import ArticleAlchemyRepository
from src.infrastructure.database.repositories.subscriptions import SubscriptionRepository, BaseSubscribtionRepository

from src.infrastructure.database.gateways.write_file_disc_storage_gateway import WriteFileDiscStorageGateway

from collections.abc import AsyncIterable


from src.application.interactors.articles import TestSaveObjectInteractor,\
                                            GetAllCategorysInteractor,\
                                            GetArticlesFeedInteractor,\
                                            GetArticlesDetailInteractor,\
                                            GetSlideShowInteractor,\
                                            GetVideoInteractor,\
                                            GetArticlesFeedTopStoriesInteractor,\
                                            SearchInteractors

from src.application.interactors.users import LoginRegularInteractor,\
                                            LoginGmailRequestToCloudInteractor,\
                                            LoginGmailResponseFromCloudInteractor,\
                                            RegistrationInteractor,\
                                            DeleteUserInteractor,\
                                            UpdatePasswordUserInteractor,\
                                            RefreshTokendUserInteractor

from src.application.interactors.comments import CreateCommentInteractor, ShowCommentInteractor

from src.infrastructure.database.repositories.categories import CategoryAlchemyRepository
from src.infrastructure.database.repositories.comments import CommentsAlchemyRepository
from src.infrastructure.database.repositories.unregistered_device import UnregisteredDeviceRepository


from src.application.interfaces.repositories import IAlchemyRepository, \
                                                    BaseArticleRepository, \
                                                    BaseCategoryRepository, \
                                                    BaseCommentsRepository, \
                                                    BaseUnregisteredDeviceRepository,\
                                                    BaseUserRepository

from src.main.config.settings import Settings
from src.application.services.jwt_token_service import JWTTokenService
from src.application.services.search import SearchPostgresqlService
from src.application.interfaces.services import ITokenService, ISearchService




class CommentsProvider(Provider):
    
    # interactors
    create_comment = provide(
        source=CreateCommentInteractor,
        scope=Scope.REQUEST
    )

    get_all_comments = provide(
        source=ShowCommentInteractor,
        scope=Scope.REQUEST
    )

    # repositories
    comments_repository = provide(
        source = CommentsAlchemyRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[BaseCommentsRepository, IAlchemyRepository]
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




class ArticleProvider(Provider):
    async_engine = from_context(provides=AsyncEngine, scope=Scope.APP)
    settings = from_context(provides=Settings, scope=Scope.APP)

    # article interactors

    get_all_categorys_interactor = provide(
        source=GetAllCategorysInteractor,
        scope=Scope.REQUEST
    )

    get_articles_feed_interactor = provide(
        source=GetArticlesFeedInteractor,
        scope=Scope.REQUEST
    )

    get_article_top_stories_feed_interactor = provide(
        source=GetArticlesFeedTopStoriesInteractor,
        scope=Scope.REQUEST
    )

    get_detail_article_interactor = provide(
        source=GetArticlesDetailInteractor,
        scope=Scope.REQUEST
    )

    get_slide_show_interactor = provide(
        source=GetSlideShowInteractor,
        scope=Scope.REQUEST
    )

    get_video_section = provide(
        source=GetVideoInteractor,
        scope=Scope.REQUEST
    )

    search_request_interactor = provide(
        source=SearchInteractors,
        scope=Scope.REQUEST,
    )

    search_request_service = provide(
        source=SearchPostgresqlService,
        scope=Scope.REQUEST,
        provides=ISearchService,
    )

    # repository
    article_repository = provide(
        source = ArticleAlchemyRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[BaseArticleRepository, IAlchemyRepository]
    )

    
    category_repository = provide(
        source = CategoryAlchemyRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[BaseCategoryRepository, IAlchemyRepository]
    )

    unregistered_device_repository = provide(
        source=UnregisteredDeviceRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[BaseUnregisteredDeviceRepository, IAlchemyRepository]
    )

    # gateways
    write_file_gateway = provide(source=WriteFileDiscStorageGateway,
                                 scope=Scope.REQUEST,
                                 provides=IWriteFileStorageGateway)
    
    # ------------------------------------------------------------
    # test article interactors
    article_section_with_photo_interactor = provide(
        source=TestSaveObjectInteractor,
        scope=Scope.REQUEST
    )
    # ------------------------------------------------------------


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



class UserProvider(Provider):

    async_engine = from_context(provides=AsyncEngine, scope=Scope.APP)
    settings = from_context(provides=Settings, scope=Scope.APP)


    # users interactors
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

    registration_user = provide(
        source=RegistrationInteractor,
        scope=Scope.REQUEST
    )

    delete_user_interactor = provide(
        source=DeleteUserInteractor,
        scope=Scope.REQUEST
    )

    update_password_user_interactor = provide(
        source=UpdatePasswordUserInteractor,
        scope=Scope.REQUEST
    )

    refresh_token_user_interactor = provide(
        source=RefreshTokendUserInteractor,
        scope=Scope.REQUEST
    )


    # repositories
    user_repository = provide(
        source=UserAlchemyRepository,
        scope=Scope.APP,
        provides=AnyOf[BaseUserRepository, IAlchemyRepository]
    )

    subscription_repository = provide(
        source=SubscriptionRepository,
        scope=Scope.APP,
        provides=AnyOf[BaseSubscribtionRepository, IAlchemyRepository]
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
    
    @provide(scope=Scope.APP)
    async def get_alchemy_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AnyOf[AsyncSession, IDatabaseSession]]:
        """Provide async session."""
        async with session_maker() as session:
            yield session
