"""
* choose character/difficulty
"""
import unicodedata
from dataclasses import dataclass, field

from src.utils import config

app_config = config.AppConfig()


@dataclass
class Obstacle:
    obstacle_emoji: str
    proc_rate: float

    def __post_init__(self):
        """Performs validation of developer-defined input.
        
        Makes sure that the specified emoji has an effective display size of 1, and
        that the defined proc_rate is a probability between 0 and 1.

        Raises:
            ValueError: Raised if one if the emoji has a larger display size than 1 or
                the proc rate is not a probability.
        """
        emoji_display_size = Obstacle.get_char_length(
            input_str=self.obstacle_emoji
        )
        if emoji_display_size > 1:
            error_msg = f"The emoji you chose `{self.obstacle_emoji}` has a display size larger than 1 (`{emoji_display_size}`); choose a different one!"
            raise ValueError(error_msg)

        if not 0 <= self.proc_rate <= 1:
            error_msg = "proc_rate must be a probability between 0 and 1!"
            raise ValueError(error_msg)
    
    @classmethod
    def get_char_length(cls, input_str):
        """Calculates the actual character length of a symbol.

        Args:
            char: Input character.
        
        Returns:
            Length of UTF-encoded input character.
        """
        char_length = 0

        category_length_mapping = {
            "W": 2,
            "N": 1,
            "Na": 1
        }

        for char in input_str:

            char_category = unicodedata.east_asian_width(char)
            char_length += category_length_mapping[char_category]

        return char_length


@dataclass
class Character:
    name: str
    emoji: str
    speed_multiplier: float
    horizontal_padding: float
    rel_horizontal_pos: float
    description: str
    obstacle: Obstacle


snow = Obstacle(
    obstacle_emoji="☃",
    proc_rate=0.05
)

beach = Obstacle(
    obstacle_emoji="☼",
    proc_rate=0.1
)

traffic = Obstacle(
    obstacle_emoji="$",
    proc_rate=0.1
)

skiing_simon = Character(
    name="Shredding Simon",
    emoji="🏂",
    speed_multiplier=1,
    horizontal_padding=10,
    rel_horizontal_pos=0.25,
    description="Can Simon count on your help to reach the ski resort?",
    obstacle=snow
    )


surfing_sandy = Character(
    name="Surfing Sandy",
    emoji="🏄",
    speed_multiplier=1.5,
    horizontal_padding=20,
    rel_horizontal_pos=0.5,
    description="The waves are calling, and Sandy needs to go surfing ASAP!",
    obstacle=beach
    )


running_ryan = Character(
    name="Running Ryan",
    emoji="🏃",
    speed_multiplier=3,
    horizontal_padding=40,
    rel_horizontal_pos=0.75,
    description="Ryan has overslept on his first day at work; help him reach the office!",
    obstacle=traffic
    )


class CharacterFactory:

    characters = dict(
        A=skiing_simon,
        B=surfing_sandy,
        C=running_ryan
    )

    def __init__(self):
        
        pass

    def get_character(self, key_input):

        return self.characters[CharacterFactory.key_mapping(key_input=key_input)]

    @classmethod
    def key_mapping(cls, key_input):

        key_map = {
            "97": "A",
            "98": "B",
            "99": "C",
        }

        return key_map[str(key_input)]


if __name__=='__main__':

    print(len("😁"))