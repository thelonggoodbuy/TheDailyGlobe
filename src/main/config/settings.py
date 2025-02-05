from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from starlette.config import Config as GoogleStarletteConfig
from authlib.integrations.starlette_client import OAuth

from dotenv import load_dotenv
import os



BASE_DIR: str = str(Path(__file__).parent.parent.parent.parent)

load_dotenv(os.path.join(BASE_DIR, '.env'))


class FastAPISettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )



class DatabaseSettings(FastAPISettings):
    POSTGRES_HOST: str = os.environ.get('POSTGRES_HOST')
    POSTGRES_PORT: int = os.environ.get('POSTGRES_PORT')
    POSTGRES_USER: str = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB: str = os.environ.get('POSTGRES_DB')

    @property
    def URL(self) -> str:
        if all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB]):
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        raise ValueError("Database URL is not set")


class AppSettings(FastAPISettings):
    PROJECT_NAME: str = "FastAPI Project"
    DEBUG: bool = True


class GoogleAuthSettings(FastAPISettings):

    GOOGLE_CLIENT_ID: str = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_CONF_URL: str = os.environ.get('GOOGLE_CONF_URL')


    @property
    def google_auth_object(self):
        """Google auth object"""
        config = GoogleStarletteConfig('.env')
        oauth = OAuth(config)
        CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
        oauth.register(
            name='google',
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        return oauth
    

class JWTTokenSettings(FastAPISettings):
    SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY')
    ALGORITHM: str = os.environ.get('JWT_ALGORITHM')


class Settings(FastAPISettings):
    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    google_auth: GoogleAuthSettings = Field(default_factory=GoogleAuthSettings)
    jwt_token: JWTTokenSettings = Field(default_factory=JWTTokenSettings)





