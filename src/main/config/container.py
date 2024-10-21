
from dishka import AsyncContainer
from dishka import make_async_container
from src.application.ioc import ArticleProvider, UserProvider
from src.main.config.settings import Settings
from sqlalchemy.ext.asyncio import AsyncEngine




def get_async_container(
        settings: Settings,
        alchemy_engine: AsyncEngine,
) -> AsyncContainer:
    """Get dependency container."""
    # article_provider = ArticleProvider()
    
    return make_async_container(ArticleProvider(),
                                UserProvider(),
                                context={
                                    Settings: settings,
                                    AsyncEngine: alchemy_engine,
                                }   
                                )
