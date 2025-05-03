from pydantic import BaseModel
from common.base.interactor import BaseInteractor
from src.infrastructure.interfaces.uow import IDatabaseSession

from starlette.requests import Request

from src.presentation.schemas.users import LogOutRequestData, LoginRequestData, RegisterData, LoginUserSuccessData, LoginSuccessDataSchema, RegisterGoogleData, UserDataSchema
from src.presentation.schemas.base_schemas import BaseResponseSchema

from sqlalchemy.exc import IntegrityError

from src.application.interfaces.services import INotificationService, ITokenService
from src.application.interfaces.repositories import BaseSubscribtionRepository, BaseUserRepository
from src.main.config.settings import Settings
from fastapi import status
from fastapi.responses import JSONResponse
from src.presentation.schemas.subscriptions import SubscriptionResponseSchema
import os
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
        user_obj = await self.user_repository.get_user_by_email(user_email=login_data.email)
        if user_obj is None:
            result = BaseResponseSchema(error=True, message='Користувача з таким емейлом не існує', data={})
            return JSONResponse(status_code=401, content=result.model_dump())

        elif not self.verify_password(login_data.password, user_obj.password):
            result = BaseResponseSchema(error=True, message='помилка в паролі', data={})
            return JSONResponse(status_code=401, content=result.model_dump())
        else:
            jwt_token = await self.token_service.create_access_token(user_obj.email)
            refresh_token = await self.token_service.create_access_token(user_obj.email, is_refresh=True)

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
                    subscription_data=str(subscription_data))
            result = BaseResponseSchema(error=False, message='', data=data.model_dump(by_alias=True))

        return result
    
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    

class LogOutRegularInteractor(BaseInteractor):
    """
    Interactor for request to base logout
    """
    def __init__(self,
                 db_session: IDatabaseSession,
                 user_repository: BaseUserRepository,
                 subscription_repository: BaseSubscribtionRepository,
                 notification_service: INotificationService,
                 token_service: ITokenService):

                 self.db_session = db_session
                 self.user_repository = user_repository
                 self.subscription_repository = subscription_repository
                 self.notification_service = notification_service
                 self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                 self.token_service = token_service

    async def __call__(self,
                    logout_data: LogOutRequestData) -> BaseResponseSchema:

        token = logout_data.refresh_token
        user_obj = await self.token_service.get_user_by_token(token)
        if not user_obj.is_valid:
            result = BaseResponseSchema(
                error=True,
                message=user_obj.error_text,
                data=None
            )
            return JSONResponse(status_code=401, content=result.model_dump())
        
        black_list_entity = await self.user_repository.add_to_blacklist(logout_data)
        await self.notification_service.stop_notification(logout_data.registration_id, user_obj.id)
        print('=========================================')
        print(black_list_entity)
        print('=========================================')
        return BaseResponseSchema(error=False, message='', data={"result": "success"})


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
        print(request.session)

        redirect_uri = os.environ.get('GOOGLE_REDIRECT_URL')


        # ***work only in browser
        auth_url = await auth_obj.google.create_authorization_url(redirect_uri, **{"prompt": 'select_account'})
        await auth_obj.google.save_authorize_data(request, redirect_uri=str(redirect_uri), **auth_url)
        response_data = {'error': False, 'message': '', 'data': auth_url}
        return JSONResponse(status_code=302, content=response_data)
    

