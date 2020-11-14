from typing import SupportsFloat

from secunit.drive_train.drive_train import DriveTrain
from secunit.drive_train.motor import MotorAbc
import pytest


class MockMotor(MotorAbc):
    def __init__(self):
        self._speed = 0

    @property
    def speed(self):
        return self._speed

    def move(self, speed: SupportsFloat):
        self._speed = speed


@pytest.fixture()
def left_motor():
    return MockMotor()


@pytest.fixture()
def right_motor():
    return MockMotor()


@pytest.fixture()
def drive_train(left_motor, right_motor):
    return DriveTrain(left_motor, right_motor)