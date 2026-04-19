from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class PromptMode:
    name: str
    extra_instructions: str


def parse_candidate_num(name: str) -> int | None:
    if not name.startswith("candidate_"):
        return None
    try:
        return int(name.split("_", 1)[1])
    except Exception:
        return None


def detect_bottleneck(history: list[dict], best: dict | None) -> dict | None:
    enabled = os.environ.get("EVOLVER_BRAINSTORM_ENABLED", "1") == "1"
    if not enabled:
        return None
    try:
        window = int(os.environ.get("EVOLVER_BRAINSTORM_WINDOW", "10"))
    except Exception:
        window = 10
    window = max(1, window)
    try:
        min_delta = float(os.environ.get("EVOLVER_BRAINSTORM_MIN_DELTA", "1e-12"))
    except Exception:
        min_delta = 1e-12

    if not best or "final_score" not in best:
        return None
    try:
        best_score = float(best.get("final_score", 0.0))
    except Exception:
        return None

    scored: list[tuple[int, float]] = []
    for h in history:
        cand_name = str(h.get("candidate", ""))
        cand_num = parse_candidate_num(cand_name)
        if cand_num is None:
            continue
        scores = h.get("scores", {})
        if not isinstance(scores, dict):
            continue
        try:
            s = float(scores.get("final_score", -1e18))
        except Exception:
            continue
        scored.append((cand_num, s))

    if not scored:
        return None
    scored.sort(key=lambda x: x[0])

    last_best_idx: int | None = None
    for i, (_, s) in enumerate(scored):
        if s >= best_score - min_delta:
            last_best_idx = i
    if last_best_idx is None:
        return None

    stagnation_count = (len(scored) - 1) - last_best_idx
    if stagnation_count < window:
        return None
    if stagnation_count % window != 0:
        return None

    last_best_candidate_num = scored[last_best_idx][0]
    level = max(1, stagnation_count // window)
    return {
        "window": int(window),
        "stagnation_count": int(stagnation_count),
        "best_score": float(best_score),
        "last_best_candidate_num": int(last_best_candidate_num),
        "level": int(level),
    }


def _explore_every(candidate_num: int) -> int:
    try:
        v = int(os.environ.get("EVOLVER_EXPLORE_EVERY", "5"))
    except Exception:
        v = 5
    if v <= 0:
        return 0
    if candidate_num <= 0:
        return 0
    if candidate_num % v != 0:
        return 0
    return v


def choose_prompt_mode(history: list[dict], best: dict | None, candidate_num: int) -> PromptMode | None:
    bottleneck = detect_bottleneck(history, best)
    if bottleneck:
        lvl = int(bottleneck.get("level", 1))
        extra = f"""
## Bottleneck Detected (Brainstorm Mode)
Best score has not improved for {bottleneck['stagnation_count']} evaluated candidates (last best: candidate_{bottleneck['last_best_candidate_num']}).

Override: ignore the earlier \"one targeted edit max\" constraint for this candidate.

You are allowed to do a larger, more creative change. Prefer changes that are materially different from the last ~10 attempts.

Brainstorm Level: {lvl}
- Level 1: substantial rewrite within the most important allowed harness file
- Level 2+: new direction; if allowed by project rules, you may refactor across multiple harness files
"""
        return PromptMode(name="brainstorm", extra_instructions=extra)

    explore_period = _explore_every(int(candidate_num))
    if explore_period > 0:
        extra = f"""
## Explore Mode
This is a scheduled exploration round (every {explore_period} candidates).

Try a meaningfully different approach than the recent candidates (not a minor hyperparameter tweak).
If you can justify it from history, you may refactor the main allowed harness file to a different algorithmic strategy.
"""
        return PromptMode(name="explore", extra_instructions=extra)

    return None

