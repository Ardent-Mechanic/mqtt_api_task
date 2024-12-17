from pydantic import BaseModel
from pydantic import ConfigDict


# Базовая схема
class UserBase(BaseModel):
    id: int
    phone_number: str
    name: str
    second_name: str
    last_name: str
    password: str

    class Config:
        from_attributes = True


# Схема для создания пользователя
class UserCreate(BaseModel):
    phone_number: str = '+7-123-444-78-90'
    name: str = 'Test'
    second_name: str = 'Test'
    last_name: str = 'Test'
    password: str = '12345678'


#
# # Схема для обновления пользователя
# class UserUpdate(BaseModel):
#     phone_number: str | None = None
#     name: str | None = None
#     second_name: str | None = None
#     middle_name: str | None = None


class UserLogin(BaseModel):
    phone_number: str
    password: str


class UserRegistration(BaseModel):
    phone_number: str
    name: str
    second_name: str
    last_name: str
    password: str


class UserMsg(BaseModel):
    msg: str
