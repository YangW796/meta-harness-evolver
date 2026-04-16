import argparse
import json
import os
from pathlib import Path

import esm
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import f1_score


def parse_cif(cif_path: str) -> list[float]:
    atom_count = 0
    residue_set = set()

    if not os.path.exists(cif_path):
        return [0.0, 0.0]

    with open(cif_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("ATOM"):
                atom_count += 1
                parts = line.split()
                if len(parts) > 5:
                    residue_set.add(parts[5])

    return [atom_count / 10000.0, len(residue_set) / 1000.0]


def get_cif_path(structure: str, root_dir: str) -> str:
    pdb_id = structure.split("_")[0]
    return os.path.join(root_dir, pdb_id, "af3_output", structure, f"{structure}_model.cif")


def compute_x(df: pd.DataFrame) -> pd.Series:
    return df["iptm"] - 0.1 * df["DDG"] - 0.01 * df["SAP Score"] - 0.1 * df["FV Charge"].abs()


class Model(nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)


def load_esm():
    print("Loading ESM...")
    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model.eval()
    return model, batch_converter


def _make_topk_labels(values: np.ndarray, top_ratio: float) -> np.ndarray:
    n = len(values)
    k = max(1, int(n * top_ratio))
    idx = np.argsort(-values)
    labels = np.zeros(n, dtype=np.int64)
    labels[idx[:k]] = 1
    return labels


def _load_split(split_path: str) -> tuple[np.ndarray, np.ndarray]:
    payload = json.loads(Path(split_path).read_text(encoding="utf-8"))
    train_idx = np.array(payload.get("train_indices", []), dtype=np.int64)
    test_idx = np.array(payload.get("test_indices", []), dtype=np.int64)
    if train_idx.size == 0 or test_idx.size == 0:
        raise ValueError(f"Invalid split file (empty indices): {split_path}")
    return train_idx, test_idx


def train(csv_path: str, root_dir: str, model_path: str, top_ratio: float, split_path: str) -> dict:
    df = pd.read_csv(csv_path)
    required_columns = {"Sequence", "Structure", "iptm", "DDG", "SAP Score", "FV Charge"}
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["x"] = compute_x(df)
    sequences = df["Sequence"].tolist()
    structures = df["Structure"].tolist()
    y_all = torch.tensor(df["x"].values, dtype=torch.float32)
    train_idx, test_idx = _load_split(split_path)
    if int(train_idx.max(initial=0)) >= len(df) or int(test_idx.max(initial=0)) >= len(df):
        raise ValueError(f"Split indices out of range for csv (n={len(df)}): {split_path}")

    esm_model, batch_converter = load_esm()

    print("Encoding sequences...")
    batch = [(str(i), seq) for i, seq in enumerate(sequences)]
    _, _, tokens = batch_converter(batch)

    with torch.no_grad():
        out = esm_model(tokens, repr_layers=[6])
    seq_emb = out["representations"][6].mean(1)

    print("Parsing CIF...")
    struct_feats = []
    for structure in structures:
        cif = get_cif_path(structure, root_dir)
        struct_feats.append(parse_cif(cif))
    struct_feats_t = torch.tensor(struct_feats, dtype=torch.float32)

    X = torch.cat([seq_emb, struct_feats_t], dim=1)
    X_train = X[train_idx]
    y_train = y_all[train_idx]
    X_test = X[test_idx]
    y_test = y_all[test_idx]

    model = Model(X.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    print("Training...")
    for epoch in range(30):
        pred = model(X_train)
        loss = loss_fn(pred, y_train)
        opt.zero_grad()
        loss.backward()
        opt.step()
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

    test_pred = model(X_test).detach().numpy()
    y_test_np = y_test.detach().numpy()
    true_label = _make_topk_labels(y_test_np, top_ratio)
    pred_label = _make_topk_labels(test_pred, top_ratio)
    f1 = float(f1_score(true_label, pred_label))

    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")
    print(f"F1 score (top-k): {f1:.6f}")

    output_dir = Path(model_path).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    top_k = max(1, int(len(test_idx) * top_ratio))
    metrics_payload = {
        "metrics": {
            "test": {
                "f1": f1,
                "top_ratio": float(top_ratio),
                "top_k": int(top_k),
                "num_samples": int(len(test_idx)),
                "split_file": str(split_path),
            }
        }
    }
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
    print(f"Metrics saved to {metrics_path}")
    return metrics_payload


def predict(sequence: str, structure: str, root_dir: str, model_path: str) -> float:
    esm_model, batch_converter = load_esm()
    model = Model(320 + 2)
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    batch = [("x", sequence)]
    _, _, tokens = batch_converter(batch)
    with torch.no_grad():
        out = esm_model(tokens, repr_layers=[6])
        seq_emb = out["representations"][6].mean(1)

    cif_path = get_cif_path(structure, root_dir)
    struct_feat = torch.tensor(parse_cif(cif_path), dtype=torch.float32).unsqueeze(0)
    x = torch.cat([seq_emb, struct_feat], dim=1)

    pred = model(x)
    return float(pred.item())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "predict"], required=True)
    parser.add_argument("--csv", help="merged_results.csv path")
    parser.add_argument("--root_dir", required=True)
    parser.add_argument("--model_path", default="iptm_model.pt")
    parser.add_argument("--top_ratio", type=float, default=0.1)
    parser.add_argument("--split_file", help="train/test split json generated by compute_x_generate_fix_train_test.py")
    parser.add_argument("--sequence", help="sequence for prediction")
    parser.add_argument("--structure", help="structure name")
    args = parser.parse_args()

    if args.mode == "train":
        if not args.csv:
            raise ValueError("Need --csv for training")
        if not args.split_file:
            raise ValueError("Need --split_file for training")
        train(args.csv, args.root_dir, args.model_path, args.top_ratio, args.split_file)
        return 0

    if not args.sequence or not args.structure:
        raise ValueError("Need --sequence and --structure for prediction")
    pred = predict(args.sequence, args.structure, args.root_dir, args.model_path)
    print(f"Predicted x: {pred}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
