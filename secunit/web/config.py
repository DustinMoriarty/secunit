from flask import current_app
from secunit.drive_train import DriveTrain
from typing import NamedTuple, SupportsFloat


class Config(NamedTuple):
    drive_train: DriveTrain
    time_step: SupportsFloat


def config() -> Config:
    return current_app.extensions["SECUNIT"]

