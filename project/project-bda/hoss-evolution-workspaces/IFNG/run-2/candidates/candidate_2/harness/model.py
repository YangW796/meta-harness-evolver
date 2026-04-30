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
    
    Strategy: Improved Thompson Sampling with adaptive exploration and hit-based exploitation.
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
                    
                    # Fill the rest using Thompson Sampling
                    if remaining_batch > 0:
                        thompson_selected = _thompson_sampling(
                            candidates, history, available_indices, 
                            selected, remaining_batch, rng
                        )
                        selected.extend(thompson_selected)
                    
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
                        # Take up to 40% of batch from diverse exploration
                        num_diverse = min(len(diverse_available), batch_size * 2 // 5)
                        selected = diverse_available[:num_diverse]
                        remaining_batch = batch_size - len(selected)
                        
                        # Fill the rest using Thompson Sampling
                        if remaining_batch > 0:
                            thompson_selected = _thompson_sampling(
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
    
    # Use pure Thompson Sampling
    selected = _thompson_sampling(candidates, history, available_indices, [], batch_size, rng)
    rng.shuffle(selected)
    return selected[:batch_size]


def _thompson_sampling(candidates, history, available_indices, exclude_indices, batch_size, rng):
    """Helper function for Thompson Sampling with Beta distribution."""
    
    # Filter out excluded indices
    available = [idx for idx in available_indices if idx not in exclude_indices]
    
    if len(available) <= batch_size:
        return available[:batch_size]
    
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
    
    for idx in available:
        if idx in candidate_successes:
            # Explored candidate: use observed successes/failures
            alpha = candidate_successes[idx] + 1
            beta = candidate_failures[idx] + 1
        else:
            # Unexplored candidate: use optimistic prior
            # Bias toward exploration of potentially good candidates (hits)
            # Use alpha > beta to favor success (finding hits)
            alpha = 4  # Slightly higher than before for more optimism
            beta = 1
        
        # Sample from Beta distribution
        sample = np.random.beta(alpha, beta)
        thompson_samples.append((sample, idx))
    
    # Sort by Thompson sample (descending) and select top batch_size
    thompson_samples.sort(reverse=True)
    selected = [idx for _, idx in thompson_samples[:batch_size]]
    
    return selected