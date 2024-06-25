from typing import override
from urllib.parse import urlparse, parse_qs
from js import Response

from routes.route import Route
from clients.auth import community_auth


class Community(Route):

    @override
    async def auth(self, request, env) -> bool:
        community_id = parse_qs(urlparse(request.url).query).get("id")[0]
        return (
            await community_auth(
                env.BACKEND_URL, request.headers.get("Authorization"), community_id
            )
        ).is_success

    @override
    async def get(self, request, env) -> Response:
        return Response.new("Community")
