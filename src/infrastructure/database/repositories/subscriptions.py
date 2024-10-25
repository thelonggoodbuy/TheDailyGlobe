from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UserTable
from src.infrastructure.database.tables.articles import CategortyTable
from src.domain.entities.users.users_entities import SubscriptionEntity

from src.domain.entities.articles.articles_entities import ArticleSectionSlideShowEntity,\
                                                        ArticleWithPlainTextSectionEntity,\
                                                        ArticleWithVideoSectionEntity


from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.subscriptions import SubscriptionResponseSchema
from src.infrastructure.database.utilities.get_password_hash import get_password_hash

from sqlalchemy import select

from src.presentation.schemas.articles import ArticlesFeedRequestSchema, \
                                                ArticleFeedResponseSchema, \
                                                ArticleItem, \
                                                ArticlesDetailRequestSchema, \
                                                ArticlesDetailResponseSchema


from src.domain.entities.articles.articles_entities import ArticleEntity
from sqlalchemy.orm import selectinload

from babel.dates import format_datetime


# # TODO -> application interfaces
class BaseSubscribtionRepository(ABC):
    @abstractmethod
    async def return_user_subscribtion_by_user_id():
        raise NotImplementedError


class SubscriptionRepository(BaseSubscribtionRepository, IAlchemyRepository):
    async def return_user_subscribtion_by_user_id(self, user_id) -> SubscriptionResponseSchema | None:

        query = select(SubscriptionEntity).filter(SubscriptionEntity.user_id == user_id)
        user = await self._session.execute(query)
        result = user.scalar_one_or_none()
        return result