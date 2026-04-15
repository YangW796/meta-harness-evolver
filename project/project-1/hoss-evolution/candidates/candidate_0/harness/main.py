#!/usr/bin/env python3
import argparse
import csv
import json
import math
import random
from pathlib import Path

import numpy as np

AA_ORDER = "ACDEFGHIKLMNPQRSTVWY"
AA_INDEX = {aa: i for i, aa in enumerate(AA_ORDER)}


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def safe_float(x):
    try:
        if x is None:
            return None
        s = str(x).strip()
        if s == "":
            return None
        return float(s)
    except Exception:
        return None


def find_csv(data_root: Path, explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"CSV not found: {p}")
        return p
    for name in ["merged_results.csv", "data.csv", "dataset.csv"]:
        p = data_root / name
        if p.exists():
            return p.resolve()
    all_csv = sorted(data_root.rglob("*.csv"))
    if all_csv:
        return all_csv[0].resolve()
    raise FileNotFoundError(f"No CSV found under {data_root}")


def load_rows(csv_path: Path):
    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = reader.fieldnames or []
    if not rows:
        raise ValueError(f"Empty CSV: {csv_path}")
    return cols, rows


def infer_columns(columns, rows):
    lower_to_col = {c.lower(): c for c in columns}

    seq_col = None
    for k in ["sequence", "seq", "fasta", "mut_seq", "wt_seq"]:
        if k in lower_to_col:
            seq_col = lower_to_col[k]
            break

    struct_col = None
    for k in ["structure", "pdb", "cif", "structure_path", "pdb_path", "cif_path"]:
        if k in lower_to_col:
            struct_col = lower_to_col[k]
            break

    numeric_cols = []
    for c in columns:
        ok = 0
        for r in rows:
            if safe_float(r.get(c)) is not None:
                ok += 1
        if ok >= max(3, int(0.5 * len(rows))):
            numeric_cols.append(c)

    if not numeric_cols:
        raise ValueError("No numeric columns found for label inference")

    label_col = None
    for k in ["ddg", "delta_g", "target", "label", "y"]:
        if k in lower_to_col and lower_to_col[k] in numeric_cols:
            label_col = lower_to_col[k]
            break

    if label_col is None:
        filtered = []
        for c in numeric_cols:
            lc = c.lower()
            if any(tok in lc for tok in ["id", "index", "fold", "split", "seed"]):
                continue
            filtered.append(c)
        label_col = filtered[0] if filtered else numeric_cols[0]

    return label_col, seq_col, struct_col


def maybe_read_text_file(value: str, data_root: Path) -> str | None:
    raw = value.strip()
    if not raw:
        return None
    for p in [Path(raw), data_root / raw]:
        if p.exists() and p.is_file():
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if text.strip().startswith(">"):
                lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith(">")]
                return "".join(lines)
            return text.strip()
    return None


def extract_sequence(value, data_root: Path) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    if not s:
        return ""
    from_file = maybe_read_text_file(s, data_root)
    if from_file is not None:
        s = from_file
    return "".join(ch for ch in s.upper() if ch in AA_INDEX)


def sequence_features(seq: str) -> np.ndarray:
    feats = np.zeros(26, dtype=np.float32)
    if not seq:
        return feats

    length = float(len(seq))
    feats[0] = length / 1000.0
    counts = np.zeros(len(AA_ORDER), dtype=np.float32)
    for ch in seq:
        idx = AA_INDEX.get(ch)
        if idx is not None:
            counts[idx] += 1.0
    counts /= max(length, 1.0)
    feats[1:21] = counts

    hydrophobic = set("AILMFWV")
    charged = set("KRDE")
    polar = set("STNQCY")

    feats[21] = sum(ch in hydrophobic for ch in seq) / length
    feats[22] = sum(ch in charged for ch in seq) / length
    feats[23] = sum(ch in polar for ch in seq) / length
    feats[24] = seq.count("P") / length
    feats[25] = seq.count("G") / length
    return feats


def resolve_structure_path(value, data_root: Path) -> Path | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None

    base_candidates = [Path(raw), data_root / raw]
    if Path(raw).suffix.lower() in {".pdb", ".cif"}:
        for c in base_candidates:
            if c.exists() and c.is_file():
                return c
    else:
        for ext in [".pdb", ".cif"]:
            for c in base_candidates:
                p = c.with_suffix(ext)
                if p.exists() and p.is_file():
                    return p
    return None


