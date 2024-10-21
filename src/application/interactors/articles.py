from pydantic import BaseModel
from common.base.interactor import BaseInteractor
from src.infrastructure.interfaces.uow import IDatabaseSession
from src.infrastructure.database.repositories.users import IAlchemyRepository
from src.infrastructure.database.repositories.articles import BaseArticleRepository
from src.main.config.settings import Settings
from src.application.interfaces.gateways import IWriteFileStorageGateway


class ArtictleResponse(BaseModel):
    result: str
    

class Service_One():
    async def __call__(self):
        print('Service One called by interactor')
        return 'Article from service one'


class Service_Two():
    async def __call__(self):
        print('Service Two called by interactor')
        return 'Article from service two'


class ArticleInteractor(BaseInteractor):
    """
    Test Interactor for returning random object
    """

    async def __call__(self) -> ArtictleResponse:
        print('===You want to get all articles!===')
        resp = ArtictleResponse(result = 'Articles!')
        # resp.
        return resp
    




class TestSaveObjectInteractor(BaseInteractor):
    """
    Test Interactor for saving article section with image
    """

    def __init__(self,
                db_session: IDatabaseSession,
                article_repository: BaseArticleRepository,
                settings: Settings,
                write_file_gateway: IWriteFileStorageGateway):

                self.db_session = db_session
                self.article_repository = article_repository
                self.settings = settings
                self.write_file_gateway = write_file_gateway


    async def __call__(self,
                        article_id, 
                        text, 
                        intex_number_in_article, 
                        file) -> ArtictleResponse:
        

        upload_directory ="/galery/"
        stopped_session = await self.article_repository.save_section_with_image(article_id=article_id,
                                                              text=text,
                                                              intex_number_in_article=intex_number_in_article,
                                                              image=f"{upload_directory}{file.filename}")
        await stopped_session.flush()
        success: bool = await self.write_file_gateway.safe_file_in_storage(upload_directory, file)
        if not success:
            raise Exception("-----Проблема с сохранением файла-----")
        await stopped_session.commit()
        result = ArtictleResponse(result = 'sawing file work!!')

        return result