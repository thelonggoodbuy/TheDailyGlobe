from datetime import datetime, timedelta, timezone


import jwt


from src.application.interfaces.services import ITokenService
from src.main.config.settings import Settings

from jwt.exceptions import DecodeError, InvalidTokenError
from src.application.interfaces.repositories import IAlchemyRepository
from src.infrastructure.database.repositories.users import BaseUserRepository


from pydantic import BaseModel
import time


class TokenResponse(BaseModel):
    is_valid: bool
    id: int = None
    error_text: str = None
    user_email: str = None
    user_password: str = None




class JWTTokenService(ITokenService):
    """ Service for JWT Token logic """

    def __init__(
        self,
        settings: Settings,
        user_repository: BaseUserRepository
    ):
        """Initialize Jwt token settings."""
        self.secret_key: str = settings.jwt_token.SECRET_KEY
        self.algorithm: str = settings.jwt_token.ALGORITHM
        self.user_repository = user_repository



    async def create_access_token(self, email: str, is_refresh=False) -> str:
        if is_refresh:
            expire = datetime.now(timezone.utc) + timedelta(days=28)
        else:
            # expire = datetime.now(timezone.utc) + timedelta(minutes=10)
            expire = datetime.now(timezone.utc) + timedelta(minutes=20)
        to_encode = {'email': email, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    

    async def refresh_token(self, refresh_token: str) -> str:
        token_status = await self.validate_token(refresh_token)
        match token_status.is_valid:
            case True:
                print('Token valid')
                # user = await self.get_user_by_payload(token_status.user_email)
                # response = TokenResponse(is_valid=True, user_email=user.email, user_password=user.password)
                # return response
                encoded_jwt = await self.create_access_token(email=token_status.user_email)
                return {"access_token": encoded_jwt}
            
            case False:
                print('Token false')
                print(token_status)
                return token_status




    async def validate_token(self, token: str):
        is_token_in_black_list = await self.user_repository.check_if_token_in_blacklist(token)
        # print('***is_token_in_black_list***')
        # print(is_token_in_black_list)
        # print('***')
        if is_token_in_black_list:
            # print('***1***')
            response = TokenResponse(is_valid=False, error_text="Токен не валідний")
        else:
            # print('***2***')
            try:
                payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
                if int(payload['exp']) < int(time.time()):
                    raise InvalidTokenError
                response = TokenResponse(is_valid=True, user_email=payload['email'])
                return response
            except DecodeError:
                response = TokenResponse(is_valid=False, error_text="Токен не валідний")
                return response
            except InvalidTokenError:
                response = TokenResponse(is_valid=False, error_text="Токен застарів")
        return response
            

    async def get_user_by_token(self, token: str):
        token_status = await self.validate_token(token)

        match token_status.is_valid:
            case True:
                user = await self.get_user_by_payload(token_status.user_email)
                print('_______')
                print(user)
                print('_______')
                if user.is_registered_throw_google:
                    response = TokenResponse(is_valid=True, user_email=user.email, id=user.id)
                else:
                    response = TokenResponse(is_valid=True, user_email=user.email, id=user.id, user_password=user.password)
                # if user.password: response.password = user.password
                return response

            case False:
                return token_status
            

    async def get_user_by_payload(self, email:str):
        user_obj = await self.user_repository.get_user_by_email(email)
        return user_obj
    

    async def return_subscription_by_token(self, token: str):
        status = await self.get_user_by_token(token)
        email = status.user_email
        user = await self.user_repository.get_user_by_email(user_email=email)
        if user:
            result = user.subscription[0]
        else:
            result = None
        return result