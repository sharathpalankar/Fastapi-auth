from fastapi import FastAPI,Header,HTTPException,Depends,Cookie,status,Request
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from db import database
from fastapi.security import OAuth2PasswordBearer
from routers.user_auth import users_router as user_router
from exceptions.request_errors import UserAlreadyExists
import requests

app = FastAPI()
app.include_router(user_router, prefix="/api/v1")
@app.exception_handler(UserAlreadyExists)
async def unicorn_exception_handler(request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=400,
        content={"message": f"{exc.message}"},
    )

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



class User(BaseModel):
    name: str
    email: str
    password: str

@app.get("/api/v1/{id}")
async def userdetail(id:int,name:str,city:str):
    return {"user_id":id,"personname":name,"city":city}

@app.post("/api/v1/{name}")
def say_hello(name: str):
    # res=requests.get('https://api.weatherstack.com/current?access_key=eb612d2439ec881303a8d9791bf546bc&query=New Delhi')
    # print(res.json())
    weather_data={'request': {'type': 'City', 'query': 'New Delhi, India', 'language': 'en', 'unit': 'm'}, 
     'location': {'name': 'New Delhi', 'country': 'India', 'region': 'Delhi', 'lat': '28.600', 'lon': '77.200', 'timezone_id': 'Asia/Kolkata', 'localtime': '2025-08-29 12:17', 'localtime_epoch': 1756469820, 'utc_offset': '5.50'
                  }}
    print(type(weather_data))
    # for i in weather_data:
    #     print(weather_data[i])

    for key, value in weather_data.items():
        print(value)
        for v in value:
            print(value[v])

    return {"message": f"Hello, {name}!"}

# Pydantic model for data validation
class Item(BaseModel):
    name: str
    description: str = None

# Dependency to get the MongoDB collection
def get_collection():
    return database['users']  # Change 'items' to your collection name



#  



# Create an item
# @app.post("/items/", response_model=Item)
# async def create_item(item: Item, collection=Depends(get_collection)):
#     item_dict = item.dict()
#     result = await collection.insert_one(item_dict)
#     item_dict["_id"] = str(result.inserted_id)
#     return item_dict




# Create a user
# @app.post("/users/")
# async def create_user(user: User, collection = Depends(get_collection)):
#     result = await collection.insert_one(user.dict())
#     print(result)
#     return {"id": str(result.inserted_id)}

#user login
# @app.post("/login/")
# async def login_user(email: str, password: str, collection = Depends(get_collection)):
#     user = await collection.find_one({"email": email, "password": password})
#     if user:
#         return {"message": "Login successful"}
#     return {"message": "Invalid email or password"}

#user forget password
# @app.post("/forget-password/")
# async def forget_password(email: str, new_password: str, collection = Depends(get_collection)):
#     result = await collection.update_one({"email": email}, {"$set": {"password": new_password}})
#     if result.modified_count:
#         return {"message": "Password updated successfully"}
#     return {"message": "Email not found"}
# Get all users
# @app.get("/users/")
# async def get_users(collection = Depends(get_collection)):
#     users = []
#     async for user in collection.find():
#         user['_id'] = str(user['_id'])  
#         users.append(user)
#     return users    

