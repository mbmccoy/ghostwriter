import abc
import logging
from typing import Tuple, Dict

import cv2
import numpy as np
try:
    from matplotlib import pyplot as plt
except ImportError:
    matplotlib = None

try:
    import neopixel
except NotImplementedError as _neopixel_import_error:
    neopixel = None
else:
    _neopixel_import_error = None

try:
    from adafruit_blinka.board.raspberrypi.raspi_40pin import pin as rpi_pin
except ImportError as _rpi_import_error:
    rpi_pin = None
    DEFAULT_PIN = None
else:
    _rpi_import_error = None
    DEFAULT_PIN = rpi_pin.D18


class Display(abc.ABC):
    """Abstract class for a display."""

    @abc.abstractmethod
    def show(self, frame: np.ndarray):
        pass


class OpenCVDisplay(Display):
    """Display a numpy array using OpenCV cv.imshow"""

    def __init__(
            self,
            shape: Tuple[int, int, int],
            window_size: Tuple[int, int],
            window_name="display",
    ):
        self.shape = shape
        self.window_name = window_name
        self.window_size = window_size
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, *window_size)

    def show(self, frame: np.ndarray) -> None:
        if frame.shape != self.shape:
            raise ValueError("Array shape must match window shape")
        cv2.imshow(self.window_name, frame)


class MatplotlibDisplay(Display):
    """Display to a matplotlib figure."""

    def __init__(
            self,
            is_brg: bool = True,
    ):
        self._image = None
        self._is_brg = is_brg
        self._has_been_closed = False

    @property
    def figure(self):
        return self._image.figure

    def show(self, frame: np.ndarray) -> None:
        if self._is_brg:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if self._image is None or self._has_been_closed:
            self._image = plt.imshow(frame)
            self._image.figure.canvas.mpl_connect("close_event", self._on_close)
        else:
            self._image.set_data(frame)
        # TODO: Implement animation API rather than direct drawing?
        plt.gcf().canvas.draw_idle()
        plt.pause(0.0001)

    def _on_close(self, event):
        self._has_been_closed = True


class AVIFileDisplay(Display):
    """Write output to .avi file."""

    def __init__(
            self,
            file_name: str,
            shape: Tuple[int, int, int],
            frames_per_second: float,
    ):
        if not file_name.endswith(".avi"):
            raise ValueError("File must end in .avi")
        self.file_name = file_name
        self.is_color = len(shape) == 3
        self.shape = shape
        self.code_name = "MJPG"
        self.frames_per_second = frames_per_second
        self._codec = cv2.VideoWriter_fourcc(*self.code_name)
        self._video_writer = cv2.VideoWriter(
            file_name=file_name,
            fourcc=self._codec,
            apiPreference=0,
            frameSize=shape[:1],
            isColer=self.is_color,
            fps=frames_per_second,
        )

    def __del__(self):
        self._video_writer.release()

    def show(self,  frame: np.ndarray) -> None:
        if frame.shape != self.shape:
            raise ValueError("Array shape must match window shape")
        self._video_writer.write(frame)


class NeoPixelDisplay(Display):

    def __init__(
            self,
            display_shape: Tuple[int, int],
            pin: "rpi_pin.Pin" = DEFAULT_PIN,
            brightness: float = 1.0,
    ):
        self._display_shape = display_shape
        self._n_pixels = np.product(self._display_shape[:1])
        self._pin = pin
        self._logger = logging.getLogger(__name__)
        self._raster_index = raster_index(
            self._display_shape,
        )
        if rpi_pin is not None:
            self._pixels = neopixel.NeoPixel(
                rpi_pin.D18,
                np.product(display_shape),
                brightness=brightness,
            )
        else:
            self._logger.warning("Unable to import pins: %s", _rpi_import_error)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._pixels.deinit()

    def show(self, frame: np.ndarray) -> None:
        #resized = cv2.resize(frame, self._display_shape, interpolation=cv2.INTER_AREA)
        resized = frame
        self._pixels[:] = resized[self._raster_index]


def raster_index(
    shape: Tuple[int, int],
    rows: bool = True,
    reverse_rows: bool = False,
    reverse_columns: bool = False,
) -> Tuple[np.ndarray, ...]:
    """

    Parameters
    ----------
    shape
        The shape of the array.
    rows
        If ``True``, raster along rows. Otherwise, raster along columns.
    reverse_rows
        A changes the raster orientation over rows. The default (``False``)
        starts left-to-right.
    reverse_columns
        A changes the raster orientation over columns. The default (``False``)
        starts top-to-bottom.

    Returns
    -------
    A pair (x, y) of indices into an array.
    """
    # Swap rows and columns
    if not rows:
        shape = shape[1], shape[0]
        reverse_rows, reverse_columns = reverse_columns, reverse_rows
    parity = 0
    index = []
    for i in range(shape[0]):
        if reverse_columns:
            i = shape[0] - i - 1
            parity = (shape[0] + 1) % 2
        for j in range(shape[1]):
            if reverse_rows:
                j = shape[1] - j - 1
            if (i + parity) % 2:
                index.append((i + 1) * shape[1] - (j + 1))
            else:
                index.append(i * shape[1] + j)
    results = np.unravel_index(index, shape)
    # Undo swap
    if not rows:
        results = results[1], results[0]
    return results


_DISPLAYS: Dict[str, Display] = {}


def mpl_imshow(window_name: str, opencv_image: np.ndarray):
    """Matplotlib imageshow"""
    if window_name not in _DISPLAYS:
        _DISPLAYS[window_name] = MatplotlibDisplay(is_brg=True)
    print("Drawing")
    _DISPLAYS[window_name].show(opencv_image)
