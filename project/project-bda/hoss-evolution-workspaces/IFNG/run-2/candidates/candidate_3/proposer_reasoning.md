# Evolution Proposer Reasoning - Candidate 3

## What Changed
Increased the diverse gene search allocation from 40% to 60% of batch size when no hits have been discovered yet.

**Specific change in `model.py`:**
- Line 106: Changed `batch_size * 2 // 5` to `batch_size * 3 // 5`
- This increases diverse exploration from 40% (51 genes) to 60% (76 genes) of the 128-gene batch

## Why This Change

### Historical Performance Analysis
- **Candidate 1** (baseline Thompson Sampling + similar gene search): 2 hits in round 1 (1.56% precision)
- **Candidate 2** (added diverse search at 40% allocation): 8 hits in round 2 (6.25% precision)
- The diverse gene search strategy showed a **4x improvement** in hit rate

### Hypothesis
The diverse gene search (`diverse=True`) is highly effective at discovering new hit-rich regions of the gene space. By increasing its allocation from 40% to 60%, we:
1. **Enhance exploration**: Allocate more resources to discovering diverse gene families early
2. **Accelerate hit discovery**: Find promising regions faster in the limited query budget (5 rounds)
3. **Balance exploration-exploitation**: Still retain 40% for Thompson Sampling to refine selection

### Expected Impact
- **Higher early-round hit rates**: More diverse exploration should yield more hits in rounds 2-3
- **Better cumulative hits**: With 60% diverse search, expect 10-12 hits per round vs. 8 with 40%
- **Improved final score**: Target 16-18 total hits (up from 10) for a score of ~16-18

### Risk Assessment (Conservative Exploit Mode)
This is a **low-risk, targeted adjustment**:
- Does not change the core algorithm (Thompson Sampling remains)
- Does not add new dependencies
- Only tunes a proven successful parameter (diverse search proportion)
- Maintains the same random seed behavior and overall structure

The diverse search has already proven effective; this change simply increases its resource allocation to maximize its impact within the query budget constraints.