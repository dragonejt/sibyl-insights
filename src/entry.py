import logging
from datetime import datetime, timezone
from js import Response
from http import HTTPStatus, HTTPMethod

from routes.root import Root
from routes.community import Community


async def on_fetch(request, env) -> Response:
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler())

    log.info(
        "[%s] '%s %s'",
        datetime.now(timezone.utc).isoformat(),
        request.method,
        request.url,
    )

    routes = [Root([]), Community(["community"])]

    for route in routes:
        if route.matches(request) is False:
            log.debug("Route %s does not match request", route.__class__.__name__)
            continue

        log.debug("Route %s matches request", route.__class__.__name__)
        if await route.auth(request, env) is False:
            return Response.new(
                HTTPStatus.UNAUTHORIZED.description,
                status=HTTPStatus.UNAUTHORIZED,
            )

        match request.method:
            case HTTPMethod.GET:
                log.debug("Request is %s %s", HTTPMethod.GET, route.__class__.__name__)
                return await route.get(request, env)
            case HTTPMethod.HEAD:
                log.debug("Request is %s %s", HTTPMethod.HEAD, route.__class__.__name__)
                return await route.head(request, env)
            case HTTPMethod.POST:
                log.debug("Request is %s %s", HTTPMethod.POST, route.__class__.__name__)
                return await route.post(request, env)
            case HTTPMethod.PUT:
                log.debug("Request is %s %s", HTTPMethod.PUT, route.__class__.__name__)
                return await route.put(request, env)
            case HTTPMethod.PATCH:
                log.debug(
                    "Request is %s %s", HTTPMethod.PATCH, route.__class__.__name__
                )
                return await route.patch(request, env)
            case HTTPMethod.DELETE:
                log.debug(
                    "Request is %s %s", HTTPMethod.DELETE, route.__class__.__name__
                )
                return await route.delete(request, env)
            case HTTPMethod.OPTIONS:
                log.debug(
                    "Request is %s %s", HTTPMethod.OPTIONS, route.__class__.__name__
                )
                return await route.options(request, env)
            case _:
                log.debug("Request method %s is not supported", request.method)
                return Response.new(
                    HTTPStatus.METHOD_NOT_ALLOWED.description,
                    status=HTTPStatus.METHOD_NOT_ALLOWED,
                )

    log.debug("No route matches request")
    return Response.new(HTTPStatus.NOT_FOUND.description, status=HTTPStatus.NOT_FOUND)
