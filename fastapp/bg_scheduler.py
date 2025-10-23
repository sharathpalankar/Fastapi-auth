import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import get_collection
from apscheduler.triggers.cron import CronTrigger
from datetime import timedelta,datetime
from db import database,log_collection

async def find_inactive_users():
    collection = get_collection()
    two_days_ago = datetime.utcnow() - timedelta(days=2)
    # Find users whose last_login is older than 2 days
    users = []
    cursor=  ( collection).find({"last_login": {"$lt": two_days_ago}})
    print(cursor)
   
    async for user in cursor:
        users.append({
            "id": str(user["_id"]),
            "name": user.get("name"),
            "email": user.get("email"),
            "last_login": user.get("last_login")
        })
        # users.append(user)
    print(users)  # Print each user document

    if users:
        log_entry = {
            "timestamp": datetime.utcnow(),
            "inactive_users": users,
            "count": len(users)
        }

        await log_collection.insert_one(log_entry)

    print(f"[{datetime.now()}] Found {len(users)} inactive users.")

    
    return users
# Shared global scheduler

def schedulefunc():
    print("yes bg round")

scheduler = AsyncIOScheduler()
async def start_scheduler():
    # scheduler=BackgroundScheduler()
    # scheduler = AsyncIOScheduler()
    scheduler.add_job(schedulefunc,'cron',hour=15,minute=41)
    scheduler.start()
    print("Scheduler started...")

    # Keep the event loop running forever
    while True:
        await asyncio.sleep(3600)
    
    

# asyncio.run(find_inactive_users())

if __name__ == "__main__":
    asyncio.run(start_scheduler())
    # loop = asyncio.get_event_loop()
    # # loop.run_until_complete(find_inactive_users())
    # start_scheduler()

    # try:
    #     print("Running event loop...")
    #     loop.run_forever()
    # except (KeyboardInterrupt, SystemExit):
    #     print("Scheduler stopped.")

