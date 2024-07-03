from typing import override
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
from js import Response

from routes.route import Route
from insightsdb import CommunityInsights


class Community(Route):

    @override
    async def auth(self, request, env) -> bool:
        community_id = parse_qs(urlparse(request.url).query).get("id")[0]
        return (await env.auth.community(community_id)).is_success

    @override
    async def get(self, request, env) -> Response:
        community_id = parse_qs(urlparse(request.url).query).get("id")[0]
        community_insights = await self.insightsdb.get_community(community_id)
        return Response.new(community_insights.serialize(), status=HTTPStatus.OK)

    @override
    async def post(self, request, env) -> Response:
        request_body = (await request.json()).to_py()
        community_insights = CommunityInsights.deserialize(request_body)
        community_id = community_insights.community_id
        await self.insightsdb.put_community(community_id, community_insights)
        return Response.new(
            (await self.insightsdb.get_community(community_id)).serialize(),
            status=HTTPStatus.CREATED,
        )

    @override
    async def delete(self, request, env) -> Response:
        community_id = parse_qs(urlparse(request.url).query).get("id")[0]
        await self.insightsdb.delete_community(community_id)
        return Response.new(None, status=HTTPStatus.NO_CONTENT)
