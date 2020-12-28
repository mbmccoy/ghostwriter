import numpy as np
from ghostwriter.display import raster_index


def test_raster_index():
    shape = (3, 4)
    array = np.arange(np.product(shape)).reshape(shape)
    np.testing.assert_array_equal(
        array[raster_index(shape=shape)],
        [0, 1, 2, 3, 7, 6, 5, 4, 8, 9, 10, 11]
    )

    np.testing.assert_array_equal(
        array[raster_index(shape=shape, reverse_rows=True)],
        [3, 2, 1, 0, 4, 5, 6, 7, 11, 10, 9, 8],
    )

    np.testing.assert_array_equal(
        array[raster_index(shape=shape, reverse_columns=True)],
        [8, 9, 10, 11, 7, 6, 5, 4, 0, 1, 2, 3],
    )

    np.testing.assert_array_equal(
        array[raster_index(shape=shape, reverse_rows=True, reverse_columns=True)],
        [11, 10, 9, 8, 4, 5, 6, 7, 3, 2, 1, 0],
    )

    np.testing.assert_array_equal(
        array[raster_index(shape=shape, rows=False)],
        [0, 4, 8, 9, 5, 1, 2, 6, 10, 11, 7, 3],
    )

    np.testing.assert_array_equal(
        array[raster_index(shape=shape, rows=False, reverse_rows=True)],
        [3, 7, 11, 10, 6, 2, 1, 5, 9, 8, 4, 0],
    )

    np.testing.assert_array_equal(
        array[raster_index(shape=shape, rows=False, reverse_columns=True)],
        [8, 4, 0, 1, 5, 9, 10, 6, 2, 3, 7, 11],
    )

    np.testing.assert_array_equal(
        array[raster_index(shape=shape, rows=False, reverse_rows=True, reverse_columns=True)],
        [11, 7, 3, 2, 6, 10, 9, 5, 1, 0, 4, 8]
    )
