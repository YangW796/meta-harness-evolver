# Evolution Proposal: Candidate 4

## What Changed

Enhanced the Thompson Sampling score boosting mechanism to consider both **average score** and **maximum observed score** (max_score) when prioritizing genes.

**Specific change in `model.py` (lines 88-99):**
- Added tracking of `max_score` for each gene (was already being calculated but not used)
- Added two new boosting conditions based on extreme values:
  - Boost genes with `max_score > 0.3` (shown strongly positive behavior at least once)
  - Boost genes with `max_score < -0.3` (shown strongly negative behavior at least once)
- The max_score boost is multiplicative with the existing avg_score boost

## Why This Change

**Analysis of hit patterns:**
- All 13 hits have extreme scores: either >0.38 or <-0.33
- The current model only boosts based on average score, which can miss genes that showed one extreme measurement but have moderate average
- Example: A gene with scores [0.4, 0.1, 0.1] has avg=0.2 (gets moderate boost) but max=0.4 (indicating hit potential)

**Evolution history context:**
- Candidate 1→2 (+4.22 score): Added continuous score information (avg_score)
- Candidate 2→3 (+1.8 score): Started boosting extreme negative scores instead of penalizing them
- **Candidate 3→4 hypothesis**: Add max_score awareness to catch genes with sporadic extreme behavior

## Expected Impact

**Positive effects:**
1. Better identification of genes with "sporadic extreme" behavior patterns
2. More aggressive pursuit of genes that have shown any extreme values (|score| > 0.3)
3. Complementary to existing avg_score boosting (both can apply multiplicatively)

**Risk mitigation:**
- Conservative thresholds (0.3 for max_score vs 0.1 for avg_score positive) to avoid over-boosting noisy signals
- Only applies to genes already in the Thompson Sampling pool (not changing exploration)
- Maintains all existing logic, just adds an additional boost factor

**Target metric improvement:**
- Expect to find 1-3 additional hits in the next round (current: 13 hits over 3 rounds)
- Should improve ncg by better prioritizing extreme-scoring candidates
- Low risk as it's an additive enhancement to proven successful approach

## Why This Is Better Than Prior Attempts

This is a **precision refinement** rather than a fundamental strategy change:
- Candidate 2 introduced score-based boosting (proven successful)
- Candidate 3 refined negative score treatment (proven successful)  
- Candidate 4 adds a complementary signal (max_score) that the existing successful framework can leverage

The model already tracks max_score but doesn't use it—this change extracts additional signal from existing data without adding computational cost or complexity.