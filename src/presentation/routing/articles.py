from fastapi import APIRouter

from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka, inject
from src.application.interactors.articles import ArticleInteractor,\
                                                TestSaveObjectInteractor,\
                                                GetAllCategorysInteractor,\
                                                GetArticlesFeedInteractor, \
                                                GetArticlesDetailInteractor,\
                                                GetSlideShowInteractor
from src.application.ioc import ArticleProvider

from src.presentation.schemas.articles import ArticlesFeedRequestSchema, \
                                                ArticleFeedResponseSchema, \
                                                ArticlesDetailRequestSchema, \
                                                ArticlesDetailResponseSchema, \
                                                GetSlideshowRequestSchema, \
                                                SlideShowResponseSchema



router = APIRouter(route_class=DishkaRoute)




# @router.get("/articles/", tags=["articles"])
# @inject
# async def read_articles(interactor: FromDishka[ArticleInteractor]):

#     result = await interactor()
#     return result


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


@router.post("/get_detail_article/", tags=["articles"])
@inject
async def get_detail_article(get_detail_article_schema: ArticlesDetailRequestSchema,
                             interactor: FromDishka[GetArticlesDetailInteractor])-> ArticlesDetailResponseSchema:
    result = await interactor(get_detail_article_schema)

    return result



@router.post("/get_slideshow/", tags=["articles"])
@inject
async def get_slideshow(get_slideshow_schema: GetSlideshowRequestSchema,
                        interactor: FromDishka[GetSlideShowInteractor])-> SlideShowResponseSchema:
    result = await interactor(get_slideshow_schema)

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



