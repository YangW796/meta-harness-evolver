#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

import numpy as np


def _parse_cell(v: str) -> object:
    s = (v or "").strip()
    if s == "":
        return ""
    try:
        x = float(s)
    except Exception:
        return s
    if not np.isfinite(x):
        return 0.0
    return x


def _read_rows(path: str) -> tuple[list[str], list[dict[str, object]]]:
    p = Path(path).expanduser().resolve()
    with p.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV missing header: {p}")
        fieldnames = list(reader.fieldnames)
        rows: list[dict[str, object]] = []
        for r in reader:
            row: dict[str, object] = {}
            for k in fieldnames:
                row[k] = _parse_cell(r.get(k, ""))
            rows.append(row)
    return fieldnames, rows


def _write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})


def _as_float_array(values: list[object]) -> np.ndarray:
    out = np.asarray(values, dtype=np.float64).reshape(-1)
    out[~np.isfinite(out)] = 0.0
    return out


def _get_column(rows: list[dict[str, object]], key: str) -> np.ndarray | None:
    if not rows:
        return _as_float_array([])
    if key not in rows[0]:
        return None
    return _as_float_array([r.get(key, 0.0) for r in rows])


def _fallback_numeric_matrix(rows: list[dict[str, object]], deny: set[str]) -> tuple[list[str], np.ndarray]:
    if not rows:
        return [], np.zeros((0, 0), dtype=np.float64)
    keys = []
    for k, v in rows[0].items():
        kk = str(k)
        if kk in deny:
            continue
        if isinstance(v, (int, float)) and np.isfinite(float(v)):
            keys.append(kk)
    if not keys:
        return [], np.zeros((len(rows), 0), dtype=np.float64)
    mat = np.zeros((len(rows), len(keys)), dtype=np.float64)
    for i, r in enumerate(rows):
        for j, k in enumerate(keys):
            v = r.get(k, 0.0)
            try:
                x = float(v)
            except Exception:
                x = 0.0
            if not np.isfinite(x):
                x = 0.0
            mat[i, j] = x
    return keys, mat


