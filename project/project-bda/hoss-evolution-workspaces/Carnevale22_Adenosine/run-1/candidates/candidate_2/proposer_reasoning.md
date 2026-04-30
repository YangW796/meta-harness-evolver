# Proposer Reasoning - Candidate 2

## What Changed
Modified the exploitation strategy in `model.py` to use score-based proximity weighting instead of position-based diversity weighting. Specifically:

1. **Score Interpretation**: Changed sorting from descending (higher is better) to ascending (lower/negative is better) to match the task objective (negative scores boost T cell proliferation).

2. **Exploitation Logic**: Replaced the position-based weighted sampling (which used `np.linspace` to create diversity) with a proximity-based approach that weights candidates by their distance to top performers in the candidate index space.

3. **Weighting Formula**: Candidates closer to known top performers receive higher weights: `weight = 1.0 / (1.0 + min_dist / 100.0)`

## Why This Is Better
The previous strategy used position-based weights that promoted diversity but didn't effectively exploit the knowledge gained from observed scores. The key insights from candidate_1's results:

- **Hits have strongly negative scores**: ARMH4 (-0.474) and HLA-DPA1 (-0.344)
- **Task rewards negative scores**: The goal is to find genes that boost T cell proliferation
- **Candidate space has locality**: Genes with similar indices may have related functions or be clustered in the dataset

The new strategy directly uses the observed scores to guide exploration toward promising regions of the search space, increasing the likelihood of finding more hits in subsequent rounds.

## Expected Impact
- **Higher hit rate**: By biasing selection toward regions near known good performers, we should find more hits per batch
- **Better ncg score**: More hits earlier in the selection process improves normalized cumulative gain
- **Conservative improvement**: This is a targeted change that maintains the exploration-exploitation balance while making exploitation more intelligent

This is a low-risk, high-reward modification that directly addresses the weakness in the previous exploitation strategy.