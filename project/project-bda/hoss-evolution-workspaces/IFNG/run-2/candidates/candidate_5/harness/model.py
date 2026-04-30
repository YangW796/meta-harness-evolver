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
    
         Strategy: Gradient-based adaptive bandit selection with score-driven exploration.    """
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
    
    # Separate hits from non-hits for better modeling
    hit_indices = [h['candidate_index'] for h in history if h.get('hit', 0) == 1]
    hit_scores = [h['score'] for h in history if h.get('hit', 0) == 1]
    
    # Try to use gene search if available (for both exploitation and exploration)
    try:
        import bda_tools
        
        # If we have hits, prioritize exploring similar genes (exploitation)
        if hit_indices and len(hit_indices) > 0:
            # Find the best hit (most negative score)
            best_hit_idx = hit_indices[np.argmin(hit_scores)]
            best_hit_gene = candidates[best_hit_idx].get('gene')
            
            if best_hit_gene:
                # Search for similar genes
                similar_indices = bda_tools.gene_search(best_hit_gene, k=20, diverse=False)
                
                # Filter to available indices only
                similar_available = [idx for idx in similar_indices if idx in available_indices]
                
                # If we found similar genes, include some in the selection
                if similar_available:
                    # Take up to 30% of batch from similar genes
                    num_similar = min(len(similar_available), batch_size // 3)
                    selected = similar_available[:num_similar]
                    remaining_batch = batch_size - len(selected)
                    
                                             # Fill the rest using Gradient Bandit Selection
                                            if remaining_batch > 0:
                                                thompson_selected = _gradient_bandit_selection(
                                                    candidates, history, available_indices, 
                                                    selected, remaining_batch, rng
                                                )                        selected.extend(thompson_selected)
                    
                    rng.shuffle(selected)
                    return selected[:batch_size]
        else:
            # No hits yet: use diverse gene search for proactive exploration
            # Pick a random gene from history to start diverse search
            if history:
                # Select a random gene from those already explored
                random_history_gene = rng.choice(history)
                start_gene = candidates[random_history_gene['candidate_index']].get('gene')
                
                if start_gene:
                    # Search for diverse genes to explore different gene families
                    diverse_indices = bda_tools.gene_search(start_gene, k=30, diverse=True)
                    
                    # Filter to available indices only
                    diverse_available = [idx for idx in diverse_indices if idx in available_indices]
                    
                    # If we found diverse genes, include some in the selection
                    if diverse_available:
                        # Take up to 45% of batch from diverse exploration
                        num_diverse = min(len(diverse_available), batch_size * 45 // 100)
                        selected = diverse_available[:num_diverse]
                        remaining_batch = batch_size - len(selected)
                        
                        # Fill the rest using Gradient Bandit Selection
                        if remaining_batch > 0:
                            thompson_selected = _gradient_bandit_selection(
                                candidates, history, available_indices, 
                                selected, remaining_batch, rng
                            )
                            selected.extend(thompson_selected)
                        
                        rng.shuffle(selected)
                        return selected[:batch_size]
    except ImportError:
        # Gene search not available, fall back to pure Thompson Sampling
        pass
    except Exception:
        # Gene search failed, fall back to pure Thompson Sampling
        pass
    
         # Use pure Gradient Bandit Selection
        selected = _gradient_bandit_selection(candidates, history, available_indices, [], batch_size, rng)    rng.shuffle(selected)
    return selected[:batch_size]


def _gradient_bandit_selection(candidates, history, available_indices, exclude_indices, batch_size, rng):
    """
    Gradient-based adaptive bandit selection using direct score optimization.
    
    Strategy: Uses score values directly to compute selection probabilities via
    exponential weighting (softmax), adapting exploration based on score variance.
    """
    
    # Filter out excluded indices
    available = [idx for idx in available_indices if idx not in exclude_indices]
    
    if len(available) <= batch_size:
        return available[:batch_size]
    
    # Extract all scores for normalization and statistics
    all_scores = [h['score'] for h in history]
    min_score = min(all_scores)
    max_score = max(all_scores)
    score_range = max_score - min_score
    
    # Calculate score statistics for adaptive exploration
    mean_score = np.mean(all_scores)
    std_score = np.std(all_scores) if len(all_scores) > 1 else 1.0
    
    # Build score accumulators for each candidate
    candidate_scores = {}
    candidate_counts = {}
    
    for h in history:
        idx = h['candidate_index']
        score = h['score']
        
        if idx not in candidate_scores:
            candidate_scores[idx] = 0.0
            candidate_counts[idx] = 0
        
        # Accumulate scores (we want more negative = better)
        candidate_scores[idx] += score
        candidate_counts[idx] += 1
    
    # Compute average scores for each candidate
    candidate_avg_scores = {}
    for idx in candidate_scores:
        candidate_avg_scores[idx] = candidate_scores[idx] / candidate_counts[idx]
    
    # Adaptive temperature for softmax based on score variance
    # Higher variance = higher temperature = more exploration
    # Lower variance = lower temperature = more exploitation
    temperature = max(0.1, std_score * 2.0)
    
    # Compute selection weights using softmax on normalized scores
    weights = []
    indices_for_weights = []
    
    for idx in available:
        if idx in candidate_avg_scores:
            # Explored candidate: use its average score
            avg_score = candidate_avg_scores[idx]
        else:
            # Unexplored candidate: use optimistic estimate
            # Base it on the best observed score with some randomness
            best_score = min(all_scores) if all_scores else 0
            # Add exploration bonus: more uncertain = more optimistic
            avg_score = best_score - std_score * 0.5
        
        # Normalize score to emphasize differences
        if score_range > 0.001:
            normalized_score = (avg_score - mean_score) / score_range
        else:
            normalized_score = 0.0
        
        # Apply softmax with adaptive temperature
        # We negate because we want lower (more negative) scores to have higher probability
        weight = np.exp(-normalized_score / temperature)
        
        weights.append(weight)
        indices_for_weights.append(idx)
    
    # Convert to probabilities
    weight_sum = sum(weights)
    if weight_sum > 0:
        probabilities = [w / weight_sum for w in weights]
    else:
        # Fallback to uniform if all weights are zero
        probabilities = [1.0 / len(weights)] * len(weights)
    
    # Sample indices based on probabilities (without replacement)
    # Use numpy's choice with probabilities
    selected_indices = np.random.choice(
        indices_for_weights,
        size=min(batch_size, len(indices_for_weights)),
        replace=False,
        p=probabilities
    ).tolist()
    
    return selected_indices