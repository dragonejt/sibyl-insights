from http import HTTPStatus
from js import Response
from urllib.parse import urlparse, parse_qs
from clients.auth import auth
from insights import InsightsDB


async def on_fetch(request, env) -> Response:
    community_id = parse_qs(urlparse(request.url).query).get("id")[0]
    auth_status = await auth(
        env.BACKEND_URL, request.headers.get("Authorization"), community_id
    )
    if auth_status.is_success is False:
        return Response.new(auth_status.description, status=auth_status.value)
    insights_db = InsightsDB(env.insightsdb)
    return Response.new("Hello World!")
