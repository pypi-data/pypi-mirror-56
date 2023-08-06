import sys
from typing import Any, TypeVar, Type


config_inst_t = TypeVar('config_inst_t', bound='config.config.Config')


def export(fn: callable) -> callable:
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        mod.__all__.append(fn.__name__)
    else:
        mod.__all__ = [fn.__name__]
    return fn


def set_config(
    config_inst: Type[config_inst_t],
    key: str,
    default: str = None,
    cast: Any = None,
) -> None:
    """Sets the config variable on the instance of a class.

    Parameters
    ----------
    config_inst : Type[config_inst_t]
        Instance of the config class.
    key : str
        The key referencing the config variable.
    default : str, optional
        The default value.
    cast : Any, optional
        The type of the variable.
    """
    config_var = key.lower().replace('.', '_')
    setattr(config_inst, config_var, config_inst.get(key, default, cast))
