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


def train(csv_path: str, root_dir: str, model_path: str, top_ratio: float) -> dict:
    df = pd.read_csv(csv_path)
    required_columns = {"Sequence", "Structure", "iptm", "DDG", "SAP Score", "FV Charge"}
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["x"] = compute_x(df)
    df = df.sort_values("x", ascending=False).reset_index(drop=True)
    k = max(1, int(len(df) * top_ratio))

    df["label"] = 0
    df.iloc[:k, df.columns.get_loc("label")] = 1

    sequences = df["Sequence"].tolist()
    structures = df["Structure"].tolist()
    y = torch.tensor(df["x"].values, dtype=torch.float32)

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

    model = Model(X.shape[1])
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    print("Training...")
    for epoch in range(30):
        pred = model(X)
        loss = loss_fn(pred, y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

    pred = model(X).detach().numpy()
    df["pred"] = pred
    df = df.sort_values("pred", ascending=False).reset_index(drop=True)

    pred_label = np.zeros(len(df))
    pred_label[:k] = 1
    true_label = df["label"].values
    f1 = float(f1_score(true_label, pred_label))

    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")
    print(f"F1 score (top-k): {f1:.6f}")

    output_dir = Path(model_path).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_payload = {
        "metrics": {
            "test": {
                "f1": f1,
                "top_ratio": float(top_ratio),
                "top_k": int(k),
                "num_samples": int(len(df)),
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
    parser.add_argument("--sequence", help="sequence for prediction")
    parser.add_argument("--structure", help="structure name")
    args = parser.parse_args()

    if args.mode == "train":
        if not args.csv:
            raise ValueError("Need --csv for training")
        train(args.csv, args.root_dir, args.model_path, args.top_ratio)
        return 0

    if not args.sequence or not args.structure:
        raise ValueError("Need --sequence and --structure for prediction")
    pred = predict(args.sequence, args.structure, args.root_dir, args.model_path)
    print(f"Predicted x: {pred}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
