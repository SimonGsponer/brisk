# pylint: disable=no-self-use
"""Contains all unittests for objects defined in src.ingame_settings."""
import pytest

from src import ingame_settings


class TestObstacle:
    """Test obstacle class."""

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
    def test_init(self, emoji_input: str, proc_input: float) -> None:
        """Test instantiation of data class with different values, with some expected to fail."""
        _ = ingame_settings.Obstacle(obstacle_emoji=emoji_input,
                                     proc_rate=proc_input)

    @pytest.mark.parametrize("input_string,expected_len", [("kk", 2), ("k", 1),
                                                           ("☃", 1), ("😀", 2),
                                                           ("🔥", 2), ("🔥", 2)])
    def test_get_char_length(self, input_string: str,
                             expected_len: int) -> None:
        """Tests the get character length classmethod."""
        output_len = ingame_settings.Obstacle.get_char_length(
            input_str=input_string)
        assert output_len == expected_len
