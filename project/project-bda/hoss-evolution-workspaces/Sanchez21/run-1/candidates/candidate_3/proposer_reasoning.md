# Proposer Reasoning - Candidate 3

## What Changed
Modified the exploitation strategy in `model.py` to target both extremes of the score distribution (very negative AND very positive) instead of only targeting the most negative scores.

**Specific change:** Line 62-66
- **Before:** `sorted(history, key=lambda x: x['score'], reverse=False)` - prioritized lowest (most negative) scores
- **After:** `sorted(history, key=lambda x: abs(x['score']), reverse=True)` - prioritizes highest absolute scores (both tails)

## Why This Change
Analysis of the hit patterns in the metrics shows that hits occur at BOTH extremes:
- Strong negative scores (e.g., -3.09)
- Scores near zero/mildly positive (e.g., -0.03, -0.04)

The task definition confirms this: "identify genes that, when knocked out, either **increase or decrease** expression of endogenous tau protein levels."

**Evolution History Insight:**
- Candidate 1 (20.61): Sorted by score descending (positive bias)
- Candidate 2 (23.15 - best): Sorted by score ascending (negative bias) - **improved score**
- **Gap:** Still missing the positive extreme hits

The improvement from Candidate 1 to Candidate 2 came from targeting negative scores, suggesting the negative tail is important. However, the hit definition is clearly two-tailed, so we should exploit BOTH directions.

## Expected Impact
By targeting absolute scores (both extremes), the model should:
1. **Find more hits per round** - Can discover both positive and negative effect genes
2. **Improve ncg and final_score** - Better coverage of the hit distribution
3. **Maintain exploration** - The exploration ratio and gene search mechanisms remain unchanged

This is a conservative, targeted change that addresses the clear gap in the current best strategy while maintaining all other aspects of the successful hybrid approach.