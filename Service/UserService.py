from Mapper import UserMapper
from sanic.response import json
from DTO.UserDTO import User
from pydantic import BaseModel, EmailStr, ValidationError, field_validator
from typing import Optional


class UserModel(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: Optional[str] = None

    @field_validator('username')
    def username_alphanumeric(cls, value):
        if not value.isalnum():
            raise ValueError('username must be alphanumeric')
        if not (3 <= len(value) <= 12):
            raise ValueError('username length must be between 3 and 12 characters')
        return value

    @field_validator('password')
    def password_length(cls, value):
        if not (8 <= len(value) <= 20):
            raise ValueError('password length must be between 8 and 20 characters')
        return value
class LoginModel(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def username_alphanumeric(cls, value):
        if not value.isalnum():
            raise ValueError('username must be alphanumeric')
        if not (3 <= len(value) <= 12):
            raise ValueError('username length must be between 3 and 12 characters')
        return value

    @field_validator('password')
    def password_length(cls, value):
        if not (8 <= len(value) <= 20):
            raise ValueError('password length must be between 8 and 20 characters')
        return value


class UserService:

    def __init__(self):
        self.userMapper = UserMapper.UserMapper()

    async def register(self, request):
        try:
            data = request.json
            user_data = UserModel(**data)  # Pydantic 校验
        except ValidationError as e:
            return json({'error': str(e.errors()[0]['msg'])}, status=400)

        new_user = User(username=user_data.username, password=user_data.password,
                        email=user_data.email, avatar=user_data.avatar)

        return json({'data': self.userMapper.register(new_user)})

    async def login(self, request):
        try:
            data = request.json
            user_data = LoginModel(**data)  # Pydantic 校验
        except ValidationError as e:
            return json({'error': str(e.errors()[0]['msg'])}, status=400)
        username = user_data.username
        password = user_data.password
        return json({'data': self.userMapper.login(username, password)})
