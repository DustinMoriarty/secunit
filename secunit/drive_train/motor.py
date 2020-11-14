from abc import ABC, abstractmethod
from typing import SupportsFloat, SupportsAbs, Union
from gpiozero import DigitalOutputDevice, PWMOutputDevice


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


class ThreePinMotor(MotorAbc):

    def __init__(
            self,
            forward_device: DigitalOutputDevice,
            reverse_device: DigitalOutputDevice,
            speed_device: PWMOutputDevice
    ):
        super().__init__()
        self.forward_device = forward_device
        self.reverse_device = reverse_device
        self.speed_device = speed_device

    @property
    def speed(self):
        if self.reverse_device and self.forward_device:
            raise ValueError("reverse_device and forward_device are both true.")
        sgn = -1 if self.reverse_device.value and not self.forward_device else 1
        return sgn * self.speed_device

    def move(self, speed: Union[SupportsFloat, SupportsAbs]):
        self.forward_device = bool(float(speed) >= 0)
        self.reverse_device = bool(float(speed) < 0)
        self.speed_device = abs(speed)
