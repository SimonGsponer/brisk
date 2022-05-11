"""

Game Phases
* lobby
    * press any key to continue; press esc to exit.
    * select character
    * countdown
* game
* game_over
    * press any key to restart; press esc to exit.
"""
import time
import curses
from typing import List, Tuple, TypeVar, Type

from src.utils import config
from src import ingame_settings

app_config = config.AppConfig()

InterfaceType = TypeVar('InterfaceType', bound='Interface')


class Interface():

    app_config = app_config

    def __init__(self) -> None:

        pass

    def generate_lobby_landing_page(self) -> List[str]:

        str_frame = []

        screen_messages = [
            " HELLO! PRESS ANY ", " KEY TO START OR ESC TO EXIT. "
        ]

        n_upper_fillrows, n_lower_fillrows = self.get_fillrows(
            screen_messages=screen_messages)

        for _ in range(n_upper_fillrows):
            str_frame.append(
                "=" *
                self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        for message in screen_messages:

            len_rjust = (
                (self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH
                 + len(message)) // 2)

            str_frame.append(
                message.rjust(len_rjust, "=").ljust(
                    self.app_config.game_config.INTERFACE_CONFIG.
                    MAIN_FRAME_LENGTH, "="))

        for _ in range(n_lower_fillrows):
            str_frame.append(
                "=" *
                self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        return str_frame

    def generate_lobby_character_selection_page(self) -> List[str]:

        str_frame = []

        screen_messages = [
            " PRESS KEY TO CHOOSE YOUR CHARACTER ",
            " THE FASTER THE CHARACTER, THE MORE POINTS YOU GET! "
            " USE ASDW KEYS TO MOVE YOUR CHARACTER "
        ]

        character_descriptions = [
            f" ({key}) {char.name} {char.emoji}: {char.description} " for key,
            char in ingame_settings.CharacterFactory.characters.items()
        ]

        screen_messages.extend(character_descriptions)

        n_upper_fillrows, n_lower_fillrows = self.get_fillrows(
            screen_messages=screen_messages)

        for _ in range(n_upper_fillrows):
            str_frame.append(
                "=" *
                self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        for message in screen_messages:

            str_frame.append(
                message.rjust(len(message) + 5, "=").ljust(
                    self.app_config.game_config.INTERFACE_CONFIG.
                    MAIN_FRAME_LENGTH, "="))

        for _ in range(n_lower_fillrows):
            str_frame.append(
                "=" *
                self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        return str_frame

    def generate_game_over_page(self, final_score: int) -> List[str]:

        str_frame = []

        screen_messages = [
            " GAME OVER! ", f" YOUR FINAL SCORE: {final_score} ",
            " PRESS ANY KEY TO RESTART OR ESC to EXIT. "
        ]

        n_upper_fillrows, n_lower_fillrows = self.get_fillrows(
            screen_messages=screen_messages)

        for _ in range(n_upper_fillrows):
            str_frame.append(
                "=" *
                self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        for message in screen_messages:

            len_rjust = (
                (self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH
                 + len(message)) // 2)

            str_frame.append(
                message.rjust(len_rjust, "=").ljust(
                    self.app_config.game_config.INTERFACE_CONFIG.
                    MAIN_FRAME_LENGTH, "="))

        for _ in range(n_lower_fillrows):
            str_frame.append(
                "=" *
                self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        return str_frame

    def get_fillrows(self, screen_messages: List[str]) -> Tuple[int, int]:

        n_upper_fillrows = (
            self.app_config.game_config.INTERFACE_CONFIG.TOTAL_FRAME_WIDTH -
            len(screen_messages)) // 2

        if (self.app_config.game_config.INTERFACE_CONFIG.TOTAL_FRAME_WIDTH -
                len(screen_messages)) % 2 == 1:
            n_lower_fillrows = n_upper_fillrows + 1
        else:
            n_lower_fillrows = n_upper_fillrows

        return n_upper_fillrows, n_lower_fillrows

    @classmethod
    def display_str_frame(cls: Type[InterfaceType],
                          str_frame: List[str]) -> None:
        stdscr = curses.initscr()
        stdscr.keypad(True)
        stdscr.nodelay(True)
        curses.noecho()
        curses.cbreak()

        for i, str_row in enumerate(str_frame):

            stdscr.addstr(i, 0, str_row)

        stdscr.refresh()
        time.sleep(10)

        curses.echo()
        curses.nocbreak()
        curses.endwin()
