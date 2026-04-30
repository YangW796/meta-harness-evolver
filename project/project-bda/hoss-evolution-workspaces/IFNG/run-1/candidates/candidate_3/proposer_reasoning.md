# Evolution Proposal — candidate_3

## What Changed

Made two targeted adjustments to the UCB selection policy in `model.py`:

1. **Fixed UCB exploration bonus calculation**: Changed from using `sum(candidate_counts.values())` to `len(history)` for the total observation count in the exploration term `sqrt(2 * ln(n) / count)`. This corrects the UCB formula to use the total number of observations made, not the sum of visit counts per candidate.

2. **Increased negative bias**: Changed the unexplored candidate exploration blend from 70%/30% (negative/positive) to 75%/25%, further prioritizing exploration of the negative score region where all hits have been found.

## Why This Change

**Analysis of History:**
- Candidate 1 (baseline UCB): 2 hits at scores -0.4002 (AARS1) and -0.5053 (ABCB7)
- Candidate 2 (70% negative bias): Found 1 additional hit at -0.4993 (ZSCAN18), improving score from 10.53 to 14.33

**Key Insight:**
All 3 hits are clustered in the extreme negative tail (scores -0.4 to -0.51), confirming that the hit distribution is heavily skewed toward very negative values. The 70% negative bias helped, suggesting even more bias could be beneficial.

**UCB Formula Correction:**
The standard UCB formula uses `ln(n)` where `n` is the total number of observations (arm pulls), not the sum of individual visit counts. Using `sum(candidate_counts.values())` is mathematically incorrect and can over-penalize exploration. Using `len(history)` properly represents the total number of observations made across all candidates.

## Expected Impact

1. **Better exploration-exploitation balance**: The corrected UCB formula should more properly balance between exploiting known good candidates and exploring uncertain ones.

2. **Increased hit discovery**: The stronger negative bias (75% vs 70%) should prioritize exploration of candidates more likely to be extreme negatives, potentially finding more hits in the limited query budget.

3. **Conservative improvement**: This is a low-risk change—it doesn't alter the overall strategy, just calibrates the exploration mechanism and slightly increases focus on the promising negative region.

## Risk Assessment

Low risk. The change is:
- Mathematically well-founded (corrects UCB to standard formulation)
- Incremental (only 5% increase in negative bias)
- Consistent with observed data (all hits are strongly negative)
- Does not change function signatures or IO behavior

The policy should remain stable and fast, with potential for improved hit discovery in early rounds where exploration matters most.