import threading

import cv2
from django.conf import settings

from .yolo_engine import load_yolo_model


class YOLOWebcam:
    def __init__(self):
        self.camera = None
        self.lock = threading.Lock()

    def open_camera(self):
        if self.camera is None or not self.camera.isOpened():
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not self.camera.isOpened():
                self.camera = cv2.VideoCapture(0)

            if not self.camera.isOpened():
                raise RuntimeError(
                    "Webcam could not be opened. Close other camera apps and check camera permission."
                )

            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        return self.camera

    def get_frame(self):
        with self.lock:
            camera = self.open_camera()
            success, frame = camera.read()
            if not success:
                return None

            model = load_yolo_model()
            results = model.predict(
                source=frame,
                conf=getattr(settings, "MODEL_CONFIDENCE", 0.45),
                imgsz=640,
                verbose=False,
            )
            detected_frame = results[0].plot()

            success, buffer = cv2.imencode('.jpg', detected_frame)
            if not success:
                return None

            return buffer.tobytes()


webcam = YOLOWebcam()


def generate_frames():
    while True:
        frame = webcam.get_frame()

        if frame is None:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )
