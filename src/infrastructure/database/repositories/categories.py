from contextlib import asynccontextmanager

from src.domain.entities.articles.articles_entities import CategoryEntity

from src.domain.entities.articles.articles_entities import ArticleSectionSlideShowEntity

from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.users import RegisterData
from src.infrastructure.database.utilities.get_password_hash import get_password_hash
from src.presentation.schemas.categorys import CategorysResponse


from sqlalchemy import select





# # TODO -> application interfaces
class BaseCategoryRepository(ABC):
    @abstractmethod
    async def get_all():
        raise NotImplementedError


class CategoryAlchemyRepository(BaseCategoryRepository, IAlchemyRepository):
    async def get_all(self) -> CategorysResponse:
        """get all categorys"""
        query = select(CategoryEntity)
        categorys_rows = await self._session.execute(query)
        print('--->categorys_rows<---')
        print(categorys_rows)
        category_entities = categorys_rows.scalars().all()

        categorys_list = []
        for category in category_entities:
            one_category = {}
            one_category['id'] = category.id
            one_category['title'] = category.title
            categorys_list.append(one_category)

        result = CategorysResponse(categories=categorys_list)

        print('--->result<-----')
        print(result)
        print('***')

        return result

