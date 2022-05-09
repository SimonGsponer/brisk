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
import sys 
import time
from pathlib import Path
import curses

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent.parent))

from src.utils import config
from src import ingame_settings

app_config = config.AppConfig()

class Interface():

    app_config = app_config

    def __init__(self):

        pass

    def generate_lobby_landing_page(self):
        
        str_frame = list()

        screen_messages = [
            " HELLO! PRESS ANY ",
            " KEY TO START OR ESC TO EXIT. "
        ]

        n_upper_fillrows, n_lower_fillrows = self.get_fillrows(
            screen_messages=screen_messages
        )

        for i in range(n_upper_fillrows):
            str_frame.append("=" * self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        for message in screen_messages:

            len_rjust = (
                (self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH + len(message) ) // 2
            )
            
            str_frame.append(message.rjust(len_rjust, "=").ljust(self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH, "="))


        for i in range(n_lower_fillrows):
            str_frame.append("=" * self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)     

        return str_frame

    def generate_lobby_character_selection_page(self):
        
        str_frame = list()

        screen_messages = [
            " PRESS KEY TO CHOOSE YOUR CHARACTER ",
            " THE FASTER THE CHARACTER, THE MORE POINTS YOU GET! "
            " USE ASDW KEYS TO MOVE YOUR CHARACTER "
        ]

        character_descriptions = [
            f" ({key}) {char.name} {char.emoji}: {char.description} " for key, char in ingame_settings.CharacterFactory.characters.items()
        ]

        screen_messages.extend(character_descriptions)

        n_upper_fillrows, n_lower_fillrows = self.get_fillrows(
            screen_messages=screen_messages
        )

        for i in range(n_upper_fillrows):
            str_frame.append("=" * self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        for message in screen_messages:

            len_rjust = (
                (self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH + len(message) ) // 2
            )
            
            str_frame.append(message.rjust(len(message) + 5, "=").ljust(self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH, "="))


        for i in range(n_lower_fillrows):
            str_frame.append("=" * self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)  

        return str_frame

    def generate_game_over_page(self, final_score):
        
        str_frame = list()

        screen_messages = [
            " GAME OVER! ",
            f" YOUR FINAL SCORE: {final_score} ",
            " PRESS ANY KEY TO RESTART OR ESC to EXIT. "
        ]

        n_upper_fillrows, n_lower_fillrows = self.get_fillrows(
            screen_messages=screen_messages
        )

        for i in range(n_upper_fillrows):
            str_frame.append("=" * self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)

        for message in screen_messages:

            len_rjust = (
                (self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH + len(message) ) // 2
            )
            
            str_frame.append(message.rjust(len_rjust, "=").ljust(self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH, "="))


        for i in range(n_lower_fillrows):
            str_frame.append("=" * self.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH)     

        return str_frame

    def get_fillrows(self, screen_messages):
        
        n_upper_fillrows = (self.app_config.game_config.INTERFACE_CONFIG.TOTAL_FRAME_WIDTH - len(screen_messages)) // 2

        if (self.app_config.game_config.INTERFACE_CONFIG.TOTAL_FRAME_WIDTH - len(screen_messages)) % 2 == 1:
            n_lower_fillrows = n_upper_fillrows + 1
        else:
            n_lower_fillrows = n_upper_fillrows

        return n_upper_fillrows, n_lower_fillrows


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

    game_interface = Interface()

    str_frame = game_interface.generate_lobby_character_selection_page()

    game_interface.display_str_frame(
        str_frame=str_frame
        )