from src.application.interfaces.services import ISearchService
from src.main.config.settings import Settings
from src.application.interfaces.repositories import BaseArticleRepository
from src.presentation.schemas.articles import SearchSchema


class SearchPostgresqlService(ISearchService):
    """ Service for Search """

    def __init__(
        self,
        settings: Settings,
        article_repository: BaseArticleRepository,
    ):
        """Initialize Jwt token settings."""
        self.article_repository = article_repository


    async def full_text_search(self, search_schema: SearchSchema):
        result_in_article_title = await self.article_repository.search_in_article_title(search_schema)
        search_result = result_in_article_title
        return search_result
