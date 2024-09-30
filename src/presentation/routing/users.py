from fastapi import APIRouter

from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka, inject
from src.application.interactors.users import LoginRegularInteractor,\
                                            LoginGmailRequestToCloudInteractor,\
                                            LoginGmailResponseFromCloudInteractor
from src.application.ioc import ArticleProvider
from src.presentation.schemas.users import LoginRequestData
from starlette.requests import Request
from src.main.config.settings import Settings



from pydantic import ValidationError
from fastapi.responses import JSONResponse
import json


router = APIRouter(route_class=DishkaRoute)


@router.post("/users/login_regular")
@inject
async def login_regular(login_data: LoginRequestData, 
                        interactor: FromDishka[LoginRegularInteractor]):

    result = await interactor(login_data)
    return result



@router.get("/users/login_gmail_request_to_cloud")
@inject
async def login_gmail_request_to_cloud(request: Request,
                                       interactor: FromDishka[LoginGmailRequestToCloudInteractor]):

    result = await interactor(request)
    return result


@router.get("/users/login_gmail_response_from_cloud")
@inject
async def login_gmail_response_from_cloud(request: Request,
                                          interactor: FromDishka[LoginGmailResponseFromCloudInteractor]):

    result = await interactor(request)
    return result