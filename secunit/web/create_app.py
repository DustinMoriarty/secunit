from flask import Flask
from secunit.web.drive_train import drive_train_app
from secunit.drive_train import APP as DRIVE_TRAIN_APP
from secunit.web.config import Config


def create_app() -> Flask:
    app = Flask("secunit", instance_relative_config=True)
    app.config.from_json("settings.json")
    app.extensions["SECUNIT"] = Config(
        DRIVE_TRAIN_APP.build(
            "DriveTrain",
            app.config.get("SEC_UNIT", {}).get("DRIVE_TRAIN", {})
        ),
        float(app.config["SECUNIT"].get("TIME_STEP", 0.02))
    )
    app.register_blueprint(drive_train_app)
    return app
