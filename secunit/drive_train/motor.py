from abc import ABC, abstractmethod
from typing import SupportsAbs, SupportsFloat, Union

from gpiozero import DigitalOutputDevice, PWMOutputDevice
from gpiozero.pins.mock import MockFactory, MockPin, MockPWMPin

from secunit.utils import saturate
from secunit.config import App

APP = App()


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
    def enable(self):
        ...

    @abstractmethod
    def disable(self):
        ...


class DeviceFactory:
    test = False

    # TODO: These class methods don't quite work with component.
    @classmethod
    @APP.component(pin=int, active_high=bool, initial_value=bool, test=bool)
    def digital_output_device(cls, pin=None, active_high=True, initial_value=False):
        if cls.test:
            return MockPin(MockFactory(), pin)
        else:
            return DigitalOutputDevice(
            pin=pin,
            active_high=active_high,
            initial_value=initial_value
        )

    @classmethod
    @APP.component(pin=int, active_high=bool, initial_value=bool, test=bool, frequency=int)
    def pwm_output_device(cls, pin=None, active_high=True, initial_value=0,
                          frequency=100, test=False):
        if cls.test:
            return MockPWMPin(MockFactory(), pin)
        else:
            return PWMOutputDevice(
                pin=pin, active_high=active_high, initial_value=initial_value,
                frequency=frequency,
                pin_factory=MockFactory() if test else None
            )


@APP.component(
    forward_device=DeviceFactory.digital_output_device,
    reverse_device=DeviceFactory.digital_output_device,
    speed_device=DeviceFactory.pwm_output_device,
    enable_device=DeviceFactory.digital_output_device
)
class ThreePinMotor(MotorAbc):
    def __init__(
        self,
        forward_device: DigitalOutputDevice,
        reverse_device: DigitalOutputDevice,
        speed_device: PWMOutputDevice,
        enable_device: DigitalOutputDevice,
    ):
        """
        Control a motor on a motor controller such as TB6612FNG.
        :param forward_device: Pin for reverse.
        :param reverse_device: Pin for forward.
        :param speed_device: Pin for speed.
        :param enable_device: Pin used to enable the motor.
        """
        super().__init__()
        self.forward_device = forward_device
        self.reverse_device = reverse_device
        self.speed_device = speed_device
        self.enable_device = enable_device

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

    def enable(self):
        self.enable_device.value = True

    def disable(self):
        self.enable_device.value = False
