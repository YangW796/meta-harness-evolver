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
    parser.add_argument("--split_out", default="train_test_split.csv")
    parser.add_argument("--test_ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    df = pd.read_csv(args.csv)

    # ===== 计算 x =====
    df["x"] = compute_x(df)

    # ===== 生成固定 train/test 划分并写入文件 =====
    n = len(df)
    rng = np.random.default_rng(int(args.seed))
    perm = rng.permutation(n)
    test_n = max(1, int(n * float(args.test_ratio))) if n > 0 else 0
    test_n = min(test_n, max(n - 1, 0)) if n > 1 else n
    test_idx = set(perm[:test_n].tolist())
    split = ["test" if i in test_idx else "train" for i in range(n)]
    split_df = df.copy()
    split_df["split"] = split
    split_df.to_csv(args.split_out, index=False)
    print(f"Saved split file: {args.split_out} (train={split.count('train')}, test={split.count('test')})")

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
