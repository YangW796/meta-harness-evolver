# Proposer Reasoning — candidate_4

## What Changed

Modified `model.py` line 96 to increase the negative bias weight for unexplored candidates from **75% to 80%**.

**Before:**
```python
ucb = 0.75 * ucb_negative + 0.25 * ucb_positive
```

**After:**
```python
ucb = 0.8 * ucb_negative + 0.2 * ucb_positive
```

## Why This Change

### Evidence from Evolution History

1. **Candidate 1 (Score: 10.53)**: Used optimistic initialization based on max score. Found 2 hits in 128 queries.

2. **Candidate 2 (Score: 14.33)**: Introduced 70% negative bias after recognizing hits have negative scores. Found 1 additional hit in round 2 (3 total).

3. **Candidate 3 (Score: 16.94)**: Increased negative bias to 75%. Found 5 hits in round 2 alone (8 total), achieving 3.9% precision.

### Key Insight

Analysis of hit scores in the metrics shows:
- Hits occur at strongly negative scores: -0.391, -0.443, -0.446, -0.478, -0.390
- The hit threshold appears to be around -0.38 to -0.40
- No hits observed in positive score ranges

The progressive improvement (70% → 75%) demonstrates that **increased negative bias directly correlates with better hit discovery**.

## Expected Impact

By increasing the negative bias to 80%, the policy will:
1. **Explore more aggressively** in the negative score region where hits are concentrated
2. **Prioritize unexplored candidates** that are more likely to be extreme negative outliers
3. **Improve hit rate** in early rounds by reducing exploration of less promising positive-scoring candidates

This is a **conservative, evidence-based refinement** that follows the established successful pattern while remaining in exploit mode (recent best updated within 5 candidates).

## Risk Assessment

**Low risk** because:
- The change is minimal (5% adjustment to existing working logic)
- It extends a proven successful pattern (70% → 75% → 80%)
- It doesn't alter the core UCB algorithm or exploration mechanics
- The policy remains robust with fallback to random selection when history is empty

**Expected outcome**: Modest improvement in hit discovery rate (1-3 additional hits) leading to a final score of 17.5-18.5.