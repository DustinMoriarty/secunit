from flask import Flask
from flask.testing import Client


def test_drive_train_step(flask_app: Flask, client: Client):
    translate = 1
    rotate = 0
    data = {"translate": translate, "rotate": rotate}
    response = client.put("/drive_train/step", json=data)
    assert response.status_code == 200
    responese_data = response.json
    assert 1 == responese_data["left_motor_speed"]
    assert 1 == responese_data["right_motor_speed"]

