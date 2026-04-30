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
    - Early rounds: More random exploration to discover promising regions
    - Later rounds: More exploitation of high-scoring candidates
    - Always maintain diversity to avoid getting stuck in local optima
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
    exploration_ratio = max(0.2, 0.9 - 0.15 * num_rounds)  # Starts at 90%, decreases to 20%
    
    # Separate exploration and exploitation
    num_explore = int(batch_size * exploration_ratio)
    num_exploit = batch_size - num_explore
    
    # Exploration: random sampling from available candidates
    explore_indices = rng.sample(available, min(num_explore, len(available)))
    
    # Exploitation: select based on historical scores
    if len(history) > 0 and num_exploit > 0:
        # Sort by absolute score to prioritize both negative and positive extremes
        sorted_history = sorted(history, key=lambda x: abs(x['score']), reverse=True)
        
        # Get top performers (highest absolute scores, 20% or at least 10)
        top_k = max(10, len(sorted_history) // 5)
        top_performers = [h['candidate_index'] for h in sorted_history[:top_k]]
        
        # Find candidates similar to top performers if gene search is available
        exploit_candidates = set()
        remaining_avail = [i for i in available if i not in explore_indices]
        
        if len(remaining_avail) > 0:
            # Try to use gene search if available
            try:
                import bda_tools
                
                # If hit information is available, prioritize actual hits over just high absolute scores
                if any('hit' in h for h in history):
                    hit_indices = [h['candidate_index'] for h in history if h.get('hit') == 1]
                    if hit_indices:
                        # Prioritize genes that are actual hits
                        top_performers = hit_indices[:min(len(hit_indices), top_k)]
                
                # Sample more aggressively from top performers
                num_to_sample = min(10, len(top_performers))
                sampled_top = rng.sample(top_performers, num_to_sample)
                
                for top_idx in sampled_top:
                    if len(exploit_candidates) >= num_exploit:
                        break
                    # Get gene name from candidate
                    candidate = candidates[top_idx]
                    gene = candidate.get('gene') or candidate.get('gene_a')
                    if gene:
                        try:
                            # Search for similar genes with higher k
                            similar = bda_tools.gene_search(gene, k=min(30, num_exploit * 2), diverse=False)
                            for idx in similar:
                                if idx in remaining_avail and idx not in exploit_candidates:
                                    exploit_candidates.add(idx)
                                    if len(exploit_candidates) >= num_exploit:
                                        break
                        except:
                            pass
                
                # If we still need candidates, also try diverse search around top performers
                if len(exploit_candidates) < num_exploit:
                    for top_idx in sampled_top:
                        if len(exploit_candidates) >= num_exploit:
                            break
                        candidate = candidates[top_idx]
                        gene = candidate.get('gene') or candidate.get('gene_a')
                        if gene:
                            try:
                                # Try diverse search for broader coverage
                                diverse_similar = bda_tools.gene_search(gene, k=min(20, num_exploit - len(exploit_candidates)), diverse=True)
                                for idx in diverse_similar:
                                    if idx in remaining_avail and idx not in exploit_candidates:
                                        exploit_candidates.add(idx)
                                        if len(exploit_candidates) >= num_exploit:
                                            break
                            except:
                                pass
            except ImportError:
                # bda_tools not available, fall back to other strategies
                pass
            
            # If we still need more candidates, use weighted sampling based on score patterns
            if len(exploit_candidates) < num_exploit:
                needed = num_exploit - len(exploit_candidates)
                
                # Analyze score distribution to target both extremes
                scores = [h['score'] for h in history]
                if scores:
                    # Target both very negative and near-zero regions
                    extreme_negative = [h['candidate_index'] for h in history if h['score'] < -2.0]
                    near_zero = [h['candidate_index'] for h in history if abs(h['score']) < 0.1]
                    
                    # Sample from both regions if available
                    if extreme_negative and needed > 1:
                        idx = rng.choice(extreme_negative)
                        if idx in remaining_avail and idx not in exploit_candidates:
                            exploit_candidates.add(idx)
                            needed -= 1
                    
                    if near_zero and needed > 0:
                        idx = rng.choice(near_zero)
                        if idx in remaining_avail and idx not in exploit_candidates:
                            exploit_candidates.add(idx)
                            needed -= 1
                
                # Use stratified sampling for remaining diversity
                if needed > 0:
                    num_buckets = min(10, len(remaining_avail))
                    bucket_size = len(remaining_avail) // num_buckets
                    
                    sampled = set()
                    for bucket in range(num_buckets):
                        if len(sampled) >= needed:
                            break
                        start = bucket * bucket_size
                        end = start + bucket_size if bucket < num_buckets - 1 else len(remaining_avail)
                        bucket_items = remaining_avail[start:end]
                        if bucket_items:
                            sampled.add(rng.choice(bucket_items))
                    
                    exploit_candidates.update(sampled)
        
        selected_indices = list(explore_indices) + list(exploit_candidates)[:num_exploit]
    else:
        # Pure exploration if no history or no exploitation needed
        selected_indices = explore_indices
    
    # Ensure we have exactly batch_size indices
    if len(selected_indices) < batch_size:
        remaining = [i for i in available if i not in selected_indices]
        needed = batch_size - len(selected_indices)
        if remaining:
            selected_indices.extend(rng.sample(remaining, min(needed, len(remaining))))
    
    return selected_indices[:batch_size]
