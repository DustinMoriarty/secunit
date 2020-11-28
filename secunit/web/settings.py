from flask import current_app

from secunit.config import SecUnit


def settings() -> SecUnit:
    return current_app.extensions["SECUNIT"]
