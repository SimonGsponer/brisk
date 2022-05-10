import time


class Score:

    base_multiplier = 2

    def __init__(self, main_char_score_multiplier):

        self.current_ts = None
        self.last_ts = None
        self.current_score = 0
        self.char_multiplier = main_char_score_multiplier

    def start_scoring(self):

        self.last_ts = time.time()

    def increment_score(self):

        self.current_ts = time.time()

        time_increase = self.current_ts - self.last_ts

        self.current_score += time_increase * self.base_multiplier * self.char_multiplier

        self.last_ts = self.current_ts

    @property
    def get_current_score(self):

        return int(self.current_score)
