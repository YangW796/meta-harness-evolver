# Evolution Proposal: Candidate 2

## What Changed

Modified `model.py` to enhance the gene search strategy by adding **proactive diverse exploration** when no hits have been found yet.

**Specific Change**: Extended the gene search logic to work in two modes:
1. **Exploitation Mode** (when hits exist): Uses `bda_tools.gene_search(..., diverse=False)` to find similar genes to known hits (existing behavior)
2. **Exploration Mode** (when NO hits exist): Uses `bda_tools.gene_search(..., diverse=True)` to explore diverse genes from different families, using a random starting gene from history

The exploration mode allocates up to 40% of the batch to diverse gene search, compared to 30% for exploitation mode, reflecting the need for broader exploration early on.

## Why This Change

**Analysis of Candidate 1**:
- Found 2 hits (AARS1: -0.400, ABCB7: -0.505) out of 128 queries
- Hit rate: 1.56%, final_score: 10.53
- Both hits belong to specific gene families (AARS: aminoacyl-tRNA synthetases, ABCB: ATP-binding cassette transporters)
- The current strategy only uses gene search AFTER finding hits, missing opportunities for proactive exploration

**Hypothesis**:
Gene families may cluster in the feature space used by Achilles gene search. By using **diverse** gene search even before finding hits, we can:
1. Explore multiple gene families simultaneously
2. Increase the probability of stumbling upon hit-rich regions
3. Balance exploration better than pure Thompson Sampling alone

This is particularly valuable in the early rounds when the history is small and Thompson Sampling has limited signal.

## Expected Impact

**Conservative Improvement**: This is a low-risk change that:
- Maintains all existing logic (Thompson Sampling still handles the majority of selection)
- Only adds a new exploration pathway when gene search is available
- Preserves the exploitation behavior when hits are found
- Increases batch diversity early in the search process

**Expected Outcome**:
- Higher hit discovery rate in early rounds
- Better coverage of the gene family search space
- Improved final_score through better exploration-exploitation balance
- Potential to discover hit-rich gene families that pure random/Thompson Sampling might miss

The change is minimal (adds ~30 lines) and maintains backward compatibility with the existing Thompson Sampling fallback.
