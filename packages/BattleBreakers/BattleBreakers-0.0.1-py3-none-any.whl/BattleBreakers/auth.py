import aiohttp
import asyncio
import pyglet

class Authorization:
    def __init__(self, email, password, *args):
        self.email = email
        self.password = password

    async def get_access_token(self, email, password):
        async with aiohttp.ClientSession(cookies=None) as session:
            crsf = await session.get("https://www.epicgames.com/id/api/csrf")

            login = await session.post(
                "https://www.epicgames.com/id/api/login", 
                headers={
                    "x-xsrf-token": crsf.cookies.get("XSRF-TOKEN").value
                },
                data={
                    "email": self.email,
                    "password": self.password,
                    "rememberMe": False
                },
                cookies=crsf.cookies
            )
            
            login = await session.post("https://www.epicgames.com/id/api/login", headers={"x-xsrf-token": crsf.cookies.get("XSRF-TOKEN").value}, data={"email": self.email, "password": self.password, "rememberMe": False} ,cookies=crsf.cookies)

            # Raises error if wrong email/password is inputted.
            if login.status == 400:
                raise ValueError("Wrong email/password entered.")

            # Fetch exchange code.
            res = await session.get(
                "https://www.epicgames.com/id/api/exchange", 
                headers={
                    "x-xsrf-token": crsf.cookies.get("XSRF-TOKEN").value
                },
                cookies=login.cookies
            )

            json = await res.json()
            exchange_code = json["code"]

            # Exchange the code to fetch the launcher access token.
            res = await session.post(
                "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token", 
                headers={
                    "Authorization": "basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
                },
                data={
                    "grant_type": "exchange_code",
                    "exchange_code": exchange_code,
                    "token_type": "eg1"
                }
            )
            json = await res.json()
            launcher_access_token = json["access_token"]
            
            # The following code will use the launcher access token to retrieve
            # a fortnite access token. If you don't require fortnite permissions
            # you can cut out the part below.
            res = await session.get(
                "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange",
                headers={
                    "Authorization": f"Bearer {launcher_access_token}"
                }
            )
            json = await res.json()
            exchange_code = json["code"]

            res = await session.post(
                "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Authorization": "basic M2NmNzhjZDNiMDBiNDM5YTg3NTVhODc4YjE2MGM3YWQ6YjM4M2UwZjQtZjBjYy00ZDE0LTk5ZTMtODEzYzMzZmMxZTlk="
                },
                data={
                    "grant_type": "exchange_code",
                    "token_type": "eg1",
                    "exchange_code": exchange_code
                }
            )

            # NOTE: Tokens expires after eight hours.
            json = await res.json()
            return json