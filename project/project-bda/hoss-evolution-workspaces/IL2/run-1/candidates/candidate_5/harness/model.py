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

    Strategy:
    - Thompson Sampling with Beta-Bernoulli model for hit probability
    - Uses gene search to expand candidate pool for similar genes
    - Naturally balances exploration vs exploitation through posterior sampling
    """
    rng = random.Random(seed)
    np.random.seed(seed)
    
    # Get already selected indices
    already_selected = {h['candidate_index'] for h in history}
    
    # Get all available candidate indices
    all_indices = list(range(len(candidates)))
    available_indices = [idx for idx in all_indices if idx not in already_selected]
    
    # If no history or not enough candidates, return random selection
    if not history or len(available_indices) <= batch_size:
        selected = rng.sample(available_indices, min(batch_size, len(available_indices)))
        return selected
    
    # Build gene performance statistics
    # Track hits and trials per gene
    gene_stats = {}  # gene_name -> {'hits': int, 'trials': int}
    
    for h in history:
        idx = h['candidate_index']
        candidate = candidates[idx]
        
        # Get gene name
        if 'gene' in candidate:
            gene = candidate['gene']
        elif 'gene_a' in candidate:
            gene = candidate['gene_a']
        else:
            continue
        
        if gene not in gene_stats:
            gene_stats[gene] = {'hits': 0, 'trials': 0}
        
        gene_stats[gene]['trials'] += 1
        if h.get('hit', 0) == 1:
            gene_stats[gene]['hits'] += 1
    
    # Thompson Sampling: Sample hit probabilities from Beta posterior
    # Prior: Beta(1, 1) which is uniform [0, 1]
    # Posterior: Beta(1 + hits, 1 + trials - hits)
    gene_sampled_probs = {}
    
    for gene, stats in gene_stats.items():
        hits = stats['hits']
        trials = stats['trials']
        # Sample from Beta posterior
        sampled_prob = np.random.beta(1 + hits, 1 + trials - hits)
        gene_sampled_probs[gene] = sampled_prob
    
    # Create candidate pool with Thompson Sampling scores
    candidate_pool = []
    
    # Add candidates corresponding to tested genes with sampled probabilities
    for h in history:
        idx = h['candidate_index']
        if idx not in available_indices:
            continue
        
        candidate = candidates[idx]
        if 'gene' in candidate:
            gene = candidate['gene']
        elif 'gene_a' in candidate:
            gene = candidate['gene_a']
        else:
            continue
        
        if gene in gene_sampled_probs:
            candidate_pool.append((idx, gene_sampled_probs[gene]))
    
    # Try to use gene search to expand pool with similar genes
    try:
        import bda_tools
        
        # Sort genes by sampled probability (descending)
        sorted_genes = sorted(gene_sampled_probs.items(), key=lambda x: x[1], reverse=True)
        
        # Search similar genes for top performers
        genes_seen = set()
        for gene, prob in sorted_genes[:max(10, len(sorted_genes) // 5)]:
            if gene in genes_seen:
                continue
            genes_seen.add(gene)
            
            try:
                # Search for similar genes
                similar_indices = bda_tools.gene_search(gene, k=10, diverse=False)
                
                # Assign Thompson Sampling score to similar genes
                # Use the sampled probability of the query gene
                for sim_idx in similar_indices:
                    if sim_idx in available_indices and sim_idx not in [c[0] for c in candidate_pool]:
                        candidate_pool.append((sim_idx, prob))
            except:
                pass
    except ImportError:
        pass
    
    # Sort candidate pool by Thompson Sampling score
    candidate_pool.sort(key=lambda x: x[1], reverse=True)
    
    # Select top candidates from pool
    selected = []
    if candidate_pool:
        # Take top candidates based on Thompson Sampling scores
        num_from_pool = min(batch_size, len(candidate_pool))
        selected = [idx for idx, _ in candidate_pool[:num_from_pool]]
    
    # If we need more candidates, add random exploration
    if len(selected) < batch_size:
        remaining_available = [idx for idx in available_indices if idx not in selected]
        if remaining_available:
            num_needed = batch_size - len(selected)
            num_to_add = min(num_needed, len(remaining_available))
            selected.extend(rng.sample(remaining_available, num_to_add))
    
    return selected[:batch_size]