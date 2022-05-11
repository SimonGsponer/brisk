# pylint: disable=no-self-use
"""Contains all unittests for objects defined in src.game_interface."""
from src import game_interface


class TestInterface():
    """Test interface class."""

    def test_init(self) -> None:
        """Test instantiation."""
        _ = game_interface.Interface()
