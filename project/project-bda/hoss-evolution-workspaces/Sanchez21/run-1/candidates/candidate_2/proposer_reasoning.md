# Proposer Reasoning - Candidate 2

## What Changed
Modified line 62 in `model.py`: Changed the sorting direction for historical scores from descending (highest first) to ascending (lowest first).

**Before:**
```python
sorted_history = sorted(history, key=lambda x: x['score'], reverse=True)
```

**After:**
```python
sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
```

## Why This Change
Analysis of the hit patterns from candidate_1's metrics.json revealed:

1. **All 8 hits have negative scores** (range: -0.03 to -4.21)
2. **The strongest hits have the most negative scores**: CCDC84 (-4.21), CLDN7 (-3.40), COX7A1 (-3.09), PSAP (-3.12), LPPR5 (-2.68)
3. The task measures "change in tau protein level" where negative values indicate decreased tau expression
4. The current model was selecting genes similar to the **highest** scorers, but hits are actually the **lowest** (most negative) scorers

This is a **sign alignment bug**: the exploitation strategy was optimizing in the wrong direction.

## Expected Impact
- **Improved hit rate**: By exploiting genes with the most negative scores (which are the actual hits), the model should find more hits in subsequent rounds
- **Better NCG score**: Prioritizing the extreme negative tail should yield higher normalized cumulative gain
- **Conservative change**: This is a minimal, low-risk edit that doesn't change the overall exploration-exploitation structure, only fixes the direction of exploitation

## Why This Is Better
- **Data-driven**: Directly addresses the observed mismatch between selection criteria and hit distribution
- **Task-aware**: Aligns with the biological objective of finding genes that decrease tau protein
- **Low risk**: Single line change with clear semantics; maintains all other diversity and exploration mechanisms