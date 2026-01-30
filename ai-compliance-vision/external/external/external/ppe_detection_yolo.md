# PPE_detection_YOLO

This document describes the external open-source project **PPE_detection_YOLO**.

## Overview

PPE_detection_YOLO is an object detection model trained with YOLO to identify personal protective equipment (PPE) and common site objects. It can detect classes such as **Hardhat**, **Mask**, **NO-Hardhat**, **NO-Mask**, **NO-Safety Vest**, **Person**, **Safety Cone**, **Safety Vest**, **machinery** and **vehicle**. The project includes a dataset of approximately 2.6k images and a Flask web application that allows uploading photos or videos for inference.

## License

This project is released under the MIT license, allowing free use, modification and distribution.

## How to Use

To use this model in your AI compliance workflow:

1. Clone the repository to your machine:

   ```bash
   git clone https://github.com/vinayakmane31/PPE_detection_YOLO.git
   ```

2. Install the required dependencies and download the pretrained weights as described in the project’s README.
3. Run the provided inference script or integrate the model weights into your own detection pipeline.
4. Fine-tune or expand the class set by labelling additional images if you need to detect other types of PPE or equipment.

For more details, refer to the [PPE_detection_YOLO repository](https://github.com/vinayakmane31/PPE_detection_YOLO).
