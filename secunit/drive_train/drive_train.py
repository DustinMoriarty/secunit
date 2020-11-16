from secunit.drive_train.motor import MotorAbc
from secunit.utils import saturate
from secunit.config import App

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

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()
