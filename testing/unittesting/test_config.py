# pylint: disable=no-self-use, protected-access
"""Contains all unittests for objects defined in src.utils.config"""

from src.utils import config


class TestInterfaceConfig():
    """Tests InterfaceConfig class."""

    def test_init(self) -> None:
        """Test instantiation with default params."""
        _ = config.InterfaceConfig()

    def test_init_custom_attrs(self) -> None:
        """Test instantiation with custom params."""
        _ = config.InterfaceConfig(MAIN_FRAME_LENGTH=100)

    def test_init_custom_attrs_2(self) -> None:
        """Test instantiation with custom params II."""
        interface_config = config.InterfaceConfig(MAIN_FRAME_WIDTH=100)

        assert interface_config.TOTAL_FRAME_WIDTH == 101

    def test_init_custom_street_init(self) -> None:
        """Statically instantiate road edges."""
        interface_config = config.InterfaceConfig(ROAD_WIDTH=4,
                                                  _STREET_INIT_UPPER_EDGE=1)

        assert interface_config._STREET_INIT_UPPER_EDGE == 1
        assert interface_config._STREET_INIT_LOWER_EDGE == 6

    def test_init_custom_street_init2(self) -> None:
        """Manually setting both edges should ignore road width."""
        interface_config = config.InterfaceConfig(ROAD_WIDTH=4,
                                                  _STREET_INIT_UPPER_EDGE=1,
                                                  _STREET_INIT_LOWER_EDGE=1)

        assert interface_config._STREET_INIT_UPPER_EDGE == 1
        assert interface_config._STREET_INIT_LOWER_EDGE == 1

    def test_random_init_street_edges(self) -> None:
        """Inclusive counting makes frame width == road width."""
        interface_config = config.InterfaceConfig(MAIN_FRAME_WIDTH=6,
                                                  ROAD_WIDTH=4)

        assert interface_config._STREET_INIT_UPPER_EDGE == 0
        assert interface_config._STREET_INIT_LOWER_EDGE == 5


class TestAppConfig():
    """Test AppConfig class."""

    def test_init(self) -> None:
        """Test instantiation."""
        _ = config.AppConfig()

    def test_init_no_config_fp(self) -> None:
        """Test instantiation with config filepath set to None."""
        config.AppConfig.clear_instance()
        app_config = config.AppConfig(config_fp=None)

        assert app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH == 12
        assert app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH == 120
        assert app_config.game_config.INTERFACE_CONFIG.ROAD_WIDTH == 8

    def test_singleton_id(self) -> None:
        """Test singleton behaviour."""
        app_config_1 = config.AppConfig()

        app_config_2 = config.AppConfig()

        assert id(app_config_1) == id(app_config_2)

    def test_singleton_random_inits(self) -> None:
        """Assure singleton returns same random instance attributes."""
        app_config_1 = config.AppConfig()

        app_config_2 = config.AppConfig()

        assert app_config_1.id_ == app_config_2.id_
