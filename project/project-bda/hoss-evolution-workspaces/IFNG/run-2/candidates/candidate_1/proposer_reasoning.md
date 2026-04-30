# Evolution Proposal Reasoning

## What Changed
Implemented an improved Thompson Sampling selection policy with adaptive exploration and hit-based exploitation. The key improvements over the baseline stub implementation are:

1. **Thompson Sampling Core**: Uses Beta distribution to balance exploration-exploitation, modeling the probability of finding hits (genes with very negative scores).

2. **Gene Search Integration**: When hits are discovered, the policy attempts to use the `bda_tools.gene_search()` function to find similar genes, dedicating up to 30% of the batch to exploring these biologically similar candidates.

3. **Hit-Based Exploitation**: Prioritizes exploration around confirmed hits, leveraging the assumption that functionally related genes may have similar perturbation effects.

4. **Optimistic Exploration**: Unexplored candidates receive an optimistic prior (alpha=4, beta=1) to encourage exploration while biasing toward potential hits.

## Why This Approach
Analysis of run-1 evolution history showed:
- The Thompson Sampling approach (candidate_5) achieved the best score: **20.12 final_score with 12 hits**
- UCB-based approaches (candidate_2) performed worse: **14.33 final_score with 3 hits**
- The baseline stub implementation scores 0

Thompson Sampling is particularly well-suited for this problem because:
- It naturally balances exploring uncertain candidates vs. exploiting known good ones
- The Beta distribution models the probability of "success" (finding a hit) effectively
- It handles the small-data regime well (only 5 rounds × 128 queries = 640 total)

## Expected Impact
This implementation should significantly improve upon the baseline (which currently returns no selections). Based on run-1 results, I expect:

- **Final score**: ~15-25 (compared to baseline 0)
- **Total hits**: ~8-15 hits discovered
- **NCG improvement**: Better ranking of hits early in the search process

The gene search integration provides an additional boost by leveraging biological similarity, which should help discover hit clusters more efficiently than random exploration alone.

## Why Better Than Prior Attempts
This implementation refines the successful Thompson Sampling approach from run-1 by:
1. Adding gene search capability for more intelligent exploration
2. Using a slightly more optimistic prior (alpha=4 vs alpha=3) to encourage exploration
3. Better code organization with helper functions for maintainability
4. Robust error handling when gene search is unavailable

The approach maintains the proven Thompson Sampling core while adding biological domain knowledge through the gene similarity search.