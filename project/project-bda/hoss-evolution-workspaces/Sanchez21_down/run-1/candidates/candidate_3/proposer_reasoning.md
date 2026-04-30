# Evolution Proposal - Candidate 3

## What Changed

Modified the Bayesian update in `model.py` (lines 214-219) to use a more conservative prior weight when updating candidate posteriors from single observations.

**Specific change**: Instead of using `cluster_post['lambda_n']` directly as the prior weight, we now use `max(cluster_post['lambda_n'], 2.0)` to ensure at least 2 pseudo-observations worth of prior strength.

## Why This Change

**Context from evolution history**:
- Candidate 1: Used Beta distributions for binary hits → Score 16.83
- Candidate 2: Switched to Gaussian-Gamma for continuous scores → Score 20.32 (BEST)

The switch from binary to continuous modeling was highly successful, doubling the hit rate. However, analyzing the Bayesian update logic reveals a potential instability:

When a candidate has only been observed once, the current update adds a full observation's worth of precision (`+ 1` to lambda_n). If the cluster itself has limited data (low `lambda_n`), this single observation can dominate the posterior, leading to overconfident predictions.

**The problem**: With limited history, clusters may have weak priors (low `lambda_n` close to 1.0). A single observation then gets equal or greater weight than the entire cluster prior, causing overfitting to potentially noisy individual measurements.

## Expected Impact

**Conservative improvement**: By enforcing a minimum prior weight of 2.0 pseudo-observations, we:
1. **Stabilize early-round selections**: When history is small, the prior maintains reasonable influence
2. **Reduce overfitting**: Single outliers have less ability to drastically shift the posterior mean
3. **Maintain exploration**: Weaker updates preserve uncertainty, encouraging continued exploration of promising clusters

**Risk profile**: This is a low-risk, conservative change. It doesn't alter the core algorithm (Gaussian-Gamma Thompson Sampling), only tunes the Bayesian update to be more robust with limited data. The change is minimal (6 lines) and maintains backward compatibility.

**Success criteria**: We expect modest improvement (1-3% score increase) through better stability in early rounds, leading to more consistent hit discovery across all rounds rather than overcommitting to potentially lucky first-round hits.

## Why Better Than Prior Attempts

- Candidate 2's success came from better utilizing score information (continuous vs binary)
- This proposal builds on that success by improving the statistical stability of the continuous model
- It addresses a specific weakness (overfitting to limited data) without changing the winning strategy
- In "exploit mode" (recent best updated), this is the right kind of conservative, targeted improvement