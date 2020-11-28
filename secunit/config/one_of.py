from typing import Iterator, Callable

from secunit.config.exc import TypeNotDefined
from secunit.config.utils import get_type
from collections.abc import Mapping


class OneOf(Mapping):

    def __init__(self, name, *callables: Callable):
        self.callables = {}
        self.update(*callables)
        self.__name__ = name

    def __call__(self, **kwargs):
        try:
            # Get type this way in order to avoid colliding with built in name type.
            type_name = kwargs.pop("type")
        except KeyError:
            raise TypeError(
                f'{self.__name__} missing required argument "type" in kwargs'
            )
        tp = self.callables.get(type_name)
        if tp is None:
            raise TypeNotDefined(f"Type {tp} not defined for {type(self)}")
        return tp(**kwargs)

    def __getitem__(self, item):
        return self.callables[item]

    def __iter__(self) -> Iterator[Callable]:
        return iter(self.callables)

    def __len__(self) -> int:
        return len(self.callables)

    def update(self, *callables: Callable):
        self.callables.update({get_type(t): t for t in callables})

    def type(self, f):
        """
        Decorator for selectable type constructor functions and classes.
        """
        self.update(f)
        return f
