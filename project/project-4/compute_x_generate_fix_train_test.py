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
    parser.add_argument("--top_ratio", type=float, default=0.2)
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

    y = np.asarray(compute_x(pool_rows), dtype=np.float64).reshape(-1)
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
    out_path = out_dir / f"candidate_pool_labeled_{suffix}_top{ratio_tag}_n{len(pool_rows)}_seed{int(args.seed)}.csv"

    labeled_fieldnames = list(fieldnames)
    if split_values is not None and "split" not in labeled_fieldnames:
        labeled_fieldnames.append("split")
    if "label" not in labeled_fieldnames:
        labeled_fieldnames.append("label")
    labeled_rows: list[dict[str, object]] = []
    for i, (r, lab) in enumerate(zip(pool_rows, labels.tolist())):
        rr = dict(r)
        if split_values is not None:
            rr["split"] = split_values[i]
        rr["label"] = int(lab)
        labeled_rows.append(rr)
    _write_rows(out_path, fieldnames=labeled_fieldnames, rows=labeled_rows)

    print(f"Saved labeled candidate pool: {out_path}")


if __name__ == "__main__":
    main()
'''
python project/project-4/compute_x_generate_fix_train_test.py \
  --csv /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/Ruiqi_Lin/project/A07/Odesign/5vli/merged_results.csv \
  --pool_size 5000 \
  --top_ratio 0.2 \
  --split_train_test \
  --test_ratio 0.2 \
  --seed 42 \
  --out /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/data

python project/project-4/compute_x_generate_fix_train_test.py \
  --csv /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/Ruiqi_Lin/project/A07/Odesign/5vli/merged_results.csv \
  --pool_size 5000 \
  --top_ratio 0.2 \
  --out /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/data
'''
