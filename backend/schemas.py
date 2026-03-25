from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    email: EmailStr = Field(min_length=5)
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr = Field(min_length=5)
    password: str = Field(min_length=6)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    created_at: datetime
