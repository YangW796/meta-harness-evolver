import torch
import torch.nn as nn
import esm
import pandas as pd
import os
import argparse

# ========= CIF解析 =========
def parse_cif(cif_path):
    atom_count = 0
    residue_set = set()
    chain_set = set()

    if not os.path.exists(cif_path):
        return [0, 0, 0]

    with open(cif_path) as f:
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
def get_cif_path(structure, root_dir):
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
    def __init__(self, dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


# ========= 加载ESM =========
def load_esm():
    print("Loading ESM...")
    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
    batch_converter = alphabet.get_batch_converter()
    model.eval()
    return model, batch_converter


# ========= 训练 =========
def train(csv_path, root_dir, model_path):

    df = pd.read_csv(csv_path)

    sequences = df["Sequence"].tolist()
    structures = df["Structure"].tolist()
    labels = torch.tensor(df["iptm"].values, dtype=torch.float32)

    esm_model, batch_converter = load_esm()

    print("Encoding sequences...")
    batch = [(str(i), seq) for i, seq in enumerate(sequences)]
    _, _, tokens = batch_converter(batch)

    with torch.no_grad():
        out = esm_model(tokens, repr_layers=[6])

    seq_emb = out["representations"][6].mean(1)

    print("Parsing CIF...")
    struct_feats = []
    for s in structures:
        cif_path = get_cif_path(s, root_dir)
        feat = parse_cif(cif_path)
        struct_feats.append(feat)

    struct_feats = torch.tensor(struct_feats, dtype=torch.float32)

    X = torch.cat([seq_emb, struct_feats], dim=1)

    model = Model(X.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    print("Training...")
    for epoch in range(50):
        pred = model(X)
        loss = loss_fn(pred, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch}: loss={loss.item():.4f}")

    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")


# ========= 预测 =========
def predict(sequence, structure, root_dir, model_path):

    esm_model, batch_converter = load_esm()

    model = Model(320 + 3)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # sequence
    batch = [("x", sequence)]
    _, _, tokens = batch_converter(batch)

    with torch.no_grad():
        out = esm_model(tokens, repr_layers=[6])
        seq_emb = out["representations"][6].mean(1)

    # structure
    cif_path = get_cif_path(structure, root_dir)
    struct_feat = torch.tensor(parse_cif(cif_path), dtype=torch.float32).unsqueeze(0)

    x = torch.cat([seq_emb, struct_feat], dim=1)

    pred = model(x)
    return pred.item()


# ========= CLI =========
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", choices=["train", "predict"], required=True)
    parser.add_argument("--csv", help="merged_results.csv path")
    parser.add_argument("--root_dir", default=".")
    parser.add_argument("--model_path", default="iptm_model.pt")

    parser.add_argument("--sequence", help="sequence for prediction")
    parser.add_argument("--structure", help="structure name")

    args = parser.parse_args()

    if args.mode == "train":
        if not args.csv:
            raise ValueError("Need --csv for training")
        train(args.csv, args.root_dir, args.model_path)

    elif args.mode == "predict":
        if not args.sequence or not args.structure:
            raise ValueError("Need --sequence and --structure for prediction")

        pred = predict(
            args.sequence,
            args.structure,
            args.root_dir,
            args.model_path
        )

        print("Predicted ipTM:", pred)


if __name__ == "__main__":
    main()
