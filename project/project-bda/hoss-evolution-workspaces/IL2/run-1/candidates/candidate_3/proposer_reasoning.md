# Proposer Reasoning — candidate_3

## What Changed
Modified the exploitation strategy in `model.py` to be more focused. Previously, when using gene search to find similar genes to high performers, ALL similar gene indices were added to the exploit pool. Now, only the top 50% (higher-ranked by the gene search) are kept.

**Specific change:** In the gene search loop (line ~107), changed from:
```python
exploit_pool.extend(similar_available)
```
to:
```python
keep_count = max(1, len(similar_available) // 2)
exploit_pool.extend(similar_available[:keep_count])
```

## Why This Change
**Evidence from history:**
- Candidate 1: 2 hits (round 1 only), score 10.95
- Candidate 2: 8 hits (2 in round 1 + 6 in round 2), score 14.83

The key improvement in candidate 2 was increasing the hit weight (2.0→10.0) and prioritizing hit genes in gene search with k=10. This successfully found 6 more hits in round 2.

**Hypothesis:** While adding more similar genes (k=10 vs k=5) helped, it may also dilute the exploit pool with lower-quality candidates. The gene search returns results ranked by similarity, so the first results are more promising.

**Goal:** Maintain the benefits of broader search while focusing exploitation on the most promising similar genes, improving hit precision.

## Expected Impact
- **Conservative improvement:** This is a low-risk refinement, not a major architectural change
- **Quality over quantity:** By keeping only top 50% of similar genes, the exploit pool should have higher average quality
- **Better hit rate:** With a more focused exploit pool, the 70% exploitation budget should yield more hits
- **Maintains exploration:** The 30% exploration budget is unchanged, preserving diversity

## Why Better Than Prior Attempts
- Candidate 2's strength was gene search; this refines it rather than replacing it
- Addresses potential dilution from k=10 while keeping its benefits
- Follows "Exploit Mode" guidance: conservative, calibration-focused improvement
- Builds on what works (hit prioritization) while improving signal-to-noise