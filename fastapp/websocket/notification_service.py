from db import database
from websocket.redis_client import redis_client
import json 

def get_collection():
    return database['notifications'] 

def create_notification_service(data:dict):
    
    collection = get_collection()
    result = collection.insert_one(data)

    redis_client.publish('notifications', f'New notification created with ID: {str(data["message"])}')

    return data["message"]

redis_client.publish(
    "notifications",
    json.dumps({
        "type": "TEST",
        "message": "Hello from Redis 🚀"
    })
)