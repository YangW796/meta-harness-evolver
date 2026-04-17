import argparse
import json
import os
import sys
from pathlib import Path

import esm
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import f1_score

try:
    project_dir = Path(__file__).resolve().parents[4]
except IndexError:
    project_dir = None

if project_dir is not None:
    sys.path.insert(0, str(project_dir))
else:
    for p in Path(__file__).resolve().parents:
        if (p / "index.py").exists():
            sys.path.insert(0, str(p))
            break

from index import compute_x

try:
    from tqdm import tqdm  # type: ignore
except ModuleNotFoundError:
    def tqdm(it, **kwargs):
        return it


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


def _resolve_device(device: str) -> torch.device:
    d = (device or "auto").strip().lower()
    if d == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if d.startswith("cuda") and not torch.cuda.is_available():
        return torch.device("cpu")
    return torch.device(d)


def load_esm(device: torch.device):
    print("Loading ESM...")
    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model.eval()
    model = model.to(device)
    return model, batch_converter


def _make_topk_labels(values: np.ndarray, top_ratio: float) -> np.ndarray:
    n = len(values)
    k = max(1, int(n * top_ratio))
    idx = np.argsort(-values)
    labels = np.zeros(n, dtype=np.int64)
    labels[idx[:k]] = 1
    return labels


def _encode_sequences(
    sequences: list[str],
    esm_model,
    batch_converter,
    device: torch.device,
    batch_size: int,
) -> torch.Tensor:
    out_chunks: list[torch.Tensor] = []
    for start in tqdm(range(0, len(sequences), batch_size), desc="Encoding", unit="batch"):
        batch = [(str(i), sequences[i]) for i in range(start, min(len(sequences), start + batch_size))]
        _, _, tokens = batch_converter(batch)
        tokens = tokens.to(device)
        with torch.no_grad():
            out = esm_model(tokens, repr_layers=[6])
        emb = out["representations"][6].mean(1).detach().cpu()
        out_chunks.append(emb)
    return torch.cat(out_chunks, dim=0)


def train(
    csv_path: str,
    root_dir: str,
    model_path: str,
    top_ratio: float,
    test_ratio: float,
    seed: int,
    device: str,
    batch_size: int,
    split_file: str,
) -> dict:
    df = pd.read_csv(csv_path)
    required_columns = {"Sequence", "Structure", "iptm", "DDG", "SAP Score", "FV Charge"}
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    split_path = Path(split_file).expanduser()
    if not split_path.is_absolute():
        split_path = Path(csv_path).expanduser().resolve().parent / split_path
    if not split_path.exists():
        raise ValueError(f"Missing split_file: {split_path}")

    split_df = pd.read_csv(split_path)
    if "split" not in split_df.columns:
        raise ValueError(f"split_file missing 'split' column: {split_path}")

    if required_columns.issubset(set(split_df.columns)):
        df = split_df
    else:
        if "Structure" not in split_df.columns:
            raise ValueError(f"split_file missing 'Structure' column for merge: {split_path}")
        df = df.merge(split_df[["Structure", "split"]], on="Structure", how="inner")

    df["x"] = compute_x(df)
    sequences = df["Sequence"].tolist()
    structures = df["Structure"].tolist()
    y_all = torch.tensor(df["x"].values, dtype=torch.float32)

    n = len(df)
    if n < 2:
        train_idx = np.arange(n)
        test_idx = np.arange(n)
    else:
        if "split" not in df.columns:
            raise ValueError(f"No split column available after loading split_file: {split_path}")
        split_values = df["split"].astype(str).str.lower()
        train_idx = np.flatnonzero(split_values == "train")
        test_idx = np.flatnonzero(split_values == "test")
        if len(train_idx) == 0 or len(test_idx) == 0:
            raise ValueError(f"Invalid split distribution in split_file: train={len(train_idx)}, test={len(test_idx)}")

    resolved_device = _resolve_device(device)
    esm_model, batch_converter = load_esm(resolved_device)

    seq_emb = _encode_sequences(sequences, esm_model, batch_converter, resolved_device, int(batch_size))

    struct_feats = []
    for structure in tqdm(structures, desc="CIF", unit="item"):
        cif = get_cif_path(structure, root_dir)
        struct_feats.append(parse_cif(cif))
    struct_feats_t = torch.tensor(struct_feats, dtype=torch.float32)

    X_all = torch.cat([seq_emb, struct_feats_t], dim=1).to(resolved_device)
    y_all = y_all.to(resolved_device)
    X_train = X_all[train_idx]
    y_train = y_all[train_idx]
    X_test = X_all[test_idx]
    y_test = y_all[test_idx]

    model = Model(X_all.shape[1]).to(resolved_device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    for epoch in tqdm(range(30), desc="Train", unit="epoch"):
        pred_train = model(X_train)
        loss = loss_fn(pred_train, y_train)
        opt.zero_grad()
        loss.backward()
        opt.step()

    with torch.no_grad():
        test_pred = model(X_test).detach().cpu().numpy()
    y_test_np = y_test.detach().cpu().numpy()
    true_label = _make_topk_labels(y_test_np, top_ratio)
    pred_label = _make_topk_labels(test_pred, top_ratio)
    f1 = float(f1_score(true_label, pred_label))

    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")
    print(f"F1 score (top-k): {f1:.6f}")

    output_dir = Path(model_path).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    top_k_test = int(max(1, int(len(y_test_np) * top_ratio)))
    metrics_payload = {
        "metrics": {
            "test": {
                "f1": f1,
                "top_ratio": float(top_ratio),
                "top_k": top_k_test,
                "num_samples": int(len(test_idx)),
                "test_ratio": float(test_ratio),
                "seed": int(seed),
                "device": str(resolved_device),
            }
        }
    }
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
    print(f"Metrics saved to {metrics_path}")
    return metrics_payload


def predict(sequence: str, structure: str, root_dir: str, model_path: str) -> float:
    resolved_device = _resolve_device(os.environ.get("HARNESS_DEVICE", "auto"))
    esm_model, batch_converter = load_esm(resolved_device)
    cif_path = get_cif_path(structure, root_dir)
    struct_feat = torch.tensor(parse_cif(cif_path), dtype=torch.float32).unsqueeze(0)
    model_input_dim = 320 + int(struct_feat.shape[1])
    model = Model(model_input_dim).to(resolved_device)
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    batch = [("x", sequence)]
    _, _, tokens = batch_converter(batch)
    tokens = tokens.to(resolved_device)
    with torch.no_grad():
        out = esm_model(tokens, repr_layers=[6])
        seq_emb = out["representations"][6].mean(1)

    struct_feat = struct_feat.to(resolved_device)
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
    parser.add_argument("--test_ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", type=str, default=os.environ.get("HARNESS_DEVICE", "auto"))
    parser.add_argument("--batch_size", type=int, default=int(os.environ.get("HARNESS_BATCH_SIZE", "16")))
    parser.add_argument("--split_file", default="train_test_split.csv")
    parser.add_argument("--sequence", help="sequence for prediction")
    parser.add_argument("--structure", help="structure name")
    args = parser.parse_args()

    if args.mode == "train":
        if not args.csv:
            raise ValueError("Need --csv for training")
        train(
            args.csv,
            args.root_dir,
            args.model_path,
            args.top_ratio,
            args.test_ratio,
            args.seed,
            args.device,
            args.batch_size,
            args.split_file,
        )
        return 0

    if not args.sequence or not args.structure:
        raise ValueError("Need --sequence and --structure for prediction")
    pred = predict(args.sequence, args.structure, args.root_dir, args.model_path)
    print(f"Predicted x: {pred}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
