# Proposer Reasoning - Candidate 5

## What Changed

Replaced the weighted random sampling exploitation strategy with **Thompson Sampling**, a Bayesian multi-armed bandit algorithm.

**Specific change in `model.py`:**
- Removed the position-based weighted sampling (lines 84-100 in original)
- Added Thompson Sampling implementation that:
  - Maintains Beta distributions for each candidate based on observed hits/misses
  - Samples from the posterior distribution to balance exploration-exploitation
  - Uses optimistic initialization (0.7-1.0) for unexplored candidates
  - Selects candidates with highest sampled probabilities

## Why This Change

**Evolution History Analysis:**
- Candidate 1 → 3: Fixed score direction (ascending for negative scores) → +5 hits
- Candidate 3 → 4: Prioritized confirmed hits over raw scores → +8 hits  
- Current best (Candidate 4): 15 hits in 384 queries (3.9% hit rate)

**Problem with Current Approach:**
The weighted random sampling uses candidate list **position** as a proxy for diversity, which is biologically meaningless. It treats the candidate list as having spatial structure when it likely doesn't.

**Thompson Sampling Advantages:**
1. **Principled Exploration-Exploitation**: Naturally balances trying promising candidates vs exploring uncertain ones
2. **Bayesian**: Incorporates uncertainty - candidates with few observations have higher variance
3. **Hit-Focused**: Directly optimizes for hit probability rather than continuous scores
4. **Adaptive**: Automatically adjusts exploration rate based on observed performance

## Expected Impact

**Quantitative:**
- Increase hit rate from 3.9% to 5-7% (target: 20-25 hits in next 128 queries)
- Improve final score from 25.77 to 28-30
- Better cumulative hit progression in later rounds

**Qualitative:**
- More efficient use of query budget
- Better identification of promising gene regions
- Reduced wasted queries on low-potential candidates

## Novelty

**Strategy Tags:** `bandit`, `bayesian`, `thompson-sampling`

**Recent Strategies to Avoid:** `feature`, `nn`

**Most Similar To:** Candidate 4 (both prioritize hits)

**Key Differences:**
- Candidate 4: Uses hit prioritization with crude diversity sampling
- Candidate 5: Uses hit prioritization with principled Bayesian bandit algorithm
- Switches from heuristic weights to probabilistic inference
- Introduces uncertainty quantification via posterior sampling

This is a **model-family switch** from heuristic weighted sampling to principled Bayesian bandit algorithms, fitting the exploration round requirement.