# Proposer Reasoning - Candidate 4

## What Changed

Modified the exploitation strategy in `model.py` to use hit-based weighting when hit information is available in the history. The key changes:

1. **Hit-aware weighting**: When `hit` field is present in history records, the weighting now prioritizes hit candidates with a 10x multiplier
2. **Combined weighting**: Final weights combine both hit status (10x for hits, 1x for non-hits) and score extremity (absolute deviation from median)
3. **Backward compatibility**: Falls back to pure score-based weighting when hit information is not available

## Why This Change

**Problem identified from history:**
- Round 1: 8 hits (6.25% precision)
- Round 2: 7 hits (5.47% precision)  
- Round 3: 4 hits (3.13% precision)

The precision is declining each round because the current strategy tries to re-select historical candidates that are already selected. The existing score-based weighting doesn't effectively distinguish between hits and non-hits with similar score magnitudes.

**Biological rationale:**
- Genes that are hits likely share functional pathways or regulatory mechanisms with other hit genes
- By giving 10x weight to hit genes when sampling for exploitation, we bias the selection toward regions of the search space that are more likely to contain additional hits
- This is a conservative approximation of using gene similarity (like Achilles features) without requiring external dependencies

## Expected Impact

**Positive expectations:**
- Higher hit rate in exploitation phase by focusing on candidates similar to known hits
- Better use of the hit signal that was previously underutilized
- More efficient search through the candidate space

**Risks:**
- May reduce exploration diversity if hit-based weighting is too aggressive
- Could potentially miss novel hit regions if they're very different from existing hits

**Target metric improvement:**
- Aim to improve final_score from 25.41 to 26.5+ (4% improvement)
- Maintain or improve hit precision in later rounds (currently 3.13% in round 3)

## Why This Is Better Than Prior Attempts

- **Candidate 1**: Used random exploitation (no guidance from history)
- **Candidate 2**: Added score-based weighting (targets extremes but ignores hit/non-hit distinction)  
- **Candidate 3**: Tried to re-select historical candidates directly (mostly failed due to already-selected filter)
- **Candidate 4 (this)**: Uses hit signal to guide exploitation toward hit-rich regions while maintaining exploration

This is a targeted, low-risk improvement that leverages information (hit status) that was available but not fully utilized in the previous candidates.