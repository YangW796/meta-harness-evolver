# Proposer Reasoning - Candidate 1

## What Changed
Implemented a complete selection policy using the Upper Confidence Bound (UCB) algorithm to replace the empty `pass` implementation.

## Why This Change
The current model implementation was a stub with no functionality (`pass` statement). For the first candidate, I needed to implement a basic but effective selection strategy that:
1. Balances exploration (trying new genes) and exploitation (selecting known high-scoring genes)
2. Handles the cold-start problem when no history exists
3. Uses the available score information from history to make informed decisions

## Expected Impact
The UCB algorithm is theoretically well-founded for multi-armed bandit problems, which closely matches the perturbation search task:
- **Exploitation**: Selects genes with high average scores from history
- **Exploration**: Gives bonus to genes that haven't been explored much
- **Optimism under uncertainty**: Unexplored genes get optimistic initial scores based on the maximum observed score

This should perform significantly better than random selection while remaining computationally efficient and robust even with limited history.

## Why Better Than Prior Attempts
This is the first candidate, so there are no prior attempts to compare against. However, UCB is a strong baseline for active search/bandit problems and should provide a solid foundation for future evolution iterations to build upon.