
import unittest

import numpy as np


class InterfaceTestCase(unittest.TestCase):

    def test_slice(self):
        """Asserts slicing behaviour for numpy matrices."""
        list_matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 48],
            [100, 20, 30, 40]
        ]
        matrix = np.array(list_matrix, dtype=np.int64)

        matrix_slice = matrix[:, 1:2]
        expected_slice = np.array(
            [
                [2],
                [6],
                [20]
            ],
            dtype=np.int64
        )

        np.testing.assert_array_equal(matrix_slice, expected_slice)

    def test_cell_indexing(self):
        """Asserts cell indexing behaviour for numpy matrices."""
        list_matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 48],
            [100, 20, 30, 40]
        ]
        matrix = np.array(list_matrix, dtype=np.int64)

        matrix_slice = matrix[1, 1]
        expected_slice = np.array(
            [
                [6],
            ],
            dtype=np.int64
        )

        np.testing.assert_array_equal(matrix_slice, expected_slice)
