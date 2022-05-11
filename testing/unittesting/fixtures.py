"""This file contains fixtures used in unittesting.

For more information about the concept of fixtures, please see:
https://docs.pytest.org/en/6.2.x/fixture.html.

"""
import pytest
import numpy as np

from src.utils import config
from src import ingame_settings
from src.engine import GraphMatrixType


@pytest.fixture
def default_configs() -> config.AppConfig:
    """Provides default configurations.

    Since the configuration class represents a singleton, any previously instantiation
    would override a new instantiation of the fixture. Therefore, all singleton instances
    are cleared prior to instantiating a configuration object with the default params.

    Returns:
        Configurations with default values.
    """
    config.AppConfig.clear_instance()
    default_configs_ = config.AppConfig(config_fp=None)

    return default_configs_


@pytest.fixture
def any_character() -> ingame_settings.Character:
    """Returns a random character of the pre-defined list of available characters.

    Returns:
        Randomly selected character available to player.
    """
    character_factory = ingame_settings.CharacterFactory()

    return character_factory.get_random_character()


@pytest.fixture
def example_road_graph_matrix() -> GraphMatrixType:

    list_matrix = [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
    ]
    matrix: GraphMatrixType = np.array(list_matrix, dtype=np.int64)

    return matrix
