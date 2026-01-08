import httpx
from fastapi import Depends
from confsettings.config import CONFIG
from core.httpx_client import get_httpx_client

async def get_weather(apikey, 
                      city_name: str,
                      client: httpx.AsyncClient):
          
    #url = await client.get('http://api.weatherstack.com/current?access_key={api_key}')
    url = "http://api.weatherstack.com/current"

    params = {
        "access_key": apikey,
        "query": city_name
    }

    response = await client.get(url, params=params)

    # print("RAW URL:", response.request.url)
    # print("STATUS:", response.status_code)
    # print("BODY:", response.text)

    return response.json()