import os

import pytest
from flask import Flask

from secunit.web.create_app import create_app


@pytest.fixture()
def flask_app() -> Flask:
    os.environ["FLASK_ENV"] = "testing"
    return create_app()


@pytest.fixture()
def client(flask_app: Flask):
    return flask_app.test_client()
