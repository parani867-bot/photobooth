import cv2
import time
import os
from datetime import datetime
import config

def capture_single_photo(mode):
    os.makedirs(config.PHOTOS_DIR, exist_ok=True)

    cam = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)
    time.sleep(1)

    if not cam.isOpened():
        print("Camera not opened")
        return None

    for sec in range(config.COUNTDOWN_SECONDS, 0, -1):
        ret, frame = cam.read()
        if not ret:
            continue

        cv2.putText(
            frame,
            str(sec),
            (frame.shape[1]//2 - 40, frame.shape[0]//2),
            cv2.FONT_HERSHEY_SIMPLEX,
            4,
            (0, 0, 255),
            8
        )
        cv2.imshow("Photo Booth", frame)
        cv2.waitKey(1000)

    ret, frame = cam.read()
    cam.release()
    cv2.destroyAllWindows()

    if not ret:
        return None

    if mode == "BW":
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    filename = os.path.join(
        config.PHOTOS_DIR,
        f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    )
    cv2.imwrite(filename, frame)
    return filename


def capture_photos(mode, count):
    photos = []
    for _ in range(count):
        photo = capture_single_photo(mode)
        if photo:
            photos.append(photo)
    return photos
