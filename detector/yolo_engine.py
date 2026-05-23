import os
from functools import lru_cache
from pathlib import Path

import cv2
from django.conf import settings
from ultralytics import YOLO


DEFAULT_MODEL = getattr(settings, "NEWEST_YOLO_MODEL", os.getenv("YOLO_MODEL", "yolo26n.pt"))
FALLBACK_MODELS = ["yolo26n.pt", "yolo11n.pt", "yolov8n.pt"]


@lru_cache(maxsize=4)
def load_yolo_model(model_name: str | None = None):
    """Load an Ultralytics YOLO model once and reuse it for faster requests."""
    selected_model = model_name or DEFAULT_MODEL
    candidates = [selected_model] + [m for m in FALLBACK_MODELS if m != selected_model]
    last_error = None

    for candidate in candidates:
        try:
            return YOLO(candidate)
        except Exception as exc:  # fallback keeps the project runnable on older ultralytics releases
            last_error = exc

    raise RuntimeError(f"Could not load any YOLO model. Last error: {last_error}")


def result_to_detections(result):
    """Convert one Ultralytics Result object to template-friendly dictionaries."""
    detections = []
    names = result.names or {}

    if result.boxes is None:
        return detections

    for box in result.boxes:
        xyxy = box.xyxy[0].tolist()
        cls_id = int(box.cls[0].item()) if box.cls is not None else -1
        conf = float(box.conf[0].item()) if box.conf is not None else 0.0
        detections.append({
            "name": names.get(cls_id, str(cls_id)),
            "confidence": conf,
            "xmin": xyxy[0],
            "ymin": xyxy[1],
            "xmax": xyxy[2],
            "ymax": xyxy[3],
            "class": cls_id,
        })

    return detections


def save_plotted_result(result, output_path):
    """Save YOLO annotated result image to disk."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plotted_bgr = result.plot()
    cv2.imwrite(str(output_path), plotted_bgr)
