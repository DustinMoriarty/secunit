from secunit.drive_train.drive_train import APP as _DRIVE_TRAIN_APP
from secunit.drive_train.drive_train import DriveTrain
from secunit.drive_train.motor import APP as _MOTOR_APP
from secunit.drive_train.motor import MotorAbc, ThreePinMotor

APP = _DRIVE_TRAIN_APP + _MOTOR_APP
