from secunit.drive_train.motor import MotorAbc
from secunit.utils import saturate
from typing import NamedTuple, SupportsFloat
from time import sleep
from config_injector import config


class DriveTrain:
    def __init__(self, left_motor: MotorAbc, right_motor: MotorAbc):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.left_motor.enable()
        self.right_motor.enable()

    def move(self, translate, rotate):
        print(f"translate={translate}, rotate={rotate}")
        speed_left = saturate(translate - rotate, -1, 1)
        speed_right = saturate(translate + rotate, -1, 1)
        print(f"speed_left={speed_left}, speed_right={speed_right}")
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