# Evolution Proposal - Candidate 5

## What Changed

Replaced the fixed 70/30 exploit/explore strategy with **Thompson Sampling**, a Bayesian bandit algorithm:

**Key Changes in `model.py`:**
- Removed fixed 70/30 exploitation/exploration split
- Removed explicit hit weighting (previously hit * 10.0)
- Implemented Beta-Bernoulli Thompson Sampling:
  - Models each gene's hit probability with Beta(1 + hits, 1 + trials - hits) posterior
  - Samples from posterior to get exploration/exploitation balance naturally
  - Uses gene search to propagate sampled probabilities to similar genes
- Selection is now based on sampled hit probabilities rather than fixed scores

## Why This Change

**Historical Pattern Analysis:**
- Candidate 1 → 2 → 3: Progressive refinement of fixed-ratio strategy (10.95 → 14.83 → 16.48)
- All prior attempts used explicit 70/30 split with manual hit weighting
- Improvements came from better exploitation quality (gene search, filtering)

**Limitation of Prior Approach:**
The fixed 70/30 ratio is rigid:
- Early rounds: 30% exploration may be too little when we know almost nothing
- Late rounds: 30% exploration may be too much when we've found good regions
- Manual hit weighting (10x) is arbitrary and doesn't adapt

**Thompson Sampling Advantages:**
- **Adaptive balance**: Automatically adjusts exploration based on uncertainty
  - High uncertainty (few trials) → more exploration naturally
  - Low uncertainty (many trials) → more exploitation naturally
- **Bayesian optimal**: Provably near-optimal for Bernoulli bandits
- **No hyperparameters**: No need to tune 70/30 ratio or hit weights
- **Contextual**: Uses actual hit observations directly, not hand-crafted scores

## Expected Impact

**Explore Mode Goals:**
- Meaningfully different from fixed-ratio approaches
- Better adaptation to search space characteristics
- More principled exploration/exploitation balance

**Performance Expectations:**
- May underperform initially (rounds 1-2) due to high exploration
- Should improve in later rounds as posterior concentrates
- Overall: potentially higher ceiling due to adaptive balancing

**Risk:** Moderate - This is a fundamental algorithmic change, not just parameter tuning. However, Thompson Sampling is well-established and theoretically sound.

## Novelty

**Strategy Tags:** `bayesian`, `bandit`, `thompson_sampling`

**New Tags Compared to Recent Candidates:**
- `bayesian`: First use of Bayesian inference for gene selection
- `bandit`: First formulation as a multi-armed bandit problem
- `thompson_sampling`: First use of posterior sampling for exploration

**Most Similar To:** Candidate 1 (both are foundational approaches)

**Key Differences from Similar Candidate:**
- Candidate 1 used fixed-ratio heuristic (70/30)
- This candidate uses principled Bayesian bandit algorithm
- No manual tuning of exploration rate or hit weights
- Adaptive based on uncertainty quantification

**Why This is Explore-Worthy:**
Thompson Sampling represents a fundamentally different paradigm:
- Prior work: Hand-crafted heuristics with fixed exploration
- This work: Principled Bayesian method with adaptive exploration
- Switches from "rules-based" to "probability-based" selection