from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date

# from typing import Literal
from enum import Enum


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


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class CategoryCreate(BaseModel):
    user_id: int | None = Field(default=None, ge=1)
    transaction_type: TransactionType
    name: str


class CategoryResponse(CategoryCreate):
    id: int


class Transaction(BaseModel):
    transaction_type: TransactionType
    category_id: int
    amount: float
    description: str
    date: date


class TransactionResponse(Transaction):
    id: int
    user_id: int
    created_at: datetime
