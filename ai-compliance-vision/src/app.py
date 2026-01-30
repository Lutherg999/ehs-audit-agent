"""Flask application for uploading or capturing images and running hazard detection.

The `/` route serves a simple HTML page allowing users to upload a photo or
capture one from a webcam.  Upon submission, the server processes the image
through a YOLO model and maps detections to potential regulatory violations.

Returns a JSON report of violations and detection details.

Note: For security reasons the webcam capture will only work on systems that
have a camera accessible via OpenCV and may require appropriate browser
permissions.  When running on a server without a camera the capture endpoint
will return an error.
"""

from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Any, Dict, List

import cv2  # type: ignore
import numpy as np  # type: ignore
from flask import Flask, render_template_string, request, jsonify

from .detect import load_model, detect_image
from .violation_engine import ViolationEngine


def create_app(weights_path: str = None, standards_dir: str = None) -> Flask:
    """Factory to create and configure the Flask app.

    This function loads the primary YOLO model from ``weights_path`` and
    optionally loads additional models for PPE or safety detection if
    corresponding weight files are present in the ``models/`` directory.
    """
    app = Flask(__name__)

    # Determine default paths
    base_dir = Path(__file__).resolve().parent.parent
    models_dir = base_dir / "models"
    if weights_path is None:
        # Use first file in models directory if available
        weights_candidates = list(models_dir.glob("*.pt"))
        if not weights_candidates:
            raise FileNotFoundError(
                "No model weights found in 'models/'. Please provide a weights file."
            )
        weights_path = str(weights_candidates[0])
    if standards_dir is None:
        standards_dir = str(base_dir / "standards")

    # Load base model
    base_model = load_model(str(weights_path))

    # Discover optional external model weights
    extra_weights = []
    for name in [
        "safety-detection-yolov8.pt",
        "ppe_detection_yolo.pt",
        "ppe_detection-yolov8.pt",
    ]:
        candidate = models_dir / name
        if candidate.exists():
            extra_weights.append(str(candidate))

    # Load all models (base + external)
    models: List[Any]
    if extra_weights:
        models = [base_model] + [load_model(w) for w in extra_weights]
    else:
        models = [base_model]

    engine = ViolationEngine(standards_dir)

    # Simple HTML page
    PAGE_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Compliance Vision</title>
        <style>
            body { font-family: sans-serif; margin: 2rem; }
            .container { max-width: 600px; margin: auto; }
            input[type=file] { display: block; margin-bottom: 1rem; }
            button { padding: 0.5rem 1rem; margin-top: 0.5rem; }
            pre { background: #f5f5f5; padding: 1rem; overflow-x: auto; }
        </style>
    </head>
    <body>
    <div class="container">
        <h1>AI Compliance Vision</h1>
        <p>Upload an image or capture a photo to detect potential safety and compliance issues.</p>
        <form id="upload-form" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" />
            <button type="submit">Upload Image</button>
        </form>
        <button id="capture-button">Capture Photo</button>
        <h2>Result</h2>
        <pre id="result"></pre>
    </div>
    <script>
        // Upload image via AJAX
        document.getElementById('upload-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const data = await res.json();
            document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        });
        // Capture photo from webcam and submit
        document.getElementById('capture-button').addEventListener('click', async () => {
            const res = await fetch('/capture', { method: 'POST' });
            const data = await res.json();
            document.getElementById('result').textContent = JSON.stringify(data, null, 2);
        });
    </script>
    </body>
    </html>
    """

    @app.route("/")
    def index() -> Any:
        return render_template_string(PAGE_TEMPLATE)

    @app.route("/upload", methods=["POST"])
    def upload() -> Any:
        file = request.files.get("image")
        if not file:
            return jsonify({"error": "No file provided."}), 400
        # Read file into a numpy array
        in_memory = file.read()
        file_bytes = np.frombuffer(in_memory, dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({"error": "Failed to decode image."}), 400
        detections = detect_image(models, img)
        violations = engine.evaluate(detections)
        return jsonify({"detections": detections, "violations": violations})

    @app.route("/capture", methods=["POST"])
    def capture() -> Any:
        # Attempt to open default camera
        cap = cv2.VideoCapture(0)
        if not cap or not cap.isOpened():
            return jsonify({"error": "Unable to access camera."}), 500
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return jsonify({"error": "Failed to capture frame."}), 500
        detections = detect_image(models, frame)
        violations = engine.evaluate(detections)
        return jsonify({"detections": detections, "violations": violations})

    return app


if __name__ == "__main__":  # pragma: no cover
    weights = os.environ.get("YOLO_WEIGHTS")  # optional environment override
    standards = os.environ.get("STANDARDS_DIR")
    app = create_app(weights, standards)
    app.run(debug=True)
