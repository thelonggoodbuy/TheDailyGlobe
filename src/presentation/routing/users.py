from fastapi import APIRouter

from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, DishkaRoute, setup_dishka, inject
from src.application.interactors.users import LoginRegularInteractor,\
                                            LoginGmailRequestToCloudInteractor,\
                                            LoginGmailResponseFromCloudInteractor,\
                                            RegistrationInteractor,\
                                            DeleteUserInteractor,\
                                            UpdatePasswordUserInteractor,\
                                            RefreshTokendUserInteractor
from src.application.ioc import ArticleProvider
from src.presentation.schemas.users import LoginRequestData, RegisterData, DeleteUsersData, ChangePasswordUsersData, RefreshTokenUsersData
from starlette.requests import Request
from src.main.config.settings import Settings
from src.infrastructure.openapi.openapi import bearer_scheme

from typing import Annotated
from fastapi import Depends



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


@router.post("/users/registration")
@inject
async def registration(register_data: RegisterData,
                        interactor: FromDishka[RegistrationInteractor]):

    result = await interactor(register_data)
    return result





@router.post("/users/delete_user")
@inject
async def delete_user(delete_user_data: DeleteUsersData, 
                      token: Annotated[str, Depends(bearer_scheme)],
                      interactor: FromDishka[DeleteUserInteractor]):

    result = await interactor(delete_user_data, token.credentials)

    return result




@router.post("/users/change_password")
@inject
async def delete_user(change_password_user_data: ChangePasswordUsersData, 
                      token: Annotated[str, Depends(bearer_scheme)],
                      interactor: FromDishka[UpdatePasswordUserInteractor]):

    result = await interactor(change_password_user_data, token.credentials)

    return result



@router.post("/users/refresh_token")
@inject
async def refresh_token(refresh_token: RefreshTokenUsersData,
                      interactor: FromDishka[RefreshTokendUserInteractor]):

    result = await interactor(refresh_token)

    return result