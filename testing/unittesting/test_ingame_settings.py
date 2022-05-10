from multiprocessing.sharedctypes import Value
import pytest

from src import ingame_settings


class TestCaseObstacle:

    @pytest.mark.parametrize(
        "emoji_input, proc_input",
        [
            (pytest.param(
                "kk", 0.5, marks=pytest.mark.xfail(raises=ValueError))),
            (pytest.param("😀", 0.5,
                          marks=pytest.mark.xfail(raises=ValueError))),
            (pytest.param("😀", 2, marks=pytest.mark.xfail(raises=ValueError))),
            (pytest.param("☃", 2, marks=pytest.mark.xfail(raises=ValueError))),
            (pytest.param("☃", 0.5)),
            (pytest.param("k", 0)),
            (pytest.param("k", 1)),
        ],
    )
    def test_init(self, emoji_input, proc_input):

        _ = ingame_settings.Obstacle(obstacle_emoji=emoji_input,
                                     proc_rate=proc_input)

    @pytest.mark.parametrize("input_string,expected_len", [("kk", 2), ("k", 1),
                                                           ("☃", 1), ("😀", 2),
                                                           ("🔥", 2), ("🔥", 2)])
    def test_get_char_length(self, input_string, expected_len):
        output_len = ingame_settings.Obstacle.get_char_length(
            input_str=input_string)
        assert output_len == expected_len
