"""Detection wrapper for YOLO models.

This module provides helper functions to load a YOLO model and run detection on
images.  It returns a list of detection dictionaries that can be passed into
the violation engine to map conditions to potential regulatory citations.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Sequence, Union

import cv2  # type: ignore
import numpy as np  # type: ignore
from ultralytics import YOLO  # type: ignore

from .hazard_conditions import CLASS_NAMES, CLASS_CONDITIONS

_model_cache: Dict[str, YOLO] = {}


def load_model(weights_path: str) -> YOLO:
    """Load a YOLO model from the given weights file.

    Models are cached in `_model_cache` so repeated calls with the same path
    will not reload weights from disk.

    Args:
        weights_path: Path to the YOLO weights file.

    Returns:
        A loaded YOLO model.
    """
    global _model_cache
    weights_path = str(Path(weights_path).resolve())
    if weights_path not in _model_cache:
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Weights file '{weights_path}' not found.")
        _model_cache[weights_path] = YOLO(weights_path)
    return _model_cache[weights_path]


def prepare_image(image: np.ndarray, max_size: int = 1024) -> np.ndarray:
    """Resize image while preserving aspect ratio.

    Args:
        image: Input BGR image as a numpy array.
        max_size: Maximum side length for the resized image.

    Returns:
        Resized image.
    """
    h, w = image.shape[:2]
    scale = min(max_size / max(h, w), 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    return resized


def detect_image(model: Union[YOLO, Sequence[YOLO]], image: np.ndarray, conf_threshold: float = 0.25) -> List[Dict[str, Any]]:
    """Run object detection on an image and return hazard conditions.

    This function can accept a single YOLO model or a sequence of models.  If a
    sequence is provided, detections from all models are aggregated.  Unknown
    classes not present in `CLASS_NAMES` are mapped to their original
    class names as conditions.

    Args:
        model: A loaded YOLO model or a sequence of YOLO models.
        image: BGR image as a numpy array.
        conf_threshold: Confidence threshold to filter detections.

    Returns:
        A list of detection dictionaries containing bounding box coordinates,
        class name, confidence score and underlying hazard condition.
    """
    # If multiple models are provided, aggregate detections from each
    if isinstance(model, Sequence) and not isinstance(model, YOLO):
        all_detections: List[Dict[str, Any]] = []
        for m in model:
            all_detections.extend(detect_image(m, image, conf_threshold))
        return all_detections

    # Single model inference
    prepared = prepare_image(image)
    results = model.predict(source=prepared, verbose=False)
    detections: List[Dict[str, Any]] = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls.item())
            score = float(box.conf.item())
            if score < conf_threshold:
                continue
            if 0 <= cls_id < len(CLASS_NAMES):
                class_name = CLASS_NAMES[cls_id]
                condition = CLASS_CONDITIONS.get(class_name, class_name)
            else:
                # For classes outside our known list, use the raw class id
                # returned by the model.  YOLO stores class names in
                # result.names if available.
                if hasattr(result, "names"):
                    class_name = result.names.get(cls_id, str(cls_id))  # type: ignore
                else:
                    class_name = str(cls_id)
                condition = class_name
            # Extract bounding box coordinates relative to original image size
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            h_ratio = image.shape[0] / prepared.shape[0]
            w_ratio = image.shape[1] / prepared.shape[1]
            orig_x1 = x1 * w_ratio
            orig_y1 = y1 * h_ratio
            orig_x2 = x2 * w_ratio
            orig_y2 = y2 * h_ratio
            detections.append({
                "class_name": class_name,
                "condition": condition,
                "confidence": score,
                "bbox": [orig_x1, orig_y1, orig_x2, orig_y2],
            })
    return detections


def draw_detections(image: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
    """Draw bounding boxes and labels on the image for visualisation.

    Args:
        image: BGR image array.  This array will not be modified; a copy
            is made internally.
        detections: List of detection dictionaries as returned by
            `detect_image`.

    Returns:
        A new image array with bounding boxes and labels drawn.
    """
    draw = image.copy()
    for det in detections:
        x1, y1, x2, y2 = [int(coord) for coord in det["bbox"]]
        label = f"{det['class_name']} {det['confidence']:.2f}"
        # Draw box
        cv2.rectangle(draw, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        # Draw label background
        (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(draw, (x1, y1 - text_h - baseline), (x1 + text_w, y1), color=(0, 255, 0), thickness=-1)
        cv2.putText(draw, label, (x1, y1 - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return draw
