from typing import Callable, Dict


class Component:
    def __init__(self, callback: Callable, arg_types: Dict):
        self.callback = callback
        self.arg_types = arg_types
