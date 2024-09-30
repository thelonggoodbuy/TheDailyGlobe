from datetime import datetime, timedelta, timezone


import jwt


from src.application.interfaces.services import ITokenService
from src.main.config.settings import Settings



class JWTTokenService(ITokenService):
    """ Service for JWT Token logic """

    def __init__(
        self,
        settings: Settings,
    ):
        """Initialize Jwt token settings."""
        self.secret_key: str = settings.jwt_token.SECRET_KEY
        self.algorithm: str = settings.jwt_token.ALGORITHM



    async def create_access_token(self, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=28)
        to_encode = {'email': email, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt