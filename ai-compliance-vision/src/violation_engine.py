"""Violation engine mapping detections to potential regulatory citations.

This module reads standard definitions from JSON files under the `standards`
directory and provides a function to evaluate detections.  It returns a list
of potential violations with references to the standard, citation and
description.

The engine also includes simple logic for compound conditions such as
proximity between persons and forklifts (a potential struck‑by hazard).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np  # type: ignore


class ViolationEngine:
    """Load standard mappings and evaluate detections."""

    def __init__(self, standards_dir: str) -> None:
        self.standards: Dict[str, Dict[str, Any]] = {}
        self._load_standards(Path(standards_dir))

    def _load_standards(self, directory: Path) -> None:
        for json_file in directory.glob("*.json"):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Store mapping keyed by standard name (filename without ext)
            standard_name = json_file.stem.lower()
            self.standards[standard_name] = data

    def _lookup_condition(self, condition: str) -> List[Dict[str, Any]]:
        """Return all standard entries matching the given condition."""
        matches: List[Dict[str, Any]] = []
        for std_name, mapping in self.standards.items():
            for citation, entry in mapping.items():
                # Each entry must contain `condition` and `description`
                if entry.get("condition") == condition:
                    matches.append({
                        "standard": std_name.upper(),
                        "citation": citation,
                        "description": entry.get("description", ""),
                        "severity": entry.get("severity", ""),
                    })
        return matches

    @staticmethod
    def _bbox_center(bbox: List[float]) -> Tuple[float, float]:
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    @staticmethod
    def _euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        return float(np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))

    def evaluate(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Evaluate a list of detections and return potential violations.

        Args:
            detections: List of detection dictionaries as returned by the
                detection module.

        Returns:
            List of violation dictionaries.  Each violation dictionary
            contains keys: `standard`, `citation`, `description`,
            `confidence` and optionally `evidence` or other metadata.
        """
        violations: List[Dict[str, Any]] = []

        # Evaluate individual detections
        for det in detections:
            condition = det["condition"]
            matches = self._lookup_condition(condition)
            for match in matches:
                violations.append({
                    **match,
                    "confidence": det["confidence"],
                    "evidence": {
                        "bbox": det["bbox"],
                        "class_name": det["class_name"],
                    },
                })

        # Evaluate proximity between person and forklift
        persons = [d for d in detections if d["condition"] == "person"]
        forklifts = [d for d in detections if d["condition"] == "forklift"]
        if persons and forklifts:
            # Compute distances and check for close proximity
            for person in persons:
                p_center = self._bbox_center(person["bbox"])
                for forklift in forklifts:
                    f_center = self._bbox_center(forklift["bbox"])
                    distance = self._euclidean_distance(p_center, f_center)
                    # Use a simple threshold; you might tune this based on
                    # camera resolution and physical scale
                    threshold = 200.0
                    if distance < threshold:
                        # Create a synthetic condition
                        condition = "forklift_pedestrian_proximity"
                        matches = self._lookup_condition(condition)
                        for match in matches:
                            # The confidence for proximity is the minimum
                            # confidence of the two contributing detections
                            confidence = min(person["confidence"], forklift["confidence"])
                            violations.append({
                                **match,
                                "confidence": confidence,
                                "evidence": {
                                    "person_bbox": person["bbox"],
                                    "forklift_bbox": forklift["bbox"],
                                },
                            })

        return violations
