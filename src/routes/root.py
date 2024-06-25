from typing import override
from js import Response

from routes.route import Route


class Root(Route):

    @override
    async def auth(self, request, env) -> bool:
        return True

    @override
    async def get(self, request, env) -> Response:
        return Response.new("Sibyl Insights API")
