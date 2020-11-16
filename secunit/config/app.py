from logging import INFO, Formatter, StreamHandler, getLogger
from sys import stderr
from typing import Callable, Dict, Text, Tuple

from secunit.config.component import Component
from secunit.config.exc import (ComponentNotFound, InvalidConfigKey,
                                KeyNotInConfig, TypeNotDefined)


def mk_logger(name, level):
    logger = getLogger(name)
    logger.setLevel(level)
    sh = StreamHandler(stderr)
    sh.setLevel(level)
    logger.addHandler(sh)
    fmt = Formatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s")
    sh.setFormatter(fmt)
    return logger


def get_type(f: Callable):
    return f.__name__


class App:
    def __init__(self, logger=None):
        self._constructors: Dict[Text, Component] = {}
        self.logger = logger if logger is not None else mk_logger(str(self), INFO)
        self.logger.debug("Created App.")

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

    def build(self, tp: Text, context: Dict):
        self.logger.debug(f"Building type {tp} from {context}")
        try:
            constructor: Component = self.constructors[tp]
        except KeyError:
            raise ComponentNotFound(f"Component {tp} not found.")
        _kwargs = {}
        for arg_name, arg in context.items():
            if hasattr(arg, "items"):
                if arg_name in constructor.arg_types:
                    arg_tp = str(get_type(constructor.arg_types[arg_name]))
                elif "type" in arg:
                    arg_tp = str(arg.pop("type"))
                else:
                    raise TypeNotDefined(
                        f"Unable to determine type for {arg_name} in {tp}"
                    )
                _kwargs[arg_name] = self.build(arg_tp, arg)
            else:
                try:
                    arg_tp = constructor.arg_types[arg_name]
                except KeyError:
                    raise InvalidConfigKey(
                        f"Config key {arg_name} not in {constructor.arg_types.values()}"
                    )
                _kwargs[arg_name] = arg_tp(arg)
        return constructor.callback(**_kwargs)
