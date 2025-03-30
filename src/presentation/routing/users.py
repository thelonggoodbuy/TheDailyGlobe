from fastapi import APIRouter

from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, DishkaRoute, inject
from src.application.interactors.users import LogOutRegularInteractor, LoginRegularInteractor,\
                                            LoginGmailRequestToCloudInteractor,\
                                            LoginGmailResponseFromCloudInteractor,\
                                            RegistrationInteractor,\
                                            DeleteUserInteractor,\
                                            UpdatePasswordUserInteractor,\
                                            RefreshTokendUserInteractor
from src.application.ioc import ArticleProvider
from src.presentation.schemas.base_schemas import BaseResponseSchema
from src.presentation.schemas.users import LogOutRequestData, LoginRequestData, RegisterData, DeleteUsersData, ChangePasswordUsersData, RefreshTokenUsersData, UserRegisterResponse
from starlette.requests import Request
from src.main.config.settings import Settings
from src.infrastructure.openapi.openapi import bearer_scheme

from fastapi import status
from fastapi.responses import JSONResponse

from typing import Annotated
from fastapi import Depends



router = APIRouter(route_class=DishkaRoute)


@router.post("/users/login_regular", tags=["Auth"])
@inject
async def login_regular(login_data: LoginRequestData, 
                        interactor: FromDishka[LoginRegularInteractor]) -> BaseResponseSchema:

    result = await interactor(login_data)

    return result


@router.post("/users/logout_regular", tags=["Auth"])
@inject
async def login_regular(logout_data: LogOutRequestData, 
                        interactor: FromDishka[LogOutRegularInteractor]) -> BaseResponseSchema:

    result = await interactor(logout_data)

    return result


@router.get("/users/login_gmail_request_to_cloud", tags=["Auth"])
@inject
async def login_gmail_request_to_cloud(request: Request,
                                       interactor: FromDishka[LoginGmailRequestToCloudInteractor]):

    result = await interactor(request)
    return result


@router.get("/users/login_gmail_response_from_cloud", tags=["Auth"])
@inject
async def login_gmail_response_from_cloud(request: Request,
                                          interactor: FromDishka[LoginGmailResponseFromCloudInteractor]):

    result = await interactor(request)
    return result


@router.post("/users/registration", tags=["users_profile"])
@inject
async def registration(register_data: RegisterData,
                        interactor: FromDishka[RegistrationInteractor]) -> BaseResponseSchema:
    
    result_unformatted = await interactor(register_data)
    # result = result_unformatted.model_dump(by_alias=True)
    return result_unformatted





@router.post("/users/delete_user", tags=["users_profile"])
@inject
async def delete_user(delete_user_data: DeleteUsersData, 
                      token: Annotated[str, Depends(bearer_scheme)],
                      interactor: FromDishka[DeleteUserInteractor]):

    result_unformated = await interactor(delete_user_data, token.credentials)
    result = result_unformated.model_dump(by_alias=True)
    return result




@router.post("/users/change_password", tags=["users_profile"])
@inject
async def change_password(change_password_user_data: ChangePasswordUsersData, 
                      token: Annotated[str, Depends(bearer_scheme)],
                      interactor: FromDishka[UpdatePasswordUserInteractor]):

    result_unformated = await interactor(change_password_user_data, token.credentials)
    if type(result_unformated) == JSONResponse:
        return result_unformated
    else:
        result = result_unformated.model_dump(by_alias=True)
        # return result
        if result_unformated.error:
            return JSONResponse(content=result, status_code=status.HTTP_400_BAD_REQUEST)

        return JSONResponse(content=result, status_code=status.HTTP_200_OK)




@router.post("/users/refresh_token", tags=["Auth"])
@inject
async def refresh_token(refresh_token: RefreshTokenUsersData,
                      interactor: FromDishka[RefreshTokendUserInteractor]):

    result = await interactor(refresh_token)

    return result