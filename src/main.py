"""
https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage

TODO:
* Dockerfile
* relative position characters (padding)
"""
import curses
import time

from src.environment import Street
from src.character_controller import CharacterController
from src.engine import Engine
from src import game_interface
from src import stats
from src import ingame_settings


def display(str_frame):

    for i, str_row in enumerate(str_frame):

        stdscr.addstr(i, 0, str_row.encode('UTF-8'))

    stdscr.refresh()


if __name__ == "__main__":

    GAME_OVER = False
    PLAYING = True
    PRESSED_KEY = False
    CHARACTER_CHOSEN = False

    interface = game_interface.Interface()

    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()

    try:
        while not PRESSED_KEY:

            display(str_frame=interface.generate_lobby_landing_page())
            stdscr.nodelay(0)
            last_key_pressed = stdscr.getch()

            if last_key_pressed == 27:
                PRESSED_KEY = True
                CHARACTER_CHOSEN = True
                PLAYING = False
            else:
                PRESSED_KEY = True

        while not CHARACTER_CHOSEN:

            display(
                str_frame=interface.generate_lobby_character_selection_page())
            stdscr.nodelay(0)
            last_key_pressed = stdscr.getch()

            if last_key_pressed == 27:
                CHARACTER_CHOSEN = True
                PLAYING = False
            elif last_key_pressed in (97, 98, 99):

                main_character = ingame_settings.CharacterFactory(
                ).get_character(key_input=last_key_pressed)

                CHARACTER_CHOSEN = True

        while PLAYING:

            engine = Engine(char=main_character)
            street = Street(engine=engine)
            char_controller = CharacterController(
                start_street=street.get_graph_matrix,
                char_horizontal_starting_pos=engine.
                char_horizontal_starting_pos)
            engine.start_game()
            score = stats.Score(
                main_char_score_multiplier=main_character.speed_multiplier)

            while not GAME_OVER:
                if score.last_ts:
                    score.increment_score()
                    street.update_street()
                    char_controller.update_bike(last_key_pressed)
                stdscr.nodelay(1)

                engine_graph_matrix = engine.generate_graph_matrix(
                    bike_graph_matrix=char_controller.create_graph_matrix(),
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
                    GAME_OVER = True

                time.sleep(engine.get_frame_rate)

            while GAME_OVER:
                display(str_frame=interface.generate_game_over_page(
                    final_score=score.get_current_score))
                stdscr.nodelay(0)
                last_key_pressed = stdscr.getch()
                time.sleep(1)

                if last_key_pressed == 27:
                    GAME_OVER = False
                    PLAYING = False
                else:
                    PLAYING = True
                    GAME_OVER = False

    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
