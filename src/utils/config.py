"""Defines classes handling game configuration."""

import configparser
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Type
import random
import uuid
import warnings

from src.utils import meta


@dataclass(frozen=True)
class InterfaceConfig:
    """Interface configuration dataclass storing all configurations as immutable.

    Attributes:
        MAIN_FRAME_WIDTH: Number of lines displayed in terminal for actual game.
        MAIN_FRAME_LENGTH: Number of characters displayed in terminal per line.
        ROAD_WIDTH: Width of road in which game character can move.
        MAX_OBSTACLE_RATIO: Maximum share of the road which can be occupied by obstacles
            at a given vertical position.
        TOTAL_FRAME_WIDTH: Total number of lines displayed for the game (hardcoded to +1
            to display game statistics on top).
        _STREET_INIT_UPPER_EDGE: Initial vertical position where upper part of road ends.
        _STREET_INIT_LOWER_EDGE: Initial vertical position where lower part of road ends.
    """
    MAIN_FRAME_WIDTH: int = 12  # pylint: disable=invalid-name
    MAIN_FRAME_LENGTH: int = 120  # pylint: disable=invalid-name
    ROAD_WIDTH: int = 8  # pylint: disable=invalid-name
    MAX_OBSTACLE_RATIO: float = 0.5  # pylint: disable=invalid-name
    TOTAL_FRAME_WIDTH: int = MAIN_FRAME_WIDTH + 1  # pylint: disable=invalid-name
    _STREET_INIT_UPPER_EDGE: Optional[int] = None  # pylint: disable=invalid-name
    _STREET_INIT_LOWER_EDGE: Optional[int] = None  # pylint: disable=invalid-name

    def __post_init__(self) -> None:
        """Defines attributes which can only be set after instantiation.

        This method makes sure that TOTAL_FRAME_WIDTH is adjusted if a custom value
        was passed to MAIN_FRAME_WIDTH lest the default value is used at instantiation.
        Moreover, if no custom value was provided for the private attributes (which
        should only happen for unit testing in the first place), the initial positions
        of the upper and lower edges are randomly generated.
        """
        object.__setattr__(self, 'TOTAL_FRAME_WIDTH',
                           self.MAIN_FRAME_WIDTH + 1)

        if not self._STREET_INIT_UPPER_EDGE:
            object.__setattr__(self, '_STREET_INIT_UPPER_EDGE',
                               self._init_upper_edge())

        if not self._STREET_INIT_LOWER_EDGE:
            object.__setattr__(self, '_STREET_INIT_LOWER_EDGE',
                               self._init_lower_edge())

    def _init_upper_edge(self) -> int:
        """Randomly generates the upper end of the road.

        A `-2` is applied to i) accomodate for python's 0 indexing and ii) assure the
        road in the game has its truthful width.
        """
        return random.randint(0, self.MAIN_FRAME_WIDTH - 2 - self.ROAD_WIDTH)

    def _init_lower_edge(self) -> int:
        """Generates the lower end of the road, given the random position of the upper end.

        Similar to _init_upper_edge(), a `+1` is applied to make sure the road has its
        truthful width.
        """
        if self._STREET_INIT_UPPER_EDGE is None:
            raise AttributeError(
                "_STREET_INIT_UPPER_EDGE have not been defined yet!")

        return self._STREET_INIT_UPPER_EDGE + self.ROAD_WIDTH + 1

    def _init_char_vertical_pos(self) -> int:
        """Generates the initial vertical position of game character based on road position.

        Deprecated: Left in code to showcase a scenario when the singleton pattern is essential.
        """
        warning_msg = "The method _init_char_vertical_pos is not actively used in the game anymore!"
        warnings.warn(warning_msg, DeprecationWarning)

        if not self._STREET_INIT_UPPER_EDGE or not self._STREET_INIT_LOWER_EDGE:
            raise AttributeError(
                "_STREET_INIT_LOWER_EDGE and _STREET_INIT_UPPER_EDGE have not been defined yet!"
            )

        random_vertical_pos = random.randint(self._STREET_INIT_UPPER_EDGE,
                                             self._STREET_INIT_LOWER_EDGE)

        return random_vertical_pos


@dataclass(frozen=True)
class GameConfigs:
    """Dataclass storing all game configurations.

    Attributes:
        INTERFACE_CONFIG: Interface configurations.
    """
    INTERFACE_CONFIG: InterfaceConfig  # pylint: disable=invalid-name


class AppConfig(metaclass=meta.SingletonMeta):
    """Main configuration class hanlding all configuration logic.

    The overarching purpose of this class is to provide a single source of truth for
    all configurations, regardless where and how they are accessed in the code. Its
    singleton pattern make sure the randomly generated configuration values are the
    same in the entire code. Moreover, the class explicitly defines which configurations
    can be overriden and customised.

    Attributes:
        config_parser: ConfigParser object containing custom configurations from .INI file.
        id_: Unique ID of configuration object.
        game_config: GameConfig dataclass storing all game configurations.

    Args:
        config_fp: Filepath pointing to .INI file containing custom configs. Defaults to pre-defined
            file location.
    """

    def __init__(
        self,
        config_fp: Optional[Path] = Path("config").joinpath("game_config.ini")
    ) -> None:
        """Class instantiation."""
        self.config_parser = configparser.ConfigParser()
        if config_fp:
            with open(config_fp, encoding='utf-8') as ini_file:
                self.config_parser.read_file(ini_file)
        else:
            pass

        self.id_ = uuid.uuid4()

        self.game_config = GameConfigs(
            INTERFACE_CONFIG=self._populate_interface_configs())

    def _populate_interface_configs(self) -> InterfaceConfig:
        """Populates interface configs with allowed custom configurations.

        Returns:
            Instantiated InterfaceConfig dataclass containing final config values.
        """
        ud_main_frame_width = self.config_parser.get('INTERFACE',
                                                     'MAIN_FRAME_WIDTH',
                                                     fallback=None)
        ud_main_frame_length = self.config_parser.get('INTERFACE',
                                                      'MAIN_FRAME_LENGTH',
                                                      fallback=None)
        ud_road_width = self.config_parser.get('INTERFACE',
                                               'ROAD_WIDTH',
                                               fallback=None)

        ud_interface_configs = dict(
            MAIN_FRAME_WIDTH=int(ud_main_frame_width)
            if ud_main_frame_width else None,
            MAIN_FRAME_LENGTH=int(ud_main_frame_length)
            if ud_main_frame_length else None,
            ROAD_WIDTH=int(ud_road_width) if ud_road_width else None)

        return InterfaceConfig(
            **{key: val
               for (key, val) in ud_interface_configs.items() if val})
