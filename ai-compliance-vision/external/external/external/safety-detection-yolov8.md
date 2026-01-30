# Safety-Detection-YOLOv8

This document describes the external open-source project **Safety-Detection-YOLOv8**.

## Overview

Safety-Detection-YOLOv8 is a YOLOv8-based model that identifies various safety-related objects such as hard hats, masks, safety vests and more. It performs real-time object detection and can classify each detection as compliant or non-compliant, making it well suited for PPE compliance monitoring. The project’s design encourages adding new classes for additional types of hazards.

## License

The project is released under the MIT license, allowing free use, modification and distribution.

## How to Use

To include this model in your AI compliance system:

1. Clone the repository to a local directory:

   ```bash
   git clone https://github.com/BiswadeepRoy/Safety-Detection-YOLOv8.git
   ```

2. Follow the installation instructions in the project’s README to set up dependencies and download pretrained weights.
3. Use the provided detection script or integrate the YOLO weights into your own inference pipeline.
4. Extend the classes or retrain the model using your labelled data if additional hazards need to be detected.

For more details see the [Safety-Detection-YOLOv8 repository](https://github.com/BiswadeepRoy/Safety-Detection-YOLOv8).
