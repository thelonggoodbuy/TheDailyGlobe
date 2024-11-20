from src.application.interfaces.services import ISearchService
from src.main.config.settings import Settings

from src.infrastructure.database.repositories.articles import BaseArticleRepository

from src.presentation.schemas.articles import SearchSchema






# class BaseSearchService()







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
        print('---------')
        print(search_schema)
        print('---------')

        result_in_article_title = await self.article_repository.search_in_article_title(search_schema)

        search_result = result_in_article_title

        return search_result
        # if is_refresh:
        #     expire = datetime.now(timezone.utc) + timedelta(days=28)
        # else:
        #     # expire = datetime.now(timezone.utc) + timedelta(minutes=10)
        #     expire = datetime.now(timezone.utc) + timedelta(minutes=20)
        # to_encode = {'email': email, "exp": expire}
        # encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        # return encoded_jwt