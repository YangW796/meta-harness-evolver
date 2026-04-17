import pandas as pd
import argparse
import numpy as np
from index import compute_x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", default=".")
    parser.add_argument("--top_ratio", type=float, default=0.1)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--split_out", default=".")
    parser.add_argument("--test_ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num", type=int, default=None)

    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    if args.num is not None and args.num > 0 and args.num < len(df):
        rng = np.random.default_rng(int(args.seed))
        keep_idx = rng.choice(len(df), size=int(args.num), replace=False)
        df = df.iloc[keep_idx].reset_index(drop=True)

    # ===== 计算 x =====
    df["x"] = compute_x(df)

    def _fmt_float(x: float) -> str:
        return str(x).replace(".", "p")

    num_tag = "all" if args.num is None else str(int(args.num))
    split_name = f"train_test_split_num{num_tag}_test{_fmt_float(float(args.test_ratio))}_seed{int(args.seed)}.csv"

    if args.threshold is not None:
        out_name = f"topk_x_num{num_tag}_thr{_fmt_float(float(args.threshold))}_seed{int(args.seed)}.csv"
    else:
        out_name = f"topk_x_num{num_tag}_top{_fmt_float(float(args.top_ratio))}_seed{int(args.seed)}.csv"

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
    from pathlib import Path

    split_out = Path(args.split_out)
    if split_out.suffix.lower() == ".csv":
        split_path = split_out
    else:
        split_out.mkdir(parents=True, exist_ok=True)
        split_path = split_out / split_name
    split_df.to_csv(split_path, index=False)
    print(f"Saved split file: {split_path} (train={split.count('train')}, test={split.count('test')})")

    # ===== 排序 =====
    df = df.sort_values("x", ascending=False)

    # ===== 选取 =====
    if args.threshold is not None:
        selected = df[df["x"] >= args.threshold]
    else:
        k = int(len(df) * args.top_ratio)
        selected = df.head(k)

    out = Path(args.out)
    if out.suffix.lower() == ".csv":
        out_path = out
    else:
        out.mkdir(parents=True, exist_ok=True)
        out_path = out / out_name
    selected.to_csv(out_path, index=False)

    print(f"Saved {len(selected)} samples to {out_path}")


if __name__ == "__main__":
    main()
'''
python project/project-2/compute_x_generate_fix_train_test.py \
    --csv /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/Ruiqi_Lin/project/A07/Odesign/5vli/merged_results.csv \
    --top_ratio 0.2 \
    --out /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/data \
    --split_out /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/data \
    --num 5000 \
    --test_ratio 0.5 \
'''      
    