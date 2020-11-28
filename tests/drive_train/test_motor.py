from typing import SupportsFloat

import pytest
from gpiozero import DigitalOutputDevice, PWMOutputDevice

from secunit.drive_train.motor import ThreePinMotor


@pytest.fixture()
def three_pin_motor(pin_factory):
    motor = ThreePinMotor(
        DigitalOutputDevice(1, pin_factory=pin_factory),
        DigitalOutputDevice(2, pin_factory=pin_factory),
        PWMOutputDevice(3, pin_factory=pin_factory),
    )
    yield motor
    motor.close()


@pytest.mark.parametrize(
    (
        "speed",
        "expected_forward_value",
        "expected_reverse_value",
        "expected_speed_value",
    ),
    ((1, True, False, 1), (0, False, False, 0), (-1, False, True, 1)),
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


@pytest.mark.parametrize("speed", (-1, -0.5, 0, 0.5, 1))
def test_three_pin_motor_speed(three_pin_motor: ThreePinMotor, speed):
    three_pin_motor.move(speed)
    assert float(three_pin_motor.speed) == float(speed)


def test_three_pin_motor_stop(three_pin_motor: ThreePinMotor):
    three_pin_motor.move(1)
    three_pin_motor.stop()
    assert not three_pin_motor.forward_device.value
    assert not three_pin_motor.reverse_device.value
    assert three_pin_motor.speed_device.value == 0
