# Evolution Proposal - Candidate 4

## What Changed

Modified the gene search quality filtering logic in `model.py` (lines 110-113) to be **adaptive** based on the observed hit rate:

- **Before**: Fixed 50% cutoff - always kept the top half of similar genes from search results
- **After**: Dynamic threshold ranging from 30% (high hit rate) to 80% (low hit rate)

The adaptive logic:
- If hit rate ≥ 10%: keep only top 30% (high selectivity, we're in a good region)
- If hit rate < 10%: keep 30% to 80% based on how low the hit rate is (more exploration needed)

## Why This Change

**Historical Pattern Analysis:**
- Candidate 1 → 2: Increased hit weight (2→10) and search breadth (k=5→10) → Score: 10.95 → 14.83
- Candidate 2 → 3: Added 50% quality filtering → Score: 14.83 → 16.48 ✓ Best

The 50% filtering in candidate_3 improved quality but may be too aggressive. Looking at the metrics:
- Round 1 precision: 1.6% (2 hits/128)
- Round 2 precision: 4.7% (6 hits/128) 
- Round 3 precision: 1.6% (2 hits/128)

The drop in round 3 suggests we might be over-filtering and missing opportunities.

**Hypothesis:**
When we have many hits (like after round 2 with 8 cumulative hits), we're in a productive region and should be **highly selective** (30% cutoff) to focus on the best candidates. When we have few hits, we need **broader exploration** (up to 80% cutoff) to discover new promising regions.

## Expected Impact

**Conservative Improvement:**
- Better adaptation to search space characteristics
- More exploration when needed (low hit rate)
- Higher selectivity when warranted (high hit rate)
- Should improve discovery of new hit genes while maintaining quality

**Risk:** Low - This is a calibration change, not a structural rewrite. The 70/30 exploit/explore balance and hit prioritization remain unchanged.

## Why Better Than Prior Attempts

- Candidate 3's fixed 50% was an improvement but one-size-fits-all
- This change adds **adaptivity** - the policy now responds to its own performance
- Small, targeted modification in the "exploit mode" spirit
- Builds on the proven success of quality filtering while addressing its rigidity