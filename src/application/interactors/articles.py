from pydantic import BaseModel
from common.base.interactor import BaseInteractor
from src.infrastructure.interfaces.uow import IDatabaseSession
from src.infrastructure.database.repositories.users import IAlchemyRepository
from src.infrastructure.database.repositories.articles import BaseArticleRepository
from src.infrastructure.database.repositories.categories import BaseCategoryRepository
from src.infrastructure.database.repositories.unregistered_device import BaseUnregisteredDeviceRepository
from src.main.config.settings import Settings
from src.application.interfaces.gateways import IWriteFileStorageGateway
from src.presentation.schemas.categorys import CategorysResponse

from src.presentation.schemas.articles import ArticlesFeedRequestSchema, \
                                                ArticleFeedResponseSchema, \
                                                ArticlesDetailRequestSchema, \
                                                ArticlesDetailResponseSchema, \
                                                GetSlideshowRequestSchema, \
                                                SlideShowResponseSchema, \
                                                GetVideoSchema, \
                                                VideoArticlSections, \
                                                VideoResponseSchema, \
                                                ArticleDetailDemoSchema

from src.presentation.schemas.base_schemas import BaseResponseSchema, BaseSchema
from src.application.interfaces.services import ITokenService
from datetime import datetime


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
    

    


class GetAllCategorysInteractor(BaseInteractor):
     
    def __init__(self,
                db_session: IDatabaseSession,
                category_repository: BaseCategoryRepository,
                settings: Settings):

                self.db_session = db_session
                self.category_repository = category_repository
                self.settings = settings


    async def __call__(self) -> CategorysResponse:
        categorys_obj = await self.category_repository.get_all()

        print('===========!!!==============')

        data = {"categories":[]}
        for categoty_item in categorys_obj.categories:
            data["categories"].append(categoty_item.model_dump(by_alias=True))

        print('--->data<----')
        print(data)
        print('--------------')

        result = BaseResponseSchema(error=False, message="", data=data)
        return result



class GetArticlesFeedInteractor(BaseInteractor):
    def __init__(self,
        db_session: IDatabaseSession,
        article_repository: BaseArticleRepository,
        settings: Settings):

        self.db_session = db_session
        self.article_repository = article_repository
        self.settings = settings

    async def __call__(self, article_feed_request_schema: ArticlesFeedRequestSchema) -> ArticleFeedResponseSchema:
        result_unformated = await self.article_repository.return_article_feed(article_feed_request_schema)
        result = result_unformated.model_dump(by_alias=True)
        return result
         



