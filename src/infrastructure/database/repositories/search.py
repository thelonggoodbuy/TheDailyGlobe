
from src.domain.entities.search.search_entities import SearchRequestEntity
from src.application.interfaces.repositories import IAlchemyRepository, BaseSearchRepository
from sqlalchemy import select
from sqlalchemy import func
from src.presentation.schemas.articles import SearchRequestState



class SearchAlchemyRepository(BaseSearchRepository, IAlchemyRepository):

    async def check_if_word_exist_and_update(self, search_word):
        similarity_threshold = 0.6
        term = search_word

        query = select(
            SearchRequestEntity,
                func.similarity(SearchRequestEntity.text, term),
        ).where(
            func.greatest(
                func.similarity(SearchRequestEntity.text, term)
            ) > similarity_threshold
        ).group_by(
            SearchRequestEntity.id
        )

        query_row = await self._session.execute(query)
        search_request = query_row.scalars().first()

        if search_request:
            search_request.quantity_of_search_requests += 1
            self._session.add(search_request)
            await self._session.commit()
            result = SearchRequestState.updated

        else: 
            new_request = SearchRequestEntity(text=search_word, quantity_of_search_requests=1)
            self._session.add(new_request)
            await self._session.commit()
            result = SearchRequestState.created


        return result


        

    async def save_search_word(self, search_word):
        new_search_request = SearchRequestEntity(text=search_word, quantity_of_search_requests=1)
        self._session.add(new_search_request)
        await self._session.commit()

        return True



    async def return_similar_search_request(self, search_word):
        similarity_threshold = 0.3
        term = search_word

        query = select(
            SearchRequestEntity.text,
                func.similarity(SearchRequestEntity.text, term),
        ).where(
            func.greatest(
                func.similarity(SearchRequestEntity.text, term)
            ) > similarity_threshold
        ).group_by(
            SearchRequestEntity.id
        ).order_by(SearchRequestEntity.quantity_of_search_requests.desc()).limit(6)

        query_row = await self._session.execute(query)
        search_request = query_row.scalars().all()
        return search_request
    


    async def return_most_popular_search_requests(self):
        query = select(SearchRequestEntity.text).order_by(SearchRequestEntity.quantity_of_search_requests.desc()).limit(6)
        query_row = await self._session.execute(query)
        search_request = query_row.scalars().all()
        return search_request
