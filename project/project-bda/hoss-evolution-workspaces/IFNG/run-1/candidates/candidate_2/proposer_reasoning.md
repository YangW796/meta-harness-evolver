# Proposer Reasoning - Candidate 2

## What Changed
Modified the UCB (Upper Confidence Bound) selection strategy in `model.py` to better explore both extremes of the score distribution, with a bias toward negative scores.

**Specific change**: In the unexplored candidate initialization (lines 84-90), instead of only using `max_score` for optimistic initialization, the policy now:
1. Calculates both `min_observed_score` and `max_observed_score` from history
2. For unexplored candidates, creates a blended UCB score: `0.7 * ucb_negative + 0.3 * ucb_positive`
3. `ucb_negative = min_observed_score - 0.1 * abs(min_observed_score)` (exploration bonus for negative direction)
4. `ucb_positive = max_observed_score + 0.1 * abs(max_observed_score)` (exploration bonus for positive direction)

## Why This Change
Analysis of candidate_1's results revealed:
- **Hit pattern**: The 2 hits found were AARS1 (score: -0.400) and ABCB7 (score: -0.505)
- **Current strategy weakness**: The original UCB used only `max_score` for unexplored genes, biasing selection toward potentially high-positive-score genes
- **Task insight**: The goal is to find genes that "regulate IFNG production," which includes both enhancers (positive scores) and suppressors (negative scores). The hit definition in this dataset appears to favor strong negative regulators

## Expected Impact
**Positive**: 
- Better exploration of the negative score space where hits are located
- Higher probability of discovering additional hit genes in early rounds
- Improved ncg and cumulative_hits metrics by finding more hits within the query budget

**Conservative nature**: 
- This is a calibration change, not a wholesale rewrite
- Maintains the UCB framework's theoretical guarantees
- Only affects unexplored candidates (exploration behavior)
- The 70/30 negative/positive split is tunable but provides strong bias toward hit-discovery

## Why Better Than Prior Attempts
Candidate_1 established a baseline UCB implementation. This evolution specifically addresses the observed hit distribution (extreme negative scores) that the baseline didn't account for. By biasing exploration toward the negative tail while maintaining some positive exploration, we expect to discover more hits without sacrificing the exploration-exploitation balance.