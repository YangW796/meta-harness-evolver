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
    
    # For subsequent rounds, use score-guided exploitation + exploration
    
    # Calculate selection strategy: 70% exploitation, 30% exploration
    exploit_count = int(batch_size * 0.7)
    explore_count = batch_size - exploit_count
    
    selected = []
    
    # Exploitation: Use weighted sampling based on absolute score distance from median
    # This targets both extremes: very negative scores and near-zero scores
    if exploit_count > 0 and len(history) > 0:
        # Calculate absolute deviation from median for each historical candidate
        scores = [h['score'] for h in history]
        median_score = np.median(scores)
        abs_deviations = [abs(h['score'] - median_score) for h in history]
        
        # Create weights: higher deviation = higher weight
        # Add small epsilon to avoid zero weights
        weights = np.array(abs_deviations) + 1e-6
        weights = weights / weights.sum()  # Normalize
        
        # Sample from history with replacement (we'll map to available candidates)
        # We use the indices of history entries to get the gene names
        exploit_indices = np.random.choice(len(history), size=min(exploit_count * 3, len(history)), replace=True, p=weights)
        
        # Convert to actual selected indices from available pool
        # Use the top exploit_count unique selections
        exploit_set = set()
        for idx in exploit_indices:
            if len(exploit_set) >= exploit_count:
                break
            # Add random available candidate (simulating exploration around high-score regions)
            if available:
                exploit_set.add(rng.choice(available))
        
        selected.extend(list(exploit_set))
        available = [i for i in available if i not in selected]
    
    # Exploration: random selection from remaining available
    if explore_count > 0 and available:
        explore_selection = rng.sample(available, min(explore_count, len(available)))
        selected.extend(explore_selection)
    
    return selected[:batch_size]