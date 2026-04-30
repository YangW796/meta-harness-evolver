# Change Record — candidate_1

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IFNG/run-2/best/current/harness
Generated at: 2026-04-30T07:10:41.706303

## Files Changed

- model.py: modified (added=150, deleted=8, delta=142)
- outputs/metrics.json: new (added=2233, deleted=0, delta=2233)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -1,12 +1,14 @@
 from __future__ import annotations
+import random
+import numpy as np
 
 def select(candidates, history, batch_size, seed) -> list[int]:
     """
     Selection policy for Project-BDA.
-
+    
     Contract (MUST KEEP EXACTLY):
         select(candidates, history, batch_size, seed) -> list[int]
-
+    
     Inputs:
     - candidates: list[dict]
         - single-gene datasets: each item includes {"gene": "<HGNC>"}
@@ -21,12 +23,152 @@
           - hit: int (0/1) if enabled by runner
     - batch_size: int
     - seed: int
-
+    
     Output:
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
+    
+    Strategy: Improved Thompson Sampling with adaptive exploration and hit-based exploitation.
+    """
+    rng = random.Random(seed)
+    np.random.seed(seed)
+    
+    # Get all candidate indices
+    all_indices = list(range(len(candidates)))
+    
+    # Get already selected indices
+    selected_indices = {h['candidate_index'] for h in history}
+    
+    # Get available indices (not yet selected)
+    available_indices = [i for i in all_indices if i not in selected_indices]
+    
+    # If no history, use random selection
+    if not history:
+        selected = available_indices[:batch_size]
+        rng.shuffle(selected)
+        return selected[:batch_size]
+    
+    # Separate hits from non-hits for better modeling
+    hit_indices = [h['candidate_index'] for h in history if h.get('hit', 0) == 1]
+    hit_scores = [h['score'] for h in history if h.get('hit', 0) == 1]
+    
+    # If we have hits, prioritize exploring similar genes
+    if hit_indices and len(hit_indices) > 0:
+        # Try to use gene search if available
+        try:
+            import bda_tools
+            
+            # Find the best hit (most negative score)
+            best_hit_idx = hit_indices[np.argmin(hit_scores)]
+            best_hit_gene = candidates[best_hit_idx].get('gene')
+            
+            if best_hit_gene:
+                # Search for similar genes
+                similar_indices = bda_tools.gene_search(best_hit_gene, k=20, diverse=False)
+                
+                # Filter to available indices only
+                similar_available = [idx for idx in similar_indices if idx in available_indices]
+                
+                # If we found similar genes, include some in the selection
+                if similar_available:
+                    # Take up to 30% of batch from similar genes
+                    num_similar = min(len(similar_available), batch_size // 3)
+                    selected = similar_available[:num_similar]
+                    remaining_batch = batch_size - len(selected)
+                    
+                    # Fill the rest using Thompson Sampling
+                    if remaining_batch > 0:
+                        thompson_selected = _thompson_sampling(
+                            candidates, history, available_indices, 
+                            selected, remaining_batch, rng
+                        )
+                        selected.extend(thompson_selected)
+                    
+                    rng.shuffle(selected)
+                    return selected[:batch_size]
+        except ImportError:
+            # Gene search not available, fall back to pure Thompson Sampling
+            pass
+        except Exception:
+            # Gene search failed, fall back to pure Thompson Sampling
+            pass
+    
+    # Use pure Thompson Sampling
+    selected = _thompson_sampling(candidates, history, available_indices, [], batch_size, rng)
+    rng.shuffle(selected)
+    return selected[:batch_size]
 
-    You may implement any suitable algorithmic model here, including but not limited to:
-    traditional algorithms, machine learning models, deep learning models, biological models,
-    and mathematical models.
-    """
-    pass
+
+def _thompson_sampling(candidates, history, available_indices, exclude_indices, batch_size, rng):
+    """Helper function for Thompson Sampling with Beta distribution."""
+    
+    # Filter out excluded indices
+    available = [idx for idx in available_indices if idx not in exclude_indices]
+    
+    if len(available) <= batch_size:
+        return available[:batch_size]
+    
+    # Normalize scores to [0, 1] for Beta distribution
+    # Hits have negative scores around -0.4 to -0.5, we want these to have low normalized scores
+    all_scores = [h['score'] for h in history]
+    min_score = min(all_scores)
+    max_score = max(all_scores)
+    score_range = max_score - min_score
+    
+    # Build success/failure counts for each candidate
+    # For Thompson Sampling with Beta distribution, we model the probability of "success"
+    # Here "success" means being a hit (having a very negative score)
+    candidate_successes = {}
+    candidate_failures = {}
+    
+    for h in history:
+        idx = h['candidate_index']
+        score = h['score']
+        
+        # Normalize score to [0, 1] where 0 is worst (most negative) and 1 is best
+        if score_range > 0:
+            normalized_score = (score - min_score) / score_range
+        else:
+            normalized_score = 0.5
+        
+        # For hits (very negative scores), normalized_score will be close to 0
+        # We define "success" as finding a hit, so we want to maximize (1 - normalized_score)
+        # The more negative the score, the higher the success probability
+        
+        if idx not in candidate_successes:
+            candidate_successes[idx] = 0
+            candidate_failures[idx] = 0
+        
+        # Accumulate successes and failures based on normalized score
+        # Use the complement since hits (what we want) have low normalized scores
+        success_weight = 1.0 - normalized_score
+        failure_weight = normalized_score
+        
+        # Add to counts (with some scaling to get reasonable Beta parameters)
+        candidate_successes[idx] += success_weight
+        candidate_failures[idx] += failure_weight
+    
+    # For Thompson Sampling, we sample from Beta(alpha, beta) for each candidate
+    # where alpha = successes + 1, beta = failures + 1 (add-1 smoothing for uninformed prior)
+    thompson_samples = []
+    
+    for idx in available:
+        if idx in candidate_successes:
+            # Explored candidate: use observed successes/failures
+            alpha = candidate_successes[idx] + 1
+            beta = candidate_failures[idx] + 1
+        else:
+            # Unexplored candidate: use optimistic prior
+            # Bias toward exploration of potentially good candidates (hits)
+            # Use alpha > beta to favor success (finding hits)
+            alpha = 4  # Slightly higher than before for more optimism
+            beta = 1
+        
+        # Sample from Beta distribution
+        sample = np.random.beta(alpha, beta)
+        thompson_samples.append((sample, idx))
+    
+    # Sort by Thompson sample (descending) and select top batch_size
+    thompson_samples.sort(reverse=True)
+    selected = [idx for _, idx in thompson_samples[:batch_size]]
+    
+    return selected
```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -0,0 +1,2233 @@
+{
+  "task": "perturb-genes-brief",
+  "data_name": "IFNG",
+  "measurement": "the log fold change in Interferon-gamma (IFNG) normalized read counts",
+  "task_prompt": {
+    "Task": "identify genes that regulate the production of Interferon-gamma (IFNG)",
+    "Measurement": "the log fold change in Interferon-gamma (IFNG) normalized read counts"
+  },
+  "metrics": {
+    "test": {
+      "pool_size": 18418,
+      "rounds": 1,
+      "executed_rounds": 1,
+      "batch_size": 128,
+      "seed": 42,
+      "baseline_total_queries": 0,
+      "baseline_total_hits": 0,
+      "delta_queries": 128,
+      "delta_hits": 2,
+      "total_queries": 128,
+      "total_hits": 2,
+      "top_k": 920,
+      "hit_curve": {
+        "queries": [
+          0,
+          128
+        ],
+        "hits": [
+          0,
+          2
+        ]
+      },
+      "auc": 128.0,
+      "auc_normalized": 0.0010869565217391304,
+      "ncg": 0.10533733408464835,
+      "round_details": [
+        {
+          "round": 0,
+          "selected_count": 128,
+          "hits": 2,
+          "cumulative_hits": 2,
+          "precision_at_batch": 0.015625,
+          "selected": [
+            "AADAC",
+            "ABHD5",
+            "ABLIM1",
+            "ABHD10",
+            "ABCB8",
+            "AAMDC",
+            "ABCD1",
+            "ABLIM2",
+            "ABLIM3",
+            "ABHD14B",
+            "ABCB6",
+            "AARS1",
+            "ABCA1",
+            "ACACB",
+            "ABCA12",
+            "ABCB9",
+            "ABCD2",
+            "ACADL",
+            "ABI2",
+            "AANAT",
+            "ABCG8",
+            "A2M",
+            "ABCE1",
+            "ABHD13",
+            "ABCA4",
+            "ABHD16B",
+            "AAAS",
+            "A1CF",
+            "ABHD17B",
+            "ABHD12B",
+            "AASS",
+            "ABL2",
+            "ABCC8",
+            "ABCG5",
+            "ABI1",
+            "ABCC6",
+            "ABCA7",
+            "ABCG4",
+            "ABCA2",
+            "ABCC1",
+            "ABCC9",
+            "ABCA6",
+            "ABT1",
+            "ABCA9",
+            "ABHD16A",
+            "ABHD12",
+            "ABCC3",
+            "ABCB1",
+            "ABL1",
+            "AARS2",
+            "ABCC10",
+            "ABCG1",
+            "AARSD1",
+            "ABI3",
+            "ABCA8",
+            "ABR",
+            "ACAD8",
+            "ABCF1",
+            "A4GNT",
+            "ABCC2",
+            "AAGAB",
+            "ABHD3",
+            "ABCD4",
+            "ABI3BP",
+            "ABRA",
+            "ACACA",
+            "AACS",
+            "AASDH",
+            "ABCB5",
+            "ABCA5",
+            "AADACL2",
+            "ABHD14A",
+            "AAK1",
+            "ABCF2",
+            "ABCC5",
+            "A4GALT",
+            "ABCA13",
+            "ABO",
+            "ABCB11",
+            "ABCB4",
+            "AADACL4",
+            "ABCB7",
+            "ABRAXAS1",
+            "ACAD10",
+            "ABHD17C",
+            "ABRACL",
+            "AAR2",
+            "ABHD6",
+            "ABCB10",
+            "ABTB1",
+            "ABITRAM",
+            "AARD",
+            "A1BG",
+            "ACADM",
+            "ABTB2",
+            "ABCC4",
+            "ACAD9",
+            "ABCC11",
+            "ACAA1",
+            "ABHD2",
+            "ABHD15",
+            "ABHD4",
+            "AASDHPPT",
+            "ABCG2",
+            "ABRAXAS2",
+            "ABHD11",
+            "ABCD3",
+            "ABAT",
+            "AATF",
+            "ACAA2",
+            "ACADSB",
+            "A3GALT2",
+            "ABCC12",
+            "ABHD1",
+            "AADACL3",
+            "ABCF3",
+            "ABTB3",
+            "ACAD11",
+            "ABHD17A",
+            "AADAT",
+            "ACADS",
+            "AAMP",
+            "ACADVL",
+            "ABCA10",
+            "ABCA3",
+            "ABHD8",
+            "A2ML1",
+            "AATK"
+          ],
+          "selected_scores": [
+            0.09700375,
+            -0.123051,
+            -0.095673,
+            -0.083665,
+            -0.009105,
+            0.01205,
+            -0.0909125,
+            -0.220065,
+            0.131625,
+            0.025335,
+            -0.042354,
+            -0.40020835,
+            0.1342295,
+            0.018345,
+            -0.108835,
+            0.21014065,
+            0.00524,
+            0.147555,
+            -0.22205,
+            0.14409,
+            -0.038225,
+            -0.18934,
+            0.359895,
+            0.022985,
+            -0.159105,
+            -0.002058,
+            0.130627,
+            0.129081,
+            0.23368,
+            -0.01068,
+            -0.085326,
+            0.11353,
+            0.051595,
+            0.103443,
+            0.0107805,
+            0.307105,
+            -0.01946,
+            0.25585085,
+            -0.2907179,
+            -0.165605,
+            0.19773,
+            -0.1365005,
+            0.0858425,
+            0.27268896,
+            -0.1640935,
+            0.1263665,
+            -0.0762865,
+            -0.266345,
+            0.0765485,
+            0.03688,
+            -0.1349245,
+            0.04291255,
+            -0.007871,
+            -0.1086473,
+            0.0039675,
+            0.339915,
+            0.02707,
+            -0.105515,
+            0.029995,
+            -0.1535965,
+            -0.31044,
+            0.071691,
+            -0.04102,
+            -0.12602566,
+            0.031534,
+            0.035085,
+            0.19899,
+            0.140285,
+            0.0766415,
+            0.09411,
+            0.180098,
+            -0.0982965,
+            -0.144225,
+            -0.1052725,
+            0.16644,
+            0.15113,
+            -0.01498,
+            0.016455,
+            0.09610045,
+            0.2502,
+            -0.165411,
+            -0.505255,
+            0.02837,
+            0.037576,
+            -0.0872855,
+            -0.0995285,
+            0.17943,
+            -0.01869,
+            -0.091724,
+            0.0953785,
+            0.18748,
+            0.0074185,
+            -0.161214,
+            -0.17399,
+            -0.15948,
+            0.07494,
+            0.0464,
+            -0.1653245,
+            0.27926,
+            -0.033632,
+            0.054218,
+            -0.015138,
+            0.0825805,
+            -0.000475,
+            -0.240335,
+            0.178475,
+            -0.367169,
+            -0.01351,
+            0.3854245,
+            -0.0323105,
+            0.0369245,
+            0.183225,
+            -0.09262565,
+            0.09580065,
+            -0.217905,
+            0.0637145,
+            0.33209,
+            0.184825,
+            -0.35325,
+            0.23516,
+            0.243119,
+            0.1659475,
+            0.0484775,
+            -0.00779,
+            0.20382,
+            -0.239638,
+            0.005275,
+            -0.027445
+          ],
+          "selected_hits": [
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            1,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            1,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0
+          ]
+        }
+      ],
+      "queried_records": [
+        {
+          "candidate_index": 9,
+          "gene": "AADAC",
+          "score": 0.09700375,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 92,
+          "gene": "ABHD5",
+          "score": -0.123051,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 102,
+          "gene": "ABLIM1",
+          "score": -0.095673,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 76,
+          "gene": "ABHD10",
+          "score": -0.083665,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 49,
+          "gene": "ABCB8",
+          "score": -0.009105,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16,
+          "gene": "AAMDC",
+          "score": 0.01205,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 62,
+          "gene": "ABCD1",
+          "score": -0.0909125,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 103,
+          "gene": "ABLIM2",
+          "score": -0.220065,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 104,
+          "gene": "ABLIM3",
+          "score": 0.131625,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 82,
+          "gene": "ABHD14B",
+          "score": 0.025335,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 47,
+          "gene": "ABCB6",
+          "score": -0.042354,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 21,
+          "gene": "AARS1",
+          "score": -0.40020835,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 30,
+          "gene": "ABCA1",
+          "score": 0.1342295,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 118,
+          "gene": "ACACB",
+          "score": 0.018345,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 32,
+          "gene": "ABCA12",
+          "score": -0.108835,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 50,
+          "gene": "ABCB9",
+          "score": 0.21014065,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 63,
+          "gene": "ABCD2",
+          "score": 0.00524,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 123,
+          "gene": "ACADL",
+          "score": 0.147555,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 96,
+          "gene": "ABI2",
+          "score": -0.22205,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18,
+          "gene": "AANAT",
+          "score": 0.14409,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 74,
+          "gene": "ABCG8",
+          "score": -0.038225,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2,
+          "gene": "A2M",
+          "score": -0.18934,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 66,
+          "gene": "ABCE1",
+          "score": 0.359895,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 80,
+          "gene": "ABHD13",
+          "score": 0.022985,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 36,
+          "gene": "ABCA4",
+          "score": -0.159105,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 85,
+          "gene": "ABHD16B",
+          "score": -0.002058,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7,
+          "gene": "AAAS",
+          "score": 0.130627,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1,
+          "gene": "A1CF",
+          "score": 0.129081,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 87,
+          "gene": "ABHD17B",
+          "score": 0.23368,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 79,
+          "gene": "ABHD12B",
+          "score": -0.01068,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 26,
+          "gene": "AASS",
+          "score": -0.085326,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 101,
+          "gene": "ABL2",
+          "score": 0.11353,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 60,
+          "gene": "ABCC8",
+          "score": 0.051595,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 73,
+          "gene": "ABCG5",
+          "score": 0.103443,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 95,
+          "gene": "ABI1",
+          "score": 0.0107805,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 59,
+          "gene": "ABCC6",
+          "score": 0.307105,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 39,
+          "gene": "ABCA7",
+          "score": -0.01946,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 72,
+          "gene": "ABCG4",
+          "score": 0.25585085,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 34,
+          "gene": "ABCA2",
+          "score": -0.2907179,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 51,
+          "gene": "ABCC1",
+          "score": -0.165605,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 61,
+          "gene": "ABCC9",
+          "score": 0.19773,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 38,
+          "gene": "ABCA6",
+          "score": -0.1365005,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 111,
+          "gene": "ABT1",
+          "score": 0.0858425,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 41,
+          "gene": "ABCA9",
+          "score": 0.27268896,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 84,
+          "gene": "ABHD16A",
+          "score": -0.1640935,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 78,
+          "gene": "ABHD12",
+          "score": 0.1263665,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 56,
+          "gene": "ABCC3",
+          "score": -0.0762865,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 42,
+          "gene": "ABCB1",
+          "score": -0.266345,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 100,
+          "gene": "ABL1",
+          "score": 0.0765485,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 22,
+          "gene": "AARS2",
+          "score": 0.03688,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 52,
+          "gene": "ABCC10",
+          "score": -0.1349245,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 70,
+          "gene": "ABCG1",
+          "score": 0.04291255,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 23,
+          "gene": "AARSD1",
+          "score": -0.007871,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 97,
+          "gene": "ABI3",
+          "score": -0.1086473,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 40,
+          "gene": "ABCA8",
+          "score": 0.0039675,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 106,
+          "gene": "ABR",
+          "score": 0.339915,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 121,
+          "gene": "ACAD8",
+          "score": 0.02707,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 67,
+          "gene": "ABCF1",
+          "score": -0.105515,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6,
+          "gene": "A4GNT",
+          "score": 0.029995,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 55,
+          "gene": "ABCC2",
+          "score": -0.1535965,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14,
+          "gene": "AAGAB",
+          "score": -0.31044,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 90,
+          "gene": "ABHD3",
+          "score": 0.071691,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 65,
+          "gene": "ABCD4",
+          "score": -0.04102,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 98,
+          "gene": "ABI3BP",
+          "score": -0.12602566,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 107,
+          "gene": "ABRA",
+          "score": 0.031534,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 117,
+          "gene": "ACACA",
+          "score": 0.035085,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8,
+          "gene": "AACS",
+          "score": 0.19899,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 24,
+          "gene": "AASDH",
+          "score": 0.140285,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 46,
+          "gene": "ABCB5",
+          "score": 0.0766415,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 37,
+          "gene": "ABCA5",
+          "score": 0.09411,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10,
+          "gene": "AADACL2",
+          "score": 0.180098,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 81,
+          "gene": "ABHD14A",
+          "score": -0.0982965,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15,
+          "gene": "AAK1",
+          "score": -0.144225,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 68,
+          "gene": "ABCF2",
+          "score": -0.1052725,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 58,
+          "gene": "ABCC5",
+          "score": 0.16644,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5,
+          "gene": "A4GALT",
+          "score": 0.15113,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 33,
+          "gene": "ABCA13",
+          "score": -0.01498,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 105,
+          "gene": "ABO",
+          "score": 0.016455,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 44,
+          "gene": "ABCB11",
+          "score": 0.09610045,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 45,
+          "gene": "ABCB4",
+          "score": 0.2502,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12,
+          "gene": "AADACL4",
+          "score": -0.165411,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 48,
+          "gene": "ABCB7",
+          "score": -0.505255,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 109,
+          "gene": "ABRAXAS1",
+          "score": 0.02837,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 119,
+          "gene": "ACAD10",
+          "score": 0.037576,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 88,
+          "gene": "ABHD17C",
+          "score": -0.0872855,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 108,
+          "gene": "ABRACL",
+          "score": -0.0995285,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 19,
+          "gene": "AAR2",
+          "score": 0.17943,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 93,
+          "gene": "ABHD6",
+          "score": -0.01869,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 43,
+          "gene": "ABCB10",
+          "score": -0.091724,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 112,
+          "gene": "ABTB1",
+          "score": 0.0953785,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 99,
+          "gene": "ABITRAM",
+          "score": 0.18748,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 20,
+          "gene": "AARD",
+          "score": 0.0074185,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 0,
+          "gene": "A1BG",
+          "score": -0.161214,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 124,
+          "gene": "ACADM",
+          "score": -0.17399,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 113,
+          "gene": "ABTB2",
+          "score": -0.15948,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 57,
+          "gene": "ABCC4",
+          "score": 0.07494,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 122,
+          "gene": "ACAD9",
+          "score": 0.0464,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 53,
+          "gene": "ABCC11",
+          "score": -0.1653245,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 115,
+          "gene": "ACAA1",
+          "score": 0.27926,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 89,
+          "gene": "ABHD2",
+          "score": -0.033632,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 83,
+          "gene": "ABHD15",
+          "score": 0.054218,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 91,
+          "gene": "ABHD4",
+          "score": -0.015138,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 25,
+          "gene": "AASDHPPT",
+          "score": 0.0825805,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 71,
+          "gene": "ABCG2",
+          "score": -0.000475,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 110,
+          "gene": "ABRAXAS2",
+          "score": -0.240335,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 77,
+          "gene": "ABHD11",
+          "score": 0.178475,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 64,
+          "gene": "ABCD3",
+          "score": -0.367169,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 29,
+          "gene": "ABAT",
+          "score": -0.01351,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 27,
+          "gene": "AATF",
+          "score": 0.3854245,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 116,
+          "gene": "ACAA2",
+          "score": -0.0323105,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 126,
+          "gene": "ACADSB",
+          "score": 0.0369245,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4,
+          "gene": "A3GALT2",
+          "score": 0.183225,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 54,
+          "gene": "ABCC12",
+          "score": -0.09262565,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 75,
+          "gene": "ABHD1",
+          "score": 0.09580065,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11,
+          "gene": "AADACL3",
+          "score": -0.217905,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 69,
+          "gene": "ABCF3",
+          "score": 0.0637145,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 114,
+          "gene": "ABTB3",
+          "score": 0.33209,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 120,
+          "gene": "ACAD11",
+          "score": 0.184825,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 86,
+          "gene": "ABHD17A",
+          "score": -0.35325,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13,
+          "gene": "AADAT",
+          "score": 0.23516,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 125,
+          "gene": "ACADS",
+          "score": 0.243119,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17,
+          "gene": "AAMP",
+          "score": 0.1659475,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 127,
+          "gene": "ACADVL",
+          "score": 0.0484775,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 31,
+          "gene": "ABCA10",
+          "score": -0.00779,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 35,
+          "gene": "ABCA3",
+          "score": 0.20382,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 94,
+          "gene": "ABHD8",
+          "score": -0.239638,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3,
+          "gene": "A2ML1",
+          "score": 0.005275,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 28,
+          "gene": "AATK",
+          "score": -0.027445,
+          "hit": 0,
+          "round": 0
+        }
+      ],
+      "queried_history": [
+        {
+          "candidate_index": 9,
+          "gene": "AADAC",
+          "score": 0.09700375,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 92,
+          "gene": "ABHD5",
+          "score": -0.123051,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 102,
+          "gene": "ABLIM1",
+          "score": -0.095673,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 76,
+          "gene": "ABHD10",
+          "score": -0.083665,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 49,
+          "gene": "ABCB8",
+          "score": -0.009105,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16,
+          "gene": "AAMDC",
+          "score": 0.01205,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 62,
+          "gene": "ABCD1",
+          "score": -0.0909125,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 103,
+          "gene": "ABLIM2",
+          "score": -0.220065,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 104,
+          "gene": "ABLIM3",
+          "score": 0.131625,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 82,
+          "gene": "ABHD14B",
+          "score": 0.025335,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 47,
+          "gene": "ABCB6",
+          "score": -0.042354,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 21,
+          "gene": "AARS1",
+          "score": -0.40020835,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 30,
+          "gene": "ABCA1",
+          "score": 0.1342295,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 118,
+          "gene": "ACACB",
+          "score": 0.018345,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 32,
+          "gene": "ABCA12",
+          "score": -0.108835,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 50,
+          "gene": "ABCB9",
+          "score": 0.21014065,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 63,
+          "gene": "ABCD2",
+          "score": 0.00524,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 123,
+          "gene": "ACADL",
+          "score": 0.147555,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 96,
+          "gene": "ABI2",
+          "score": -0.22205,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18,
+          "gene": "AANAT",
+          "score": 0.14409,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 74,
+          "gene": "ABCG8",
+          "score": -0.038225,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2,
+          "gene": "A2M",
+          "score": -0.18934,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 66,
+          "gene": "ABCE1",
+          "score": 0.359895,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 80,
+          "gene": "ABHD13",
+          "score": 0.022985,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 36,
+          "gene": "ABCA4",
+          "score": -0.159105,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 85,
+          "gene": "ABHD16B",
+          "score": -0.002058,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7,
+          "gene": "AAAS",
+          "score": 0.130627,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1,
+          "gene": "A1CF",
+          "score": 0.129081,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 87,
+          "gene": "ABHD17B",
+          "score": 0.23368,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 79,
+          "gene": "ABHD12B",
+          "score": -0.01068,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 26,
+          "gene": "AASS",
+          "score": -0.085326,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 101,
+          "gene": "ABL2",
+          "score": 0.11353,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 60,
+          "gene": "ABCC8",
+          "score": 0.051595,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 73,
+          "gene": "ABCG5",
+          "score": 0.103443,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 95,
+          "gene": "ABI1",
+          "score": 0.0107805,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 59,
+          "gene": "ABCC6",
+          "score": 0.307105,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 39,
+          "gene": "ABCA7",
+          "score": -0.01946,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 72,
+          "gene": "ABCG4",
+          "score": 0.25585085,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 34,
+          "gene": "ABCA2",
+          "score": -0.2907179,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 51,
+          "gene": "ABCC1",
+          "score": -0.165605,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 61,
+          "gene": "ABCC9",
+          "score": 0.19773,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 38,
+          "gene": "ABCA6",
+          "score": -0.1365005,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 111,
+          "gene": "ABT1",
+          "score": 0.0858425,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 41,
+          "gene": "ABCA9",
+          "score": 0.27268896,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 84,
+          "gene": "ABHD16A",
+          "score": -0.1640935,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 78,
+          "gene": "ABHD12",
+          "score": 0.1263665,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 56,
+          "gene": "ABCC3",
+          "score": -0.0762865,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 42,
+          "gene": "ABCB1",
+          "score": -0.266345,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 100,
+          "gene": "ABL1",
+          "score": 0.0765485,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 22,
+          "gene": "AARS2",
+          "score": 0.03688,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 52,
+          "gene": "ABCC10",
+          "score": -0.1349245,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 70,
+          "gene": "ABCG1",
+          "score": 0.04291255,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 23,
+          "gene": "AARSD1",
+          "score": -0.007871,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 97,
+          "gene": "ABI3",
+          "score": -0.1086473,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 40,
+          "gene": "ABCA8",
+          "score": 0.0039675,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 106,
+          "gene": "ABR",
+          "score": 0.339915,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 121,
+          "gene": "ACAD8",
+          "score": 0.02707,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 67,
+          "gene": "ABCF1",
+          "score": -0.105515,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6,
+          "gene": "A4GNT",
+          "score": 0.029995,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 55,
+          "gene": "ABCC2",
+          "score": -0.1535965,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14,
+          "gene": "AAGAB",
+          "score": -0.31044,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 90,
+          "gene": "ABHD3",
+          "score": 0.071691,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 65,
+          "gene": "ABCD4",
+          "score": -0.04102,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 98,
+          "gene": "ABI3BP",
+          "score": -0.12602566,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 107,
+          "gene": "ABRA",
+          "score": 0.031534,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 117,
+          "gene": "ACACA",
+          "score": 0.035085,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8,
+          "gene": "AACS",
+          "score": 0.19899,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 24,
+          "gene": "AASDH",
+          "score": 0.140285,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 46,
+          "gene": "ABCB5",
+          "score": 0.0766415,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 37,
+          "gene": "ABCA5",
+          "score": 0.09411,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10,
+          "gene": "AADACL2",
+          "score": 0.180098,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 81,
+          "gene": "ABHD14A",
+          "score": -0.0982965,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15,
+          "gene": "AAK1",
+          "score": -0.144225,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 68,
+          "gene": "ABCF2",
+          "score": -0.1052725,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 58,
+          "gene": "ABCC5",
+          "score": 0.16644,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5,
+          "gene": "A4GALT",
+          "score": 0.15113,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 33,
+          "gene": "ABCA13",
+          "score": -0.01498,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 105,
+          "gene": "ABO",
+          "score": 0.016455,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 44,
+          "gene": "ABCB11",
+          "score": 0.09610045,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 45,
+          "gene": "ABCB4",
+          "score": 0.2502,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12,
+          "gene": "AADACL4",
+          "score": -0.165411,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 48,
+          "gene": "ABCB7",
+          "score": -0.505255,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 109,
+          "gene": "ABRAXAS1",
+          "score": 0.02837,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 119,
+          "gene": "ACAD10",
+          "score": 0.037576,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 88,
+          "gene": "ABHD17C",
+          "score": -0.0872855,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 108,
+          "gene": "ABRACL",
+          "score": -0.0995285,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 19,
+          "gene": "AAR2",
+          "score": 0.17943,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 93,
+          "gene": "ABHD6",
+          "score": -0.01869,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 43,
+          "gene": "ABCB10",
+          "score": -0.091724,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 112,
+          "gene": "ABTB1",
+          "score": 0.0953785,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 99,
+          "gene": "ABITRAM",
+          "score": 0.18748,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 20,
+          "gene": "AARD",
+          "score": 0.0074185,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 0,
+          "gene": "A1BG",
+          "score": -0.161214,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 124,
+          "gene": "ACADM",
+          "score": -0.17399,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 113,
+          "gene": "ABTB2",
+          "score": -0.15948,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 57,
+          "gene": "ABCC4",
+          "score": 0.07494,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 122,
+          "gene": "ACAD9",
+          "score": 0.0464,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 53,
+          "gene": "ABCC11",
+          "score": -0.1653245,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 115,
+          "gene": "ACAA1",
+          "score": 0.27926,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 89,
+          "gene": "ABHD2",
+          "score": -0.033632,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 83,
+          "gene": "ABHD15",
+          "score": 0.054218,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 91,
+          "gene": "ABHD4",
+          "score": -0.015138,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 25,
+          "gene": "AASDHPPT",
+          "score": 0.0825805,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 71,
+          "gene": "ABCG2",
+          "score": -0.000475,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 110,
+          "gene": "ABRAXAS2",
+          "score": -0.240335,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 77,
+          "gene": "ABHD11",
+          "score": 0.178475,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 64,
+          "gene": "ABCD3",
+          "score": -0.367169,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 29,
+          "gene": "ABAT",
+          "score": -0.01351,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 27,
+          "gene": "AATF",
+          "score": 0.3854245,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 116,
+          "gene": "ACAA2",
+          "score": -0.0323105,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 126,
+          "gene": "ACADSB",
+          "score": 0.0369245,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4,
+          "gene": "A3GALT2",
+          "score": 0.183225,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 54,
+          "gene": "ABCC12",
+          "score": -0.09262565,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 75,
+          "gene": "ABHD1",
+          "score": 0.09580065,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11,
+          "gene": "AADACL3",
+          "score": -0.217905,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 69,
+          "gene": "ABCF3",
+          "score": 0.0637145,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 114,
+          "gene": "ABTB3",
+          "score": 0.33209,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 120,
+          "gene": "ACAD11",
+          "score": 0.184825,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 86,
+          "gene": "ABHD17A",
+          "score": -0.35325,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13,
+          "gene": "AADAT",
+          "score": 0.23516,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 125,
+          "gene": "ACADS",
+          "score": 0.243119,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17,
+          "gene": "AAMP",
+          "score": 0.1659475,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 127,
+          "gene": "ACADVL",
+          "score": 0.0484775,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 31,
+          "gene": "ABCA10",
+          "score": -0.00779,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 35,
+          "gene": "ABCA3",
+          "score": 0.20382,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 94,
+          "gene": "ABHD8",
+          "score": -0.239638,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3,
+          "gene": "A2ML1",
+          "score": 0.005275,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 28,
+          "gene": "AATK",
+          "score": -0.027445,
+          "hit": 0,
+          "round": 0
+        }
+      ]
+    }
+  }
+}
```
