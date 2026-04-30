# Evolution Proposal - Candidate 5

## What Changed

Replaced the heuristic exploration-exploitation strategy with **Thompson Sampling**, a Bayesian multi-armed bandit algorithm.

**Key changes:**
1. **Thompson Sampling Core**: Instead of using a fixed exploration ratio (90% → 20%), the algorithm now samples from Beta distributions to naturally balance exploration and exploitation based on uncertainty.
2. **Bayesian Hierarchical Model**: Uses a two-level hierarchy:
   - **Cluster level**: Groups genes by similarity (using gene search when available)
   - **Candidate level**: Individual gene observations
3. **Empirical Bayes Priors**: Uses global hit statistics to inform cluster priors, which then inform individual candidate beliefs.
4. **Adaptive Uncertainty**: Candidates/clusters with fewer observations have higher uncertainty and get explored more naturally.

**Technical implementation:**
- For each candidate, maintains Beta(α, β) posterior distribution
- α = successes + prior_α (hit count plus prior)
- β = failures + prior_β (miss count plus prior)
- At selection time, samples a probability from each candidate's Beta distribution
- Selects candidates with highest sampled probabilities
- Unobserved candidates inherit their cluster's distribution

## Why This Is Better

**Problem with current approach:**
The current best model uses a fixed exploration schedule that:
- Decreases linearly regardless of actual performance
- Doesn't adapt to uncertainty in different gene families
- Uses heuristics for exploration/exploitation balance

**Advantages of Thompson Sampling:**
1. **Optimal Exploration**: Thompson Sampling is proven to be asymptotically optimal for bandit problems
2. **Uncertainty-Aware**: Automatically explores candidates with high uncertainty (few observations)
3. **Adaptive**: No fixed exploration schedule - adjusts based on actual observations
4. **Information Sharing**: Genes in the same cluster share statistical strength through Bayesian priors
5. **Hit-Focused**: When hit information is available, directly optimizes for hits rather than scores

## Expected Impact

**What I expect to improve:**
- Better hit rate in later rounds as the algorithm focuses on promising gene families
- More intelligent exploration that targets uncertain regions rather than random sampling
- Better utilization of gene similarity information through cluster priors
- Higher cumulative hits over the budget as exploitation becomes more targeted

**Potential risks:**
- If hit information is noisy or sparse, the Beta distributions may not converge well
- Gene search dependency - falls back to simpler strategy if unavailable
- First round performance may be similar (pure exploration)

## Novelty

**Chosen strategy tags:** ['thompson_sampling', 'bayesian', 'bandit']

**Most similar to:** Candidate 1 (both use hybrid exploration-exploitation)

**How this differs:**
- Candidate 1-4 all use heuristic exploration ratios and score-based sorting
- This candidate uses a principled Bayesian approach that automatically balances exploration/exploitation
- Instead of fixed schedules, uses uncertainty quantification to guide exploration
- Introduces hierarchical Bayesian modeling to share information across similar genes
- Fundamentally different algorithmic paradigm (bandit algorithm vs. heuristic search)

This is a meaningfully different approach as required for the exploration round, switching from heuristic search to a theoretically-grounded Bayesian bandit algorithm.