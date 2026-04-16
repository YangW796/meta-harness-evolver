import pandas as pd
import argparse
import numpy as np
from index import compute_x

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", default="topk_x.csv")
    parser.add_argument("--top_ratio", type=float, default=0.1)
    parser.add_argument("--threshold", type=float, default=None)

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


if __name__ == "__main__":
    main()
# python compute_topk_x.py \
#     --csv merged_results.csv \
#     --top_ratio 0.1 \
#     --out top10_x.csv