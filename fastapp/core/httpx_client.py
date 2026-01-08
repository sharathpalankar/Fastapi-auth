import httpx
from typing import Optional, AsyncGenerator

async def get_httpx_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient() as client:
        yield client