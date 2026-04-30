# Evolution Proposal: Candidate 2

## What Changed

Modified the UCB (Upper Confidence Bound) algorithm in `model.py` to use the **absolute value** of mean scores for the exploitation term, rather than the raw signed scores.

**Before:**
```python
exploitation = mean_scores[idx]
```

**After:**
```python
exploitation = abs(mean_scores[idx])
```

## Why This Change

Analysis of candidate_1's results revealed the hit pattern:
- Hits occurred at **extreme score values** in both directions:
  - Large negative: ATP6V0D1 (-0.9752), FBXO4 (-0.56094), RIMBP3B (-0.34541)
  - Large positive: CDH13 (0.52117), ABCB1 (0.34192)

The original UCB algorithm treated positive and negative scores asymmetrically, potentially favoring positive-scoring genes even if their absolute effect was small. Since the task is to find genes with **extreme perturbations** (large absolute effects), the algorithm should prioritize candidates based on the magnitude of their effect, not its direction.

## Expected Impact

This change should improve the policy's ability to:
1. **Identify hits more efficiently**: By focusing on absolute effect size, the algorithm will prioritize genes with large deviations regardless of sign
2. **Better exploration-exploitation balance**: Genes with large negative effects (which are also hits) will now receive appropriate UCB scores for follow-up
3. **Increase cumulative hits**: With a more accurate utility function, the policy should discover more hits within the query budget

This is a conservative, targeted improvement that maintains the UCB framework while better aligning the exploitation term with the actual objective (finding extreme outliers).
