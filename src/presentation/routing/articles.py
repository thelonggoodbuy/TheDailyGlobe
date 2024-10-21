from fastapi import APIRouter

from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka, inject
from src.application.interactors.articles import ArticleInteractor, TestSaveObjectInteractor
from src.application.ioc import ArticleProvider





router = APIRouter(route_class=DishkaRoute)




@router.get("/articles/")
@inject
async def read_articles(interactor: FromDishka[ArticleInteractor]):

    result = await interactor()
    return result



# ==================================================================================================================================
# TODO delete this code after testing

from fastapi import UploadFile, File

@router.post("/test_section_with_slider/", tags=["test_endpoint"])
async def save_article_section_with_image(article_id: int, 
                                        text: str,
                                        intex_number_in_article: int,
                                        interactor: FromDishka[TestSaveObjectInteractor],
                                        image: UploadFile = File(...)):
    

    result = await interactor(article_id=article_id, text=text, intex_number_in_article=intex_number_in_article, file=image)

    return result

