# Change Record — candidate_1

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IL2/run-2/best/current/harness
Generated at: 2026-04-30T07:03:42.938721

## Files Changed

- model.py: modified (added=123, deleted=4, delta=119)
- outputs/metrics.json: new (added=2233, deleted=0, delta=2233)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -1,4 +1,6 @@
 from __future__ import annotations
+import random
+import numpy as np
 
 def select(candidates, history, batch_size, seed) -> list[int]:
     """
@@ -25,8 +27,125 @@
     Output:
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
 
-    You may implement any suitable algorithmic model here, including but not limited to:
-    traditional algorithms, machine learning models, deep learning models, biological models,
-    and mathematical models.
+    Strategy:
+    - Thompson Sampling with Beta-Bernoulli model for hit probability
+    - Uses gene search to expand candidate pool for similar genes
+    - Naturally balances exploration vs exploitation through posterior sampling
     """
-    pass
+    rng = random.Random(seed)
+    np.random.seed(seed)
+    
+    # Get already selected indices
+    already_selected = {h['candidate_index'] for h in history}
+    
+    # Get all available candidate indices
+    all_indices = list(range(len(candidates)))
+    available_indices = [idx for idx in all_indices if idx not in already_selected]
+    
+    # If no history or not enough candidates, return random selection
+    if not history or len(available_indices) <= batch_size:
+        selected = rng.sample(available_indices, min(batch_size, len(available_indices)))
+        return selected
+    
+    # Build gene performance statistics
+    # Track hits and trials per gene
+    gene_stats = {}  # gene_name -> {'hits': int, 'trials': int}
+    
+    for h in history:
+        idx = h['candidate_index']
+        candidate = candidates[idx]
+        
+        # Get gene name
+        if 'gene' in candidate:
+            gene = candidate['gene']
+        elif 'gene_a' in candidate:
+            gene = candidate['gene_a']
+        else:
+            continue
+        
+        if gene not in gene_stats:
+            gene_stats[gene] = {'hits': 0, 'trials': 0}
+        
+        gene_stats[gene]['trials'] += 1
+        if h.get('hit', 0) == 1:
+            gene_stats[gene]['hits'] += 1
+    
+    # Thompson Sampling: Sample hit probabilities from Beta posterior
+    # Prior: Beta(1, 1) which is uniform [0, 1]
+    # Posterior: Beta(1 + hits, 1 + trials - hits)
+    gene_sampled_probs = {}
+    
+    for gene, stats in gene_stats.items():
+        hits = stats['hits']
+        trials = stats['trials']
+        # Sample from Beta posterior
+        sampled_prob = np.random.beta(1 + hits, 1 + trials - hits)
+        gene_sampled_probs[gene] = sampled_prob
+    
+    # Create candidate pool with Thompson Sampling scores
+    candidate_pool = []
+    
+    # Add candidates corresponding to tested genes with sampled probabilities
+    for h in history:
+        idx = h['candidate_index']
+        if idx not in available_indices:
+            continue
+        
+        candidate = candidates[idx]
+        if 'gene' in candidate:
+            gene = candidate['gene']
+        elif 'gene_a' in candidate:
+            gene = candidate['gene_a']
+        else:
+            continue
+        
+        if gene in gene_sampled_probs:
+            candidate_pool.append((idx, gene_sampled_probs[gene]))
+    
+    # Try to use gene search to expand pool with similar genes
+    try:
+        import bda_tools
+        
+        # Sort genes by sampled probability (descending)
+        sorted_genes = sorted(gene_sampled_probs.items(), key=lambda x: x[1], reverse=True)
+        
+        # Search similar genes for top performers
+        genes_seen = set()
+        for gene, prob in sorted_genes[:max(10, len(sorted_genes) // 5)]:
+            if gene in genes_seen:
+                continue
+            genes_seen.add(gene)
+            
+            try:
+                # Search for similar genes
+                similar_indices = bda_tools.gene_search(gene, k=10, diverse=False)
+                
+                # Assign Thompson Sampling score to similar genes
+                # Use the sampled probability of the query gene
+                for sim_idx in similar_indices:
+                    if sim_idx in available_indices and sim_idx not in [c[0] for c in candidate_pool]:
+                        candidate_pool.append((sim_idx, prob))
+            except:
+                pass
+    except ImportError:
+        pass
+    
+    # Sort candidate pool by Thompson Sampling score
+    candidate_pool.sort(key=lambda x: x[1], reverse=True)
+    
+    # Select top candidates from pool
+    selected = []
+    if candidate_pool:
+        # Take top candidates based on Thompson Sampling scores
+        num_from_pool = min(batch_size, len(candidate_pool))
+        selected = [idx for idx, _ in candidate_pool[:num_from_pool]]
+    
+    # If we need more candidates, add random exploration
+    if len(selected) < batch_size:
+        remaining_available = [idx for idx in available_indices if idx not in selected]
+        if remaining_available:
+            num_needed = batch_size - len(selected)
+            num_to_add = min(num_needed, len(remaining_available))
+            selected.extend(rng.sample(remaining_available, num_to_add))
+    
+    return selected[:batch_size]

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -0,0 +1,2233 @@
+{
+  "task": "perturb-genes-brief",
+  "data_name": "IL2",
+  "measurement": "the log fold change in Interleukin-2 (IL-2) normalized read counts",
+  "task_prompt": {
+    "Task": "identify genes that regulate the production of Interleukin-2 (IL-2)",
+    "Measurement": "the log fold change in Interleukin-2 (IL-2) normalized read counts"
+  },
+  "metrics": {
+    "test": {
+      "pool_size": 18939,
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
+      "top_k": 654,
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
+      "auc_normalized": 0.0015290519877675841,
+      "ncg": 0.10946446196271965,
+      "round_details": [
+        {
+          "round": 0,
+          "selected_count": 128,
+          "hits": 2,
+          "cumulative_hits": 2,
+          "precision_at_batch": 0.015625,
+          "selected": [
+            "ILKAP",
+            "SLC7A3",
+            "C21orf59",
+            "EPM2A",
+            "CMBL",
+            "BCAP29",
+            "POLE2",
+            "ALYREF",
+            "SSBP3",
+            "USP35",
+            "ATP1A2",
+            "TIMM10B",
+            "PLA2G16",
+            "CENPBD1",
+            "CFHR4",
+            "DCTN5",
+            "KIAA0754",
+            "CELF3",
+            "SH3BP5",
+            "LMBR1L",
+            "ATP5G3",
+            "MOV10L1",
+            "HLA-DQA1",
+            "GPALPP1",
+            "CREBBP",
+            "TMEM53",
+            "APTX",
+            "IGSF22",
+            "NRG2",
+            "KRTAP22-2",
+            "SPO11",
+            "PQLC2L",
+            "SIMC1",
+            "CNTNAP3B",
+            "LRRC20",
+            "EPS8L3",
+            "LHX5",
+            "OR8H3",
+            "CEP68",
+            "CATSPER1",
+            "EIF4EBP3",
+            "ECM2",
+            "LOC284898",
+            "OR5M3",
+            "CEP78",
+            "NFKBIA",
+            "OVCA2",
+            "KREMEN2",
+            "MEMO1",
+            "RWDD2B",
+            "ZNF490",
+            "SH3BP2",
+            "YWHAZ",
+            "MRTO4",
+            "POU4F3",
+            "C6orf132",
+            "TMEM229B",
+            "ATP8A2",
+            "CTAGE6",
+            "LCN8",
+            "SRGAP2C",
+            "ACKR2",
+            "WNT3A",
+            "NOL12",
+            "FOXS1",
+            "DRD4",
+            "CNPPD1",
+            "MMP21",
+            "TXNDC8",
+            "MAGI2",
+            "SYNE1",
+            "SFTPA2",
+            "ZNF566",
+            "KRTAP19-5",
+            "NAGS",
+            "C20orf144",
+            "NIFK",
+            "TMEM268",
+            "GFM2",
+            "TNFSF11",
+            "LRIG2",
+            "RPLP0",
+            "SFRP4",
+            "HBEGF",
+            "THTPA",
+            "LRPPRC",
+            "ZNF740",
+            "WNT5A",
+            "NASP",
+            "GYS1",
+            "ZFYVE27",
+            "APC2",
+            "OR2J3",
+            "PARD3",
+            "MYLK",
+            "DPP7",
+            "CLEC16A",
+            "FA2H",
+            "PPFIA1",
+            "DEFB116",
+            "HLA-DQB1",
+            "FAM43B",
+            "SOX30",
+            "FOXO6",
+            "SLC25A34",
+            "ACIN1",
+            "DMKN",
+            "FYB",
+            "OR2F2",
+            "IFNA14",
+            "SPINK8",
+            "SLAMF8",
+            "TMEM260",
+            "NAGPA",
+            "VPS33A",
+            "RAB1B",
+            "LCE5A",
+            "BFAR",
+            "MFSD8",
+            "TIMM17B",
+            "TMBIM4",
+            "DCXR",
+            "SLC25A40",
+            "IER2",
+            "TRAK1",
+            "SUMO1",
+            "NAMPT",
+            "PTTG2"
+          ],
+          "selected_scores": [
+            0.01106,
+            -0.10663,
+            0.046914,
+            -0.054053,
+            0.052273,
+            0.051055,
+            0.093466,
+            0.19903,
+            -0.23246,
+            0.03355,
+            -0.2031,
+            -0.28268,
+            -0.21437,
+            0.059897,
+            -0.096415,
+            0.50045,
+            -0.17078,
+            0.076988,
+            0.17998,
+            0.072043,
+            -0.071837,
+            -0.056153,
+            0.062367,
+            0.15528,
+            -0.25859,
+            -0.098286,
+            0.052481,
+            -0.097452,
+            0.12534,
+            -0.024004,
+            0.12787,
+            -0.04925,
+            -0.064746,
+            -0.03737,
+            0.082693,
+            0.050768,
+            0.17887,
+            0.034619,
+            -0.13196,
+            -0.18712,
+            0.14182,
+            0.13478,
+            0.0091898,
+            -0.057844,
+            0.12283,
+            0.14574,
+            0.21121,
+            -0.08067,
+            0.73471,
+            0.093253,
+            -0.15993,
+            -0.11788,
+            -0.052884,
+            -0.057524,
+            -0.033234,
+            -0.017814,
+            -0.11726,
+            0.15144,
+            -0.04022,
+            -0.084012,
+            0.01427,
+            -0.093882,
+            0.19544,
+            -0.062201,
+            -0.087002,
+            0.017744,
+            -0.12037,
+            -0.046955,
+            -0.018096,
+            0.10336,
+            -0.12223,
+            0.064198,
+            0.12948,
+            0.073363,
+            -0.049917,
+            0.16321,
+            0.26479,
+            0.0085949,
+            -0.0091051,
+            -0.25904,
+            -0.024438,
+            0.25585,
+            0.057375,
+            0.14176,
+            -0.051704,
+            0.17284,
+            0.058713,
+            0.03889,
+            0.2853,
+            0.054807,
+            0.14991,
+            -0.0010187,
+            -0.055757,
+            0.061334,
+            0.046966,
+            0.14819,
+            0.23957,
+            0.032426,
+            0.011903,
+            0.056855,
+            0.083377,
+            0.070334,
+            -0.034098,
+            0.15798,
+            -0.043333,
+            -0.1498,
+            -0.089161,
+            -0.11311,
+            -0.035877,
+            0.055208,
+            -0.043273,
+            -0.19809,
+            0.015501,
+            -0.069095,
+            0.084537,
+            0.34005,
+            0.014338,
+            0.15287,
+            -0.15928,
+            0.010223,
+            0.092215,
+            0.281,
+            0.068711,
+            -0.081251,
+            0.017949,
+            0.027002,
+            -0.11147,
+            -0.0016693
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
+          "candidate_index": 3648,
+          "gene": "ILKAP",
+          "score": 0.01106,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 819,
+          "gene": "SLC7A3",
+          "score": -0.10663,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9012,
+          "gene": "C21orf59",
+          "score": 0.046914,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8024,
+          "gene": "EPM2A",
+          "score": -0.054053,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7314,
+          "gene": "CMBL",
+          "score": 0.052273,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4572,
+          "gene": "BCAP29",
+          "score": 0.051055,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3358,
+          "gene": "POLE2",
+          "score": 0.093466,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17870,
+          "gene": "ALYREF",
+          "score": 0.19903,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2848,
+          "gene": "SSBP3",
+          "score": -0.23246,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13825,
+          "gene": "USP35",
+          "score": 0.03355,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1041,
+          "gene": "ATP1A2",
+          "score": -0.2031,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 976,
+          "gene": "TIMM10B",
+          "score": -0.28268,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3070,
+          "gene": "PLA2G16",
+          "score": -0.21437,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7164,
+          "gene": "CENPBD1",
+          "score": 0.059897,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7623,
+          "gene": "CFHR4",
+          "score": -0.096415,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16559,
+          "gene": "DCTN5",
+          "score": 0.50045,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 869,
+          "gene": "KIAA0754",
+          "score": -0.17078,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18390,
+          "gene": "CELF3",
+          "score": 0.076988,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6515,
+          "gene": "SH3BP5",
+          "score": 0.17998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17856,
+          "gene": "LMBR1L",
+          "score": 0.072043,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13746,
+          "gene": "ATP5G3",
+          "score": -0.071837,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7223,
+          "gene": "MOV10L1",
+          "score": -0.056153,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14719,
+          "gene": "HLA-DQA1",
+          "score": 0.062367,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9115,
+          "gene": "GPALPP1",
+          "score": 0.15528,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 212,
+          "gene": "CREBBP",
+          "score": -0.25859,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5231,
+          "gene": "TMEM53",
+          "score": -0.098286,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13848,
+          "gene": "APTX",
+          "score": 0.052481,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11149,
+          "gene": "IGSF22",
+          "score": -0.097452,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9105,
+          "gene": "NRG2",
+          "score": 0.12534,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5094,
+          "gene": "KRTAP22-2",
+          "score": -0.024004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7055,
+          "gene": "SPO11",
+          "score": 0.12787,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11029,
+          "gene": "PQLC2L",
+          "score": -0.04925,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3349,
+          "gene": "SIMC1",
+          "score": -0.064746,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3039,
+          "gene": "CNTNAP3B",
+          "score": -0.03737,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12449,
+          "gene": "LRRC20",
+          "score": 0.082693,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3169,
+          "gene": "EPS8L3",
+          "score": 0.050768,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11763,
+          "gene": "LHX5",
+          "score": 0.17887,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11270,
+          "gene": "OR8H3",
+          "score": 0.034619,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8667,
+          "gene": "CEP68",
+          "score": -0.13196,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1423,
+          "gene": "CATSPER1",
+          "score": -0.18712,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15054,
+          "gene": "EIF4EBP3",
+          "score": 0.14182,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17571,
+          "gene": "ECM2",
+          "score": 0.13478,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4090,
+          "gene": "LOC284898",
+          "score": 0.0091898,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12403,
+          "gene": "OR5M3",
+          "score": -0.057844,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2582,
+          "gene": "CEP78",
+          "score": 0.12283,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18089,
+          "gene": "NFKBIA",
+          "score": 0.14574,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9606,
+          "gene": "OVCA2",
+          "score": 0.21121,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11850,
+          "gene": "KREMEN2",
+          "score": -0.08067,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18918,
+          "gene": "MEMO1",
+          "score": 0.73471,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 6300,
+          "gene": "RWDD2B",
+          "score": 0.093253,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2279,
+          "gene": "ZNF490",
+          "score": -0.15993,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1501,
+          "gene": "SH3BP2",
+          "score": -0.11788,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7467,
+          "gene": "YWHAZ",
+          "score": -0.052884,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9482,
+          "gene": "MRTO4",
+          "score": -0.057524,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2614,
+          "gene": "POU4F3",
+          "score": -0.033234,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7628,
+          "gene": "C6orf132",
+          "score": -0.017814,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3309,
+          "gene": "TMEM229B",
+          "score": -0.11726,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12455,
+          "gene": "ATP8A2",
+          "score": 0.15144,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9108,
+          "gene": "CTAGE6",
+          "score": -0.04022,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14857,
+          "gene": "LCN8",
+          "score": -0.084012,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11954,
+          "gene": "SRGAP2C",
+          "score": 0.01427,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5329,
+          "gene": "ACKR2",
+          "score": -0.093882,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12130,
+          "gene": "WNT3A",
+          "score": 0.19544,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11641,
+          "gene": "NOL12",
+          "score": -0.062201,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6865,
+          "gene": "FOXS1",
+          "score": -0.087002,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8748,
+          "gene": "DRD4",
+          "score": 0.017744,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2339,
+          "gene": "CNPPD1",
+          "score": -0.12037,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5607,
+          "gene": "MMP21",
+          "score": -0.046955,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17502,
+          "gene": "TXNDC8",
+          "score": -0.018096,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8021,
+          "gene": "MAGI2",
+          "score": 0.10336,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5354,
+          "gene": "SYNE1",
+          "score": -0.12223,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15147,
+          "gene": "SFTPA2",
+          "score": 0.064198,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12433,
+          "gene": "ZNF566",
+          "score": 0.12948,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8845,
+          "gene": "KRTAP19-5",
+          "score": 0.073363,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18250,
+          "gene": "NAGS",
+          "score": -0.049917,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7196,
+          "gene": "C20orf144",
+          "score": 0.16321,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10626,
+          "gene": "NIFK",
+          "score": 0.26479,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1832,
+          "gene": "TMEM268",
+          "score": 0.0085949,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7505,
+          "gene": "GFM2",
+          "score": -0.0091051,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1051,
+          "gene": "TNFSF11",
+          "score": -0.25904,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10336,
+          "gene": "LRIG2",
+          "score": -0.024438,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13145,
+          "gene": "RPLP0",
+          "score": 0.25585,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8773,
+          "gene": "SFRP4",
+          "score": 0.057375,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2168,
+          "gene": "HBEGF",
+          "score": 0.14176,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6913,
+          "gene": "THTPA",
+          "score": -0.051704,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18585,
+          "gene": "LRPPRC",
+          "score": 0.17284,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10311,
+          "gene": "ZNF740",
+          "score": 0.058713,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6967,
+          "gene": "WNT5A",
+          "score": 0.03889,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16358,
+          "gene": "NASP",
+          "score": 0.2853,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12964,
+          "gene": "GYS1",
+          "score": 0.054807,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15035,
+          "gene": "ZFYVE27",
+          "score": 0.14991,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4681,
+          "gene": "APC2",
+          "score": -0.0010187,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8679,
+          "gene": "OR2J3",
+          "score": -0.055757,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4575,
+          "gene": "PARD3",
+          "score": 0.061334,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8081,
+          "gene": "MYLK",
+          "score": 0.046966,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18394,
+          "gene": "DPP7",
+          "score": 0.14819,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17661,
+          "gene": "CLEC16A",
+          "score": 0.23957,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8609,
+          "gene": "FA2H",
+          "score": 0.032426,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14038,
+          "gene": "PPFIA1",
+          "score": 0.011903,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13087,
+          "gene": "DEFB116",
+          "score": 0.056855,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11861,
+          "gene": "HLA-DQB1",
+          "score": 0.083377,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7186,
+          "gene": "FAM43B",
+          "score": 0.070334,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4532,
+          "gene": "SOX30",
+          "score": -0.034098,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16696,
+          "gene": "FOXO6",
+          "score": 0.15798,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16171,
+          "gene": "SLC25A34",
+          "score": -0.043333,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2978,
+          "gene": "ACIN1",
+          "score": -0.1498,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1543,
+          "gene": "DMKN",
+          "score": -0.089161,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3592,
+          "gene": "FYB",
+          "score": -0.11311,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5008,
+          "gene": "OR2F2",
+          "score": -0.035877,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5242,
+          "gene": "IFNA14",
+          "score": 0.055208,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13833,
+          "gene": "SPINK8",
+          "score": -0.043273,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2081,
+          "gene": "SLAMF8",
+          "score": -0.19809,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12608,
+          "gene": "TMEM260",
+          "score": 0.015501,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12504,
+          "gene": "NAGPA",
+          "score": -0.069095,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15337,
+          "gene": "VPS33A",
+          "score": 0.084537,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17338,
+          "gene": "RAB1B",
+          "score": 0.34005,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8238,
+          "gene": "LCE5A",
+          "score": 0.014338,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18128,
+          "gene": "BFAR",
+          "score": 0.15287,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 376,
+          "gene": "MFSD8",
+          "score": -0.15928,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3753,
+          "gene": "TIMM17B",
+          "score": 0.010223,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17595,
+          "gene": "TMBIM4",
+          "score": 0.092215,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8743,
+          "gene": "DCXR",
+          "score": 0.281,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11146,
+          "gene": "SLC25A40",
+          "score": 0.068711,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3655,
+          "gene": "IER2",
+          "score": -0.081251,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9617,
+          "gene": "TRAK1",
+          "score": 0.017949,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14246,
+          "gene": "SUMO1",
+          "score": 0.027002,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5182,
+          "gene": "NAMPT",
+          "score": -0.11147,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14867,
+          "gene": "PTTG2",
+          "score": -0.0016693,
+          "hit": 0,
+          "round": 0
+        }
+      ],
+      "queried_history": [
+        {
+          "candidate_index": 3648,
+          "gene": "ILKAP",
+          "score": 0.01106,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 819,
+          "gene": "SLC7A3",
+          "score": -0.10663,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9012,
+          "gene": "C21orf59",
+          "score": 0.046914,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8024,
+          "gene": "EPM2A",
+          "score": -0.054053,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7314,
+          "gene": "CMBL",
+          "score": 0.052273,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4572,
+          "gene": "BCAP29",
+          "score": 0.051055,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3358,
+          "gene": "POLE2",
+          "score": 0.093466,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17870,
+          "gene": "ALYREF",
+          "score": 0.19903,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2848,
+          "gene": "SSBP3",
+          "score": -0.23246,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13825,
+          "gene": "USP35",
+          "score": 0.03355,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1041,
+          "gene": "ATP1A2",
+          "score": -0.2031,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 976,
+          "gene": "TIMM10B",
+          "score": -0.28268,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3070,
+          "gene": "PLA2G16",
+          "score": -0.21437,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7164,
+          "gene": "CENPBD1",
+          "score": 0.059897,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7623,
+          "gene": "CFHR4",
+          "score": -0.096415,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16559,
+          "gene": "DCTN5",
+          "score": 0.50045,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 869,
+          "gene": "KIAA0754",
+          "score": -0.17078,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18390,
+          "gene": "CELF3",
+          "score": 0.076988,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6515,
+          "gene": "SH3BP5",
+          "score": 0.17998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17856,
+          "gene": "LMBR1L",
+          "score": 0.072043,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13746,
+          "gene": "ATP5G3",
+          "score": -0.071837,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7223,
+          "gene": "MOV10L1",
+          "score": -0.056153,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14719,
+          "gene": "HLA-DQA1",
+          "score": 0.062367,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9115,
+          "gene": "GPALPP1",
+          "score": 0.15528,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 212,
+          "gene": "CREBBP",
+          "score": -0.25859,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5231,
+          "gene": "TMEM53",
+          "score": -0.098286,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13848,
+          "gene": "APTX",
+          "score": 0.052481,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11149,
+          "gene": "IGSF22",
+          "score": -0.097452,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9105,
+          "gene": "NRG2",
+          "score": 0.12534,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5094,
+          "gene": "KRTAP22-2",
+          "score": -0.024004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7055,
+          "gene": "SPO11",
+          "score": 0.12787,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11029,
+          "gene": "PQLC2L",
+          "score": -0.04925,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3349,
+          "gene": "SIMC1",
+          "score": -0.064746,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3039,
+          "gene": "CNTNAP3B",
+          "score": -0.03737,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12449,
+          "gene": "LRRC20",
+          "score": 0.082693,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3169,
+          "gene": "EPS8L3",
+          "score": 0.050768,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11763,
+          "gene": "LHX5",
+          "score": 0.17887,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11270,
+          "gene": "OR8H3",
+          "score": 0.034619,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8667,
+          "gene": "CEP68",
+          "score": -0.13196,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1423,
+          "gene": "CATSPER1",
+          "score": -0.18712,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15054,
+          "gene": "EIF4EBP3",
+          "score": 0.14182,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17571,
+          "gene": "ECM2",
+          "score": 0.13478,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4090,
+          "gene": "LOC284898",
+          "score": 0.0091898,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12403,
+          "gene": "OR5M3",
+          "score": -0.057844,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2582,
+          "gene": "CEP78",
+          "score": 0.12283,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18089,
+          "gene": "NFKBIA",
+          "score": 0.14574,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9606,
+          "gene": "OVCA2",
+          "score": 0.21121,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11850,
+          "gene": "KREMEN2",
+          "score": -0.08067,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18918,
+          "gene": "MEMO1",
+          "score": 0.73471,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 6300,
+          "gene": "RWDD2B",
+          "score": 0.093253,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2279,
+          "gene": "ZNF490",
+          "score": -0.15993,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1501,
+          "gene": "SH3BP2",
+          "score": -0.11788,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7467,
+          "gene": "YWHAZ",
+          "score": -0.052884,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9482,
+          "gene": "MRTO4",
+          "score": -0.057524,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2614,
+          "gene": "POU4F3",
+          "score": -0.033234,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7628,
+          "gene": "C6orf132",
+          "score": -0.017814,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3309,
+          "gene": "TMEM229B",
+          "score": -0.11726,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12455,
+          "gene": "ATP8A2",
+          "score": 0.15144,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9108,
+          "gene": "CTAGE6",
+          "score": -0.04022,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14857,
+          "gene": "LCN8",
+          "score": -0.084012,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11954,
+          "gene": "SRGAP2C",
+          "score": 0.01427,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5329,
+          "gene": "ACKR2",
+          "score": -0.093882,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12130,
+          "gene": "WNT3A",
+          "score": 0.19544,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11641,
+          "gene": "NOL12",
+          "score": -0.062201,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6865,
+          "gene": "FOXS1",
+          "score": -0.087002,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8748,
+          "gene": "DRD4",
+          "score": 0.017744,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2339,
+          "gene": "CNPPD1",
+          "score": -0.12037,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5607,
+          "gene": "MMP21",
+          "score": -0.046955,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17502,
+          "gene": "TXNDC8",
+          "score": -0.018096,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8021,
+          "gene": "MAGI2",
+          "score": 0.10336,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5354,
+          "gene": "SYNE1",
+          "score": -0.12223,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15147,
+          "gene": "SFTPA2",
+          "score": 0.064198,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12433,
+          "gene": "ZNF566",
+          "score": 0.12948,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8845,
+          "gene": "KRTAP19-5",
+          "score": 0.073363,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18250,
+          "gene": "NAGS",
+          "score": -0.049917,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7196,
+          "gene": "C20orf144",
+          "score": 0.16321,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10626,
+          "gene": "NIFK",
+          "score": 0.26479,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1832,
+          "gene": "TMEM268",
+          "score": 0.0085949,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7505,
+          "gene": "GFM2",
+          "score": -0.0091051,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1051,
+          "gene": "TNFSF11",
+          "score": -0.25904,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10336,
+          "gene": "LRIG2",
+          "score": -0.024438,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13145,
+          "gene": "RPLP0",
+          "score": 0.25585,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8773,
+          "gene": "SFRP4",
+          "score": 0.057375,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2168,
+          "gene": "HBEGF",
+          "score": 0.14176,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6913,
+          "gene": "THTPA",
+          "score": -0.051704,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18585,
+          "gene": "LRPPRC",
+          "score": 0.17284,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10311,
+          "gene": "ZNF740",
+          "score": 0.058713,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6967,
+          "gene": "WNT5A",
+          "score": 0.03889,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16358,
+          "gene": "NASP",
+          "score": 0.2853,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12964,
+          "gene": "GYS1",
+          "score": 0.054807,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15035,
+          "gene": "ZFYVE27",
+          "score": 0.14991,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4681,
+          "gene": "APC2",
+          "score": -0.0010187,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8679,
+          "gene": "OR2J3",
+          "score": -0.055757,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4575,
+          "gene": "PARD3",
+          "score": 0.061334,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8081,
+          "gene": "MYLK",
+          "score": 0.046966,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18394,
+          "gene": "DPP7",
+          "score": 0.14819,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17661,
+          "gene": "CLEC16A",
+          "score": 0.23957,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8609,
+          "gene": "FA2H",
+          "score": 0.032426,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14038,
+          "gene": "PPFIA1",
+          "score": 0.011903,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13087,
+          "gene": "DEFB116",
+          "score": 0.056855,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11861,
+          "gene": "HLA-DQB1",
+          "score": 0.083377,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7186,
+          "gene": "FAM43B",
+          "score": 0.070334,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4532,
+          "gene": "SOX30",
+          "score": -0.034098,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16696,
+          "gene": "FOXO6",
+          "score": 0.15798,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16171,
+          "gene": "SLC25A34",
+          "score": -0.043333,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2978,
+          "gene": "ACIN1",
+          "score": -0.1498,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1543,
+          "gene": "DMKN",
+          "score": -0.089161,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3592,
+          "gene": "FYB",
+          "score": -0.11311,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5008,
+          "gene": "OR2F2",
+          "score": -0.035877,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5242,
+          "gene": "IFNA14",
+          "score": 0.055208,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13833,
+          "gene": "SPINK8",
+          "score": -0.043273,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2081,
+          "gene": "SLAMF8",
+          "score": -0.19809,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12608,
+          "gene": "TMEM260",
+          "score": 0.015501,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12504,
+          "gene": "NAGPA",
+          "score": -0.069095,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15337,
+          "gene": "VPS33A",
+          "score": 0.084537,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17338,
+          "gene": "RAB1B",
+          "score": 0.34005,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8238,
+          "gene": "LCE5A",
+          "score": 0.014338,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18128,
+          "gene": "BFAR",
+          "score": 0.15287,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 376,
+          "gene": "MFSD8",
+          "score": -0.15928,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3753,
+          "gene": "TIMM17B",
+          "score": 0.010223,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17595,
+          "gene": "TMBIM4",
+          "score": 0.092215,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8743,
+          "gene": "DCXR",
+          "score": 0.281,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11146,
+          "gene": "SLC25A40",
+          "score": 0.068711,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3655,
+          "gene": "IER2",
+          "score": -0.081251,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9617,
+          "gene": "TRAK1",
+          "score": 0.017949,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14246,
+          "gene": "SUMO1",
+          "score": 0.027002,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5182,
+          "gene": "NAMPT",
+          "score": -0.11147,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14867,
+          "gene": "PTTG2",
+          "score": -0.0016693,
+          "hit": 0,
+          "round": 0
+        }
+      ]
+    }
+  }
+}
```
