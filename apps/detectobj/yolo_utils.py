from functools import lru_cache
from pathlib import Path

import cv2
from django.conf import settings
from ultralytics import YOLO


@lru_cache(maxsize=8)
def load_model(model_path_or_name=None):
    model_name = model_path_or_name or getattr(settings, "NEWEST_YOLO_MODEL", "yolo26n.pt")
    candidates = [model_name]
    if model_name == getattr(settings, "NEWEST_YOLO_MODEL", "yolo26n.pt"):
        candidates += ["yolo11n.pt", "yolov8n.pt"]
    last_error = None
    for candidate in candidates:
        try:
            return YOLO(candidate)
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not load YOLO model. Last error: {last_error}")


def result_to_records(result):
    records = []
    names = result.names or {}
    if result.boxes is None:
        return records
    for box in result.boxes:
        xmin, ymin, xmax, ymax = box.xyxy[0].tolist()
        class_id = int(box.cls[0].item()) if box.cls is not None else -1
        confidence = float(box.conf[0].item()) if box.conf is not None else 0.0
        records.append({
            "xmin": xmin,
            "ymin": ymin,
            "xmax": xmax,
            "ymax": ymax,
            "confidence": confidence,
            "class": class_id,
            "name": names.get(class_id, str(class_id)),
        })
    return records


def save_result_image(result, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), result.plot())
