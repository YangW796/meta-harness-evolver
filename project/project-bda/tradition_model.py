from __future__ import annotations

import os
import random
from typing import Any

import numpy as np

import bda_tools


def _get_policy_name() -> str:
    name = str(os.environ.get("BDA_TRADITIONAL_POLICY", "random")).strip().lower()
    if not name:
        return "random"
    if name in {"rand", "uniform"}:
        return "random"
    if name in {"linear", "ridge", "linear_ridge"}:
        return "linear"
    return name


def _already_selected(history: list[dict[str, Any]]) -> set[int]:
    out: set[int] = set()
    for h in history or []:
        try:
            out.add(int(h.get("candidate_index")))
        except Exception:
            pass
    return out


def _random_select(n_candidates: int, already: set[int], batch_size: int, seed: int) -> list[int]:
    rng = random.Random(int(seed))
    pool = [i for i in range(int(n_candidates)) if i not in already]
    if not pool:
        return []
    if len(pool) <= int(batch_size):
        rng.shuffle(pool)
        return pool
    return rng.sample(pool, int(batch_size))


def _candidate_to_gene(cand: dict[str, Any]) -> str:
    if not isinstance(cand, dict):
        return ""
    if "gene" in cand:
        return str(cand.get("gene", "")).strip()
    if "gene_a" in cand:
        return str(cand.get("gene_a", "")).strip()
    return ""


def _linear_select(
    candidates: list[dict[str, Any]],
    history: list[dict[str, Any]],
    batch_size: int,
    seed: int,
) -> list[int]:
    already = _already_selected(history)
    if not history:
        return _random_select(len(candidates), already, batch_size, seed)

    feats = getattr(bda_tools, "_FEATS_SUB", None)
    sub_to_cand = getattr(bda_tools, "_SUB_TO_CAND_IDX", None)
    if feats is None or sub_to_cand is None:
        return _random_select(len(candidates), already, batch_size, seed)

    try:
        feats = np.asarray(feats, dtype=np.float32)
        sub_to_cand = [int(x) for x in list(sub_to_cand)]
    except Exception:
        return _random_select(len(candidates), already, batch_size, seed)

    cand_to_sub: dict[int, int] = {}
    for sub_i, cand_i in enumerate(sub_to_cand):
        if cand_i not in cand_to_sub:
            cand_to_sub[int(cand_i)] = int(sub_i)

    xs: list[np.ndarray] = []
    ys: list[float] = []
    use_hit = any(("hit" in (h or {})) for h in history)
    for h in history:
        try:
            cand_idx = int(h.get("candidate_index"))
        except Exception:
            continue
        sub_i = cand_to_sub.get(cand_idx)
        if sub_i is None:
            continue
        yv: float
        if use_hit:
            try:
                yv = float(h.get("hit", 0))
            except Exception:
                yv = 0.0
        else:
            try:
                yv = float(h.get("score", 0.0))
            except Exception:
                yv = 0.0
        xs.append(feats[int(sub_i)])
        ys.append(yv)

    if len(xs) < 8:
        return _random_select(len(candidates), already, batch_size, seed)

    x = np.stack(xs, axis=0).astype(np.float32, copy=False)
    y = np.asarray(ys, dtype=np.float32)
    y = y - float(np.mean(y))

    lam = float(os.environ.get("BDA_TRADITIONAL_RIDGE_LAMBDA", "1.0") or "1.0")
    lam = max(lam, 1e-6)

    xtx = x.T @ x
    xty = x.T @ y
    d = int(xtx.shape[0])
    xtx = xtx + (lam * np.eye(d, dtype=np.float32))
    try:
        w = np.linalg.solve(xtx, xty).astype(np.float32, copy=False)
    except Exception:
        return _random_select(len(candidates), already, batch_size, seed)

    pred = feats @ w
    order = np.argsort(pred)[::-1]

    chosen: list[int] = []
    for sub_i in order.tolist():
        cand_i = sub_to_cand[int(sub_i)]
        if cand_i in already:
            continue
        chosen.append(int(cand_i))
        if len(chosen) >= int(batch_size):
            break

    use_gene_search = str(os.environ.get("BDA_TRADITIONAL_USE_GENE_SEARCH", "1")).strip() == "1"
    if use_gene_search and chosen:
        anchors: list[str] = []
        for idx in chosen[: min(8, len(chosen))]:
            g = _candidate_to_gene(candidates[int(idx)])
            if g and g not in anchors:
                anchors.append(g)
        k = int(os.environ.get("BDA_TRADITIONAL_GENE_SEARCH_K", "30") or "30")
        expanded: list[int] = []
        for g in anchors:
            expanded.extend(bda_tools.gene_search(g, k=k, diverse=False))
        for idx in expanded:
            ii = int(idx)
            if ii in already:
                continue
            if ii in chosen:
                continue
            chosen.append(ii)
            if len(chosen) >= int(batch_size):
                break

    if len(chosen) < int(batch_size):
        chosen.extend(_random_select(len(candidates), already | set(chosen), int(batch_size) - len(chosen), seed))
    return chosen[: int(batch_size)]


def select(candidates, history, batch_size, seed) -> list[int]:
    policy = _get_policy_name()
    if policy == "random":
        already = _already_selected(history or [])
        return _random_select(len(candidates), already, int(batch_size), int(seed))
    if policy == "linear":
        return _linear_select(candidates, history or [], int(batch_size), int(seed))
    already = _already_selected(history or [])
    return _random_select(len(candidates), already, int(batch_size), int(seed))
