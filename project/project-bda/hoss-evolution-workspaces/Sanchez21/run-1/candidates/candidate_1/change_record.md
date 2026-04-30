# Change Record — candidate_1

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21/run-1/best/current/harness
Generated at: 2026-04-30T06:53:27.308884

## Files Changed

- model.py: modified (added=104, deleted=5, delta=99)
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
@@ -24,9 +26,106 @@
 
     Output:
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
-
-    You may implement any suitable algorithmic model here, including but not limited to:
-    traditional algorithms, machine learning models, deep learning models, biological models,
-    and mathematical models.
+    
+    Strategy: Hybrid exploration-exploitation with adaptive sampling
+    - Early rounds: More random exploration to discover promising regions
+    - Later rounds: More exploitation of high-scoring candidates
+    - Always maintain diversity to avoid getting stuck in local optima
     """
-    pass
+    rng = random.Random(seed)
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
+    # Calculate exploration ratio based on history size
+    # More exploration in early rounds, more exploitation later
+    num_rounds = len(history) // batch_size if batch_size > 0 else 0
+    exploration_ratio = max(0.2, 0.9 - 0.15 * num_rounds)  # Starts at 90%, decreases to 20%
+    
+    # Separate exploration and exploitation
+    num_explore = int(batch_size * exploration_ratio)
+    num_exploit = batch_size - num_explore
+    
+    # Exploration: random sampling from available candidates
+    explore_indices = rng.sample(available, min(num_explore, len(available)))
+    
+    # Exploitation: select based on historical scores
+    if len(history) > 0 and num_exploit > 0:
+        # Sort history by score (descending)
+        sorted_history = sorted(history, key=lambda x: x['score'], reverse=True)
+        
+        # Get top performers (top 20% or at least 10)
+        top_k = max(10, len(sorted_history) // 5)
+        top_performers = [h['candidate_index'] for h in sorted_history[:top_k]]
+        
+        # Find candidates similar to top performers if gene search is available
+        exploit_candidates = set()
+        remaining_avail = [i for i in available if i not in explore_indices]
+        
+        if len(remaining_avail) > 0:
+            # Try to use gene search if available
+            try:
+                import bda_tools
+                # Sample from top performers and find similar genes
+                num_to_sample = min(5, len(top_performers))
+                sampled_top = rng.sample(top_performers, num_to_sample)
+                
+                for top_idx in sampled_top:
+                    if len(exploit_candidates) >= num_exploit:
+                        break
+                    # Get gene name from candidate
+                    candidate = candidates[top_idx]
+                    gene = candidate.get('gene') or candidate.get('gene_a')
+                    if gene:
+                        try:
+                            similar = bda_tools.gene_search(gene, k=min(20, num_exploit), diverse=False)
+                            for idx in similar:
+                                if idx in remaining_avail and idx not in exploit_candidates:
+                                    exploit_candidates.add(idx)
+                                    if len(exploit_candidates) >= num_exploit:
+                                        break
+                        except:
+                            pass
+            except ImportError:
+                # bda_tools not available, fall back to other strategies
+                pass
+            
+            # If we still need more candidates, use weighted sampling
+            if len(exploit_candidates) < num_exploit:
+                needed = num_exploit - len(exploit_candidates)
+                # Use stratified sampling for diversity: divide remaining into buckets
+                num_buckets = min(10, len(remaining_avail))
+                bucket_size = len(remaining_avail) // num_buckets
+                
+                sampled = set()
+                for bucket in range(num_buckets):
+                    if len(sampled) >= needed:
+                        break
+                    start = bucket * bucket_size
+                    end = start + bucket_size if bucket < num_buckets - 1 else len(remaining_avail)
+                    bucket_items = remaining_avail[start:end]
+                    if bucket_items:
+                        sampled.add(rng.choice(bucket_items))
+                
+                exploit_candidates.update(sampled)
+        
+        selected_indices = list(explore_indices) + list(exploit_candidates)[:num_exploit]
+    else:
+        # Pure exploration if no history or no exploitation needed
+        selected_indices = explore_indices
+    
+    # Ensure we have exactly batch_size indices
+    if len(selected_indices) < batch_size:
+        remaining = [i for i in available if i not in selected_indices]
+        needed = batch_size - len(selected_indices)
+        if remaining:
+            selected_indices.extend(rng.sample(remaining, min(needed, len(remaining))))
+    
+    return selected_indices[:batch_size]

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -0,0 +1,2233 @@
+{
+  "task": "perturb-genes-brief",
+  "data_name": "Sanchez21",
+  "measurement": "the change in tau protein level compared to the non-targeting control, using a total tau antibody",
+  "task_prompt": {
+    "Task": "identify genes that, when knocked out, either increase or decrease expression of endogenous tau protein levels in neurons",
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
+      "delta_hits": 8,
+      "total_queries": 128,
+      "total_hits": 8,
+      "top_k": 924,
+      "hit_curve": {
+        "queries": [
+          0,
+          128
+        ],
+        "hits": [
+          0,
+          8
+        ]
+      },
+      "auc": 512.0,
+      "auc_normalized": 0.004329004329004329,
+      "ncg": 0.20608211756124528,
+      "round_details": [
+        {
+          "round": 0,
+          "selected_count": 128,
+          "hits": 8,
+          "cumulative_hits": 8,
+          "precision_at_batch": 0.0625,
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
+            "ZNF626",
+            "ADRA2C",
+            "CYP4X1",
+            "ZBTB10",
+            "LSM12",
+            "PATE3",
+            "CXCL5",
+            "MS4A13",
+            "SLC24A5",
+            "FAM24B",
+            "SPATA5",
+            "ABRA",
+            "LRMP"
+          ],
+          "selected_scores": [
+            -0.7084805590000001,
+            -0.847566367,
+            -0.646392168,
+            -1.286605531,
+            -1.011233856,
+            -0.605851751,
+            -3.0936171619999997,
+            -0.6378804539999999,
+            -1.45418052,
+            -0.463321217,
+            -1.390124729,
+            -0.5351421789999999,
+            -0.526246283,
+            -0.41687788600000003,
+            -0.8075541079999999,
+            -0.207407924,
+            -1.178192222,
+            -0.667703014,
+            -1.161694307,
+            -0.151761909,
+            -0.0308524,
+            -1.034508226,
+            -0.8907777590000001,
+            -0.296087312,
+            -2.1890067109999998,
+            -2.316107883,
+            -0.22494741199999999,
+            -0.25187241,
+            -0.58303235,
+            -1.1998195740000002,
+            -0.680339995,
+            -0.083778762,
+            -0.7748776279999999,
+            -3.4000132339999998,
+            -0.389149951,
+            -0.486427984,
+            -0.5954982870000001,
+            -0.76248473,
+            -2.680333955,
+            -0.44684414,
+            -0.957138816,
+            -1.762816357,
+            -0.343573709,
+            -0.536061023,
+            -1.925039131,
+            -0.755163757,
+            -0.10235072699999999,
+            -0.44822563,
+            -0.177922565,
+            -1.165824661,
+            -0.17457183699999998,
+            -1.491389192,
+            -0.333031154,
+            -1.312742639,
+            -1.127677133,
+            -0.156469786,
+            -3.122229945,
+            -1.420538244,
+            -0.426324209,
+            -0.991251599,
+            -0.38996551,
+            -0.641169591,
+            -0.489342847,
+            -0.194383213,
+            -0.46040265,
+            -4.211130287,
+            -0.133489856,
+            -0.7718566029999999,
+            -0.38812869200000005,
+            -0.283086165,
+            -0.733157018,
+            -1.908639,
+            -1.646824745,
+            -0.6040569410000001,
+            -1.37219963,
+            -0.798608137,
+            -0.7842747290000001,
+            -0.5480988139999999,
+            -0.7191423090000001,
+            -2.298319116,
+            -1.9909401919999998,
+            -0.7791987109999999,
+            -0.30452932899999996,
+            -1.537334942,
+            -0.26130868100000004,
+            -0.217601022,
+            -0.23205319,
+            -0.382187661,
+            -1.310862131,
+            -0.780715103,
+            -0.57855135,
+            -0.41219300799999997,
+            -0.662382259,
+            -0.739281469,
+            -1.4617258359999998,
+            -0.481618604,
+            -0.62648364,
+            -0.339161064,
+            -0.725619907,
+            -1.4750069540000001,
+            -0.43605276600000004,
+            -0.44800802,
+            -1.379951568,
+            -0.697778867,
+            -1.0208300670000001,
+            -0.615594321,
+            -0.757835777,
+            -2.014598466,
+            -0.7172328170000001,
+            -0.503657337,
+            -0.742329297,
+            -0.443164457,
+            -0.369267661,
+            -0.485805724,
+            -1.1155609,
+            -0.48027414700000004,
+            -0.514642412,
+            -0.55176932,
+            -1.454030435,
+            -2.058202489,
+            -1.255088674,
+            -0.57877837,
+            -0.6619021660000001,
+            -1.198486086,
+            -1.130251816,
+            -0.547784346,
+            -0.213723146,
+            -1.582579036
+          ],
+          "selected_hits": [
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
+            1,
+            0,
+            1,
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
+          "score": -0.7084805590000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 819,
+          "gene": "APBB1IP",
+          "score": -0.847566367,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9012,
+          "gene": "MAP2K5",
+          "score": -0.646392168,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8024,
+          "gene": "KLF6",
+          "score": -1.286605531,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7314,
+          "gene": "IKBKG",
+          "score": -1.011233856,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4572,
+          "gene": "EFNA1",
+          "score": -0.605851751,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3358,
+          "gene": "COX7A1",
+          "score": -3.0936171619999997,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 17870,
+          "gene": "ZHX2",
+          "score": -0.6378804539999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2848,
+          "gene": "CHADL",
+          "score": -1.45418052,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13825,
+          "gene": "SDAD1",
+          "score": -0.463321217,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1041,
+          "gene": "ARMCX3",
+          "score": -1.390124729,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 976,
+          "gene": "ARHGEF35",
+          "score": -0.5351421789999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3070,
+          "gene": "CLEC5A",
+          "score": -0.526246283,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7164,
+          "gene": "IBSP",
+          "score": -0.41687788600000003,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7623,
+          "gene": "ITPR1",
+          "score": -0.8075541079999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16559,
+          "gene": "TRAM2",
+          "score": -0.207407924,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 869,
+          "gene": "APOL3",
+          "score": -1.178192222,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18390,
+          "gene": "ZNF85",
+          "score": -0.667703014,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6515,
+          "gene": "GTF2E2",
+          "score": -1.161694307,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17856,
+          "gene": "ZFYVE16",
+          "score": -0.151761909,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13746,
+          "gene": "SCAND1",
+          "score": -0.0308524,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 7223,
+          "gene": "IFITM5",
+          "score": -1.034508226,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14719,
+          "gene": "SMIM4",
+          "score": -0.8907777590000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9115,
+          "gene": "MAVS",
+          "score": -0.296087312,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 212,
+          "gene": "ACTN4",
+          "score": -2.1890067109999998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5231,
+          "gene": "FAM45A",
+          "score": -2.316107883,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13848,
+          "gene": "SDPR",
+          "score": -0.22494741199999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11149,
+          "gene": "PALLD",
+          "score": -0.25187241,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9105,
+          "gene": "MAT1A",
+          "score": -0.58303235,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5094,
+          "gene": "FAM150A",
+          "score": -1.1998195740000002,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7055,
+          "gene": "HSBP1",
+          "score": -0.680339995,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11029,
+          "gene": "OTOA",
+          "score": -0.083778762,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 3349,
+          "gene": "COX4I1",
+          "score": -0.7748776279999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3039,
+          "gene": "CLDN7",
+          "score": -3.4000132339999998,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 12449,
+          "gene": "PRTN3",
+          "score": -0.389149951,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3169,
+          "gene": "CNKSR1",
+          "score": -0.486427984,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11763,
+          "gene": "PLA2G4C",
+          "score": -0.5954982870000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11270,
+          "gene": "PCDHA10",
+          "score": -0.76248473,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8667,
+          "gene": "LPPR5",
+          "score": -2.680333955,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 1423,
+          "gene": "BBS2",
+          "score": -0.44684414,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15054,
+          "gene": "SPRED3",
+          "score": -0.957138816,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17571,
+          "gene": "WRN",
+          "score": -1.762816357,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4090,
+          "gene": "DHRS3",
+          "score": -0.343573709,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12403,
+          "gene": "PRR5L",
+          "score": -0.536061023,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2582,
+          "gene": "CDCA8",
+          "score": -1.925039131,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18089,
+          "gene": "ZNF426",
+          "score": -0.755163757,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9606,
+          "gene": "MRPL13",
+          "score": -0.10235072699999999,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 11850,
+          "gene": "PLIN2",
+          "score": -0.44822563,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6300,
+          "gene": "GPR107",
+          "score": -0.177922565,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2279,
+          "gene": "CCDC178",
+          "score": -1.165824661,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1501,
+          "gene": "BFAR",
+          "score": -0.17457183699999998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7467,
+          "gene": "INSL6",
+          "score": -1.491389192,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9482,
+          "gene": "MMP3",
+          "score": -0.333031154,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2614,
+          "gene": "CDIPT",
+          "score": -1.312742639,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7628,
+          "gene": "ITPRIPL2",
+          "score": -1.127677133,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3309,
+          "gene": "COPRS",
+          "score": -0.156469786,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12455,
+          "gene": "PSAP",
+          "score": -3.122229945,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 9108,
+          "gene": "MATK",
+          "score": -1.420538244,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14857,
+          "gene": "SON",
+          "score": -0.426324209,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11954,
+          "gene": "POLA2",
+          "score": -0.991251599,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5329,
+          "gene": "FASLG",
+          "score": -0.38996551,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12130,
+          "gene": "PPP1R12B",
+          "score": -0.641169591,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11641,
+          "gene": "PIGA",
+          "score": -0.489342847,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6865,
+          "gene": "HK1",
+          "score": -0.194383213,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8748,
+          "gene": "LRRC47",
+          "score": -0.46040265,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2339,
+          "gene": "CCDC84",
+          "score": -4.211130287,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 5607,
+          "gene": "FN1",
+          "score": -0.133489856,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17502,
+          "gene": "WDR87",
+          "score": -0.7718566029999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8021,
+          "gene": "KLF3",
+          "score": -0.38812869200000005,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5354,
+          "gene": "FBP1",
+          "score": -0.283086165,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15147,
+          "gene": "SRSF6",
+          "score": -0.733157018,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12433,
+          "gene": "PRSS41",
+          "score": -1.908639,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8845,
+          "gene": "LVRN",
+          "score": -1.646824745,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18250,
+          "gene": "ZNF646",
+          "score": -0.6040569410000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7196,
+          "gene": "IDUA",
+          "score": -1.37219963,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10626,
+          "gene": "NUDT12",
+          "score": -0.798608137,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1832,
+          "gene": "C2CD2L",
+          "score": -0.7842747290000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7505,
+          "gene": "IQCF2",
+          "score": -0.5480988139999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1051,
+          "gene": "ARPC1A",
+          "score": -0.7191423090000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10336,
+          "gene": "NLGN2",
+          "score": -2.298319116,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13145,
+          "gene": "RGS20",
+          "score": -1.9909401919999998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8773,
+          "gene": "LRRC8B",
+          "score": -0.7791987109999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2168,
+          "gene": "CATSPERB",
+          "score": -0.30452932899999996,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6913,
+          "gene": "HMGN2",
+          "score": -1.537334942,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10311,
+          "gene": "NKAP",
+          "score": -0.26130868100000004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6967,
+          "gene": "HORMAD2",
+          "score": -0.217601022,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16358,
+          "gene": "TMX1",
+          "score": -0.23205319,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12964,
+          "gene": "RBM39",
+          "score": -0.382187661,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15035,
+          "gene": "SPNS3",
+          "score": -1.310862131,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4681,
+          "gene": "ELK1",
+          "score": -0.780715103,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8679,
+          "gene": "LRFN4",
+          "score": -0.57855135,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4575,
+          "gene": "EFNA4",
+          "score": -0.41219300799999997,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8081,
+          "gene": "KLK15",
+          "score": -0.662382259,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18394,
+          "gene": "ZNF862",
+          "score": -0.739281469,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17661,
+          "gene": "YKT6",
+          "score": -1.4617258359999998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8609,
+          "gene": "LOC101060179",
+          "score": -0.481618604,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14038,
+          "gene": "SFN",
+          "score": -0.62648364,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13087,
+          "gene": "RFC3",
+          "score": -0.339161064,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11861,
+          "gene": "PLOD1",
+          "score": -0.725619907,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7186,
+          "gene": "IDH2",
+          "score": -1.4750069540000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4532,
+          "gene": "EDIL3",
+          "score": -0.43605276600000004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16696,
+          "gene": "TRNP1",
+          "score": -0.44800802,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16171,
+          "gene": "TMEM189",
+          "score": -1.379951568,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2978,
+          "gene": "CISD1",
+          "score": -0.697778867,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1543,
+          "gene": "BLVRA",
+          "score": -1.0208300670000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3592,
+          "gene": "CTCFL",
+          "score": -0.615594321,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5008,
+          "gene": "F8A2",
+          "score": -0.757835777,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5242,
+          "gene": "FAM49B",
+          "score": -2.014598466,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13833,
+          "gene": "SDCCAG8",
+          "score": -0.7172328170000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2081,
+          "gene": "CAMSAP3",
+          "score": -0.503657337,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12608,
+          "gene": "PTPN6",
+          "score": -0.742329297,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12504,
+          "gene": "PSMD1",
+          "score": -0.443164457,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15337,
+          "gene": "STX3",
+          "score": -0.369267661,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17338,
+          "gene": "VN1R1",
+          "score": -0.485805724,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8238,
+          "gene": "KRTAP2-4",
+          "score": -1.1155609,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18240,
+          "gene": "ZNF626",
+          "score": -0.48027414700000004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 377,
+          "gene": "ADRA2C",
+          "score": -0.514642412,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3779,
+          "gene": "CYP4X1",
+          "score": -0.55176932,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17704,
+          "gene": "ZBTB10",
+          "score": -1.454030435,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8805,
+          "gene": "LSM12",
+          "score": -2.058202489,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11220,
+          "gene": "PATE3",
+          "score": -1.255088674,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3681,
+          "gene": "CXCL5",
+          "score": -0.57877837,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9686,
+          "gene": "MS4A13",
+          "score": -0.6619021660000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14341,
+          "gene": "SLC24A5",
+          "score": -1.198486086,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5215,
+          "gene": "FAM24B",
+          "score": -1.130251816,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14964,
+          "gene": "SPATA5",
+          "score": -0.547784346,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 106,
+          "gene": "ABRA",
+          "score": -0.213723146,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8690,
+          "gene": "LRMP",
+          "score": -1.582579036,
+          "hit": 0,
+          "round": 0
+        }
+      ],
+      "queried_history": [
+        {
+          "candidate_index": 3648,
+          "gene": "CUL1",
+          "score": -0.7084805590000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 819,
+          "gene": "APBB1IP",
+          "score": -0.847566367,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9012,
+          "gene": "MAP2K5",
+          "score": -0.646392168,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8024,
+          "gene": "KLF6",
+          "score": -1.286605531,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7314,
+          "gene": "IKBKG",
+          "score": -1.011233856,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4572,
+          "gene": "EFNA1",
+          "score": -0.605851751,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3358,
+          "gene": "COX7A1",
+          "score": -3.0936171619999997,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 17870,
+          "gene": "ZHX2",
+          "score": -0.6378804539999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2848,
+          "gene": "CHADL",
+          "score": -1.45418052,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13825,
+          "gene": "SDAD1",
+          "score": -0.463321217,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1041,
+          "gene": "ARMCX3",
+          "score": -1.390124729,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 976,
+          "gene": "ARHGEF35",
+          "score": -0.5351421789999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3070,
+          "gene": "CLEC5A",
+          "score": -0.526246283,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7164,
+          "gene": "IBSP",
+          "score": -0.41687788600000003,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7623,
+          "gene": "ITPR1",
+          "score": -0.8075541079999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16559,
+          "gene": "TRAM2",
+          "score": -0.207407924,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 869,
+          "gene": "APOL3",
+          "score": -1.178192222,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18390,
+          "gene": "ZNF85",
+          "score": -0.667703014,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6515,
+          "gene": "GTF2E2",
+          "score": -1.161694307,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17856,
+          "gene": "ZFYVE16",
+          "score": -0.151761909,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13746,
+          "gene": "SCAND1",
+          "score": -0.0308524,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 7223,
+          "gene": "IFITM5",
+          "score": -1.034508226,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14719,
+          "gene": "SMIM4",
+          "score": -0.8907777590000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9115,
+          "gene": "MAVS",
+          "score": -0.296087312,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 212,
+          "gene": "ACTN4",
+          "score": -2.1890067109999998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5231,
+          "gene": "FAM45A",
+          "score": -2.316107883,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13848,
+          "gene": "SDPR",
+          "score": -0.22494741199999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11149,
+          "gene": "PALLD",
+          "score": -0.25187241,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9105,
+          "gene": "MAT1A",
+          "score": -0.58303235,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5094,
+          "gene": "FAM150A",
+          "score": -1.1998195740000002,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7055,
+          "gene": "HSBP1",
+          "score": -0.680339995,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11029,
+          "gene": "OTOA",
+          "score": -0.083778762,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 3349,
+          "gene": "COX4I1",
+          "score": -0.7748776279999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3039,
+          "gene": "CLDN7",
+          "score": -3.4000132339999998,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 12449,
+          "gene": "PRTN3",
+          "score": -0.389149951,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3169,
+          "gene": "CNKSR1",
+          "score": -0.486427984,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11763,
+          "gene": "PLA2G4C",
+          "score": -0.5954982870000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11270,
+          "gene": "PCDHA10",
+          "score": -0.76248473,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8667,
+          "gene": "LPPR5",
+          "score": -2.680333955,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 1423,
+          "gene": "BBS2",
+          "score": -0.44684414,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15054,
+          "gene": "SPRED3",
+          "score": -0.957138816,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17571,
+          "gene": "WRN",
+          "score": -1.762816357,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4090,
+          "gene": "DHRS3",
+          "score": -0.343573709,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12403,
+          "gene": "PRR5L",
+          "score": -0.536061023,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2582,
+          "gene": "CDCA8",
+          "score": -1.925039131,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18089,
+          "gene": "ZNF426",
+          "score": -0.755163757,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9606,
+          "gene": "MRPL13",
+          "score": -0.10235072699999999,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 11850,
+          "gene": "PLIN2",
+          "score": -0.44822563,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6300,
+          "gene": "GPR107",
+          "score": -0.177922565,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2279,
+          "gene": "CCDC178",
+          "score": -1.165824661,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1501,
+          "gene": "BFAR",
+          "score": -0.17457183699999998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7467,
+          "gene": "INSL6",
+          "score": -1.491389192,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9482,
+          "gene": "MMP3",
+          "score": -0.333031154,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2614,
+          "gene": "CDIPT",
+          "score": -1.312742639,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7628,
+          "gene": "ITPRIPL2",
+          "score": -1.127677133,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3309,
+          "gene": "COPRS",
+          "score": -0.156469786,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12455,
+          "gene": "PSAP",
+          "score": -3.122229945,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 9108,
+          "gene": "MATK",
+          "score": -1.420538244,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14857,
+          "gene": "SON",
+          "score": -0.426324209,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11954,
+          "gene": "POLA2",
+          "score": -0.991251599,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5329,
+          "gene": "FASLG",
+          "score": -0.38996551,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12130,
+          "gene": "PPP1R12B",
+          "score": -0.641169591,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11641,
+          "gene": "PIGA",
+          "score": -0.489342847,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6865,
+          "gene": "HK1",
+          "score": -0.194383213,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8748,
+          "gene": "LRRC47",
+          "score": -0.46040265,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2339,
+          "gene": "CCDC84",
+          "score": -4.211130287,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 5607,
+          "gene": "FN1",
+          "score": -0.133489856,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17502,
+          "gene": "WDR87",
+          "score": -0.7718566029999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8021,
+          "gene": "KLF3",
+          "score": -0.38812869200000005,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5354,
+          "gene": "FBP1",
+          "score": -0.283086165,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15147,
+          "gene": "SRSF6",
+          "score": -0.733157018,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12433,
+          "gene": "PRSS41",
+          "score": -1.908639,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8845,
+          "gene": "LVRN",
+          "score": -1.646824745,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18250,
+          "gene": "ZNF646",
+          "score": -0.6040569410000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7196,
+          "gene": "IDUA",
+          "score": -1.37219963,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10626,
+          "gene": "NUDT12",
+          "score": -0.798608137,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1832,
+          "gene": "C2CD2L",
+          "score": -0.7842747290000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7505,
+          "gene": "IQCF2",
+          "score": -0.5480988139999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1051,
+          "gene": "ARPC1A",
+          "score": -0.7191423090000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10336,
+          "gene": "NLGN2",
+          "score": -2.298319116,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13145,
+          "gene": "RGS20",
+          "score": -1.9909401919999998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8773,
+          "gene": "LRRC8B",
+          "score": -0.7791987109999999,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2168,
+          "gene": "CATSPERB",
+          "score": -0.30452932899999996,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6913,
+          "gene": "HMGN2",
+          "score": -1.537334942,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10311,
+          "gene": "NKAP",
+          "score": -0.26130868100000004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6967,
+          "gene": "HORMAD2",
+          "score": -0.217601022,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16358,
+          "gene": "TMX1",
+          "score": -0.23205319,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12964,
+          "gene": "RBM39",
+          "score": -0.382187661,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15035,
+          "gene": "SPNS3",
+          "score": -1.310862131,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4681,
+          "gene": "ELK1",
+          "score": -0.780715103,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8679,
+          "gene": "LRFN4",
+          "score": -0.57855135,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4575,
+          "gene": "EFNA4",
+          "score": -0.41219300799999997,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8081,
+          "gene": "KLK15",
+          "score": -0.662382259,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18394,
+          "gene": "ZNF862",
+          "score": -0.739281469,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17661,
+          "gene": "YKT6",
+          "score": -1.4617258359999998,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8609,
+          "gene": "LOC101060179",
+          "score": -0.481618604,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14038,
+          "gene": "SFN",
+          "score": -0.62648364,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13087,
+          "gene": "RFC3",
+          "score": -0.339161064,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11861,
+          "gene": "PLOD1",
+          "score": -0.725619907,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7186,
+          "gene": "IDH2",
+          "score": -1.4750069540000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4532,
+          "gene": "EDIL3",
+          "score": -0.43605276600000004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16696,
+          "gene": "TRNP1",
+          "score": -0.44800802,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16171,
+          "gene": "TMEM189",
+          "score": -1.379951568,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2978,
+          "gene": "CISD1",
+          "score": -0.697778867,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1543,
+          "gene": "BLVRA",
+          "score": -1.0208300670000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3592,
+          "gene": "CTCFL",
+          "score": -0.615594321,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5008,
+          "gene": "F8A2",
+          "score": -0.757835777,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5242,
+          "gene": "FAM49B",
+          "score": -2.014598466,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13833,
+          "gene": "SDCCAG8",
+          "score": -0.7172328170000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2081,
+          "gene": "CAMSAP3",
+          "score": -0.503657337,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12608,
+          "gene": "PTPN6",
+          "score": -0.742329297,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12504,
+          "gene": "PSMD1",
+          "score": -0.443164457,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15337,
+          "gene": "STX3",
+          "score": -0.369267661,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17338,
+          "gene": "VN1R1",
+          "score": -0.485805724,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8238,
+          "gene": "KRTAP2-4",
+          "score": -1.1155609,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18240,
+          "gene": "ZNF626",
+          "score": -0.48027414700000004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 377,
+          "gene": "ADRA2C",
+          "score": -0.514642412,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3779,
+          "gene": "CYP4X1",
+          "score": -0.55176932,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17704,
+          "gene": "ZBTB10",
+          "score": -1.454030435,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8805,
+          "gene": "LSM12",
+          "score": -2.058202489,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11220,
+          "gene": "PATE3",
+          "score": -1.255088674,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3681,
+          "gene": "CXCL5",
+          "score": -0.57877837,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9686,
+          "gene": "MS4A13",
+          "score": -0.6619021660000001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14341,
+          "gene": "SLC24A5",
+          "score": -1.198486086,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5215,
+          "gene": "FAM24B",
+          "score": -1.130251816,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14964,
+          "gene": "SPATA5",
+          "score": -0.547784346,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 106,
+          "gene": "ABRA",
+          "score": -0.213723146,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8690,
+          "gene": "LRMP",
+          "score": -1.582579036,
+          "hit": 0,
+          "round": 0
+        }
+      ]
+    }
+  }
+}
```
