import typing

from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware

from app.web.utils import json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application
    from app.web.app import Request


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnauthorized as e:
        return json_response({"error": e.text}, status_code=401)
    except Exception as e:
        raise e


@middleware
async def session_updating_middleware(request: "Request", handler):
    response = await handler(request)

    return response


def setup_middlewares(app: "Application"):
    app.middlewares.append(validation_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(session_updating_middleware)
