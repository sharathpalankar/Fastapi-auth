import asyncio
import time

def test1():
    """this is test func"""
    time.sleep(5)
    return 999

async def demo1():

    res=await test1()

    print("it is not waiting for 5 seconds")


    return res

asyncio.run(demo1())