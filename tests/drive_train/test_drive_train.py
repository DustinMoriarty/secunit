import pytest
from typing import SupportsFloat
from secunit.drive_train.drive_train import DriveTrain


@pytest.mark.parametrize(
    ("translate", "rotate", "expected_left_speed", "expected_right_speed"),
    (
        (1, 0, 1, 1),
        (-1, 0, -1, -1),
        (0, 1, -1, 1),
        (0, -1, 1, -1),
        (0.5, 0.5, 0, 1),
        (-0.5, 0.5, -1, 0),
        (1, 1, 0, 1),
    ),
)
def test_drive_train_move(
    drive_train: DriveTrain,
    translate: SupportsFloat,
    rotate: SupportsFloat,
    expected_left_speed,
    expected_right_speed,
):
    drive_train.move(translate, rotate)
    assert -1 <= drive_train.left_motor.speed <= 1
    assert -1 <= drive_train.right_motor.speed <= 1
    assert expected_left_speed == drive_train.left_motor.speed
    assert expected_right_speed == drive_train.right_motor.speed


def test_drive_train_motor_stop(drive_train: DriveTrain):
    drive_train.move(1, 1)
    drive_train.stop()
    assert drive_train.right_motor.speed == 0
    assert drive_train.left_motor.speed == 0
