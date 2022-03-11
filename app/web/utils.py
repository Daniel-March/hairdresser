import typing
from datetime import datetime
from functools import wraps
from hashlib import sha256

from aiohttp.web_exceptions import HTTPUnauthorized, HTTPNotFound
from aiohttp.web_response import json_response as aiohttp_json_response

from app.web.models import Session, Customer, Administrator, Hairdresser, Organization

if typing.TYPE_CHECKING:
    from app.web.app import View


def json_response(data: dict = None, status_code: int = 200, message: str = None, headers: dict = None,
                  cookies: dict = None):
    if headers is None and cookies is not None:
        headers = {}
    if cookies is not None:
        headers["set-cookie"] = ";".join([f"{k}= {v}" for k, v in cookies.items()])

    return aiohttp_json_response(data=data, status=status_code, text=message, headers=headers)


def error_json_response(data: dict, status_code: int = 500, message: str = "server error", headers=None):
    return aiohttp_json_response(data=data, status=status_code, text=message, headers=headers)


def check_session(user_type: type):
    from app.web.app import View, Request

    def handler(func):
        @wraps(func)
        async def inner(view: View, *args, **kwargs):
            request: Request = view.request
            session_key = request.cookies.get("session")
            if session_key is None:
                raise HTTPUnauthorized

            session: Session = await request.app.store.session_accessor.get_by_key(session_key, throw_error=False)
            if session is None or session.user_type != user_type.__name__:
                raise HTTPUnauthorized
            if session.die_time < datetime.utcnow().timestamp():
                await session.delete()
                raise HTTPUnauthorized  # ToDo поменять
            if user_type == Customer:
                user = await view.request.app.store.customer_accessor.get_by_id(session.user_id)
            elif user_type == Administrator:
                user = await view.request.app.store.administrator_accessor.get_by_id(session.user_id)
            elif user_type == Hairdresser:
                user = await view.request.app.store.hairdresser_accessor.get_by_id(session.user_id)
            elif user_type == Organization:
                user = view.request.app.config.organization
            else:
                raise ValueError(f"Unknown usertype {user_type}")
            view.user = user
            view.session = session
            response = await func(view, *args, **kwargs)

            try:
                new_key = await view.request.app.store.session_accessor.update_key(session.key)
                response.cookies["session"] = new_key
            except HTTPNotFound:
                pass
            return response

        return inner

    return handler


def encode_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()
