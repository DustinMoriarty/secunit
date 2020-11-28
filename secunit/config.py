from typing import SupportsInt, NamedTuple

from config_injector import config
from gpiozero import DigitalOutputDevice, PWMOutputDevice
from gpiozero.pins import Factory
from gpiozero.pins.mock import MockFactory, MockPWMPin
from gpiozero.pins.native import NativeFactory
from gpiozero.pins.pi import PiFactory

from secunit.drive_train import DriveTrain
from secunit.drive_train.drive_train import DriveTrain
from secunit.drive_train.motor import MotorAbc, ThreePinMotor


@config()
def mock_factory():
    return MockFactory(pin_class=MockPWMPin)


@config()
def native_factory():
    return NativeFactory()


@config()
def pi_factory():
    return PiFactory()


@config(
    forward_pin=int,
    reverse_pin=int,
    speed_pin=int,
    frequency=int,
    pin_factory=(mock_factory, native_factory, pi_factory),
)
def three_pin_motor(
    forward_pin: SupportsInt,
    reverse_pin: SupportsInt,
    speed_pin: SupportsInt,
    frequency: SupportsInt = 10000,
    pin_factory: Factory = None,
):
    return ThreePinMotor(
        forward_device=DigitalOutputDevice(pin=forward_pin, pin_factory=pin_factory),
        reverse_device=DigitalOutputDevice(pin=reverse_pin, pin_factory=pin_factory),
        speed_device=PWMOutputDevice(
            pin=speed_pin, frequency=frequency, pin_factory=pin_factory
        ),
    )


@config(left_motor=tuple([three_pin_motor]), right_motor=tuple([three_pin_motor]), time_step=int)
def drive_train(left_motor: MotorAbc, right_motor: MotorAbc, time_step: SupportsInt):
    return DriveTrain(
        left_motor=left_motor, right_motor=right_motor, time_step=time_step
    )


class SecUnit(NamedTuple):
    drive_train: DriveTrain


@config(drive_train=drive_train)
def secunit(drive_train: DriveTrain):
    return SecUnit(drive_train)