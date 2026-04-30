# Evolution Proposal - Candidate 5

## What Changed

Replaced the UCB-based selection algorithm with **Thompson Sampling** using a Beta-Bernoulli model.

**Key changes:**
1. **Algorithm Family Switch**: From UCB (upper confidence bound optimization) to Thompson Sampling (Bayesian posterior sampling)
2. **Model**: Beta-Bernoulli model where:
   - Each candidate's hit probability is modeled with a Beta prior/posterior
   - Alpha = 1 + number_of_hits (Jeffreys prior + successes)
   - Beta = 1 + number_of_trials - number_of_hits (Jeffreys prior + failures)
3. **Selection Mechanism**: Sample from posterior distributions and select candidates with highest sampled probabilities
4. **Family Bonus Integration**: Family statistics used to create informed priors for never-seen candidates (pseudo-counts approach with 0.5 weight)

## Why This Change

**Theoretical Motivation:**
- Thompson Sampling is known to achieve optimal regret bounds in Bernoulli bandits
- It naturally balances exploration and exploitation through posterior sampling
- More elegant than manually tuning exploration constants (2.0 → 2.5 in candidate 3)

**Observed Patterns from History:**
- Candidate 1→2 (22.37→26.74): Switching to absolute scores helped (extreme effects matter)
- Candidate 2→3 (26.74→27.77): Tuning exploration constant helped slightly
- Candidate 3→4 (27.77→29.41): Adding family bonus helped significantly
- All improvements were incremental refinements of the same UCB approach

**Hypothesis:**
The UCB approach may be over-optimizing the bound rather than the actual objective. Thompson Sampling's probabilistic approach may better handle the exploration-exploitation tradeoff, especially when combined with family-based priors.

## Expected Impact

**Positive:**
- Better handling of uncertainty through Bayesian inference
- More principled exploration-exploitation balance
- Strong theoretical guarantees for Bernoulli outcomes
- Family-based priors provide intelligent exploration guidance

**Risks:**
- May initially perform worse if hit definition is noisy
- Less aggressive than UCB with high exploration constant
- Family prior weighting (0.5) is heuristic

**Target Metric:** Aiming for final_score > 29.41 (current best)

## Novelty

**Strategy Tags:** ['bayesian']

**New Tag Justification:**
- Previous candidates used UCB variants with incremental modifications
- Recent strategy tags: ['feature', 'uncertainty']
- Thompson Sampling introduces Bayesian inference and posterior sampling, representing a fundamentally different algorithmic paradigm from UCB's frequentist confidence bounds

**Most Similar To:** Candidate 4 (both use family information)

**Key Differences:**
- Candidate 4: Family bonus as additive term in UCB score
- Candidate 5: Family statistics as Bayesian prior in posterior sampling
- Different exploration mechanism: sampling vs. confidence bound optimization
- Different theoretical foundation: Bayesian inference vs. concentration inequalities

## Exploration Round Context

This is a scheduled exploration round (every 5 candidates). The change represents a meaningfully different approach:
- Switches algorithm family from UCB to Thompson Sampling
- Changes objective from optimizing upper confidence bounds to sampling from posterior distributions
- Introduces Bayesian inference as core mechanism

This is not a minor hyperparameter tweak but a fundamental algorithmic shift that satisfies the novelty constraint and exploration mandate.