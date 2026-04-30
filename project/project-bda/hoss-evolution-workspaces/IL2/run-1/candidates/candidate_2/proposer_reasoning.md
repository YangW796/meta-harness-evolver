# Evolution Proposal Reasoning

## What Changed
Made two targeted improvements to the selection policy in `model.py`:

1. **Increased hit weighting**: Changed the hit bonus from `2.0` to `10.0` in the candidate scoring formula, making hits dominate over raw scores
2. **Improved gene search strategy**: 
   - Prioritize searching for similar genes to HIT genes first
   - Increased `k` from 5 to 10 for more similar candidates
   - Fixed duplicate filtering by checking against `exploit_pool` in addition to `selected`
   - Added deduplication to avoid searching the same gene multiple times

## Why This Change
From the metrics analysis:
- Current model found only 2 hits out of 128 queries (1.56% precision)
- Hit genes: DCTN5 (0.50045) and MEMO1 (0.73471)
- The hit metric is the actual target, not raw scores

The original implementation had two issues:
1. **Weak hit prioritization**: A hit bonus of 2.0 is too small - hits should dominate the selection strategy since they represent the actual optimization target
2. **Inefficient gene search**: The similar gene search wasn't prioritizing hit genes, and had logic issues with duplicate filtering

## Expected Impact
This should improve hit discovery by:
1. **Better exploitation**: Hit genes and their similar neighbors will be prioritized much more aggressively
2. **More candidates from hit regions**: Increasing k from 5 to 10 and prioritizing hit genes first should populate the exploit pool with more promising candidates
3. **Reduced wasted queries**: Proper deduplication ensures we don't waste searches on the same gene

The change is conservative (only modifying weights and search parameters) while targeting the core weakness: insufficient prioritization of the actual target metric (hits).
