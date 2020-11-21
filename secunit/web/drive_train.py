from flask import Blueprint, request
from secunit.web.config import config

drive_train_app = Blueprint("drive_train", "drive_train", url_prefix="/drive_train")


@drive_train_app.route("/step", methods=["PUT"])
def step():
    data = request.json()
    config().drive_train.step(
        data["translate"], data["rotate"], config().time_step
    )