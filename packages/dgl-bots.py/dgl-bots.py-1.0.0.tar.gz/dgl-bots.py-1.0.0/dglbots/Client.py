import aiohttp


class Client:
    def __init__(self, key, base_url="https://bots.discord.gl/api/public"):
        """
        Create a Client object
        :param key: The API Key
        :param base_url: Option to change the API endpoint
        """

        self._key = key
        self.base_url = base_url
        self._headers = {"Authorization": self._key}
        self.session = aiohttp.ClientSession(headers=self._headers)

    async def _request(self, endpoint, _type="GET", data=None):
        if _type == "GET":
            resp = await self.session.get(f"{self.base_url}/{endpoint}")
            resp_json = await resp.json()
            return resp_json
        elif _type == "POST":
            json = data if data else {}

            resp = await self.session.post(f"{self.base_url}/{endpoint}", json=json)
            resp_json = await resp.json()
            return resp_json

    async def get_site_stats(self):
        return await self._request("stats")

    async def get_bot_stats(self, id: str):
        return await self._request(f"bot/{id}")

    async def get_my_stats(self):
        return await self._request("bot/me")

    async def check_user_like(self, user_id: str):
        return await self._request(f"bots/me/liked/{user_id}")

    async def get_user_info(self, user_id: str):
        return await self._request(f"user/{user_id}")

    async def post_stats(self, server_count):
        return await self._request(
            f"bot/stats", _type="POST", data={"server_count": server_count}
        )
