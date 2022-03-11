import typing
from dataclasses import dataclass

import yaml

from app.web.models import Organization

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class DatabaseConfig:
    dialect: str
    driver: str
    host: str
    port: int
    db_name: str
    user_name: str
    user_password: str


@dataclass
class Session:
    life_time: int


@dataclass
class Config:
    organization: Organization
    database_config: DatabaseConfig
    session: Session


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        organization=Organization(
            name=raw_config["organization"]["name"],
            password=raw_config["organization"]["password"],
            email=raw_config["organization"]["email"]
        ),
        database_config=DatabaseConfig(
            dialect=raw_config["database"]["dialect"],
            driver=raw_config["database"]["driver"],
            host=raw_config["database"]["host"],
            port=raw_config["database"]["port"],
            db_name=raw_config["database"]["db_name"],
            user_name=raw_config["database"]["user_name"],
            user_password=raw_config["database"]["user_password"]
        ),
        session=Session(
            life_time=raw_config["cookie"]["life_time"]
        )
    )
