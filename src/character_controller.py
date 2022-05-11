import random

import numpy as np

from src.utils import config
from src.engine import GraphMatrixType, OneDArray


class CharacterController():

    def __init__(
        self,
        start_street: GraphMatrixType,
        char_horizontal_starting_pos: int,
        app_config: config.AppConfig = config.AppConfig()
    ) -> None:

        self.config = app_config
        self.start_street = start_street
        self.horizontal_position = char_horizontal_starting_pos
        if not isinstance(self.horizontal_position, int):
            raise ValueError(
                f"self.horizontal_position is of type `{type(self.horizontal_position)}`"
            )
        empty_spots = self.find_empty_spot_to_place_char()

        self.vertical_position = random.choice(empty_spots)

        self.graph_matrix = self.create_graph_matrix()

    def find_empty_spot_to_place_char(self) -> OneDArray:
        """"""
        sliced_matrix = self.start_street[:, self.horizontal_position]
        flattened_slice = np.ravel(sliced_matrix)
        empty_spots: OneDArray = np.where(flattened_slice == 0)[0]

        return empty_spots

    def update_bike(self, last_key_pressed: int) -> None:

        if last_key_pressed == 115:
            self.move_up()
        elif last_key_pressed == 119:
            self.move_down()
        elif last_key_pressed == 100:
            self.move_right()
        elif last_key_pressed == 97:
            self.move_left()

    def move_left(self) -> None:

        if self.horizontal_position > 0:
            self.horizontal_position -= 1

    def move_right(self) -> None:
        if self.horizontal_position < (
                self.config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH -
                1):
            self.horizontal_position += 1

    def move_up(self) -> None:

        self.vertical_position += 1

    def move_down(self) -> None:

        self.vertical_position -= 1

    def create_graph_matrix(self) -> GraphMatrixType:

        graph_matrix: GraphMatrixType = np.zeros(
            (self.config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH,
             self.config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH),
            dtype=np.int64)

        graph_matrix[self.vertical_position, self.horizontal_position] = 100

        return graph_matrix