def compute_score(rows: object, difficulty: int = 1) -> np.ndarray:
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        iptm = _get_column(rows, "iptm")
        ddg = _get_column(rows, "DDG")
        sap = _get_column(rows, "SAP Score")
        fv = _get_column(rows, "FV Charge")

        if iptm is not None and ddg is not None and sap is not None and fv is not None:
            if int(difficulty) == 1:
                return iptm - 0.1 * ddg - 0.01 * sap - 0.1 * fv
            if int(difficulty) == 2:
                return iptm - 0.1 * ddg - 0.01 * sap - 0.1 * np.abs(fv) + 0.05 * iptm * fv - 0.02 * np.sqrt(np.abs(ddg) + 1.0)
            return (
                np.tanh(iptm)
                - 0.1 * np.log1p(np.abs(ddg))
                - 0.05 * np.sin(sap)
                - 0.1 * np.abs(np.tanh(fv))
                + 0.03 * (iptm * ddg) / (1.0 + np.abs(sap))
                + 0.02 * np.sin(iptm * fv)
            )

        deny = {"label", "split"}
        keys, x = _fallback_numeric_matrix(rows, deny=deny)
        if x.shape[1] == 0:
            return np.zeros((len(rows),), dtype=np.float64)
        z = x
        if int(difficulty) == 1:
            w = np.linspace(1.0, 0.2, num=z.shape[1], dtype=np.float64)
            return (z * w).sum(axis=1)
        if int(difficulty) == 2:
            w = np.linspace(1.0, 0.2, num=z.shape[1], dtype=np.float64)
            base = (z * w).sum(axis=1)
            quad = (z[:, 0] * z[:, 1]) if z.shape[1] >= 2 else 0.0
            return base + 0.05 * quad - 0.02 * np.sqrt(np.abs(z[:, 0]) + 1.0)
        w = np.linspace(1.0, 0.2, num=z.shape[1], dtype=np.float64)
        base = (z * w).sum(axis=1)
        a = z[:, 0]
        b = z[:, 1] if z.shape[1] >= 2 else 0.0
        c = z[:, 2] if z.shape[1] >= 3 else 0.0
        return np.tanh(base) + 0.1 * np.sin(a * b) - 0.05 * np.log1p(np.abs(c))

    raise TypeError("compute_score expects a list of row dicts")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pool_size", type=int, default=5000)
    parser.add_argument("--top_ratio", type=float, default=0.2)
    parser.add_argument("--difficulty", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--score_column", default="Score")
    parser.add_argument("--split_train_test", action="store_true")
    parser.add_argument("--test_ratio", type=float, default=0.2)
    parser.add_argument("--out", default=".")
    args = parser.parse_args()

    fieldnames, rows = _read_rows(args.csv)
    pool_size = int(args.pool_size)
    if pool_size <= 0:
        raise ValueError(f"pool_size must be positive, got: {pool_size}")
    rng = np.random.default_rng(int(args.seed))
    if pool_size < len(rows):
        keep_idx = rng.choice(len(rows), size=pool_size, replace=False).tolist()
        pool_rows = [rows[i] for i in keep_idx]
    else:
        pool_rows = list(rows)

    y = np.asarray(compute_score(pool_rows, difficulty=int(args.difficulty)), dtype=np.float64).reshape(-1)
    labels = np.zeros((len(pool_rows),), dtype=np.int8)
    split_values: list[str] | None = None
    top_ratio = float(args.top_ratio)
    if not (0.0 < top_ratio < 1.0):
        raise ValueError(f"top_ratio must be in (0, 1), got: {top_ratio}")

    if bool(args.split_train_test):
        test_ratio = float(args.test_ratio)
        if not (0.0 < test_ratio < 1.0):
            raise ValueError(f"test_ratio must be in (0, 1), got: {test_ratio}")
        rng_split = np.random.default_rng(int(args.seed))
        n = len(pool_rows)
        test_n = int(max(1, min(n - 1, round(n * test_ratio)))) if n > 1 else n
        perm = rng_split.permutation(n)
        test_idx = set(int(i) for i in perm[:test_n].tolist())
        split_values = ["test" if i in test_idx else "train" for i in range(n)]

        for split_name in ["train", "test"]:
            idx = [i for i, s in enumerate(split_values) if s == split_name]
            if not idx:
                continue
            k = int(max(1, int(round(len(idx) * top_ratio))))
            k = int(min(k, len(idx)))
            if k <= 0:
                continue
            order = np.argsort(-y[np.asarray(idx, dtype=np.int64)], kind="mergesort")
            for j in order[:k].tolist():
                labels[idx[int(j)]] = 1
    else:
        k = int(max(1, int(round(len(pool_rows) * top_ratio))))
        k = int(min(k, len(pool_rows)))
        order = np.argsort(-y, kind="mergesort")
        if k > 0:
            labels[order[:k]] = 1

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = "split" if bool(args.split_train_test) else "all"
    ratio_tag = str(top_ratio).replace(".", "p")
    score_tag = str(args.score_column).replace(" ", "_")
    out_path = out_dir / (
        f"candidate_pool_scored_labeled_{suffix}_diff{int(args.difficulty)}_top{ratio_tag}_n{len(pool_rows)}_seed{int(args.seed)}_{score_tag}.csv"
    )

    out_fieldnames = list(fieldnames)
    if str(args.score_column) not in out_fieldnames:
        out_fieldnames.append(str(args.score_column))
    if split_values is not None and "split" not in out_fieldnames:
        out_fieldnames.append("split")
    if "label" not in out_fieldnames:
        out_fieldnames.append("label")

    out_rows: list[dict[str, object]] = []
    for i, (r, yi, lab) in enumerate(zip(pool_rows, y.tolist(), labels.tolist())):
        rr = dict(r)
        rr[str(args.score_column)] = float(yi)
        if split_values is not None:
            rr["split"] = split_values[i]
        rr["label"] = int(lab)
        out_rows.append(rr)

    _write_rows(out_path, fieldnames=out_fieldnames, rows=out_rows)
    print(f"Saved scored+labeled candidate pool: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
