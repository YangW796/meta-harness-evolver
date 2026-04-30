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
    - If no history (round 1): random exploration
    - If history exists: 70% exploitation (top scorers + similar genes), 30% exploration
    - Uses gene search if available to find similar genes to high performers
    """
    rng = random.Random(seed)
    
    # Get already selected indices
    already_selected = {h['candidate_index'] for h in history}
    
    # Get all available candidate indices
    all_indices = list(range(len(candidates)))
    available_indices = [idx for idx in all_indices if idx not in already_selected]
    
    # If no history or not enough candidates, return random selection
    if not history or len(available_indices) <= batch_size:
        selected = rng.sample(available_indices, min(batch_size, len(available_indices)))
        return selected
    
    # Calculate scores for each candidate in history
    candidate_scores = {}
    for h in history:
        idx = h['candidate_index']
        score = h.get('score', 0.0)
        hit = h.get('hit', 0)
        # Heavily prioritize hits - they are the target metric
        # Use a large weight for hits (10x max expected score) plus the actual score
        candidate_scores[idx] = score + (hit * 10.0)
    
    # Sort candidates by score
    sorted_history = sorted(history, key=lambda h: candidate_scores.get(h['candidate_index'], 0), reverse=True)
    
    # Strategy: 70% exploitation, 30% exploration
    num_exploit = int(batch_size * 0.7)
    num_explore = batch_size - num_exploit
    
    selected = []
    
    # Exploitation: select top performers and their similar genes
    exploit_pool = []
    
    # Add top 20% of historical candidates to exploitation pool
    top_performers = [h['candidate_index'] for h in sorted_history[:max(1, len(sorted_history) // 5)]]
    exploit_pool.extend(top_performers)
    
    # Try to use gene search to find similar genes
    try:
        import bda_tools
        gene_search_available = True
    except ImportError:
        gene_search_available = False
    
    if gene_search_available:
        # Prioritize finding similar genes to HIT genes first
        hit_genes = [h for h in sorted_history if h.get('hit', 0) == 1]
        genes_to_search = hit_genes + sorted_history[:max(1, len(sorted_history) // 10)]
        genes_seen = set()
        
        for h in genes_to_search:
            idx = h['candidate_index']
            candidate = candidates[idx]
            
            # Get gene name
            if 'gene' in candidate:
                gene = candidate['gene']
            elif 'gene_a' in candidate:
                gene = candidate['gene_a']
            else:
                continue
            
            # Avoid searching for the same gene multiple times
            if gene in genes_seen:
                continue
            genes_seen.add(gene)
            
            # Search for similar genes
            try:
                similar_indices = bda_tools.gene_search(gene, k=10, diverse=False)
                # Filter to available indices only (not yet selected)
                similar_available = [i for i in similar_indices if i in available_indices and i not in exploit_pool and i not in selected]
                # Only keep top 50% of similar genes to maintain quality
                # Use the first half (higher-ranked by gene search)
                keep_count = max(1, len(similar_available) // 2)
                exploit_pool.extend(similar_available[:keep_count])
            except:
                pass
    
    # Remove duplicates and already selected
    exploit_pool = [idx for idx in exploit_pool if idx in available_indices and idx not in selected]
    
    # Sample from exploitation pool
    if exploit_pool:
        num_to_sample = min(num_exploit, len(exploit_pool))
        selected.extend(rng.sample(exploit_pool, num_to_sample))
    
    # If we need more exploitation candidates, add more top performers
    if len(selected) < num_exploit:
        remaining_needed = num_exploit - len(selected)
        top_available = [h['candidate_index'] for h in sorted_history 
                        if h['candidate_index'] in available_indices and h['candidate_index'] not in selected]
        if top_available:
            num_to_add = min(remaining_needed, len(top_available))
            selected.extend(rng.sample(top_available, num_to_add))
    
    # Exploration: random sampling from remaining available indices
    remaining_available = [idx for idx in available_indices if idx not in selected]
    if remaining_available and num_explore > 0:
        num_to_explore = min(num_explore, len(remaining_available))
        selected.extend(rng.sample(remaining_available, num_to_explore))
    
    # If we still don't have enough, fill with any available
    if len(selected) < batch_size:
        still_available = [idx for idx in available_indices if idx not in selected]
        if still_available:
            num_needed = batch_size - len(selected)
            selected.extend(rng.sample(still_available, min(num_needed, len(still_available))))
    
    return selected[:batch_size]