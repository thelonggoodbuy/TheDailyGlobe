from src.domain.entities.articles.articles_entities import CategoryEntity
from src.application.interfaces.repositories import IAlchemyRepository, BaseCategoryRepository
from src.presentation.schemas.categorys import CategorysResponse
from sqlalchemy import select



class CategoryAlchemyRepository(BaseCategoryRepository, IAlchemyRepository):
    async def get_all(self) -> CategorysResponse:
        """get all categorys"""
        query = select(CategoryEntity)
        categorys_rows = await self._session.execute(query)
        category_entities = categorys_rows.scalars().all()

        categorys_list = []
        for category in category_entities:
            one_category = {}
            one_category['id'] = category.id
            one_category['title'] = category.title
            categorys_list.append(one_category)

        result = CategorysResponse(categories=categorys_list)

        return result

