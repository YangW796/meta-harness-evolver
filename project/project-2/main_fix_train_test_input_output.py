import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

import esm
import numpy as np
import pandas as pd
import torch
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

from index import compute_x0

try:
    from tqdm import tqdm  # type: ignore
except ModuleNotFoundError:
    def tqdm(it, **kwargs):
        return it


def _load_model_api(model_dir: str):
    model_path = Path(model_dir).expanduser().resolve()
    if not model_path.exists():
        raise ValueError(f"model_dir does not exist: {model_path}")

    spec = importlib.util.spec_from_file_location("candidate_model_module", str(model_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load model module from: {model_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    required = ["train_model", "predict_model", "save_model", "load_model"]
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise ValueError(f"model file missing required functions: {missing}")
    return module


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


def _resolve_device(device: str) -> str:
    d = (device or "auto").strip().lower()
    if d == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if d.startswith("cuda") and not torch.cuda.is_available():
        return "cpu"
    return d


def load_esm(device: str):
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
    device: str,
    batch_size: int,
) -> np.ndarray:
    out_chunks: list[np.ndarray] = []
    for start in tqdm(range(0, len(sequences), batch_size), desc="Encoding", unit="batch"):
        batch = [(str(i), sequences[i]) for i in range(start, min(len(sequences), start + batch_size))]
        _, _, tokens = batch_converter(batch)
        tokens = tokens.to(device)
        with torch.no_grad():
            out = esm_model(tokens, repr_layers=[6])
        emb = out["representations"][6].mean(1).detach().cpu().numpy().astype(np.float32, copy=False)
        out_chunks.append(emb)
    if not out_chunks:
        return np.zeros((0, 320), dtype=np.float32)
    return np.concatenate(out_chunks, axis=0)


def _load_with_split(csv_path: str, split_file: str) -> pd.DataFrame:
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
        merged = split_df
    else:
        if "Structure" not in split_df.columns:
            raise ValueError(f"split_file missing 'Structure' column for merge: {split_path}")
        merged = df.merge(split_df[["Structure", "split"]], on="Structure", how="inner")
    return merged


def train(
    csv_path: str,
    root_dir: str,
    model_path: str,
    top_ratio: float,
    seed: int,
    device: str,
    batch_size: int,
    split_file: str,
    model_dir: str,
) -> dict:
    model_api = _load_model_api(model_dir)
    df = _load_with_split(csv_path, split_file)
    df["x"] = compute_x0(df)

    split_values = df["split"].astype(str).str.lower()
    train_idx = np.flatnonzero(split_values == "train")
    test_idx = np.flatnonzero(split_values == "test")
    if len(train_idx) == 0 or len(test_idx) == 0:
        raise ValueError(f"Invalid split distribution in split_file: train={len(train_idx)}, test={len(test_idx)}")

    sequences = df["Sequence"].tolist()
    structures = df["Structure"].tolist()

    resolved_device = _resolve_device(device)
    esm_model, batch_converter = load_esm(resolved_device)
    seq_emb = _encode_sequences(sequences, esm_model, batch_converter, resolved_device, int(batch_size))

    struct_feats = []
    for structure in tqdm(structures, desc="CIF", unit="item"):
        cif = get_cif_path(structure, root_dir)
        struct_feats.append(parse_cif(cif))
    struct_feats_np = np.asarray(struct_feats, dtype=np.float32)

    X_all = np.concatenate([seq_emb, struct_feats_np], axis=1).astype(np.float32, copy=False)
    y_all = df["x"].to_numpy(dtype=np.float32, copy=False)

    X_train = X_all[train_idx]
    y_train = y_all[train_idx]
    X_test = X_all[test_idx]
    y_test = y_all[test_idx]

    model = model_api.train_model(
        X_train=X_train,
        y_train=y_train,
        input_dim=int(X_all.shape[1]),
        device=resolved_device,
        seed=int(seed),
    )

    test_pred = model_api.predict_model(model=model, X=X_test, device=resolved_device)
    true_label = _make_topk_labels(y_test, top_ratio)
    pred_label = _make_topk_labels(test_pred, top_ratio)
    f1 = float(f1_score(true_label, pred_label))

    model_api.save_model(model, model_path)
    print(f"Model saved to {model_path}")
    print(f"F1 score (top-k): {f1:.6f}")

    output_dir = Path(model_path).resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    top_k_test = int(max(1, int(len(y_test) * top_ratio)))
    metrics_payload = {
        "metrics": {
            "test": {
                "f1": f1,
                "top_ratio": float(top_ratio),
                "top_k": top_k_test,
                "num_samples": int(len(test_idx)),
                "seed": int(seed),
                "device": str(resolved_device),
                "split_file": str(Path(split_file)),
            }
        }
    }
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")
    print(f"Metrics saved to {metrics_path}")
    return metrics_payload


def predict(sequence: str, structure: str, root_dir: str, model_path: str, device: str, model_dir: str) -> float:
    model_api = _load_model_api(model_dir)
    resolved_device = _resolve_device(device)
    esm_model, batch_converter = load_esm(resolved_device)

    batch = [("x", sequence)]
    _, _, tokens = batch_converter(batch)
    tokens = tokens.to(resolved_device)
    with torch.no_grad():
        out = esm_model(tokens, repr_layers=[6])
        seq_emb = out["representations"][6].mean(1).detach().cpu().numpy().astype(np.float32, copy=False)

    cif_path = get_cif_path(structure, root_dir)
    struct_feat = np.asarray(parse_cif(cif_path), dtype=np.float32).reshape(1, -1)
    x = np.concatenate([seq_emb, struct_feat], axis=1).astype(np.float32, copy=False)

    model = model_api.load_model(model_path, input_dim=int(x.shape[1]), device=resolved_device)
    pred = model_api.predict_model(model=model, X=x, device=resolved_device)
    return float(pred.reshape(-1)[0])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "predict"], required=True)
    parser.add_argument("--csv", help="merged_results.csv path")
    parser.add_argument("--root_dir", required=True)
    parser.add_argument("--model_path", default="iptm_model.pt")
    parser.add_argument("--top_ratio", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", type=str, default=os.environ.get("HARNESS_DEVICE", "auto"))
    parser.add_argument("--batch_size", type=int, default=int(os.environ.get("HARNESS_BATCH_SIZE", "16")))
    parser.add_argument("--split_file", default="train_test_split.csv")
    parser.add_argument("--model_dir", default="model.py")
    parser.add_argument("--sequence", help="sequence for prediction")
    parser.add_argument("--structure", help="structure name")
    args = parser.parse_args()

    if args.mode == "train":
        if not args.csv:
            raise ValueError("Need --csv for training")
        train(
            csv_path=args.csv,
            root_dir=args.root_dir,
            model_path=args.model_path,
            top_ratio=args.top_ratio,
            seed=args.seed,
            device=args.device,
            batch_size=args.batch_size,
            split_file=args.split_file,
            model_dir=args.model_dir,
        )
        return 0

    if not args.sequence or not args.structure:
        raise ValueError("Need --sequence and --structure for prediction")
    pred_value = predict(
        sequence=args.sequence,
        structure=args.structure,
        root_dir=args.root_dir,
        model_path=args.model_path,
        device=args.device,
        model_dir=args.model_dir,
    )
    print(f"Predicted x: {pred_value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
