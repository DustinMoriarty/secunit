from abc import ABC, abstractmethod
from typing import SupportsFloat


class MotorAbc(ABC):
    def __init__(self):
        self._speed: SupportsFloat = 0
        self.stop()

    @property
    def speed(self):
        return self._speed

    @abstractmethod
    def _move(self, speed: SupportsFloat):
        ...

    def stop(self):
        self.move(0)

    def move(self, speed: SupportsFloat):
        """
        Move the motor.
        :param speed: A value between -1 and 1 representing the speed of the motor where -1 is full reverse and 1 is
            full forward.
        """
        self._move(speed)
        self._speed = speed
