# Proposer Reasoning - Candidate 4

## What Changed

Modified the exploitation strategy in `model.py` to better target the bimodal hit distribution observed in the Sanchez21 dataset:

1. **Hit-Prioritized Sampling**: When hit information is available in history, the model now prioritizes actual hits over just high absolute scores for gene search.

2. **More Aggressive Gene Search**: Increased sampling from top performers (5 → 10 genes) and increased search depth (k=20 → k=30) to find more similar candidates.

3. **Diverse Search Fallback**: Added a second-pass diverse gene search when similar gene search doesn't yield enough candidates, providing broader coverage.

4. **Bimodal Targeting**: Added explicit targeting of both extreme negative scores (< -2.0) and near-zero scores (< 0.1) in the fallback sampling strategy, matching the observed hit distribution.

## Why This Is Better

**Evidence from History:**
- Candidate 1 → 2: Sorting by lowest scores improved hits from 8 to 15
- Candidate 2 → 3: Sorting by absolute scores improved hits from 15 to 18
- However, round 3 precision dropped to 2.34%, suggesting the absolute score approach wasn't effectively exploiting discoveries

**Hit Distribution Analysis:**
The 18 hits show a bimodal pattern:
- Extreme negatives: -4.21, -3.40, -3.35, -3.12, -3.09, -2.69, -2.68
- Near-zero: -0.10, -0.085, -0.084, -0.067, -0.048, -0.043, -0.037, -0.031, -0.027, -0.007

The current absolute score approach treats both extremes equally but doesn't effectively use the hit label or gene search to find similar candidates.

## Expected Impact

This change should:
1. **Increase hit rate**: Better targeting of both hit modes should improve precision in later rounds
2. **Better exploitation**: More aggressive gene search around actual hits should find more promising candidates
3. **Maintain diversity**: Diverse search fallback prevents over-concentration in one region
4. **Conservative improvement**: This is a targeted refinement of the existing strategy, not a risky rewrite

The modification is low-risk because it builds on the proven absolute score approach while adding better hit utilization and more comprehensive gene search.