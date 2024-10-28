from pydantic import BaseModel
from common.base.interactor import BaseInteractor
from src.infrastructure.interfaces.uow import IDatabaseSession

from src.infrastructure.database.tables.users import UserTable
from starlette.requests import Request
from dataclasses import dataclass
from sqlalchemy import select

from src.presentation.schemas.users import LoginRequestData, RegisterData, UserRegisterResponse, LoginUserSuccessData, LoginSuccessDataSchema
from src.presentation.schemas.base_schemas import BaseResponseSchema

from src.infrastructure.database.repositories.users import IAlchemyRepository

from src.infrastructure.database.repositories.users import BaseUserRepository
from src.infrastructure.database.repositories.subscriptions import BaseSubscribtionRepository
from sqlalchemy.exc import IntegrityError

from src.application.interfaces.services import ITokenService
from src.main.config.settings import Settings

import asyncpg





from passlib.context import CryptContext


class UserLoginResponse(BaseModel):
    result: dict
    


class LoginRegularInteractor(BaseInteractor):
    """
    Interactor for regular users login with email and password
    """

    def __init__(self,
                 db_session: IDatabaseSession,
                 user_repository: BaseUserRepository,
                 subscription_repository: BaseSubscribtionRepository,
                 token_service: ITokenService):

                 self.db_session = db_session
                 self.user_repository = user_repository
                 self.subscription_repository = subscription_repository
                 self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                 self.token_service = token_service
                 
  
    async def __call__(self,
                    login_data: LoginRequestData) -> BaseResponseSchema:
        # TODO return!!!   
        user_obj = await self.user_repository.get_user_by_email(user_email=login_data.email)
        if user_obj is None:
            # result = {'status': 'error', 'text': 'Користувача з таким емейлом не існує'}
            result = BaseResponseSchema(error=True, message='Користувача з таким емейлом не існує', data={})
        elif not self.verify_password(login_data.password, user_obj.password):
            # result = {'status': 'error', 'text': 'помилка в паролі'}
            result = BaseResponseSchema(error=True, message='помилка в паролі', data={})
        else:
            jwt_token = await self.token_service.create_access_token(user_obj.email)
            refresh_token = await self.token_service.create_access_token(user_obj.email, is_refresh=True)
            # print('===>user_data<===') 
            # print(user_obj)
            # print('=================')

            subscription = await self.subscription_repository.return_user_subscribtion_by_user_id(user_id=user_obj.id)

            if subscription:
                subscription_data = subscription
            else:
                subscription_data = 'unregistered_user'

            user_data = LoginUserSuccessData(id=user_obj.id,
                                             email=user_obj.email)

            data = LoginSuccessDataSchema(
                    access_token=jwt_token, 
                    refresh_token=refresh_token,
                    user_data=user_data.model_dump(by_alias=True), 
                    subscription_data=subscription_data)
            # resp = UserLoginResponse(result = result)
            # print('=======data=======')
            # print(data)
            # print('==================')
            result = BaseResponseSchema(error=False, message='', data=data.model_dump(by_alias=True))
        print('=========RESULT=========')
        print(result)
        print('========================')
        return result
    
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    

#TODO add fields in BaseInteractor
class LoginGmailRequestToCloudInteractor(BaseInteractor):
    """
    Interactor for request to gmail authorisation
    """

    def __init__(self,
                db_session: IDatabaseSession,
                settings: Settings):
        """initialize interactor"""
        self.db_session = db_session
        self.settings = settings



    async def __call__(self,
                       request: Request) -> UserLoginResponse:
       
        auth_obj = self.settings.google_auth.google_auth_object
        redirect_uri = 'http://127.0.0.1:3004/users/login_gmail_response_from_cloud'
        auth_url = await auth_obj.google.create_authorization_url(redirect_uri, **{"prompt": 'select_account'})
        await auth_obj.google.save_authorize_data(request, redirect_uri=str(redirect_uri), **auth_url)
        resp = UserLoginResponse(result = {'response':auth_url})

        return resp
    

class LoginGmailResponseFromCloudInteractor(BaseInteractor):
    """
    Interactor for hadhandling request to gmail authorisation
    """

    def __init__(self,
                db_session: IDatabaseSession,
                user_repository: BaseUserRepository,
                settings: Settings,
                 token_service: ITokenService
                ):
        """initialize interactor"""
        self.db_session = db_session
        self.settings = settings
        self.user_repository = user_repository
        self.token_service = token_service


    async def __call__(self,
                       request: Request) -> UserLoginResponse:
       
        auth_obj = self.settings.google_auth.google_auth_object
        token = await auth_obj.google.authorize_access_token(request)
        data = token.get('userinfo')
        user_email = data['email']

        user_obj = await self.user_repository.get_user_by_email(user_email=user_email)
        if user_obj is None:
            result = {'status': 'error', 'text': 'Користувача з таким емейлом не існує'}
        else:
            jwt_token = await self.token_service.create_access_token(user_obj.email)
            result = {'status': 'success', 'access_jwt_token': jwt_token}
        resp = UserLoginResponse(result = result)
        return resp


