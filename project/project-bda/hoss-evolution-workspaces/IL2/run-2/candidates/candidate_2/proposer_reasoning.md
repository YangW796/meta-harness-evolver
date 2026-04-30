# Proposer Reasoning - Candidate 2

## What Changed

Modified `model.py` to incorporate continuous score information into the Thompson Sampling framework. Specifically:

1. **Enhanced gene statistics tracking**: Now tracking not just hits and trials, but also `sum_score` and `max_score` per gene.

2. **Score-weighted probability boosting**: After sampling from the Beta posterior, the sampled probability is now adjusted based on the average score of each gene:
   - Genes with positive average scores (> 0.1) get their probability boosted by multiplying by `(1.0 + avg_score)`
   - Genes with negative average scores (< -0.1) get their probability penalized by multiplying by `(1.0 + avg_score)`
   - The probability is capped at 1.0 to maintain valid probability range

## Why This Change

From analyzing the metrics.json from candidate_1:
- The current Thompson Sampling approach only uses hit information (binary 0/1)
- However, the actual scores contain valuable continuous information:
  - The two hit genes (DCTN5: 0.50045, MEMO1: 0.73471) have very high positive scores
  - Many non-hit genes still have positive scores (e.g., ALYREF: 0.19903, SH3BP5: 0.17998)
  - Some genes have strongly negative scores (e.g., TIMM10B: -0.28268, SSBP3: -0.23246)

The original approach treats all non-hit genes equally, but genes with high positive scores are more promising than genes with negative scores, even if they didn't cross the hit threshold.

## Expected Impact

This change should:
1. **Better prioritize promising genes**: Genes with consistently high (but sub-threshold) scores will be selected more often
2. **Reduce selection of poor performers**: Genes with negative scores will be deprioritized
3. **Improve hit rate**: By using the continuous score signal, we should be able to identify more hits in subsequent rounds
4. **Maintain exploration**: The Thompson Sampling framework still ensures exploration, but now with better-informed probabilities

This is a conservative, targeted improvement that builds on the existing Thompson Sampling framework while making better use of available information.
