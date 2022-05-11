# pylint: disable=no-self-use, redefined-outer-name
"""Contains all unittests for objects defined in src.engine."""

import numpy as np

from src import engine
from src.utils import config
from src import ingame_settings
from testing.unittesting.fixtures import (  # pylint: disable=unused-import
    default_configs, any_character)


class TestEngineClassmethods():
    """Test all classmethods of Engine class."""

    def test_proc_count(self) -> None:
        """Test behaviour of counting procs."""
        threshold_probas = [0.1, 0.01, 0.001]
        effective_probas = [0.5, 0.001, 0.08]

        n_procs = engine.Engine.count_procs(threshold_probas=threshold_probas,
                                            effective_probas=effective_probas)

        assert n_procs == 1

    def test_get_n_obstacle_procs_100_pcnt(self) -> None:
        """Test behaviour for proc rate = 1."""
        n_procs = engine.Engine.get_n_procs(proc_proba=1, n_max_procs=3)

        assert n_procs == 3

    def test_get_n_obstacle_procs_0_pcnt(self) -> None:
        """Test behaviour for proc rate = 0"""
        n_procs = engine.Engine.get_n_procs(proc_proba=0, n_max_procs=3)

        assert n_procs == 0

    def test_get_n_obstacle_procs_30_pcnt(self) -> None:
        """Test if proc function returns expected range."""
        expected_n_procs = [0, 1, 2, 3]
        effective_procs = [
            engine.Engine.get_n_procs(proc_proba=0.5, n_max_procs=3)
            for _ in range(1000)
        ]

        for exepcted_n_proc in expected_n_procs:
            assert exepcted_n_proc in effective_procs

        for effective_proc in set(effective_procs):
            assert effective_proc in expected_n_procs

    def test_convert_graph_matrx(self) -> None:
        """Test conversion from numeric representation to string representation of game."""
        input_graph_matrix: np.typing.NDArray[np.int64] = np.array(
            [[1, 1, 0], [100, 1, 2], [100, 2, 350]], dtype=np.int64)

        expected_str_frame = [
            "## ",
            "X#P",
            "XP🔥",
        ]

        str_frame = engine.Engine.convert_graph_matrix(
            graph_matrix=input_graph_matrix,
            obstacle_emoji="P",
            main_char_emoji="X")

        assert str_frame == expected_str_frame


class TestEngine():
    """Test Engine class."""

    def test_class_init(self, any_character: ingame_settings.Character,
                        default_configs: config.AppConfig) -> None:
        """Test instantiation."""
        _ = engine.Engine(char=any_character, app_config=default_configs)

    def test_init_graph_matrix(self, any_character: ingame_settings.Character,
                               default_configs: config.AppConfig) -> None:
        """Test instantiation of graph matrix."""
        app_engine = engine.Engine(char=any_character,
                                   app_config=default_configs)

        expected_shape = (
            app_engine.app_config.game_config.INTERFACE_CONFIG.
            MAIN_FRAME_WIDTH,
            app_engine.app_config.game_config.INTERFACE_CONFIG.
            MAIN_FRAME_LENGTH,
        )

        assert app_engine.graph_matrix.dtype == np.int64
        assert app_engine.graph_matrix.shape == expected_shape
