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
    
    Strategy: Upper Confidence Bound (UCB) for balancing exploration and exploitation.
    """
    rng = random.Random(seed)
    
    # Get all candidate indices
    all_indices = list(range(len(candidates)))
    
    # Get already selected indices
    selected_indices = {h['candidate_index'] for h in history}
    
    # Get available indices (not yet selected)
    available_indices = [i for i in all_indices if i not in selected_indices]
    
    # If no history or all scores are equal, use random selection
    if not history:
        selected = available_indices[:batch_size]
        rng.shuffle(selected)
        return selected[:batch_size]
    
    # Build score estimates for each candidate
    # Group history by candidate index
    candidate_scores = {}
    candidate_counts = {}
    
    for h in history:
        idx = h['candidate_index']
        score = h['score']
        if idx not in candidate_scores:
            candidate_scores[idx] = 0.0
            candidate_counts[idx] = 0
        candidate_scores[idx] += score
        candidate_counts[idx] += 1
    
    # Calculate average scores for explored candidates
    candidate_avg_scores = {}
    for idx in candidate_scores:
        candidate_avg_scores[idx] = candidate_scores[idx] / candidate_counts[idx]
    
    # Calculate total number of observations for UCB exploration bonus
    total_observations = len(history)
    
    # For each available candidate, calculate UCB score
    # UCB = mean + sqrt(2 * ln(total_observations) / count)
    # For unexplored candidates, count = 1 for optimistic initialization
    ucb_scores = []
    
    # Calculate min and max observed scores for exploration
    min_observed_score = min(candidate_avg_scores.values()) if candidate_avg_scores else 0
    max_observed_score = max(candidate_avg_scores.values()) if candidate_avg_scores else 0
    
    for idx in available_indices:
        if idx in candidate_avg_scores:
            # Explored candidate
            mean_score = candidate_avg_scores[idx]
            count = candidate_counts[idx]
            exploration_bonus = np.sqrt(2 * np.log(total_observations) / count) if total_observations > 0 else 0
            ucb = mean_score + exploration_bonus
        else:
            # Unexplored candidate - use optimistic initialization
            # Explore both extremes: favor candidates that could be very negative (hits) or very positive
            # Use a mixture of min and max with higher weight on min since hits are negative
            if candidate_avg_scores:
                # Bias exploration toward negative scores (hits are at -0.4 to -0.5)
                ucb_negative = min_observed_score - 0.1 * abs(min_observed_score) if min_observed_score != 0 else -1.0
                ucb_positive = max_observed_score + 0.1 * abs(max_observed_score) if max_observed_score != 0 else 1.0
                # Blend: 80% weight on negative exploration (hits), 20% on positive
                ucb = 0.8 * ucb_negative + 0.2 * ucb_positive
            else:
                ucb = -1.0  # Start with negative bias for unexplored
        ucb_scores.append((ucb, idx))
    
    # Sort by UCB score (descending) and select top batch_size
    ucb_scores.sort(reverse=True)
    selected = [idx for _, idx in ucb_scores[:batch_size]]
    
    # Shuffle to avoid bias in case of ties
    rng.shuffle(selected)
    
    return selected