class GetArticlesDetailInteractor(BaseInteractor):
    def __init__(self,
        db_session: IDatabaseSession,
        article_repository: BaseArticleRepository,
        unregistered_device_repository: BaseUnregisteredDeviceRepository,
        jwt_token_service: ITokenService,

        settings: Settings):

        self.db_session = db_session
        self.article_repository = article_repository
        self.settings = settings
        self.jwt_token_service = jwt_token_service
        self.unregistered_device_repository = unregistered_device_repository

    async def __call__(self, get_detail_article_schema: ArticlesDetailRequestSchema, token_or_device_id_extractor) -> ArticlesDetailResponseSchema:
        print('++++++++++++++++ESTRACTOR DATA++++++++++++++++++++++++++')
        print(token_or_device_id_extractor)
        print(get_detail_article_schema)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        if token_or_device_id_extractor.is_authorized:
            subscription = await self.jwt_token_service.return_subscription_by_token(token_or_device_id_extractor.token)
        else:
            subscription = None
            
            

            # print('--->subscriptions<---')
            # print(subscription)
            # print(type(subscription))
            # print(subscription.expiration_date)
            # print(type(subscription.expiration_date))
            # # print(type(subscription.expiration_date))
            # print('---------------------')

        print('====================================================================')
        print(subscription)
        print('====================================================================')
        
        # if not subscription or subscription.is_active == False or subscription.expiration_date >= datetime.now():
        if not subscription:
            result = await self.return_article_for_unregistered_user(get_detail_article_schema)
        else:
            result = await self.return_article_for_registered_user(get_detail_article_schema, subscription)
        return result
    

    async def return_article_for_unregistered_user(self, get_detail_article_schema):
        article = await self.article_repository.return_detail_article(get_detail_article_schema)

        if not article.data.is_premium:
            # здесь мы проверяем 
            unregistered_data = await self.unregistered_device_repository.get_or_create_unregistered_device(get_detail_article_schema)
            if unregistered_data.readed_articles < 4:
                await self.article_repository.update_reading_status(article.data.id)
                unregistered_data = await self.unregistered_device_repository.add_one_view(unregistered_data)
                result = article.model_dump(by_alias=True)
            else:
                demo_article = await self.transform_to_demo(article, demo_cause="Ви вже прочитали доступні сьогодні 4 статті. Будьласка зареєструйтеся")    
                result = demo_article.model_dump(by_alias=True)

        else:
            demo_article = await self.transform_to_demo(article, demo_cause="Преміум статті не доступні для незареєстрованих читачів.")
            result = demo_article.model_dump(by_alias=True)




        return result


    async def return_article_for_registered_user(self, get_detail_article_schema, subscription):
        article = await self.article_repository.return_detail_article(get_detail_article_schema)
        if not article.data.is_premium:
            # if subscription
            await self.article_repository.update_reading_status(article.data.id)
            result = article.model_dump(by_alias=True)
        else:
            print('---111subscription111---')
            print(subscription)
            print('------------------------')
            if subscription.is_active == False:
                demo_article = await self.transform_to_demo(article, demo_cause="Ваша підписка не активна.")
                result = demo_article.model_dump(by_alias=True)
            if subscription.expiration_date or subscription.expiration_date >= datetime.now():
                demo_article = await self.transform_to_demo(article, demo_cause="Ваша підписка застаріла і не активна. Оплатіть період користування.")
                result = demo_article.model_dump(by_alias=True)


        # print('***')
        # print('------------article-for-REGISTERED-user------------')
        # print(article.data)
        # print('***')
        # result = article.model_dump(by_alias=True)
        return result 


    async def transform_to_demo(self, article_response: ArticlesDetailResponseSchema, demo_cause: str):
        print('----aritle_response----')
        # print(artile_response)
        print(type(article_response.data))
        print(article_response.data)
        print('aritle_response')
        full_version = article_response.data
        article_response.data = ArticleDetailDemoSchema(
            is_demo = True,
            is_demo_cause = demo_cause,
            id = full_version.id,
            title = full_version.title,
            main_image = full_version.main_image,
            category_id = full_version.category_id,
            lead = full_version.lead,
            author = full_version.author,
            publication_date = full_version.publication_date,
            category_title = full_version.category_title,
            is_premium = full_version.is_premium
        )
        return article_response


class GetSlideShowInteractor(BaseInteractor):

    def __init__(self,
        db_session: IDatabaseSession,
        article_repository: BaseArticleRepository,
        settings: Settings):

        self.db_session = db_session
        self.article_repository = article_repository
        self.settings = settings


    async def __call__(self, get_slideshow_schema: GetSlideshowRequestSchema) -> SlideShowResponseSchema:
        result = await self.article_repository.return_slideshow(get_slideshow_schema)
        return result



class GetVideoInteractor(BaseInteractor):
    def __init__(self,
                db_session: IDatabaseSession,
                article_repository: BaseArticleRepository,
                settings: Settings):
        
        self.db_session = db_session
        self.article_repository = article_repository
        self.settings = settings

    async def __call__(self, 
                       get_video_schema: GetVideoSchema):
        print('==============get==vide====interactor=========1========')
        article_video_sections = await self.article_repository.get_video_section_by_id(get_video_schema.id)
        print('==============get==vide====interactor=========2========')
        video_section = VideoArticlSections(id=article_video_sections.id,
                                            text=article_video_sections.text,
                                            video_url=article_video_sections.video_url,
                                            title=article_video_sections.title,
                                            categoty_title=article_video_sections.article.category.title)
                                            # categoty_title='заглушка')
        print('==============get==vide====interactor=========3========')

        result = VideoResponseSchema(
             error=False,
             message="",
             data=video_section
        )


        return result


# =========================TEST========INTERACTORS=========================


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
