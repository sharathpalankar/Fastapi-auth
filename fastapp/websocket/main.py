# websocket/manager.py

from fastapi import WebSocket
import json
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data):
        message = json.dumps({
            "type": "INFO",
            "message": data,
            "timestamp": datetime.utcnow().isoformat()
        })

        for connection in self.active_connections:
            await connection.send_text(message)


# ✅ SINGLETON INSTANCE
manager = ConnectionManager()


# from fastapi.websockets import WebSocket, WebSocketDisconnect 
# from fastapi import FastAPI ,WebSocket 
# from websocket.redis_client import redis_client

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)

        
