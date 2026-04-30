from __future__ import annotations
import random
import numpy as np
from collections import defaultdict

def select(candidates, history, batch_size, seed) -> list[int]:
    """
    Selection policy for Project-BDA using Thompson Sampling.
    
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
    
    Thompson Sampling implementation for perturbation search.
    """
    rng = random.Random(seed)
    np.random.seed(seed)
    
    # Get already selected indices
    already_selected = {h['candidate_index'] for h in history}
    
    # Get all available candidate indices
    all_indices = list(range(len(candidates)))
    available = [i for i in all_indices if i not in already_selected]
    
    # If no history (first round), use random exploration
    if not history:
        selected = rng.sample(available, min(batch_size, len(available)))
        return selected
    
    # Thompson Sampling strategy
    # Model each candidate's probability of being a hit using Beta distribution
    # Success = hit (score <= threshold), Failure = non-hit
    
    # Determine hit threshold: use 5th percentile of absolute scores as cutoff for "extreme"
    abs_scores = [abs(h['score']) for h in history]
    hit_threshold = np.percentile(abs_scores, 95)  # Top 5% most extreme scores are hits
    
    # Count successes (hits) and failures (non-hits) for each candidate
    # Since we can't track individual candidates that haven't been tested,
    # we use a Bayesian approach with empirical priors
    
    # Calculate empirical hit rate from history
    if 'hit' in history[0]:
        # Use provided hit labels if available
        total_hits = sum(1 for h in history if h['hit'] == 1)
        total_trials = len(history)
    else:
        # Define hits as extreme scores (top 5% by absolute value)
        total_hits = sum(1 for h in history if abs(h['score']) >= hit_threshold)
        total_trials = len(history)
    
    empirical_hit_rate = total_hits / total_trials if total_trials > 0 else 0.05
    
    # Beta distribution parameters (Bayesian prior)
    # Start with weak prior centered at empirical hit rate
    alpha_prior = max(1, empirical_hit_rate * 10)  # Success count
    beta_prior = max(1, (1 - empirical_hit_rate) * 10)  # Failure count
    
    # For each available candidate, sample from posterior
    # Candidates with no history get sampled from prior
    # Candidates with history get sampled from posterior (alpha + successes, beta + failures)
    
    # Group history by candidate to track per-candidate statistics
    candidate_stats = defaultdict(lambda: {'successes': 0, 'trials': 0})
    
    for h in history:
        idx = h['candidate_index']
        if 'hit' in h:
            is_hit = h['hit'] == 1
        else:
            is_hit = abs(h['score']) >= hit_threshold
        
        candidate_stats[idx]['successes'] += int(is_hit)
        candidate_stats[idx]['trials'] += 1
    
    # Sample theta (probability of being a hit) for each available candidate
    sampled_probs = []
    for idx in available:
        if idx in candidate_stats:
            # Posterior: Beta(alpha_prior + successes, beta_prior + failures)
            successes = candidate_stats[idx]['successes']
            failures = candidate_stats[idx]['trials'] - successes
            alpha_post = alpha_prior + successes
            beta_post = beta_prior + failures
        else:
            # Prior: Beta(alpha_prior, beta_prior)
            alpha_post = alpha_prior
            beta_post = beta_prior
        
        # Sample from Beta distribution
        theta = np.random.beta(alpha_post, beta_post)
        sampled_probs.append((idx, theta))
    
    # Sort by sampled probability (descending) and select top batch_size
    sampled_probs.sort(key=lambda x: x[1], reverse=True)
    selected = [idx for idx, _ in sampled_probs[:batch_size]]
    
    return selected