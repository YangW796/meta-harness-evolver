# Evolution Proposal - Candidate 4

## What Changed

Added a **gene family clustering bonus** to the UCB selection algorithm. The model now:

1. **Extracts gene family prefixes** from gene names (e.g., "ZNF" from "ZNF123", "ATP" from "ATP6V0D1")
2. **Calculates average absolute scores** per family based on historical observations
3. **Adds a family bonus** (0.3 × family_avg_abs) to the UCB score for genes from families with extreme historical effects

## Why This Change

**Key Observation:** Analysis of the top 15 hit genes revealed:
- ZNHIT2 (abs=1.360)
- ATP6V0D1 (abs=0.975)
- ZNF76 (abs=0.610)
- ZNF785 (abs=0.576)
- ZNG1A (abs=0.566)
- ZNF619 (abs=0.462)
- ZNF804A (abs=0.431)
- ZNF697 (abs=0.390)
- ZNF713 (abs=0.381)
- ZNG1C (abs=0.380)
- ZNF615 (abs=0.370)
- ZNF671 (abs=0.362)

**Pattern:** 8 out of 15 top hits (53%) are ZNF (Zinc Finger) genes, and 2 are ZNG genes. This strong clustering suggests that:
- Genes from the same family may have similar functional effects
- Family-level signals can guide exploration more efficiently than pure UCB

## Expected Impact

**Hypothesis:** By adding a family bonus, the algorithm will:
1. **Prioritize exploration of promising gene families** (like ZNF, ZNG, ATP families)
2. **Improve hit rate** by exploiting the biological clustering pattern
3. **Maintain exploration** through the existing UCB mechanism
4. **Achieve better scores** than the current best (27.77)

**Conservative Tuning:** The family bonus weight (0.3) is moderate to avoid overfitting to the observed pattern while still providing meaningful guidance.

## Why This Is Better Than Prior Attempts

- **Candidate 1 → 2:** Added `abs()` to handle extreme effects in both directions (fundamental improvement)
- **Candidate 2 → 3:** Tuned exploration constant (2.0 → 2.5) and added regularization (incremental improvement)
- **Candidate 3 → 4:** Leverages biological signal through family clustering (novel, data-driven improvement)

This change goes beyond pure algorithmic tuning to exploit domain-specific patterns observed in the data.
