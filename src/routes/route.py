from abc import ABC, abstractmethod
from http import HTTPStatus
from urllib.parse import urlparse
from js import Response


class Route(ABC):

    def __init__(self, path: list[str]) -> None:
        self.path = path

    def matches(self, url: str) -> bool:
        url_path = list(
            filter(lambda slice: slice != "", urlparse(url).path.split("/"))
        )
        return url_path == self.path

    def context(self, db=None) -> None:
        self.insightsdb = db

    @abstractmethod
    async def auth(self, request, env) -> bool:
        raise NotImplementedError

    async def get(self, request, env) -> Response:
        return Response.new(
            HTTPStatus.METHOD_NOT_ALLOWED.description,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )

    async def head(self, request, env) -> Response:
        get_response = await self.get(request, env)
        return Response.new(None, status=get_response.status, headers=get_response.headers)

    async def post(self, request, env) -> Response:
        return Response.new(
            HTTPStatus.METHOD_NOT_ALLOWED.description,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )

    async def put(self, request, env) -> Response:
        return Response.new(
            HTTPStatus.METHOD_NOT_ALLOWED.description,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )

    async def patch(self, request, env) -> Response:
        return Response.new(
            HTTPStatus.METHOD_NOT_ALLOWED.description,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )

    async def delete(self, request, env) -> Response:
        return Response.new(
            HTTPStatus.METHOD_NOT_ALLOWED.description,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )

    async def options(self, request, env) -> Response:
        return Response.new(
            HTTPStatus.METHOD_NOT_ALLOWED.description,
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
