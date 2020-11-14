from typing import SupportsFloat
import pytest
from secunit.drive_train.motor import ThreePinMotor


class MockDevice:
    value = None


@pytest.fixture()
def three_pin_motor():
    return ThreePinMotor(MockDevice(), MockDevice(), MockDevice(), MockDevice())


@pytest.mark.parametrize(
    (
        "speed",
        "expected_forward_value",
        "expected_reverse_value",
        "expected_speed_value",
    ),
    (
            (1, True, False, 1),
            (0, False, False, 0),
            (-1, False, True, 1)
    )
)
def test_three_pin_motor_move(
    three_pin_motor: ThreePinMotor,
    speed: SupportsFloat,
    expected_forward_value: bool,
    expected_reverse_value: bool,
    expected_speed_value: SupportsFloat,
):
    three_pin_motor.stop()
    three_pin_motor.move(speed)
    assert expected_forward_value == three_pin_motor.forward_device.value
    assert expected_reverse_value == three_pin_motor.reverse_device.value
    assert expected_speed_value == three_pin_motor.speed_device.value
