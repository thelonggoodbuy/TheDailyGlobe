from fastapi import APIRouter

from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka, inject
from src.application.interactors.articles import ArticleInteractor
from src.application.ioc import ArticleProvider





router = APIRouter(route_class=DishkaRoute)




@router.get("/articles/")
@inject
async def read_articles(interactor: FromDishka[ArticleInteractor]):

    result = await interactor()
    return result

