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
            one_category['extended_title'] = category.extended_title
            print('*')
            print(category.extended_title)
            print('*')
            categorys_list.append(one_category)

        result = CategorysResponse(categories=categorys_list)

        return result
    
    
    async def get_one_by_id(self, id):
        print('======REQUEST TO REPOSITORY======')
        print(id)
        query = select(CategoryEntity).filter(CategoryEntity.id==id)
        category_rows = await self._session.execute(query)
        category_entitity = category_rows.scalar()
        print(category_entitity)
        print('================================')
        return category_entitity

