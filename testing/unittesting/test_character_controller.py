# pylint: disable=no-self-use
"""Contains all unittests for objects defined in src.character_controller."""

import numpy as np
import pytest
from src import character_controller
from src.engine import GraphMatrixType, OneDArray
from src.utils import config

from testing.unittesting.fixtures import (  # pylint: disable=unused-import
    example_road_graph_matrix, default_configs)


class TestCharacterController():
    """Test character controller class."""

    def test_slice(self) -> None:
        """Asserts slicing behaviour for numpy matrices."""
        list_matrix = [[1, 2, 3, 4], [5, 6, 7, 48], [100, 20, 30, 40]]
        matrix: GraphMatrixType = np.array(list_matrix, dtype=np.int64)

        matrix_slice = matrix[:, 1:2]
        expected_slice: GraphMatrixType = np.array([[2], [6], [20]],
                                                   dtype=np.int64)

        np.testing.assert_array_equal(matrix_slice, expected_slice)

    def test_cell_indexing(self) -> None:
        """Asserts cell indexing behaviour for numpy matrices."""
        list_matrix = [[1, 2, 3, 4], [5, 6, 7, 48], [100, 20, 30, 40]]
        matrix: GraphMatrixType = np.array(list_matrix, dtype=np.int64)

        matrix_slice = matrix[1, 1]
        expected_slice: GraphMatrixType = np.array([
            [6],
        ], dtype=np.int64)

        np.testing.assert_array_equal(matrix_slice, expected_slice)

    @pytest.mark.parametrize(
        "starting_pos, expected_index_positions",
        [
            (pytest.param(2, np.array([3, 4], dtype=np.int64))),
            (pytest.param(0, np.array([4, 5], dtype=np.int64))),
            (pytest.param(-1, np.array([3, 4], dtype=np.int64))),
            (pytest.param(4, np.array([2, 3], dtype=np.int64))),
        ],
    )
    def test_find_empty_spot_to_place_char(
            self, example_road_graph_matrix: GraphMatrixType,
            default_configs: config.AppConfig, starting_pos: int,
            expected_index_positions: OneDArray) -> None:

        char_controller = character_controller.CharacterController(
            start_street=example_road_graph_matrix,
            app_config=default_configs,
            char_horizontal_starting_pos=starting_pos)

        empty_spots = char_controller.find_empty_spot_to_place_char()

        np.testing.assert_array_equal(empty_spots, expected_index_positions)
