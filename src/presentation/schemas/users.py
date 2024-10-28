from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic import field_validator, model_validator
from pydantic.networks import EmailStr
from pydantic_core.core_schema import FieldValidationInfo

from src.presentation.schemas.base_schemas import BaseResponseSchema, BaseSchema


class BaseModelWithCamelCase(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class LoginRequestData(BaseModel):
    email: str
    password: str


    @field_validator("email")
    def email_have_not_be_empty(cls, value):
        if not value:
            raise ValueError("Поле 'email' не повинно бути пустим")
        return value
    

    @field_validator('email')
    def email_valid(cls, value):
        try:
            EmailStr._validate(value)
        except ValueError:
            raise ValueError('Не корректна емейл адресса.')
            # return 'Не корректна емейл адресса.'
        return value
    
    
    @field_validator("password")
    def password_have_not_be_empty(cls, value):
        if not value:
            raise ValueError("Поле 'password' не повинно бути пустим")
        return value
    

from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel, to_snake
from typing import Any, Dict, Optional
from typing import Type



class RegisterData(BaseSchema):
    email: str
    password: str
    repeat_password: str = Field(alias='repeatPassword')

    # model_config = ConfigDict(
    #     alias_generator=AliasGenerator(
    #         validation_alias=to_snake,
    #         serialization_alias=to_camel,
    #     ),
    #     populate_by_name=True,
    #     from_attributes=True,
        
    # )

    


    # model_config = ConfigDict(
    #     alias_generator=lambda field_name: ''.join(
    #         word.capitalize() if i > 0 else word
    #         for i, word in enumerate(field_name.split('_'))
    #     ),
    #     populate_by_name=True,
    #     from_attributes=True,
    # )


    @field_validator("email")
    def email_have_not_be_empty(cls, value):
        if not value:
            raise ValueError("Поле 'email' не повинно бути пустим")
        return value
    
    @field_validator('email')
    def email_valid(cls, value):
        try:
            EmailStr._validate(value)
        except ValueError:
            raise ValueError('Не корректна емейл адресса.')
        return value
    
    @field_validator("password")
    def password_have_not_be_empty(cls, value):
        if not value:
            raise ValueError("Поле 'password' не повинно бути пустим")
        return value
    
    @field_validator("repeat_password")
    def validate_repeat_password_match(cls, value: str, values: FieldValidationInfo):
        if "password" in values.data and value != values.data["password"]:
            raise ValueError("Паролі не співпадають")
        return value

    @model_validator(mode="after")
    def validate_password_and_repeat_password_not_empty(cls, data):
        if ("password" in data and "repeat_password" not in data) or (
            "password" not in data and "repeat_password" in data
        ):
            raise ValueError(
                "Для зміни паролю потрібно ввести пароль, та повторити його. Одне з полів пусте."
            )
        else:
            return data
        

class UserRegisterResponse(BaseResponseSchema):
    result: str
    jwt_access_token: str



class LoginUserSuccessData(BaseModel):
    id: int
    email: str

class LoginSuccessDataSchema(BaseSchema):
    access_token: str
    refresh_token: str
    user_data: dict
    #TODO subscription это пока заглушка
    subscription_data: str


class DeleteUsersData(BaseModel):
    password: str


class ChangePasswordUsersData(BaseSchema):
    old_password: str = Field(alias='oldPassword')
    new_password: str = Field(alias='newPassword')
    repeat_new_password: str = Field(alias='repeatNewPassword')

    @field_validator("old_password")
    def password_have_not_be_empty(cls, value):
        if not value:
            raise ValueError("Поле 'old_password' не повинно бути пустим")
        return value
    
    @field_validator("new_password")
    def password_have_not_be_empty(cls, value):
        if not value:
            raise ValueError("Поле 'new_password' не повинно бути пустим")
        return value


    @field_validator("repeat_new_password")
    def validate_repeat_password_match(cls, value: str, values: FieldValidationInfo):
        if "new_password" in values.data and value != values.data["new_password"]:
            raise ValueError("Паролі не співпадають")
        return value


    # @model_validator(mode="before")
    # def validate_password_and_repeat_password_not_empty(cls, data):
    #     if ("password" in data and "repeat_password" not in data) or (
    #         "password" not in data and "repeat_password" in data
    #     ):
    #         raise ValueError(
    #             "Для зміни паролю потрібно ввести пароль, та повторити його. Одне з полів пусте."
    #         )
    #     else:
    #         return data


class RefreshTokenUsersData(BaseModel):
    refresh_token: str