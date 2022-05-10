"""This file contains fixtures used in unittesting.

For more information about the concept of fixtures, please see: https://docs.pytest.org/en/6.2.x/fixture.html.

"""
import pytest

from src.utils import config
from src import ingame_settings

@pytest.fixture
def default_configs() -> config.AppConfig:
    """Provides default configurations.
    
    Since the configuration class represents a singleton, any previously instantiation
    would override a new instantiation of the fixture. Therefore, all singleton instances
    are cleared prior to instantiating a configuration object with the default params.
    """
    config.AppConfig.clear_instance()
    default_configs = config.AppConfig(config_fp=None)

    return default_configs


@pytest.fixture
def any_character() -> ingame_settings.Character:

    character_factory = ingame_settings.CharacterFactory()

    return character_factory.get_random_character()
