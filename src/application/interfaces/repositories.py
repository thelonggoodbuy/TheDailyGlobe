from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod



# TODO generic repository/
class IAlchemyRepository(SQLAlchemyAsyncRepository):
    """Base repository class."""

    _session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Configure the repository object."""
        self._session: AsyncSession = session




class BaseArticleRepository(ABC):
    @abstractmethod
    async def save_section_with_image():
        raise NotImplementedError
    
    @abstractmethod
    async def return_article_feed():
        raise NotImplementedError
    
    @abstractmethod
    async def return_top_stories_article_feed():
        raise NotImplementedError

    @abstractmethod
    async def return_detail_article():
        raise NotImplementedError
    
    @abstractmethod
    async def update_reading_status():
        raise NotImplementedError


    @abstractmethod
    async def return_slideshow():
        raise NotImplementedError
    
    @abstractmethod
    async def get_video_section_by_id():
        raise NotImplementedError
    
    @abstractmethod
    async def search_in_article_title():
        raise NotImplementedError


class BaseCategoryRepository(ABC):
    @abstractmethod
    async def get_all():
        raise NotImplementedError
    



class BaseCommentsRepository(ABC):
    @abstractmethod
    async def create_comment():
        raise NotImplementedError
    
    @abstractmethod
    async def return_all_comments():
        raise NotImplementedError
    



class BaseSubscribtionRepository(ABC):
    @abstractmethod
    async def return_user_subscribtion_by_user_id():
        raise NotImplementedError
    
    @abstractmethod
    async def create_subscription():
        raise NotImplementedError




class BaseUnregisteredDeviceRepository(ABC):
    @abstractmethod
    async def get_or_create_unregistered_device():
        raise NotImplementedError
    
    @abstractmethod
    async def add_one_view():
        raise NotImplementedError



class BaseUserRepository(ABC):
    @abstractmethod
    async def get_user_by_email():
        raise NotImplementedError

    @abstractmethod
    async def register_user():
        raise NotImplementedError

    @abstractmethod
    async def delete_user():
        raise NotImplementedError
    
    @abstractmethod
    async def update_user():
        raise NotImplementedError
    


class BaseSearchRepository(ABC):
    @abstractmethod
    async def check_if_word_exist_and_update():
        raise NotImplementedError

    @abstractmethod
    async def save_search_word():
        raise NotImplementedError
    

class BaseNotificationsRepository(ABC):
    @abstractmethod
    async def save_registration_token():
        raise NotImplementedError
    

class BaseTariffRepository(ABC):
    @abstractmethod
    async def return_all():
        raise NotImplementedError
    

class BaseTransactionsRepository(ABC):
    @abstractmethod
    async def create_transaction():
        raise NotImplementedError
    
    @abstractmethod
    async def print_all_transaction():
        raise NotImplementedError
    
    @abstractmethod
    async def update_transaction_status_by_order_id():
        raise NotImplementedError