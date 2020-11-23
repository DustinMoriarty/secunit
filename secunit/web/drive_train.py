from flask import Blueprint, request, jsonify
from secunit.web.config import config

drive_train_app = Blueprint("drive_train", "drive_train", url_prefix="/drive_train")


@drive_train_app.route("/step", methods=["PUT"])
def step():
    data = request.json
    return jsonify(config().drive_train.step(**data)._asdict())


@drive_train_app.route("/enable", methods=["PUT"])
def enable():
    return jsonify(config().drive_train.enable()._asdict())
