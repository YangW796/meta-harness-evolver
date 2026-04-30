# Evolution Proposal: Candidate 2

## What Changed

Modified `model.py` to replace the Beta-Bernoulli Thompson Sampling (based on binary hits) with a Gaussian-Gamma Thompson Sampling approach that models continuous scores directly.

**Key changes:**
1. **Continuous Score Modeling**: Instead of using binary hit observations (0 or 1), the new approach models the actual continuous scores using a Gaussian-Gamma conjugate prior model.
2. **Posterior Updates**: The algorithm now maintains posterior distributions over candidate scores, updating both cluster-level and candidate-level beliefs as observations arrive.
3. **Sampling Strategy**: Samples from the posterior predictive distribution (Student-t) to balance exploration vs exploitation based on the full score distribution, not just hit frequency.

## Why This Is Better

**Problem with previous approach:**
- The Beta-Bernoulli model only used binary hit information, discarding valuable continuous score magnitude data
- With only 5 hits in 128 queries, the algorithm had very sparse feedback, making it hard to distinguish between moderately good and very good candidates
- Candidates with scores like -1.6 (not a hit) were treated the same as candidates with scores near 0

**Benefits of new approach:**
1. **Better Exploitation**: Can distinguish between candidates with scores of -4.9 vs -2.5 vs -1.0, prioritizing the most extreme negative scores
2. **More Efficient Exploration**: Uncertainty estimates are based on score variance, allowing targeted exploration of promising regions
3. **Adaptive to Task**: The task rewards finding extreme negative scores (decreasing tau protein), and continuous modeling directly optimizes for this
4. **Empirical Bayes**: Uses global score statistics to inform cluster priors, sharing information across similar genes

## Expected Impact

- **Higher Hit Rate**: By prioritizing candidates with more extreme negative sampled scores, should find more hits per batch
- **Improved NCG**: Better ranking of candidates should improve normalized cumulative gain
- **Conservative Change**: Maintains the same clustering structure and overall Thompson Sampling framework, just replaces the observation model

## Risk Assessment

**Low Risk:**
- The change is algorithmic but maintains the same function signature and overall structure
- Falls back gracefully when no history exists (same random exploration)
- Uses well-established Bayesian methods (Gaussian-Gamma conjugate prior)
- No new dependencies or complex logic added

**Potential Issues:**
- Numerical stability with variance calculations (handled with defaults)
- May be slightly more computationally intensive, but still within acceptable bounds for the problem size