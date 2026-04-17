import argparse
import csv
import numpy as np
from pathlib import Path

from index import compute_x


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pool_size", type=int, default=5000)
    parser.add_argument("--top_k", type=int, default=1000)
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

    y = np.asarray(compute_x(pool_rows), dtype=np.float64).reshape(-1)
    k = int(max(0, min(int(args.top_k), len(pool_rows))))
    order = np.argsort(-y, kind="mergesort")
    labels = np.zeros((len(pool_rows),), dtype=np.int8)
    if k > 0:
        labels[order[:k]] = 1

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    pool_path = out_dir / f"candidate_pool_n{len(pool_rows)}_seed{int(args.seed)}.csv"
    gt_path = out_dir / f"ground_truth_top{k}_n{len(pool_rows)}_seed{int(args.seed)}.csv"

    _write_rows(pool_path, fieldnames=fieldnames, rows=pool_rows)
    with gt_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate_index", "label"])
        writer.writeheader()
        for i, lab in enumerate(labels.tolist()):
            writer.writerow({"candidate_index": int(i), "label": int(lab)})

    print(f"Saved candidate pool: {pool_path}")
    print(f"Saved ground truth labels: {gt_path}")


if __name__ == "__main__":
    main()
