from http import HTTPStatus
from js import Response
from urllib.parse import urlparse, parse_qs
from clients.auth import auth
from insights import InsightsDB


async def on_fetch(request, env) -> Response:
    community_id = parse_qs(urlparse(request.url).query).get("id")[0]
    if not await auth(
        env.BACKEND_URL, request.headers.get("Authorization"), community_id
    ):
        return Response.new(
            HTTPStatus.UNAUTHORIZED.description, status=HTTPStatus.UNAUTHORIZED.value
        )
    insights_db = InsightsDB(env.insightsdb)
    return Response.new("Hello World!")
