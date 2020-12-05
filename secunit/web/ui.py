from flask import Blueprint, current_app

ui_app = Blueprint("ui", "ui", url_prefix="", static_folder="static")

@ui_app.route("/", methods=["GET"])
def root():
    current_app.logger.info("Getting Root")
    return ui_app.send_static_file("index.html")