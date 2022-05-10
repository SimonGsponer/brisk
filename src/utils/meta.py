"""Contains definitions of metaclasses."""

from weakref import WeakValueDictionary
from typing import TypeVar, Generic

from typing_extensions import ParamSpec


P = ParamSpec('P')
T = TypeVar('T')
SingletonType = Generic[T, P]


class SingletonMeta(type):
    """Singleton meta class.

    For more information about the Singleton desing pattern, please see:
    https://refactoring.guru/design-patterns/singleton.

    Attributes:
        _instances: Stores instantiated class object; if the singleton
            class is instantiated a second time, the first instantiation
            will be returned, even if configs differ.
    """

    _instances: WeakValueDictionary = WeakValueDictionary()

    def __call__(cls: SingletonType, *args: P.args, **kwargs: P.kwargs) -> SingletonType:
        """Makes sure class only instantiates a new object if none exists yet.
        
        Args:
            *args: Variable length argument list passed at instantiation.
            **kwargs: Arbitrary keyword arguments passed at instantiation.
        
        Returns:
            Class instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @classmethod
    def clear_instance(cls) -> None:
        """For unittesting purposes: resets the state of the Singleton."""
        del cls._instances
        cls._instances = WeakValueDictionary()