class RegistrationInteractor(BaseInteractor):
    """
    Interactor for user registration
    """

    def __init__(self,
                db_session: IDatabaseSession,
                user_repository: BaseUserRepository,
                subscription_repository: BaseSubscribtionRepository,
                settings: Settings,
                token_service: ITokenService
                ):
        """initialize interactor"""
        self.db_session = db_session
        self.settings = settings
        self.user_repository = user_repository
        self.subscription_repository = subscription_repository
        self.token_service = token_service


    async def __call__(self,
                    register_data: RegisterData) -> BaseResponseSchema:
        
        print('===>>>This is my register data!<<<====')
        print(register_data)
        print('======================================')

        try:
            user_obj = await self.user_repository.register_user(register_data)
            access_token = await self.token_service.create_access_token(user_obj.email)
            refresh_token = await self.token_service.create_access_token(user_obj.email, is_refresh=True)
            subscription = await self.subscription_repository.return_user_subscribtion_by_user_id(user_id=user_obj.id)

            if subscription:
                subscription_data = subscription
            else:
                subscription_data = 'unregistered_user'

            user_data = LoginUserSuccessData(id=user_obj.id,
                                                email=user_obj.email)

            data = LoginSuccessDataSchema(
                    access_token=access_token, 
                    refresh_token=refresh_token,
                    user_data=user_data.model_dump(by_alias=True), 
                    subscription_data=subscription_data)

            result = BaseResponseSchema(error=False, message='', data=data.model_dump(by_alias=True))

        except IntegrityError as e:

            # print('************')
            # print(e.__dict__)
            # print('*****')
            # print(e.orig)
            # print('*******')
            # print('***1***')
            # print(e.statement)
            # print(type(e.statement))
            # print('***2***')
            # print(e.params)
            # print(type(e.params))
            # print('***3***')
            # print(e.orig)
            # print('*')
            # print(type(e.orig))
            # print('*')
            # print(str(e.orig))
            # print('***4***')
            # print(e.hide_parameters)
            # print(type(e.hide_parameters))
            # print('***5***')
            # print(e.connection_invalidated)
            # print(type(e.connection_invalidated))
            # print('************')

            # if isinstance(e.orig, asyncpg.exceptions.UniqueViolationError):
            #     print(e.orig)
            if 'duplicate key value violates unique constraint "users_email_key"' in str(e.orig):
                await self.db_session.rollback()
                # raise ValueError("Користувач з таким емейлом існує.")
                result = BaseResponseSchema(error=True, message='Користувач з таким емейлом існує.', data={})

            # else:
            #     raise ValueError(f"Ошибка при регистрации: {str(e.orig)}")

        return result
    

class DeleteUserInteractor(BaseInteractor):
    """
    Interactor for user registration
    """ 
    def __init__(self,
                db_session: IDatabaseSession,
                user_repository: BaseUserRepository,
                settings: Settings,
                token_service: ITokenService
                ):
        """initialize interactor"""
        self.db_session = db_session
        self.settings = settings
        self.user_repository = user_repository
        self.token_service = token_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def __call__(self,
                       delete_user_data,
                       token):

        user_obj = await self.token_service.get_user_by_token(token)
        if not user_obj.is_valid:
            # return {"error": user_obj.error_text}
            result = BaseResponseSchema(error=True, message=user_obj.error_text, data={})
            return result
        password_valid = self.verify_password(plain_password=delete_user_data.password, 
                                   hashed_password=user_obj.user_password)
        if not password_valid:
            # return {"error": "Помилка в паролі."}
            result = BaseResponseSchema(error=True, message="Помилка в паролі", data={})
            return result
        result_message = await self.user_repository.delete_user(user_obj.user_email)
        result = BaseResponseSchema(error=False, message="", data=result_message)
        return result



    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)




class UpdatePasswordUserInteractor(BaseInteractor):
    """
    Interactor for update users password
    """ 
    def __init__(self,
                db_session: IDatabaseSession,
                user_repository: BaseUserRepository,
                settings: Settings,
                token_service: ITokenService
                ):
        """initialize interactor"""
        self.db_session = db_session
        self.settings = settings
        self.user_repository = user_repository
        self.token_service = token_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def __call__(self,
                       update_password_users_data,
                       token):

        user_obj = await self.token_service.get_user_by_token(token)
        if not user_obj.is_valid:
            result = BaseResponseSchema(error=True, message=user_obj.error_text, data={})
            return result
        password_valid = self.verify_password(plain_password=update_password_users_data.old_password, 
                                   hashed_password=user_obj.user_password)
        if not password_valid:
            result = BaseResponseSchema(error=True, message="Помилка в паролі.", data={})
            return result
        user = await self.user_repository.get_user_by_email(user_obj.user_email)
        repository_result = await self.user_repository.update_user(user, **{"password": update_password_users_data.new_password})
        result = BaseResponseSchema(error=False, message="", data=repository_result)

        return result

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)





class RefreshTokendUserInteractor(BaseInteractor):
    """
    Interactor for update access token by using refresh token
    """ 
    def __init__(self,
                db_session: IDatabaseSession,
                user_repository: BaseUserRepository,
                settings: Settings,
                token_service: ITokenService
                ):
        """initialize interactor"""
        self.db_session = db_session
        self.settings = settings
        self.user_repository = user_repository
        self.token_service = token_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    async def __call__(self,
                       refresh_token_obj):

        user_obj = await self.token_service.get_user_by_token(refresh_token_obj.refresh_token)
        if not user_obj.is_valid:
            result = BaseResponseSchema(error=True, message=user_obj.error_text, data={})
            return result
        
        token_dict = await self.token_service.refresh_token(refresh_token=refresh_token_obj.refresh_token)
        result = BaseResponseSchema(error=False, message="", data=token_dict)
        return result

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)