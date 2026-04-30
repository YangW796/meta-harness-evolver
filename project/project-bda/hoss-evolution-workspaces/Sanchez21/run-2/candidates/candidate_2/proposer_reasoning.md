# Evolution Proposal: Candidate 2

## What Changed

Modified the exploitation strategy in `model.py` from pure random selection to **absolute score-based weighted sampling**.

**Key changes:**
1. **Removed ineffective top_percentile filtering** - The previous code calculated top 30% but then ignored it
2. **Introduced weighted sampling based on absolute deviation from median** - Candidates with extreme scores (both very negative and near-zero) receive higher weights
3. **Mapping to available pool** - Selected high-weight regions are mapped to the available candidate pool

## Why This Is Better

**Problem with current approach:**
- The "exploitation" phase (70% of selections) was purely random
- It completely ignored the historical score data
- No mechanism to preferentially select candidates similar to high-performing ones

**Solution:**
- Analyze historical scores to identify what makes a "hit" (score extremes)
- From candidate_1 results, hits occur at both:
  - Very negative scores: -4.21, -3.40, -3.12, -2.68
  - Near-zero scores: -0.03, -0.08, -0.10
- Weighted sampling by absolute deviation from median naturally targets both extremes
- Higher weight = higher probability of selection in exploitation phase

## Expected Impact

- **Higher hit rate**: By focusing exploitation on extreme-score regions, should discover more hits per batch
- **Better ncg score**: Earlier discovery of high-value candidates improves normalized cumulative gain
- **Conservative improvement**: Maintains 30% exploration to avoid getting stuck in local optima
- **Robust**: Works with any score distribution (handles both negative and positive extremes if they exist)

## Risk Assessment

**Low risk:**
- Maintains same function signature and interface
- Keeps 30% exploration budget for diversity
- Uses numpy which is already imported
- No new dependencies

**Potential issues:**
- If all scores are similar, weighted sampling approaches uniform (graceful degradation)
- Requires at least some history (but first round is still random, so safe)
