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


def _get_scored_history(history: list[dict]) -> list[tuple[int, float]]:
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
    scored.sort(key=lambda x: x[0])
    return scored


def _get_best_score(best: dict | None) -> float | None:
    if not best or "final_score" not in best:
        return None
    try:
        return float(best.get("final_score", 0.0))
    except Exception:
        return None


def _stagnation_info(scored: list[tuple[int, float]], best_score: float, min_delta: float) -> tuple[int, int | None]:
    last_best_idx: int | None = None
    for i, (_, s) in enumerate(scored):
        if s >= best_score - min_delta:
            last_best_idx = i
    if last_best_idx is None:
        return 0, None
    stagnation_count = (len(scored) - 1) - last_best_idx
    last_best_candidate_num = scored[last_best_idx][0]
    return int(stagnation_count), int(last_best_candidate_num)


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
    scored = _get_scored_history(history)
    best_score = _get_best_score(best)
    if best_score is None or not scored:
        return None

    try:
        min_delta = float(os.environ.get("EVOLVER_BRAINSTORM_MIN_DELTA", "1e-12"))
    except Exception:
        min_delta = 1e-12

    stagnation_count, last_best_candidate_num = _stagnation_info(scored, best_score=best_score, min_delta=min_delta)

    try:
        exploit_window = int(os.environ.get("EVOLVER_EXPLOIT_WINDOW", "5"))
    except Exception:
        exploit_window = 5
    exploit_window = max(1, exploit_window)

    try:
        explore_window = int(os.environ.get("EVOLVER_EXPLORE_WINDOW", "10"))
    except Exception:
        explore_window = 10
    explore_window = max(1, explore_window)

    try:
        restart_window = int(os.environ.get("EVOLVER_RESTART_WINDOW", "30"))
    except Exception:
        restart_window = 30
    restart_window = max(explore_window, restart_window)

    explore_period = _explore_every(int(candidate_num))

    if stagnation_count >= restart_window and stagnation_count % restart_window == 0 and os.environ.get("EVOLVER_BRAINSTORM_ENABLED", "1") == "1":
        lvl = max(1, stagnation_count // restart_window)
        extra = f"""
## Restart Mode (Strong Exploration)
Best score has not improved for {stagnation_count} evaluated candidates (last best: candidate_{last_best_candidate_num}).

Override: ignore the earlier "one targeted edit max" constraint for this candidate.

You MUST choose a different algorithm family than the recent attempts. This is not a hyperparameter tweak round.
Restart Level: {lvl}

Choose exactly ONE direction:
- Switch objective: regression -> pairwise ranking / listwise ranking / quantile
- Switch model family: linear -> tree/boosting -> kernel -> (small) neural -> calibrated classifier
- Add explicit exploration component (if applicable): uncertainty/diversity/ensemble
"""
        return PromptMode(name="restart", extra_instructions=extra)

    if stagnation_count >= explore_window and stagnation_count % explore_window == 0 and os.environ.get("EVOLVER_BRAINSTORM_ENABLED", "1") == "1":
        lvl = max(1, stagnation_count // explore_window)
        extra = f"""
## Explore Mode (Adaptive)
Best score has not improved for {stagnation_count} evaluated candidates (last best: candidate_{last_best_candidate_num}).
Explore Level: {lvl}

You MUST switch to a different algorithm family than your most recent attempts (not a minor hyperparameter tweak).
If you change the objective, ensure evaluation compatibility.
"""
        return PromptMode(name="explore", extra_instructions=extra)

    if explore_period > 0:
        extra = f"""
## Explore Mode (Scheduled)
This is a scheduled exploration round (every {explore_period} candidates).

Try a meaningfully different approach than the recent candidates (not a minor hyperparameter tweak).
Prefer switching model family or objective.
"""
        return PromptMode(name="explore", extra_instructions=extra)

    if stagnation_count <= exploit_window:
        extra = f"""
## Exploit Mode (Conservative)
Recent best was updated within the last {exploit_window} evaluated candidates.

Prefer a small, low-risk improvement over a large rewrite:
- calibration, normalization, regularization, stable training
- avoid adding new heavy dependencies unless clearly justified
"""
        return PromptMode(name="exploit", extra_instructions=extra)

    return None
