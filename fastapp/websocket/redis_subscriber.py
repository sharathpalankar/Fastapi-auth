import asyncio
from websocket.redis_client import redis_client
from websocket.main import ConnectionManager 

manager = ConnectionManager()


async def redis_subscriber():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('notifications')

    print("Subscribed to Redis channel 'notifications'")

    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = message['data']
                print("Received message from Redis:", data)
                await manager.broadcast(data)
    except asyncio.CancelledError:
        print("Redis subscriber task cancelled")
    finally:
        pubsub.close()

