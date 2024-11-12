from fastapi import APIRouter

from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka, inject
from src.application.interactors.articles import ArticleInteractor,\
                                                TestSaveObjectInteractor,\
                                                GetAllCategorysInteractor,\
                                                GetArticlesFeedInteractor, \
                                                GetArticlesDetailInteractor,\
                                                GetSlideShowInteractor,\
                                                GetVideoInteractor
from src.application.ioc import ArticleProvider

from src.presentation.schemas.articles import ArticlesFeedRequestSchema, \
                                                ArticleFeedResponseSchema, \
                                                ArticlesDetailRequestSchema, \
                                                ArticlesDetailResponseSchema, \
                                                GetSlideshowRequestSchema, \
                                                SlideShowResponseSchema, \
                                                GetVideoSchema, \
                                                VideoResponseSchema
from typing import Annotated, Optional
from fastapi import Depends
from src.infrastructure.openapi.openapi import bearer_scheme, bearer_scheme_for_pages_with_unregistered_users



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









def bearer_or_device_id_extractor(
    token: Annotated[str, Depends(bearer_scheme)],
    get_detail_article_schema: ArticlesDetailRequestSchema
):
    if not token:
        print('================YOU ARE NOT WITH BEARER================')
        print(token)
        # return last_query
    else:
        print('=========YOU ARE WITH SCHEMA WIRH DEVICE ID=========')
        print(get_detail_article_schema)








# @router.post("/get_detail_article/", tags=["articles"])
# @inject
# async def get_detail_article(get_detail_article_schema: ArticlesDetailRequestSchema,
#                              interactor: FromDishka[GetArticlesDetailInteractor],
#                              token: Annotated[str, Depends(bearer_scheme_for_pages_with_unregistered_users)])-> ArticlesDetailResponseSchema:
    

@router.post("/get_detail_article/", tags=["articles"])
@inject
async def get_detail_article(get_detail_article_schema: ArticlesDetailRequestSchema,
                             interactor: FromDishka[GetArticlesDetailInteractor],
                             token_or_device_id_extractor: Annotated[str, Depends(bearer_or_device_id_extractor)])-> ArticlesDetailResponseSchema:

    # if token:
    #     unformated_result = await interactor(get_detail_article_schema, token)
    #     result = unformated_result.model_dump(by_alias=True)
    # else:
    # unformated_result = await interactor(get_detail_article_schema, token)
    # result = unformated_result.model_dump(by_alias=True)

        # result = ArticlesDetailResponseSchema(error=False, message='', data={"result": "you want to register from other device!"})

    # result = token_or_device_id_extractor
    result = ArticlesDetailResponseSchema(error=False, message='', data={"result": "whatch the print!"})

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




# --------------------------TEST--------DATA----------ROUTINGS-----------------------------

from fastapi import UploadFile, File

@router.post("/test_section_with_slider/", tags=["test_endpoint"])
async def save_article_section_with_image(article_id: int, 
                                        text: str,
                                        intex_number_in_article: int,
                                        interactor: FromDishka[TestSaveObjectInteractor],
                                        image: UploadFile = File(...)):
    

    result = await interactor(article_id=article_id, text=text, intex_number_in_article=intex_number_in_article, file=image)
    return result



