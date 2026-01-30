# AI‑Compliance‑Vision

An end‑to‑end example repository for building an AI‑powered hazard recognition system that helps identify potential OSHA, EPA, NFPA and ANSI compliance issues from images or video frames.  

This repository demonstrates how to structure training code, inference scripts and a simple web interface for uploading photos or capturing frames from a camera.  All detections are mapped to relevant regulatory citations via a rule engine.

## Features

* **Fine‑tune a YOLO model** for PPE compliance, housekeeping and environmental hazards.
* **Upload or capture images** through a Flask web app to run inference on demand.
* **Rule engine** maps detection conditions to standards (OSHA, EPA, NFPA, ANSI) defined in JSON.
* **Human‑readable reports** summarise potential violations along with confidence scores and citations.

## Directory Structure

```
ai-compliance-vision/
|
├── README.md
├── requirements.txt
├── models/               # exported YOLO weights (not provided)
├── data/                 # placeholder for your dataset
│   └── .gitkeep
├── src/
│   ├── detect.py         # detection wrapper around YOLO
│   ├── hazard_conditions.py  # class list and helper functions
│   ├── violation_engine.py   # maps detections to standards
│   ├── app.py            # Flask app for uploads and camera capture
│   └── utils.py          # shared utilities
├── standards/
│   ├── osha.json
│   ├── epa.json
│   ├── nfpa.json
│   └── ansi.json
├── docs/
│   ├── labeling_guide.md
│   ├── violation_mapping.md
│   └── legal_disclaimer.md
└── examples/
    └── output_report.json
```

## Quick Start

1.  **Install dependencies**.  Create a virtual environment and install the packages:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Download or train a model**.  Place your YOLO weights (`yolov8n.pt`, etc.) in the `models/` directory.  See `src/detect.py` for details on how the model is loaded.

3.  **Start the web app**.

    ```bash
    python -m src.app
    ```

    By default the app runs on `http://localhost:5000`.  You can upload images from your computer or capture a frame from an attached webcam and receive a JSON report of potential violations.

## Disclaimer

This project is intended for educational purposes and is **not** a replacement for professional safety inspections.  AI detections may be incomplete or inaccurate and all reported violations should be reviewed by a qualified safety professional.
