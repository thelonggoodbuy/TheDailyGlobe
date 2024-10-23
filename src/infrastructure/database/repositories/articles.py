from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UserTable
from src.infrastructure.database.tables.articles import CategortyTable
from src.domain.entities.users.users_entities import UserEntity

from src.domain.entities.articles.articles_entities import ArticleSectionSlideShowEntity

from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.users import RegisterData
from src.infrastructure.database.utilities.get_password_hash import get_password_hash

from sqlalchemy import select

from src.presentation.schemas.articles import ArticlesFeedRequestSchema, \
                                                ArticleFeedResponseSchema, \
                                                ArticleItem

from src.domain.entities.articles.articles_entities import ArticleEntity
from sqlalchemy.orm import selectinload

from babel.dates import format_datetime


# # TODO -> application interfaces
class BaseArticleRepository(ABC):
    @abstractmethod
    async def save_section_with_image():
        raise NotImplementedError
    @abstractmethod
    async def return_article_feed():
        raise NotImplementedError


class ArticleAlchemyRepository(BaseArticleRepository, IAlchemyRepository):
    async def save_section_with_image(self, 
                                    article_id,
                                    text,
                                    intex_number_in_article,
                                    image):
        new_article_sections_slide_show = ArticleSectionSlideShowEntity(article_id, text, intex_number_in_article, image)
        self._session.add(new_article_sections_slide_show)
        return self._session
    
    async def return_article_feed(self, article_feed_request_schema: ArticlesFeedRequestSchema) -> ArticleFeedResponseSchema:

        offset_value = article_feed_request_schema.pagination_length * article_feed_request_schema.current_pagination_position

        query = (
        select(ArticleEntity)
        .options(selectinload(ArticleEntity.category))
        .filter(ArticleEntity.category_id == article_feed_request_schema.category_id)
        .order_by(ArticleEntity.id)
        .offset(offset_value)
        .limit(article_feed_request_schema.pagination_length)
    )
        article_rows = await self._session.execute(query)
        article_objects = article_rows.scalars().all()
        response = ArticleFeedResponseSchema(articles=[])
        for article_obj in article_objects:
            print('====>article_obj.publication_date<======')
            print(article_obj.publication_date)
            print(type(article_obj.publication_date))
            print('========================================')
            article = ArticleItem(
                category_title=article_obj.category.title,
                id=article_obj.id,
                title=article_obj.title,
                author=article_obj.author,
                main_image=article_obj.main_image,
                publication_date=(format_datetime(article_obj.publication_date, format='MMMM dd, yyyy', locale='uk')).capitalize()
            )
            response.articles.append(article)

        print('===>REPOSITORY===DATA<===')
        print(response)
        print('=========================')

        

        return response
    
