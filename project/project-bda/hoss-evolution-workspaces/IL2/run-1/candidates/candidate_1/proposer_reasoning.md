# Evolution Proposal Reasoning

## What Changed
Implemented a complete selection policy in `model.py` that replaces the placeholder `pass` statement. The policy uses a hybrid exploration-exploitation strategy:

1. **Round 1 (No History)**: Pure random exploration from all available candidates
2. **Subsequent Rounds**: 70% exploitation, 30% exploration
   - **Exploitation**: Selects top 20% performers from history and uses gene search (if available) to find similar genes
   - **Exploration**: Random sampling from remaining candidates
3. **Gene Search Integration**: Attempts to import and use `bda_tools.gene_search()` to find similar genes to top performers

## Why This Change
The original implementation was a stub that did nothing. For a perturbation search task, we need an active learning approach that:
- Learns from historical outcomes (scores and hits)
- Balances exploring new candidates vs. exploiting known good candidates
- Leverages biological similarity when available through the Achilles gene search tool

## Expected Impact
This should significantly improve performance because:
1. **Baseline Functionality**: Moves from no selection logic to a working policy
2. **Adaptive Learning**: Uses historical data to guide future selections
3. **Biological Relevance**: When gene search is available, exploits the insight that similar genes may have similar effects
4. **Robustness**: Handles edge cases (empty history, insufficient candidates) gracefully

The 70/30 split balances the need to exploit known high-scoring regions while maintaining exploration to discover new hits.