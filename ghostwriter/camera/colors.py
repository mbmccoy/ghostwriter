import os
from typing import Dict, Tuple

import numpy as np

from ghostwriter.paths import DATA_DIR

COLOR_FILE = os.path.join(DATA_DIR, "xkcd", "colors.txt")

_XKCD_COLORS = None

def _get_color_bgr(color: str) -> Tuple[int, int, int]:
    return int(color[5:7], base=16), int(color[3:5], base=16), int(color[1:3], base=16)


def load_xkcd_colors() -> Dict[str, Tuple[int, int, int]]:
    """Loads XKCD colors as dict, in BGR order."""
    global _XKCD_COLORS
    if  _XKCD_COLORS is not None:
        return _XKCD_COLORS

    with open(COLOR_FILE, "r") as fp:
        color_lines = fp.readlines()

    # Remove commented lines (start with '#')
    colors = (line.split("\t") for line in color_lines if not line.startswith("#"))
    _XKCD_COLORS = {
        color_name: _get_color_bgr(color_value) for color_name, color_value in colors
    }
    return _XKCD_COLORS


def xkcd_color_matrix_like(matrix: np.ndarray, color_name: str) -> np.ndarray:
    colors = load_xkcd_colors()
    color = colors[color_name]
    return np.full_like(matrix, color)  # noqa
