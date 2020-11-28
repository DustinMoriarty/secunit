from abc import ABC, abstractmethod
from typing import SupportsAbs, SupportsFloat, Union

from gpiozero import DigitalOutputDevice, PWMOutputDevice
from gpiozero.pins.mock import MockFactory, MockPWMPin

from secunit.utils import saturate


class MotorAbc(ABC):
    @property
    @abstractmethod
    def speed(self):
        ...

    def stop(self):
        self.move(0)

    @abstractmethod
    def move(self, speed: SupportsFloat):
        """
        Move the motor.

        :param speed: A value between -1 and 1 representing the speed of the motor
            where -1 is full reverse and 1 is full forward.
        """
        ...

    @abstractmethod
    def close(self):
        ...


def mock_factory():
    return MockFactory(pin_class=MockPWMPin)


def digital_output_device(pin=None, active_high=True, initial_value=False):
    return DigitalOutputDevice(
        pin=pin, active_high=active_high, initial_value=initial_value
    )


def pwm_output_device(pin=None, active_high=True, initial_value=0, frequency=100):
    return PWMOutputDevice(
        pin=pin,
        active_high=active_high,
        initial_value=initial_value,
        frequency=frequency,
    )


class ThreePinMotor(MotorAbc):
    def __init__(
        self,
        forward_device: DigitalOutputDevice,
        reverse_device: DigitalOutputDevice,
        speed_device: PWMOutputDevice,
    ):
        """
        Control a motor on a motor controller such as TB6612FNG.
        :param forward_device: Pin for reverse.
        :param reverse_device: Pin for forward.
        :param speed_device: Pin for speed.
        """
        super().__init__()
        self.forward_device = forward_device
        self.reverse_device = reverse_device
        self.speed_device = speed_device

    @property
    def speed(self):
        if self.reverse_device.value and self.forward_device.value:
            raise ValueError("reverse_device and forward_device are both true.")
        sgn = -1 if self.reverse_device.value and not self.forward_device.value else 1
        return sgn * self.speed_device.value

    def move(self, speed: Union[SupportsFloat, SupportsAbs]):
        _speed = float(saturate(speed, -1, 1))
        self.forward_device.value = bool(_speed > 0)
        self.reverse_device.value = bool(_speed < 0)
        self.speed_device.value = abs(_speed)

    def close(self):
        self.forward_device.value = False
        self.reverse_device.value = False
        self.speed_device.value = 0
        self.forward_device.close()
        self.reverse_device.close()
        self.speed_device.close()
