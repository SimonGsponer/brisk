import unittest

from src import game_interface


class InterfaceTestCase(unittest.TestCase):

    def test_init(self):

        interface = game_interface.Interface()

    # def test_width_size_odd(self):

    #     interface_config = game_interface.Interface()

    #     assert not interface_config.main_width_size_odd

    # def test_length_size_odd(self):

    #     interface_config = game_interface.Interface()

    #     assert not interface_config.main_length_size_odd
