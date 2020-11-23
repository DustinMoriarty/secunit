from typing import Callable, Dict


class Component:
    def __init__(self, callback: Callable, arg_types: Dict = None):
        self.callback = callback
        self.arg_types = arg_types if arg_types is None else {}

    def __call__(self, **kwargs):
        return self.callback(**kwargs)
