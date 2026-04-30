import argparse
import csv
from pathlib import Path

import numpy as np

from main_fix_train_test_input_output import (
    _extract_inline_labels,
    _make_candidate_pool,
    _make_pu_labels,
    _read_csv_rows,
)


def _write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a fixed PU candidate pool with inline labels.")
    parser.add_argument("--csv", required=True, help="Large unlabeled/candidate CSV")
    parser.add_argument("--positive_csv", required=True, help="CSV containing known positive examples")
    parser.add_argument("--pool_size", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--id_column", default="")
    parser.add_argument("--match_columns", default="")
    parser.add_argument("--out", default=".")
    args = parser.parse_args()

    candidate_fields, rows = _read_csv_rows(args.csv)
    pool_rows = _make_candidate_pool(rows, pool_size=int(args.pool_size), seed=int(args.seed))
    pool_rows, inline_labels = _extract_inline_labels(pool_rows)
    if inline_labels is not None:
        labels = inline_labels
        diagnostics = {
            "positive_in_pool": int(labels.sum()),
            "match_mode": "inline_label",
            "match_columns": [],
        }
    else:
        positive_fields, positive_rows = _read_csv_rows(args.positive_csv)
        labels, diagnostics = _make_pu_labels(
            pool_rows=pool_rows,
            positive_rows=positive_rows,
            positive_fields=positive_fields,
            candidate_fields=[c for c in candidate_fields if c != "label"],
            id_column=str(args.id_column or ""),
            match_columns=str(args.match_columns or ""),
        )

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"candidate_pool_pu_labeled_n{len(pool_rows)}_seed{int(args.seed)}.csv"

    fieldnames = [c for c in candidate_fields if c != "label"]
    if "label" not in fieldnames:
        fieldnames.append("label")
    labeled_rows: list[dict[str, object]] = []
    for row, lab in zip(pool_rows, labels.tolist()):
        rr = dict(row)
        rr.pop("label", None)
        rr["label"] = int(lab)
        labeled_rows.append(rr)

    _write_rows(out_path, fieldnames=fieldnames, rows=labeled_rows)
    print(f"Saved PU labeled candidate pool: {out_path}")
    print(
        "Diagnostics: "
        f"positive_in_pool={int(np.asarray(labels).sum())}, "
        f"match_mode={diagnostics.get('match_mode')}, "
        f"match_columns={diagnostics.get('match_columns')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
