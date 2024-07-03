from typing import override
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
from js import Response

from routes.route import Route
from insightsdb import UserInsights


class User(Route):

    @override
    async def auth(self, request, env) -> bool:
        user_id = parse_qs(urlparse(request.url).query).get("id")[0]
        return (await env.auth.user(user_id)).is_success

    @override
    async def get(self, request, env) -> Response:
        user_id = parse_qs(urlparse(request.url).query).get("id")[0]
        user_insights = await self.insightsdb.get_user(user_id)
        return Response.new(user_insights.serialize(), status=HTTPStatus.OK)

    @override
    async def post(self, request, env) -> Response:
        request_body = (await request.json()).to_py()
        user_insights = UserInsights.deserialize(request_body)
        user_id = user_insights.user_id
        await self.insightsdb.put_user(user_id, user_insights)
        return Response.new(
            (await self.insightsdb.get_user(user_id)).serialize(),
            status=HTTPStatus.CREATED,
        )

    @override
    async def delete(self, request, env) -> Response:
        user_id = parse_qs(urlparse(request.url).query).get("id")[0]
        await self.insightsdb.delete_user(user_id)
        return Response.new(None, status=HTTPStatus.NO_CONTENT)
