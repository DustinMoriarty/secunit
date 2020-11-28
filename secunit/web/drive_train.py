from flask import Blueprint, jsonify, request

from secunit.web.settings import settings

drive_train_app = Blueprint("drive_train", "drive_train", url_prefix="/drive_train")


@drive_train_app.route("/step", methods=["PUT"])
def step():
    data = request.json
    return jsonify(settings().drive_train.step(**data)._asdict())
