import logging

import cv2 as cv
import numpy as np


class GammaCorrector:
    _BASE = np.linspace(0, 1, 256)

    def __init__(self, num_levels=128, gamma_min=0.001, gamma_max=5.0):
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Building lookup tables")
        self._gamma_min = gamma_min
        self._gamma_max = gamma_max
        self._gammas = np.logspace(np.log10(gamma_min), np.log10(gamma_max), num_levels)
        self._lookup_tables = [
            self._generate_lookup_table(gamma) for gamma in self._gammas
        ]
        self.logger.debug("Done building lookup tables.")

    @classmethod
    def _generate_lookup_table(cls, gamma):
        look_up_table = np.clip(np.power(cls._BASE, gamma) * 255.0, 0, 255)
        return look_up_table.astype(np.uint8)

    def _get_lookup_table(self, gamma):
        gamma = np.clip(gamma, self._gamma_min, self._gamma_max)
        index = np.searchsorted(self._gammas, gamma)
        return self._lookup_tables[index]

    def correct(self, image, gamma):
        return cv.LUT(image, self._get_lookup_table(gamma))
