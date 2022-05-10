"""
TODO:

Add singleton config

AppConfig -> Singleton
"""

import configparser
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Type
import random
import uuid

from src.utils import meta


@dataclass(frozen=True)
class InterfaceConfig:
    MAIN_FRAME_WIDTH: int = 12
    MAIN_FRAME_LENGTH: int = 120
    ROAD_WIDTH: int = 8
    MAX_OBSTACLE_RATIO: float = 0.5
    TOTAL_FRAME_WIDTH: int = MAIN_FRAME_WIDTH + 1
    _STREET_INIT_UPPER_EDGE: Optional[int] = None
    _STREET_INIT_LOWER_EDGE: Optional[int] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, 'TOTAL_FRAME_WIDTH',
                           self.MAIN_FRAME_WIDTH + 1)

        if not self._STREET_INIT_UPPER_EDGE:
            object.__setattr__(self, '_STREET_INIT_UPPER_EDGE',
                               self._init_upper_edge())

        if not self._STREET_INIT_LOWER_EDGE:
            object.__setattr__(self, '_STREET_INIT_LOWER_EDGE',
                               self._init_lower_edge())

    def _init_upper_edge(self) -> int:

        return random.randint(0, self.MAIN_FRAME_WIDTH - 2 - self.ROAD_WIDTH)

    def _init_lower_edge(self) -> int:

        return self._STREET_INIT_UPPER_EDGE + self.ROAD_WIDTH + 1

    def _init_char_vertical_pos(self) -> int:

        return random.randint(self._STREET_INIT_UPPER_EDGE,
                              self._STREET_INIT_LOWER_EDGE)


@dataclass(frozen=True)
class GameConfigs:
    INTERFACE_CONFIG: Type[InterfaceConfig] = InterfaceConfig


class AppConfig(metaclass=meta.SingletonMeta):

    def __init__(self, config_fp: Optional[Path] = Path("config").joinpath("game_config.ini")) -> None:

        self.config_parser = configparser.ConfigParser()
        if config_fp:
            self.config_parser.read_file(open(config_fp))
        else:
            pass

        self.random_var = random.randint(1, 10)
        self.id_ = uuid.uuid4()

        self.game_config = GameConfigs(
            INTERFACE_CONFIG=self._populate_interface_configs())

    def _populate_interface_configs(self) -> InterfaceConfig:

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

    def _validate_configs(self) -> None:

        if int(
                self.config_parser.get(
                    'INTERFACE', 'MAIN_FRAME_WIDTH', fallback=None)) < 10:
            raise ValueError("MAIN_FRAME_WIDTH must be at least 10.")
