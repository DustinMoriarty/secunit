from flask import Flask
from secunit.web.drive_train import drive_train_app
from secunit.drive_train import APP as DRIVE_TRAIN_APP
from secunit.web.config import Config
from pathlib import Path
from typing import Dict
import json
from secunit.config.exc import KeyNotInConfig
from secunit.drive_train.motor import mock_factory
from gpiozero import Device

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
    pin_factory = mock_factory() if app.testing else None
    Device.pin_factory = pin_factory
    try:
        sec_unit_config = settings["SECUNIT"]
        sec_unit_config.update(app.config.get("SECUNIT", {}))
        app.extensions["SECUNIT"] = Config(
            DRIVE_TRAIN_APP.build(
                "DriveTrain",
                sec_unit_config["DRIVE_TRAIN"]
            ),
            float(sec_unit_config["TIME_STEP"]),
            pin_factory
        )
    except KeyError as e:
        raise KeyNotInConfig(e)
    app.register_blueprint(drive_train_app)
    return app
