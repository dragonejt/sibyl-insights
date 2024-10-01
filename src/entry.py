from logging import getLogger, INFO, StreamHandler
from datetime import datetime, UTC
from http import HTTPStatus, HTTPMethod
from urllib.parse import urlparse
from js import Response

from insightsdb import InsightsDB
from clients.auth import Auth
from routes.root import Root
from routes.community import Community
from routes.user import User


async def on_fetch(request, env) -> Response:
    log = getLogger(__name__)
    log.setLevel(INFO)
    log.addHandler(StreamHandler())

    log.info(
        "[%s] %s %s",
        datetime.now(UTC).isoformat(),
        request.method,
        f"{urlparse(request.url).path}?{urlparse(request.url).query}",
    )

    routes = [Root([]), Community(["community"]), User(["user"])]

    for route in routes:
        if route.matches(request.url) is False:
            log.debug("Route %s does not match request", route.__class__.__name__)
            continue

        env.auth = Auth(env.BACKEND_URL, request.headers.get("Authorization"))
        if await route.auth(request, env) is False:
            return Response.new(
                HTTPStatus.UNAUTHORIZED.description, status=HTTPStatus.UNAUTHORIZED
            )

        route.context(db=InsightsDB(env.INSIGHTSDB))
        log.info("Request routed to %s %s", request.method, route.__class__.__name__)
        match request.method:
            case HTTPMethod.GET:
                return await route.get(request, env)
            case HTTPMethod.HEAD:
                return await route.head(request, env)
            case HTTPMethod.POST:
                return await route.post(request, env)
            case HTTPMethod.PUT:
                return await route.put(request, env)
            case HTTPMethod.PATCH:
                return await route.patch(request, env)
            case HTTPMethod.DELETE:
                return await route.delete(request, env)
            case HTTPMethod.OPTIONS:
                return await route.options(request, env)
            case _:
                return Response.new(
                    HTTPStatus.METHOD_NOT_ALLOWED.description,
                    status=HTTPStatus.METHOD_NOT_ALLOWED,
                )

    log.debug("No route matches request")
    return Response.new(HTTPStatus.NOT_FOUND.description, status=HTTPStatus.NOT_FOUND)
