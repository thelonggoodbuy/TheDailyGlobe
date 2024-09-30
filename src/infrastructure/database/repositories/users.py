from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UserTable
from src.domain.entities.users.users_entities import UserEntity
from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod

from sqlalchemy import select





# TODO -> application interfaces
class BaseUserRepository(ABC):
    @abstractmethod
    async def get_user_by_email():
        raise NotImplementedError



class UserAlchemyRepository(IAlchemyRepository, BaseUserRepository):
    async def get_user_by_email(self, user_email: str):
        """get user from db with users email"""
        query = select(UserTable).filter(UserEntity.email == user_email)
        user = await self._session.execute(query)
        result = user.first()
        return result


    