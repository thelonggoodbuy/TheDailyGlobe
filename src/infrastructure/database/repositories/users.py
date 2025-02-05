from contextlib import asynccontextmanager
import datetime

from src.infrastructure.database.tables.users import UserTable
from src.domain.entities.users.users_entities import UserEntity, TokenBlacklistEntity
from src.application.interfaces.repositories import IAlchemyRepository, BaseUserRepository
from abc import ABC, abstractmethod
from src.presentation.schemas.users import LogOutRequestData, RegisterData
from src.infrastructure.database.utilities.get_password_hash import get_password_hash
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from sqlalchemy import or_, select




class UserAlchemyRepository(BaseUserRepository, IAlchemyRepository):
    async def get_user_by_email(self, user_email: str):
        """get user from db with users email"""
        query = select(UserEntity).options(selectinload(UserEntity.subscription)).filter(UserEntity.email == user_email)
        user = await self._session.execute(query)
        result = user.scalar_one_or_none()
        return result


    async def register_user(self, register_data: RegisterData):
        """register new user"""
        existing_user = await self.get_user_by_email(user_email=register_data.email)
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
        await self._session.commit()
        return {"message": f"Користувач {user_obj.email} змінив данні."}        


    async def add_to_blacklist(self, logout_data: LogOutRequestData):

        token_is_compromised = await self.check_if_token_in_blacklist(logout_data.access_token)

        print('===token_is_compromised===')
        print(token_is_compromised)
        print('==========================')

        if token_is_compromised == False:
            print('NOT COMPROMISSED~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            new_black_list_token = TokenBlacklistEntity(
                access_token=logout_data.access_token,
                refresh_token=logout_data.refresh_token,
                added_date=datetime.datetime.now(datetime.timezone.utc)
            )
            self._session.add(new_black_list_token)
            await self._session.commit()
            return new_black_list_token
    

    async def check_if_token_in_blacklist(self, token: str):
        query = select(TokenBlacklistEntity).filter(or_(TokenBlacklistEntity.access_token == token, 
                                                    TokenBlacklistEntity.refresh_token == token))
        compromised_token = await self._session.execute(query)
        # print('===compromised_token===')
        # print(compromised_token.scalars().all())
        # print('=======================')
        is_token_compromised = compromised_token.scalars().all()
        print('===is_token_compromised result===')
        print(is_token_compromised)
        print('=================================')
        if len(is_token_compromised) > 0:
            print('111111111111111111111111111111111')
            result = True
        else:
            print('222222222222222222222222222222222')
            result = False
        return result