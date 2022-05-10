import pytest

from src.utils import config


@pytest.fixture
def default_configs():
    """Provides default configurations.
    
    Since the configuration class represents a singleton, any previously instantiation
    would override a new instantiation of the fixture. Therefore, all singleton instances
    are cleared prior to instantiating a configuration object with the default params.
    """
    config.AppConfig.clear_instance()
    default_configs = config.AppConfig(config_fp=None)

    return default_configs
