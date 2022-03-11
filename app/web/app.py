from typing import Optional

from aiohttp.web import (Application as AiohttpApplication,
                         Request as AiohttpRequest)
from aiohttp.web_urldispatcher import View as AiohttpView
from aiohttp_apispec import setup_aiohttp_apispec
from app.store import setup_store, Store
from app.store.database.database import Database
from app.web.config import setup_config, Config
from app.web.middlewares import setup_middlewares
from app.web.models import Customer, Administrator, Hairdresser, Session
from app.web.routes import setup_routes


class Application(AiohttpApplication):
    database: Optional[Database] = None
    store: Optional[Store] = None
    config: Optional[Config] = None


class Request(AiohttpRequest):

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    user: Customer | Administrator | Hairdresser | None = None
    session: Session | None = None

    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


def setup_app(app: Application, config_path: str):
    setup_config(app, config_path)
    setup_routes(app)
    setup_store(app)
    setup_aiohttp_apispec(app)
    setup_middlewares(app)
