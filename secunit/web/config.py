from flask import current_app
from secunit.drive_train import DriveTrain
from typing import NamedTuple, SupportsFloat
from gpiozero.pins import Factory


class Config(NamedTuple):
    drive_train: DriveTrain
    time_step: SupportsFloat
    pin_factory: Factory


def config() -> Config:
    return current_app.extensions["SECUNIT"]

