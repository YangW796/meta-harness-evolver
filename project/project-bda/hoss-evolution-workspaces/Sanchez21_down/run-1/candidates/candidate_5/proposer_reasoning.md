# Evolution Proposal: Candidate 5

## What Changed

**Model Family Switch**: Replaced Thompson Sampling with Gaussian-Gamma continuous modeling with a **Bayesian Sparse Hit Detection** approach using **Laplace priors**.

**Key Technical Changes**:
1. **Two-Component Mixture Model**: Explicitly models the data as a mixture of:
   - **Hit component** (sparse): Laplace distribution for extreme-scoring genes
   - **Background component** (dense): Gaussian distribution for normal genes

2. **Sparsity-Inducing Prior**: Uses empirical Bayes to estimate the hit rate from observed data, with a prior that assumes only 1-20% of genes are true hits.

3. **Laplace Prior for Hits**: Instead of Gaussian modeling, uses Laplace (double exponential) distribution which has heavier tails and better captures extreme outliers.

4. **Upper Confidence Bound (UCB) Selection**: Replaces Thompson Sampling with UCB that balances:
   - Expected hit probability (exploitation)
   - Score extremity (more negative = better)
   - Uncertainty reduction (exploration)

5. **Posterior Hit Probability**: For each candidate, computes P(candidate is hit | observed score) using Bayesian inference on the mixture model.

## Why This Is Better

**Biological Plausibility**: 
- The sparsity assumption is biologically realistic: only a small fraction of the ~18,000 genes should significantly affect tau protein levels.
- Laplace distribution better models extreme biological effects (heavy tails).

**Statistical Efficiency**:
- Explicitly models the hit/background distinction rather than treating all scores uniformly.
- Uses all observed data to estimate the global sparsity level, improving inference on individual candidates.

**Adaptive Exploration**:
- UCB naturally balances exploring uncertain candidates vs. exploiting known hits.
- The exploration parameter automatically scales with rounds (√log(t) like in standard bandit algorithms).

## Expected Impact

**Target Improvement**: +1.5 to +3.0 points in final score (based on prior candidate improvements)

**Mechanism**:
- Better identification of true hits by modeling their sparsity explicitly
- Reduced waste on borderline candidates that are unlikely to be hits
- More aggressive exploration of high-uncertainty candidates early on

**Risk**: 
- Laplace prior may be too aggressive if hits are not actually sparse
- UCB may explore too much compared to Thompson Sampling
- Mitigation: Conservative sparsity prior (1-20% range) and empirical estimation from data

## Novelty

**Strategy Tags**: `['sparsity', 'laplace', 'mixture', 'ucb']`

**New Tag**: **'sparsity'** - This is the first candidate to explicitly model and exploit the sparsity of hits in the gene perturbation space.

**Most Similar To**: Candidate 2 (both use continuous score modeling rather than binary hits)

**Key Differences from Candidate 2**:
- Candidate 2: Gaussian-Gamma model assumes all genes have effects following a normal distribution
- Candidate 5: Two-component mixture explicitly separates sparse hits from dense background
- Candidate 2: Thompson Sampling for exploration-exploitation
- Candidate 5: UCB with uncertainty quantification
- Candidate 2: Gene clustering for information sharing
- Candidate 5: Global sparsity estimation for information sharing

**Different from Recent Candidates**:
- Candidate 3: Added conservative updates (minor refinement)
- Candidate 4: Added exploration bonus decay (minor refinement)  
- Candidate 5: **Switched model family entirely** from continuous regression to sparse classification with continuous scores as features

## Hypothesis

The current Thompson Sampling approach treats all genes as having potentially interesting effects, just with different magnitudes. However, in biological systems, most genes have minimal effect on any given phenotype. By explicitly modeling this sparsity, we can:
1. More accurately identify the small subset of true hits
2. Avoid over-exploring genes that are likely background
3. Focus resources on candidates that have higher posterior probability of being hits

This is a fundamentally different approach from the previous candidates, which all maintained the Thompson Sampling framework with various refinements.