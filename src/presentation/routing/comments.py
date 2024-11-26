from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute, inject
from fastapi import Depends
from src.infrastructure.openapi.openapi import bearer_scheme
from typing import Annotated

from src.presentation.schemas.comments import CreateCommentRequestData,\
                                                SingleCommentResponseData,\
                                                MultipleCommentResponseData, \
                                                AllCommentRequestData

from src.application.interactors.comments import CreateCommentInteractor,\
                                                ShowCommentInteractor

router = APIRouter(route_class=DishkaRoute)


@router.post("/comments/create_comment", tags=["comments"])
@inject
async def create_comment(comment_data: CreateCommentRequestData,
                        token: Annotated[str, Depends(bearer_scheme)],
                        interractor: FromDishka[CreateCommentInteractor]) -> SingleCommentResponseData:

    result = await interractor(comment_data, token)
    return result



@router.post("/comments/show_all_comment", tags=["comments"])
@inject
async def show_article_comment(comment_request_data: AllCommentRequestData,
                        token: Annotated[str, Depends(bearer_scheme)],
                        interractor: FromDishka[ShowCommentInteractor]) -> MultipleCommentResponseData:

    result = await interractor(comment_request_data, token)
    print("***")
    print(result)
    print("***")
    return result