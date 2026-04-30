from __future__ import annotations
import random
import numpy as np
from collections import defaultdict

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
    
    Strategy: Thompson Sampling with Gene Cluster Priors
    - Uses Thompson Sampling (Bayesian bandit algorithm) for adaptive exploration-exploitation
    - Models each candidate with Beta distribution based on hit observations
    - Uses gene search to create clusters and share information via Bayesian priors
    - Enhanced fallback: Uses gene name prefix clustering when gene search unavailable
    - Naturally balances exploration vs exploitation based on uncertainty
    """
    rng = random.Random(seed)
    np.random.seed(seed)
    
    # Get already selected indices
    selected = set(h['candidate_index'] for h in history)
    
    # Get all available candidate indices
    all_indices = list(range(len(candidates)))
    available = [i for i in all_indices if i not in selected]
    
    if len(available) <= batch_size:
        return available
    
    # If no history, use pure exploration
    if len(history) == 0:
        return rng.sample(available, batch_size)
    
    # Check if hit information is available
    has_hits = any('hit' in h for h in history)
    
    if not has_hits:
        # Fall back to score-based selection using absolute scores
        sorted_history = sorted(history, key=lambda x: abs(x['score']), reverse=True)
        top_k = max(10, len(sorted_history) // 5)
        top_performers = [h['candidate_index'] for h in sorted_history[:top_k]]
        
        # Sample from top performers
        selected_indices = []
        remaining = available.copy()
        
        # Take some top performers if available
        top_available = [idx for idx in top_performers if idx in remaining]
        if top_available:
            n_top = min(len(top_available), batch_size // 2)
            selected_indices.extend(rng.sample(top_available, n_top))
            remaining = [i for i in remaining if i not in selected_indices]
        
        # Fill rest with random exploration
        if len(selected_indices) < batch_size:
            needed = batch_size - len(selected_indices)
            selected_indices.extend(rng.sample(remaining, min(needed, len(remaining))))
        
        return selected_indices[:batch_size]
    
    # Thompson Sampling with Gene Cluster Priors
    # Group candidates into clusters based on gene similarity
    clusters = defaultdict(list)
    candidate_to_cluster = {}
    
    # Try to use gene search to create clusters
    try:
        import bda_tools
        
        # Create clusters for all candidates we have history for
        for h in history:
            idx = h['candidate_index']
            candidate = candidates[idx]
            gene = candidate.get('gene') or candidate.get('gene_a')
            
            if gene and idx not in candidate_to_cluster:
                # Find similar genes
                try:
                    similar = bda_tools.gene_search(gene, k=20, diverse=False)
                    cluster_id = f"cluster_{gene}"
                    
                    for sim_idx in similar:
                        if sim_idx not in candidate_to_cluster:
                            candidate_to_cluster[sim_idx] = cluster_id
                            clusters[cluster_id].append(sim_idx)
                except:
                    # If gene search fails, put in singleton cluster
                    cluster_id = f"singleton_{idx}"
                    candidate_to_cluster[idx] = cluster_id
                    clusters[cluster_id] = [idx]
        
        # Assign unassigned candidates to singleton clusters
        for idx in all_indices:
            if idx not in candidate_to_cluster:
                cluster_id = f"singleton_{idx}"
                candidate_to_cluster[idx] = cluster_id
                clusters[cluster_id] = [idx]
                
    except ImportError:
        # No gene search available - use enhanced fallback: gene family prefix clustering
        # Group genes by name prefix to capture gene families (e.g., ZNF, ZSCAN, TNF, etc.)
        gene_to_prefix = {}
        
        for idx in all_indices:
            candidate = candidates[idx]
            gene = candidate.get('gene') or candidate.get('gene_a')
            if gene:
                # Extract prefix: typically first 3-4 letters before numbers
                # This captures gene families like ZNF, ZSCAN, TNF, IL, etc.
                prefix = ''.join([c for c in gene if not c.isdigit()])[:4]
                if len(prefix) >= 2:
                    gene_to_prefix[idx] = f"family_{prefix}"
                else:
                    gene_to_prefix[idx] = f"singleton_{idx}"
            else:
                gene_to_prefix[idx] = f"singleton_{idx}"
        
        # Create clusters based on prefix
        for idx, prefix in gene_to_prefix.items():
            candidate_to_cluster[idx] = prefix
            clusters[prefix].append(idx)
    
    # Compute cluster statistics (empirical Bayes priors)
    cluster_successes = defaultdict(int)
    cluster_trials = defaultdict(int)
    
    for h in history:
        idx = h['candidate_index']
        cluster_id = candidate_to_cluster[idx]
        cluster_trials[cluster_id] += 1
        if h.get('hit') == 1:
            cluster_successes[cluster_id] += 1
    
    # Compute global prior from all history
    total_hits = sum(1 for h in history if h.get('hit') == 1)
    global_alpha = total_hits + 1
    global_beta = len(history) - total_hits + 1
    
    # For each cluster, compute posterior parameters
    cluster_alpha = {}
    cluster_beta = {}
    
    for cluster_id in clusters:
        successes = cluster_successes.get(cluster_id, 0)
        trials = cluster_trials.get(cluster_id, 0)
        
        # Use global prior with cluster observations
        # This is empirical Bayes: use global distribution as prior
        cluster_alpha[cluster_id] = successes + global_alpha
        cluster_beta[cluster_id] = (trials - successes) + global_beta
    
    # For candidates with direct observations, compute posterior
    candidate_alpha = {}
    candidate_beta = {}
    
    for h in history:
        idx = h['candidate_index']
        hit = h.get('hit', 0)
        cluster_id = candidate_to_cluster[idx]
        
        # Start with cluster prior, update with direct observation
        candidate_alpha[idx] = hit + cluster_alpha[cluster_id]
        candidate_beta[idx] = (1 - hit) + cluster_beta[cluster_id]
    
    # Thompson Sampling: sample theta for each candidate and select top ones
    sampled_probs = {}
    
    for idx in available:
        cluster_id = candidate_to_cluster[idx]
        
        if idx in candidate_alpha:
            # Candidate has been observed, use its posterior
            alpha = candidate_alpha[idx]
            beta = candidate_beta[idx]
        else:
            # Candidate not observed, use cluster posterior
            alpha = cluster_alpha[cluster_id]
            beta = cluster_beta[cluster_id]
        
        # Sample from Beta distribution
        sampled_probs[idx] = np.random.beta(alpha, beta)
    
    # Select top candidates by sampled probability
    sorted_by_sample = sorted(available, key=lambda x: sampled_probs[x], reverse=True)
    selected_indices = sorted_by_sample[:batch_size]
    
    return selected_indices