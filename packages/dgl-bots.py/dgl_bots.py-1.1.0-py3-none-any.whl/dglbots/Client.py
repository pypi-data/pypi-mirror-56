import aiohttp


class Client:
    def __init__(self, key, base_url="https://bots.discord.gl/api/public"):
        """
        Create a Client object

        :param key: The API Key
        :param base_url: Option to change the API endpoint
        """
        self.base_url = base_url
        self.session = aiohttp.ClientSession(headers={"Authorization": key})

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
        """
        Get the website stats
        """
        return await self._request("stats")

    async def get_bot_stats(self, _id: str):
        """
        Get stats of a bot listed on the site.

        :param _id: the user id of the bot.
        :return: The Bot stats
        """
        return await self._request(f"bot/{_id}")

    async def get_my_stats(self):
        """
        Get the currently authenticated bot's stats

        :return: Stats of the currently authenticated bot.
        """
        return await self._request("bot/me")

    async def check_user_like(self, user_id: str):
        """
        Check if the user has liked the bot or not.

        :param user_id: The ID of the user to be checked.
        """
        return await self._request(f"bots/me/liked/{user_id}")

    async def get_user_info(self, user_id: str):
        """
        Get a user's info from the site.

        :param user_id:The user's ID.
        """
        return await self._request(f"user/{user_id}")

    async def post_stats(self, server_count):
        """
        Post the stats of the bot.

        :param server_count: The sever count of the bot.
        """
        return await self._request(
            f"bot/stats", _type="POST", data={"server_count": server_count}
        )
