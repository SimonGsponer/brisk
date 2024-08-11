try:
    from game_core import sum_as_string
except ModuleNotFoundError:
    from .game_core import sum_as_string

print(sum_as_string(2, 2))