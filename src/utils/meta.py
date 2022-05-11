"""Contains definitions of metaclasses."""

from weakref import WeakValueDictionary, ReferenceType
from typing import TypeVar, Generic, Type, ClassVar, Dict

from typing_extensions import ParamSpec


class SingletonMeta(type):
    """Singleton meta class.

    For more information about the Singleton desing pattern, please see:
    https://refactoring.guru/design-patterns/singleton.

    Attributes:
        _instances: Stores instantiated class object; if the singleton
            class is instantiated a second time, the first instantiation
            will be returned, even if configs differ.
    """

    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        """Makes sure class only instantiates a new object if none exists yet.

        Args:
            *args: Variable length argument list passed at instantiation.
            **kwargs: Arbitrary keyword arguments passed at instantiation.

        Returns:
            Class instance.
        """
        if cls not in cls._instances:
            instance: T = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @classmethod
    def clear_instance(cls) -> None:
        """For unittesting purposes: resets the state of the Singleton."""
        del cls._instances
        cls._instances = WeakValueDictionary()
