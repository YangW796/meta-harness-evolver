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
    
         # Exploitation: Use hit-based weighting when available, fall back to score-based weighting
        if exploit_count > 0 and len(history) > 0:
            # Check if hit information is available
            has_hits = 'hit' in history[0]
            
            if has_hits:
                # Use hit-based weighting: prioritize candidates that were hits
                # Weight by both hit status and score extremity
                hit_weights = []
                for h in history:
                    # Base weight: 10x for hits, 1x for non-hits
                    base_weight = 10.0 if h['hit'] == 1 else 1.0
                    # Multiply by score extremity (absolute deviation from median)
                    scores = [h['score'] for h in history]
                    median_score = np.median(scores)
                    score_weight = abs(h['score'] - median_score) + 1e-6
                    hit_weights.append(base_weight * score_weight)
                weights = np.array(hit_weights)
            else:
                # Fall back to score-based weighting
                scores = [h['score'] for h in history]
                median_score = np.median(scores)
                abs_deviations = [abs(h['score'] - median_score) for h in history]
                weights = np.array(abs_deviations) + 1e-6
            
            weights = weights / weights.sum()  # Normalize
            
            # Sample candidate indices from history with replacement, using the weights
            exploit_indices = np.random.choice(len(history), size=min(exploit_count * 3, len(history)), replace=True, p=weights)
            
            # Convert to actual selected indices from available pool
            exploit_set = set()
            for idx in exploit_indices:
                if len(exploit_set) >= exploit_count:
                    break
                # Add the historically high-value candidate if still available
                hist_idx = history[idx]['candidate_index']
                if hist_idx in available:
                    exploit_set.add(hist_idx)
            
            # If we don't have enough from direct hits, supplement with random available candidates
            if len(exploit_set) < exploit_count:
                remaining_needed = exploit_count - len(exploit_set)
                supplemental = rng.sample(available, min(remaining_needed, len(available)))
                exploit_set.update(supplemental)
            
            selected.extend(list(exploit_set))
            available = [i for i in available if i not in selected]    
    # Exploration: random selection from remaining available
    if explore_count > 0 and available:
        explore_selection = rng.sample(available, min(explore_count, len(available)))
        selected.extend(explore_selection)
    
    return selected[:batch_size]