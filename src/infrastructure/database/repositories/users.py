from contextlib import asynccontextmanager

from src.infrastructure.database.tables.users import UserTable
from src.domain.entities.users.users_entities import UserEntity
from src.application.interfaces.repositories import IAlchemyRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.users import RegisterData
from src.infrastructure.database.utilities.get_password_hash import get_password_hash
from fastapi import HTTPException

from sqlalchemy import select





# TODO -> application interfaces
class BaseUserRepository(ABC):
    @abstractmethod
    async def get_user_by_email():
        raise NotImplementedError

    @abstractmethod
    async def register_user():
        raise NotImplementedError




class UserAlchemyRepository(BaseUserRepository, IAlchemyRepository):
    async def get_user_by_email(self, user_email: str):
        """get user from db with users email"""
        query = select(UserEntity).filter(UserEntity.email == user_email)
        user = await self._session.execute(query)
        result = user.scalar_one_or_none()
        return result


    async def register_user(self, register_data: RegisterData):
        """register new user"""
        existing_user = await self.get_user_by_email(user_email=register_data.email)

        # if existing_user is not None:
        #     raise HTTPException(status_code=400, detail="Email уже используется")
    
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
        return {"message": f"Пользователь с id {user_id} був видалений з системи"}
    

    async def update_user(self, user_obj, **values_dict):
        for obj_field in values_dict.keys():
            match obj_field:
                case 'password':
                    password_value=get_password_hash(values_dict['password'])
                    user_obj.password = password_value
                case _:
                    setattr(user_obj, obj_field, values_dict[obj_field])
        # await self._session.update(user)
        await self._session.commit()
        return {"message": f"Користувач с id {user_obj.id} змінив данні."}        


        
