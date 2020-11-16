import pytest
from secunit.drive_train import APP, DriveTrain
from secunit.config.app import get_type


@pytest.fixture()
def drive_train_config():
    return {
        "drive_train": {
            "left_motor": {
                "type": "ThreePinMotor",
                "forward_device": {"pin": 1},
                "reverse_device": {"pin": 2},
                "speed_device": {"pin": 3},
                "enabled_device": {"pin": 4}
            },
            "right_motor": {
                "type": "ThreePinMotor",
                "forward_device": {"pin": 5},
                "reverse_device": {"pin": 6},
                "speed_device": {"pin": 7},
                "enabled_device": {"pin": 8}
            }
        }
    }


def test_app(drive_train_config):
    drive_train = APP.build(get_type(DriveTrain), drive_train_config["drive_train"])