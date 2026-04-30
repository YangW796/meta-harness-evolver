# Proposer Reasoning: Candidate 1

## What Changed
Replaced the placeholder `select()` function in `model.py` with a working implementation using a hybrid exploration-exploitation strategy with adaptive sampling.

## Key Features of the Implementation

1. **Adaptive Exploration-Exploitation Balance**: 
   - Early rounds: 90% exploration, 10% exploitation
   - Later rounds: 20% exploration, 80% exploitation
   - Ratio adjusts automatically based on the number of completed rounds

2. **Exploration Component**:
   - Pure random sampling from unselected candidates
   - Ensures broad coverage of the search space initially

3. **Exploitation Component**:
   - Identifies top-performing candidates from history (top 20% or minimum 10)
   - Attempts to use gene search (`bda_tools.gene_search`) when available to find similar candidates
   - Falls back to stratified sampling for diversity when gene search is unavailable
   - Uses bucket-based sampling to maintain diversity across the candidate space

4. **Robustness**:
   - Handles edge cases (empty history, insufficient available candidates)
   - Graceful degradation when optional tools (bda_tools) are unavailable
   - Ensures exactly `batch_size` candidates are returned

## Expected Impact

This implementation should significantly improve performance over the placeholder because:

1. **Early Discovery**: High exploration in early rounds helps discover promising regions of the search space quickly
2. **Progressive Refinement**: Increasing exploitation in later rounds focuses on high-performing areas
3. **Diversity Maintenance**: Stratified sampling prevents premature convergence to local optima
4. **Biological Relevance**: When available, gene search leverages biological similarity to find related high-performing candidates

## Why This Is Better Than Prior Attempts

This is the first candidate, so the baseline is a non-functional placeholder. The implementation follows best practices from:
- Multi-armed bandit algorithms (adaptive exploration-exploitation)
- Active learning strategies (balancing exploration and exploitation)
- Biological perturbation screening (leveraging gene similarity when available)

The strategy is designed to be robust across different dataset types (single-gene and gene-pair) and works efficiently even with limited historical data.