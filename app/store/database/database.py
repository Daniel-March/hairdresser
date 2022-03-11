import typing

from app.web.models import *

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Database:
    recover_password_requests: dict[str:str] = {}

    async def connect(self, app: "Application"):
        dialect = app.config.database_config.dialect
        driver = app.config.database_config.driver
        host = app.config.database_config.host
        port = app.config.database_config.port
        db_name = app.config.database_config.db_name
        user_name = app.config.database_config.user_name
        user_password = app.config.database_config.user_password
        await db.set_bind(f"{dialect}+{driver}://{user_name}:{user_password}@{host}:{port}/{db_name}")
        await db.gino.create_all()
        print("Database connected")

    async def disconnect(self, app: "Application" = None):
        await db.pop_bind().close()
        print("Database disconnected")

    async def regenerate(self):
        await db.status("DROP TABLE IF EXISTS shift_x_hairdresser;")
        await db.status("DROP TABLE IF EXISTS sessions;")
        await db.status("DROP TABLE IF EXISTS reception_x_service;")
        await db.status("DROP TABLE IF EXISTS department_x_administrator;")
        await db.status("DROP TABLE IF EXISTS department_x_hairdresser;")
        await db.status("DROP TABLE IF EXISTS department_x_service;")
        await db.status("DROP TABLE IF EXISTS administrators;")
        await db.status("DROP TABLE IF EXISTS services;")
        await db.status("DROP TABLE IF EXISTS departments;")
        await db.status("DROP TABLE IF EXISTS receptions;")
        await db.status("DROP TABLE IF EXISTS customers;")
        await db.status("DROP TABLE IF EXISTS shifts;")
        await db.status("DROP TABLE IF EXISTS hairdressers;")
        await db.gino.create_all()
