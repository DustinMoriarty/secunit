from typing import Callable, Dict, Text

from secunit.config.exc import TypeNotDefined
from secunit.config.utils import get_type


class SelectableTypeNoConstructors(Exception):
    ...


class SelectableType:
    def __init__(self, name, *constructors):
        self.constructors = {}
        self.update(*constructors)
        self.__name__ = name

    def __call__(self, **kwargs):
        try:
            # Get type this way in order to avoid colliding with built in name type.
            type_name = kwargs.pop("type")
        except KeyError:
            raise TypeError(
                f'{self.__name__} missing required argument "type" in kwargs'
            )
        tp = self.constructors.get(type_name)
        if tp is None:
            raise TypeNotDefined(f"Type {tp} not defined for {type(self)}")
        return tp(**kwargs)

    def update(self, *constructors):
        self.constructors.update({get_type(t): t for t in constructors})

    def type(self, f):
        """
        Decorator for selectable type constructor functions and classes.
        """
        self.update(f)
        return f
