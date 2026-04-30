from __future__ import annotations

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
    import numpy as np
    
    # Set random seed for reproducibility
    rng = np.random.RandomState(seed)
    
    # Get all candidate indices
    n_candidates = len(candidates)
    candidate_indices = list(range(n_candidates))
    
    # Remove already selected candidates
    selected_indices = {h['candidate_index'] for h in history}
    available_indices = [i for i in candidate_indices if i not in selected_indices]
    
    # If no history (first round), use random selection with some diversity
    if not history:
        # Simple random sampling for the first batch
        selected = rng.choice(available_indices, size=min(batch_size, len(available_indices)), replace=False)
        return selected.tolist()
    
    # Build statistics from history
    # Track mean score and count for each candidate
    scores = {}
    counts = {}
    
    for h in history:
        idx = h['candidate_index']
        score = h['score']
        if idx not in scores:
            scores[idx] = 0.0
            counts[idx] = 0
        scores[idx] += score
        counts[idx] += 1
    
    # Calculate mean scores
    mean_scores = {idx: scores[idx] / counts[idx] for idx in scores}
    
    # UCB algorithm: balance mean reward vs exploration bonus
    total_pulls = len(history)
    ucb_scores = []
    
    for idx in available_indices:
        if idx in mean_scores:
            # Exploitation term: absolute mean score (prioritize extreme effects)
            # Since hits are defined by large deviations in either direction
            exploitation = abs(mean_scores[idx])
            # Exploration term: uncertainty bonus with tuned constant and epsilon regularization
            # Use a slightly higher exploration constant (2.5 vs 2.0) to encourage more exploration
            # Add small epsilon to prevent division by zero and handle low-count candidates
            exploration = np.sqrt(2.5 * np.log(total_pulls + 1) / (counts[idx] + 1e-6))
            ucb = exploitation + exploration
        else:
            # Never-seen candidates get high priority for exploration
            ucb = float('inf')
        ucb_scores.append((ucb, idx))
    
    # Sort by UCB score (descending) and select top candidates
    ucb_scores.sort(reverse=True)
    selected = [idx for _, idx in ucb_scores[:batch_size]]
    
    # If we don't have enough high-UCB candidates, fill with random unexplored ones
    if len(selected) < batch_size:
        remaining = [idx for idx in available_indices if idx not in selected]
        needed = batch_size - len(selected)
        if remaining:
            additional = rng.choice(remaining, size=min(needed, len(remaining)), replace=False)
            selected.extend(additional.tolist())
    
    return selected
