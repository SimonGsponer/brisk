import pytest

from src import game_interface


class TestInterface():

    def test_init(self) -> None:

        _ = game_interface.Interface()
