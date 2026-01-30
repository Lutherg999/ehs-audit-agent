# Labeling Guide

This guide outlines recommended practices for labeling images in support of the AI‑Compliance‑Vision model.  Accurate and consistent annotations are critical for high‑quality training data.

## Classes

The model uses the following classes (in order):

- `person`: Any human subject in the frame.  Required for proximity logic and general situational awareness.
- `forklift`: Powered industrial trucks and similar vehicles.
- `hardhat_missing`: A person whose head is uncovered in an area where hard hats are required.
- `hi_vis_missing`: A person not wearing a high‑visibility vest where required.
- `safety_glasses_missing`: A person without eye protection where required.
- `ungaurded_machine`: Machinery lacking required guarding (e.g. exposed moving parts on a conveyor).
- `blocked_exit`: An exit door or path blocked by equipment, materials, or other obstructions.
- `ladder_unsafe`: Unsafe ladder usage, such as steep angles, damaged ladders, or overreaching.
- `spill`: Spilled liquids, especially oil or chemicals.
- `no_guardrail`: Elevated platforms, walkways, or edges without guardrails.

## Annotation Tool

You may use any annotation tool that exports the **YOLO format**.  Popular choices include:

- [Roboflow](https://roboflow.com/)
- [CVAT](https://github.com/openvinotoolkit/cvat)
- [Label Studio](https://labelstud.io/)

Ensure the exported `data.yaml` reflects the class order above.
