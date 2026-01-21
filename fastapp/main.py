from fastapi import FastAPI,Header,HTTPException,Depends,Cookie,status,Request,Body, WebSocket,WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from db import database
from fastapi.security import OAuth2PasswordBearer
from routers.user_auth import users_router as user_router
from books.routes import book_router
from exceptions.request_errors import UserAlreadyExists,InvalidCredentials
from tasks import add_numbers
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis  import RedisBackend
import requests,asyncio
import redis.asyncio as redis 
from websocket.redis_client import redis_client
from websocket.notification_service import create_notification_service
from websocket.redis_subscriber import redis_subscriber as redis_listener

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup code here
#     print("code start up...")
#     redis_client = redis.Redis(host='localhost', port=6379, db=0)
#     # FastAPICache.init(RedisBackend(redis_client), prefix="fastapp_cache")
#      # 🔥 START REDIS SUBSCRIBER
#     redis_task = asyncio.create_task(redis_listener())
#     try:
#         yield
#     finally:
#         redis_task.cancel()
#         await redis_task.close()
#         # Shutdown code here
#         print("code Shutting down...")
#         await redis_client.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App startup")

    # DO NOT create a new redis client here
    redis_task = asyncio.create_task(redis_listener())

    try:
        yield
    finally:
        print(" App shutdown")
        redis_task.cancel()


app = FastAPI(lifespan=lifespan)

@app.exception_handler(UserAlreadyExists)
async def unicorn_exception_handler(request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        status_code=400,
        content={"message": f"{exc.message}"},
    )

@app.exception_handler(InvalidCredentials)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentials):
    return JSONResponse(
        status_code=401,
        content={"message": f"{exc.message}"},
    )

app.include_router(user_router, prefix="/api/v1", tags=["user_auth"])
app.include_router(book_router, prefix="/api/v1", tags=["books_api"])

@app.get("/")
def read_root():
    print("webhook called")
    return {"message": "Hello, FastAPI world!"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    name: str
    email: str
    password: str

import time

@app.get("/api/v1/")
async def userdetail():
    t1=time.time()

    t2=time.time()
    totaltime = t2 - t1
    print("time taken is",totaltime)

    return f"api v1 called in {totaltime} seconds"

    return "f test api v1 called"

@app.get("/api/v2/")
def userdetail():
    t1=time.time()

    t2=time.time()
    totaltime = t2 - t1
    print("time taken is",totaltime)

    return f"api v2 called in {totaltime} seconds"

@app.get("/api/v1/{id}")
async def userdetail(id:int,name:str,city:str):
    return {"user_id":id,"personname":name,"city":city}

@app.post("/api/v1/{name}")
def say_hello(name: str):
    res=requests.get('https://api.weatherstack.com/current?access_key=eb612d2439ec881303a8d9791bf546bc&query=New Delhi')
    print(res.json())
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

@app.get("/api/weather")
async def get_weather(api_key = Header(...)):
    res=requests.get('http://api.weatherstack.com/current?access_key={api_key}')
    url = f"https://api.weatherstack.com/current?access_key={api_key}"

    querystring = {"query":"New Delhi"}

    response = requests.get(url, params=querystring)
    return response.json()

# Pydantic model for data validation
class Item(BaseModel):
    name: str
    description: str = None

# Dependency to get the MongoDB collection
def get_collection():
    return database['users']  # Change 'items' to your collection name

@app.get("/start-task")
def start_task():
    task = add_numbers.delay(10, 20)   # QUEUES the task
    return {"task_id": task.id}


class Flower(BaseModel):
    name: str
    color: str
    price: float
    description: Optional[str] |None = None

class offerFlower(BaseModel):
    discount_percentage: float

@app.post("/flowers/")
async def create_flower(flower: Flower = Body(...), offer: offerFlower =Body(...),
                        merchant_id:str = Header(...)
):
                        
    return {
        "flower": flower,
        "offer": offer
    }
    
Brands=[
    {"brand_name":"brand1","country":"india"},
    {"brand_name":"brand2","country":"usa"},
]


class BrandModel(BaseModel):
    brand_name: str
    country: str  


@app.get("/brands")
async def get_brands():
    return [ BrandModel(**brand) for brand in Brands]
# @app.get("/task-status/{task_id}")
# def get_status(task_id: str):
#     result = add_numbers.AsyncResult(task_id)

#     return {
#         "task_id": task_id,
#         "state": result.state,
#         "result": result.result
#     }



#  

@app.post("/webhook/n8n")
async def webhook_fun(request:Request):
    payload = await request.json()
    print("payload receivued from webhook ", payload)

    return {"success":"payload Success to server",
            "event":payload.get("url")}

@app.post("/notifications/")
async def create_notification(request: Request):
    data = await request.json()
    result = create_notification_service(data)
    return {"notification_id": 1 , "message": data["message"]}


# ---------------- WEBSOCKET ----------------
from websocket.main import ConnectionManager


manager = ConnectionManager()

@app.websocket("/ws/notifications/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)



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

