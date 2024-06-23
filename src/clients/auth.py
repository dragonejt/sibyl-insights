from http import HTTPStatus
from js import fetch
from pyodide.ffi import to_js


async def auth(base_url: str, authorization: str, community_id: str) -> HTTPStatus:
    response = await fetch(
        f"{base_url}/community?id={community_id}",
        method="HEAD",
        headers=to_js({"Authorization": authorization, "User-Agent": "sibyl-insights"}),
    )
    return HTTPStatus(response.status)
