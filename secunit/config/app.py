from logging import INFO
from typing import Callable, Dict, Text, Tuple

from secunit.config.component import Component
from secunit.config.exc import (AppMergeCollisions, ComponentNotFound,
                                InvalidConfigKey, TypeNotDefined)
from secunit.config.one_of import OneOf
from secunit.config.utils import get_type
from secunit.utils import default_logger


class App:
    def __init__(self, logger=None):
        self._components: Dict[Text, Component] = {}
        self.logger = logger if logger is not None else default_logger(str(self), INFO)
        self.logger.debug("Created App.")

    def __add__(self, other):
        collisions = set(self.components.keys()) & set(other.components.keys())
        if collisions:
            raise AppMergeCollisions(
                f"Apps cannot be merged due to collisions on the following "
                f"keys {collisions}"
            )
        new = type(self)()
        for k, v in self.components.items():
            new.set_callable(k, v)
        for k, v in other.components.items():
            new.set_callable(k, v)
        return new

    @property
    def components(self):
        return self._components

    def set_callable(self, key, value):
        self.logger.debug(f"Registering constructor {key} with value {value}")
        self._components[key] = value

    def component(self, **kwargs):
        """
        Decorator for constructor functions.

        :param key: The key to use for the configuration.
        :param kwargs: The type for each argument in the function f.
        :return:
        """

        def wrapper(f):
            _key = get_type(f)
            component = Component(f, kwargs)
            self.set_callable(_key, component)
            return component

        return wrapper

    def selectable_component(self, name, *constructors):
        selectable_constructor = OneOf(name, *constructors)
        self.set_callable(
            get_type(selectable_constructor), Component(selectable_constructor)
        )
        return selectable_constructor

    def build(self, tp: Text, context: Dict):
        self.logger.debug(f"Building type {tp} from {context}")
        try:
            component: Component = self.components[tp]
        except KeyError:
            raise ComponentNotFound(f"Component {tp} not found.")
        _kwargs = {}
        for arg_name, arg in context.items():
            if hasattr(arg, "items"):
                # Recursion for nested dictionaries/constructors.
                if arg_name in component.arg_types:
                    arg_tp = str(get_type(component.arg_types[arg_name]))
                elif "type" in arg:
                    component_type = arg["type"]
                else:
                    raise TypeNotDefined(
                        f"Unable to determine type for {arg_name} in config object {tp}"
                    )
                _kwargs[arg_name] = self.build(arg_tp, arg)
            else:
                try:
                    arg_tp = component.arg_types[arg_name]
                except KeyError:
                    raise InvalidConfigKey(
                        f"Config key {arg_name} not in {component.arg_types.keys()}"
                    )
                _kwargs[arg_name] = arg_tp(arg)
        return component(**_kwargs)
