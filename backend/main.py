from fastapi import FastAPI, status, HTTPException
from schemas import (
    UserLogin,
    UserResponse,
    UserRegister,
    CategoryCreate,
    CategoryResponse,
)
from utilities import hash_password, verify_password
from datetime import datetime


app = FastAPI()

users: list[UserResponse] = []
categories: list[CategoryResponse] = []


@app.get("/")
def home():
    return {"message": "Welcome to my home page"}


@app.get(
    "/api/users",
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Not Found"}},
    response_model=list[UserResponse],
)
def get_all_users():
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users Not Found"
        )

    return users


@app.post(
    "/api/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def register_user(data: UserRegister):
    id = len(users) + 1

    user_data = data.model_dump()
    user_data["id"] = id

    hashed_password = hash_password(user_data["password"])
    confirm_password = verify_password(hashed_password, user_data["confirm_password"])
    if not confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password mismatch"
        )

    user_data["password"] = hashed_password
    user_data["created_at"] = datetime.now()

    users.append(user_data)

    return user_data


@app.post(
    "/api/login",
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Not found"}, 400: {"description": "Bad request"}},
)
def login_user(data: UserLogin):
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found, please register first",
        )

    for user in users:
        if user["email"].strip().lower() == data.email.lower():
            verify_pass = verify_password(user["password"], data.password)

            if not verify_pass:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user Credentials",
                )

            return {"message": "Login Successful"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found, please register first",
    )


@app.get(
    "/api/categories",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
def get_categories():
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categories not found"
        )

    return categories


@app.post(
    "/api/categories",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse,
)
def add_category(category: CategoryCreate):
    id = len(categories) + 1

    category = category.model_dump()
    category["id"] = id

    categories.append(category)

    return category
