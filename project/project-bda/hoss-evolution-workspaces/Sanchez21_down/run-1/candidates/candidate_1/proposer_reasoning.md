# Proposer Reasoning - Candidate 1

## What Changed

**Targeted Edit**: Enhanced the Thompson Sampling with Gene Cluster Priors model by improving the fallback clustering strategy when gene search (bda_tools.gene_search) is unavailable.

**Specific Change**: In the `except ImportError` block (lines 119-135), instead of creating singleton clusters for all genes, I implemented gene family prefix clustering:
- Extract the alphabetic prefix from gene names (e.g., "ZNF" from "ZNF823", "TNF" from "TNFRSF")
- Group genes with the same 2-4 character prefix into family clusters
- This captures biological gene families that often share similar functions

## Why This Change

**Problem Identified**: The original Thompson Sampling implementation (from Sanchez21/candidate_5) relied heavily on the Achilles gene search tool for clustering. When this tool is unavailable (ImportError), it falls back to singleton clusters where each gene is its own cluster, losing all information sharing benefits.

**Hypothesis**: Gene families (indicated by name prefixes like ZNF, ZSCAN, TNF, IL, etc.) often share biological functions and perturbation effects. By clustering based on name prefixes, we can maintain Bayesian information sharing even without the gene search tool, leading to better exploration-exploitation balance.

**Expected Impact**:
1. **Better performance when gene search is disabled**: The enhanced fallback maintains cluster-based information sharing
2. **More biologically informed exploration**: Gene families often have correlated effects
3. **Robustness**: Works well regardless of whether Achilles dataset is available
4. **Low risk**: Only affects the fallback path; when gene search is available, behavior is identical to the proven candidate_5

## Why This Is Better Than Prior Attempts

The Sanchez21 evolution showed:
- **Candidate 4**: Hybrid exploration-exploitation with adaptive ratios (score: 26.9)
- **Candidate 5**: Thompson Sampling with Gene Cluster Priors using gene search (score: 28.3)

Candidate 5's Thompson Sampling was clearly superior, but it had a weakness: dependency on gene search. This change addresses that weakness while preserving the core Bayesian inference approach that made candidate_5 successful.

The prefix clustering is a simple yet biologically meaningful heuristic that should provide similar benefits to gene search clustering when the tool is unavailable.