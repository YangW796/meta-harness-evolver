# Evolution Proposal Reasoning

## What Changed
Implemented a hybrid exploration-exploitation selection policy in `model.py` to replace the stub `pass` implementation.

## Key Features of the Implementation
1. **Adaptive Exploration-Exploitation Balance**: 
   - Starts with 80% exploration in early rounds
   - Gradually shifts to 70% exploitation in later rounds (minimum 30% exploration)
   - Formula: `exploration_ratio = max(0.3, 0.8 - 0.15 * num_rounds)`

2. **Random Exploration**: Uses `random.sample()` for unbiased exploration of the candidate space.

3. **Score-Based Exploitation**: 
   - Ranks historical candidates by their scores
   - Uses top performers to guide selection
   - Maintains diversity through weighted sampling across the candidate space

4. **Diversity Maintenance**: 
   - Uses weighted sampling to avoid clustering
   - Ensures coverage across different regions of the candidate list

## Why This Is Better
- **Baseline Establishment**: The previous implementation was a stub that selected nothing. This provides a functional baseline.
- **Balanced Strategy**: The adaptive ratio ensures we don't get stuck in local optima early while still capitalizing on discoveries later.
- **Practical for Biology Context**: Given the limited query budget (640 total queries), this strategy maximizes the chance of finding hits without over-optimizing prematurely.
- **Robust to Small History**: Works even with empty or small history by falling back to pure exploration.

## Expected Impact
- Should significantly improve from the baseline (which effectively scores 0)
- Expected to find some high-scoring perturbations through the exploitation mechanism
- The exploration component should provide decent coverage of the search space
- This serves as a strong foundation for future evolution iterations to build upon

## Future Improvement Directions
Once we have evaluation results, we can:
1. Tune the exploration decay rate
2. Incorporate gene similarity search if available
3. Add more sophisticated exploitation strategies (e.g., UCB, Thompson sampling)
4. Implement pair-specific strategies for gene pair datasets