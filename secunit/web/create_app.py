import json
from pathlib import Path
from typing import Dict

from config_injector import Injector
from flask import Flask
from gpiozero import Device

from secunit.drive_train.motor import mock_factory
from secunit.exc import KeyNotInConfig
from secunit.web.drive_train import drive_train_app
from secunit.config import secunit

RESOURCES_DIRECTORY = Path(__file__).parent.parent / "resources"
DEFAULT_SETTINGS_FILE = RESOURCES_DIRECTORY / "settings.json"


def default_settings() -> Dict:
    with DEFAULT_SETTINGS_FILE.open() as f:
        return json.load(f)


def create_app() -> Flask:
    app = Flask("secunit", instance_relative_config=True)
    settings = default_settings()
    app.config.from_object(settings)
    app.config.from_json("settings.json", silent=True)
    if app.env.lower() == "testing":
        app.testing = True
    try:
        context = settings["SECUNIT"]
    except KeyError as e:
        raise KeyNotInConfig(e)
    injector = Injector(context=context)
    app.extensions["SECUNIT"] = injector.instantiate(secunit)
    app.register_blueprint(drive_train_app)
    return app
