from time import sleep
from typing import NamedTuple
from typing import SupportsFloat

from secunit.drive_train.motor import MotorAbc
from secunit.utils import saturate


class DriveTrainState(NamedTuple):
    left_motor_speed: SupportsFloat
    right_motor_speed: SupportsFloat


class DriveTrain:
    def __init__(self, left_motor: MotorAbc, right_motor: MotorAbc, time_step=0.5):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.time_step = time_step

    @property
    def state(self) -> DriveTrainState:
        return DriveTrainState(self.left_motor.speed, self.right_motor.speed)

    def move(self, translate, rotate) -> DriveTrainState:
        speed_left = saturate(translate - rotate, -1, 1)
        speed_right = saturate(translate + rotate, -1, 1)
        self.left_motor.move(speed_left)
        self.right_motor.move(speed_right)
        return self.state

    def step(self, translate, rotate) -> DriveTrainState:
        state = self.move(translate, rotate)
        sleep(self.time_step)
        self.stop()
        return state

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
        return self.state

    def close(self):
        self.left_motor.close()
        self.right_motor.close()
        return self.state
