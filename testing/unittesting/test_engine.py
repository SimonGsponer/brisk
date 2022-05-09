
import unittest

import numpy as np
import pytest

from src import engine
from testing.unittesting.fixtures import default_configs


class TestEngineClassmethods():


    def test_proc_count(self):
        """Test behaviour of counting procs."""
        
        threshold_probas = [0.1, 0.01, 0.001]
        effective_probas = [0.5, 0.001, 0.08]

        n_procs = engine.Engine.count_procs(
            threshold_probas=threshold_probas,
            effective_probas=effective_probas
        )

        assert n_procs == 1


    def test_get_n_obstacle_procs_100_pcnt(self):
        """Test behaviour for proc rate = 1."""

        n_procs = engine.Engine.get_n_procs(
            proc_proba=1,
            n_max_procs=3
        )

        assert n_procs == 3


    def test_get_n_obstacle_procs_0_pcnt(self):
        """Test behaviour for proc rate = 0"""

        n_procs = engine.Engine.get_n_procs(
            proc_proba=0,
            n_max_procs=3
        )

        assert n_procs == 0


    def test_get_n_obstacle_procs_30_pcnt(self):
        """Test if proc function returns expected range."""

        expected_n_procs = [0, 1, 2, 3]
        effective_procs = []

        for i in range(1000):
            n_procs = engine.Engine.get_n_procs(
                proc_proba=0,
                n_max_procs=3
            )

            effective_procs.append(n_procs)

        assert all([True if item in expected_n_procs else False for item in effective_procs])


    def test_convert_graph_matrx(self):

        input_graph_matrix = np.array(
            [
                [1, 1, 0],
                [100, 1, 2],
                [100, 2, 350]
            ]
        )

        expected_str_frame = [
            "## ",
            "X#P",
            "XP🔥",
        ]

        str_frame = engine.Engine.convert_graph_matrix(
            graph_matrix=input_graph_matrix,
            obstacle_emoji="P",
            main_char_emoji="X"
        )

        assert str_frame == expected_str_frame

class TestEngine():


    def test_class_init(self, default_configs):

        _ = engine.Engine(char=None, app_config=default_configs)


    def test_init_graph_matrix(self, default_configs):

        app_engine = engine.Engine(char=None, app_config=default_configs)
        
        expected_shape = (
            app_engine.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_WIDTH,
            app_engine.app_config.game_config.INTERFACE_CONFIG.MAIN_FRAME_LENGTH,
        )

        assert app_engine.graph_matrix.dtype == np.int64
        assert app_engine.graph_matrix.shape == expected_shape

