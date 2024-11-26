from pydantic import BaseModel
from common.base.interactor import BaseInteractor
from src.infrastructure.interfaces.uow import IDatabaseSession

from src.application.interfaces.repositories import BaseArticleRepository

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
                                                ArticleDetailDemoSchema,\
                                                ArticlesFeedTopStoriesRequestSchema,\
                                                SearchSchema, \
                                                DemoCauseSchema

from src.presentation.schemas.base_schemas import BaseResponseSchema, BaseSchema
from src.application.interfaces.services import ITokenService, ISearchService
from datetime import datetime


class ArtictleResponse(BaseModel):
    result: str
       


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
        data = {"categories":[]}
        for categoty_item in categorys_obj.categories:
            data["categories"].append(categoty_item.model_dump(by_alias=True))

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
         



class GetArticlesFeedTopStoriesInteractor(BaseInteractor):
    def __init__(self,
        db_session: IDatabaseSession,
        article_repository: BaseArticleRepository,
        settings: Settings):

        self.db_session = db_session
        self.article_repository = article_repository
        self.settings = settings

    async def __call__(self, article_feed_request_schema: ArticlesFeedTopStoriesRequestSchema) -> ArticleFeedResponseSchema:
        result_unformated = await self.article_repository.return_top_stories_article_feed(article_feed_request_schema)
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

        if token_or_device_id_extractor.is_authorized:
            subscription = await self.jwt_token_service.return_subscription_by_token(token_or_device_id_extractor.token)
        else:
            subscription = None
                    
        if not subscription:
            result = await self.return_article_for_unregistered_user(get_detail_article_schema)
        else:
            result = await self.return_article_for_registered_user(get_detail_article_schema, subscription)
        return result
    

    async def return_article_for_unregistered_user(self, get_detail_article_schema):
        article = await self.article_repository.return_detail_article(get_detail_article_schema)

        if not article.data.is_premium:
            unregistered_data = await self.unregistered_device_repository.get_or_create_unregistered_device(get_detail_article_schema)
            if unregistered_data.readed_articles < 4:
                await self.article_repository.update_reading_status(article.data.id)
                unregistered_data = await self.unregistered_device_repository.add_one_view(unregistered_data)
                result = article.model_dump(by_alias=True)
            else:
                demo_article = await self.transform_to_demo(article, demo_cause=DemoCauseSchema.four_article_limit.value)    
                result = demo_article.model_dump(by_alias=True)

        else:
            demo_article = await self.transform_to_demo(article, demo_cause=DemoCauseSchema.article_is_premium.value)
            result = demo_article.model_dump(by_alias=True)

        return result


    async def return_article_for_registered_user(self, get_detail_article_schema, subscription):
        article = await self.article_repository.return_detail_article(get_detail_article_schema)
        if not article.data.is_premium:
            await self.article_repository.update_reading_status(article.data.id)
            result = article.model_dump(by_alias=True)
        else:
            if subscription.is_active == False or subscription.expiration_date == None:
                demo_article = await self.transform_to_demo(article, demo_cause=DemoCauseSchema.article_is_premium.value)
                result = demo_article.model_dump(by_alias=True)
            if subscription.expiration_date and subscription.expiration_date >= datetime.now():
                demo_article = await self.transform_to_demo(article, demo_cause=DemoCauseSchema.subscription_expired.value)
                result = demo_article.model_dump(by_alias=True)

        return result 


    async def transform_to_demo(self, article_response: ArticlesDetailResponseSchema, demo_cause: str):

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
        article_video_sections = await self.article_repository.get_video_section_by_id(get_video_schema.id)
        video_section = VideoArticlSections(id=article_video_sections.id,
                                            text=article_video_sections.text,
                                            video_url=article_video_sections.video_url,
                                            title=article_video_sections.title,
                                            categoty_title=article_video_sections.article.category.title)

        result = VideoResponseSchema(
             error=False,
             message="",
             data=video_section
        )


        return result


class SearchInteractors(BaseInteractor):
    def __init__(self,
        db_session: IDatabaseSession,
        article_repository: BaseArticleRepository,
        search_service: ISearchService,
        settings: Settings):

        self.db_session = db_session
        self.article_repository = article_repository
        self.search_service = search_service
        self.settings = settings


    async def __call__(self, search_schema: SearchSchema):
        result = await self.search_service.full_text_search(search_schema)
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
