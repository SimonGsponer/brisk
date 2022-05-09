import unittest

from src.utils import config

class InterfaceConfigTestCase(unittest.TestCase):

    def test_init(self):
        
        interface_config = config.InterfaceConfig()

    def test_init_custom_attrs(self):
        
        interface_config = config.InterfaceConfig(
            MAIN_FRAME_LENGTH=100
        )
    
    def test_init_custom_attrs_2(self):
        
        interface_config = config.InterfaceConfig(
            MAIN_FRAME_WIDTH=100
        )

        assert interface_config.TOTAL_FRAME_WIDTH == 101

    def test_init_custom_street_init(self):
        """Statically instantiate road edges."""
        interface_config = config.InterfaceConfig(
            ROAD_WIDTH=4,
            _STREET_INIT_UPPER_EDGE=1
        )

        assert interface_config._STREET_INIT_UPPER_EDGE == 1
        assert interface_config._STREET_INIT_LOWER_EDGE == 6

    def test_init_custom_street_init2(self):
        """Manually setting both edges should ignore road width."""
        interface_config = config.InterfaceConfig(
            ROAD_WIDTH=4,
            _STREET_INIT_UPPER_EDGE=1,
            _STREET_INIT_LOWER_EDGE=1
        )

        assert interface_config._STREET_INIT_UPPER_EDGE == 1
        assert interface_config._STREET_INIT_LOWER_EDGE == 1


    def test_random_init_streed_edges(self):
        """Inclusive counting makes frame width == road width."""
        interface_config = config.InterfaceConfig(
            MAIN_FRAME_WIDTH=6,
            ROAD_WIDTH=4
        )

        assert interface_config._STREET_INIT_UPPER_EDGE == 0
        assert interface_config._STREET_INIT_LOWER_EDGE == 5


class TestAppConfig():

    def test_init(self):
        
        _ = config.AppConfig()

    def test_init_no_config_fp(self):

        config.AppConfig.clear_instance()
        app_config = config.AppConfig(config_fp=None)

        assert app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH == 12
        assert app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH == 120
        assert app_config.game_config.INTERFACE_CONFIG.ROAD_WIDTH == 8

    def test_singleton_id(self):

        app_config_1 = config.AppConfig()

        app_config_2 = config.AppConfig()

        assert id(app_config_1) == id(app_config_2)

    def test_singleton_random_inits(self):

        app_config_1 = config.AppConfig()

        app_config_2 = config.AppConfig()

        assert app_config_1.random_var == app_config_2.random_var
        assert app_config_1.id_ == app_config_2.id_

if __name__ == '__main__':
    unittest.main()
