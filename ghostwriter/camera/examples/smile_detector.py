from typing import Dict

import cv2 as cv
import logging

from ghostwriter.display import mpl_imshow
from ghostwriter.paths import DATA_DIR
from ghostwriter.utils import default_arguments, set_up_logging
from ghostwriter.camera.gamma import GammaCorrector
from ghostwriter.camera.keymap import KEY_UP, KEY_DOWN

import matplotlib

from scripts.python_info import is_m1_mac



def update_gamma_from_key_press(gamma, key, factor=1.1):
    logger = logging.getLogger(__name__)
    if key == KEY_UP:
        new_gamma = gamma / factor
    elif key == KEY_DOWN:
        new_gamma = gamma * factor
    else:
        new_gamma = gamma
    logger.debug("gamma = %s", gamma)
    return new_gamma


def detect_and_display(frame, face_cascade, eyes_cascade, smile_cascade):
    logger = logging.getLogger(__name__)
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

    # cv.imshow("Capture - Face detection", frame)
    mpl_imshow("Capture - Face detection", frame)


def main():
    parser = default_arguments(description="Code for Cascade Classifier tutorial.")
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

    # Turn on mac
    if is_m1_mac():
        matplotlib.use("MacOSX")

    args = parser.parse_args()
    set_up_logging(args.verbose)
    logger = logging.getLogger(__name__)
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


if __name__ == "__main__":
    main()
