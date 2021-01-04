from itertools import product
from typing import Tuple

from adafruit_blinka.board.raspberrypi.raspi_40pin import pin
import time

import numpy as np

from ghostwriter.display import NeoPixelDisplay, Display


# GPIO.XX =  pin.DXX


def main():
    shape = (24, 16)
    with NeoPixelDisplay(
        display_shape=shape,
        pin=pin.D18,
        brightness=0.05,
    ) as display:
        run(display, shape=shape)


def run(display: Display, shape: Tuple[int, ...]):
    start_time = time.time()
    n = np.product(shape)
    image = np.zeros((shape[0], shape[1], 3), dtype=int)
    for i, j in product(*map(range, shape)):
        pixel_value = (100 % 256, (8 * i) % 256, (128 - 12 * j) % 256)
        image[i, j, :] = pixel_value
        display.show(image)
    run_time = time.time() - start_time
    print(f"Ran {n} frames in {run_time} seconds ({n/run_time} fps)")


if __name__ == "__main__":
    main()
