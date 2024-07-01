from typing import override
from urllib.parse import urlparse, parse_qs
from js import Response

from routes.route import Route


class Community(Route):

    @override
    async def auth(self, request, env) -> bool:
        community_id = parse_qs(urlparse(request.url).query).get("id")[0]
        return (await env.auth.community(community_id)).is_success

    @override
    async def get(self, request, env) -> Response:
        return Response.new("Community")
