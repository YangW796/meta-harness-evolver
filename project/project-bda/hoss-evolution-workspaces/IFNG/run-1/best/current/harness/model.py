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
    
    Strategy: Thompson Sampling with Beta distribution for balancing exploration and exploitation.
    """
    rng = random.Random(seed)
    np.random.seed(seed)
    
    # Get all candidate indices
    all_indices = list(range(len(candidates)))
    
    # Get already selected indices
    selected_indices = {h['candidate_index'] for h in history}
    
    # Get available indices (not yet selected)
    available_indices = [i for i in all_indices if i not in selected_indices]
    
    # If no history, use random selection
    if not history:
        selected = available_indices[:batch_size]
        rng.shuffle(selected)
        return selected[:batch_size]
    
    # Normalize scores to [0, 1] for Beta distribution
    # Hits have negative scores around -0.4 to -0.5, we want these to have low normalized scores
    all_scores = [h['score'] for h in history]
    min_score = min(all_scores)
    max_score = max(all_scores)
    score_range = max_score - min_score
    
    # Build success/failure counts for each candidate
    # For Thompson Sampling with Beta distribution, we model the probability of "success"
    # Here "success" means being a hit (having a very negative score)
    candidate_successes = {}
    candidate_failures = {}
    
    for h in history:
        idx = h['candidate_index']
        score = h['score']
        
        # Normalize score to [0, 1] where 0 is worst (most negative) and 1 is best
        if score_range > 0:
            normalized_score = (score - min_score) / score_range
        else:
            normalized_score = 0.5
        
        # For hits (very negative scores), normalized_score will be close to 0
        # We define "success" as finding a hit, so we want to maximize (1 - normalized_score)
        # The more negative the score, the higher the success probability
        
        if idx not in candidate_successes:
            candidate_successes[idx] = 0
            candidate_failures[idx] = 0
        
        # Accumulate successes and failures based on normalized score
        # Use the complement since hits (what we want) have low normalized scores
        success_weight = 1.0 - normalized_score
        failure_weight = normalized_score
        
        # Add to counts (with some scaling to get reasonable Beta parameters)
        candidate_successes[idx] += success_weight
        candidate_failures[idx] += failure_weight
    
    # For Thompson Sampling, we sample from Beta(alpha, beta) for each candidate
    # where alpha = successes + 1, beta = failures + 1 (add-1 smoothing for uninformed prior)
    thompson_samples = []
    
    for idx in available_indices:
        if idx in candidate_successes:
            # Explored candidate: use observed successes/failures
            alpha = candidate_successes[idx] + 1
            beta = candidate_failures[idx] + 1
        else:
            # Unexplored candidate: use optimistic prior
            # Bias toward exploration of potentially good candidates (hits)
            # Use alpha > beta to favor success (finding hits)
            alpha = 3  # Higher alpha = more optimistic about success
            beta = 1
        
        # Sample from Beta distribution
        sample = np.random.beta(alpha, beta)
        thompson_samples.append((sample, idx))
    
    # Sort by Thompson sample (descending) and select top batch_size
    thompson_samples.sort(reverse=True)
    selected = [idx for _, idx in thompson_samples[:batch_size]]
    
    # Shuffle to avoid bias in case of ties
    rng.shuffle(selected)
    
    return selected