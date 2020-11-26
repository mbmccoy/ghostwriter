import numpy as np
from ghostwriter.display import raster_index


def test_raster_index():
    array = np.arange(9).reshape((3, 3))
    result = raster_index(shape=(3, 3))
    print(result)
    print(array)
    print(array.reshape(np.product(array.shape))[result])
    assert np.testing.assert_equal(
        result,
        array[result],
    )
