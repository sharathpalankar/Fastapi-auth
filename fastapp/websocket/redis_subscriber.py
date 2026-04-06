import asyncio
from websocket.redis_client import redis_client
from websocket.main import manager 

async def redis_subscriber():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('notifications')

    print("Subscribed to Redis channel 'notifications'")

    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)

            if message:
                data = message["data"]
                print("📩 Redis:", data)

                await manager.broadcast(data)

            await asyncio.sleep(0.1)  # ✅ CRITICAL (prevents blocking)

    except asyncio.CancelledError:
        print("Redis listener stopped")
    finally:
        pubsub.close()
        # for message in pubsub.listen():
        #     if message['type'] == 'message':
        #         data = message['data']
        #         print("Received messages from Redis:", data)
        #         await manager.broadcast(data)
    # except asyncio.CancelledError:
    #     print("Redis subscriber task cancelled")
    # finally:
    #     pubsub.close()

