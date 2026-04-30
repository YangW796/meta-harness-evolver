# Proposer Reasoning — candidate_4

## What Changed

Modified the Thompson Sampling strategy in `model.py` to include an **explicit exploration bonus** based on posterior variance:

1. **Added variance-based exploration**: Instead of sampling purely from the posterior predictive distribution, the algorithm now computes the standard deviation (uncertainty) for each candidate and adds an exploration bonus: `exploration_sample = mean_sample - exploration_coeff * std_dev`

2. **Adaptive exploration coefficient**: The exploration coefficient starts at 2.0 in early rounds and decays to 0.5 by the final round, balancing aggressive early exploration with focused exploitation later.

3. **Round estimation**: The algorithm estimates the current round from history to calibrate the exploration decay schedule.

## Why This Change

**Analysis of prior candidates:**
- Candidate 1 → 2: Switching from binary (Beta) to continuous (Gaussian-Gamma) modeling improved scores (16.8 → 20.3)
- Candidate 2 → 3: Conservative Bayesian update prevented overfitting and further improved scores (20.3 → 22.4)

**Problem identified:**
The current Thompson Sampling approach balances exploration and exploitation implicitly through posterior sampling. However, for this task where hits are very rare (only ~4% hit rate) and concentrated in extreme negative scores (< -2.0), we need more **targeted exploration** of high-uncertainty regions.

Looking at the metrics:
- Hits: KLF6 (-4.96), FMO1 (-4.34), CHRNB3 (-2.97)
- Most non-hits: -0.1 to -1.5 range
- The "hit zone" is in the extreme negative tail

The current pure Thompson Sampling may be too conservative in exploring unobserved candidates, especially those with high uncertainty that could be in the hit zone.

## Expected Impact

**Positive effects:**
1. **Better exploration of uncertain candidates**: High-variance candidates (especially unobserved ones in promising clusters) will be prioritized, increasing chances of finding hits
2. **Adaptive balance**: The decaying exploration coefficient ensures we explore aggressively early (when we know little) and exploit more later (when we have good models)
3. **Targeted search**: By explicitly adding variance as a bonus, we're more likely to sample from the extreme negative tail where hits reside

**Risk mitigation:**
- Minimum exploration coefficient of 0.5 prevents completely random exploration in later rounds
- The change is additive to the existing conservative Bayesian framework, maintaining stability
- Only affects the sampling step, not the posterior computation

**Expected score improvement:**
Given that candidate 3 achieved 16 hits in 384 queries (4.2% hit rate), adding better exploration should increase this to **18-20 hits** in the next round, improving the final score from 22.35 to **23.5-24.5**.

## Why This Is Better Than Prior Attempts

- **Candidate 1** used binary hit modeling (Beta), which wasted continuous score information
- **Candidate 2** improved with continuous modeling but could overfit to single observations
- **Candidate 3** fixed overfitting with conservative updates but may under-explore

**Candidate 4** builds on all prior improvements while adding explicit exploration guidance:
- Keeps the continuous Gaussian-Gamma model (from candidate 2)
- Keeps the conservative Bayesian update (from candidate 3)
- Adds variance-based exploration to find more hits faster

This is a **low-risk, targeted improvement** that addresses the specific challenge of this task: finding rare extreme-negative-scoring hits in a large search space.