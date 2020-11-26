import abc
import logging
from typing import Tuple, Optional, Dict

import cv2
import numpy as np
from matplotlib import pyplot as plt

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
else:
    _rpi_import_error = None


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
            input_shape: Tuple[int, ...],
            display_shape: Tuple[int, ...],
            pin: "rpi_pin.Pin",
    ):
        self._input_shape = input_shape
        self._display_shape = display_shape
        self._n_pixels = np.product(input_shape[:1])
        self._pin = pin
        self._logger = logging.getLogger(__name__)
        if rpi_pin is not None:
            self._pixels = neopixel.NeoPixel(rpi_pin.D18, 16 * 16, brightness=0.05)
        else:
            self._logger.warning("Unable to import pixels: %s", _rpi_import_error)
        self._raster_index = np.arange(self._n_pixels)

    def show(self, frame: np.ndarray) -> None:
        pass


def raster_index(
        shape: Tuple[int, ...],
        direction: Optional[Tuple[int, ...]] = None,
) -> np.ndarray:
    if direction is None:
        direction = tuple(0 for _ in shape)

    def _raster_multi_index(multi_index: Tuple[int, ...]) -> Tuple[int, ...]:
        result = tuple(
            m if (i + d + 1) % 2 else s - m - 1
            for i, (s, m, d) in enumerate(zip(shape, multi_index, direction))
        )
        print(multi_index, result)
        return result
    multi_indices = np.unravel_index(
        np.arange(np.product(shape)),
        shape=shape,
    )
    rastered_multi = np.apply_along_axis(
        _raster_multi_index,
        axis=0,
        arr=multi_indices,
    )
    return np.ravel_multi_index(rastered_multi, dims=shape)


_DISPLAYS: Dict[str, Display] = {}


def mpl_imshow(window_name: str, opencv_image: np.ndarray):
    """Matplotlib imageshow"""
    if window_name not in _DISPLAYS:
        _DISPLAYS[window_name] = MatplotlibDisplay(is_brg=True)
    print("Drawing")
    _DISPLAYS[window_name].show(opencv_image)