"""Utilities for converting predicted utilities back to raw metrics."""

from __future__ import annotations

import json
from pathlib import Path


def load_normalization(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def inverse_utility(metric_name: str, utility: float, normalization: dict) -> float:
    spec = normalization["metrics"][metric_name]
    min_value = float(spec["min_value"])
    max_value = float(spec["max_value"])
    utility = max(0.0, min(1.0, float(utility)))
    if spec["direction"] == "higher":
        return min_value + utility * (max_value - min_value)
    if spec["direction"] == "lower":
        return max_value - utility * (max_value - min_value)
    raise ValueError(f"Unknown direction for {metric_name}: {spec['direction']}")


def inverse_utility_vector(
    utilities: list[float],
    metric_names: list[str],
    normalization: dict,
) -> dict[str, float]:
    return {
        name: inverse_utility(name, value, normalization)
        for name, value in zip(metric_names, utilities, strict=True)
    }

