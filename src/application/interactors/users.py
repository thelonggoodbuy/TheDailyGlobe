from pydantic import BaseModel
from common.base.interactor import BaseInteractor
from src.infrastructure.interfaces.uow import IDatabaseSession

from src.infrastructure.database.tables.users import UserTable
from starlette.requests import Request
from dataclasses import dataclass
from sqlalchemy import select

from src.presentation.schemas.users import LoginRequestData
from src.infrastructure.database.repositories.users import IAlchemyRepository

from src.application.interfaces.services import ITokenService
from src.main.config.settings import Settings



from passlib.context import CryptContext


class UserLoginResponse(BaseModel):
    result: dict
    


class LoginRegularInteractor(BaseInteractor):
    """
    Interactor for regular users login with email and password
    """

    def __init__(self,
                 db_session: IDatabaseSession,
                 user_repository: IAlchemyRepository,
                 token_service: ITokenService):

                 self.db_session = db_session
                 self.user_repository = user_repository
                 self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                 self.token_service = token_service
                 
  
    async def __call__(self,
                    login_data: LoginRequestData) -> UserLoginResponse:
        # TODO return!!!   
        user_obj = await self.user_repository.get_user_by_email(user_email=login_data.email)
        if user_obj is None:
            result = {'status': 'error', 'text': 'Користувача з таким емейлом не існує'}
        elif not self.verify_password(login_data.password, user_obj.password):
            result = {'status': 'error', 'text': 'помилка в паролі'}
        else:
            jwt_token = await self.token_service.create_access_token(user_obj.email)
            result = {'status': 'success', 'access_jwt_token': jwt_token}
        resp = UserLoginResponse(result = result)
        return resp
    
    
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
        redirect_uri = 'http://127.0.0.1:8000/users/login_gmail_response_from_cloud'
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
                user_repository: IAlchemyRepository,
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
