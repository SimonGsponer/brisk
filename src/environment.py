
from time import sleep
import sys
import random

import numpy as np

# WORLD_WIDTH = 20
WORLD_LENGTH = 120
STREET_TURN_PROBA = 0.5

from src.utils import config
from src import engine
from src import ingame_settings

class Street:

    def __init__(self, engine: engine.Engine, config=config.AppConfig()):
        
        self.config = config
        self.engine = engine
        self.upper_boundary = 0
        self.lower_boundary = config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH - 1

        self.rightmost_upper_edge = config.game_config.INTERFACE_CONFIG._STREET_INIT_UPPER_EDGE
        self.rightmost_lower_edge = config.game_config.INTERFACE_CONFIG._STREET_INIT_LOWER_EDGE

        self.street_upper_edges = list()
        self.street_upper_edges.append(self.rightmost_upper_edge)
        self.street_lower_edges = list()
        self.street_lower_edges.append(self.rightmost_lower_edge)

        for i in range(config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH - 1):
            
            self.rightmost_upper_edge, self.rightmost_lower_edge = self.increment_street(
                upper_edge = self.rightmost_upper_edge,
                lower_edge = self.rightmost_lower_edge
            )

            self.street_upper_edges.insert(0, self.rightmost_upper_edge)  # .append(self.rightmost_upper_edge)
            self.street_lower_edges.insert(0, self.rightmost_lower_edge)  # .append(self.rightmost_lower_edge)

        self.graph_matrix = []
        for i in range(config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH):
            self.graph_matrix.append(
                [
                    1
                    if ((upper_edge >= i) or (lower_edge <= i))
                    else 0
                    for upper_edge, lower_edge 
                    in zip(self.street_upper_edges, self.street_lower_edges) 
                ]
            )


    def increment_street(self, upper_edge, lower_edge):
        
        street_turns = random.random() <= STREET_TURN_PROBA
        street_turns_up = random.choice([True, False])

        upper_edge_increment = upper_edge
        lower_edge_increment = lower_edge

        if street_turns and street_turns_up and not self.edge_on_upper_boundary:
            
            upper_edge_increment -= 1
            lower_edge_increment -= 1
        
        elif street_turns and not street_turns_up and not self.edge_on_lower_boundary:
            
            upper_edge_increment += 1
            lower_edge_increment += 1
        
        else:
            pass
        
        return upper_edge_increment, lower_edge_increment


    def update_street(self):

        for row in self.graph_matrix:

            _ = self.graph_matrix[row.pop(-1)]

        self.rightmost_upper_edge, self.rightmost_lower_edge = self.increment_street(
                upper_edge = self.rightmost_upper_edge,
                lower_edge = self.rightmost_lower_edge
            )

        for row in range(len(self.graph_matrix)):
            
            if (row <= self.rightmost_upper_edge) or (row >= self.rightmost_lower_edge):

                self.graph_matrix[row].insert(0, 1) #  .append(1)
            
            else:

                self.graph_matrix[row].insert(0, 0) #  .append(0)

        self.add_obstacles()
    
    def add_obstacles(self):
        
        n_obstacles = self.engine.get_n_obstacles_to_put_on_street()

        obstacles_on_upper_edge: int = self.engine.get_n_procs(
            proc_proba=0.5,
            n_max_procs=1
        )

        spots_for_obstacles = self.engine.find_empty_spots_in_matrix(
            graph_matrix=np.matrix(self.graph_matrix),
            col_index=0  # TODO: make dynamic when allowing for changing direction
        )

        if not obstacles_on_upper_edge:
            spots_for_obstacles = spots_for_obstacles[::-1]

        for i, row in enumerate(self.graph_matrix):
                
            if i in spots_for_obstacles[0:n_obstacles]:
                row[0] = 2

    @property
    def edge_on_upper_boundary(self):

        if self.rightmost_upper_edge == self.upper_boundary:
            return True
        else:
            return False

    @property
    def edge_on_lower_boundary(self):

        if self.rightmost_lower_edge == self.lower_boundary:
            return True
        else:
            return False

    @property
    def get_graph_matrix(self):

        return np.array(self.graph_matrix)

import curses
import time

def display_street(street, last_key_pressed):
    """progress: 0-10"""

    stdscr.addstr(0, 0, f"last key pressed: {last_key_pressed}")

    for i in range(len(street.graph_matrix)):
        
        this_str = "".join(["#" if item == 1 else "2" if item == 2 else " " for item in street.graph_matrix[i]])
        # print(this_str)
        # print("###")
        # print(f"{i}")
        stdscr.addstr(i+1, 0, this_str)
        

    # stdscr.addstr(0, 0, "Moving file: {0}".format(filename))
    # stdscr.addstr(1, 0, "Total progress: [{1:10}] {0}%".format(progress * 10, "#" * progress))
    stdscr.refresh()


if __name__ == "__main__":

    street = Street(engine=engine.Engine(char=ingame_settings.CharacterFactory().get_character(97)))

    stdscr = curses.initscr()
    stdscr.nodelay(1)
    curses.noecho()
    curses.cbreak()
    last_key_pressed = ""

    try:
        for i in range(40):
            display_street(street=street, last_key_pressed=last_key_pressed)
            street.update_street()
            last_key_pressed = stdscr.getch()
            time.sleep(0.05)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()