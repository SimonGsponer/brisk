import curses
import time
import random
from typing import List, TypeVar, Type, Optional

import numpy as np
import numpy.typing as npt

from src.utils import config
from src import ingame_settings

app_config = config.AppConfig()

TE = TypeVar('TE', bound='Engine')
GraphMatrixType = npt.NDArray[np.int64]
OneDArray = npt.NDArray[np.int64]


class Engine():

    base_frame_rate: int = 10

    def __init__(self,
                 char: ingame_settings.Character,
                 app_config: config.AppConfig = app_config) -> None:

        self.app_config: config.AppConfig = app_config
        self.graph_matrix = self.create_graph_matrix()
        self.char: ingame_settings.Character = char
        self.start_ts: Optional[float] = None

    def start_game(self) -> None:

        self.start_ts = time.time()

    @property
    def get_frame_rate(self) -> float:

        char_increase = self.base_frame_rate * self.char.speed_multiplier
        time_incease = char_increase * self.get_time_frame_rate_increase

        return 1 / time_incease

    @property
    def get_time_frame_rate_increase(self) -> float:

        current_ts = time.time()

        if not self.start_ts:
            raise AttributeError("Method start_game has not been called yet!")

        time_elapsed = current_ts - self.start_ts
        time_elapsed = max([20, time_elapsed])
        time_elapsed = time_elapsed / 20

        return time_elapsed

    @property
    def char_horizontal_starting_pos(self) -> int:

        horizontal_starting_pos = int(
            self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH -
            round(
                self.char.rel_horizontal_pos *
                self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH,
                0))

        return horizontal_starting_pos

    def create_graph_matrix(self) -> GraphMatrixType:
        width = self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH
        length = self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH

        graph_matrix: GraphMatrixType = np.zeros((width, length),
                                                 dtype=np.int64)

        return graph_matrix

    def get_n_obstacles_to_put_on_street(self) -> int:

        max_obstacles = round(
            (self.app_config.game_config.INTERFACE_CONFIG.ROAD_WIDTH *
             self.app_config.game_config.INTERFACE_CONFIG.MAX_OBSTACLE_RATIO),
            0)

        n_obstacles = Engine.get_n_procs(
            proc_proba=self.char.obstacle.proc_rate,
            n_max_procs=int(max_obstacles))

        return n_obstacles

    @classmethod
    def find_empty_spots_in_matrix(cls: Type[TE],
                                   graph_matrix: GraphMatrixType,
                                   col_index: int) -> GraphMatrixType:

        sliced_matrix = graph_matrix[:, col_index]
        flattened_slice = np.ravel(sliced_matrix)
        empty_spots = np.where(flattened_slice == 0)[0]

        return empty_spots

    @classmethod
    def get_n_procs(cls: Type[TE], proc_proba: float, n_max_procs: int) -> int:

        threshold_procs = [(proc_proba)**(i + 1) for i in range(n_max_procs)]
        effective_probas = [
            np.prod([random.random()**(i + 1)]) for i in range(n_max_procs)
        ]

        n_procs = cls.count_procs(threshold_procs, effective_probas)

        return n_procs

    @classmethod
    def count_procs(cls: Type[TE], threshold_probas: List[float],
                    effective_probas: List[float]) -> int:

        proc_list = [
            1 if proba < threshold_proba else 0 for threshold_proba, proba in
            zip(threshold_probas, effective_probas)
        ]

        n_procs = sum(proc_list)

        return n_procs

    def generate_graph_matrix(
            self, bike_graph_matrix: GraphMatrixType,
            env_graph_matrix: GraphMatrixType) -> GraphMatrixType:

        layered_matrix: GraphMatrixType = np.add(env_graph_matrix,
                                                 bike_graph_matrix)

        return layered_matrix

    def generate_interface_str_frame(
            self, graph_matrix: GraphMatrixType, current_score: int,
            main_character: ingame_settings.Character) -> List[str]:

        str_frame = list()

        current_score_label = "CURRENT SCORE: "
        current_score_str = f"{current_score:,}"

        ljust_score_label = self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH
        current_score_str = f"{current_score_label}{current_score_str}".ljust(
            ljust_score_label, ' ')
        str_frame.append(current_score_str)

        main_str_frame = Engine.convert_graph_matrix(
            graph_matrix=graph_matrix,
            obstacle_emoji=self.char.obstacle.obstacle_emoji,
            main_char_emoji=main_character.emoji)

        str_frame.extend(main_str_frame)

        return str_frame

    @classmethod
    def convert_graph_matrix(cls: Type[TE], graph_matrix: GraphMatrixType,
                             obstacle_emoji: str,
                             main_char_emoji: str) -> List[str]:
        """Translates the numerical graph matrix into its string representation for game display.

        Since the graph matrix only consist of a pre-defined set of numbers, each number is mapped
        to a string in this function, where every row of the matrix forms one single string to be
        displayed in the terminal as a line.

        Args:
            graph_matrix: Final graph matrix to be displayed on screen; represents a combination of the
                environment graph matrix and the character graph matrix.
            obstacle_emoji: Specific character to be used to display an obstacle on the screen.
            main_char_emoji: Emoji representing character of the player.

        Returns:
            str_frame: List of strings representing a single line to be displayed on the user's terminal for
                a given frame.
        """
        str_frame = list()
        for row in graph_matrix:
            str_row = "".join([
                "#" if item == 1 else
                f"{obstacle_emoji}" if item == 2 else f"{main_char_emoji}"
                if item == 100 else " " if item == 0 else "🔥"
                for item in row.tolist()
            ])

            str_frame.append(str_row)

        return str_frame
