# Proposer Reasoning — candidate_3

## What Changed
Modified the score-based boosting logic in `model.py` (lines 88-96) to also aggressively pursue genes with strongly negative scores, not just penalize them.

**Specific change:**
- Changed `elif avg_score < -0.1:` penalty to `elif avg_score < -0.2:` boost
- Changed `sampled_prob *= (1.0 + avg_score)` (which reduces probability) to `sampled_prob *= (1.0 + abs(avg_score))` (which increases probability)

## Why This Change
Analysis of the best run (candidate_2, score 15.17) revealed:
- 10 total hits found across 2 rounds
- 2 hits had **negative scores**: `SLC15A1` (-0.332) and `SIN3B` (-0.416)
- The previous logic **penalized** negative scores, making it harder to find negative-score hits
- The hit definition captures extreme scores in **both directions** (positive and negative)

The original logic treated all negative scores as "bad" and reduced their selection probability. However, in this task, extreme negative scores are just as valuable as extreme positive scores.

## Expected Impact
- **Better exploration of negative-score space**: Genes with strongly negative average scores (avg_score < -0.2) will now be boosted instead of penalized
- **More hits found**: Should discover additional hits that have negative effects on IL-2 production
- **Improved final score**: By pursuing both positive and negative extremes more aggressively

This is a **conservative, targeted improvement** that:
- Maintains the existing Thompson Sampling framework
- Preserves the positive score boosting (avg_score > 0.1)
- Only changes behavior for strongly negative scores
- Uses a slightly more conservative threshold (-0.2 vs -0.1) to focus on truly extreme negative scores

## Risk Assessment
**Low risk**: The change only affects genes with very negative scores (< -0.2), which were previously being actively avoided. This is pure upside for this task where extreme negatives are hits.