from __future__ import annotations

import numpy as np

def select(candidates, history, batch_size, seed) -> list[int]:
    """
    Selection policy for Project-BDA.

    Contract (MUST KEEP EXACTLY):
        select(candidates, history, batch_size, seed) -> list[int]

    Inputs:
    - candidates: list[dict]
        - single-gene datasets: each item includes {"gene": "<HGNC>"}
        - gene-pair datasets: each item includes {"gene_a": "<HGNC>", "gene_b": "<HGNC>"}
        - gene search (optional): when enabled by the runner, you may call:
          - import bda_tools
          - bda_tools.gene_search(query_gene: str, k: int = 10, diverse: bool = False) -> list[int]
    - history: list[dict]
        - each item includes at least:
          - candidate_index: int
          - score: float
          - hit: int (0/1) if enabled by runner
    - batch_size: int
    - seed: int

    Output:
    - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
    """
    n = len(candidates)
    if n <= 0:
        return []

    already: set[int] = set()
    for r in history or []:
        try:
            already.add(int(r.get("candidate_index", -1)))
        except Exception:
            continue

    remaining = [i for i in range(n) if i not in already]
    rng = np.random.default_rng(int(seed))
    if remaining:
        rng.shuffle(remaining)
    return [int(x) for x in remaining[: int(batch_size)]]
