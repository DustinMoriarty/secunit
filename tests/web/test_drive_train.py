from flask import Flask
from flask.testing import Client
import pytest


@pytest.mark.parametrize("translate, rotate", [(1, 0), (0, 1)])
def test_drive_train_step(flask_app: Flask, client: Client, translate, rotate):
    data = {"translate": translate, "rotate": rotate}
    response = client.put("/drive_train/step", json=data)


