import pytest

from secunit.config.app import get_type
from secunit.drive_train import APP, DriveTrain


@pytest.fixture()
def drive_train_config():
    return {
        "drive_train": {
            "left_motor": {
                "type": "ThreePinMotor",
                "forward_device": {"pin": 1},
                "reverse_device": {"pin": 2},
                "speed_device": {"pin": 3},
                "enable_device": {"pin": 4},
            },
            "right_motor": {
                "type": "ThreePinMotor",
                "forward_device": {"pin": 5},
                "reverse_device": {"pin": 6},
                "speed_device": {"pin": 7},
                "enable_device": {"pin": 8},
            },
        }
    }


def test_app(drive_train_config, pin_factory):
    drive_train: DriveTrain = APP.build(
        get_type(DriveTrain), drive_train_config["drive_train"]
    )
    assert (
        drive_train_config["drive_train"]["left_motor"]["forward_device"]["pin"]
        == drive_train.left_motor.forward_device.pin.number
    )
    assert (
            drive_train_config["drive_train"]["left_motor"]["reverse_device"]["pin"]
            == drive_train.left_motor.reverse_device.pin.number
    )
    assert (
            drive_train_config["drive_train"]["left_motor"]["speed_device"]["pin"]
            == drive_train.left_motor.speed_device.pin.number
    )
    assert (
            drive_train_config["drive_train"]["left_motor"]["enable_device"]["pin"]
            == drive_train.left_motor.enable_device.pin.number
    )
    assert (
            drive_train_config["drive_train"]["right_motor"]["forward_device"]["pin"]
            == drive_train.right_motor.forward_device.pin.number
    )
    assert (
            drive_train_config["drive_train"]["right_motor"]["reverse_device"]["pin"]
            == drive_train.right_motor.reverse_device.pin.number
    )
    assert (
            drive_train_config["drive_train"]["right_motor"]["speed_device"]["pin"]
            == drive_train.right_motor.speed_device.pin.number
    )
    assert (
            drive_train_config["drive_train"]["right_motor"]["enable_device"]["pin"]
            == drive_train.right_motor.enable_device.pin.number
    )
