import motor
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from fastapi import FastAPI,HTTPException,status
from confsettings.config import CONFIG
 
MONGO_URI = CONFIG.MONGO_URI # Use your MongoDB URI here

# Creating the MongoDB client with connection pooling
client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_URI, 
    maxPoolSize=10,    # Max number of connections
    minPoolSize=2,     # Min number of connections
    maxIdleTimeMS=5000 # Idle time in milliseconds
)

# Database instance
database = client['School']
print("runned main file your seeing db.py")
print(database)

users_collection = database["users"]
log_collection = database["inactive_users_logs"]

# Update one document
users_collection.update_one(
    {"email": "appushet@gmail.com"},      # Match condition
    {"$set": {"role": "admin"}}           # New field
)