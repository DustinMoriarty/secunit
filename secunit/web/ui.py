from flask import Blueprint
from flask import current_app


ui_app = Blueprint("ui", "ui", url_prefix="")


@ui_app.route("/", methods=["GET"])
def root():
    current_app.logger.info("Getting Root")
    return current_app.send_static_file("index.html")
