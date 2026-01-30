"""Utility functions for the AI Compliance Vision project.

Currently includes helper functions to format detection outputs into a
report‑friendly structure.  Additional utilities can be added as the
project evolves.
"""

from __future__ import annotations

from typing import List, Dict, Any


def summarise_violations(violations: List[Dict[str, Any]]) -> str:
    """Return a human‑readable summary string for a list of violations."""
    if not violations:
        return "No potential violations detected."
    lines = []
    for v in violations:
        lines.append(
            f"{v['standard']} {v['citation']}: {v['description']} (confidence {v['confidence']:.2f})"
        )
    return "\n".join(lines)
