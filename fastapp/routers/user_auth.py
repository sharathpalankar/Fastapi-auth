from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from db import database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPBearer
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from auth import verify_token, create_access_token
from dependencies import AccessTokenBearer,TokenBearer, RefreshTokenBearer,get_current_user,RoleChecker
from exceptions.request_errors import UserAlreadyExists,RefreshTokenExpired, InvalidCredentials
# Dependency to get the MongoDB collection

REFRESH_TOKEN_EXPIRY = 2

def get_collection():
    return database['users'] 

class User(BaseModel):
    name: str
    email: str
    password: str

users_router = APIRouter()
# Create a user
@users_router.post("/signup", status_code=201)
async def signup_user(user: User, collection=Depends(get_collection)):
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise UserAlreadyExists
        
        #raise HTTPException(status_code=400, detail="Email already registered")

    user.role = 'user'  # Default role
    # user['created_at'] = datetime.utcnow()
    # user['last_login'] = None

    result = await collection.insert_one(user.dict())
    return JSONResponse(content={"message": "User created successfully", "user_id": str(result.inserted_id)})

@users_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), collection=Depends(get_collection)):
    user = await collection.find_one({"email": form_data.username, "password": form_data.password})
    print(user)
    if not user:
        raise InvalidCredentials
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # Update last_login field with current datetime
    await collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )

    access_token = create_access_token(
                user_data={
                    "email": user['email'],
                    "user_uid": str(user['_id']),
                    "role": user['role'],
                }
            )

    refresh_token = create_access_token(
        user_data={"email": user['email'], "user_uid": str(user['_id'])},
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
    )

    return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user['email']},
                }
            )
#     user

@users_router.get("/refresh_token")
async def refresh_access_token(token_details: str = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise RefreshTokenExpired

from fastapi import Security


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user


@users_router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user),role_checker: str = Depends(RoleChecker(allowed_roles=["user", "admin"]))):
    return current_user

@users_router.get("/admin")
async def read_admin_data(current_user: dict = Security(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return {"admin_data": "This is sensitive admin data"}