from fastapi import APIRouter

from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka, inject
from src.application.interactors.articles import TestSaveObjectInteractor,\
                                                GetAllCategorysInteractor,\
                                                GetArticlesFeedInteractor, \
                                                GetArticlesDetailInteractor,\
                                                GetSlideShowInteractor,\
                                                GetVideoInteractor,\
                                                GetArticlesFeedTopStoriesInteractor,\
                                                SearchInteractors,\
                                                SaveOrUpdateSearchWordInteractor,\
                                                ReturnPopularArticlesInSearch

from src.application.ioc import ArticleProvider

from src.presentation.schemas.articles import ArticlesFeedRequestSchema, \
                                                ArticleFeedResponseSchema, \
                                                ArticlesDetailRequestSchema, \
                                                ArticlesDetailResponseSchema, \
                                                GetSlideshowRequestSchema, \
                                                SlideShowResponseSchema, \
                                                GetVideoSchema, \
                                                VideoResponseSchema,\
                                                BearerOrDeviceIdExtractorResult, \
                                                ArticlesFeedTopStoriesRequestSchema, \
                                                SearchSchema
from typing import Annotated, Optional
from fastapi import Depends
from src.infrastructure.openapi.openapi import bearer_scheme, bearer_scheme_for_pages_with_unregistered_users
from fastapi.responses import JSONResponse



router = APIRouter(route_class=DishkaRoute)


@router.get("/all_categorys/", tags=["articles"])
@inject
async def all_categorys(interactor: FromDishka[GetAllCategorysInteractor]):

    result = await interactor()
    return result



@router.post("/get_articles_feed/", tags=["articles"])
@inject
async def get_articles_feed(article_feed_request_schema: ArticlesFeedRequestSchema, 
                        interactor: FromDishka[GetArticlesFeedInteractor]) -> ArticleFeedResponseSchema:

    result = await interactor(article_feed_request_schema)
    return result



@router.post("/get_top_stories_feed/", tags=["articles"])
@inject
async def get_top_stories_feed(article_feed_top_stories_request_schema: ArticlesFeedTopStoriesRequestSchema, 
                        interactor: FromDishka[GetArticlesFeedTopStoriesInteractor]):
    result = await interactor(article_feed_top_stories_request_schema)
    return result






def bearer_or_device_id_extractor(
    token: Annotated[str, Depends(bearer_scheme_for_pages_with_unregistered_users)],
    get_detail_article_schema: ArticlesDetailRequestSchema
) -> BearerOrDeviceIdExtractorResult:
    if token:
        print('=========YOU ARE WITH SCHEMA WIRH TOKEN=========')
        print(get_detail_article_schema)
        print('===')
        print(token)
        print('===')
        result = BearerOrDeviceIdExtractorResult(is_authorized=True, token=token.credentials)
        # если есть токен и юзер авторизован, то мы проверяем есть ли у пользователь премиум:
        # 1.1. если есть - то открываем любую статью и добавляем единичку к количеству просмотров
        # 1.2. если нет - то проверяем премиум ли статья.
        # 1.2.1 если нет премиума - возвращаем только лид и не добавляем единицу к просмотрам
        # 1.2.2 если есть премиум - открыавем всю статью и добавляем единицу к просмотру
    else:
        print('================YOU ARE Not authenticated user================')
        if get_detail_article_schema.unregistered_device == None:
            return JSONResponse(status_code=403, content={"error": True, "message": "Для незареєстрованиих користувачів потрібна дата про девайс", "data":[]})
        result = BearerOrDeviceIdExtractorResult(is_authorized=False)
        # print(token)
        # если токена нет и пользователь не авторизован, то проверяем премиум ли статья:
        # 2.1. если статья премиум - возвращаем только лид и не добавляем единицу к просмотрам
        # 2.2. если статья НЕ премиум, то делаем запрос к unregistered_device с registration_id:
        # 2.2.1. если readed_articles_today < 4, то добавляем к readed_articles_today 1 и добавляем единичку к просмотрам
        # 2.2.2. если readed_articles_today >= 4, то к readed_articles_today и просмотрам не добавляем единицу и возвращаем толкьо лид
        
    return result

from typing import Annotated

from fastapi import Body, FastAPI



@router.post("/get_detail_article/", tags=["articles"])
@inject
async def get_detail_article(get_detail_article_schema: Annotated[ArticlesDetailRequestSchema, Body(
            openapi_examples={
                "Request for authorized user": {
                    "summary": "Request for authorized user",
                    "description": "This request required JWT token too.",
                    "value": {
                        "articleId": 2
                    },
                },
                "Request for unauthorized user": {
                    "summary": "Request for unauthorized user",
                    "description": "Request require data about device operation system and data about device.",
                    "value": {
                        "articleId": 2,
                        "unregisteredDevice": {
                            "deviceId": "432423fdsfsd",
                            "deviceType": "android",
                            "registrationId": "fdafsdafsda"
                        }
                    },
                },
            },
        ),

],
                             interactor: FromDishka[GetArticlesDetailInteractor],
                             token_or_device_id_extractor: Annotated[str, Depends(bearer_or_device_id_extractor)])-> ArticlesDetailResponseSchema:

    if type(token_or_device_id_extractor) == JSONResponse:
        return token_or_device_id_extractor
    result = await interactor(get_detail_article_schema, token_or_device_id_extractor)
       

    return result



@router.post("/get_slideshow/", tags=["articles"])
@inject
async def get_slideshow(get_slideshow_schema: GetSlideshowRequestSchema,
                        interactor: FromDishka[GetSlideShowInteractor])-> SlideShowResponseSchema:
    result = await interactor(get_slideshow_schema)

    return result


@router.post("/get_video/", tags=["articles"])
@inject
async def get_video(get_video_schema: GetVideoSchema,
                    interactor: FromDishka[GetVideoInteractor]) -> VideoResponseSchema:
    result = await interactor(get_video_schema)
    return result


@router.post("/full_text_search/", tags=["search"])
@inject
async def full_text_search(search_schema: SearchSchema,
                           interactor: FromDishka[SearchInteractors]):

    result = await interactor(search_schema)
    return result


@router.post("/save_search_word_and_return_similar/", tags=["search"])
@inject
async def save_or_update_search_word(search_word: str,
                           interactor:FromDishka[SaveOrUpdateSearchWordInteractor]):
    result = await interactor(search_word)
    
    return result


@router.post("/return_popular_articles/", tags=["search"])
@inject
async def return_similar_search(interactor:FromDishka[ReturnPopularArticlesInSearch],
                                return_popular_article_in_search: ArticlesFeedTopStoriesRequestSchema):
    result = await interactor(return_popular_article_in_search)
    
    return result


# --------------------------TEST--------DATA----------ROUTINGS-----------------------------

from fastapi import UploadFile, File

@router.post("/test_section_with_slider/", tags=["test_endpoint"])
async def save_article_section_with_image(article_id: int, 
                                        text: str,
                                        index_number_in_article: int,
                                        interactor: FromDishka[TestSaveObjectInteractor],
                                        image: UploadFile = File(...)):
    

    result = await interactor(article_id=article_id, text=text, index_number_in_article=index_number_in_article, file=image)
    return result



