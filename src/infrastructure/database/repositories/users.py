from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UserTable
from src.domain.entities.users.users_entities import UserEntity
from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.users import RegisterData
from src.infrastructure.database.utilities.get_password_hash import get_password_hash

from sqlalchemy import select





# TODO -> application interfaces
class BaseUserRepository(ABC):
    @abstractmethod
    async def get_user_by_email():
        raise NotImplementedError

    @abstractmethod
    async def register_user():
        raise NotImplementedError




class UserAlchemyRepository(IAlchemyRepository, BaseUserRepository):
    async def get_user_by_email(self, user_email: str):
        """get user from db with users email"""
        query = select(UserEntity).filter(UserEntity.email == user_email)
        user = await self._session.execute(query)
        result = user.scalar_one_or_none()
        return result


    async def register_user(self, register_data: RegisterData):
        """register new user"""
        new_user = UserEntity(
                email=register_data.email,
                password=get_password_hash(register_data.password)
            )
        self._session.add(new_user)
        await self._session.commit()
        return new_user
    
    
    async def delete_user(self, email):
        user = await self.get_user_by_email(user_email=email)
        user_id = user.id
        await self._session.delete(user)
        await self._session.commit()
        return {"result": f"Пользователь с id {user_id} був видалений з системи"}

        
