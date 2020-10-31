import cv2 as cv
import argparse
import logging

import numpy as np

from ghostwriter.paths import DATA_DIR

logger = logging.getLogger(__name__)

KEY_LEFT = 81
KEY_UP = 82
KEY_RIGHT = 83
KEY_DOWN = 84
QUIT = ord("q")


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
        logger.debug("Index=%d", index)
        return self._lookup_tables[index]

    def correct(self, image, gamma):
        return cv.LUT(image, self._get_lookup_table(gamma))


def update_gamma_from_key_press(gamma, key, factor=1.1):
    if key == KEY_UP:
        new_gamma = gamma / factor
    elif key == KEY_DOWN:
        new_gamma = gamma * factor
    else:
        new_gamma = gamma
    logger.debug("gamma = %s", gamma)
    return new_gamma


def detect_and_display(frame, face_cascade, eyes_cascade, smile_cascade):

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    # -- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y : y + h, x : x + w]

        # -- In each face, detect eyes and smiles
        eyes = eyes_cascade.detectMultiScale(faceROI)
        smiles = smile_cascade.detectMultiScale(faceROI, 1.8, 20)

        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)

        for (x2, y2, w2, h2) in smiles:
            pt1 = (x + x2, y + y2)
            pt2 = (x + x2 + w2, y + y2 + h2)
            logger.debug("Smile detected!")
            frame = cv.rectangle(frame, pt1, pt2, color=(255, 255, 0))

    cv.imshow("Capture - Face detection", frame)


def main():
    log_format = "%(levelname)s:%(asctime)s:%(name)s:%(filename)s:" \
                 "%(funcName)s:%(lineno)d:%(message)s"
    logging.basicConfig(format=log_format, level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        description="Code for Cascade Classifier tutorial."
    )
    parser.add_argument(
        "--face_cascade",
        help="Path to face cascade.",
        default="{}/haarcascades/haarcascade_frontalface_alt.xml".format(DATA_DIR),
    )
    parser.add_argument(
        "--smile_cascade",
        help="Path to face cascade.",
        default="{}/haarcascades/haarcascade_smile.xml".format(DATA_DIR),
    )
    parser.add_argument(
        "--eyes_cascade",
        help="Path to eyes cascade.",
        default="{}/haarcascades/haarcascade_eye_tree_eyeglasses.xml".format(DATA_DIR),
    )
    parser.add_argument("--camera", help="Camera number.", type=int, default=0)
    args = parser.parse_args()

    gamma_corrector = GammaCorrector()

    face_cascade_name = args.face_cascade
    eyes_cascade_name = args.eyes_cascade
    smile_cascade_name = args.smile_cascade

    face_cascade = cv.CascadeClassifier()
    eyes_cascade = cv.CascadeClassifier()
    smile_cascade = cv.CascadeClassifier()
    # -- 1. Load the cascades
    if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
        logger.error("Error loading face cascade")
        return
    if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
        logger.error("Error loading eyes cascade")
        return
    if not smile_cascade.load(cv.samples.findFile(smile_cascade_name)):
        logger.error("Error loading smile cascade")
        return

    camera_device = args.camera
    # -- 2. Read the video stream
    cap = cv.VideoCapture(camera_device)
    if not cap.isOpened:
        logger.error("Error opening video capture")
        return

    gamma = 1.0

    while True:
        ret, frame = cap.read()
        if frame is None:
            logger.error("No captured frame; is your camera available?")
            break
        detect_and_display(
            gamma_corrector.correct(frame, gamma),
            face_cascade=face_cascade,
            eyes_cascade=eyes_cascade,
            smile_cascade=smile_cascade,
        )
        key = cv.waitKey(30)
        logger.debug("Key = %s", key)
        gamma = update_gamma_from_key_press(gamma, key)
        if key == QUIT:
            logger.info("Quit key pressed.")
            break


if __name__ == "__main__":
    main()