class LoginGmailResponseFromCloudInteractor(BaseInteractor):
    """
    Interactor for hadhandling request to gmail authorisation
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
                       request: Request) -> UserLoginResponse:
       
        auth_obj = self.settings.google_auth.google_auth_object
        
        token = await auth_obj.google.authorize_access_token(request)
        data = token.get('userinfo')
        user_email = data['email']


        user_obj = await self.user_repository.get_user_by_email(user_email=user_email)
        print("==============================")
        print(user_obj)
        print("==============================")
        if user_obj is None:
            # TODO: make registration here
            # self.user_repository.register_google_user(RegisterGoogleData(email=user_email))

            # result = {'error': True, 'message': 'Користувача з таким емейлом не існує', 'data': []}
            # return JSONResponse(status_code=401, content=result)

            user_obj = await self.user_repository.register_google_user(RegisterGoogleData(email=user_email))
            await self.subscription_repository.create_subscription(user_id=user_obj.id)
            access_token = await self.token_service.create_access_token(user_obj.email)
            refresh_token = await self.token_service.create_access_token(user_obj.email, is_refresh=True)
            subscription = await self.subscription_repository.return_user_subscribtion_by_user_id(user_id=user_obj.id)

            if subscription:
                subscription_data = SubscriptionResponseSchema(expiration_date=subscription.expiration_date, 
                                                                is_active=subscription.is_active)
            else:
                subscription_data = None

            user_data = LoginUserSuccessData(id=user_obj.id,
                                                email=user_obj.email)

            data = LoginSuccessDataSchema(
                    access_token=access_token, 
                    refresh_token=refresh_token,
                    user_data=user_data.model_dump(by_alias=True), 
                    subscription_data=subscription_data)

            result_data = BaseResponseSchema(error=False, message='', data=data.model_dump(by_alias=True))
            result = JSONResponse(content=result_data.model_dump(mode='json'), status_code=status.HTTP_200_OK)

            
        elif user_obj and user_obj.is_registered_throw_google == True:
            # authentication 
            jwt_token = await self.token_service.create_access_token(user_obj.email)
            refresh_token = await self.token_service.create_access_token(user_obj.email, is_refresh=True)

            data = {'error': False, 'message': '', 'data': {'access_token': jwt_token, 'refresh_token': refresh_token}}
            result = JSONResponse(status_code=200, content=data)
        
        else:
            result = {'error': True, 'message': 'Користувача з таким емейлом зареєструвався через емейл та пароль. Аутентифікуйтеся в такий спосіб, будь ласка.', 'data': []}
            return JSONResponse(status_code=401, content=result)

        return result


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
        

        user_obj = await self.user_repository.get_user_by_email(user_email=register_data.email)
        if user_obj and user_obj.is_registered_throw_google == False:
            result_data = BaseResponseSchema(error=True, message='Користувач з таким емейлом існує.', data={})
            result = JSONResponse(content=result_data.model_dump(mode='json'), status_code=status.HTTP_400_BAD_REQUEST)
        elif user_obj and user_obj.is_registered_throw_google == True:
            result_data = BaseResponseSchema(error=True, message='Користувач з таким емейлом зареєструвався через гугл аккаунт. аутентифікуйтеся через нього..', data={})
            result = JSONResponse(content=result_data.model_dump(mode='json'), status_code=status.HTTP_400_BAD_REQUEST)
        else:
            user_obj = await self.user_repository.register_user(register_data)
            await self.subscription_repository.create_subscription(user_id=user_obj.id)
            access_token = await self.token_service.create_access_token(user_obj.email)
            refresh_token = await self.token_service.create_access_token(user_obj.email, is_refresh=True)
            subscription = await self.subscription_repository.return_user_subscribtion_by_user_id(user_id=user_obj.id)

            if subscription:
                subscription_data = SubscriptionResponseSchema(expiration_date=subscription.expiration_date, 
                                                                is_active=subscription.is_active)
            else:
                subscription_data = None

            user_data = LoginUserSuccessData(id=user_obj.id,
                                                email=user_obj.email)

            data = LoginSuccessDataSchema(
                    access_token=access_token, 
                    refresh_token=refresh_token,
                    user_data=user_data.model_dump(by_alias=True), 
                    subscription_data=subscription_data)

            result_data = BaseResponseSchema(error=False, message='', data=data.model_dump(by_alias=True))
            result = JSONResponse(content=result_data.model_dump(mode='json'), status_code=status.HTTP_200_OK)

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
            result = BaseResponseSchema(error=True, message=user_obj.error_text, data={})
            return JSONResponse(status_code=401, content=result.model_dump())
        password_valid = self.verify_password(plain_password=delete_user_data.password, 
                                   hashed_password=user_obj.user_password)
        if not password_valid:
            result = BaseResponseSchema(error=True, message="Помилка в паролі", data={})
            return JSONResponse(status_code=401, content=result.model_dump())
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

            return JSONResponse(status_code=401, content=result.model_dump())
        
        password_valid = self.verify_password(plain_password=update_password_users_data.old_password, 
                                   hashed_password=user_obj.user_password)
        if not password_valid:
            result = BaseResponseSchema(error=True, message="Помилка в паролі.", data={})
            return JSONResponse(status_code=401, content=result.model_dump())
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
        print('=====!!!user_obj!!!======')
        print(type(user_obj))
        print('===================')
        if not user_obj.is_valid:
            result = BaseResponseSchema(error=True, message=user_obj.error_text, data={})
            return JSONResponse(status_code=401, content=result.model_dump())
        
        token_dict = await self.token_service.refresh_token(refresh_token=refresh_token_obj.refresh_token)
        result = BaseResponseSchema(error=False, message="", data=token_dict)
        return result

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    



class GetUserDataInteractor(BaseInteractor):
    """
    Interactor for get user data
    """ 
    def __init__(self,
                db_session: IDatabaseSession,
                user_repository: BaseUserRepository,
                # settings: Settings,
                subscription_repository: BaseSubscribtionRepository,
                token_service: ITokenService
                ):
        """initialize interactor"""
        self.db_session = db_session
        # self.settings = settings
        self.subscription_repository = subscription_repository
        self.user_repository = user_repository
        self.token_service = token_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def __call__(self,
                       token):

        # print('===========TOKEN==================')
        # print(token)
        # print('==================================')

        user_obj = await self.token_service.get_user_by_token(token.credentials)
        
        if not user_obj.is_valid:
            result = BaseResponseSchema(error=True, message=user_obj.error_text, data={})

            return JSONResponse(status_code=401, content=result.model_dump())
        
        user = await self.user_repository.get_user_by_email(user_obj.user_email)
        subscription = await self.subscription_repository.return_user_subscribtion_by_user_id(user.id)

        print('--->subscription<----')
        print(subscription)
        # print(subscription.expiration_date.strftime("%m/%d/%Y, %H:%M:%S"))
        if subscription.expiration_date:
            # print('subscription exist')
            expiration_date = subscription.expiration_date
            # print(expiration_date)
        else:
            # print('subscription NOT exist')
            expiration_date = None
            # print(expiration_date)
        print('---------------------')

        
        data = {
            "email": user.email,
            "is_registered_throw_google": user.is_registered_throw_google,
            "expiration_date": expiration_date,
            "is_active_subscription": subscription.is_active if subscription else None,
        }


        user_data = UserDataSchema(**data)

        print('=================user_data===============')
        print(user_data)
        print(type(user_data))
        print('-----dictionary date-------')
        print(data)
        print('=========================================')
        
        result = BaseResponseSchema(error=False, message="", data=user_data.model_dump(by_alias=True))

        return result
