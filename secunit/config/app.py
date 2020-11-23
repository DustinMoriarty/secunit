from logging import INFO
from typing import Callable, Dict, Text, Tuple

from secunit.config.component import Component
from secunit.config.exc import (AppMergeCollisions, ComponentNotFound,
                                InvalidConfigKey, TypeNotDefined)
from secunit.config.selectable_type import SelectableType
from secunit.config.utils import get_type
from secunit.utils import default_logger


class App:
    def __init__(self, logger=None):
        self._constructors: Dict[Text, Component] = {}
        self.logger = logger if logger is not None else default_logger(str(self), INFO)
        self.logger.debug("Created App.")

    def __add__(self, other):
        collisions = set(self.constructors.keys()) & set(other.constructors.keys())
        if collisions:
            raise AppMergeCollisions(
                f"Apps cannot be merged due to collisions on the following "
                f"keys {collisions}"
            )
        new = type(self)()
        for k, v in self.constructors.items():
            new.set_constructor(k, v)
        for k, v in other.constructors.items():
            new.set_constructor(k, v)
        return new

    @property
    def constructors(self):
        return self._constructors

    def set_constructor(self, key, value):
        self.logger.debug(f"Registering constructor {key} with value {value}")
        self._constructors[key] = value

    @property
    def types(self) -> Tuple[Callable]:
        return tuple(x.callback for x in self.constructors.values())

    def component(self, **kwargs):
        """
        Decorator for constructor functions.

        :param key: The key to use for the configuration.
        :param kwargs: The type for each argument in the function f.
        :return:
        """

        def wrapper(f):
            _key = get_type(f)
            cls = Component(f, kwargs)
            self.set_constructor(_key, cls)
            return f

        return wrapper

    def selectable_component(self, name, *constructors):
        selectable_constructor = SelectableType(name, *constructors)
        # TODO: Need kwargs for Component.
        self.set_constructor(
            get_type(selectable_constructor), Component(selectable_constructor)
        )
        return selectable_constructor

    def build(self, tp: Text, context: Dict):
        self.logger.debug(f"Building type {tp} from {context}")
        try:
            constructor: Component = self.constructors[tp]
        except KeyError:
            raise ComponentNotFound(f"Component {tp} not found.")
        _kwargs = {}
        for arg_name, arg in context.items():
            if hasattr(arg, "items"):
                # Recursion for nested dictionaries/constructors.
                if arg_name.lower() in constructor.arg_types:
                    arg_tp = str(get_type(constructor.arg_types[arg_name.lower()]))
                else:
                    raise TypeNotDefined(
                        f"Unable to determine type for {arg_name} in config object {tp}"
                    )
                _kwargs[arg_name] = self.build(arg_tp, arg)
            else:
                try:
                    arg_tp = constructor.arg_types[arg_name]
                except KeyError:
                    raise InvalidConfigKey(
                        f"Config key {arg_name} not in {constructor.arg_types.keys()}"
                    )
                _kwargs[arg_name] = arg_tp(arg)
        return constructor.callback(**_kwargs)
