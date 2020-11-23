from typing import NamedTuple, SupportsFloat

from flask import current_app
from gpiozero.pins import Factory

from secunit.drive_train import DriveTrain


class Config(NamedTuple):
    drive_train: DriveTrain
    time_step: SupportsFloat
    pin_factory: Factory


def config() -> Config:
    return current_app.extensions["SECUNIT"]
