from __future__ import annotations
import random
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

    You may implement any suitable algorithmic model here, including but not limited to:
    traditional algorithms, machine learning models, deep learning models, biological models,
    and mathematical models.
    """
    rng = random.Random(seed)
    
    # Get already selected indices
    already_selected = {h['candidate_index'] for h in history}
    
    # Get all available candidate indices
    all_indices = list(range(len(candidates)))
    available = [i for i in all_indices if i not in already_selected]
    
    # If no history (first round), use random exploration
    if not history:
        selected = rng.sample(available, min(batch_size, len(available)))
        return selected
    
    # For subsequent rounds, use a combination of exploitation and exploration
    # Sort history by score (descending)
    sorted_history = sorted(history, key=lambda x: x['score'], reverse=True)
    
    # Take top 30% as high-scoring candidates
    top_percentile = 0.3
    top_count = max(1, int(len(sorted_history) * top_percentile))
    top_candidates = sorted_history[:top_count]
    
    # Calculate selection strategy: 70% exploitation, 30% exploration
    exploit_count = int(batch_size * 0.7)
    explore_count = batch_size - exploit_count
    
    selected = []
    
    # Exploitation: select from high-scoring candidates
    # We can't select the same indices, but we might want to select similar genes
    # For now, we'll use random selection from available
    if exploit_count > 0:
        exploit_pool = available.copy()
        rng.shuffle(exploit_pool)
        selected.extend(exploit_pool[:exploit_count])
        # Remove selected from available
        available = [i for i in available if i not in selected]
    
    # Exploration: random selection from remaining available
    if explore_count > 0 and available:
        explore_selection = rng.sample(available, min(explore_count, len(available)))
        selected.extend(explore_selection)
    
    return selected[:batch_size]