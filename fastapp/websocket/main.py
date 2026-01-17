from fastapi.websockets import WebSocket, WebSocketDisconnect 
from fastapi import FastAPI ,WebSocket 
from websocket.redis_client import redis_client

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def notification_message(self,  websocket: WebSocket, message: str):
        await websocket.accept()

        pubsub = redis_client.pubsub()
        pubsub.subscribe('notifications')

        try:
            while True:
                message = pubsub.get_message()
                if message and message['type'] == 'message':
                    await websocket.send_text(message['data'])
        except Exception as e:
            print("WebSocket exception details:", e)
        finally:
            #await websocket.close()
            pubsub.close()
        
