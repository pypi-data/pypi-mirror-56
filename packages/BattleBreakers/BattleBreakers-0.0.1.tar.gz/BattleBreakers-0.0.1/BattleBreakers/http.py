import aiohttp
import asyncio
import pyglet

class HTTPClient:
    def __init__(self, auth_token):
        self.authorization = auth_token

    async def get(self, url, headers, data, *args):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=headers, data=data)
            return response

    async def post(self, url, headers, data, *args):
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, headers=headers, data=data)
            return response