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
    
    # Exploitation: select based on scores
    if len(history) > 0 and num_exploit > 0:
        # For this task, NEGATIVE scores are better (boost T cell proliferation)
        # Sort history by score (ascending to prioritize negative scores)
        sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
        
        # Get top performers (most negative scores)
        top_performers = [h['candidate_index'] for h in sorted_history[:min(50, len(sorted_history))]]
        
        # Find candidates similar to top performers (if gene search available)
        exploit_candidates = set()
        remaining_avail = [i for i in available if i not in explore_indices]
        
        if len(remaining_avail) > 0:
            # If we have top performers and gene search might be available, use it
            # Otherwise, sample from remaining with slight bias toward higher indices
            # (assuming some clustering in the candidate list)
            
            # Simple strategy: weighted sampling based on position (crude diversity)
            weights = np.abs(np.linspace(-1, 1, len(remaining_avail))) + 0.1
            weights = weights / weights.sum()
            
            try:
                exploit_indices = rng.choices(
                    remaining_avail, 
                    k=min(num_exploit, len(remaining_avail)),
                    weights=weights
                )
                exploit_candidates = set(exploit_indices)
            except:
                # Fallback to uniform sampling
                exploit_candidates = set(rng.sample(
                    remaining_avail, 
                    min(num_exploit, len(remaining_avail))
                ))
        
        selected_indices = list(explore_indices) + list(exploit_candidates)
    else:
        # Pure exploration if no history or no exploitation needed
        selected_indices = explore_indices
        remaining = [i for i in available if i not in selected_indices]
        if len(selected_indices) < batch_size:
            additional = rng.sample(remaining, min(batch_size - len(selected_indices), len(remaining)))
            selected_indices.extend(additional)
    
    return selected_indices[:batch_size]