def parse_structure_features(path: Path | None) -> np.ndarray:
    feats = np.zeros(6, dtype=np.float32)
    if path is None or not path.exists():
        return feats

    atom_count = 0
    residue_set = set()
    chain_set = set()

    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    atom_count += 1
                    if path.suffix.lower() == ".pdb":
                        chain = line[21:22].strip() or "_"
                        resi = line[22:27].strip() or "0"
                    else:
                        parts = line.split()
                        chain = parts[4] if len(parts) > 5 else "_"
                        resi = parts[5] if len(parts) > 6 else "0"
                    chain_set.add(chain)
                    residue_set.add((chain, resi))
    except Exception:
        return feats

    size_kb = path.stat().st_size / 1024.0
    feats[0] = atom_count / 20000.0
    feats[1] = len(residue_set) / 2000.0
    feats[2] = len(chain_set) / 20.0
    feats[3] = size_kb / 1000.0
    feats[4] = 1.0 if path.suffix.lower() == ".pdb" else 0.0
    feats[5] = 1.0 if path.suffix.lower() == ".cif" else 0.0
    return feats


def split_indices(n: int, seed: int, train_ratio: float, val_ratio: float):
    rng = np.random.default_rng(seed)
    idx = np.arange(n)
    rng.shuffle(idx)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    train_idx = idx[:n_train]
    val_idx = idx[n_train:n_train + n_val]
    test_idx = idx[n_train + n_val:]
    if len(test_idx) == 0:
        test_idx = idx[-max(1, n // 10):]
        val_idx = idx[n_train:-len(test_idx)]
    return train_idx, val_idx, test_idx


def regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    y_true = y_true.astype(np.float64)
    y_pred = y_pred.astype(np.float64)
    mse = float(np.mean((y_true - y_pred) ** 2))
    rmse = float(np.sqrt(mse))
    mae = float(np.mean(np.abs(y_true - y_pred)))

    ss_res = float(np.sum((y_true - y_pred) ** 2))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2 = float(1.0 - ss_res / (ss_tot + 1e-12))

    yt = y_true - np.mean(y_true)
    yp = y_pred - np.mean(y_pred)
    denom = (np.sqrt(np.sum(yt ** 2)) * np.sqrt(np.sum(yp ** 2))) + 1e-12
    pearson = float(np.sum(yt * yp) / denom)

    return {"r2": r2, "rmse": rmse, "mae": mae, "pearson": pearson}


class NumpyMLPRegressor:
    def __init__(self, input_dim: int, hidden_dims=(128, 64, 32), lr=1e-3, seed=42):
        self.lr = lr
        rng = np.random.default_rng(seed)
        dims = [input_dim, *hidden_dims, 1]
        self.W = []
        self.b = []
        for i in range(len(dims) - 1):
            scale = np.sqrt(2.0 / dims[i])
            self.W.append((rng.standard_normal((dims[i], dims[i + 1])) * scale).astype(np.float32))
            self.b.append(np.zeros((1, dims[i + 1]), dtype=np.float32))

    @staticmethod
    def relu(x):
        return np.maximum(0.0, x)

    @staticmethod
    def relu_grad(x):
        return (x > 0.0).astype(np.float32)

    def forward(self, X):
        A = X
        activations = [A]
        pre_acts = []
        for i in range(len(self.W) - 1):
            Z = A @ self.W[i] + self.b[i]
            pre_acts.append(Z)
            A = self.relu(Z)
            activations.append(A)
        Z = A @ self.W[-1] + self.b[-1]
        pre_acts.append(Z)
        activations.append(Z)
        return Z.squeeze(-1), activations, pre_acts

    def predict(self, X):
        y_hat, _, _ = self.forward(X)
        return y_hat

    def train_epoch(self, X, y, batch_size=64):
        idx = np.arange(len(X))
        np.random.shuffle(idx)
        X = X[idx]
        y = y[idx]

        total_loss = 0.0
        for start in range(0, len(X), batch_size):
            xb = X[start:start + batch_size]
            yb = y[start:start + batch_size]
            n = max(1, len(xb))

            pred, acts, pre = self.forward(xb)
            diff = (pred - yb)
            loss = float(np.mean(diff ** 2))
            total_loss += loss * n

            dZ = (2.0 / n) * diff.reshape(-1, 1)

            dW = [None] * len(self.W)
            db = [None] * len(self.b)

            dW[-1] = acts[-2].T @ dZ
            db[-1] = np.sum(dZ, axis=0, keepdims=True)

            dA = dZ @ self.W[-1].T
            for i in range(len(self.W) - 2, -1, -1):
                dZ_i = dA * self.relu_grad(pre[i])
                dW[i] = acts[i].T @ dZ_i
                db[i] = np.sum(dZ_i, axis=0, keepdims=True)
                if i > 0:
                    dA = dZ_i @ self.W[i].T

            for i in range(len(self.W)):
                self.W[i] -= self.lr * dW[i]
                self.b[i] -= self.lr * db[i]

        return total_loss / len(X)


def write_predictions_csv(path: Path, y_true: np.ndarray, y_pred: np.ndarray):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["split", "y_true", "y_pred"])
        for yt, yp in zip(y_true, y_pred):
            w.writerow(["test", float(yt), float(yp)])


def train_and_evaluate(args):
    data_root = Path(args.data_root).expanduser().resolve()
    csv_path = find_csv(data_root, args.data_csv)
    columns, rows = load_rows(csv_path)

    label_col, seq_col, struct_col = infer_columns(columns, rows)

    X_list = []
    y_list = []

    for r in rows:
        y = safe_float(r.get(label_col))
        if y is None:
            continue

        seq = extract_sequence(r.get(seq_col), data_root) if seq_col else ""
        sfeat = sequence_features(seq)

        struct_path = resolve_structure_path(r.get(struct_col), data_root) if struct_col else None
        pfeat = parse_structure_features(struct_path)

        X_list.append(np.concatenate([sfeat, pfeat], axis=0))
        y_list.append(y)

    if len(y_list) < 20:
        raise ValueError(f"Dataset too small ({len(y_list)} rows with label), need >=20")

    X = np.stack(X_list).astype(np.float32)
    y = np.array(y_list, dtype=np.float32)

    train_idx, val_idx, test_idx = split_indices(len(y), args.seed, 0.7, 0.15)
    x_train, y_train = X[train_idx], y[train_idx]
    x_val, y_val = X[val_idx], y[val_idx]
    x_test, y_test = X[test_idx], y[test_idx]

    mu = x_train.mean(axis=0, keepdims=True)
    sigma = x_train.std(axis=0, keepdims=True) + 1e-6
    x_train = (x_train - mu) / sigma
    x_val = (x_val - mu) / sigma
    x_test = (x_test - mu) / sigma

    model = NumpyMLPRegressor(
        input_dim=x_train.shape[1],
        hidden_dims=(128, 64, 32),
        lr=args.lr,
        seed=args.seed,
    )

    best_val_r2 = -1e9
    best_state = None
    wait = 0

    for epoch in range(args.epochs):
        train_loss = model.train_epoch(x_train, y_train, batch_size=args.batch_size)
        val_pred = model.predict(x_val)
        val_metrics = regression_metrics(y_val, val_pred)

        print(
            f"epoch={epoch + 1:03d} train_loss={train_loss:.6f} "
            f"val_r2={val_metrics['r2']:.4f} val_rmse={val_metrics['rmse']:.4f}"
        )

        if val_metrics["r2"] > best_val_r2:
            best_val_r2 = val_metrics["r2"]
            best_state = {
                "W": [w.copy() for w in model.W],
                "b": [b.copy() for b in model.b],
            }
            wait = 0
        else:
            wait += 1
            if wait >= args.patience:
                print(f"early_stop at epoch {epoch + 1}")
                break

    if best_state is not None:
        model.W = best_state["W"]
        model.b = best_state["b"]

    train_pred = model.predict(x_train)
    val_pred = model.predict(x_val)
    test_pred = model.predict(x_test)

    metrics = {
        "train": regression_metrics(y_train, train_pred),
        "val": regression_metrics(y_val, val_pred),
        "test": regression_metrics(y_test, test_pred),
    }

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    model_meta = {
        "input_dim": int(x_train.shape[1]),
        "hidden_dims": [128, 64, 32],
        "label_col": label_col,
        "seq_col": seq_col,
        "struct_col": struct_col,
    }
    (output_dir / "model_meta.json").write_text(json.dumps(model_meta, indent=2), encoding="utf-8")

    write_predictions_csv(output_dir / "test_predictions.csv", y_test, test_pred)

    result = {
        "data_csv": str(csv_path),
        "label_col": label_col,
        "sequence_col": seq_col,
        "structure_col": struct_col,
        "sizes": {
            "train": int(len(train_idx)),
            "val": int(len(val_idx)),
            "test": int(len(test_idx)),
            "total": int(len(y)),
        },
        "metrics": metrics,
    }

    (output_dir / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== Final Metrics ===")
    print(json.dumps(result["metrics"], indent=2))
    print(f"Saved outputs to: {output_dir}")


def parse_args():
    parser = argparse.ArgumentParser(description="Candidate-0 deep regression baseline")
    parser.add_argument("--data-root", default=".", help="Root path for csv/fasta/pdb/cif data")
    parser.add_argument("--data-csv", default=None, help="Optional explicit csv path")
    parser.add_argument("--output-dir", default="outputs", help="Artifacts output dir")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--patience", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=1e-3)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    set_seed(args.seed)
    train_and_evaluate(args)
