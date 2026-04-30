# Change Record — candidate_1

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21_down/run-1/best/current/harness
Generated at: 2026-04-30T06:58:24.122566

## Files Changed

- model.py: modified (added=181, deleted=5, delta=176)
- outputs/metrics.json: new (added=2233, deleted=0, delta=2233)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -1,4 +1,7 @@
 from __future__ import annotations
+import random
+import numpy as np
+from collections import defaultdict
 
 def select(candidates, history, batch_size, seed) -> list[int]:
     """
@@ -24,9 +27,182 @@
 
     Output:
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
-
-    You may implement any suitable algorithmic model here, including but not limited to:
-    traditional algorithms, machine learning models, deep learning models, biological models,
-    and mathematical models.
+    
+    Strategy: Thompson Sampling with Gene Cluster Priors
+    - Uses Thompson Sampling (Bayesian bandit algorithm) for adaptive exploration-exploitation
+    - Models each candidate with Beta distribution based on hit observations
+    - Uses gene search to create clusters and share information via Bayesian priors
+    - Enhanced fallback: Uses gene name prefix clustering when gene search unavailable
+    - Naturally balances exploration vs exploitation based on uncertainty
     """
-    pass
+    rng = random.Random(seed)
+    np.random.seed(seed)
+    
+    # Get already selected indices
+    selected = set(h['candidate_index'] for h in history)
+    
+    # Get all available candidate indices
+    all_indices = list(range(len(candidates)))
+    available = [i for i in all_indices if i not in selected]
+    
+    if len(available) <= batch_size:
+        return available
+    
+    # If no history, use pure exploration
+    if len(history) == 0:
+        return rng.sample(available, batch_size)
+    
+    # Check if hit information is available
+    has_hits = any('hit' in h for h in history)
+    
+    if not has_hits:
+        # Fall back to score-based selection using absolute scores
+        sorted_history = sorted(history, key=lambda x: abs(x['score']), reverse=True)
+        top_k = max(10, len(sorted_history) // 5)
+        top_performers = [h['candidate_index'] for h in sorted_history[:top_k]]
+        
+        # Sample from top performers
+        selected_indices = []
+        remaining = available.copy()
+        
+        # Take some top performers if available
+        top_available = [idx for idx in top_performers if idx in remaining]
+        if top_available:
+            n_top = min(len(top_available), batch_size // 2)
+            selected_indices.extend(rng.sample(top_available, n_top))
+            remaining = [i for i in remaining if i not in selected_indices]
+        
+        # Fill rest with random exploration
+        if len(selected_indices) < batch_size:
+            needed = batch_size - len(selected_indices)
+            selected_indices.extend(rng.sample(remaining, min(needed, len(remaining))))
+        
+        return selected_indices[:batch_size]
+    
+    # Thompson Sampling with Gene Cluster Priors
+    # Group candidates into clusters based on gene similarity
+    clusters = defaultdict(list)
+    candidate_to_cluster = {}
+    
+    # Try to use gene search to create clusters
+    try:
+        import bda_tools
+        
+        # Create clusters for all candidates we have history for
+        for h in history:
+            idx = h['candidate_index']
+            candidate = candidates[idx]
+            gene = candidate.get('gene') or candidate.get('gene_a')
+            
+            if gene and idx not in candidate_to_cluster:
+                # Find similar genes
+                try:
+                    similar = bda_tools.gene_search(gene, k=20, diverse=False)
+                    cluster_id = f"cluster_{gene}"
+                    
+                    for sim_idx in similar:
+                        if sim_idx not in candidate_to_cluster:
+                            candidate_to_cluster[sim_idx] = cluster_id
+                            clusters[cluster_id].append(sim_idx)
+                except:
+                    # If gene search fails, put in singleton cluster
+                    cluster_id = f"singleton_{idx}"
+                    candidate_to_cluster[idx] = cluster_id
+                    clusters[cluster_id] = [idx]
+        
+        # Assign unassigned candidates to singleton clusters
+        for idx in all_indices:
+            if idx not in candidate_to_cluster:
+                cluster_id = f"singleton_{idx}"
+                candidate_to_cluster[idx] = cluster_id
+                clusters[cluster_id] = [idx]
+                
+    except ImportError:
+        # No gene search available - use enhanced fallback: gene family prefix clustering
+        # Group genes by name prefix to capture gene families (e.g., ZNF, ZSCAN, TNF, etc.)
+        gene_to_prefix = {}
+        
+        for idx in all_indices:
+            candidate = candidates[idx]
+            gene = candidate.get('gene') or candidate.get('gene_a')
+            if gene:
+                # Extract prefix: typically first 3-4 letters before numbers
+                # This captures gene families like ZNF, ZSCAN, TNF, IL, etc.
+                prefix = ''.join([c for c in gene if not c.isdigit()])[:4]
+                if len(prefix) >= 2:
+                    gene_to_prefix[idx] = f"family_{prefix}"
+                else:
+                    gene_to_prefix[idx] = f"singleton_{idx}"
+            else:
+                gene_to_prefix[idx] = f"singleton_{idx}"
+        
+        # Create clusters based on prefix
+        for idx, prefix in gene_to_prefix.items():
+            candidate_to_cluster[idx] = prefix
+            clusters[prefix].append(idx)
+    
+    # Compute cluster statistics (empirical Bayes priors)
+    cluster_successes = defaultdict(int)
+    cluster_trials = defaultdict(int)
+    
+    for h in history:
+        idx = h['candidate_index']
+        cluster_id = candidate_to_cluster[idx]
+        cluster_trials[cluster_id] += 1
+        if h.get('hit') == 1:
+            cluster_successes[cluster_id] += 1
+    
+    # Compute global prior from all history
+    total_hits = sum(1 for h in history if h.get('hit') == 1)
+    global_alpha = total_hits + 1
+    global_beta = len(history) - total_hits + 1
+    
+    # For each cluster, compute posterior parameters
+    cluster_alpha = {}
+    cluster_beta = {}
+    
+    for cluster_id in clusters:
+        successes = cluster_successes.get(cluster_id, 0)
+        trials = cluster_trials.get(cluster_id, 0)
+        
+        # Use global prior with cluster observations
+        # This is empirical Bayes: use global distribution as prior
+        cluster_alpha[cluster_id] = successes + global_alpha
+        cluster_beta[cluster_id] = (trials - successes) + global_beta
+    
+    # For candidates with direct observations, compute posterior
+    candidate_alpha = {}
+    candidate_beta = {}
+    
+    for h in history:
+        idx = h['candidate_index']
+        hit = h.get('hit', 0)
+        cluster_id = candidate_to_cluster[idx]
+        
+        # Start with cluster prior, update with direct observation
+        candidate_alpha[idx] = hit + cluster_alpha[cluster_id]
+        candidate_beta[idx] = (1 - hit) + cluster_beta[cluster_id]
+    
+    # Thompson Sampling: sample theta for each candidate and select top ones
+    sampled_probs = {}
+    
+    for idx in available:
+        cluster_id = candidate_to_cluster[idx]
+        
+        if idx in candidate_alpha:
+            # Candidate has been observed, use its posterior
+            alpha = candidate_alpha[idx]
+            beta = candidate_beta[idx]
+        else:
+            # Candidate not observed, use cluster posterior
+            alpha = cluster_alpha[cluster_id]
+            beta = cluster_beta[cluster_id]
+        
+        # Sample from Beta distribution
+        sampled_probs[idx] = np.random.beta(alpha, beta)
+    
+    # Select top candidates by sampled probability
+    sorted_by_sample = sorted(available, key=lambda x: sampled_probs[x], reverse=True)
+    selected_indices = sorted_by_sample[:batch_size]
+    
+    return selected_indices
```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -0,0 +1,2233 @@
+{
+  "task": "perturb-genes-brief",
+  "data_name": "Sanchez21_down",
+  "measurement": "the change in tau protein level compared to the non-targeting control, using a total tau antibody",
+  "task_prompt": {
+    "Task": "identify genes that, when knocked out, decrease expression of endogenous tau protein levels in neurons",
+    "Measurement": "the change in tau protein level compared to the non-targeting control, using a total tau antibody"
+  },
+  "metrics": {
+    "test": {
+      "pool_size": 18469,
+      "rounds": 1,
+      "executed_rounds": 1,
+      "batch_size": 128,
+      "seed": 42,
+      "baseline_total_queries": 0,
+      "baseline_total_hits": 0,
+      "delta_queries": 128,
+      "delta_hits": 5,
+      "total_queries": 128,
+      "total_hits": 5,
+      "top_k": 924,
+      "hit_curve": {
+        "queries": [
+          0,
+          128
+        ],
+        "hits": [
+          0,
+          5
+        ]
+      },
+      "auc": 320.0,
+      "auc_normalized": 0.0027056277056277055,
+      "ncg": 0.1683378563733971,
+      "round_details": [
+        {
+          "round": 0,
+          "selected_count": 128,
+          "hits": 5,
+          "cumulative_hits": 5,
+          "precision_at_batch": 0.0390625,
+          "selected": [
+            "CUL1",
+            "APBB1IP",
+            "MAP2K5",
+            "KLF6",
+            "IKBKG",
+            "EFNA1",
+            "COX7A1",
+            "ZHX2",
+            "CHADL",
+            "SDAD1",
+            "ARMCX3",
+            "ARHGEF35",
+            "CLEC5A",
+            "IBSP",
+            "ITPR1",
+            "TRAM2",
+            "APOL3",
+            "ZNF85",
+            "GTF2E2",
+            "ZFYVE16",
+            "SCAND1",
+            "IFITM5",
+            "SMIM4",
+            "MAVS",
+            "ACTN4",
+            "FAM45A",
+            "SDPR",
+            "PALLD",
+            "MAT1A",
+            "FAM150A",
+            "HSBP1",
+            "OTOA",
+            "COX4I1",
+            "CLDN7",
+            "PRTN3",
+            "CNKSR1",
+            "PLA2G4C",
+            "PCDHA10",
+            "LPPR5",
+            "BBS2",
+            "SPRED3",
+            "WRN",
+            "DHRS3",
+            "PRR5L",
+            "CDCA8",
+            "ZNF426",
+            "MRPL13",
+            "PLIN2",
+            "GPR107",
+            "CCDC178",
+            "BFAR",
+            "INSL6",
+            "MMP3",
+            "CDIPT",
+            "ITPRIPL2",
+            "COPRS",
+            "PSAP",
+            "MATK",
+            "SON",
+            "POLA2",
+            "FASLG",
+            "PPP1R12B",
+            "PIGA",
+            "HK1",
+            "LRRC47",
+            "CCDC84",
+            "FN1",
+            "WDR87",
+            "KLF3",
+            "FBP1",
+            "SRSF6",
+            "PRSS41",
+            "LVRN",
+            "ZNF646",
+            "IDUA",
+            "NUDT12",
+            "C2CD2L",
+            "IQCF2",
+            "ARPC1A",
+            "NLGN2",
+            "RGS20",
+            "LRRC8B",
+            "CATSPERB",
+            "HMGN2",
+            "NKAP",
+            "HORMAD2",
+            "TMX1",
+            "RBM39",
+            "SPNS3",
+            "ELK1",
+            "LRFN4",
+            "EFNA4",
+            "KLK15",
+            "ZNF862",
+            "YKT6",
+            "LOC101060179",
+            "SFN",
+            "RFC3",
+            "PLOD1",
+            "IDH2",
+            "EDIL3",
+            "TRNP1",
+            "TMEM189",
+            "CISD1",
+            "BLVRA",
+            "CTCFL",
+            "F8A2",
+            "FAM49B",
+            "SDCCAG8",
+            "CAMSAP3",
+            "PTPN6",
+            "PSMD1",
+            "STX3",
+            "VN1R1",
+            "KRTAP2-4",
+            "ZNF486",
+            "ADRA2B",
+            "CYP2C8",
+            "XCL1",
+            "LRRC41",
+            "PAK7",
+            "CUL9",
+            "MRPL23",
+            "SLC10A6",
+            "FAM209B",
+            "SOS1",
+            "ABRA",
+            "LOC730183"
+          ],
+          "selected_scores": [
+            -0.440718299,
+            -0.211908354,
+            -0.453119592,
+            -4.965011117,
+            -1.083120102,
+            -0.482325554,
+            -0.426778306,
+            -0.572145006,
+            -0.600054381,
+            -1.638094938,
+            -1.479928967,
+            -0.531641773,
+            -2.501769779,
+            -0.53460571,
+            -1.655053509,
+            -0.316263145,
+            -1.841883456,
+            -0.467002565,
+            -1.382644681,
+            -0.349429341,
+            -0.338453236,
+            -0.303647301,
+            -1.12269276,
+            -0.676953445,
+            -3.015036203,
+            -0.355781568,
+            -0.567475521,
+            -0.233841029,
+            -0.115840676,
+            -0.761357564,
+            -0.507730569,
+            -0.727924428,
+            -0.799337128,
+            -0.853079197,
+            -1.414528018,
+            -0.624452994,
+            -0.37051967,
+            -1.103645237,
+            -0.528293503,
+            -0.626249194,
+            -0.538715688,
+            -1.361523575,
+            -0.493907098,
+            -0.359608657,
+            -0.319706721,
+            -1.665457326,
+            -1.108543714,
+            -1.283785665,
+            -0.483560745,
+            -0.168391389,
+            -0.212794819,
+            -1.01708101,
+            -1.555198412,
+            -3.846843544,
+            -0.314854751,
+            -0.687615875,
+            -0.887118123,
+            -1.785320636,
+            -1.11090559,
+            -1.474057418,
+            -0.454534112,
+            -0.473458847,
+            -0.353922365,
+            -1.169893979,
+            -1.080713719,
+            -0.463768342,
+            -0.893653613,
+            -0.500746844,
+            -0.05541296,
+            -2.292532726,
+            -1.065641167,
+            -0.458249888,
+            -0.248697989,
+            -1.723707673,
+            -1.248742525,
+            -0.606074539,
+            -1.616315535,
+            -0.625833814,
+            -1.887446516,
+            -0.760030351,
+            -0.790477636,
+            -1.498557032,
+            -0.45372378,
+            -1.619798825,
+            -1.139585963,
+            -1.069497046,
+            -1.000614035,
+            -0.600012888,
+            -0.990899065,
+            -0.512726259,
+            -1.179428663,
+            -0.979729795,
+            -0.686840974,
+            -0.625917622,
+            -1.421392615,
+            -1.585646831,
+            -0.312904766,
+            -1.139817189,
+            -0.556111904,
+            -1.445795344,
+            -0.450441631,
+            -0.520950282,
+            -1.158650374,
+            -0.544454627,
+            -0.748603479,
+            -0.06859385,
+            -0.694079177,
+            -0.173578048,
+            -0.185874668,
+            -0.899583631,
+            -0.59555894,
+            -0.547705879,
+            -1.129825101,
+            -0.480012617,
+            -0.569548136,
+            -1.087354143,
+            -0.449956719,
+            -0.530776837,
+            -0.49094761,
+            -0.60240636,
+            -1.725716417,
+            -0.772827818,
+            -1.783244708,
+            -0.83255635,
+            -0.313176705,
+            -1.076033352,
+            -0.909825102,
+            -0.61144655
+          ],
+          "selected_hits": [
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
+            0
+          ]
+        }
+      ],
+      "queried_records": [
+        {
+          "candidate_index": 3648,
+          "gene": "CUL1",
+          "score": -0.440718299,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 819,
+          "gene": "APBB1IP",
+          "score": -0.211908354,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9012,
+          "gene": "MAP2K5",
+          "score": -0.453119592,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8024,
+          "gene": "KLF6",
+          "score": -4.965011117,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 7314,
+          "gene": "IKBKG",
+          "score": -1.083120102,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4572,
+          "gene": "EFNA1",
+          "score": -0.482325554,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3358,
+          "gene": "COX7A1",
+          "score": -0.426778306,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17870,
+          "gene": "ZHX2",
+          "score": -0.572145006,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2848,
+          "gene": "CHADL",
+          "score": -0.600054381,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13825,
+          "gene": "SDAD1",
+          "score": -1.638094938,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1041,
+          "gene": "ARMCX3",
+          "score": -1.479928967,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 976,
+          "gene": "ARHGEF35",
+          "score": -0.531641773,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3070,
+          "gene": "CLEC5A",
+          "score": -2.501769779,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 7164,
+          "gene": "IBSP",
+          "score": -0.53460571,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7623,
+          "gene": "ITPR1",
+          "score": -1.655053509,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16559,
+          "gene": "TRAM2",
+          "score": -0.316263145,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 869,
+          "gene": "APOL3",
+          "score": -1.841883456,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18390,
+          "gene": "ZNF85",
+          "score": -0.467002565,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6515,
+          "gene": "GTF2E2",
+          "score": -1.382644681,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17856,
+          "gene": "ZFYVE16",
+          "score": -0.349429341,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13746,
+          "gene": "SCAND1",
+          "score": -0.338453236,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7223,
+          "gene": "IFITM5",
+          "score": -0.303647301,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14719,
+          "gene": "SMIM4",
+          "score": -1.12269276,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9115,
+          "gene": "MAVS",
+          "score": -0.676953445,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 212,
+          "gene": "ACTN4",
+          "score": -3.015036203,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 5231,
+          "gene": "FAM45A",
+          "score": -0.355781568,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13848,
+          "gene": "SDPR",
+          "score": -0.567475521,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11149,
+          "gene": "PALLD",
+          "score": -0.233841029,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9105,
+          "gene": "MAT1A",
+          "score": -0.115840676,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5094,
+          "gene": "FAM150A",
+          "score": -0.761357564,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7055,
+          "gene": "HSBP1",
+          "score": -0.507730569,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11029,
+          "gene": "OTOA",
+          "score": -0.727924428,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3349,
+          "gene": "COX4I1",
+          "score": -0.799337128,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3039,
+          "gene": "CLDN7",
+          "score": -0.853079197,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12449,
+          "gene": "PRTN3",
+          "score": -1.414528018,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3169,
+          "gene": "CNKSR1",
+          "score": -0.624452994,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11763,
+          "gene": "PLA2G4C",
+          "score": -0.37051967,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11270,
+          "gene": "PCDHA10",
+          "score": -1.103645237,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8667,
+          "gene": "LPPR5",
+          "score": -0.528293503,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1423,
+          "gene": "BBS2",
+          "score": -0.626249194,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15054,
+          "gene": "SPRED3",
+          "score": -0.538715688,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17571,
+          "gene": "WRN",
+          "score": -1.361523575,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4090,
+          "gene": "DHRS3",
+          "score": -0.493907098,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12403,
+          "gene": "PRR5L",
+          "score": -0.359608657,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2582,
+          "gene": "CDCA8",
+          "score": -0.319706721,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18089,
+          "gene": "ZNF426",
+          "score": -1.665457326,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9606,
+          "gene": "MRPL13",
+          "score": -1.108543714,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11850,
+          "gene": "PLIN2",
+          "score": -1.283785665,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6300,
+          "gene": "GPR107",
+          "score": -0.483560745,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2279,
+          "gene": "CCDC178",
+          "score": -0.168391389,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1501,
+          "gene": "BFAR",
+          "score": -0.212794819,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7467,
+          "gene": "INSL6",
+          "score": -1.01708101,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9482,
+          "gene": "MMP3",
+          "score": -1.555198412,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2614,
+          "gene": "CDIPT",
+          "score": -3.846843544,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 7628,
+          "gene": "ITPRIPL2",
+          "score": -0.314854751,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3309,
+          "gene": "COPRS",
+          "score": -0.687615875,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12455,
+          "gene": "PSAP",
+          "score": -0.887118123,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9108,
+          "gene": "MATK",
+          "score": -1.785320636,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14857,
+          "gene": "SON",
+          "score": -1.11090559,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11954,
+          "gene": "POLA2",
+          "score": -1.474057418,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5329,
+          "gene": "FASLG",
+          "score": -0.454534112,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12130,
+          "gene": "PPP1R12B",
+          "score": -0.473458847,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11641,
+          "gene": "PIGA",
+          "score": -0.353922365,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6865,
+          "gene": "HK1",
+          "score": -1.169893979,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8748,
+          "gene": "LRRC47",
+          "score": -1.080713719,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2339,
+          "gene": "CCDC84",
+          "score": -0.463768342,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5607,
+          "gene": "FN1",
+          "score": -0.893653613,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17502,
+          "gene": "WDR87",
+          "score": -0.500746844,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8021,
+          "gene": "KLF3",
+          "score": -0.05541296,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5354,
+          "gene": "FBP1",
+          "score": -2.292532726,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 15147,
+          "gene": "SRSF6",
+          "score": -1.065641167,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12433,
+          "gene": "PRSS41",
+          "score": -0.458249888,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8845,
+          "gene": "LVRN",
+          "score": -0.248697989,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18250,
+          "gene": "ZNF646",
+          "score": -1.723707673,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7196,
+          "gene": "IDUA",
+          "score": -1.248742525,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10626,
+          "gene": "NUDT12",
+          "score": -0.606074539,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1832,
+          "gene": "C2CD2L",
+          "score": -1.616315535,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7505,
+          "gene": "IQCF2",
+          "score": -0.625833814,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1051,
+          "gene": "ARPC1A",
+          "score": -1.887446516,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10336,
+          "gene": "NLGN2",
+          "score": -0.760030351,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13145,
+          "gene": "RGS20",
+          "score": -0.790477636,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8773,
+          "gene": "LRRC8B",
+          "score": -1.498557032,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2168,
+          "gene": "CATSPERB",
+          "score": -0.45372378,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6913,
+          "gene": "HMGN2",
+          "score": -1.619798825,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10311,
+          "gene": "NKAP",
+          "score": -1.139585963,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6967,
+          "gene": "HORMAD2",
+          "score": -1.069497046,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16358,
+          "gene": "TMX1",
+          "score": -1.000614035,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12964,
+          "gene": "RBM39",
+          "score": -0.600012888,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15035,
+          "gene": "SPNS3",
+          "score": -0.990899065,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4681,
+          "gene": "ELK1",
+          "score": -0.512726259,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8679,
+          "gene": "LRFN4",
+          "score": -1.179428663,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4575,
+          "gene": "EFNA4",
+          "score": -0.979729795,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8081,
+          "gene": "KLK15",
+          "score": -0.686840974,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18394,
+          "gene": "ZNF862",
+          "score": -0.625917622,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17661,
+          "gene": "YKT6",
+          "score": -1.421392615,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8609,
+          "gene": "LOC101060179",
+          "score": -1.585646831,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14038,
+          "gene": "SFN",
+          "score": -0.312904766,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13087,
+          "gene": "RFC3",
+          "score": -1.139817189,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11861,
+          "gene": "PLOD1",
+          "score": -0.556111904,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7186,
+          "gene": "IDH2",
+          "score": -1.445795344,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4532,
+          "gene": "EDIL3",
+          "score": -0.450441631,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16696,
+          "gene": "TRNP1",
+          "score": -0.520950282,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16171,
+          "gene": "TMEM189",
+          "score": -1.158650374,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2978,
+          "gene": "CISD1",
+          "score": -0.544454627,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1543,
+          "gene": "BLVRA",
+          "score": -0.748603479,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3592,
+          "gene": "CTCFL",
+          "score": -0.06859385,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5008,
+          "gene": "F8A2",
+          "score": -0.694079177,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5242,
+          "gene": "FAM49B",
+          "score": -0.173578048,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13833,
+          "gene": "SDCCAG8",
+          "score": -0.185874668,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2081,
+          "gene": "CAMSAP3",
+          "score": -0.899583631,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12608,
+          "gene": "PTPN6",
+          "score": -0.59555894,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12504,
+          "gene": "PSMD1",
+          "score": -0.547705879,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15337,
+          "gene": "STX3",
+          "score": -1.129825101,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17338,
+          "gene": "VN1R1",
+          "score": -0.480012617,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8238,
+          "gene": "KRTAP2-4",
+          "score": -0.569548136,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18128,
+          "gene": "ZNF486",
+          "score": -1.087354143,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 376,
+          "gene": "ADRA2B",
+          "score": -0.449956719,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3753,
+          "gene": "CYP2C8",
+          "score": -0.530776837,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17595,
+          "gene": "XCL1",
+          "score": -0.49094761,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8743,
+          "gene": "LRRC41",
+          "score": -0.60240636,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11146,
+          "gene": "PAK7",
+          "score": -1.725716417,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3655,
+          "gene": "CUL9",
+          "score": -0.772827818,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9617,
+          "gene": "MRPL23",
+          "score": -1.783244708,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14246,
+          "gene": "SLC10A6",
+          "score": -0.83255635,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5182,
+          "gene": "FAM209B",
+          "score": -0.313176705,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14867,
+          "gene": "SOS1",
+          "score": -1.076033352,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 106,
+          "gene": "ABRA",
+          "score": -0.909825102,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8630,
+          "gene": "LOC730183",
+          "score": -0.61144655,
+          "hit": 0,
+          "round": 0
+        }
+      ],
+      "queried_history": [
+        {
+          "candidate_index": 3648,
+          "gene": "CUL1",
+          "score": -0.440718299,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 819,
+          "gene": "APBB1IP",
+          "score": -0.211908354,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9012,
+          "gene": "MAP2K5",
+          "score": -0.453119592,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8024,
+          "gene": "KLF6",
+          "score": -4.965011117,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 7314,
+          "gene": "IKBKG",
+          "score": -1.083120102,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4572,
+          "gene": "EFNA1",
+          "score": -0.482325554,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3358,
+          "gene": "COX7A1",
+          "score": -0.426778306,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17870,
+          "gene": "ZHX2",
+          "score": -0.572145006,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2848,
+          "gene": "CHADL",
+          "score": -0.600054381,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13825,
+          "gene": "SDAD1",
+          "score": -1.638094938,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1041,
+          "gene": "ARMCX3",
+          "score": -1.479928967,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 976,
+          "gene": "ARHGEF35",
+          "score": -0.531641773,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3070,
+          "gene": "CLEC5A",
+          "score": -2.501769779,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 7164,
+          "gene": "IBSP",
+          "score": -0.53460571,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7623,
+          "gene": "ITPR1",
+          "score": -1.655053509,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16559,
+          "gene": "TRAM2",
+          "score": -0.316263145,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 869,
+          "gene": "APOL3",
+          "score": -1.841883456,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18390,
+          "gene": "ZNF85",
+          "score": -0.467002565,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6515,
+          "gene": "GTF2E2",
+          "score": -1.382644681,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17856,
+          "gene": "ZFYVE16",
+          "score": -0.349429341,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13746,
+          "gene": "SCAND1",
+          "score": -0.338453236,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7223,
+          "gene": "IFITM5",
+          "score": -0.303647301,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14719,
+          "gene": "SMIM4",
+          "score": -1.12269276,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9115,
+          "gene": "MAVS",
+          "score": -0.676953445,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 212,
+          "gene": "ACTN4",
+          "score": -3.015036203,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 5231,
+          "gene": "FAM45A",
+          "score": -0.355781568,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13848,
+          "gene": "SDPR",
+          "score": -0.567475521,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11149,
+          "gene": "PALLD",
+          "score": -0.233841029,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9105,
+          "gene": "MAT1A",
+          "score": -0.115840676,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5094,
+          "gene": "FAM150A",
+          "score": -0.761357564,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7055,
+          "gene": "HSBP1",
+          "score": -0.507730569,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11029,
+          "gene": "OTOA",
+          "score": -0.727924428,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3349,
+          "gene": "COX4I1",
+          "score": -0.799337128,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3039,
+          "gene": "CLDN7",
+          "score": -0.853079197,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12449,
+          "gene": "PRTN3",
+          "score": -1.414528018,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3169,
+          "gene": "CNKSR1",
+          "score": -0.624452994,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11763,
+          "gene": "PLA2G4C",
+          "score": -0.37051967,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11270,
+          "gene": "PCDHA10",
+          "score": -1.103645237,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8667,
+          "gene": "LPPR5",
+          "score": -0.528293503,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1423,
+          "gene": "BBS2",
+          "score": -0.626249194,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15054,
+          "gene": "SPRED3",
+          "score": -0.538715688,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17571,
+          "gene": "WRN",
+          "score": -1.361523575,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4090,
+          "gene": "DHRS3",
+          "score": -0.493907098,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12403,
+          "gene": "PRR5L",
+          "score": -0.359608657,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2582,
+          "gene": "CDCA8",
+          "score": -0.319706721,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18089,
+          "gene": "ZNF426",
+          "score": -1.665457326,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9606,
+          "gene": "MRPL13",
+          "score": -1.108543714,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11850,
+          "gene": "PLIN2",
+          "score": -1.283785665,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6300,
+          "gene": "GPR107",
+          "score": -0.483560745,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2279,
+          "gene": "CCDC178",
+          "score": -0.168391389,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1501,
+          "gene": "BFAR",
+          "score": -0.212794819,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7467,
+          "gene": "INSL6",
+          "score": -1.01708101,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9482,
+          "gene": "MMP3",
+          "score": -1.555198412,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2614,
+          "gene": "CDIPT",
+          "score": -3.846843544,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 7628,
+          "gene": "ITPRIPL2",
+          "score": -0.314854751,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3309,
+          "gene": "COPRS",
+          "score": -0.687615875,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12455,
+          "gene": "PSAP",
+          "score": -0.887118123,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9108,
+          "gene": "MATK",
+          "score": -1.785320636,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14857,
+          "gene": "SON",
+          "score": -1.11090559,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11954,
+          "gene": "POLA2",
+          "score": -1.474057418,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5329,
+          "gene": "FASLG",
+          "score": -0.454534112,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12130,
+          "gene": "PPP1R12B",
+          "score": -0.473458847,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11641,
+          "gene": "PIGA",
+          "score": -0.353922365,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6865,
+          "gene": "HK1",
+          "score": -1.169893979,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8748,
+          "gene": "LRRC47",
+          "score": -1.080713719,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2339,
+          "gene": "CCDC84",
+          "score": -0.463768342,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5607,
+          "gene": "FN1",
+          "score": -0.893653613,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17502,
+          "gene": "WDR87",
+          "score": -0.500746844,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8021,
+          "gene": "KLF3",
+          "score": -0.05541296,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5354,
+          "gene": "FBP1",
+          "score": -2.292532726,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 15147,
+          "gene": "SRSF6",
+          "score": -1.065641167,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12433,
+          "gene": "PRSS41",
+          "score": -0.458249888,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8845,
+          "gene": "LVRN",
+          "score": -0.248697989,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18250,
+          "gene": "ZNF646",
+          "score": -1.723707673,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7196,
+          "gene": "IDUA",
+          "score": -1.248742525,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10626,
+          "gene": "NUDT12",
+          "score": -0.606074539,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1832,
+          "gene": "C2CD2L",
+          "score": -1.616315535,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7505,
+          "gene": "IQCF2",
+          "score": -0.625833814,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1051,
+          "gene": "ARPC1A",
+          "score": -1.887446516,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10336,
+          "gene": "NLGN2",
+          "score": -0.760030351,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13145,
+          "gene": "RGS20",
+          "score": -0.790477636,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8773,
+          "gene": "LRRC8B",
+          "score": -1.498557032,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2168,
+          "gene": "CATSPERB",
+          "score": -0.45372378,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6913,
+          "gene": "HMGN2",
+          "score": -1.619798825,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10311,
+          "gene": "NKAP",
+          "score": -1.139585963,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6967,
+          "gene": "HORMAD2",
+          "score": -1.069497046,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16358,
+          "gene": "TMX1",
+          "score": -1.000614035,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12964,
+          "gene": "RBM39",
+          "score": -0.600012888,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15035,
+          "gene": "SPNS3",
+          "score": -0.990899065,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4681,
+          "gene": "ELK1",
+          "score": -0.512726259,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8679,
+          "gene": "LRFN4",
+          "score": -1.179428663,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4575,
+          "gene": "EFNA4",
+          "score": -0.979729795,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8081,
+          "gene": "KLK15",
+          "score": -0.686840974,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18394,
+          "gene": "ZNF862",
+          "score": -0.625917622,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17661,
+          "gene": "YKT6",
+          "score": -1.421392615,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8609,
+          "gene": "LOC101060179",
+          "score": -1.585646831,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14038,
+          "gene": "SFN",
+          "score": -0.312904766,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13087,
+          "gene": "RFC3",
+          "score": -1.139817189,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11861,
+          "gene": "PLOD1",
+          "score": -0.556111904,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7186,
+          "gene": "IDH2",
+          "score": -1.445795344,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4532,
+          "gene": "EDIL3",
+          "score": -0.450441631,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16696,
+          "gene": "TRNP1",
+          "score": -0.520950282,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16171,
+          "gene": "TMEM189",
+          "score": -1.158650374,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2978,
+          "gene": "CISD1",
+          "score": -0.544454627,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1543,
+          "gene": "BLVRA",
+          "score": -0.748603479,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3592,
+          "gene": "CTCFL",
+          "score": -0.06859385,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5008,
+          "gene": "F8A2",
+          "score": -0.694079177,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5242,
+          "gene": "FAM49B",
+          "score": -0.173578048,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13833,
+          "gene": "SDCCAG8",
+          "score": -0.185874668,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2081,
+          "gene": "CAMSAP3",
+          "score": -0.899583631,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12608,
+          "gene": "PTPN6",
+          "score": -0.59555894,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12504,
+          "gene": "PSMD1",
+          "score": -0.547705879,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15337,
+          "gene": "STX3",
+          "score": -1.129825101,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17338,
+          "gene": "VN1R1",
+          "score": -0.480012617,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8238,
+          "gene": "KRTAP2-4",
+          "score": -0.569548136,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18128,
+          "gene": "ZNF486",
+          "score": -1.087354143,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 376,
+          "gene": "ADRA2B",
+          "score": -0.449956719,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3753,
+          "gene": "CYP2C8",
+          "score": -0.530776837,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17595,
+          "gene": "XCL1",
+          "score": -0.49094761,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8743,
+          "gene": "LRRC41",
+          "score": -0.60240636,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11146,
+          "gene": "PAK7",
+          "score": -1.725716417,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3655,
+          "gene": "CUL9",
+          "score": -0.772827818,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9617,
+          "gene": "MRPL23",
+          "score": -1.783244708,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14246,
+          "gene": "SLC10A6",
+          "score": -0.83255635,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5182,
+          "gene": "FAM209B",
+          "score": -0.313176705,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14867,
+          "gene": "SOS1",
+          "score": -1.076033352,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 106,
+          "gene": "ABRA",
+          "score": -0.909825102,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8630,
+          "gene": "LOC730183",
+          "score": -0.61144655,
+          "hit": 0,
+          "round": 0
+        }
+      ]
+    }
+  }
+}
```
