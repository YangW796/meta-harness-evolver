# Proposer Reasoning - Candidate 3

## What Changed
Modified the exploitation strategy in `model.py` to correctly interpret scores for the task objective. Specifically:

1. **Score Interpretation**: Changed sorting from descending (higher is better) to ascending (lower/negative is better) to match the task objective (negative scores boost T cell proliferation).

2. **Comments**: Updated comments to clarify that negative scores are the target.

## Why This Is Better
The previous strategy (candidate_1) used descending sort which prioritized positive scores. The key insights from candidate_1's results:

- **Hits have strongly negative scores**: ARMH4 (-0.474) and HLA-DPA1 (-0.344)
- **Task rewards negative scores**: The goal is to find genes that boost T cell proliferation when knocked out
- **Current model was backwards**: Sorting in descending order was actively selecting against the hits

Candidate_2 attempted this fix but introduced syntax errors (broken indentation). This candidate applies the correct fix cleanly.

## Expected Impact
- **Higher hit rate**: By correctly biasing selection toward negative-scoring candidates, we should find more hits per batch
- **Better ncg score**: More hits earlier in the selection process improves normalized cumulative gain
- **Conservative improvement**: This is a minimal, targeted change that fixes the core logic error while maintaining the existing exploration-exploitation framework

This is a low-risk, high-reward modification that directly addresses the fundamental flaw in the previous model's exploitation logic.