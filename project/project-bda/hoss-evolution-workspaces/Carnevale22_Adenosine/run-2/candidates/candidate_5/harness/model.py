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
    
    # If no history (first round), use random selection
    if not history:
        selected = rng.choice(available_indices, size=min(batch_size, len(available_indices)), replace=False)
        return selected.tolist()
    
    # Thompson Sampling with Beta-Bernoulli model
    # Model hit (extreme outcome) as Bernoulli event with Beta prior
    # Beta(alpha, beta) where:
    # - alpha = 1 + number_of_hits (Jeffreys prior + successes)
    # - beta = 1 + number_of_trials - number_of_hits (Jeffreys prior + failures)
    
    # Track hits and trials for each candidate
    hits = {}
    trials = {}
    
    for h in history:
        idx = h['candidate_index']
        is_hit = h.get('hit', 0)
        
        if idx not in hits:
            hits[idx] = 0
            trials[idx] = 0
        
        hits[idx] += is_hit
        trials[idx] += 1
    
    # Calculate gene family hit rates for prior strengthening
    # Genes from families with high hit rates get boosted priors
    family_hits = {}
    family_trials = {}
    
    for idx in hits:
        gene_name = candidates[idx].get('gene', '')
        family = gene_name.split('_')[0].split('-')[0]
        
        if family not in family_hits:
            family_hits[family] = 0
            family_trials[family] = 0
        
        family_hits[family] += hits[idx]
        family_trials[family] += trials[idx]
    
    # Sample from posterior for each available candidate
    sampled_probs = []
    
    for idx in available_indices:
        gene_name = candidates[idx].get('gene', '')
        family = gene_name.split('_')[0].split('-')[0]
        
        if idx in hits:
            # Candidate has been tried before
            # Use Beta posterior: Beta(1 + hits, 1 + trials - hits)
            alpha = 1 + hits[idx]
            beta = 1 + trials[idx] - hits[idx]
        else:
            # Never-seen candidate - use informed prior based on family
            if family in family_hits and family_trials[family] > 0:
                # Use family statistics to create informed prior
                # More conservative: weight family evidence less for never-seen
                family_hit_rate = family_hits[family] / family_trials[family]
                # Scale down family influence for never-seen (pseudo-counts approach)
                alpha = 1 + 0.5 * family_hits[family]
                beta = 1 + 0.5 * (family_trials[family] - family_hits[family])
            else:
                # No family info - use uniform Jeffreys prior
                alpha = 1
                beta = 1
        
        # Sample from Beta posterior
        sampled_prob = rng.beta(alpha, beta)
        sampled_probs.append((sampled_prob, idx))
    
    # Sort by sampled probability (descending) and select top candidates
    sampled_probs.sort(reverse=True)
    selected = [idx for _, idx in sampled_probs[:batch_size]]
    
    # If we don't have enough candidates, fill with random unexplored ones
    if len(selected) < batch_size:
        remaining = [idx for idx in available_indices if idx not in selected]
        needed = batch_size - len(selected)
        if remaining:
            additional = rng.choice(remaining, size=min(needed, len(remaining)), replace=False)
            selected.extend(additional.tolist())
    
    return selected
