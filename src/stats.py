import time
from typing import Union, Optional


class Score:

    base_multiplier = 2

    def __init__(self, main_char_score_multiplier: Union[float, int]) -> None:

        self.current_ts: Optional[float] = None
        self.last_ts: Optional[float] = None
        self.current_score: float = 0.0
        self.char_multiplier = main_char_score_multiplier

    def start_scoring(self) -> None:

        self.last_ts = time.time()

    def increment_score(self) -> None:

        self.current_ts = time.time()

        if not self.last_ts:
            raise AttributeError(
                "start_scoring() has not been called yet, self.last_ts is null!"
            )

        time_increase = self.current_ts - self.last_ts

        self.current_score += time_increase * float(
            self.base_multiplier) * float(self.char_multiplier)

        self.last_ts = self.current_ts

    @property
    def get_current_score(self) -> int:

        return int(self.current_score)
