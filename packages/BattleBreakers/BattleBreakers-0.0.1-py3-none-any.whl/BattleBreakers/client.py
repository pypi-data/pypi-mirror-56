import aiohttp
import asyncio
import pyglet

from .auth import Authorization
from .http import HTTPClient

class client(pyglet.event.EventDispatcher):
    def __init__(self, email, password, *args):
        self.email = email
        self.password = password
        self.register_event_type('event_ready')
    
    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        loop.close()

    async def start(self):
        auth = Authorization(email=self.email, password=self.password)
        access_token = await auth.get_access_token(self.email, self.password)

        self.id = access_token['account_id']
        self.auth_token = access_token['access_token']

        #account = await aiohttp.get(f"https://account-public-service-prod03.ol.epicgames.com/account/api/public/account/{self.id}", headers={"Authorization": f"bearer {self.auth_token}"})
        #body = account.json()

        #self.

        self.dispatch_event('event_ready')