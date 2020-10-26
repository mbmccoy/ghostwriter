import cv2 as cv
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This program shows how to use "
                    "background subtraction methods provided by" 
                    "OpenCV. You can process both videos and images."
    )
    args = parser.parse_args()
    backSub = cv.createBackgroundSubtractorMOG2()
    capture = cv.VideoCapture(0)
    if not capture.isOpened:
        print("Unable to open camera")
        exit(0)
    while True:
        ret, frame = capture.read()
        if frame is None:
            break

        fgMask = backSub.apply(frame)

        cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
        cv.putText(
            frame,
            str(capture.get(cv.CAP_PROP_POS_FRAMES)),
            (15, 15),
            cv.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
        )

        cv.imshow("Frame", frame)
        cv.imshow("FG Mask", fgMask)

        keyboard = cv.waitKey(30)
        if keyboard == "q" or keyboard == 27:
            break
