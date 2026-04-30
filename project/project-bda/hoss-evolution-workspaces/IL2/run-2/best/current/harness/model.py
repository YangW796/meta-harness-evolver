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
    - Evolutionary Strategy (ES) approach for gene selection
    - Maintains a population of promising genes based on fitness (score magnitude)
    - Uses mutation (gene search for similar genes) to explore neighborhood
    - Uses selection pressure to focus on high-fitness regions
    - Balances exploration (new genes) vs exploitation (known good gene families)
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
    
    # Build gene fitness scores based on extreme values (both positive and negative)
    # Fitness = absolute score magnitude (we care about extreme effects in either direction)
    gene_fitness = {}  # gene_name -> {'fitness': float, 'count': int, 'indices': list[int]}
    
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
        
        score = h.get('score', 0.0)
        # Use absolute score as fitness (extreme values in either direction are interesting)
        fitness = abs(score)
        
        if gene not in gene_fitness:
            gene_fitness[gene] = {'fitness': 0.0, 'count': 0, 'indices': []}
        
        # Accumulate fitness (could use max, sum, or weighted average)
        # Using max to prioritize genes that have shown extreme behavior
        gene_fitness[gene]['fitness'] = max(gene_fitness[gene]['fitness'], fitness)
        gene_fitness[gene]['count'] += 1
        gene_fitness[gene]['indices'].append(idx)
    
    # Sort genes by fitness (descending)
    sorted_genes = sorted(gene_fitness.items(), key=lambda x: x[1]['fitness'], reverse=True)
    
    # Evolutionary Strategy: Select parents and generate offspring
    selected = []
    
    # Phase 1: Exploitation - Select top-performing genes (elite selection)
    # Take top 20% of genes as "parents"
    num_parents = max(5, len(sorted_genes) // 5)
    parents = sorted_genes[:num_parents]
    
    for gene, data in parents:
        # Add the actual tested indices that are still available
        for idx in data['indices']:
            if idx in available_indices and idx not in selected:
                selected.append(idx)
                if len(selected) >= batch_size // 2:  # Reserve half for exploration
                    break
        if len(selected) >= batch_size // 2:
            break
    
    # Phase 2: Mutation - Use gene search to find similar genes to top performers
    try:
        import bda_tools
        
        genes_seen = set()
        for gene, data in parents[:max(3, len(parents) // 2)]:  # Top 50% of parents
            if gene in genes_seen:
                continue
            genes_seen.add(gene)
            
            try:
                # Search for similar genes (mutation with small perturbation)
                similar_indices = bda_tools.gene_search(gene, k=15, diverse=False)
                
                # Add similar genes that haven't been selected
                for sim_idx in similar_indices:
                    if sim_idx in available_indices and sim_idx not in selected:
                        selected.append(sim_idx)
                        if len(selected) >= batch_size * 3 // 4:  # Reserve 75% total
                            break
                    if len(selected) >= batch_size * 3 // 4:
                        break
            except:
                pass
            
            if len(selected) >= batch_size * 3 // 4:
                break
    except ImportError:
        pass
    
    # Phase 3: Exploration - Add diverse genes to maintain population diversity
    try:
        import bda_tools
        
        # For top 2-3 parents, also search for DIVERSE genes (exploration)
        genes_seen_diverse = set()
        for gene, data in parents[:min(3, len(parents))]:
            if gene in genes_seen_diverse:
                continue
            genes_seen_diverse.add(gene)
            
            try:
                # Search for diverse genes (explore different regions)
                diverse_indices = bda_tools.gene_search(gene, k=10, diverse=True)
                
                for div_idx in diverse_indices:
                    if div_idx in available_indices and div_idx not in selected:
                        selected.append(div_idx)
                        if len(selected) >= batch_size - 10:  # Leave room for random
                            break
                    if len(selected) >= batch_size - 10:
                        break
            except:
                pass
            
            if len(selected) >= batch_size - 10:
                break
    except ImportError:
        pass
    
    # Phase 4: Fill remaining slots with random genes from high-fitness families
    if len(selected) < batch_size:
        # Create a probability distribution based on gene fitness
        remaining_available = [idx for idx in available_indices if idx not in selected]
        
        if remaining_available:
            # Score remaining candidates by their gene family fitness
            candidate_scores = []
            for idx in remaining_available:
                candidate = candidates[idx]
                if 'gene' in candidate:
                    gene = candidate['gene']
                elif 'gene_a' in candidate:
                    gene = candidate['gene_a']
                else:
                    gene = None
                
                if gene and gene in gene_fitness:
                    score = gene_fitness[gene]['fitness']
                else:
                    # Give unknown genes a small chance
                    score = 0.01
                
                candidate_scores.append((idx, score))
            
            # Sample with probability proportional to fitness
            num_needed = batch_size - len(selected)
            if candidate_scores:
                indices, scores = zip(*candidate_scores)
                scores = np.array(scores)
                # Add small epsilon to avoid division by zero
                scores = scores + 0.01
                probs = scores / scores.sum()
                
                # Sample without replacement
                sampled_indices = np.random.choice(
                    list(indices), 
                    size=min(num_needed, len(indices)), 
                    replace=False, 
                    p=probs
                )
                selected.extend(sampled_indices.tolist())
    
    # Final fallback: if we still need more, add pure random
    if len(selected) < batch_size:
        remaining_available = [idx for idx in available_indices if idx not in selected]
        if remaining_available:
            num_needed = batch_size - len(selected)
            num_to_add = min(num_needed, len(remaining_available))
            selected.extend(rng.sample(remaining_available, num_to_add))
    
    return selected[:batch_size]
