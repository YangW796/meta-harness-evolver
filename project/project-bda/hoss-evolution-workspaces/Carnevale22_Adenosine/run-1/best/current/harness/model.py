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
    
    Strategy: Hybrid exploration-exploitation with adaptive sampling
    - Early rounds: More random exploration
    - Later rounds: More exploitation of high-scoring candidates
    - Always maintain some diversity
    """
    rng = random.Random(seed)
    
    # Get already selected indices
    selected = set(h['candidate_index'] for h in history)
    
    # Get all available candidate indices
    all_indices = list(range(len(candidates)))
    available = [i for i in all_indices if i not in selected]
    
    if len(available) <= batch_size:
        return available
    
    # Calculate exploration ratio based on history size
    # More exploration in early rounds, more exploitation later
    num_rounds = len(history) // batch_size if batch_size > 0 else 0
    exploration_ratio = max(0.3, 0.8 - 0.15 * num_rounds)  # Starts at 80%, decreases to 30%
    
    # Separate exploration and exploitation
    num_explore = int(batch_size * exploration_ratio)
    num_exploit = batch_size - num_explore
    
    # Exploration: random sampling
    explore_indices = rng.sample(available, min(num_explore, len(available)))
    
    # Exploitation: select based on hits first, then scores
    if len(history) > 0 and num_exploit > 0:
        # Check if we have hits in history
        hits = [h for h in history if h.get('hit', 0) == 1]
        
        if len(hits) > 0:
            # Prioritize hit genes (they're confirmed to boost T cell proliferation)
            # Sort hits by score (ascending to prioritize most negative)
            sorted_hits = sorted(hits, key=lambda x: x['score'], reverse=False)
            top_performers = [h['candidate_index'] for h in sorted_hits[:min(50, len(sorted_hits))]]
        else:
            # Fall back to best scores if no hits yet
            # For this task, NEGATIVE scores are better (boost T cell proliferation)
            sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
            top_performers = [h['candidate_index'] for h in sorted_history[:min(50, len(sorted_history))]]
        
        # Thompson Sampling for exploitation: Bayesian bandit algorithm
        # Maintains Beta distributions for each candidate and samples from posteriors
        exploit_candidates = set()
        remaining_avail = [i for i in available if i not in explore_indices]
        
        if len(remaining_avail) > 0 and len(history) > 0:
            # Build hit/miss counts for each candidate
            candidate_successes = {}
            candidate_trials = {}
            
            for h in history:
                idx = h['candidate_index']
                if idx not in candidate_trials:
                    candidate_successes[idx] = 0
                    candidate_trials[idx] = 0
                candidate_trials[idx] += 1
                if h.get('hit', 0) == 1:
                    candidate_successes[idx] += 1
            
            # For candidates with no history, use optimistic initialization
            # For candidates with history, sample from Beta(successes + 1, failures + 1)
            ts_scores = []
            for idx in remaining_avail:
                if idx in candidate_trials:
                    successes = candidate_successes.get(idx, 0)
                    failures = candidate_trials[idx] - successes
                    # Sample from Beta posterior
                    sampled_prob = rng.betavariate(successes + 1, failures + 1)
                else:
                    # Optimistic initialization for unexplored candidates
                    # Use a high value to encourage exploration
                    sampled_prob = 0.7 + 0.3 * rng.random()
                ts_scores.append((idx, sampled_prob))
            
            # Select top candidates by Thompson Sampling score
            ts_scores.sort(key=lambda x: x[1], reverse=True)
            exploit_indices = [idx for idx, _ in ts_scores[:min(num_exploit, len(ts_scores))]]
            exploit_candidates = set(exploit_indices)
        
        selected_indices = list(explore_indices) + list(exploit_candidates)
    else:
        # Pure exploration if no history or no exploitation needed
        selected_indices = explore_indices
        remaining = [i for i in available if i not in selected_indices]
        if len(selected_indices) < batch_size:
            additional = rng.sample(remaining, min(batch_size - len(selected_indices), len(remaining)))
            selected_indices.extend(additional)
    
    return selected_indices[:batch_size]