import logging

import cv2 as cv
import numpy as np

from ghostwriter.camera.colors import xkcd_color_matrix_like
from ghostwriter.camera.keymap import QUIT
from ghostwriter.utils import default_arguments, set_up_logging

BACKGROUND_SUBTRACTION_ALGORITHMS = {
    "MOG2": cv.createBackgroundSubtractorMOG2,
    "KNN": cv.createBackgroundSubtractorKNN,
    "CNT": cv.bgsegm.createBackgroundSubtractorCNT,
    "GMG": cv.bgsegm.createBackgroundSubtractorGMG,  # Fucking great
    "GSOC": cv.bgsegm.createBackgroundSubtractorGSOC,  # Meh
    "LSBP": cv.bgsegm.createBackgroundSubtractorLSBP,  # Interesting
    "MOG": cv.bgsegm.createBackgroundSubtractorMOG,
}


def main():
    parser = default_arguments(description="Background substraction methods.")
    parser.add_argument(
        "--algorithm",
        choices=sorted(BACKGROUND_SUBTRACTION_ALGORITHMS),
        default="GMG",
    )

    args = parser.parse_args()
    set_up_logging(args.verbose)
    logger = logging.getLogger(__name__)

    back_sub = BACKGROUND_SUBTRACTION_ALGORITHMS[args.algorithm]()

    camera_device = args.camera
    # -- 2. Read the video stream
    cap = cv.VideoCapture(camera_device)
    if not cap.isOpened:
        logger.error("Error opening video capture")
        return

    ret, frame = cap.read()
    codec = cv.VideoWriter_fourcc(*"MJPG")
    video_writer = cv.VideoWriter(
        filename="outpy.avi",
        apiPreference=0,
        fourcc=codec,
        fps=12.0,
        frameSize=frame.shape[:2][::-1],
        isColor=1,
    )
    writing_started = False
    assert video_writer.isOpened()
    output = np.zeros_like(frame)

    output_green = output.copy()
    last_pink = output.copy()
    pink = xkcd_color_matrix_like(frame, color_name="hot pink")
    green = xkcd_color_matrix_like(frame, color_name="neon green")

    kernel = np.array(
        [
            [2.0, 0.5, 0.5, -1.0],
            [0.5, -1, 1, 0.5],
            [0, 1, -1, 0.5],
            [1.0, 0.5, 0.5, 2.0],
        ],
        np.float32,
    )
    kernel = 0.9 * kernel / kernel.sum()
    cv.namedWindow("OutputDown", cv.WINDOW_NORMAL)
    cv.resizeWindow("OutputDown", 400, 400)
    while cv.waitKey(33) != QUIT and frame is not None:
        ret, frame = cap.read()
        foreground_mask = back_sub.apply(frame, learningRate=0.1)
        try:
            background_image = back_sub.getBackgroundImage()
        except cv.error:
            background_image = None
        background_mask = ~foreground_mask
        pink_mask = cv.bitwise_and(pink, pink, mask=foreground_mask)
        green_mask = cv.bitwise_and(green, green, mask=foreground_mask)

        output_green = cv.bitwise_and(output_green, output_green, mask=background_mask)
        output_green += green_mask
        output_green = cv.filter2D(output_green, -1, kernel)

        output = pink_mask.copy()
        mask = (np.maximum(pink_mask, last_pink).sum(axis=2) < 150).astype(np.uint8)
        last_pink = output.copy()
        output += cv.bitwise_and(output_green, output_green, mask=mask)

        output_down = cv.resize(
            output,
            (16, 16),
            interpolation=cv.INTER_NEAREST,
        )
        cv.imshow("Frame", frame)
        cv.imshow("Foreground Mask", pink_mask)
        if background_image is not None:
            cv.imshow("Background image", background_image)
        cv.imshow("Output", output)
        cv.imshow("OutputDown", output_down)

        if np.any(output) or writing_started:
            writing_started = True
            video_writer.write(output)

        key = cv.waitKey(10)
        logger.debug("Key = %s", key)
        if key == QUIT:
            logger.info("Quit key pressed.")
            break
    video_writer.release()
    cap.release()


if __name__ == "__main__":
    main()
