import pandas as pd
import argparse
import numpy as np
import json
from index import compute_x



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", default="topk_x.csv")
    parser.add_argument("--top_ratio", type=float, default=0.1)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--split_out", default="train_test_split.json")
    parser.add_argument("--test_ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    # ===== 计算 x =====
    df["x"] = compute_x(df)

    # ===== 排序 =====
    df = df.sort_values("x", ascending=False)

    # ===== 选取 =====
    if args.threshold is not None:
        selected = df[df["x"] >= args.threshold]
    else:
        k = int(len(df) * args.top_ratio)
        selected = df.head(k)

    selected.to_csv(args.out, index=False)

    print(f"Saved {len(selected)} samples to {args.out}")

    n = len(df)
    if n < 2:
        train_indices = list(range(n))
        test_indices = list(range(n))
    else:
        test_n = max(1, int(n * float(args.test_ratio)))
        test_n = min(test_n, n - 1)
        rng = np.random.default_rng(int(args.seed))
        perm = rng.permutation(n)
        test_indices = perm[:test_n].tolist()
        train_indices = perm[test_n:].tolist()

    split_payload = {
        "num_samples": int(n),
        "seed": int(args.seed),
        "test_ratio": float(args.test_ratio),
        "train_indices": train_indices,
        "test_indices": test_indices,
    }
    with open(args.split_out, "w", encoding="utf-8") as f:
        json.dump(split_payload, f, ensure_ascii=False, indent=2)
    print(f"Saved split: train={len(train_indices)} test={len(test_indices)} to {args.split_out}")


if __name__ == "__main__":
    main()
# python compute_topk_x.py \
#     --csv merged_results.csv \
#     --top_ratio 0.1 \
#     --out top10_x.csv
