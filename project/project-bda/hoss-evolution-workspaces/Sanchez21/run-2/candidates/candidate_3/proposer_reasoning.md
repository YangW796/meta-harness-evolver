# Proposer Reasoning - Candidate 3

## What Changed

Fixed the exploitation logic in `model.py` (lines 56-84) to actually use the weighted sampling results instead of discarding them.

**Before:** The code performed weighted sampling on history indices based on score extremity (absolute deviation from median), but then threw away this carefully computed information and just selected random available candidates:
```python
exploit_set.add(rng.choice(available))  # Random selection - wastes the weighted sampling!
```

**After:** The weighted sampling now actually guides selection. We first try to select the historically high-value candidates (those with extreme scores) if they're still available:
```python
hist_idx = history[idx]['candidate_index']
if hist_idx in available:
    exploit_set.add(hist_idx)
```

Only if we need more candidates do we fall back to random sampling from the available pool.

## Why This Is Better

The evolution history shows:
- **Candidate 1** (score: 20.19): Pure random + naive exploitation
- **Candidate 2** (score: 23.07): Introduced weighted sampling based on score extremity

The improvement from candidate 1 to 2 came from recognizing that hits occur at both extremes:
- Very negative scores (e.g., -3.4, -4.2)
- Scores near zero (e.g., -0.03, -0.007)

However, candidate 2's implementation was fundamentally flawed - it computed smart weights then ignored them! The weighted sampling told us *which historical candidates were most promising*, but the code discarded this and picked randomly.

My fix ensures the weighted sampling actually matters. By preferentially selecting the historically extreme-scoring candidates (when available), we:
1. Actually exploit the knowledge gained from previous rounds
2. Focus on regions of the search space that have proven to yield hits
3. Maintain the exploration fallback when needed

## Expected Impact

This should improve the final score by:
- Better exploitation of historical data (higher precision in later rounds)
- More efficient search of the candidate space
- Better cumulative hits and NCG metrics

The change is minimal and low-risk (conservative exploit mode), maintaining the same overall structure while fixing the critical flaw in the exploitation logic.
