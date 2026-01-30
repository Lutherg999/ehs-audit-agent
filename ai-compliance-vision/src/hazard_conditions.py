"""Defines the class names and hazard conditions.

The class list determines the order of labels expected by the YOLO model.
The `CLASS_CONDITIONS` mapping provides a more human‑readable description
that is passed to the violation engine to look up applicable standards.
"""

from __future__ import annotations

from typing import Dict

# This list should match the order of classes used during training.  If you
# modify the class list, update your dataset's `data.yaml` accordingly.
CLASS_NAMES = [
    "person",
    "forklift",
    "hardhat_missing",
    "hi_vis_missing",
    "safety_glasses_missing",
    "ungaurded_machine",
    "blocked_exit",
    "ladder_unsafe",
    "spill",
    "no_guardrail",
]

# Map model class names to hazard conditions.  In most cases the condition
# matches the class name, but you could group similar conditions under a
# common name (e.g. multiple PPE violations mapping to `ppe_violation`).
CLASS_CONDITIONS: Dict[str, str] = {
    "hardhat_missing": "hardhat_missing",
    "hi_vis_missing": "hi_vis_missing",
    "safety_glasses_missing": "safety_glasses_missing",
    "ungaurded_machine": "unguarded_machine",
    "blocked_exit": "blocked_exit",
    "ladder_unsafe": "ladder_unsafe",
    "spill": "spill",
    "no_guardrail": "no_guardrail",
    # person and forklift are not violations themselves but are needed for
    # proximity logic in the rule engine.
    "person": "person",
    "forklift": "forklift",
}

if __name__ == "__main__":  # pragma: no cover
    # Simple sanity check when running this module directly
    for idx, name in enumerate(CLASS_NAMES):
        cond = CLASS_CONDITIONS.get(name, name)
        print(f"{idx}: {name} -> {cond}")
