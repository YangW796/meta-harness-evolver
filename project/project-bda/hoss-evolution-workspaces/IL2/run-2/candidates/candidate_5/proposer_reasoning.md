# Evolution Proposal — candidate_5

## What Changed

Switched from **Thompson Sampling with heuristic score boosting** to an **Evolutionary Strategy (ES)** approach for gene selection.

### Key Changes in model.py:

1. **Algorithm Family Change**: Replaced Thompson Sampling (Bayesian bandit) with Evolutionary Strategy (population-based optimization)
2. **Fitness Function**: Uses absolute score magnitude as fitness (prioritizes extreme effects in both positive and negative directions)
3. **Selection Mechanism**: 
   - **Phase 1 (Exploitation)**: Elite selection of top 20% performing genes
   - **Phase 2 (Mutation)**: Gene search for similar genes to top performers (local search)
   - **Phase 3 (Exploration)**: Gene search for diverse genes from top performers (global search)
   - **Phase 4 (Filling)**: Probability-weighted sampling from remaining genes based on gene family fitness

4. **Removed**: Beta-Bernoulli posterior sampling, hand-tuned boosting factors for avg_score and max_score

## Why This Is Better

### Addresses Limitations of Previous Approach:

1. **Thompson Sampling Limitations**: 
   - Required careful tuning of boosting factors (0.1, 0.2, 0.3 thresholds)
   - Assumed stationary hit probability distribution
   - Didn't explicitly model gene family relationships

2. **Evolutionary Strategy Advantages**:
   - **Natural balance**: ES inherently balances exploration (mutation/diverse search) vs exploitation (elite selection)
   - **Population-based**: Maintains diversity by considering multiple promising gene families simultaneously
   - **Adaptive**: Automatically focuses on high-fitness regions without manual threshold tuning
   - **Structured search**: Mutation explores local neighborhoods, diverse search explores globally

3. **Biological Intuition**:
   - Mimics natural evolution: select fit genes, mutate to explore similar genes, maintain population diversity
   - Gene families often share functions; ES explicitly exploits this through mutation operator

## Expected Impact

### Positive:
- **Better hit discovery**: ES should find more hits by systematically exploring neighborhoods of promising genes
- **Improved robustness**: Less sensitive to hyperparameters than hand-tuned boosting factors
- **Better scaling**: ES naturally adapts as more history accumulates

### Potential Risks:
- **Initial exploration**: May be slightly less efficient in very first round (no fitness info), but random fallback handles this
- **Gene search dependency**: Relies on quality of gene_search tool, but has fallbacks

### Target Metric:
- Aiming for **>20 final_score** (current best: 19.44)
- Expect improved cumulative_hits and ncg through better exploration-exploitation balance

## Novelty

### Strategy Tags
- **evolutionary**: Population-based optimization with selection, mutation, and diversity maintenance
- **optimization**: Formulates gene selection as a fitness optimization problem

### Comparison to Recent Candidates

**Most similar to**: Candidate 4 (best current)

**Key differences**:
1. **Algorithm family**: ES vs Thompson Sampling (completely different paradigm)
2. **Selection logic**: 
   - Candidate 4: Sample from Beta posterior, boost by avg_score and max_score with fixed thresholds
   - Candidate 5: Elite selection + mutation (similar genes) + exploration (diverse genes) + fitness-proportional sampling
3. **Hyperparameters**: 
   - Candidate 4: Required tuning 0.1, 0.2, 0.3 thresholds and 0.3 boosting coefficient
   - Candidate 5: Uses adaptive ratios (top 20%, top 50%) and fitness-proportional sampling
4. **Exploration mechanism**:
   - Candidate 4: Random exploration when pool exhausted
   - Candidate 5: Structured exploration via diverse gene search and fitness-weighted sampling

### Novelty Constraint Satisfaction
- **Avoided tags**: ['feature', 'nn', 'uncertainty'] ✓
- **New tags introduced**: ['evolutionary', 'optimization'] ✓
- **Not a minor tweak**: Complete algorithm family change from Bayesian bandits to evolutionary optimization ✓

## Implementation Notes

- Maintains same function signature and IO behavior (drop-in replacement)
- Uses same gene search tool (bda_tools.gene_search) but in a more structured way
- Preserves random fallback for edge cases
- CPU-only implementation (no CUDA/GPU)
