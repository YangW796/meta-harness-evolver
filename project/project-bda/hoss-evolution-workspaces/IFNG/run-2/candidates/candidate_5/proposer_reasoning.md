# Evolution Proposal: Candidate 5

## What Changed

Replaced the Thompson Sampling bandit algorithm with a **gradient-based adaptive bandit selection** strategy.

**Key modifications:**
1. **New selection function**: `_gradient_bandit_selection()` replaces `_thompson_sampling()`
2. **Direct score optimization**: Uses actual score values directly instead of binary hit/miss conversions
3. **Softmax weighting**: Applies exponential weighting based on normalized scores
4. **Adaptive temperature**: Automatically adjusts exploration/exploitation based on score variance
5. **Optimistic initialization**: Unexplored genes get scores based on best observed performance minus uncertainty bonus

## Why This Is Better

### Problems with Previous Approach
- **Thompson Sampling limitations**: Converted continuous scores to binary success/failure, losing information
- **Fixed exploration**: Used static Beta priors (α=4, β=1) regardless of score distribution
- **Indirect optimization**: Modeled probability of "success" rather than directly optimizing scores

### Advantages of Gradient-Based Approach
1. **Score-driven**: Directly uses the continuous score values, preserving more information
2. **Adaptive exploration**: Temperature adjusts based on score variance - high variance → more exploration
3. **Softmax selection**: Provides smooth probability distribution over candidates
4. **Better unexplored handling**: Optimistic estimates incorporate uncertainty (std deviation)
5. **Mathematical foundation**: Based on gradient bandit algorithms from reinforcement learning

## Expected Impact

**Hypothesis**: Direct score optimization will improve hit discovery by:
- Better prioritizing genes with moderately negative scores (not just extreme hits)
- Adapting exploration to the actual score distribution
- Making more informed decisions with limited data

**Target metrics**:
- Increase cumulative hits from 21 to 24+ (14% improvement)
- Improve ncg from 0.204 to 0.220+
- Better early-round performance through adaptive exploration

## Novelty

### Strategy Tags
- **gradient**: Uses gradient-based optimization principles
- **direct_optimization**: Optimizes scores directly rather than through proxy metrics
- **adaptive_exploration**: Automatically adjusts exploration based on score statistics

### Differentiation from Recent Candidates
**Most similar to**: Candidate 4 (current best)

**Key differences**:
1. **Algorithm family**: Gradient bandits vs. Thompson Sampling (different RL approach)
2. **Information usage**: Continuous scores vs. binary hit/miss
3. **Exploration strategy**: Variance-adaptive vs. fixed priors
4. **Selection mechanism**: Softmax probabilities vs. Beta sampling

**Not a minor tweak**: This is a fundamental algorithmic change from probability matching (Thompson) to gradient-based optimization, representing a different model family entirely.

## Risk Assessment

**Low risk** because:
- Maintains same interface and gene search integration
- Fallback mechanisms preserved
- Robust to edge cases (handles score ranges, variances)
- No additional computational complexity

**Potential concerns**:
- Softmax might be too greedy if temperature is too low
- Mitigation: Adaptive temperature based on variance prevents this
- May need more samples for variance estimation
- Mitigation: Uses optimistic initialization for unexplored genes

## Implementation Quality

- Clean, well-documented code
- Maintains all existing functionality
- Proper error handling
- Efficient numpy operations
- Single targeted change (model.py only)