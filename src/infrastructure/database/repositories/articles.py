from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UserTable
from src.domain.entities.users.users_entities import UserEntity

from src.domain.entities.articles.articles_entities import ArticleSectionSlideShowEntity

from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.users import RegisterData
from src.infrastructure.database.utilities.get_password_hash import get_password_hash

from sqlalchemy import select





# # TODO -> application interfaces
class BaseArticleRepository(ABC):
    @abstractmethod
    async def save_section_with_image():
        raise NotImplementedError


class ArticleAlchemyRepository(BaseArticleRepository, IAlchemyRepository):
# class ArticleAlchemyRepository(IAlchemyRepository):
    async def save_section_with_image(self, 
                                    article_id,
                                    text,
                                    intex_number_in_article,
                                    image):
        new_article_sections_slide_show = ArticleSectionSlideShowEntity(article_id, text, intex_number_in_article, image)
        self._session.add(new_article_sections_slide_show)
        return self._session
    


        
