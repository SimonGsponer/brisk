"""
https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage

TODO:
* Dockerfile
* relative position characters (padding)
"""

from src.utils import config

app_config = config.AppConfig()

from src.environment import Street
from src.character_controller import CharacterController
from src.engine import Engine
from src import game_interface
from src import stats
from src import ingame_settings

import curses
import time

import numpy as np


def display(str_frame):

    for i, str_row in enumerate(str_frame):

        stdscr.addstr(i, 0, str_row.encode('UTF-8'))

    stdscr.refresh()


if __name__ == "__main__":

    game_over = False
    playing = True
    pressed_key = False
    character_chosen = False

    interface = game_interface.Interface()

    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()

    try:
        while not pressed_key:

            display(str_frame=interface.generate_lobby_landing_page())
            stdscr.nodelay(0)
            last_key_pressed = stdscr.getch()

            if last_key_pressed == 27:
                pressed_key = True
                character_chosen = True
                playing = False
            else:
                pressed_key = True

        while not character_chosen:

            display(
                str_frame=interface.generate_lobby_character_selection_page())
            stdscr.nodelay(0)
            last_key_pressed = stdscr.getch()

            if last_key_pressed == 27:
                character_chosen = True
                playing = False
            elif last_key_pressed in (97, 98, 99):

                main_character = ingame_settings.CharacterFactory(
                ).get_character(key_input=last_key_pressed)

                character_chosen = True

        while playing:

            engine = Engine(char=main_character)
            street = Street(engine=engine)
            bike = CharacterController(start_street=street.graph_matrix,
                                       char_horizontal_starting_pos=engine.
                                       char_horizontal_starting_pos)
            engine.start_game()
            score = stats.Score(
                main_char_score_multiplier=main_character.speed_multiplier)

            while not game_over:
                if score.last_ts:
                    score.increment_score()
                    street.update_street()
                    bike.update_bike(last_key_pressed)
                stdscr.nodelay(1)

                engine_graph_matrix = engine.generate_graph_matrix(
                    bike_graph_matrix=bike.create_graph_matrix(),
                    env_graph_matrix=street.get_graph_matrix)

                str_frame = engine.generate_interface_str_frame(
                    graph_matrix=engine_graph_matrix,
                    current_score=score.get_current_score,
                    main_character=main_character)
                display(str_frame=str_frame)
                if not score.last_ts:
                    score.start_scoring()
                    time.sleep(1.5)

                last_key_pressed = stdscr.getch()

                if (101 in engine_graph_matrix) or (102
                                                    in engine_graph_matrix):
                    game_over = True

                time.sleep(engine.get_frame_rate)

            while game_over:
                display(str_frame=interface.generate_game_over_page(
                    final_score=score.get_current_score))
                stdscr.nodelay(0)
                last_key_pressed = stdscr.getch()
                time.sleep(1)

                if last_key_pressed == 27:
                    game_over = False
                    playing = False
                else:
                    playing = True
                    game_over = False

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
