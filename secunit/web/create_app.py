import json

from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
from logging import INFO
from logging import Logger
from logging import StreamHandler
from logging import getLogger
from logging.config import dictConfig
from pathlib import Path
from sys import stderr
from typing import Dict
from typing import SupportsInt
from typing import Text
from typing import Union

from config_injector import Injector
from flask import Flask
from jsonformatter import JsonFormatter

from secunit.config import SecUnit
from secunit.config import secunit
from secunit.exc import InvalidFlaskEnv
from secunit.exc import KeyNotInConfig
from secunit.utils import APP_NAME
from secunit.web.drive_train import drive_train_app
from secunit.web.ui import ui_app


RESOURCES_DIRECTORY = Path(__file__).parent.parent / "resources"


def default_settings(env) -> Dict:
    config_file = RESOURCES_DIRECTORY / f"{env}.json"
    try:
        with config_file.open() as f:
            return json.load(f)
    except FileNotFoundError:
        supported_env = tuple(
            x.name.split(".")[0] for x in RESOURCES_DIRECTORY.glob("*.json")
        )
        raise InvalidFlaskEnv(f"FLASK_ENV {env} is not one of {supported_env}")


def converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    elif isinstance(o, timedelta):
        return str(o)
    else:
        return o


def handler(level: Union[SupportsInt, Text] = INFO) -> Logger:
    fmt = OrderedDict(
        (
            ("Name", "name"),
            ("Asctime", "asctime"),
            ("LevelName", "levelname"),
            ("Message", "message"),
        )
    )
    formatter = JsonFormatter(fmt, mix_extra=True, default=converter)
    handler = StreamHandler(stderr)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def create_app() -> Flask:
    app = Flask(
        APP_NAME,
        instance_relative_config=True,
        instance_path=Path().home() / f".{APP_NAME}",
        static_url_path="/"
    )
    config = default_settings(app.env)
    app.config.update(config)
    app.config.from_json("config.json", silent=True)
    if app.env.lower() == "testing":
        app.testing = True
    try:
        context = config["SECUNIT"]
    except KeyError as e:
        raise KeyNotInConfig(e)
    injector = Injector(context=context)
    unit: SecUnit = injector.instantiate(secunit)
    app.extensions["SECUNIT"] = unit
    dictConfig(unit.logging)
    app.logger = getLogger("flaskapp")
    app.logger.info(msg="Application setup.")
    app.register_blueprint(drive_train_app)
    app.register_blueprint(ui_app)
    return app
