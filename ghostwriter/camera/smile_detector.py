from __future__ import print_function
import cv2 as cv
import argparse

from ghostwriter.paths import DATA_DIR


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
        smiles = smile_cascade.detectMultiScale(faceROI, 1.8,  20)

        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)

        for (x2, y2, w2, h2) in smiles:
            pt1 = (x+x2, y+y2)
            pt2 = (x+x2+w2, y+y2+h2)
            print(pt1, pt2)
            frame = cv.rectangle(frame, pt1, pt2, color=(255, 255, 0))

    cv.imshow("Capture - Face detection", frame)


if __name__ == "__main__":
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
    parser.add_argument("--camera", help="Camera divide number.", type=int, default=0)
    args = parser.parse_args()
    face_cascade_name = args.face_cascade
    eyes_cascade_name = args.eyes_cascade
    smile_cascade_name = args.smile_cascade

    face_cascade = cv.CascadeClassifier()
    eyes_cascade = cv.CascadeClassifier()
    smile_cascade = cv.CascadeClassifier()
    # -- 1. Load the cascades
    if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
        print("--(!)Error loading face cascade")
        exit(0)
    if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
        print("--(!)Error loading eyes cascade")
        exit(0)
    if not smile_cascade.load(cv.samples.findFile(smile_cascade_name)):
        print("--(!)Error loading smile cascade")
        exit(0)

    camera_device = args.camera
    # -- 2. Read the video stream
    cap = cv.VideoCapture(camera_device)
    if not cap.isOpened:
        print("--(!)Error opening video capture")
        exit(0)
    while True:
        ret, frame = cap.read()
        if frame is None:
            print("--(!) No captured frame -- Break!")
            break
        detect_and_display(
            frame,
            face_cascade=face_cascade,
            eyes_cascade=eyes_cascade,
            smile_cascade=smile_cascade,
        )
        if cv.waitKey(30) == 27:
            break
