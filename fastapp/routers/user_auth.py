from fastapi import APIRouter, Depends, HTTPException, status, Header, UploadFile
from pydantic import BaseModel
from db import database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm,HTTPBearer
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from auth import verify_token, create_access_token, hash_password, verify_password
from books.schemas import BookCreateModel
from dependencies import AccessTokenBearer,TokenBearer, RefreshTokenBearer,get_current_user,RoleChecker
from exceptions.request_errors import UserAlreadyExists,RefreshTokenExpired, InvalidCredentials
from .user_service import userService
from core.httpx_client import get_httpx_client
from external_services.weather import get_weather
import httpx
from redis.asyncio import Redis
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache
from PIL import UnidentifiedImageError
from starlette.concurrency import  run_in_threadpool
from image_utils import delete_profile_image ,process_profile_image
from confsettings.config import CONFIG
# Dependency to get the MongoDB collection

REFRESH_TOKEN_EXPIRY = 2

def get_collection():
    return database['users'] 

def get_books_collection():
    return database['books']

class User(BaseModel):
    name: str
    email: str
    password: str
    role: str 

class updateUser(BaseModel):
    name: str = None
    email:str = None
    role:str

users_router = APIRouter()
# Create a user
@users_router.post("/signup", status_code=201)
async def signup_user(user: User, collection=Depends(get_collection)):
    print("user data is ",user.dict())
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise UserAlreadyExists
        
        #raise HTTPException(status_code=400, detail="Email already registered")

    user.role = 'user'  # Default role
    user.password = hash_password(user.password)
    # user['created_at'] = datetime.utcnow()
    # user['last_login'] = None
    print(user.dict())

    result = await collection.insert_one(user.dict())
    return JSONResponse(content={"message": "User created successfully", "user_id": str(result.inserted_id)})

@users_router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), collection=Depends(get_collection)):
 
    user = await collection.find_one({"email": form_data.username})
    hashed_password = verify_password(form_data.password,user["password"])
    print(hashed_password)
    print("info is ",user)
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
                    "user": {"email": user['email'], "role": user['role']},
                    
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

@users_router.put("/me/profilePicture")
async def upload_profile_picture(file:UploadFile,
                                 users_collection=Depends(get_collection),
                                 current_user: dict = Depends(get_current_user)
                                       ):
    content = await file.read()

    if len(content) > CONFIG.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {CONFIG.max_upload_size_bytes // (1024 * 1024)}MB",
        )
    try:
        new_filename = await run_in_threadpool(process_profile_image, content)
    except UnidentifiedImageError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file. Please upload a valid image (JPEG, PNG, GIF, WebP).",
        ) from err
    
    await users_collection.update_one(
        {"email": current_user['email']},
        {"$set": {"profile_picture": new_filename}}
    )
    
    return "still in development"

@users_router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user),role_checker: str = Depends(RoleChecker(allowed_roles=["user", "admin","storeowner"]))):
    return current_user


# current_user: dict = Depends(get_current_user), 
#                          role_checker: str = Depends(RoleChecker(allowed_roles=["admin","user"])
@users_router.get("/users")
async def read_all_users(
                           collection=Depends(get_collection)):
    users = []
    async for user in collection.find():
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        users.append(user)
    return users

@users_router.put("/update_userinfo")
async def update_user_info(user: updateUser, 
                           collection=Depends(get_collection),
                               current_user: dict = Depends(get_current_user)
                             ):
    if current_user['email'] != user.email:
        raise HTTPException(status_code=403, detail="You can only update your own information")
    existing_user = await collection.find_one({"email": current_user['email']})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    await collection.update_one({"email": current_user['email']}, {"$set": update_data})
    return {"message": "User information updated successfully"}


@users_router.delete("/delete_user")
async def delete_user(
    collection=Depends(get_collection),
    current_user: dict = Depends(get_current_user)
):
    if current_user['email'] != current_user['email']:
        raise HTTPException(status_code=403, detail="You can only delete your own account")
    result = await collection.delete_one({"email": current_user['email']})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@users_router.get("/admin")
async def read_admin_data(current_user: dict = Security(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return {"admin_data": "This is sensitive admin data"}


@users_router.post("/createBook")
async def create_book(bookdata:BookCreateModel,
                      books_collection=Depends(get_books_collection),
                      users_collection=Depends(get_collection),
                      current_user: dict = Depends(get_current_user)
                      ):
    bookrecord=bookdata.dict()
    # print("user email is ",current_user.email)
    print("user email  isis ",current_user['email'])
    
    try:
        user_age_instance= await userService.create(current_user['email'], users_collection)
        userage=user_age_instance.age
       
        if userage<18:
            print("if condition entered")
            raise HTTPException(status_code=403, detail="User is underaged to create a book")
        
        bookrecord['created_by']=current_user['email']
        result=  books_collection.insert_one(bookrecord)

        return {"message": "Book created successfully", "book": bookrecord, "created_by": current_user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        pass    

from fastapi import Request

def weather_cache_key_builder(
    func,
    namespace,
    request: Request,
    response,
    args,
    **kwargs,
):
    city_name = kwargs.get("city_name")
    access_key = request.headers.get("access_key")
    return f"{namespace}:weather:{city_name}:{access_key}"



@users_router.get("/city/{city_name}")
@cache(expire=300,key_builder=weather_cache_key_builder)
async def get_weatherdetails_by_city(city_name: str,request: Request, apikey = Header(..., alias="access_key") ,client: httpx.AsyncClient = Depends(get_httpx_client)):
    print("api key in header is true value ",apikey)
    weatherdata = await get_weather(apikey,city_name,client)
    return weatherdata