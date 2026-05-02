from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np

_GENE_SEARCH_READY = False
_GENES: list[str] | None = None
_FEATS_SUB: np.ndarray | None = None
_GENE_TO_SUB: dict[str, int] | None = None
_SUB_TO_CAND_IDX: list[int] | None = None
_CAND_GENE_SET: set[str] | None = None


def init_gene_search(achilles_csv: str, candidate_genes: list[str]) -> bool:
    global _GENE_SEARCH_READY, _GENES, _FEATS_SUB, _GENE_TO_SUB, _SUB_TO_CAND_IDX, _CAND_GENE_SET

    _GENE_SEARCH_READY = False
    _GENES = None
    _FEATS_SUB = None
    _GENE_TO_SUB = None
    _SUB_TO_CAND_IDX = None
    _CAND_GENE_SET = None

    csv_path = Path(achilles_csv).expanduser().resolve()
    if not csv_path.exists():
        return False

    try:
        import pandas as pd
    except Exception:
        return False

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return False

    if df.empty:
        return False

    gene_col = None
    for c in ["gene", "Gene", "GENE", "symbol", "hgnc_symbol", "Unnamed: 0"]:
        if c in df.columns:
            gene_col = c
            break
    if gene_col is None:
        gene_col = df.columns[0]

    genes = [str(x).strip() for x in df[gene_col].tolist()]
    feat_df = df.drop(columns=[gene_col], errors="ignore")
    feat_df = feat_df.select_dtypes(include=["number"]).fillna(0.0)
    feats = feat_df.to_numpy(dtype=np.float32, copy=False)
    if feats.ndim != 2 or feats.shape[0] != len(genes) or feats.shape[1] == 0:
        return False

    norms = np.linalg.norm(feats, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-8)
    feats = feats / norms

    ach_gene_to_row: dict[str, int] = {}
    for i, g in enumerate(genes):
        if g and g not in ach_gene_to_row:
            ach_gene_to_row[g] = i

    cand_gene_to_idx: dict[str, int] = {}
    for i, g in enumerate(candidate_genes):
        gg = str(g).strip()
        if gg and gg not in cand_gene_to_idx:
            cand_gene_to_idx[gg] = int(i)

    sub_rows: list[int] = []
    sub_to_cand_idx: list[int] = []
    gene_to_sub: dict[str, int] = {}
    for g, cand_idx in cand_gene_to_idx.items():
        row = ach_gene_to_row.get(g)
        if row is None:
            continue
        gene_to_sub[g] = len(sub_rows)
        sub_rows.append(int(row))
        sub_to_cand_idx.append(int(cand_idx))

    if not sub_rows:
        return False

    feats_sub = feats[np.asarray(sub_rows, dtype=np.int64)]

    _GENES = genes
    _FEATS_SUB = feats_sub
    _GENE_TO_SUB = gene_to_sub
    _SUB_TO_CAND_IDX = sub_to_cand_idx
    _CAND_GENE_SET = set(cand_gene_to_idx.keys())
    _GENE_SEARCH_READY = True
    return True


def gene_search(query_gene: str, k: int = 10, diverse: bool = False) -> list[int]:
    if not _GENE_SEARCH_READY:
        return []
    if _FEATS_SUB is None or _GENE_TO_SUB is None or _SUB_TO_CAND_IDX is None:
        return []

    q = str(query_gene).strip()
    qi = _GENE_TO_SUB.get(q)
    if qi is None:
        return []

    qv = _FEATS_SUB[int(qi)]
    sims = _FEATS_SUB @ qv
    order = np.argsort(sims, kind="mergesort")
    if not diverse:
        order = order[::-1]

    out: list[int] = []
    for j in order.tolist():
        cand_idx = int(_SUB_TO_CAND_IDX[int(j)])
        if cand_idx not in out:
            out.append(cand_idx)
        if len(out) >= int(k):
            break

    log_path = str(os.environ.get("BDA_GENE_SEARCH_LOG_PATH", "")).strip()
    if log_path:
        try:
            p = Path(log_path).expanduser().resolve()
            payload: dict = {}
            if p.exists():
                try:
                    payload = json.loads(p.read_text(encoding="utf-8"))
                except Exception:
                    payload = {}
            calls = payload.get("calls")
            if not isinstance(calls, list):
                calls = []
            calls.append(
                {
                    "query_gene": q,
                    "k": int(k),
                    "diverse": bool(diverse),
                    "returned_indices": [int(x) for x in out],
                }
            )
            if len(calls) > 500:
                calls = calls[-500:]
            payload["calls"] = calls
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
    return out
