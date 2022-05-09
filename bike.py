import random

import numpy as np

from src.utils import config

class Bike():

    def __init__(self, start_street, char_horizontal_starting_pos, config=config.AppConfig()):

        self.config = config
        self.start_street = start_street
        self.horizontal_position = char_horizontal_starting_pos
        if not isinstance(self.horizontal_position, int):
            raise ValueError(f"self.horizontal_position is of type `{type(self.horizontal_position)}`")
        empty_spots = self.find_empty_spot_to_place_char()
        
        self.vertical_position = random.choice(
            empty_spots
        )

        self.graph_matrix = self.create_graph_matrix()

    def find_empty_spot_to_place_char(self):
        """"""
        sliced_matrix = np.matrix(self.start_street)[:, self.horizontal_position]
        flattened_slice = np.ravel(sliced_matrix)
        empty_spots = np.where(flattened_slice == 0)[0]

        return empty_spots

    def update_bike(self, last_key_pressed):

        if last_key_pressed == 115:
            self.move_up()
        elif last_key_pressed == 119:
            self.move_down()
        elif last_key_pressed == 100:
            self.move_right()
        elif last_key_pressed == 97:
            self.move_left()

    def move_left(self):

        if self.horizontal_position > 0:
            self.horizontal_position -= 1

    def move_right(self):
        if self.horizontal_position < (self.config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH -1 ):
            self.horizontal_position += 1

    def move_up(self):

        self.vertical_position += 1

    def move_down(self):

        self.vertical_position -= 1

    def create_graph_matrix(self):

        graph_matrix = np.zeros((
            self.config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH, 
            self.config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)
        )

        graph_matrix[self.vertical_position, self.horizontal_position] = 100

        return graph_matrix


if __name__ == "__main__":

    from environment import Street




    street = Street()
    print(np.matrix(street.graph_matrix))
    bike = Bike(start_street=street.graph_matrix, horizontal_padding=2)
    test = np.add(bike.graph_matrix, street.graph_matrix)

    print(bike.graph_matrix)
    

