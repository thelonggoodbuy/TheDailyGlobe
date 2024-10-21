from pydantic import BaseModel
from pydantic import field_validator, model_validator
from pydantic.networks import EmailStr
from pydantic_core.core_schema import FieldValidationInfo





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
        return value
    
    
    @field_validator("password")
    def password_have_not_be_empty(cls, value):
        if not value:
            raise ValueError("Поле 'password' не повинно бути пустим")
        return value
    

class RegisterData(BaseModel):
    email: str
    password: str
    repeat_password: str

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

    @model_validator(mode="before")
    def validate_password_and_repeat_password_not_empty(cls, data):
        if ("password" in data and "repeat_password" not in data) or (
            "password" not in data and "repeat_password" in data
        ):
            raise ValueError(
                "Для зміни паролю потрібно ввести пароль, та повторити його. Одне з полів пусте."
            )
        else:
            return data
        

class UserRegisterResponse(BaseModel):
    result: str
    jwt_access_token: str