from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, DishkaRoute, inject
from fastapi import Depends
from src.infrastructure.openapi.openapi import bearer_scheme
from typing import Annotated

from src.presentation.schemas.comments import CreateCommentRequestData,\
                                                CommentResponseData

from src.application.interactors.comments import CreateCommentInteractor

router = APIRouter(route_class=DishkaRoute)


@router.post("/comments/create_comment", tags=["comments"])
@inject
async def create_comment(comment_data: CreateCommentRequestData,
                        token: Annotated[str, Depends(bearer_scheme)],
                        interactor: FromDishka[CreateCommentInteractor]) -> CommentResponseData:

    # print('***--->')
    # print('comment_data')
    # print(comment_data)
    # print('token')
    # print(token)
    # print('***--->')
    result = await interactor(comment_data, token)
    # result = result_unformated.model_dump(by_alias=True)
    return result
