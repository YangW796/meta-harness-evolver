# Proposer Reasoning: Candidate 1

## What Changed
Replaced the placeholder `pass` statement in `model.py` with a functional selection policy based on the Upper Confidence Bound (UCB) algorithm.

## Implementation Details
The new policy implements:
1. **Random initialization**: For the first round with no history, selects candidates randomly to ensure broad initial exploration.
2. **UCB algorithm**: For subsequent rounds, balances:
   - **Exploitation**: Prioritizes candidates with high mean scores from history
   - **Exploration**: Adds an uncertainty bonus to candidates with few observations
3. **Fallback strategy**: Ensures the batch size is always met by filling with random unexplored candidates if needed

## Why This Is Better
- **Theoretical foundation**: UCB is a proven algorithm for multi-armed bandit problems, which matches the perturbation search task structure
- **Balanced approach**: Naturally balances exploring new candidates vs. exploiting known high-scorers
- **Adaptive**: Learns from history and adjusts selection strategy over rounds
- **Robust**: Handles edge cases (no history, insufficient candidates) gracefully

## Expected Impact
This should significantly improve over the baseline (which does nothing) by:
- Increasing cumulative hits through intelligent candidate selection
- Improving normalized cumulative gain by prioritizing high-value perturbations
- Making efficient use of the limited query budget (5 rounds × 128 per round)

This is a foundational implementation that can be built upon in future iterations.