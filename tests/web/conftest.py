import os

import pytest

from flask import Flask

from secunit.web.create_app import create_app


@pytest.fixture()
def flask_app(pin_factory) -> Flask:
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()
    yield app


@pytest.fixture()
def client(flask_app: Flask):
    return flask_app.test_client()
