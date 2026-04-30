# Proposer Reasoning - Candidate 5

## What Changed

Completely replaced the fixed-ratio exploitation/exploration strategy with **Thompson Sampling**, a Bayesian bandit algorithm that dynamically balances exploration and exploitation.

**Key changes:**
1. **Thompson Sampling core**: Uses Beta distributions to model each candidate's probability of being a hit
2. **Bayesian updating**: Incorporates historical observations to update beliefs about candidate quality
3. **Dynamic balance**: No fixed 70/30 split - exploration emerges naturally from uncertainty
4. **Hit definition**: Uses both explicit hit labels (when available) and extreme score thresholds (top 5% by absolute value)

## Why This Change

**Problem with current approach:**
- All previous candidates (1-4) used fixed 70% exploitation / 30% exploration ratio
- Precision declining each round (6.25% → 5.47% → 3.13%)
- Fixed ratios don't adapt to the search space characteristics
- Score-based weighting in candidates 2-4 treats all untested candidates equally

**Thompson Sampling advantages:**
- **Theoretically optimal**: Thompson Sampling has provable optimal regret bounds for bandit problems
- **Natural exploration**: Candidates with high uncertainty get explored automatically
- **Adaptive**: As we gather more data, the algorithm becomes more exploitative naturally
- **Context-aware**: Untested candidates near known hits get higher probability through empirical priors

**Biological rationale:**
- Genes related to known hits likely share pathways and have similar perturbation effects
- Bayesian approach allows us to express this as a prior belief that gets updated with evidence
- Unlike fixed ratios, this can discover "hot regions" of the search space more efficiently

## Expected Impact

**Positive expectations:**
- Better adaptive balance between exploration and exploitation
- Higher hit rate in later rounds by focusing on promising regions
- More efficient search through the candidate space
- Better utilization of the hit signal through Bayesian updating

**Risks:**
- More complex than previous approaches (but still simple implementation)
- Requires tuning of prior parameters (using empirical data mitigates this)
- May initially explore more than exploit if hit rate is very low

**Target metric improvement:**
- Aim to improve final_score from 25.41 to 27+ (6% improvement)
- Improve or maintain hit precision in round 3 (currently 3.13%)
- Better cumulative hits through more intelligent selection

## Novelty

**Chosen strategy tags:**
- `thompson-sampling`
- `bayesian`
- `bandit-algorithm`

**Most similar to:** Candidate 2 (both use statistical modeling of score distributions)

**How this differs:**
- **Model family**: Moves from heuristic weighting to principled Bayesian inference
- **Exploration/exploitation**: Dynamic balance instead of fixed 70/30 ratio
- **Theoretical foundation**: Thompson Sampling has proven optimality properties that heuristic approaches lack
- **Uncertainty quantification**: Explicitly models uncertainty about each candidate, which guides exploration naturally

This is a meaningfully different approach that switches from heuristic score-based weighting to a theoretically-grounded Bayesian bandit algorithm, representing a true model family change as required for explore mode.