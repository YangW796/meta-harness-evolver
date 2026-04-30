# Proposer Reasoning — candidate_5

## What Changed

**Model Family Switch:** Replaced Upper Confidence Bound (UCB) with Thompson Sampling using Beta distributions.

**Key Changes in model.py:**
1. **Algorithmic Approach:** Switched from UCB's deterministic optimism-under-uncertainty to Thompson Sampling's Bayesian probability matching
2. **Score Modeling:** Instead of using raw scores with exploration bonuses, we now:
   - Normalize scores to [0, 1] range
   - Model each candidate with a Beta distribution representing the probability of "success" (finding a hit)
   - Sample from the posterior distribution to select candidates
3. **Exploration Mechanism:** 
   - UCB: Explicit exploration bonus added to mean estimate
   - Thompson Sampling: Implicit exploration through posterior sampling
4. **Prior Beliefs:**
   - Explored candidates: Beta(successes + 1, failures + 1)
   - Unexplored candidates: Beta(3, 1) - optimistic prior favoring hit discovery

## Why This Is Better

**Theoretical Advantages:**
1. **Optimal Regret Bounds:** Thompson Sampling has been proven to achieve optimal regret bounds in multi-armed bandit problems, often outperforming UCB in practice
2. **Natural Exploration:** Unlike UCB which needs hand-tuned exploration parameters, Thompson Sampling naturally balances exploration and exploitation through Bayesian posterior sampling
3. **Score Agnostic:** Works well regardless of score distribution, whereas UCB's exploration bonus assumes sub-Gaussian rewards
4. **Contextual:** The Beta distribution naturally models the Bernoulli-like success/failure nature of finding hits

**Empirical Evidence from History:**
- Candidate 1→2: Adding negative bias helped (10.53 → 14.33)
- Candidate 2→3: Increasing bias helped more (14.33 → 16.94)
- Candidate 3→4: Diminishing returns (16.94 → 18.53, only +1 hit)
- The UCB approach is showing diminishing returns, suggesting we're hitting its limits

**Problem-Specific Fit:**
- Hits are rare events (only 9 hits in 512 queries = 1.76% hit rate)
- Thompson Sampling excels at finding rare good actions
- The Beta-Bernoulli model is well-suited for binary hit outcomes
- No need to manually tune exploration parameters (like the 70%→75%→80% progression in UCB)

## Expected Impact

**Short-term (Round 5):**
- May discover more hits through better exploration of uncertain candidates
- Should maintain or improve upon the 18.53 score
- Better diversity in selected candidates

**Long-term:**
- More robust to different score distributions
- Less hyperparameter sensitivity
- Better asymptotic performance as more data accumulates

**Risks:**
- Initial exploration may be more conservative than UCB's optimistic initialization
- The normalization step adds computational overhead (minimal)
- May need adjustment if score distribution changes dramatically

## Novelty

**Strategy Tags:** ['thompson_sampling', 'bayesian', 'beta_distribution']

**Comparison to Recent Candidates:**
- **Most similar to:** Candidate 4 (both aim to optimize exploration-exploitation)
- **Key differences:**
  1. Different model family: Bayesian probability matching vs. optimism-under-uncertainty
  2. Different exploration mechanism: implicit (posterior sampling) vs. explicit (exploration bonus)
  3. Different hyperparameter philosophy: minimal tuning (Beta priors) vs. manual tuning (UCB weights)
  4. Different theoretical foundations: Bayesian inference vs. concentration inequalities

**Novelty Assessment:**
- ✓ Fundamentally different algorithmic approach (not a hyperparameter tweak)
- ✓ New strategy tag: 'thompson_sampling' not in recent history
- ✓ New strategy tag: 'bayesian' not in recent history  
- ✓ New strategy tag: 'beta_distribution' not in recent history
- ✓ Addresses the explore mode requirement for a meaningfully different approach

## Hypothesis

**If Thompson Sampling is implemented,** then we expect to see:
1. Improved hit discovery in early-to-mid rounds due to better exploration
2. More consistent performance across rounds (less variance than UCB)
3. Better utilization of the limited query budget (640 total queries)
4. Potential to exceed the current best score of 18.53

The hypothesis is grounded in Thompson Sampling's theoretical optimality for Bernoulli bandits and its empirical success in similar rare-event discovery problems.