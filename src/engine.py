import curses
import time
import sys
from pathlib import Path
import random

import numpy as np

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent.parent))

from src.utils import config
from src import ingame_settings

app_config = config.AppConfig()

class Engine():

    base_frame_rate: int = 10

    def __init__(self, char: ingame_settings.Character, app_config: config.AppConfig = app_config):

        self.app_config: config.AppConfig = app_config
        self.graph_matrix = self.create_graph_matrix()
        self.char: ingame_settings.Character = char
        self.start_ts = None

    def start_game(self):

        self.start_ts = time.time()

    @property
    def get_frame_rate(self):

        char_increase = self.base_frame_rate * self.char.speed_multiplier
        time_incease = char_increase * self.get_time_frame_rate_increase

        return  1 / time_incease

    @property
    def get_time_frame_rate_increase(self):

        current_ts = time.time()

        time_elapsed = current_ts - self.start_ts
        time_elapsed = max([20, time_elapsed])

        return time_elapsed / 20

    @property
    def char_horizontal_starting_pos(self):
        
        horizontal_starting_pos = int(
            self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH
            - round(
                self.char.rel_horizontal_pos
                * self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH,
                0
            )
        )

        return horizontal_starting_pos

    def create_graph_matrix(self):
        width = self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH
        length = self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH
        
        graph_matrix: np.NDarray = np.zeros(
            (width, length), dtype=np.int64
        )

        return graph_matrix

    def get_n_obstacles_to_put_on_street(self):

        max_obstacles = round(
                (
                    self.app_config.game_config.INTERFACE_CONFIG.ROAD_WIDTH
                    * self.app_config.game_config.INTERFACE_CONFIG.MAX_OBSTACLE_RATIO
                ),
                0
            )

        n_obstacles = Engine.get_n_procs(
            proc_proba=self.char.obstacle.proc_rate,
            n_max_procs=int(max_obstacles)
        )

        return n_obstacles

    @classmethod
    def find_empty_spots_in_matrix(cls, graph_matrix, col_index):

        sliced_matrix = graph_matrix[:, col_index]
        flattened_slice = np.ravel(sliced_matrix)
        empty_spots = np.where(flattened_slice == 0)[0]

        return empty_spots 

    @classmethod
    def get_n_procs(cls, proc_proba, n_max_procs):
        
        threshold_procs = [(proc_proba)**(i+1) for i in range(n_max_procs)]
        effective_probas = [np.prod([random.random()**(i+1)]) for i in range(n_max_procs)]

        n_procs = cls.count_procs(threshold_procs, effective_probas)

        return n_procs

    @classmethod
    def count_procs(cls, threshold_probas, effective_probas):
        
        proc_list = [1 if proba < threshold_proba else 0 for threshold_proba, proba in zip(threshold_probas, effective_probas)]

        n_procs = sum(proc_list)

        return n_procs

    def generate_graph_matrix(self, bike_graph_matrix, env_graph_matrix):
        
        layered_matrix = np.add(env_graph_matrix, bike_graph_matrix)

        return layered_matrix

    def generate_interface_str_frame(self, graph_matrix, current_score, main_character):
        
        str_frame = list()

        current_score_label = "CURRENT SCORE: "
        current_score_str = f"{current_score:,}"

        ljust_score_label = self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH
        current_score = f"{current_score_label}{current_score_str}".ljust(ljust_score_label, ' ')
        str_frame.append(current_score)

        main_str_frame = Engine.convert_graph_matrix(
            graph_matrix=graph_matrix,
            obstacle_emoji=self.char.obstacle.obstacle_emoji,
            main_char_emoji=main_character.emoji
        )

        str_frame.extend(main_str_frame)

        return str_frame

    @classmethod
    def convert_graph_matrix(cls, graph_matrix, obstacle_emoji, main_char_emoji):
        
        str_frame = list()
        for row in graph_matrix:
            str_row = "".join([
                "#" if item == 1
                else f"{obstacle_emoji}" if item == 2
                else f"{main_char_emoji}" if item == 100 
                else " " if item == 0 else "🔥"
                for item in row.tolist()])
            
            str_frame.append(str_row)
        
        return str_frame


    @classmethod
    def display_str_frame(cls, str_frame):
        stdscr = curses.initscr()
        stdscr.keypad(True)
        stdscr.nodelay(1)
        curses.noecho()
        curses.cbreak()

        for i, str_row in enumerate(str_frame):

            stdscr.addstr(i, 0, str_row)

        stdscr.refresh()
        time.sleep(10)

        curses.echo()
        curses.nocbreak()
        curses.endwin()


if __name__ == "__main__":

    engine = Engine(main_char_speed=1)

    # str_frame = engine.generate_interface_str_frame(graph_matrix=[], current_score=0)
    # print(len(str_frame[0]))
    # engine.display_str_frame(str_frame=str_frame)

    engine.start_game()

    print(engine.get_time_frame_rate_increase)
    print(engine.get_frame_rate)
