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



# ==================================================================================================================================
# TODO delete this code after testing

from fastapi import UploadFile


# TODO delete this entrypoint after testing
@router.post("/test_section_with_slider/")
async def save_article_section_with_image(article_id: int, 
                                          text: str,
                                          intex_number_in_article: str,
                                          image: UploadFile):
    



    print('***')
    print(article_id)
    print(text)
    print(intex_number_in_article)
    print(image)
    print('****')

    
        query = select(UserTable).filter(UserEntity.email == user_email)
        user = await self._session.execute(query)
        result = user.first()
        return result


    return {"result": "success!!"}

