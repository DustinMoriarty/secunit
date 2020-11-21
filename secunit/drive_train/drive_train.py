from secunit.config import App
from secunit.drive_train.motor import MotorAbc
from secunit.utils import saturate
from time import sleep
from typing import NamedTuple, SupportsFloat

APP = App()


@APP.component()
class DriveTrain:
    def __init__(self, left_motor: MotorAbc, right_motor: MotorAbc):
        self.left_motor = left_motor
        self.right_motor = right_motor

    def move(self, translate, rotate):
        speed_left = saturate(translate - rotate, -1, 1)
        speed_right = saturate(translate + rotate, -1, 1)
        self.left_motor.move(speed_left)
        self.right_motor.move(speed_right)

    def step(self, translate, rotate, t=0.02):
        self.move(translate, rotate)
        sleep(t)
        self.stop()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def close(self):
        self.left_motor.close()
        self.right_motor.close()


class DriveTrainState(NamedTuple):
    left_motor_speed: SupportsFloat
    right_motor_speed: SupportsFloat


def drive_train_state(drive_train: DriveTrain):
    return DriveTrainState(drive_train.left_motor.speed, drive_train.right_motor.speed)