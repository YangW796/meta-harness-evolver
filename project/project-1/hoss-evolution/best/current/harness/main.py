import argparse
import json
import math
import os
from pathlib import Path
import math
import esm
import pandas as pd
import torch
import torch.nn as nn

try:
    from tqdm import tqdm  # type: ignore
except ModuleNotFoundError:
    def tqdm(it, **kwargs):
        return it

# ========= CIF解析 =========
def parse_cif(cif_path: str) -> list[float]:
    atom_count = 0
    residue_set = set()
    chain_set = set()

    if not os.path.exists(cif_path):
        return [0, 0, 0]

    with open(cif_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("ATOM"):
                atom_count += 1
                parts = line.split()
                if len(parts) > 5:
                    chain = parts[4]
                    resi = parts[5]
                    chain_set.add(chain)
                    residue_set.add((chain, resi))

    return [
        atom_count / 10000.0,
        len(residue_set) / 1000.0,
        len(chain_set)
    ]


# ========= Structure → CIF路径 =========
def get_cif_path(structure: str, root_dir: str) -> str:
    pdb_id = structure.split("_")[0]
    cif_path = os.path.join(
        root_dir,
        pdb_id,
        "af3_output",
        structure,
        f"{structure}_model.cif"
    )
    return cif_path


# ========= 模型 =========
class Model(nn.Module):
    def __init__(self, dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)


# ========= 加载ESM =========
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


def _compute_regression_metrics(pred: torch.Tensor, y: torch.Tensor) -> dict:
    diff = pred - y
    mse = torch.mean(diff ** 2).item()
    rmse = math.sqrt(mse)
    mae = torch.mean(torch.abs(diff)).item()

    y_mean = torch.mean(y)
    ss_res = torch.sum((y - pred) ** 2).item()
    ss_tot = torch.sum((y - y_mean) ** 2).item()
    r2 = 1.0 - ss_res / (ss_tot + 1e-12)

    vx = pred - torch.mean(pred)
    vy = y - y_mean
    pearson_num = torch.sum(vx * vy).item()
    pearson_den = math.sqrt(torch.sum(vx ** 2).item() * torch.sum(vy ** 2).item()) + 1e-12
    pearson = pearson_num / pearson_den

    return {
        "r2": float(r2),
        "rmse": float(rmse),
        "mae": float(mae),
        "pearson": float(pearson),
    }


# ========= 训练 =========
def train(
    csv_path: str,
    root_dir: str,
    model_path: str,
    test_ratio: float,
    seed: int,
    device: str,
    batch_size: int,
) -> dict:
    df = pd.read_csv(csv_path)
    sequences = df["Sequence"].tolist()
    structures = df["Structure"].tolist()
    labels = torch.tensor(df["iptm"].values, dtype=torch.float32)

    n = len(labels)
    if n < 2:
        train_idx = torch.arange(n)
        test_idx = torch.arange(n)
    else:
        test_n = max(1, int(n * float(test_ratio)))
        test_n = min(test_n, n - 1)
        gen = torch.Generator().manual_seed(int(seed))
        perm = torch.randperm(n, generator=gen)
        test_idx = perm[:test_n]
        train_idx = perm[test_n:]

    resolved_device = _resolve_device(device)
    esm_model, batch_converter = load_esm(resolved_device)
    seq_emb = _encode_sequences(sequences, esm_model, batch_converter, resolved_device, int(batch_size))

    struct_feats = []
    for s in tqdm(structures, desc="CIF", unit="item"):
        cif_path = get_cif_path(s, root_dir)
        struct_feats.append(parse_cif(cif_path))
    struct_feats_t = torch.tensor(struct_feats, dtype=torch.float32)

    X_all = torch.cat([seq_emb, struct_feats_t], dim=1).to(resolved_device)
    y_all = labels.to(resolved_device)
    X_train = X_all[train_idx]
    y_train = y_all[train_idx]
    X_test = X_all[test_idx]
    y_test = y_all[test_idx]

    model = Model(X_all.shape[1]).to(resolved_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    for epoch in tqdm(range(50), desc="Train", unit="epoch"):
        pred_train = model(X_train)
        loss = loss_fn(pred_train, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")

    with torch.no_grad():
        train_pred = model(X_train)
        test_pred = model(X_test)
    train_metrics = _compute_regression_metrics(train_pred, y_train)
    test_metrics = _compute_regression_metrics(test_pred, y_test)

    output_dir = Path(model_path).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_payload = {
        "metrics": {
            "train": {
                **train_metrics,
                "num_samples": int(len(train_idx)),
            },
            "test": {
                **test_metrics,
                "num_samples": int(len(test_idx)),
                "test_ratio": float(test_ratio),
                "seed": int(seed),
                "device": str(resolved_device),
            },
        }
    }
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
    print(f"Metrics saved to {metrics_path}")
    return metrics_payload


# ========= 预测 =========
def predict(sequence: str, structure: str, root_dir: str, model_path: str, device: str) -> float:
    resolved_device = _resolve_device(device)
    esm_model, batch_converter = load_esm(resolved_device)
    model = Model(320 + 3)
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    model = model.to(resolved_device)

    batch = [("x", sequence)]
    _, _, tokens = batch_converter(batch)
    tokens = tokens.to(resolved_device)
    with torch.no_grad():
        out = esm_model(tokens, repr_layers=[6])
        seq_emb = out["representations"][6].mean(1)

    cif_path = get_cif_path(structure, root_dir)
    struct_feat = torch.tensor(parse_cif(cif_path), dtype=torch.float32).unsqueeze(0).to(resolved_device)
    x = torch.cat([seq_emb, struct_feat], dim=1)

    pred = model(x)
    return float(pred.item())


# ========= CLI =========
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", choices=["train", "predict"], required=True)
    parser.add_argument("--csv", help="merged_results.csv path")
    parser.add_argument("--root_dir", default=".")
    parser.add_argument("--model_path", default="iptm_model.pt")
    parser.add_argument("--test_ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", type=str, default=os.environ.get("HARNESS_DEVICE", "auto"))
    parser.add_argument("--batch_size", type=int, default=int(os.environ.get("HARNESS_BATCH_SIZE", "16")))

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
            args.test_ratio,
            args.seed,
            args.device,
            args.batch_size,
        )

    elif args.mode == "predict":
        if not args.sequence or not args.structure:
            raise ValueError("Need --sequence and --structure for prediction")

        pred = predict(
            args.sequence,
            args.structure,
            args.root_dir,
            args.model_path,
            args.device,
        )

        print("Predicted ipTM:", pred)


if __name__ == "__main__":
    main()
