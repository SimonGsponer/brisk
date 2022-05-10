import pytest

from src.utils import config


@pytest.fixture
def default_configs():

    config.AppConfig.clear_instance()
    default_configs = config.AppConfig(config_fp=None)

    return default_configs
