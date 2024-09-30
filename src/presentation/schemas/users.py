from pydantic import BaseModel
from pydantic import field_validator
from pydantic.networks import EmailStr




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