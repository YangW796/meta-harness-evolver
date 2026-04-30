# Proposer Reasoning — candidate_4

## Evolution History Analysis

**Score Progression:**
- Candidate 1: 10.53 (2 hits, round 0)
- Candidate 2: 14.93 (10 hits, rounds 0-1) - Added diverse exploration (40%)
- Candidate 3: 18.08 (16 hits, rounds 0-2) - Increased diverse exploration to 60%

**Key Observation:**
While total hits increased from 10 to 16 between candidates 2 and 3, the **precision dropped significantly**:
- Round 1 (candidate 2): 8 hits / 128 = 6.25% precision
- Round 2 (candidate 3): 6 hits / 128 = 4.69% precision

This suggests that increasing diverse exploration from 40% to 60% helped find more total hits but reduced per-round efficiency.

## Hypothesis

The current 60% allocation to diverse exploration is **too aggressive**, leaving insufficient budget for Thompson Sampling to exploit the knowledge gained from previous rounds. The diverse search is finding new regions, but Thompson Sampling needs more samples to effectively model and select the best candidates from what we've learned.

## Targeted Change

**File:** `harness/model.py`  
**Line:** 106  
**Change:** Reduced diverse exploration allocation from 60% to 45%

```python
# Before:
num_diverse = min(len(diverse_available), batch_size * 3 // 5)  # 60%

# After:
num_diverse = min(len(diverse_available), batch_size * 45 // 100)  # 45%
```

## Expected Impact

1. **Better Balance:** 45% diverse exploration + 55% Thompson Sampling (vs. 40%/60% split)
2. **Higher Precision:** Thompson Sampling will have more budget to select promising candidates based on historical data
3. **Continued Exploration:** Still maintains substantial diverse exploration (45% vs. original 40%)
4. **Conservative Improvement:** This is a small, low-risk adjustment in "exploit mode"

## Why This Is Better

- Candidate 2 showed that 40% diverse exploration works well (6.25% precision)
- Candidate 3 showed that 60% diverse exploration finds more total hits but reduces per-round efficiency
- The 45% compromise should retain the benefits of diverse exploration while improving Thompson Sampling's ability to exploit learned patterns
- This follows the "conservative, low-risk" guideline for exploit mode