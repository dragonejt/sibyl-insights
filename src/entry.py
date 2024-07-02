import logging
from datetime import datetime, timezone
from insightsdb import InsightsDB
from js import Response
from http import HTTPStatus, HTTPMethod

from clients.auth import Auth
from routes.root import Root
from routes.community import Community


async def on_fetch(request, env) -> Response:
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler())

    log.info(
        "[%s] %s %s",
        datetime.now(timezone.utc).isoformat(),
        request.method,
        request.url,
    )

    routes = [Root([]), Community(["community"])]

    for route in routes:
        if route.matches(request.url) is False:
            log.debug("Route %s does not match request", route.__class__.__name__)
            continue

        env.auth = Auth(env.BACKEND_URL, request.headers.get("Authorization"))
        if await route.auth(request, env) is False:
            return Response.new(
                HTTPStatus.UNAUTHORIZED.description, status=HTTPStatus.UNAUTHORIZED
            )

        env.insights = InsightsDB(env.insightsdb)
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
