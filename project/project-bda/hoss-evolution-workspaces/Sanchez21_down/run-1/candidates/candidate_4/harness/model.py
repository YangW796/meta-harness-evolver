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
    
    # Enhanced Thompson Sampling with Continuous Score Modeling
    # Use Gaussian-Gamma model for continuous scores instead of Beta for binary hits
    
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
    
    # Compute cluster statistics using continuous scores
    cluster_sums = defaultdict(float)
    cluster_sums_sq = defaultdict(float)
    cluster_counts = defaultdict(int)
    
    for h in history:
        idx = h['candidate_index']
        cluster_id = candidate_to_cluster[idx]
        score = h['score']
        
        cluster_sums[cluster_id] += score
        cluster_sums_sq[cluster_id] += score * score
        cluster_counts[cluster_id] += 1
    
    # Compute global statistics for empirical Bayes prior
    all_scores = [h['score'] for h in history]
    global_mean = np.mean(all_scores) if all_scores else 0.0
    global_var = np.var(all_scores) if len(all_scores) > 1 else 1.0
    
    # Gaussian-Gamma prior parameters (uninformative but centered at global stats)
    mu_0 = global_mean  # Prior mean
    lambda_0 = 1.0      # Prior precision scaling
    alpha_0 = 1.0       # Prior shape for precision
    beta_0 = global_var if global_var > 0 else 1.0  # Prior rate for precision
    
    # For each cluster, compute posterior parameters
    cluster_posterior = {}
    
    for cluster_id in clusters:
        n = cluster_counts.get(cluster_id, 0)
        
        if n == 0:
            # No observations, use prior
            cluster_posterior[cluster_id] = {
                'mu_n': mu_0,
                'lambda_n': lambda_0,
                'alpha_n': alpha_0,
                'beta_n': beta_0
            }
        else:
            # Update posterior with cluster observations
            sum_x = cluster_sums[cluster_id]
            sum_x_sq = cluster_sums_sq[cluster_id]
            mean_x = sum_x / n
            
            # Gaussian-Gamma posterior update
            lambda_n = lambda_0 + n
            mu_n = (lambda_0 * mu_0 + sum_x) / lambda_n
            alpha_n = alpha_0 + n / 2.0
            beta_n = beta_0 + 0.5 * (sum_x_sq - (sum_x * sum_x) / n) + \
                     (lambda_0 * n * (mean_x - mu_0) ** 2) / (2 * lambda_n)
            
            cluster_posterior[cluster_id] = {
                'mu_n': mu_n,
                'lambda_n': lambda_n,
                'alpha_n': alpha_n,
                'beta_n': beta_n
            }
    
    # For candidates with direct observations, compute posterior
    candidate_posterior = {}
    
    for h in history:
        idx = h['candidate_index']
        score = h['score']
        cluster_id = candidate_to_cluster[idx]
        cluster_post = cluster_posterior[cluster_id]
        
        # Conservative update: treat cluster prior as having stronger weight
        # This prevents overfitting to a single observation when cluster has limited data
        effective_prior_weight = max(cluster_post['lambda_n'], 2.0)  # At least 2 pseudo-observations
        lambda_n = effective_prior_weight + 1
        mu_n = (effective_prior_weight * cluster_post['mu_n'] + score) / lambda_n
        alpha_n = cluster_post['alpha_n'] + 0.5
        beta_n = cluster_post['beta_n'] + 0.5 * (score - cluster_post['mu_n']) ** 2 * \
                 effective_prior_weight / lambda_n
        
        candidate_posterior[idx] = {
            'mu_n': mu_n,
            'lambda_n': lambda_n,
            'alpha_n': alpha_n,
            'beta_n': beta_n
        }
    
    # Enhanced Thompson Sampling with explicit exploration bonus
    # Estimate total rounds from history to calibrate exploration
    observed_rounds = len(set(h.get('round', 0) for h in history))
    total_rounds_estimate = max(5, observed_rounds + 1)  # At least 5 rounds expected
    
    # Exploration coefficient: higher early on, decays with rounds
    # Starts at 2.0 for round 1, decays to 0.5 by final round
    exploration_coeff = 2.0 * (1.0 - 0.75 * (observed_rounds / total_rounds_estimate))
    exploration_coeff = max(0.5, exploration_coeff)  # Minimum exploration
    
    sampled_scores = {}
    
    for idx in available:
        cluster_id = candidate_to_cluster[idx]
        
        if idx in candidate_posterior:
            # Candidate has been observed, use its posterior
            post = candidate_posterior[idx]
        else:
            # Candidate not observed, use cluster posterior
            post = cluster_posterior[cluster_id]
        
        # Sample precision from Gamma
        tau = np.random.gamma(post['alpha_n'], 1.0 / post['beta_n'])
        
        # Compute standard deviation (uncertainty)
        std_dev = 1.0 / np.sqrt(post['lambda_n'] * tau)
        
        # Sample mean from Gaussian given precision
        mean_sample = np.random.normal(post['mu_n'], std_dev)
        
        # Add exploration bonus: favor high-uncertainty candidates
        # For this task (more negative = better), subtract exploration term
        exploration_bonus = exploration_coeff * std_dev
        exploration_sample = mean_sample - exploration_bonus
        
        # Store sampled score with exploration bonus
        sampled_scores[idx] = exploration_sample
    
    # Select top candidates by sampled score (prioritize more negative values)
    sorted_by_sample = sorted(available, key=lambda x: sampled_scores[x])
    selected_indices = sorted_by_sample[:batch_size]
    
    return selected_indices