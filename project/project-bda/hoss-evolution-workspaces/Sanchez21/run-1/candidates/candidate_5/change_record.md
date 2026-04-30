# Change Record — candidate_5

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21/run-1/best/current/harness
Generated at: 2026-04-30T06:57:16.539080

## Files Changed

- model.py: modified (added=137, deleted=128, delta=9)
- outputs/metrics.json: modified (added=2411, deleted=619, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -1,6 +1,7 @@
 from __future__ import annotations
 import random
 import numpy as np
+from collections import defaultdict
 
 def select(candidates, history, batch_size, seed) -> list[int]:
     """
@@ -27,12 +28,14 @@
     Output:
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
     
-    Strategy: Hybrid exploration-exploitation with adaptive sampling
-    - Early rounds: More random exploration to discover promising regions
-    - Later rounds: More exploitation of high-scoring candidates
-    - Always maintain diversity to avoid getting stuck in local optima
+    Strategy: Thompson Sampling with Gene Cluster Priors
+    - Uses Thompson Sampling (Bayesian bandit algorithm) for adaptive exploration-exploitation
+    - Models each candidate with Beta distribution based on hit observations
+    - Uses gene search to create clusters and share information via Bayesian priors
+    - Naturally balances exploration vs exploitation based on uncertainty
     """
     rng = random.Random(seed)
+    np.random.seed(seed)
     
     # Get already selected indices
     selected = set(h['candidate_index'] for h in history)
@@ -44,138 +47,144 @@
     if len(available) <= batch_size:
         return available
     
-    # Calculate exploration ratio based on history size
-    # More exploration in early rounds, more exploitation later
-    num_rounds = len(history) // batch_size if batch_size > 0 else 0
-    exploration_ratio = max(0.2, 0.9 - 0.15 * num_rounds)  # Starts at 90%, decreases to 20%
+    # If no history, use pure exploration
+    if len(history) == 0:
+        return rng.sample(available, batch_size)
     
-    # Separate exploration and exploitation
-    num_explore = int(batch_size * exploration_ratio)
-    num_exploit = batch_size - num_explore
+    # Check if hit information is available
+    has_hits = any('hit' in h for h in history)
     
-    # Exploration: random sampling from available candidates
-    explore_indices = rng.sample(available, min(num_explore, len(available)))
-    
-    # Exploitation: select based on historical scores
-    if len(history) > 0 and num_exploit > 0:
-        # Sort by absolute score to prioritize both negative and positive extremes
+    if not has_hits:
+        # Fall back to score-based selection using absolute scores
         sorted_history = sorted(history, key=lambda x: abs(x['score']), reverse=True)
-        
-        # Get top performers (highest absolute scores, 20% or at least 10)
         top_k = max(10, len(sorted_history) // 5)
         top_performers = [h['candidate_index'] for h in sorted_history[:top_k]]
         
-        # Find candidates similar to top performers if gene search is available
-        exploit_candidates = set()
-        remaining_avail = [i for i in available if i not in explore_indices]
+        # Sample from top performers
+        selected_indices = []
+        remaining = available.copy()
         
-        if len(remaining_avail) > 0:
-            # Try to use gene search if available
-            try:
-                import bda_tools
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
                 
-                # If hit information is available, prioritize actual hits over just high absolute scores
-                if any('hit' in h for h in history):
-                    hit_indices = [h['candidate_index'] for h in history if h.get('hit') == 1]
-                    if hit_indices:
-                        # Prioritize genes that are actual hits
-                        top_performers = hit_indices[:min(len(hit_indices), top_k)]
-                
-                # Sample more aggressively from top performers
-                num_to_sample = min(10, len(top_performers))
-                sampled_top = rng.sample(top_performers, num_to_sample)
-                
-                for top_idx in sampled_top:
-                    if len(exploit_candidates) >= num_exploit:
-                        break
-                    # Get gene name from candidate
-                    candidate = candidates[top_idx]
-                    gene = candidate.get('gene') or candidate.get('gene_a')
-                    if gene:
-                        try:
-                            # Search for similar genes with higher k
-                            similar = bda_tools.gene_search(gene, k=min(30, num_exploit * 2), diverse=False)
-                            for idx in similar:
-                                if idx in remaining_avail and idx not in exploit_candidates:
-                                    exploit_candidates.add(idx)
-                                    if len(exploit_candidates) >= num_exploit:
-                                        break
-                        except:
-                            pass
-                
-                # If we still need candidates, also try diverse search around top performers
-                if len(exploit_candidates) < num_exploit:
-                    for top_idx in sampled_top:
-                        if len(exploit_candidates) >= num_exploit:
-                            break
-                        candidate = candidates[top_idx]
-                        gene = candidate.get('gene') or candidate.get('gene_a')
-                        if gene:
-                            try:
-                                # Try diverse search for broader coverage
-                                diverse_similar = bda_tools.gene_search(gene, k=min(20, num_exploit - len(exploit_candidates)), diverse=True)
-                                for idx in diverse_similar:
-                                    if idx in remaining_avail and idx not in exploit_candidates:
-                                        exploit_candidates.add(idx)
-                                        if len(exploit_candidates) >= num_exploit:
-                                            break
-                            except:
-                                pass
-            except ImportError:
-                # bda_tools not available, fall back to other strategies
-                pass
-            
-            # If we still need more candidates, use weighted sampling based on score patterns
-            if len(exploit_candidates) < num_exploit:
-                needed = num_exploit - len(exploit_candidates)
-                
-                # Analyze score distribution to target both extremes
-                scores = [h['score'] for h in history]
-                if scores:
-                    # Target both very negative and near-zero regions
-                    extreme_negative = [h['candidate_index'] for h in history if h['score'] < -2.0]
-                    near_zero = [h['candidate_index'] for h in history if abs(h['score']) < 0.1]
-                    
-                    # Sample from both regions if available
-                    if extreme_negative and needed > 1:
-                        idx = rng.choice(extreme_negative)
-                        if idx in remaining_avail and idx not in exploit_candidates:
-                            exploit_candidates.add(idx)
-                            needed -= 1
-                    
-                    if near_zero and needed > 0:
-                        idx = rng.choice(near_zero)
-                        if idx in remaining_avail and idx not in exploit_candidates:
-                            exploit_candidates.add(idx)
-                            needed -= 1
-                
-                # Use stratified sampling for remaining diversity
-                if needed > 0:
-                    num_buckets = min(10, len(remaining_avail))
-                    bucket_size = len(remaining_avail) // num_buckets
-                    
-                    sampled = set()
-                    for bucket in range(num_buckets):
-                        if len(sampled) >= needed:
-                            break
-                        start = bucket * bucket_size
-                        end = start + bucket_size if bucket < num_buckets - 1 else len(remaining_avail)
-                        bucket_items = remaining_avail[start:end]
-                        if bucket_items:
-                            sampled.add(rng.choice(bucket_items))
-                    
-                    exploit_candidates.update(sampled)
+    except ImportError:
+        # No gene search available, use singleton clusters
+        for idx in all_indices:
+            cluster_id = f"singleton_{idx}"
+            candidate_to_cluster[idx] = cluster_id
+            clusters[cluster_id] = [idx]
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
         
-        selected_indices = list(explore_indices) + list(exploit_candidates)[:num_exploit]
-    else:
-        # Pure exploration if no history or no exploitation needed
-        selected_indices = explore_indices
+        # Use global prior with cluster observations
+        # This is empirical Bayes: use global distribution as prior
+        cluster_alpha[cluster_id] = successes + global_alpha
+        cluster_beta[cluster_id] = (trials - successes) + global_beta
     
-    # Ensure we have exactly batch_size indices
-    if len(selected_indices) < batch_size:
-        remaining = [i for i in available if i not in selected_indices]
-        needed = batch_size - len(selected_indices)
-        if remaining:
-            selected_indices.extend(rng.sample(remaining, min(needed, len(remaining))))
+    # For candidates with direct observations, compute posterior
+    candidate_alpha = {}
+    candidate_beta = {}
     
-    return selected_indices[:batch_size]
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
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18469,
-      "rounds": 4,
+      "rounds": 5,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 384,
-      "baseline_total_hits": 18,
+      "baseline_total_queries": 512,
+      "baseline_total_hits": 29,
       "delta_queries": 128,
-      "delta_hits": 11,
-      "total_queries": 512,
-      "total_hits": 29,
+      "delta_hits": 5,
+      "total_queries": 640,
+      "total_hits": 34,
       "top_k": 924,
       "hit_curve": {
         "queries": [
-          384,
-          512
+          512,
+          640
         ],
         "hits": [
-          18,
-          29
+          29,
+          34
         ]
       },
-      "auc": 3008.0,
-      "auc_normalized": 0.006358225108225108,
-      "ncg": 0.2690165741423913,
+      "auc": 4032.0,
+      "auc_normalized": 0.006818181818181818,
+      "ncg": 0.283009836354777,
       "round_details": [
         {
-          "round": 3,
+          "round": 4,
           "selected_count": 128,
-          "hits": 11,
-          "cumulative_hits": 29,
-          "precision_at_batch": 0.0859375,
+          "hits": 5,
+          "cumulative_hits": 34,
+          "precision_at_batch": 0.0390625,
           "selected": [
-            "MATN1",
-            "SERPINB8",
-            "TMOD3",
-            "LOC728763",
-            "CEP126",
-            "NDUFS1",
-            "PCNXL3",
-            "ANKRD35",
-            "CCPG1",
-            "TMEM220",
-            "ADORA3",
-            "DCAF4L1",
-            "MOGAT3",
-            "DDX42",
-            "NOP56",
-            "ATG4C",
-            "CCDC124",
-            "EDN2",
-            "MASP1",
-            "FAM19A5",
-            "HSD17B4",
-            "SLC24A4",
-            "CD53",
-            "SACM1L",
-            "EPB42",
-            "C7orf73",
-            "ARSB",
-            "FXYD5",
-            "ODF2",
-            "LETM1",
-            "POC1B-GALNT4",
-            "OAZ1",
-            "CMTM4",
-            "SCHIP1",
-            "CLCN2",
-            "ANKRD27",
-            "OS9",
-            "NUCB2",
-            "RBM23",
-            "ZC3H15",
-            "ZNF214",
-            "LIN52",
-            "CACFD1",
-            "TP53INP2",
-            "PSMD9",
-            "HPS6",
-            "PLA2G4B",
-            "FAM46D",
-            "ALG13",
-            "LCE1B",
-            "TSC22D1",
-            "SIPA1L1",
-            "MVK",
-            "HRASLS5",
-            "SEC61B",
-            "RASGRP3",
-            "RAB1B",
-            "PABPC5",
-            "KCNH3",
-            "SULT1A1",
-            "GNB2L1",
-            "BRF1",
-            "TRPV4",
-            "DRP2",
-            "CD163L1",
-            "MRPL37",
-            "SLAMF8",
-            "RPS20",
-            "CRISP2",
-            "ABI3",
-            "PPP2R5D",
-            "MIA3",
-            "STKLD1",
-            "SNAI3",
-            "HEY1",
-            "P2RX2",
-            "MAST4",
-            "KRT23",
-            "VWF",
-            "ITFG1",
-            "TREX1",
-            "ARGLU1",
-            "F9",
-            "ANO8",
-            "LTK",
-            "TMEM133",
-            "CNTN6",
-            "GAPT",
-            "IFIH1",
-            "CARD18",
-            "CLK1",
-            "CBL",
-            "DYNC2LI1",
-            "RHOV",
-            "FGFR4",
-            "CERS5",
-            "SPIN4",
-            "RETSAT",
-            "MFSD12",
-            "RANBP6",
-            "RPUSD3",
-            "PYHIN1",
-            "FGF11",
-            "YEATS4",
-            "ARL14",
-            "CCR7",
-            "OPRL1",
-            "SEPT9",
-            "KIAA0100",
-            "OR10G3",
-            "PRDM9",
-            "SMIM24",
-            "IFT52",
-            "RHOA",
-            "WDR48",
-            "ZNF432",
-            "ABCA3",
-            "SEC24D",
-            "ASCL1",
-            "TCEAL2",
-            "C7orf60",
-            "KDELR2",
-            "KBTBD3",
-            "ITGAE",
-            "CAMTA1",
-            "BTBD17",
-            "CHI3L2",
-            "PRY"
+            "RPN2",
+            "ZNF524",
+            "ANKRD26",
+            "C1QL4",
+            "ATG10",
+            "FDXACB1",
+            "NKPD1",
+            "LOC100129924",
+            "PPM1E",
+            "GUCA2B",
+            "RIN2",
+            "BCL7C",
+            "TOP1MT",
+            "ERO1L",
+            "EXOSC4",
+            "SDR42E1",
+            "DUSP3",
+            "TSNAXIP1",
+            "CATSPER1",
+            "HIST2H4A",
+            "PAPD5",
+            "MORF4L2",
+            "CMAS",
+            "CD70",
+            "LRRC69",
+            "PHF19",
+            "TRMT1",
+            "SLC27A6",
+            "PSIP1",
+            "FAM120A",
+            "GYPE",
+            "TFIP11",
+            "FERMT1",
+            "NTRK1",
+            "ZNF101",
+            "CTSC",
+            "OR6Y1",
+            "TPO",
+            "AKAP14",
+            "NPFFR1",
+            "GUCY2C",
+            "IPO4",
+            "CNOT11",
+            "IKZF1",
+            "ANKRD62",
+            "PPIC",
+            "STRN4",
+            "ADIPOR1",
+            "IL11",
+            "HMHA1",
+            "AKAP8L",
+            "ZNF146",
+            "PCDHGA11",
+            "ZNF766",
+            "ASB4",
+            "CXCL9",
+            "COMMD3",
+            "UPF2",
+            "IMPA2",
+            "SLC14A2",
+            "FAM153B",
+            "FTH1",
+            "FMNL2",
+            "CHRNA7",
+            "PPP1R16A",
+            "CUL4A",
+            "MAPRE3",
+            "TARS",
+            "UHRF1BP1L",
+            "IRX1",
+            "ITCH",
+            "PABPC1L2B",
+            "TRIM38",
+            "AGTR1",
+            "SOHLH2",
+            "TLE4",
+            "RHAG",
+            "KIF26B",
+            "INPP5K",
+            "PDE8B",
+            "C2orf73",
+            "GBP5",
+            "KCTD10",
+            "KBTBD7",
+            "DDI1",
+            "DRAM2",
+            "FYN",
+            "CPLX3",
+            "AFP",
+            "ZSWIM4",
+            "TRA2B",
+            "TUBB3",
+            "HIST1H2AC",
+            "STRN3",
+            "DKK3",
+            "TCEA2",
+            "DSG2",
+            "GATS",
+            "NMS",
+            "RFWD2",
+            "TMEM115",
+            "TEX35",
+            "TBX3",
+            "PTPN7",
+            "CD2AP",
+            "ADAMTS1",
+            "PSMB6",
+            "ALDH2",
+            "NFIA",
+            "MRAP2",
+            "TCHH",
+            "TMEM106A",
+            "POTEB",
+            "MAX",
+            "LIPN",
+            "USHBP1",
+            "TTC39C",
+            "CCZ1",
+            "MATN3",
+            "NLRP5",
+            "ZAR1",
+            "PCNP",
+            "FANCL",
+            "BVES",
+            "RPAP1",
+            "MEX3B",
+            "CYP4A11",
+            "C20orf27"
           ],
           "selected_scores": [
-            -0.4104380999999999,
-            -0.329490148,
-            -0.22175702600000002,
-            -1.1886534709999999,
-            -0.156549957,
-            -0.5231745529999999,
-            -1.567926415,
-            -0.519084251,
-            -0.461368483,
-            -1.182195947,
-            -1.2535028959999999,
-            -1.23915844,
-            -0.702892028,
-            -1.368088589,
-            -3.12504232,
-            -1.294710559,
-            -1.3287066109999999,
-            -0.223556442,
-            -0.966823482,
-            -1.176611027,
-            -0.9546285259999999,
-            -0.662405857,
-            -1.053278716,
-            -2.148767173,
-            -0.061137486,
-            -0.396462735,
-            -0.5009418520000001,
-            -0.33476787399999997,
-            -0.469909029,
-            -0.559237908,
-            -0.11615138300000001,
-            -0.32720166300000003,
-            -0.716024876,
-            -1.139779623,
-            -1.1597699479999999,
-            -0.7868462820000001,
-            -0.23046398,
-            -0.628037608,
-            -0.743159424,
-            -4.642818375,
-            -0.434667445,
-            -3.093945923,
-            -0.6513169289999999,
-            -0.47062887600000003,
-            -0.604428159,
-            -1.890446505,
-            -0.477295927,
-            -0.070973971,
-            -2.780068955,
-            -0.664128853,
-            -2.02432083,
-            -0.8523889179999999,
-            -0.33314050100000003,
-            -0.17696316399999998,
-            -0.732267441,
-            -2.396689074,
-            -0.590366287,
-            -0.775620894,
-            -0.504159483,
-            -1.1862740440000001,
-            -1.769044294,
-            -1.374109684,
-            -0.72425143,
-            -1.152236536,
-            -1.4734528830000002,
-            -2.2005796159999997,
-            -0.646016172,
-            -1.065640001,
-            -0.481033955,
-            -0.18754147399999999,
-            -0.370238175,
-            -0.6449656570000001,
-            -0.166186834,
-            -0.774750712,
-            -2.094411689,
-            -0.58233107,
-            -1.059639734,
-            -0.09050302199999999,
-            -0.584625911,
-            -1.19117938,
-            -0.342036268,
-            -3.2208133180000003,
-            -0.644513575,
-            -1.947826808,
-            -0.7503026909999999,
-            -2.072937505,
-            -0.812852122,
-            -0.663318773,
-            -0.5536093000000001,
-            -0.6228774029999999,
-            -0.270706545,
-            -0.204112658,
-            -0.47467650899999997,
-            -0.392412264,
-            -0.593319123,
-            -0.19005876800000002,
-            -0.023098108,
-            -1.03093522,
-            -3.015320243,
-            -0.542753612,
-            -1.2502314829999999,
-            -0.548085777,
-            -2.175442962,
-            -1.1739566909999999,
-            -0.496439061,
-            -0.32461639800000003,
-            -0.746379056,
-            -0.326716425,
-            -0.580674799,
-            -0.823717975,
-            -0.669017746,
-            -0.29737308100000004,
-            -1.4153385,
-            -2.9459395660000003,
-            -0.528011775,
-            -1.8124296130000002,
-            -0.21133955100000001,
-            -0.7292541159999999,
-            -0.18055578100000003,
-            -0.8765485590000001,
-            -0.546959614,
-            -0.487717731,
-            -1.066628225,
-            -0.215583203,
-            -0.456741119,
-            -0.126790438,
-            -0.885074315,
-            -0.83277222
+            -1.072642225,
+            -0.701245465,
+            -0.7000300979999999,
+            -0.921619408,
+            -1.389136745,
+            -1.4648971919999998,
+            -1.079146919,
+            -0.8757421479999999,
+            -1.567175107,
+            -0.585928335,
+            -0.5871104229999999,
+            -1.4200866419999998,
+            -1.262787231,
+            -0.44012297899999997,
+            -2.8849797789999996,
+            -0.39897536299999997,
+            -1.4338238840000002,
+            -1.167008766,
+            -0.219501516,
+            -1.216771716,
+            -0.09046830900000001,
+            -1.301956869,
+            -0.09473950099999999,
+            -0.954214553,
+            -0.522880595,
+            -1.467490089,
+            -0.786866135,
+            -0.549412566,
+            -0.342268356,
+            -3.939774678,
+            -1.4383159769999998,
+            -1.5623279330000002,
+            -0.711104238,
+            -1.145320792,
+            -0.45488637200000004,
+            -1.243525299,
+            -0.7966781690000001,
+            -0.40068333,
+            -0.7970176529999999,
+            -0.345893616,
+            -0.463074449,
+            -0.573281973,
+            -1.4087829530000002,
+            -0.328590812,
+            -0.445463528,
+            -0.8380380620000001,
+            -2.532463187,
+            -0.627363333,
+            -0.748475472,
+            -0.485296687,
+            -0.505764849,
+            -0.21671926,
+            -0.317556635,
+            -0.300786966,
+            -1.043560733,
+            -0.573437973,
+            -0.956465454,
+            -0.441269554,
+            -1.983105057,
+            -1.2126064140000001,
+            -2.6040197640000002,
+            -0.631323055,
+            -1.225692125,
+            -0.627056724,
+            -0.5026894679999999,
+            -0.798165942,
+            -2.60754938,
+            -0.512684126,
+            -0.53352791,
+            -0.380680081,
+            -0.92167761,
+            -0.9224545259999999,
+            -0.43126190299999995,
+            -0.594623295,
+            -1.658807138,
+            -1.476070148,
+            -0.204187578,
+            -0.132942002,
+            -0.400332564,
+            -0.281771261,
+            -0.661731399,
+            -1.4164563819999998,
+            -0.634082225,
+            -0.46124898799999997,
+            -0.358771214,
+            -0.939301191,
+            -0.553065424,
+            -0.822700098,
+            -0.172061842,
+            -0.842698985,
+            -0.8024864890000001,
+            -0.335623464,
+            -0.24827214399999997,
+            -0.736097775,
+            -0.9725016759999999,
+            -0.424226424,
+            -1.465331935,
+            -0.41898935200000004,
+            -2.195215852,
+            -2.345944742,
+            -2.480368085,
+            -1.061614066,
+            -0.138851181,
+            -0.433048772,
+            -1.110952407,
+            -0.499217543,
+            -0.553505129,
+            -0.205798622,
+            -1.357139567,
+            -1.9987967119999999,
+            -0.652392517,
+            -0.6247561389999999,
+            -1.212309898,
+            -0.18873263,
+            -0.775888713,
+            -0.615645307,
+            -0.981961396,
+            -0.531150152,
+            -0.6518451510000001,
+            -0.8361084759999999,
+            -0.068593917,
+            -1.563176744,
+            -0.6546992070000001,
+            -0.318176712,
+            -0.231945911,
+            -1.684934863,
+            -0.9190545790000001,
+            -0.5204385970000001
           ],
           "selected_hits": [
             0,
@@ -321,107 +321,107 @@
             0,
             0,
             0,
-            0,
-            0,
-            0,
-            0,
             1,
             0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
             1,
             0,
+            0,
+            0,
+            0,
+            0,
+            0,
             1,
             0,
             0,
             0,
             0,
             0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
             1,
-            1,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            1,
-            0,
-            0,
-            0,
-            1,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            1,
-            0,
-            1,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            1,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
             0,
             0,
             0,
@@ -3126,896 +3126,1792 @@
           "gene": "MATN1",
           "score": -0.4104380999999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13984,
           "gene": "SERPINB8",
           "score": -0.329490148,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16328,
           "gene": "TMOD3",
           "score": -0.22175702600000002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8629,
           "gene": "LOC728763",
           "score": -1.1886534709999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2744,
           "gene": "CEP126",
           "score": -0.156549957,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10158,
           "gene": "NDUFS1",
           "score": -0.5231745529999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11344,
           "gene": "PCNXL3",
           "score": -1.567926415,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 716,
           "gene": "ANKRD35",
           "score": -0.519084251,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2424,
           "gene": "CCPG1",
           "score": -0.461368483,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16204,
           "gene": "TMEM220",
           "score": -1.182195947,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 366,
           "gene": "ADORA3",
           "score": -1.2535028959999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3858,
           "gene": "DCAF4L1",
           "score": -1.23915844,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9513,
           "gene": "MOGAT3",
           "score": -0.702892028,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3954,
           "gene": "DDX42",
           "score": -1.368088589,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10418,
           "gene": "NOP56",
           "score": -3.12504232,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1190,
           "gene": "ATG4C",
           "score": -1.294710559,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2233,
           "gene": "CCDC124",
           "score": -1.3287066109999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4534,
           "gene": "EDN2",
           "score": -0.223556442,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9098,
           "gene": "MASP1",
           "score": -0.966823482,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5172,
           "gene": "FAM19A5",
           "score": -1.176611027,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7069,
           "gene": "HSD17B4",
           "score": -0.9546285259999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14340,
           "gene": "SLC24A4",
           "score": -0.662405857,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2513,
           "gene": "CD53",
           "score": -1.053278716,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13666,
           "gene": "SACM1L",
           "score": -2.148767173,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4794,
           "gene": "EPB42",
           "score": -0.061137486,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1912,
           "gene": "C7orf73",
           "score": -0.396462735,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1071,
           "gene": "ARSB",
           "score": -0.5009418520000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5777,
           "gene": "FXYD5",
           "score": -0.33476787399999997,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10738,
           "gene": "ODF2",
           "score": -0.469909029,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8436,
           "gene": "LETM1",
           "score": -0.559237908,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11941,
           "gene": "POC1B-GALNT4",
           "score": -0.11615138300000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10717,
           "gene": "OAZ1",
           "score": -0.32720166300000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3144,
           "gene": "CMTM4",
           "score": -0.716024876,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13775,
           "gene": "SCHIP1",
           "score": -1.139779623,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3010,
           "gene": "CLCN2",
           "score": -1.1597699479999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 704,
           "gene": "ANKRD27",
           "score": -0.7868462820000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10999,
           "gene": "OS9",
           "score": -0.23046398,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10617,
           "gene": "NUCB2",
           "score": -0.628037608,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12954,
           "gene": "RBM23",
           "score": -0.743159424,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17756,
           "gene": "ZC3H15",
           "score": -4.642818375,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17964,
           "gene": "ZNF214",
           "score": -0.434667445,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8515,
           "gene": "LIN52",
           "score": -3.093945923,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2000,
           "gene": "CACFD1",
           "score": -0.6513169289999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16487,
           "gene": "TP53INP2",
           "score": -0.47062887600000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12517,
           "gene": "PSMD9",
           "score": -0.604428159,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7024,
           "gene": "HPS6",
           "score": -1.890446505,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11762,
           "gene": "PLA2G4B",
           "score": -0.477295927,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5235,
           "gene": "FAM46D",
           "score": -0.070973971,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 560,
           "gene": "ALG13",
           "score": -2.780068955,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8363,
           "gene": "LCE1B",
           "score": -0.664128853,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16731,
           "gene": "TSC22D1",
           "score": -2.02432083,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14194,
           "gene": "SIPA1L1",
           "score": -0.8523889179999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9844,
           "gene": "MVK",
           "score": -0.33314050100000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7032,
           "gene": "HRASLS5",
           "score": -0.17696316399999998,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13880,
           "gene": "SEC61B",
           "score": -0.732267441,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12900,
           "gene": "RASGRP3",
           "score": -2.396689074,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12728,
           "gene": "RAB1B",
           "score": -0.590366287,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11107,
           "gene": "PABPC5",
           "score": -0.775620894,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7748,
           "gene": "KCNH3",
           "score": -0.504159483,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15367,
           "gene": "SULT1A1",
           "score": -1.1862740440000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6184,
           "gene": "GNB2L1",
           "score": -1.769044294,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1617,
           "gene": "BRF1",
           "score": -1.374109684,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16722,
           "gene": "TRPV4",
           "score": -0.72425143,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4376,
           "gene": "DRP2",
           "score": -1.152236536,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2458,
           "gene": "CD163L1",
           "score": -1.4734528830000002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9628,
           "gene": "MRPL37",
           "score": -2.2005796159999997,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14238,
           "gene": "SLAMF8",
           "score": -0.646016172,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13490,
           "gene": "RPS20",
           "score": -1.065640001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3465,
           "gene": "CRISP2",
           "score": -0.481033955,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 97,
           "gene": "ABI3",
           "score": -0.18754147399999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12181,
           "gene": "PPP2R5D",
           "score": -0.370238175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9363,
           "gene": "MIA3",
           "score": -0.6449656570000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15293,
           "gene": "STKLD1",
           "score": -0.166186834,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14759,
           "gene": "SNAI3",
           "score": -0.774750712,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6743,
           "gene": "HEY1",
           "score": -2.094411689,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11073,
           "gene": "P2RX2",
           "score": -0.58233107,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9103,
           "gene": "MAST4",
           "score": -1.059639734,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8149,
           "gene": "KRT23",
           "score": -0.09050302199999999,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17417,
           "gene": "VWF",
           "score": -0.584625911,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7573,
           "gene": "ITFG1",
           "score": -1.19117938,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16587,
           "gene": "TREX1",
           "score": -0.342036268,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 923,
           "gene": "ARGLU1",
           "score": -3.2208133180000003,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5010,
           "gene": "F9",
           "score": -0.644513575,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 756,
           "gene": "ANO8",
           "score": -1.947826808,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8833,
           "gene": "LTK",
           "score": -0.7503026909999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16109,
           "gene": "TMEM133",
           "score": -2.072937505,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3209,
           "gene": "CNTN6",
           "score": -0.812852122,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5889,
           "gene": "GAPT",
           "score": -0.663318773,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7213,
           "gene": "IFIH1",
           "score": -0.5536093000000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2121,
           "gene": "CARD18",
           "score": -0.6228774029999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3088,
           "gene": "CLK1",
           "score": -0.270706545,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2177,
           "gene": "CBL",
           "score": -0.204112658,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4461,
           "gene": "DYNC2LI1",
           "score": -0.47467650899999997,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13190,
           "gene": "RHOV",
           "score": -0.392412264,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5519,
           "gene": "FGFR4",
           "score": -0.593319123,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2786,
           "gene": "CERS5",
           "score": -0.19005876800000002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15015,
           "gene": "SPIN4",
           "score": -0.023098108,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13079,
           "gene": "RETSAT",
           "score": -1.03093522,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9330,
           "gene": "MFSD12",
           "score": -3.015320243,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12853,
           "gene": "RANBP6",
           "score": -0.542753612,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13524,
           "gene": "RPUSD3",
           "score": -1.2502314829999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12684,
           "gene": "PYHIN1",
           "score": -0.548085777,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5491,
           "gene": "FGF11",
           "score": -2.175442962,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17649,
           "gene": "YEATS4",
           "score": -1.1739566909999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1004,
           "gene": "ARL14",
           "score": -0.496439061,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2432,
           "gene": "CCR7",
           "score": -0.32461639800000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10796,
           "gene": "OPRL1",
           "score": -0.746379056,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13947,
           "gene": "SEPT9",
           "score": -0.326716425,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7872,
           "gene": "KIAA0100",
           "score": -0.580674799,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10804,
           "gene": "OR10G3",
           "score": -0.823717975,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12252,
           "gene": "PRDM9",
           "score": -0.669017746,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14717,
           "gene": "SMIM24",
           "score": -0.29737308100000004,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7260,
           "gene": "IFT52",
           "score": -1.4153385,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13175,
           "gene": "RHOA",
           "score": -2.9459395660000003,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17473,
           "gene": "WDR48",
           "score": -0.528011775,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18095,
           "gene": "ZNF432",
           "score": -1.8124296130000002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 35,
           "gene": "ABCA3",
           "score": -0.21133955100000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13875,
           "gene": "SEC24D",
           "score": -0.7292541159999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1116,
           "gene": "ASCL1",
           "score": -0.18055578100000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15694,
           "gene": "TCEAL2",
           "score": -0.8765485590000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1904,
           "gene": "C7orf60",
           "score": -0.546959614,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7836,
           "gene": "KDELR2",
           "score": -0.487717731,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7710,
           "gene": "KBTBD3",
           "score": -1.066628225,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7589,
           "gene": "ITGAE",
           "score": -0.215583203,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2082,
           "gene": "CAMTA1",
           "score": -0.456741119,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1653,
           "gene": "BTBD17",
           "score": -0.126790438,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2879,
           "gene": "CHI3L2",
           "score": -0.885074315,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12453,
           "gene": "PRY",
           "score": -0.83277222,
           "hit": 0,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 13463,
+          "gene": "RPN2",
+          "score": -1.072642225,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18154,
+          "gene": "ZNF524",
+          "score": -0.701245465,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 703,
+          "gene": "ANKRD26",
+          "score": -0.7000300979999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1803,
+          "gene": "C1QL4",
+          "score": -0.921619408,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1179,
+          "gene": "ATG10",
+          "score": -1.389136745,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5456,
+          "gene": "FDXACB1",
+          "score": -1.4648971919999998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10318,
+          "gene": "NKPD1",
+          "score": -1.079146919,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8580,
+          "gene": "LOC100129924",
+          "score": -0.8757421479999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12113,
+          "gene": "PPM1E",
+          "score": -1.567175107,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6548,
+          "gene": "GUCA2B",
+          "score": -0.585928335,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13219,
+          "gene": "RIN2",
+          "score": -0.5871104229999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1466,
+          "gene": "BCL7C",
+          "score": -1.4200866419999998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16460,
+          "gene": "TOP1MT",
+          "score": -1.262787231,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4883,
+          "gene": "ERO1L",
+          "score": -0.44012297899999997,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4972,
+          "gene": "EXOSC4",
+          "score": -2.8849797789999996,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 13851,
+          "gene": "SDR42E1",
+          "score": -0.39897536299999997,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4438,
+          "gene": "DUSP3",
+          "score": -1.4338238840000002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16755,
+          "gene": "TSNAXIP1",
+          "score": -1.167008766,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2164,
+          "gene": "CATSPER1",
+          "score": -0.219501516,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6855,
+          "gene": "HIST2H4A",
+          "score": -1.216771716,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11169,
+          "gene": "PAPD5",
+          "score": -0.09046830900000001,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 9524,
+          "gene": "MORF4L2",
+          "score": -1.301956869,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3131,
+          "gene": "CMAS",
+          "score": -0.09473950099999999,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 2523,
+          "gene": "CD70",
+          "score": -0.954214553,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8763,
+          "gene": "LRRC69",
+          "score": -0.522880595,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11578,
+          "gene": "PHF19",
+          "score": -1.467490089,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16678,
+          "gene": "TRMT1",
+          "score": -0.786866135,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14406,
+          "gene": "SLC27A6",
+          "score": -0.549412566,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12475,
+          "gene": "PSIP1",
+          "score": -0.342268356,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5059,
+          "gene": "FAM120A",
+          "score": -3.939774678,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 6568,
+          "gene": "GYPE",
+          "score": -1.4383159769999998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15852,
+          "gene": "TFIP11",
+          "score": -1.5623279330000002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5467,
+          "gene": "FERMT1",
+          "score": -0.711104238,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10604,
+          "gene": "NTRK1",
+          "score": -1.145320792,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17910,
+          "gene": "ZNF101",
+          "score": -0.45488637200000004,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3624,
+          "gene": "CTSC",
+          "score": -1.243525299,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10968,
+          "gene": "OR6Y1",
+          "score": -0.7966781690000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16515,
+          "gene": "TPO",
+          "score": -0.40068333,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 495,
+          "gene": "AKAP14",
+          "score": -0.7970176529999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10460,
+          "gene": "NPFFR1",
+          "score": -0.345893616,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6553,
+          "gene": "GUCY2C",
+          "score": -0.463074449,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7492,
+          "gene": "IPO4",
+          "score": -0.573281973,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3181,
+          "gene": "CNOT11",
+          "score": -1.4087829530000002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7315,
+          "gene": "IKZF1",
+          "score": -0.328590812,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 734,
+          "gene": "ANKRD62",
+          "score": -0.445463528,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12096,
+          "gene": "PPIC",
+          "score": -0.8380380620000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15322,
+          "gene": "STRN4",
+          "score": -2.532463187,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 353,
+          "gene": "ADIPOR1",
+          "score": -0.627363333,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7323,
+          "gene": "IL11",
+          "score": -0.748475472,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6919,
+          "gene": "HMHA1",
+          "score": -0.485296687,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 504,
+          "gene": "AKAP8L",
+          "score": -0.505764849,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17931,
+          "gene": "ZNF146",
+          "score": -0.21671926,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11302,
+          "gene": "PCDHGA11",
+          "score": -0.317556635,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18331,
+          "gene": "ZNF766",
+          "score": -0.300786966,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1107,
+          "gene": "ASB4",
+          "score": -1.043560733,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3684,
+          "gene": "CXCL9",
+          "score": -0.573437973,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3292,
+          "gene": "COMMD3",
+          "score": -0.956465454,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17146,
+          "gene": "UPF2",
+          "score": -0.441269554,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7418,
+          "gene": "IMPA2",
+          "score": -1.983105057,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14265,
+          "gene": "SLC14A2",
+          "score": -1.2126064140000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5099,
+          "gene": "FAM153B",
+          "score": -2.6040197640000002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5740,
+          "gene": "FTH1",
+          "score": -0.631323055,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5597,
+          "gene": "FMNL2",
+          "score": -1.225692125,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2928,
+          "gene": "CHRNA7",
+          "score": -0.627056724,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12140,
+          "gene": "PPP1R16A",
+          "score": -0.5026894679999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3651,
+          "gene": "CUL4A",
+          "score": -0.798165942,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9069,
+          "gene": "MAPRE3",
+          "score": -2.60754938,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15572,
+          "gene": "TARS",
+          "score": -0.512684126,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17109,
+          "gene": "UHRF1BP1L",
+          "score": -0.53352791,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7546,
+          "gene": "IRX1",
+          "score": -0.380680081,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7572,
+          "gene": "ITCH",
+          "score": -0.92167761,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11103,
+          "gene": "PABPC1L2B",
+          "score": -0.9224545259999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16623,
+          "gene": "TRIM38",
+          "score": -0.43126190299999995,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 444,
+          "gene": "AGTR1",
+          "score": -0.594623295,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14856,
+          "gene": "SOHLH2",
+          "score": -1.658807138,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16000,
+          "gene": "TLE4",
+          "score": -1.476070148,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13158,
+          "gene": "RHAG",
+          "score": -0.204187578,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7969,
+          "gene": "KIF26B",
+          "score": -0.132942002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7457,
+          "gene": "INPP5K",
+          "score": -0.400332564,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11406,
+          "gene": "PDE8B",
+          "score": -0.281771261,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1843,
+          "gene": "C2orf73",
+          "score": -0.661731399,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5932,
+          "gene": "GBP5",
+          "score": -1.4164563819999998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7813,
+          "gene": "KCTD10",
+          "score": -0.634082225,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7713,
+          "gene": "KBTBD7",
+          "score": -0.46124898799999997,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3917,
+          "gene": "DDI1",
+          "score": -0.358771214,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4362,
+          "gene": "DRAM2",
+          "score": -0.939301191,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5783,
+          "gene": "FYN",
+          "score": -0.553065424,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3385,
+          "gene": "CPLX3",
+          "score": -0.822700098,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 402,
+          "gene": "AFP",
+          "score": -0.172061842,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18452,
+          "gene": "ZSWIM4",
+          "score": -0.842698985,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16538,
+          "gene": "TRA2B",
+          "score": -0.8024864890000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16885,
+          "gene": "TUBB3",
+          "score": -0.335623464,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6799,
+          "gene": "HIST1H2AC",
+          "score": -0.24827214399999997,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15321,
+          "gene": "STRN3",
+          "score": -0.736097775,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4144,
+          "gene": "DKK3",
+          "score": -0.9725016759999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15691,
+          "gene": "TCEA2",
+          "score": -0.424226424,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4388,
+          "gene": "DSG2",
+          "score": -1.465331935,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5918,
+          "gene": "GATS",
+          "score": -0.41898935200000004,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10380,
+          "gene": "NMS",
+          "score": -2.195215852,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13103,
+          "gene": "RFWD2",
+          "score": -2.345944742,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16088,
+          "gene": "TMEM115",
+          "score": -2.480368085,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15824,
+          "gene": "TEX35",
+          "score": -1.061614066,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15679,
+          "gene": "TBX3",
+          "score": -0.138851181,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12609,
+          "gene": "PTPN7",
+          "score": -0.433048772,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2484,
+          "gene": "CD2AP",
+          "score": -1.110952407,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 261,
+          "gene": "ADAMTS1",
+          "score": -0.499217543,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12493,
+          "gene": "PSMB6",
+          "score": -0.553505129,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 541,
+          "gene": "ALDH2",
+          "score": -0.205798622,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10243,
+          "gene": "NFIA",
+          "score": -1.357139567,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9574,
+          "gene": "MRAP2",
+          "score": -1.9987967119999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15726,
+          "gene": "TCHH",
+          "score": -0.652392517,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16078,
+          "gene": "TMEM106A",
+          "score": -0.6247561389999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12031,
+          "gene": "POTEB",
+          "score": -1.212309898,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9116,
+          "gene": "MAX",
+          "score": -0.18873263,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8536,
+          "gene": "LIPN",
+          "score": -0.775888713,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17185,
+          "gene": "USHBP1",
+          "score": -0.615645307,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16835,
+          "gene": "TTC39C",
+          "score": -0.981961396,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2450,
+          "gene": "CCZ1",
+          "score": -0.531150152,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9111,
+          "gene": "MATN3",
+          "score": -0.6518451510000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10354,
+          "gene": "NLRP5",
+          "score": -0.8361084759999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17690,
+          "gene": "ZAR1",
+          "score": -0.068593917,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 11340,
+          "gene": "PCNP",
+          "score": -1.563176744,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5317,
+          "gene": "FANCL",
+          "score": -0.6546992070000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1689,
+          "gene": "BVES",
+          "score": -0.318176712,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13397,
+          "gene": "RPAP1",
+          "score": -0.231945911,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9310,
+          "gene": "MEX3B",
+          "score": -1.684934863,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3769,
+          "gene": "CYP4A11",
+          "score": -0.9190545790000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1824,
+          "gene": "C20orf27",
+          "score": -0.5204385970000001,
+          "hit": 0,
+          "round": 4
         }
       ],
       "queried_history": [
@@ -6712,896 +7608,1792 @@
           "gene": "MATN1",
           "score": -0.4104380999999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13984,
           "gene": "SERPINB8",
           "score": -0.329490148,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16328,
           "gene": "TMOD3",
           "score": -0.22175702600000002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8629,
           "gene": "LOC728763",
           "score": -1.1886534709999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2744,
           "gene": "CEP126",
           "score": -0.156549957,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10158,
           "gene": "NDUFS1",
           "score": -0.5231745529999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11344,
           "gene": "PCNXL3",
           "score": -1.567926415,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 716,
           "gene": "ANKRD35",
           "score": -0.519084251,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2424,
           "gene": "CCPG1",
           "score": -0.461368483,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16204,
           "gene": "TMEM220",
           "score": -1.182195947,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 366,
           "gene": "ADORA3",
           "score": -1.2535028959999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3858,
           "gene": "DCAF4L1",
           "score": -1.23915844,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9513,
           "gene": "MOGAT3",
           "score": -0.702892028,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3954,
           "gene": "DDX42",
           "score": -1.368088589,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10418,
           "gene": "NOP56",
           "score": -3.12504232,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1190,
           "gene": "ATG4C",
           "score": -1.294710559,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2233,
           "gene": "CCDC124",
           "score": -1.3287066109999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4534,
           "gene": "EDN2",
           "score": -0.223556442,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9098,
           "gene": "MASP1",
           "score": -0.966823482,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5172,
           "gene": "FAM19A5",
           "score": -1.176611027,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7069,
           "gene": "HSD17B4",
           "score": -0.9546285259999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14340,
           "gene": "SLC24A4",
           "score": -0.662405857,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2513,
           "gene": "CD53",
           "score": -1.053278716,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13666,
           "gene": "SACM1L",
           "score": -2.148767173,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4794,
           "gene": "EPB42",
           "score": -0.061137486,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1912,
           "gene": "C7orf73",
           "score": -0.396462735,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1071,
           "gene": "ARSB",
           "score": -0.5009418520000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5777,
           "gene": "FXYD5",
           "score": -0.33476787399999997,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10738,
           "gene": "ODF2",
           "score": -0.469909029,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8436,
           "gene": "LETM1",
           "score": -0.559237908,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11941,
           "gene": "POC1B-GALNT4",
           "score": -0.11615138300000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10717,
           "gene": "OAZ1",
           "score": -0.32720166300000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3144,
           "gene": "CMTM4",
           "score": -0.716024876,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13775,
           "gene": "SCHIP1",
           "score": -1.139779623,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3010,
           "gene": "CLCN2",
           "score": -1.1597699479999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 704,
           "gene": "ANKRD27",
           "score": -0.7868462820000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10999,
           "gene": "OS9",
           "score": -0.23046398,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10617,
           "gene": "NUCB2",
           "score": -0.628037608,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12954,
           "gene": "RBM23",
           "score": -0.743159424,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17756,
           "gene": "ZC3H15",
           "score": -4.642818375,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17964,
           "gene": "ZNF214",
           "score": -0.434667445,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8515,
           "gene": "LIN52",
           "score": -3.093945923,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2000,
           "gene": "CACFD1",
           "score": -0.6513169289999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16487,
           "gene": "TP53INP2",
           "score": -0.47062887600000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12517,
           "gene": "PSMD9",
           "score": -0.604428159,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7024,
           "gene": "HPS6",
           "score": -1.890446505,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11762,
           "gene": "PLA2G4B",
           "score": -0.477295927,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5235,
           "gene": "FAM46D",
           "score": -0.070973971,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 560,
           "gene": "ALG13",
           "score": -2.780068955,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8363,
           "gene": "LCE1B",
           "score": -0.664128853,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16731,
           "gene": "TSC22D1",
           "score": -2.02432083,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14194,
           "gene": "SIPA1L1",
           "score": -0.8523889179999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9844,
           "gene": "MVK",
           "score": -0.33314050100000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7032,
           "gene": "HRASLS5",
           "score": -0.17696316399999998,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13880,
           "gene": "SEC61B",
           "score": -0.732267441,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12900,
           "gene": "RASGRP3",
           "score": -2.396689074,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12728,
           "gene": "RAB1B",
           "score": -0.590366287,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11107,
           "gene": "PABPC5",
           "score": -0.775620894,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7748,
           "gene": "KCNH3",
           "score": -0.504159483,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15367,
           "gene": "SULT1A1",
           "score": -1.1862740440000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6184,
           "gene": "GNB2L1",
           "score": -1.769044294,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1617,
           "gene": "BRF1",
           "score": -1.374109684,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16722,
           "gene": "TRPV4",
           "score": -0.72425143,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4376,
           "gene": "DRP2",
           "score": -1.152236536,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2458,
           "gene": "CD163L1",
           "score": -1.4734528830000002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9628,
           "gene": "MRPL37",
           "score": -2.2005796159999997,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14238,
           "gene": "SLAMF8",
           "score": -0.646016172,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13490,
           "gene": "RPS20",
           "score": -1.065640001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3465,
           "gene": "CRISP2",
           "score": -0.481033955,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 97,
           "gene": "ABI3",
           "score": -0.18754147399999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12181,
           "gene": "PPP2R5D",
           "score": -0.370238175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9363,
           "gene": "MIA3",
           "score": -0.6449656570000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15293,
           "gene": "STKLD1",
           "score": -0.166186834,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14759,
           "gene": "SNAI3",
           "score": -0.774750712,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6743,
           "gene": "HEY1",
           "score": -2.094411689,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11073,
           "gene": "P2RX2",
           "score": -0.58233107,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9103,
           "gene": "MAST4",
           "score": -1.059639734,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8149,
           "gene": "KRT23",
           "score": -0.09050302199999999,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17417,
           "gene": "VWF",
           "score": -0.584625911,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7573,
           "gene": "ITFG1",
           "score": -1.19117938,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16587,
           "gene": "TREX1",
           "score": -0.342036268,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 923,
           "gene": "ARGLU1",
           "score": -3.2208133180000003,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5010,
           "gene": "F9",
           "score": -0.644513575,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 756,
           "gene": "ANO8",
           "score": -1.947826808,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8833,
           "gene": "LTK",
           "score": -0.7503026909999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16109,
           "gene": "TMEM133",
           "score": -2.072937505,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3209,
           "gene": "CNTN6",
           "score": -0.812852122,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5889,
           "gene": "GAPT",
           "score": -0.663318773,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7213,
           "gene": "IFIH1",
           "score": -0.5536093000000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2121,
           "gene": "CARD18",
           "score": -0.6228774029999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3088,
           "gene": "CLK1",
           "score": -0.270706545,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2177,
           "gene": "CBL",
           "score": -0.204112658,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4461,
           "gene": "DYNC2LI1",
           "score": -0.47467650899999997,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13190,
           "gene": "RHOV",
           "score": -0.392412264,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5519,
           "gene": "FGFR4",
           "score": -0.593319123,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2786,
           "gene": "CERS5",
           "score": -0.19005876800000002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15015,
           "gene": "SPIN4",
           "score": -0.023098108,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13079,
           "gene": "RETSAT",
           "score": -1.03093522,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9330,
           "gene": "MFSD12",
           "score": -3.015320243,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12853,
           "gene": "RANBP6",
           "score": -0.542753612,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13524,
           "gene": "RPUSD3",
           "score": -1.2502314829999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12684,
           "gene": "PYHIN1",
           "score": -0.548085777,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5491,
           "gene": "FGF11",
           "score": -2.175442962,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17649,
           "gene": "YEATS4",
           "score": -1.1739566909999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1004,
           "gene": "ARL14",
           "score": -0.496439061,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2432,
           "gene": "CCR7",
           "score": -0.32461639800000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10796,
           "gene": "OPRL1",
           "score": -0.746379056,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13947,
           "gene": "SEPT9",
           "score": -0.326716425,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7872,
           "gene": "KIAA0100",
           "score": -0.580674799,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10804,
           "gene": "OR10G3",
           "score": -0.823717975,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12252,
           "gene": "PRDM9",
           "score": -0.669017746,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14717,
           "gene": "SMIM24",
           "score": -0.29737308100000004,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7260,
           "gene": "IFT52",
           "score": -1.4153385,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13175,
           "gene": "RHOA",
           "score": -2.9459395660000003,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17473,
           "gene": "WDR48",
           "score": -0.528011775,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18095,
           "gene": "ZNF432",
           "score": -1.8124296130000002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 35,
           "gene": "ABCA3",
           "score": -0.21133955100000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13875,
           "gene": "SEC24D",
           "score": -0.7292541159999999,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1116,
           "gene": "ASCL1",
           "score": -0.18055578100000003,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15694,
           "gene": "TCEAL2",
           "score": -0.8765485590000001,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1904,
           "gene": "C7orf60",
           "score": -0.546959614,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7836,
           "gene": "KDELR2",
           "score": -0.487717731,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7710,
           "gene": "KBTBD3",
           "score": -1.066628225,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7589,
           "gene": "ITGAE",
           "score": -0.215583203,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2082,
           "gene": "CAMTA1",
           "score": -0.456741119,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1653,
           "gene": "BTBD17",
           "score": -0.126790438,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2879,
           "gene": "CHI3L2",
           "score": -0.885074315,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12453,
           "gene": "PRY",
           "score": -0.83277222,
           "hit": 0,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 13463,
+          "gene": "RPN2",
+          "score": -1.072642225,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18154,
+          "gene": "ZNF524",
+          "score": -0.701245465,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 703,
+          "gene": "ANKRD26",
+          "score": -0.7000300979999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1803,
+          "gene": "C1QL4",
+          "score": -0.921619408,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1179,
+          "gene": "ATG10",
+          "score": -1.389136745,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5456,
+          "gene": "FDXACB1",
+          "score": -1.4648971919999998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10318,
+          "gene": "NKPD1",
+          "score": -1.079146919,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8580,
+          "gene": "LOC100129924",
+          "score": -0.8757421479999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12113,
+          "gene": "PPM1E",
+          "score": -1.567175107,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6548,
+          "gene": "GUCA2B",
+          "score": -0.585928335,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13219,
+          "gene": "RIN2",
+          "score": -0.5871104229999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1466,
+          "gene": "BCL7C",
+          "score": -1.4200866419999998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16460,
+          "gene": "TOP1MT",
+          "score": -1.262787231,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4883,
+          "gene": "ERO1L",
+          "score": -0.44012297899999997,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4972,
+          "gene": "EXOSC4",
+          "score": -2.8849797789999996,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 13851,
+          "gene": "SDR42E1",
+          "score": -0.39897536299999997,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4438,
+          "gene": "DUSP3",
+          "score": -1.4338238840000002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16755,
+          "gene": "TSNAXIP1",
+          "score": -1.167008766,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2164,
+          "gene": "CATSPER1",
+          "score": -0.219501516,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6855,
+          "gene": "HIST2H4A",
+          "score": -1.216771716,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11169,
+          "gene": "PAPD5",
+          "score": -0.09046830900000001,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 9524,
+          "gene": "MORF4L2",
+          "score": -1.301956869,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3131,
+          "gene": "CMAS",
+          "score": -0.09473950099999999,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 2523,
+          "gene": "CD70",
+          "score": -0.954214553,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8763,
+          "gene": "LRRC69",
+          "score": -0.522880595,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11578,
+          "gene": "PHF19",
+          "score": -1.467490089,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16678,
+          "gene": "TRMT1",
+          "score": -0.786866135,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14406,
+          "gene": "SLC27A6",
+          "score": -0.549412566,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12475,
+          "gene": "PSIP1",
+          "score": -0.342268356,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5059,
+          "gene": "FAM120A",
+          "score": -3.939774678,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 6568,
+          "gene": "GYPE",
+          "score": -1.4383159769999998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15852,
+          "gene": "TFIP11",
+          "score": -1.5623279330000002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5467,
+          "gene": "FERMT1",
+          "score": -0.711104238,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10604,
+          "gene": "NTRK1",
+          "score": -1.145320792,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17910,
+          "gene": "ZNF101",
+          "score": -0.45488637200000004,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3624,
+          "gene": "CTSC",
+          "score": -1.243525299,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10968,
+          "gene": "OR6Y1",
+          "score": -0.7966781690000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16515,
+          "gene": "TPO",
+          "score": -0.40068333,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 495,
+          "gene": "AKAP14",
+          "score": -0.7970176529999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10460,
+          "gene": "NPFFR1",
+          "score": -0.345893616,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6553,
+          "gene": "GUCY2C",
+          "score": -0.463074449,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7492,
+          "gene": "IPO4",
+          "score": -0.573281973,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3181,
+          "gene": "CNOT11",
+          "score": -1.4087829530000002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7315,
+          "gene": "IKZF1",
+          "score": -0.328590812,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 734,
+          "gene": "ANKRD62",
+          "score": -0.445463528,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12096,
+          "gene": "PPIC",
+          "score": -0.8380380620000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15322,
+          "gene": "STRN4",
+          "score": -2.532463187,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 353,
+          "gene": "ADIPOR1",
+          "score": -0.627363333,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7323,
+          "gene": "IL11",
+          "score": -0.748475472,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6919,
+          "gene": "HMHA1",
+          "score": -0.485296687,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 504,
+          "gene": "AKAP8L",
+          "score": -0.505764849,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17931,
+          "gene": "ZNF146",
+          "score": -0.21671926,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11302,
+          "gene": "PCDHGA11",
+          "score": -0.317556635,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18331,
+          "gene": "ZNF766",
+          "score": -0.300786966,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1107,
+          "gene": "ASB4",
+          "score": -1.043560733,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3684,
+          "gene": "CXCL9",
+          "score": -0.573437973,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3292,
+          "gene": "COMMD3",
+          "score": -0.956465454,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17146,
+          "gene": "UPF2",
+          "score": -0.441269554,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7418,
+          "gene": "IMPA2",
+          "score": -1.983105057,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14265,
+          "gene": "SLC14A2",
+          "score": -1.2126064140000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5099,
+          "gene": "FAM153B",
+          "score": -2.6040197640000002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5740,
+          "gene": "FTH1",
+          "score": -0.631323055,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5597,
+          "gene": "FMNL2",
+          "score": -1.225692125,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2928,
+          "gene": "CHRNA7",
+          "score": -0.627056724,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12140,
+          "gene": "PPP1R16A",
+          "score": -0.5026894679999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3651,
+          "gene": "CUL4A",
+          "score": -0.798165942,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9069,
+          "gene": "MAPRE3",
+          "score": -2.60754938,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15572,
+          "gene": "TARS",
+          "score": -0.512684126,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17109,
+          "gene": "UHRF1BP1L",
+          "score": -0.53352791,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7546,
+          "gene": "IRX1",
+          "score": -0.380680081,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7572,
+          "gene": "ITCH",
+          "score": -0.92167761,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11103,
+          "gene": "PABPC1L2B",
+          "score": -0.9224545259999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16623,
+          "gene": "TRIM38",
+          "score": -0.43126190299999995,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 444,
+          "gene": "AGTR1",
+          "score": -0.594623295,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14856,
+          "gene": "SOHLH2",
+          "score": -1.658807138,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16000,
+          "gene": "TLE4",
+          "score": -1.476070148,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13158,
+          "gene": "RHAG",
+          "score": -0.204187578,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7969,
+          "gene": "KIF26B",
+          "score": -0.132942002,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7457,
+          "gene": "INPP5K",
+          "score": -0.400332564,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11406,
+          "gene": "PDE8B",
+          "score": -0.281771261,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1843,
+          "gene": "C2orf73",
+          "score": -0.661731399,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5932,
+          "gene": "GBP5",
+          "score": -1.4164563819999998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7813,
+          "gene": "KCTD10",
+          "score": -0.634082225,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7713,
+          "gene": "KBTBD7",
+          "score": -0.46124898799999997,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3917,
+          "gene": "DDI1",
+          "score": -0.358771214,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4362,
+          "gene": "DRAM2",
+          "score": -0.939301191,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5783,
+          "gene": "FYN",
+          "score": -0.553065424,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3385,
+          "gene": "CPLX3",
+          "score": -0.822700098,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 402,
+          "gene": "AFP",
+          "score": -0.172061842,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18452,
+          "gene": "ZSWIM4",
+          "score": -0.842698985,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16538,
+          "gene": "TRA2B",
+          "score": -0.8024864890000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16885,
+          "gene": "TUBB3",
+          "score": -0.335623464,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6799,
+          "gene": "HIST1H2AC",
+          "score": -0.24827214399999997,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15321,
+          "gene": "STRN3",
+          "score": -0.736097775,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4144,
+          "gene": "DKK3",
+          "score": -0.9725016759999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15691,
+          "gene": "TCEA2",
+          "score": -0.424226424,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4388,
+          "gene": "DSG2",
+          "score": -1.465331935,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5918,
+          "gene": "GATS",
+          "score": -0.41898935200000004,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10380,
+          "gene": "NMS",
+          "score": -2.195215852,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13103,
+          "gene": "RFWD2",
+          "score": -2.345944742,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16088,
+          "gene": "TMEM115",
+          "score": -2.480368085,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15824,
+          "gene": "TEX35",
+          "score": -1.061614066,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15679,
+          "gene": "TBX3",
+          "score": -0.138851181,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12609,
+          "gene": "PTPN7",
+          "score": -0.433048772,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2484,
+          "gene": "CD2AP",
+          "score": -1.110952407,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 261,
+          "gene": "ADAMTS1",
+          "score": -0.499217543,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12493,
+          "gene": "PSMB6",
+          "score": -0.553505129,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 541,
+          "gene": "ALDH2",
+          "score": -0.205798622,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10243,
+          "gene": "NFIA",
+          "score": -1.357139567,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9574,
+          "gene": "MRAP2",
+          "score": -1.9987967119999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15726,
+          "gene": "TCHH",
+          "score": -0.652392517,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16078,
+          "gene": "TMEM106A",
+          "score": -0.6247561389999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12031,
+          "gene": "POTEB",
+          "score": -1.212309898,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9116,
+          "gene": "MAX",
+          "score": -0.18873263,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8536,
+          "gene": "LIPN",
+          "score": -0.775888713,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17185,
+          "gene": "USHBP1",
+          "score": -0.615645307,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16835,
+          "gene": "TTC39C",
+          "score": -0.981961396,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2450,
+          "gene": "CCZ1",
+          "score": -0.531150152,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9111,
+          "gene": "MATN3",
+          "score": -0.6518451510000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10354,
+          "gene": "NLRP5",
+          "score": -0.8361084759999999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17690,
+          "gene": "ZAR1",
+          "score": -0.068593917,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 11340,
+          "gene": "PCNP",
+          "score": -1.563176744,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5317,
+          "gene": "FANCL",
+          "score": -0.6546992070000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1689,
+          "gene": "BVES",
+          "score": -0.318176712,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13397,
+          "gene": "RPAP1",
+          "score": -0.231945911,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9310,
+          "gene": "MEX3B",
+          "score": -1.684934863,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3769,
+          "gene": "CYP4A11",
+          "score": -0.9190545790000001,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1824,
+          "gene": "C20orf27",
+          "score": -0.5204385970000001,
+          "hit": 0,
+          "round": 4
         }
       ]
     }

```
