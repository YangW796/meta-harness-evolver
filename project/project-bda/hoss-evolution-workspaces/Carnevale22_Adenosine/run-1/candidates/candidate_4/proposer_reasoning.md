# Proposer Reasoning - Candidate 4

## What Changed
Modified the exploitation strategy in `model.py` to prioritize **hit genes** over raw negative scores when available.

**Key change**: The exploitation logic now checks for `hit == 1` in the history first, and only falls back to score-based selection if no hits are found.

## Why This Is Better

### Analysis of Previous Results
From the metrics.json analysis:
- **7 total hits found** in 256 queries (candidate_3 score: 23.32)
- **Hit threshold**: All hits have strongly negative scores (range: -0.344 to -0.569)
- **Hit definition**: The task defines hits as genes that boost T cell proliferation

### The Problem with Score-Only Exploitation
The current model (candidate_3) correctly sorts by ascending score (prioritizing negative values), but it doesn't distinguish between:
- A gene with score -0.3 that is **not a hit**
- A gene with score -0.35 that **is a hit**

Both contribute to the "top performers" list, but only the hit gene satisfies the actual task objective.

### The Solution: Hit-First Exploitation
By prioritizing confirmed hits:
1. **Better signal**: Hits are the ground-truth objective, not just a proxy (negative scores)
2. **Faster convergence**: Once we find hits, we focus exploitation on similar patterns
3. **Conservative improvement**: Minimal change that leverages existing exploration framework
4. **Robust fallback**: If no hits exist yet, falls back to the current score-based strategy

## Expected Impact
- **Higher hit rate in later rounds**: Once hits are discovered (round 1 had 5 hits), round 2+ should find more hits by exploiting the hit signal
- **Better ncg**: Prioritizing confirmed hits should improve normalized cumulative gain
- **Low risk**: This is a targeted refinement of the existing successful strategy from candidate_3

## Pattern from History
- Candidate 1 → Candidate 3: Fixed score interpretation (ascending sort) → **Score improved from 20.76 to 23.32**
- Candidate 3 → Candidate 4: Now fixing exploitation signal (hit-first) → **Expected further improvement**

This continues the trend of making the model better aligned with the actual task objective.