from __future__ import annotations

import numpy as np


def _is_number(x: object) -> bool:
    return isinstance(x, (int, float, np.floating, np.integer)) and bool(np.isfinite(float(x)))


def _numeric_keys_from_rows(rows: list[dict[str, object]]) -> list[str]:
    drop = {"label", "candidate_index"}
    keys: set[str] = set()
    for r in rows[:200]:
        for k, v in r.items():
            if k in drop:
                continue
            if _is_number(v):
                keys.add(k)
    return sorted(keys)


def _rows_to_matrix(rows: list[dict[str, object]], keys: list[str]) -> np.ndarray:
    if not rows or not keys:
        return np.zeros((len(rows), 0), dtype=np.float32)
    X = np.zeros((len(rows), len(keys)), dtype=np.float32)
    for i, r in enumerate(rows):
        for j, k in enumerate(keys):
            v = r.get(k, 0.0)
            if _is_number(v):
                X[i, j] = float(v)
            else:
                X[i, j] = 0.0
    return X


def _fit_ridge(X: np.ndarray, y: np.ndarray, l2: float) -> np.ndarray:
    if X.size == 0:
        return np.zeros((0,), dtype=np.float32)
    X = X.astype(np.float32, copy=False)
    y = y.astype(np.float32, copy=False).reshape(-1, 1)
    XtX = X.T @ X
    XtX.flat[:: XtX.shape[0] + 1] += float(l2)
    Xty = X.T @ y
    w = np.linalg.solve(XtX, Xty).reshape(-1)
    return w.astype(np.float32, copy=False)


def select(
    candidates: list[dict[str, object]],
    history: list[dict[str, object]],
    batch_size: int,
    seed: int,
) -> list[int]:
    rng = np.random.default_rng(int(seed))
    n = int(len(candidates))
    if n == 0 or int(batch_size) <= 0:
        return []

    already: set[int] = set()
    for r in history:
        v = r.get("candidate_index", None)
        if v is None:
            continue
        try:
            already.add(int(v))
        except Exception:
            continue

    available = [i for i in range(n) if i not in already]
    if not available:
        return []
    if len(available) <= int(batch_size):
        return [int(i) for i in available]

    if not history:
        return [int(i) for i in rng.choice(np.asarray(available, dtype=np.int64), size=int(batch_size), replace=False)]

    y_hist_list: list[float] = []
    hist_rows: list[dict[str, object]] = []
    for r in history:
        if "label" not in r:
            continue
        try:
            y_hist_list.append(float(r["label"]))
        except Exception:
            continue
        hist_rows.append(r)

    if len(hist_rows) < 5:
        return [int(i) for i in rng.choice(np.asarray(available, dtype=np.int64), size=int(batch_size), replace=False)]

    y_hist = np.asarray(y_hist_list, dtype=np.float32).reshape(-1)
    if float(y_hist.min()) == float(y_hist.max()):
        return [int(i) for i in rng.choice(np.asarray(available, dtype=np.int64), size=int(batch_size), replace=False)]

    keys = _numeric_keys_from_rows(hist_rows)
    if not keys:
        return [int(i) for i in rng.choice(np.asarray(available, dtype=np.int64), size=int(batch_size), replace=False)]

    X_hist = _rows_to_matrix(hist_rows, keys)
    mu = X_hist.mean(axis=0, keepdims=True)
    sigma = X_hist.std(axis=0, keepdims=True) + 1e-6
    X_hist_z = (X_hist - mu) / sigma
    w = _fit_ridge(X_hist_z, y_hist, l2=1.0)

    X_all = _rows_to_matrix(candidates, keys)
    X_all_z = (X_all - mu) / sigma
    scores = (X_all_z @ w).reshape(-1)

    explore_n = max(0, int(round(float(batch_size) * 0.2)))
    exploit_n = int(batch_size) - explore_n

    avail_arr = np.asarray(available, dtype=np.int64)
    score_avail = scores[avail_arr]
    order = np.argsort(-score_avail, kind="mergesort")
    top = avail_arr[order[:exploit_n]].tolist()

    picked = set(int(i) for i in top)
    if explore_n > 0:
        rest = [int(i) for i in available if int(i) not in picked]
        if rest:
            extra = rng.choice(np.asarray(rest, dtype=np.int64), size=min(explore_n, len(rest)), replace=False).tolist()
            top.extend(int(i) for i in extra)

    return [int(i) for i in top]
