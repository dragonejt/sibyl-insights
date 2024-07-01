from http import HTTPStatus
from js import fetch
from pyodide.ffi import to_js


class Auth:

    def __init__(self, base_url: str, authorization: str) -> None:
        self.base_url = base_url
        self.authorization = authorization

    async def community(self, community_id: str) -> HTTPStatus:
        response = await fetch(
            f"{self.base_url}/community?id={community_id}",
            method="HEAD",
            headers=to_js(
                {"Authorization": self.authorization, "User-Agent": "sibyl-insights"}
            ),
        )
        return HTTPStatus(response.status)

    async def user(self, user_id: str) -> HTTPStatus:
        response = await fetch(
            f"{self.base_url}/psychopass/user?id={user_id}",
            method="HEAD",
            headers=to_js(
                {"Authorization": self.authorization, "User-Agent": "sibyl-insights"}
            ),
        )
        return HTTPStatus(response.status)
