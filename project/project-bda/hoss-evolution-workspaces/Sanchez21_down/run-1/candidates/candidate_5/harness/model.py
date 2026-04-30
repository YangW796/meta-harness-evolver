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
    
    Strategy: Bayesian Sparse Hit Detection with Laplace Priors
    - Uses Bayesian Lasso (Laplace prior) to model sparse hit structure
    - Assumes only a small fraction of genes are true hits (sparsity assumption)
    - Uses two-component mixture: (1) Laplace prior for hit genes, (2) Gaussian for background
    - Adaptively estimates sparsity level from observed hit rate
    - Uses Upper Confidence Bound (UCB) for selection with sparsity-aware uncertainty
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
    
    # Bayesian Sparse Hit Detection with Laplace Priors
    # Uses two-component mixture: Laplace for hits (sparse), Gaussian for background
    
    # Estimate sparsity level from observed hit rate
    total_observed = len(history)
    hit_count = sum(1 for h in history if h.get('hit') == 1)
    empirical_hit_rate = hit_count / max(total_observed, 1)
    
    # Sparsity parameter: assume at least 1% hit rate, cap at 20%
    sparsity_prior = max(0.01, min(empirical_hit_rate, 0.20)) if total_observed > 0 else 0.05
    
    # Compute global statistics for background distribution
    all_scores = [h['score'] for h in history]
    background_mean = np.mean(all_scores) if all_scores else 0.0
    background_var = np.var(all_scores) if len(all_scores) > 1 else 1.0
    
    # For hit distribution: use Laplace prior (double exponential)
    # Laplace is centered at extreme negative values for this task
    hit_scores = [h['score'] for h in history if h.get('hit') == 1]
    if len(hit_scores) > 0:
        hit_mean = np.mean(hit_scores)
        hit_scale = np.mean(np.abs(np.array(hit_scores) - hit_mean)) if len(hit_scores) > 1 else 1.0
    else:
        # Prior for hits: assume they are at least 2 std devs below background
        hit_mean = background_mean - 2 * np.sqrt(background_var)
        hit_scale = np.sqrt(background_var)
    
    # Build candidate models with empirical Bayes
    candidate_stats = {}
    
    for h in history:
        idx = h['candidate_index']
        score = h['score']
        is_hit = h.get('hit') == 1
        
        # Two-component mixture posterior weights
        # P(hit|score) \propto P(score|hit) * P(hit)
        # P(background|score) \propto P(score|background) * (1-P(hit))
        
        # Likelihood under hit model (Laplace)
        hit_likelihood = np.exp(-np.abs(score - hit_mean) / hit_scale) / (2 * hit_scale)
        
        # Likelihood under background model (Gaussian)
        bg_likelihood = np.exp(-0.5 * (score - background_mean) ** 2 / background_var) / np.sqrt(2 * np.pi * background_var)
        
        # Posterior probability this candidate is a hit
        numerator = hit_likelihood * sparsity_prior
        denominator = numerator + bg_likelihood * (1 - sparsity_prior)
        hit_posterior = numerator / denominator if denominator > 0 else sparsity_prior
        
        # Update hit mean and scale with this observation (if hit)
        effective_weight = hit_posterior
        updated_hit_mean = (hit_mean + effective_weight * score) / (1 + effective_weight)
        updated_hit_scale = hit_scale + effective_weight * np.abs(score - hit_mean)
        
        candidate_stats[idx] = {
            'hit_posterior': hit_posterior,
            'score': score,
            'is_hit': is_hit,
            'local_hit_mean': updated_hit_mean,
            'local_hit_scale': updated_hit_scale,
            'observations': 1
        }
    
    # Compute UCB scores for available candidates
    observed_rounds = len(set(h.get('round', 0) for h in history))
    exploration_param = 2.0 * np.sqrt(np.log(observed_rounds + 1)) if observed_rounds > 0 else 2.0
    
    ucb_scores = {}
    
    for idx in available:
        if idx in candidate_stats:
            # Candidate has been observed
            stats = candidate_stats[idx]
            hit_prob = stats['hit_posterior']
            score = stats['score']
            
            # Uncertainty decreases with more observations
            uncertainty = 1.0 / np.sqrt(stats['observations'] + 1)
            
            # UCB: combine expected value (hit probability) with exploration bonus
            # For this task, we want hits (high hit_prob) and extreme negative scores
            expected_value = hit_prob - (1 - hit_prob) * np.abs(score)
            ucb = expected_value - exploration_param * uncertainty
            
        else:
            # Candidate not observed: use prior
            # Prior hit probability = sparsity_prior
            # Prior score = background_mean
            
            # Higher uncertainty for unobserved candidates
            uncertainty = 1.0
            
            # Prior expected value
            prior_hit_prob = sparsity_prior
            expected_value = prior_hit_prob - (1 - prior_hit_prob) * np.abs(background_mean)
            ucb = expected_value - exploration_param * uncertainty
        
        ucb_scores[idx] = ucb
    
    # Select candidates with highest UCB scores (most negative for this task)
    sorted_by_ucb = sorted(available, key=lambda x: ucb_scores[x])
    selected_indices = sorted_by_ucb[:batch_size]
    
    return selected_indices