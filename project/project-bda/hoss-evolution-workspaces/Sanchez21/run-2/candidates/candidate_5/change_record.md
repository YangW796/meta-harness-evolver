# Change Record — candidate_5

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21/run-2/best/current/harness
Generated at: 2026-04-30T07:23:39.227528

## Files Changed

- model.py: modified (added=70, deleted=54, delta=16)
- outputs/metrics.json: modified (added=2367, deleted=575, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -1,14 +1,15 @@
 from __future__ import annotations
 import random
 import numpy as np
+from collections import defaultdict
 
 def select(candidates, history, batch_size, seed) -> list[int]:
     """
-    Selection policy for Project-BDA.
-
+    Selection policy for Project-BDA using Thompson Sampling.
+    
     Contract (MUST KEEP EXACTLY):
         select(candidates, history, batch_size, seed) -> list[int]
-
+    
     Inputs:
     - candidates: list[dict]
         - single-gene datasets: each item includes {"gene": "<HGNC>"}
@@ -23,15 +24,14 @@
           - hit: int (0/1) if enabled by runner
     - batch_size: int
     - seed: int
-
+    
     Output:
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
-
-    You may implement any suitable algorithmic model here, including but not limited to:
-    traditional algorithms, machine learning models, deep learning models, biological models,
-    and mathematical models.
+    
+    Thompson Sampling implementation for perturbation search.
     """
     rng = random.Random(seed)
+    np.random.seed(seed)
     
     # Get already selected indices
     already_selected = {h['candidate_index'] for h in history}
@@ -45,56 +45,72 @@
         selected = rng.sample(available, min(batch_size, len(available)))
         return selected
     
-    # For subsequent rounds, use score-guided exploitation + exploration
+    # Thompson Sampling strategy
+    # Model each candidate's probability of being a hit using Beta distribution
+    # Success = hit (score <= threshold), Failure = non-hit
     
-    # Calculate selection strategy: 70% exploitation, 30% exploration
-    exploit_count = int(batch_size * 0.7)
-    explore_count = batch_size - exploit_count
+    # Determine hit threshold: use 5th percentile of absolute scores as cutoff for "extreme"
+    abs_scores = [abs(h['score']) for h in history]
+    hit_threshold = np.percentile(abs_scores, 95)  # Top 5% most extreme scores are hits
     
-    selected = []
+    # Count successes (hits) and failures (non-hits) for each candidate
+    # Since we can't track individual candidates that haven't been tested,
+    # we use a Bayesian approach with empirical priors
     
-    # Exploitation: Use weighted sampling based on absolute score distance from median
-    # This targets both extremes: very negative scores and near-zero scores
-    if exploit_count > 0 and len(history) > 0:
-        # Calculate absolute deviation from median for each historical candidate
-        scores = [h['score'] for h in history]
-        median_score = np.median(scores)
-        abs_deviations = [abs(h['score'] - median_score) for h in history]
+    # Calculate empirical hit rate from history
+    if 'hit' in history[0]:
+        # Use provided hit labels if available
+        total_hits = sum(1 for h in history if h['hit'] == 1)
+        total_trials = len(history)
+    else:
+        # Define hits as extreme scores (top 5% by absolute value)
+        total_hits = sum(1 for h in history if abs(h['score']) >= hit_threshold)
+        total_trials = len(history)
+    
+    empirical_hit_rate = total_hits / total_trials if total_trials > 0 else 0.05
+    
+    # Beta distribution parameters (Bayesian prior)
+    # Start with weak prior centered at empirical hit rate
+    alpha_prior = max(1, empirical_hit_rate * 10)  # Success count
+    beta_prior = max(1, (1 - empirical_hit_rate) * 10)  # Failure count
+    
+    # For each available candidate, sample from posterior
+    # Candidates with no history get sampled from prior
+    # Candidates with history get sampled from posterior (alpha + successes, beta + failures)
+    
+    # Group history by candidate to track per-candidate statistics
+    candidate_stats = defaultdict(lambda: {'successes': 0, 'trials': 0})
+    
+    for h in history:
+        idx = h['candidate_index']
+        if 'hit' in h:
+            is_hit = h['hit'] == 1
+        else:
+            is_hit = abs(h['score']) >= hit_threshold
         
-        # Create weights: higher deviation = higher weight
-        # Add small epsilon to avoid zero weights
-        weights = np.array(abs_deviations) + 1e-6
-        weights = weights / weights.sum()  # Normalize
+        candidate_stats[idx]['successes'] += int(is_hit)
+        candidate_stats[idx]['trials'] += 1
+    
+    # Sample theta (probability of being a hit) for each available candidate
+    sampled_probs = []
+    for idx in available:
+        if idx in candidate_stats:
+            # Posterior: Beta(alpha_prior + successes, beta_prior + failures)
+            successes = candidate_stats[idx]['successes']
+            failures = candidate_stats[idx]['trials'] - successes
+            alpha_post = alpha_prior + successes
+            beta_post = beta_prior + failures
+        else:
+            # Prior: Beta(alpha_prior, beta_prior)
+            alpha_post = alpha_prior
+            beta_post = beta_prior
         
-        # Sample candidate indices from history with replacement, weighted by score extremity
-        exploit_indices = np.random.choice(len(history), size=min(exploit_count * 3, len(history)), replace=True, p=weights)
-        
-        # Convert to actual selected indices from available pool
-        # Use the top exploit_count unique selections
-        exploit_set = set()
-        for idx in exploit_indices:
-            if len(exploit_set) >= exploit_count:
-                break
-            # Add the historically high-value candidate if still available
-            hist_idx = history[idx]['candidate_index']
-            if hist_idx in available:
-                exploit_set.add(hist_idx)
-        
-        # If we don't have enough from direct hits, supplement with candidates that have similar extreme scores
-        if len(exploit_set) < exploit_count:
-            # Sort available candidates by how extreme their scores would be
-            # We don't know actual scores, so we'll prioritize based on the distribution we've seen
-            # Use the weighted sampling to bias toward regions of the search space with extreme scores
-            remaining_needed = exploit_count - len(exploit_set)
-            supplemental = rng.sample(available, min(remaining_needed, len(available)))
-            exploit_set.update(supplemental)
-        
-        selected.extend(list(exploit_set))
-        available = [i for i in available if i not in selected]
+        # Sample from Beta distribution
+        theta = np.random.beta(alpha_post, beta_post)
+        sampled_probs.append((idx, theta))
     
-    # Exploration: random selection from remaining available
-    if explore_count > 0 and available:
-        explore_selection = rng.sample(available, min(explore_count, len(available)))
-        selected.extend(explore_selection)
+    # Sort by sampled probability (descending) and select top batch_size
+    sampled_probs.sort(key=lambda x: x[1], reverse=True)
+    selected = [idx for idx, _ in sampled_probs[:batch_size]]
     
-    return selected[:batch_size]+    return selected
```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18469,
-      "rounds": 3,
+      "rounds": 4,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 256,
-      "baseline_total_hits": 15,
+      "baseline_total_queries": 384,
+      "baseline_total_hits": 19,
       "delta_queries": 128,
-      "delta_hits": 4,
-      "total_queries": 384,
-      "total_hits": 19,
+      "delta_hits": 5,
+      "total_queries": 512,
+      "total_hits": 24,
       "top_k": 924,
       "hit_curve": {
         "queries": [
-          256,
-          384
+          384,
+          512
         ],
         "hits": [
-          15,
-          19
+          19,
+          24
         ]
       },
-      "auc": 2176.0,
-      "auc_normalized": 0.006132756132756133,
-      "ncg": 0.25412715881821035,
+      "auc": 2752.0,
+      "auc_normalized": 0.005817099567099567,
+      "ncg": 0.2695663262028463,
       "round_details": [
         {
-          "round": 2,
+          "round": 3,
           "selected_count": 128,
-          "hits": 4,
-          "cumulative_hits": 19,
-          "precision_at_batch": 0.03125,
+          "hits": 5,
+          "cumulative_hits": 24,
+          "precision_at_batch": 0.0390625,
           "selected": [
-            "PCDH19",
-            "CTBS",
-            "RALA",
-            "MEGF11",
-            "ZNF208",
-            "MTHFR",
-            "PCDHGA7",
-            "CAPN3",
-            "BPIFB2",
-            "KRTAP4-5",
-            "SLC27A4",
-            "CMTR2",
-            "PLK4",
-            "UBC",
-            "KCNJ16",
-            "ZNF280A",
-            "OR1M1",
-            "BRS3",
-            "FAM25G",
-            "FAM47E",
-            "CNPY3",
-            "ZNF345",
-            "CYBA",
-            "PNLIP",
-            "ATAD2",
-            "GPCPD1",
-            "SLC35F6",
-            "RPL4",
-            "ENO1",
-            "CYP19A1",
-            "RPP30",
-            "MICU1",
-            "CYP27C1",
-            "SLC39A8",
-            "UCN3",
-            "OR52N1",
-            "FAM92B",
-            "ACSBG2",
-            "PDZD3",
-            "MIR218-1",
-            "TMED4",
-            "GPR31",
-            "ACTRT1",
-            "POLR3F",
-            "ATP5L2",
-            "SPTB",
-            "PEX3",
-            "DPP3",
-            "NPTN",
-            "GAMT",
-            "INCA1",
-            "CORO7-PAM16",
-            "RTFDC1",
-            "MAN2A2",
-            "INPP4A",
-            "CCDC77",
-            "ADAT2",
-            "TBCCD1",
-            "PTK7",
-            "SRSF5",
-            "DCP2",
-            "ADCY9",
-            "GCC1",
-            "INTS7",
-            "IPO9",
-            "PTPRM",
-            "GDF3",
-            "MAPK3",
-            "NCK1",
-            "VAPB",
-            "TDGF1",
-            "CCT7",
-            "LOC100288336",
-            "FABP12",
-            "MB",
-            "BCCIP",
-            "MRPL43",
-            "BCL10",
-            "MRPL48",
-            "CD226",
-            "C9orf85",
-            "ARHGEF11",
-            "TEX35",
-            "AK2",
-            "HAS3",
-            "DHFR",
-            "TGFB1I1",
-            "VTA1",
-            "PRKACG",
-            "GRM3",
-            "CADM4",
-            "MGAT3",
-            "TMEM161A",
-            "LRRIQ4",
-            "CAV3",
-            "UGT3A2",
-            "OSTM1",
-            "ZNF630",
-            "TMEM62",
-            "CBWD3",
-            "MOCOS",
-            "TNFSF18",
-            "NARS",
-            "RPIA",
-            "RPRML",
-            "NDE1",
-            "ZNF675",
-            "SPINT2",
-            "CCRN4L",
-            "NUAK1",
-            "LEP",
-            "DUPD1",
-            "DUSP28",
-            "DUSP4",
-            "CD300LD",
-            "SNAI1",
-            "RLBP1",
-            "PGD",
-            "SNX16",
-            "CFD",
-            "MCM3",
-            "DYX1C1",
-            "MFGE8",
-            "ZDHHC7",
-            "TSTD2",
-            "PPIG",
-            "KRIT1",
-            "ASXL1"
+            "NME1-NME2",
+            "GCNT7",
+            "WDR13",
+            "USP28",
+            "TAS2R43",
+            "ATG2B",
+            "ATPAF1",
+            "OXSM",
+            "FYN",
+            "ARL14EP",
+            "PGA4",
+            "PPP1R14A",
+            "TTLL13P",
+            "YBEY",
+            "NAP1L3",
+            "IRAK1BP1",
+            "ZFYVE26",
+            "LY6G5C",
+            "OSTN",
+            "ANGPTL7",
+            "PLA2G2D",
+            "RBFOX2",
+            "DIDO1",
+            "IL18BP",
+            "COMMD3-BMI1",
+            "KLRC1",
+            "CHRNB1",
+            "CKAP4",
+            "PSD2",
+            "FEM1C",
+            "TEX36",
+            "CALML4",
+            "ZNF169",
+            "PARG",
+            "PRAC1",
+            "ISY1-RAB43",
+            "MUL1",
+            "DPYSL4",
+            "UBA3",
+            "A1BG",
+            "C1QL3",
+            "ITGA7",
+            "FRMPD4",
+            "TOMM5",
+            "LCORL",
+            "KCP",
+            "SLC30A9",
+            "PLEC",
+            "STK10",
+            "KRT75",
+            "NR5A1",
+            "LHB",
+            "CDKL1",
+            "GPR161",
+            "OR51V1",
+            "OR13F1",
+            "DEFB123",
+            "PCNX",
+            "SIRT4",
+            "WDR18",
+            "SPATA21",
+            "SECTM1",
+            "UCK2",
+            "KIAA1147",
+            "OR4D6",
+            "TPTE",
+            "RAB7A",
+            "NDUFC1",
+            "AXDND1",
+            "MROH5",
+            "GDF11",
+            "ELAVL3",
+            "LACTB",
+            "GJB3",
+            "RGCC",
+            "ADGRB3",
+            "PAPD4",
+            "C7orf60",
+            "UBL4B",
+            "XRN2",
+            "GABRA6",
+            "CASP8",
+            "DDX26B",
+            "CASQ2",
+            "UNKL",
+            "NRXN3",
+            "TMEM135",
+            "URGCP",
+            "CD40",
+            "ZNF415",
+            "C9orf43",
+            "SLC25A2",
+            "ME2",
+            "SPRYD3",
+            "GPX5",
+            "PROK1",
+            "ALDH1A1",
+            "NAA30",
+            "RPSA",
+            "LMOD2",
+            "HIST1H4J",
+            "ADIRF",
+            "CTSL",
+            "TUBB",
+            "OPRD1",
+            "MLLT11",
+            "SUPT4H1",
+            "CCDC43",
+            "OGFOD3",
+            "CCDC54",
+            "MMP12",
+            "TUBGCP3",
+            "MED12L",
+            "ATRX",
+            "NME8",
+            "OLIG2",
+            "LHCGR",
+            "CCDC23",
+            "VPS13C",
+            "USP22",
+            "HACD1",
+            "CCNE2",
+            "PSME2",
+            "LOC100130357",
+            "C15orf61",
+            "USP40",
+            "DGKZ",
+            "THAP6"
           ],
           "selected_scores": [
-            -0.17986812300000002,
-            -0.93184741,
-            -0.110080666,
-            -1.2621971570000001,
-            -1.4629832409999999,
-            -0.53056721,
-            -1.0357653359999999,
-            -1.516184917,
-            -2.4363128119999997,
-            -0.33412183100000004,
-            -0.909587081,
-            -0.867622597,
-            -0.649978527,
-            -1.242476262,
-            -1.535717328,
-            -0.7558665640000001,
-            -0.795292752,
-            -0.87202951,
-            -2.256070067,
-            -1.432234274,
-            -0.22900884300000002,
-            -0.7923046420000001,
-            -1.995410484,
-            -0.199076256,
-            -0.534442847,
-            -1.721282059,
-            -1.467071482,
-            -1.258452004,
-            -0.10322920699999999,
-            -0.9652608109999999,
-            -0.7923896229999999,
-            -0.709519401,
-            -0.307623705,
-            -0.134866984,
-            -2.0068613999999996,
-            -0.531539028,
-            -1.174618668,
-            -0.48418083700000003,
-            -0.655837214,
-            -0.527375421,
-            -0.557226137,
-            -0.692123335,
-            -0.982993062,
-            -1.553605335,
-            -0.9284767629999999,
-            -3.8845286530000003,
-            -0.5142025179999999,
-            -0.8456294670000001,
-            -0.605387434,
-            -0.084168268,
-            -1.809067376,
-            -0.47678603700000005,
-            -1.560368985,
-            -0.7152809309999999,
-            -0.718339979,
-            -1.112939553,
-            -0.181357057,
-            -0.476479091,
-            -0.381601255,
-            -0.642006444,
-            -1.34009841,
-            -0.494880649,
-            -1.429033762,
-            -1.232835635,
-            -0.26407106399999997,
-            -0.41914722200000004,
-            -0.49975885200000003,
-            -1.175905668,
-            -1.076478817,
-            -1.2703910729999999,
-            -0.674693352,
-            -0.704492129,
-            -1.12702237,
-            -0.672295058,
-            -0.727664667,
-            -1.442685503,
-            -0.815280817,
-            -0.553760464,
-            -0.373296909,
-            -0.191011193,
-            -0.9804685870000001,
-            -0.657764427,
-            -1.061614066,
-            -0.43550246600000003,
-            -0.366737059,
-            -0.757486294,
-            -0.040351722,
-            -1.3761129980000002,
-            -1.236471839,
-            -0.352056585,
-            -0.66884535,
-            -0.671983824,
-            -2.472286256,
-            -0.26448087600000003,
-            -1.242797965,
-            -1.61152489,
-            -0.430547529,
-            -0.665419244,
-            -0.978275274,
-            -0.71276899,
-            -0.63995502,
-            -0.330687015,
-            -1.347113393,
-            -0.196614078,
-            -0.7978009709999999,
-            -1.70578438,
-            -0.47199178,
-            -0.0279334,
-            -1.149630254,
-            -0.472024826,
-            -1.021180824,
-            -1.021444857,
-            -0.212464882,
-            -2.4841461369999998,
-            -0.854753243,
-            -1.0884399340000002,
-            -1.160592356,
-            -2.3963191669999997,
-            -0.251794205,
-            -0.799418519,
-            -0.6152584329999999,
-            -1.117229415,
-            -0.667099899,
-            -1.3195440059999999,
-            -2.175362109,
-            -0.39313499,
-            -0.105699421,
-            -1.6404002359999998
+            -1.252376862,
+            -1.130409573,
+            -0.579604031,
+            -1.9408592219999998,
+            -0.7690243920000001,
+            -0.522969989,
+            -0.431048416,
+            -1.02200561,
+            -0.553065424,
+            -2.514422038,
+            -1.21730499,
+            -0.8179465890000001,
+            -0.634314348,
+            -2.786154409,
+            -0.407763396,
+            -0.9398003690000001,
+            -0.372685094,
+            -0.318525723,
+            -1.1873366859999999,
+            -0.289779722,
+            -0.927758228,
+            -3.0662884110000004,
+            -0.723933217,
+            -0.486887536,
+            -0.915257034,
+            -0.38570152399999996,
+            -0.42443180700000005,
+            -2.426025611,
+            -1.0767421670000001,
+            -1.094949631,
+            -1.897738465,
+            -0.16702054,
+            -0.299119788,
+            -1.3004787309999999,
+            -0.324149058,
+            -1.7229893680000001,
+            -1.281810851,
+            -0.70596755,
+            -1.258182508,
+            -0.647879494,
+            -1.3134030859999999,
+            -1.050882249,
+            -0.664000867,
+            -0.44174283,
+            -0.779742258,
+            -0.186406336,
+            -1.943041834,
+            -0.61110757,
+            -0.27322778,
+            -0.394239315,
+            -0.293616439,
+            -0.860142352,
+            -0.369850744,
+            -0.252635276,
+            -1.04319805,
+            -0.586772938,
+            -0.293965018,
+            -2.133285068,
+            -1.017002884,
+            -1.198067149,
+            -0.197048698,
+            -1.524477391,
+            -1.149611377,
+            -0.952481221,
+            -0.638508901,
+            -1.157818853,
+            -0.22361947899999998,
+            -0.388434302,
+            -0.557943778,
+            -0.497022199,
+            -0.16245242699999998,
+            -2.235131436,
+            -0.342449141,
+            -0.452751506,
+            -1.819849609,
+            -0.644022821,
+            -0.63254356,
+            -0.546959614,
+            -0.272564456,
+            -1.717150005,
+            -0.618924252,
+            -0.199460704,
+            -0.804941424,
+            -0.36187630299999995,
+            -1.108885959,
+            -0.6669470820000001,
+            -0.740893565,
+            -0.185063468,
+            -0.42681243799999996,
+            -0.5908581479999999,
+            -0.450731823,
+            -1.4831636780000002,
+            -1.2989149359999999,
+            -0.322876479,
+            -0.5226422310000001,
+            -1.339272014,
+            -0.25224885199999997,
+            -1.1603423240000001,
+            -0.606878867,
+            -0.005625323000000001,
+            -0.5233276,
+            -0.47789446,
+            -0.22282050399999997,
+            -1.632472006,
+            -1.250168197,
+            -0.24958256,
+            -0.543690539,
+            -2.700329584,
+            -1.1147389429999999,
+            -0.432676499,
+            -0.783165918,
+            -1.4851813109999998,
+            -1.314870408,
+            -0.977257395,
+            -0.487122008,
+            -0.935724372,
+            -0.27970373800000004,
+            -0.7098399040000001,
+            -2.874831861,
+            -0.768402252,
+            -0.938923101,
+            -0.546079632,
+            -1.979114035,
+            -0.795854176,
+            -0.49082078100000004,
+            -0.6683689660000001,
+            -0.499025348,
+            -0.7007373840000001
           ],
           "selected_hits": [
             0,
@@ -314,42 +314,14 @@
             0,
             0,
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
             1,
             0,
             0,
             0,
+            0,
+            0,
+            0,
+            0,
             1,
             0,
             0,
@@ -387,6 +359,47 @@
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
             1,
             0,
             0,
@@ -395,19 +408,6 @@
             0,
             0,
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
             0,
@@ -419,7 +419,7 @@
             0,
             0,
             0,
-            0,
+            1,
             0,
             0,
             0,
@@ -2230,896 +2230,1792 @@
           "gene": "PCDH19",
           "score": -0.17986812300000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3589,
           "gene": "CTBS",
           "score": -0.93184741,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12832,
           "gene": "RALA",
           "score": -0.110080666,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9251,
           "gene": "MEGF11",
           "score": -1.2621971570000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17960,
           "gene": "ZNF208",
           "score": -1.4629832409999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9770,
           "gene": "MTHFR",
           "score": -0.53056721,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11309,
           "gene": "PCDHGA7",
           "score": -1.0357653359999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2099,
           "gene": "CAPN3",
           "score": -1.516184917,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1592,
           "gene": "BPIFB2",
           "score": -2.4363128119999997,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8251,
           "gene": "KRTAP4-5",
           "score": -0.33412183100000004,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14404,
           "gene": "SLC27A4",
           "score": -0.909587081,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3150,
           "gene": "CMTR2",
           "score": -0.867622597,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11857,
           "gene": "PLK4",
           "score": -0.649978527,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16980,
           "gene": "UBC",
           "score": -1.242476262,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7765,
           "gene": "KCNJ16",
           "score": -1.535717328,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18007,
           "gene": "ZNF280A",
           "score": -0.7558665640000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10841,
           "gene": "OR1M1",
           "score": -0.795292752,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1633,
           "gene": "BRS3",
           "score": -0.87202951,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5219,
           "gene": "FAM25G",
           "score": -2.256070067,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5239,
           "gene": "FAM47E",
           "score": -1.432234274,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3193,
           "gene": "CNPY3",
           "score": -0.22900884300000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18048,
           "gene": "ZNF345",
           "score": -0.7923046420000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3718,
           "gene": "CYBA",
           "score": -1.995410484,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11911,
           "gene": "PNLIP",
           "score": -0.199076256,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1160,
           "gene": "ATAD2",
           "score": -0.534442847,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6280,
           "gene": "GPCPD1",
           "score": -1.721282059,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14470,
           "gene": "SLC35F6",
           "score": -1.467071482,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13451,
           "gene": "RPL4",
           "score": -1.258452004,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4754,
           "gene": "ENO1",
           "score": -0.10322920699999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3734,
           "gene": "CYP19A1",
           "score": -0.9652608109999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13468,
           "gene": "RPP30",
           "score": -0.7923896229999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9374,
           "gene": "MICU1",
           "score": -0.709519401,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3746,
           "gene": "CYP27C1",
           "score": -0.307623705,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14507,
           "gene": "SLC39A8",
           "score": -0.134866984,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17069,
           "gene": "UCN3",
           "score": -2.0068613999999996,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10926,
           "gene": "OR52N1",
           "score": -0.531539028,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5298,
           "gene": "FAM92B",
           "score": -1.174618668,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 178,
           "gene": "ACSBG2",
           "score": -0.48418083700000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11454,
           "gene": "PDZD3",
           "score": -0.655837214,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9407,
           "gene": "MIR218-1",
           "score": -0.527375421,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16064,
           "gene": "TMED4",
           "score": -0.557226137,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6346,
           "gene": "GPR31",
           "score": -0.692123335,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 223,
           "gene": "ACTRT1",
           "score": -0.982993062,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12000,
           "gene": "POLR3F",
           "score": -1.553605335,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1254,
           "gene": "ATP5L2",
           "score": -0.9284767629999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15080,
           "gene": "SPTB",
           "score": -3.8845286530000003,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11499,
           "gene": "PEX3",
           "score": -0.5142025179999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4335,
           "gene": "DPP3",
           "score": -0.8456294670000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10488,
           "gene": "NPTN",
           "score": -0.605387434,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5882,
           "gene": "GAMT",
           "score": -0.084168268,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7428,
           "gene": "INCA1",
           "score": -1.809067376,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3337,
           "gene": "CORO7-PAM16",
           "score": -0.47678603700000005,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13583,
           "gene": "RTFDC1",
           "score": -1.560368985,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8985,
           "gene": "MAN2A2",
           "score": -0.7152809309999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7449,
           "gene": "INPP4A",
           "score": -0.718339979,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2331,
           "gene": "CCDC77",
           "score": -1.112939553,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 291,
           "gene": "ADAT2",
           "score": -0.181357057,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15652,
           "gene": "TBCCD1",
           "score": -0.476479091,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12584,
           "gene": "PTK7",
           "score": -0.381601255,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15146,
           "gene": "SRSF5",
           "score": -0.642006444,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3888,
           "gene": "DCP2",
           "score": -1.34009841,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 307,
           "gene": "ADCY9",
           "score": -0.494880649,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5940,
           "gene": "GCC1",
           "score": -1.429033762,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7480,
           "gene": "INTS7",
           "score": -1.232835635,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7496,
           "gene": "IPO9",
           "score": -0.26407106399999997,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12622,
           "gene": "PTPRM",
           "score": -0.41914722200000004,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5974,
           "gene": "GDF3",
           "score": -0.49975885200000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9053,
           "gene": "MAPK3",
           "score": -1.175905668,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10078,
           "gene": "NCK1",
           "score": -1.076478817,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17277,
           "gene": "VAPB",
           "score": -1.2703910729999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15753,
           "gene": "TDGF1",
           "score": -0.674693352,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2447,
           "gene": "CCT7",
           "score": -0.704492129,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8592,
           "gene": "LOC100288336",
           "score": -1.12702237,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5015,
           "gene": "FABP12",
           "score": -0.672295058,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9118,
           "gene": "MB",
           "score": -0.727664667,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1441,
           "gene": "BCCIP",
           "score": -1.442685503,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9635,
           "gene": "MRPL43",
           "score": -0.815280817,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1447,
           "gene": "BCL10",
           "score": -0.553760464,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9640,
           "gene": "MRPL48",
           "score": -0.373296909,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2476,
           "gene": "CD226",
           "score": -0.191011193,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1968,
           "gene": "C9orf85",
           "score": -0.9804685870000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 963,
           "gene": "ARHGEF11",
           "score": -0.657764427,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15824,
           "gene": "TEX35",
           "score": -1.061614066,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 482,
           "gene": "AK2",
           "score": -0.43550246600000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6626,
           "gene": "HAS3",
           "score": -0.366737059,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4080,
           "gene": "DHFR",
           "score": -0.757486294,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15862,
           "gene": "TGFB1I1",
           "score": -0.040351722,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17398,
           "gene": "VTA1",
           "score": -1.3761129980000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12284,
           "gene": "PRKACG",
           "score": -1.236471839,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6452,
           "gene": "GRM3",
           "score": -0.352056585,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2035,
           "gene": "CADM4",
           "score": -0.66884535,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9346,
           "gene": "MGAT3",
           "score": -0.671983824,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16136,
           "gene": "TMEM161A",
           "score": -2.472286256,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8783,
           "gene": "LRRIQ4",
           "score": -0.26448087600000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2173,
           "gene": "CAV3",
           "score": -1.242797965,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17104,
           "gene": "UGT3A2",
           "score": -1.61152489,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11026,
           "gene": "OSTM1",
           "score": -0.430547529,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18244,
           "gene": "ZNF630",
           "score": -0.665419244,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16285,
           "gene": "TMEM62",
           "score": -0.978275274,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2191,
           "gene": "CBWD3",
           "score": -0.71276899,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9506,
           "gene": "MOCOS",
           "score": -0.63995502,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16402,
           "gene": "TNFSF18",
           "score": -0.330687015,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10030,
           "gene": "NARS",
           "score": -1.347113393,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13409,
           "gene": "RPIA",
           "score": -0.196614078,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13475,
           "gene": "RPRML",
           "score": -0.7978009709999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10105,
           "gene": "NDE1",
           "score": -1.70578438,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18270,
           "gene": "ZNF675",
           "score": -0.47199178,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15027,
           "gene": "SPINT2",
           "score": -0.0279334,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2436,
           "gene": "CCRN4L",
           "score": -1.149630254,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10610,
           "gene": "NUAK1",
           "score": -0.472024826,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8432,
           "gene": "LEP",
           "score": -1.021180824,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4416,
           "gene": "DUPD1",
           "score": -1.021444857,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4437,
           "gene": "DUSP28",
           "score": -0.212464882,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4439,
           "gene": "DUSP4",
           "score": -2.4841461369999998,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2490,
           "gene": "CD300LD",
           "score": -0.854753243,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14757,
           "gene": "SNAI1",
           "score": -1.0884399340000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13237,
           "gene": "RLBP1",
           "score": -1.160592356,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11539,
           "gene": "PGD",
           "score": -2.3963191669999997,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14817,
           "gene": "SNX16",
           "score": -0.251794205,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2818,
           "gene": "CFD",
           "score": -0.799418519,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9170,
           "gene": "MCM3",
           "score": -0.6152584329999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4475,
           "gene": "DYX1C1",
           "score": -1.117229415,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9320,
           "gene": "MFGE8",
           "score": -0.667099899,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17809,
           "gene": "ZDHHC7",
           "score": -1.3195440059999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16802,
           "gene": "TSTD2",
           "score": -2.175362109,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12100,
           "gene": "PPIG",
           "score": -0.39313499,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8134,
           "gene": "KRIT1",
           "score": -0.105699421,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1155,
           "gene": "ASXL1",
           "score": -1.6404002359999998,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 10364,
+          "gene": "NME1-NME2",
+          "score": -1.252376862,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5959,
+          "gene": "GCNT7",
+          "score": -1.130409573,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17448,
+          "gene": "WDR13",
+          "score": -0.579604031,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17211,
+          "gene": "USP28",
+          "score": -1.9408592219999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15594,
+          "gene": "TAS2R43",
+          "score": -0.7690243920000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1186,
+          "gene": "ATG2B",
+          "score": -0.522969989,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1293,
+          "gene": "ATPAF1",
+          "score": -0.431048416,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11068,
+          "gene": "OXSM",
+          "score": -1.02200561,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5783,
+          "gene": "FYN",
+          "score": -0.553065424,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1005,
+          "gene": "ARL14EP",
+          "score": -2.514422038,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11524,
+          "gene": "PGA4",
+          "score": -1.21730499,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12134,
+          "gene": "PPP1R14A",
+          "score": -0.8179465890000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16855,
+          "gene": "TTLL13P",
+          "score": -0.634314348,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17643,
+          "gene": "YBEY",
+          "score": -2.786154409,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 10018,
+          "gene": "NAP1L3",
+          "score": -0.407763396,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7522,
+          "gene": "IRAK1BP1",
+          "score": -0.9398003690000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17859,
+          "gene": "ZFYVE26",
+          "score": -0.372685094,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8850,
+          "gene": "LY6G5C",
+          "score": -0.318525723,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11027,
+          "gene": "OSTN",
+          "score": -1.1873366859999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 663,
+          "gene": "ANGPTL7",
+          "score": -0.289779722,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11757,
+          "gene": "PLA2G2D",
+          "score": -0.927758228,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12936,
+          "gene": "RBFOX2",
+          "score": -3.0662884110000004,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 4120,
+          "gene": "DIDO1",
+          "score": -0.723933217,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7347,
+          "gene": "IL18BP",
+          "score": -0.486887536,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3293,
+          "gene": "COMMD3-BMI1",
+          "score": -0.915257034,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8093,
+          "gene": "KLRC1",
+          "score": -0.38570152399999996,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2930,
+          "gene": "CHRNB1",
+          "score": -0.42443180700000005,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2989,
+          "gene": "CKAP4",
+          "score": -2.426025611,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12460,
+          "gene": "PSD2",
+          "score": -1.0767421670000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5461,
+          "gene": "FEM1C",
+          "score": -1.094949631,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15825,
+          "gene": "TEX36",
+          "score": -1.897738465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2055,
+          "gene": "CALML4",
+          "score": -0.16702054,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17939,
+          "gene": "ZNF169",
+          "score": -0.299119788,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11192,
+          "gene": "PARG",
+          "score": -1.3004787309999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12209,
+          "gene": "PRAC1",
+          "score": -0.324149058,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7570,
+          "gene": "ISY1-RAB43",
+          "score": -1.7229893680000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9832,
+          "gene": "MUL1",
+          "score": -1.281810851,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4357,
+          "gene": "DPYSL4",
+          "score": -0.70596755,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16964,
+          "gene": "UBA3",
+          "score": -1.258182508,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 0,
+          "gene": "A1BG",
+          "score": -0.647879494,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1802,
+          "gene": "C1QL3",
+          "score": -1.3134030859999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7585,
+          "gene": "ITGA7",
+          "score": -1.050882249,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5714,
+          "gene": "FRMPD4",
+          "score": -0.664000867,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16454,
+          "gene": "TOMM5",
+          "score": -0.44174283,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8394,
+          "gene": "LCORL",
+          "score": -0.779742258,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7811,
+          "gene": "KCP",
+          "score": -0.186406336,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14438,
+          "gene": "SLC30A9",
+          "score": -1.943041834,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11809,
+          "gene": "PLEC",
+          "score": -0.61110757,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15270,
+          "gene": "STK10",
+          "score": -0.27322778,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8177,
+          "gene": "KRT75",
+          "score": -0.394239315,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10523,
+          "gene": "NR5A1",
+          "score": -0.293616439,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8466,
+          "gene": "LHB",
+          "score": -0.860142352,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2643,
+          "gene": "CDKL1",
+          "score": -0.369850744,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6326,
+          "gene": "GPR161",
+          "score": -0.252635276,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10914,
+          "gene": "OR51V1",
+          "score": -1.04319805,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10825,
+          "gene": "OR13F1",
+          "score": -0.586772938,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4005,
+          "gene": "DEFB123",
+          "score": -0.293965018,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11342,
+          "gene": "PCNX",
+          "score": -2.133285068,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14205,
+          "gene": "SIRT4",
+          "score": -1.017002884,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17450,
+          "gene": "WDR18",
+          "score": -1.198067149,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14948,
+          "gene": "SPATA21",
+          "score": -0.197048698,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13886,
+          "gene": "SECTM1",
+          "score": -1.524477391,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17064,
+          "gene": "UCK2",
+          "score": -1.149611377,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7905,
+          "gene": "KIAA1147",
+          "score": -0.952481221,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10883,
+          "gene": "OR4D6",
+          "score": -0.638508901,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16534,
+          "gene": "TPTE",
+          "score": -1.157818853,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12778,
+          "gene": "RAB7A",
+          "score": -0.22361947899999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10155,
+          "gene": "NDUFC1",
+          "score": -0.388434302,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1332,
+          "gene": "AXDND1",
+          "score": -0.557943778,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9597,
+          "gene": "MROH5",
+          "score": -0.497022199,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5971,
+          "gene": "GDF11",
+          "score": -0.16245242699999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4672,
+          "gene": "ELAVL3",
+          "score": -2.235131436,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8299,
+          "gene": "LACTB",
+          "score": -0.342449141,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6074,
+          "gene": "GJB3",
+          "score": -0.452751506,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13117,
+          "gene": "RGCC",
+          "score": -1.819849609,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 319,
+          "gene": "ADGRB3",
+          "score": -0.644022821,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11168,
+          "gene": "PAPD4",
+          "score": -0.63254356,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1904,
+          "gene": "C7orf60",
+          "score": -0.546959614,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17029,
+          "gene": "UBL4B",
+          "score": -0.272564456,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17632,
+          "gene": "XRN2",
+          "score": -1.717150005,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5822,
+          "gene": "GABRA6",
+          "score": -0.618924252,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2153,
+          "gene": "CASP8",
+          "score": -0.199460704,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3944,
+          "gene": "DDX26B",
+          "score": -0.804941424,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2157,
+          "gene": "CASQ2",
+          "score": -0.36187630299999995,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17143,
+          "gene": "UNKL",
+          "score": -1.108885959,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10558,
+          "gene": "NRXN3",
+          "score": -0.6669470820000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16111,
+          "gene": "TMEM135",
+          "score": -0.740893565,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17172,
+          "gene": "URGCP",
+          "score": -0.185063468,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2505,
+          "gene": "CD40",
+          "score": -0.42681243799999996,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18081,
+          "gene": "ZNF415",
+          "score": -0.5908581479999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1957,
+          "gene": "C9orf43",
+          "score": -0.450731823,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14353,
+          "gene": "SLC25A2",
+          "score": -1.4831636780000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9205,
+          "gene": "ME2",
+          "score": -1.2989149359999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15071,
+          "gene": "SPRYD3",
+          "score": -0.322876479,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6396,
+          "gene": "GPX5",
+          "score": -0.5226422310000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12336,
+          "gene": "PROK1",
+          "score": -1.339272014,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 535,
+          "gene": "ALDH1A1",
+          "score": -0.25224885199999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9976,
+          "gene": "NAA30",
+          "score": -1.1603423240000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13519,
+          "gene": "RPSA",
+          "score": -0.606878867,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8567,
+          "gene": "LMOD2",
+          "score": -0.005625323000000001,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 6843,
+          "gene": "HIST1H4J",
+          "score": -0.5233276,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 355,
+          "gene": "ADIRF",
+          "score": -0.47789446,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3631,
+          "gene": "CTSL",
+          "score": -0.22282050399999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16881,
+          "gene": "TUBB",
+          "score": -1.632472006,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10794,
+          "gene": "OPRD1",
+          "score": -1.250168197,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9443,
+          "gene": "MLLT11",
+          "score": -0.24958256,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15396,
+          "gene": "SUPT4H1",
+          "score": -0.543690539,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2303,
+          "gene": "CCDC43",
+          "score": -2.700329584,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 10751,
+          "gene": "OGFOD3",
+          "score": -1.1147389429999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2308,
+          "gene": "CCDC54",
+          "score": -0.432676499,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9466,
+          "gene": "MMP12",
+          "score": -0.783165918,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16895,
+          "gene": "TUBGCP3",
+          "score": -1.4851813109999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9216,
+          "gene": "MED12L",
+          "score": -1.314870408,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1301,
+          "gene": "ATRX",
+          "score": -0.977257395,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10371,
+          "gene": "NME8",
+          "score": -0.487122008,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10770,
+          "gene": "OLIG2",
+          "score": -0.935724372,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8467,
+          "gene": "LHCGR",
+          "score": -0.27970373800000004,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2286,
+          "gene": "CCDC23",
+          "score": -0.7098399040000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17350,
+          "gene": "VPS13C",
+          "score": -2.874831861,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17206,
+          "gene": "USP22",
+          "score": -0.768402252,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6599,
+          "gene": "HACD1",
+          "score": -0.938923101,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2406,
+          "gene": "CCNE2",
+          "score": -0.546079632,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12519,
+          "gene": "PSME2",
+          "score": -1.979114035,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8581,
+          "gene": "LOC100130357",
+          "score": -0.795854176,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1733,
+          "gene": "C15orf61",
+          "score": -0.49082078100000004,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17225,
+          "gene": "USP40",
+          "score": -0.6683689660000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4074,
+          "gene": "DGKZ",
+          "score": -0.499025348,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15894,
+          "gene": "THAP6",
+          "score": -0.7007373840000001,
+          "hit": 0,
+          "round": 3
         }
       ],
       "queried_history": [
@@ -4920,896 +5816,1792 @@
           "gene": "PCDH19",
           "score": -0.17986812300000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3589,
           "gene": "CTBS",
           "score": -0.93184741,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12832,
           "gene": "RALA",
           "score": -0.110080666,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9251,
           "gene": "MEGF11",
           "score": -1.2621971570000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17960,
           "gene": "ZNF208",
           "score": -1.4629832409999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9770,
           "gene": "MTHFR",
           "score": -0.53056721,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11309,
           "gene": "PCDHGA7",
           "score": -1.0357653359999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2099,
           "gene": "CAPN3",
           "score": -1.516184917,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1592,
           "gene": "BPIFB2",
           "score": -2.4363128119999997,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8251,
           "gene": "KRTAP4-5",
           "score": -0.33412183100000004,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14404,
           "gene": "SLC27A4",
           "score": -0.909587081,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3150,
           "gene": "CMTR2",
           "score": -0.867622597,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11857,
           "gene": "PLK4",
           "score": -0.649978527,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16980,
           "gene": "UBC",
           "score": -1.242476262,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7765,
           "gene": "KCNJ16",
           "score": -1.535717328,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18007,
           "gene": "ZNF280A",
           "score": -0.7558665640000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10841,
           "gene": "OR1M1",
           "score": -0.795292752,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1633,
           "gene": "BRS3",
           "score": -0.87202951,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5219,
           "gene": "FAM25G",
           "score": -2.256070067,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5239,
           "gene": "FAM47E",
           "score": -1.432234274,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3193,
           "gene": "CNPY3",
           "score": -0.22900884300000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18048,
           "gene": "ZNF345",
           "score": -0.7923046420000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3718,
           "gene": "CYBA",
           "score": -1.995410484,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11911,
           "gene": "PNLIP",
           "score": -0.199076256,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1160,
           "gene": "ATAD2",
           "score": -0.534442847,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6280,
           "gene": "GPCPD1",
           "score": -1.721282059,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14470,
           "gene": "SLC35F6",
           "score": -1.467071482,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13451,
           "gene": "RPL4",
           "score": -1.258452004,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4754,
           "gene": "ENO1",
           "score": -0.10322920699999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3734,
           "gene": "CYP19A1",
           "score": -0.9652608109999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13468,
           "gene": "RPP30",
           "score": -0.7923896229999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9374,
           "gene": "MICU1",
           "score": -0.709519401,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3746,
           "gene": "CYP27C1",
           "score": -0.307623705,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14507,
           "gene": "SLC39A8",
           "score": -0.134866984,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17069,
           "gene": "UCN3",
           "score": -2.0068613999999996,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10926,
           "gene": "OR52N1",
           "score": -0.531539028,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5298,
           "gene": "FAM92B",
           "score": -1.174618668,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 178,
           "gene": "ACSBG2",
           "score": -0.48418083700000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11454,
           "gene": "PDZD3",
           "score": -0.655837214,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9407,
           "gene": "MIR218-1",
           "score": -0.527375421,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16064,
           "gene": "TMED4",
           "score": -0.557226137,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6346,
           "gene": "GPR31",
           "score": -0.692123335,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 223,
           "gene": "ACTRT1",
           "score": -0.982993062,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12000,
           "gene": "POLR3F",
           "score": -1.553605335,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1254,
           "gene": "ATP5L2",
           "score": -0.9284767629999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15080,
           "gene": "SPTB",
           "score": -3.8845286530000003,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11499,
           "gene": "PEX3",
           "score": -0.5142025179999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4335,
           "gene": "DPP3",
           "score": -0.8456294670000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10488,
           "gene": "NPTN",
           "score": -0.605387434,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5882,
           "gene": "GAMT",
           "score": -0.084168268,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7428,
           "gene": "INCA1",
           "score": -1.809067376,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3337,
           "gene": "CORO7-PAM16",
           "score": -0.47678603700000005,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13583,
           "gene": "RTFDC1",
           "score": -1.560368985,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8985,
           "gene": "MAN2A2",
           "score": -0.7152809309999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7449,
           "gene": "INPP4A",
           "score": -0.718339979,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2331,
           "gene": "CCDC77",
           "score": -1.112939553,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 291,
           "gene": "ADAT2",
           "score": -0.181357057,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15652,
           "gene": "TBCCD1",
           "score": -0.476479091,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12584,
           "gene": "PTK7",
           "score": -0.381601255,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15146,
           "gene": "SRSF5",
           "score": -0.642006444,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3888,
           "gene": "DCP2",
           "score": -1.34009841,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 307,
           "gene": "ADCY9",
           "score": -0.494880649,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5940,
           "gene": "GCC1",
           "score": -1.429033762,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7480,
           "gene": "INTS7",
           "score": -1.232835635,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7496,
           "gene": "IPO9",
           "score": -0.26407106399999997,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12622,
           "gene": "PTPRM",
           "score": -0.41914722200000004,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5974,
           "gene": "GDF3",
           "score": -0.49975885200000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9053,
           "gene": "MAPK3",
           "score": -1.175905668,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10078,
           "gene": "NCK1",
           "score": -1.076478817,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17277,
           "gene": "VAPB",
           "score": -1.2703910729999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15753,
           "gene": "TDGF1",
           "score": -0.674693352,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2447,
           "gene": "CCT7",
           "score": -0.704492129,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8592,
           "gene": "LOC100288336",
           "score": -1.12702237,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5015,
           "gene": "FABP12",
           "score": -0.672295058,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9118,
           "gene": "MB",
           "score": -0.727664667,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1441,
           "gene": "BCCIP",
           "score": -1.442685503,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9635,
           "gene": "MRPL43",
           "score": -0.815280817,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1447,
           "gene": "BCL10",
           "score": -0.553760464,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9640,
           "gene": "MRPL48",
           "score": -0.373296909,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2476,
           "gene": "CD226",
           "score": -0.191011193,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1968,
           "gene": "C9orf85",
           "score": -0.9804685870000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 963,
           "gene": "ARHGEF11",
           "score": -0.657764427,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15824,
           "gene": "TEX35",
           "score": -1.061614066,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 482,
           "gene": "AK2",
           "score": -0.43550246600000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6626,
           "gene": "HAS3",
           "score": -0.366737059,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4080,
           "gene": "DHFR",
           "score": -0.757486294,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15862,
           "gene": "TGFB1I1",
           "score": -0.040351722,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17398,
           "gene": "VTA1",
           "score": -1.3761129980000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12284,
           "gene": "PRKACG",
           "score": -1.236471839,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6452,
           "gene": "GRM3",
           "score": -0.352056585,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2035,
           "gene": "CADM4",
           "score": -0.66884535,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9346,
           "gene": "MGAT3",
           "score": -0.671983824,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16136,
           "gene": "TMEM161A",
           "score": -2.472286256,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8783,
           "gene": "LRRIQ4",
           "score": -0.26448087600000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2173,
           "gene": "CAV3",
           "score": -1.242797965,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17104,
           "gene": "UGT3A2",
           "score": -1.61152489,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11026,
           "gene": "OSTM1",
           "score": -0.430547529,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18244,
           "gene": "ZNF630",
           "score": -0.665419244,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16285,
           "gene": "TMEM62",
           "score": -0.978275274,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2191,
           "gene": "CBWD3",
           "score": -0.71276899,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9506,
           "gene": "MOCOS",
           "score": -0.63995502,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16402,
           "gene": "TNFSF18",
           "score": -0.330687015,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10030,
           "gene": "NARS",
           "score": -1.347113393,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13409,
           "gene": "RPIA",
           "score": -0.196614078,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13475,
           "gene": "RPRML",
           "score": -0.7978009709999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10105,
           "gene": "NDE1",
           "score": -1.70578438,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18270,
           "gene": "ZNF675",
           "score": -0.47199178,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15027,
           "gene": "SPINT2",
           "score": -0.0279334,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2436,
           "gene": "CCRN4L",
           "score": -1.149630254,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10610,
           "gene": "NUAK1",
           "score": -0.472024826,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8432,
           "gene": "LEP",
           "score": -1.021180824,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4416,
           "gene": "DUPD1",
           "score": -1.021444857,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4437,
           "gene": "DUSP28",
           "score": -0.212464882,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4439,
           "gene": "DUSP4",
           "score": -2.4841461369999998,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2490,
           "gene": "CD300LD",
           "score": -0.854753243,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14757,
           "gene": "SNAI1",
           "score": -1.0884399340000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13237,
           "gene": "RLBP1",
           "score": -1.160592356,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11539,
           "gene": "PGD",
           "score": -2.3963191669999997,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14817,
           "gene": "SNX16",
           "score": -0.251794205,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2818,
           "gene": "CFD",
           "score": -0.799418519,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9170,
           "gene": "MCM3",
           "score": -0.6152584329999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4475,
           "gene": "DYX1C1",
           "score": -1.117229415,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9320,
           "gene": "MFGE8",
           "score": -0.667099899,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17809,
           "gene": "ZDHHC7",
           "score": -1.3195440059999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16802,
           "gene": "TSTD2",
           "score": -2.175362109,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12100,
           "gene": "PPIG",
           "score": -0.39313499,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8134,
           "gene": "KRIT1",
           "score": -0.105699421,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1155,
           "gene": "ASXL1",
           "score": -1.6404002359999998,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 10364,
+          "gene": "NME1-NME2",
+          "score": -1.252376862,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5959,
+          "gene": "GCNT7",
+          "score": -1.130409573,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17448,
+          "gene": "WDR13",
+          "score": -0.579604031,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17211,
+          "gene": "USP28",
+          "score": -1.9408592219999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15594,
+          "gene": "TAS2R43",
+          "score": -0.7690243920000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1186,
+          "gene": "ATG2B",
+          "score": -0.522969989,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1293,
+          "gene": "ATPAF1",
+          "score": -0.431048416,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11068,
+          "gene": "OXSM",
+          "score": -1.02200561,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5783,
+          "gene": "FYN",
+          "score": -0.553065424,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1005,
+          "gene": "ARL14EP",
+          "score": -2.514422038,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11524,
+          "gene": "PGA4",
+          "score": -1.21730499,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12134,
+          "gene": "PPP1R14A",
+          "score": -0.8179465890000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16855,
+          "gene": "TTLL13P",
+          "score": -0.634314348,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17643,
+          "gene": "YBEY",
+          "score": -2.786154409,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 10018,
+          "gene": "NAP1L3",
+          "score": -0.407763396,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7522,
+          "gene": "IRAK1BP1",
+          "score": -0.9398003690000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17859,
+          "gene": "ZFYVE26",
+          "score": -0.372685094,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8850,
+          "gene": "LY6G5C",
+          "score": -0.318525723,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11027,
+          "gene": "OSTN",
+          "score": -1.1873366859999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 663,
+          "gene": "ANGPTL7",
+          "score": -0.289779722,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11757,
+          "gene": "PLA2G2D",
+          "score": -0.927758228,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12936,
+          "gene": "RBFOX2",
+          "score": -3.0662884110000004,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 4120,
+          "gene": "DIDO1",
+          "score": -0.723933217,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7347,
+          "gene": "IL18BP",
+          "score": -0.486887536,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3293,
+          "gene": "COMMD3-BMI1",
+          "score": -0.915257034,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8093,
+          "gene": "KLRC1",
+          "score": -0.38570152399999996,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2930,
+          "gene": "CHRNB1",
+          "score": -0.42443180700000005,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2989,
+          "gene": "CKAP4",
+          "score": -2.426025611,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12460,
+          "gene": "PSD2",
+          "score": -1.0767421670000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5461,
+          "gene": "FEM1C",
+          "score": -1.094949631,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15825,
+          "gene": "TEX36",
+          "score": -1.897738465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2055,
+          "gene": "CALML4",
+          "score": -0.16702054,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17939,
+          "gene": "ZNF169",
+          "score": -0.299119788,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11192,
+          "gene": "PARG",
+          "score": -1.3004787309999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12209,
+          "gene": "PRAC1",
+          "score": -0.324149058,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7570,
+          "gene": "ISY1-RAB43",
+          "score": -1.7229893680000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9832,
+          "gene": "MUL1",
+          "score": -1.281810851,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4357,
+          "gene": "DPYSL4",
+          "score": -0.70596755,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16964,
+          "gene": "UBA3",
+          "score": -1.258182508,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 0,
+          "gene": "A1BG",
+          "score": -0.647879494,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1802,
+          "gene": "C1QL3",
+          "score": -1.3134030859999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7585,
+          "gene": "ITGA7",
+          "score": -1.050882249,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5714,
+          "gene": "FRMPD4",
+          "score": -0.664000867,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16454,
+          "gene": "TOMM5",
+          "score": -0.44174283,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8394,
+          "gene": "LCORL",
+          "score": -0.779742258,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7811,
+          "gene": "KCP",
+          "score": -0.186406336,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14438,
+          "gene": "SLC30A9",
+          "score": -1.943041834,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11809,
+          "gene": "PLEC",
+          "score": -0.61110757,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15270,
+          "gene": "STK10",
+          "score": -0.27322778,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8177,
+          "gene": "KRT75",
+          "score": -0.394239315,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10523,
+          "gene": "NR5A1",
+          "score": -0.293616439,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8466,
+          "gene": "LHB",
+          "score": -0.860142352,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2643,
+          "gene": "CDKL1",
+          "score": -0.369850744,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6326,
+          "gene": "GPR161",
+          "score": -0.252635276,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10914,
+          "gene": "OR51V1",
+          "score": -1.04319805,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10825,
+          "gene": "OR13F1",
+          "score": -0.586772938,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4005,
+          "gene": "DEFB123",
+          "score": -0.293965018,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11342,
+          "gene": "PCNX",
+          "score": -2.133285068,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14205,
+          "gene": "SIRT4",
+          "score": -1.017002884,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17450,
+          "gene": "WDR18",
+          "score": -1.198067149,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14948,
+          "gene": "SPATA21",
+          "score": -0.197048698,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13886,
+          "gene": "SECTM1",
+          "score": -1.524477391,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17064,
+          "gene": "UCK2",
+          "score": -1.149611377,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7905,
+          "gene": "KIAA1147",
+          "score": -0.952481221,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10883,
+          "gene": "OR4D6",
+          "score": -0.638508901,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16534,
+          "gene": "TPTE",
+          "score": -1.157818853,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12778,
+          "gene": "RAB7A",
+          "score": -0.22361947899999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10155,
+          "gene": "NDUFC1",
+          "score": -0.388434302,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1332,
+          "gene": "AXDND1",
+          "score": -0.557943778,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9597,
+          "gene": "MROH5",
+          "score": -0.497022199,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5971,
+          "gene": "GDF11",
+          "score": -0.16245242699999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4672,
+          "gene": "ELAVL3",
+          "score": -2.235131436,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8299,
+          "gene": "LACTB",
+          "score": -0.342449141,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6074,
+          "gene": "GJB3",
+          "score": -0.452751506,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13117,
+          "gene": "RGCC",
+          "score": -1.819849609,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 319,
+          "gene": "ADGRB3",
+          "score": -0.644022821,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11168,
+          "gene": "PAPD4",
+          "score": -0.63254356,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1904,
+          "gene": "C7orf60",
+          "score": -0.546959614,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17029,
+          "gene": "UBL4B",
+          "score": -0.272564456,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17632,
+          "gene": "XRN2",
+          "score": -1.717150005,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5822,
+          "gene": "GABRA6",
+          "score": -0.618924252,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2153,
+          "gene": "CASP8",
+          "score": -0.199460704,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3944,
+          "gene": "DDX26B",
+          "score": -0.804941424,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2157,
+          "gene": "CASQ2",
+          "score": -0.36187630299999995,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17143,
+          "gene": "UNKL",
+          "score": -1.108885959,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10558,
+          "gene": "NRXN3",
+          "score": -0.6669470820000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16111,
+          "gene": "TMEM135",
+          "score": -0.740893565,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17172,
+          "gene": "URGCP",
+          "score": -0.185063468,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2505,
+          "gene": "CD40",
+          "score": -0.42681243799999996,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18081,
+          "gene": "ZNF415",
+          "score": -0.5908581479999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1957,
+          "gene": "C9orf43",
+          "score": -0.450731823,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14353,
+          "gene": "SLC25A2",
+          "score": -1.4831636780000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9205,
+          "gene": "ME2",
+          "score": -1.2989149359999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15071,
+          "gene": "SPRYD3",
+          "score": -0.322876479,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6396,
+          "gene": "GPX5",
+          "score": -0.5226422310000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12336,
+          "gene": "PROK1",
+          "score": -1.339272014,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 535,
+          "gene": "ALDH1A1",
+          "score": -0.25224885199999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9976,
+          "gene": "NAA30",
+          "score": -1.1603423240000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13519,
+          "gene": "RPSA",
+          "score": -0.606878867,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8567,
+          "gene": "LMOD2",
+          "score": -0.005625323000000001,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 6843,
+          "gene": "HIST1H4J",
+          "score": -0.5233276,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 355,
+          "gene": "ADIRF",
+          "score": -0.47789446,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3631,
+          "gene": "CTSL",
+          "score": -0.22282050399999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16881,
+          "gene": "TUBB",
+          "score": -1.632472006,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10794,
+          "gene": "OPRD1",
+          "score": -1.250168197,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9443,
+          "gene": "MLLT11",
+          "score": -0.24958256,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15396,
+          "gene": "SUPT4H1",
+          "score": -0.543690539,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2303,
+          "gene": "CCDC43",
+          "score": -2.700329584,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 10751,
+          "gene": "OGFOD3",
+          "score": -1.1147389429999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2308,
+          "gene": "CCDC54",
+          "score": -0.432676499,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9466,
+          "gene": "MMP12",
+          "score": -0.783165918,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16895,
+          "gene": "TUBGCP3",
+          "score": -1.4851813109999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9216,
+          "gene": "MED12L",
+          "score": -1.314870408,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1301,
+          "gene": "ATRX",
+          "score": -0.977257395,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10371,
+          "gene": "NME8",
+          "score": -0.487122008,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10770,
+          "gene": "OLIG2",
+          "score": -0.935724372,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8467,
+          "gene": "LHCGR",
+          "score": -0.27970373800000004,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2286,
+          "gene": "CCDC23",
+          "score": -0.7098399040000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17350,
+          "gene": "VPS13C",
+          "score": -2.874831861,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17206,
+          "gene": "USP22",
+          "score": -0.768402252,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6599,
+          "gene": "HACD1",
+          "score": -0.938923101,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2406,
+          "gene": "CCNE2",
+          "score": -0.546079632,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12519,
+          "gene": "PSME2",
+          "score": -1.979114035,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8581,
+          "gene": "LOC100130357",
+          "score": -0.795854176,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1733,
+          "gene": "C15orf61",
+          "score": -0.49082078100000004,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17225,
+          "gene": "USP40",
+          "score": -0.6683689660000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4074,
+          "gene": "DGKZ",
+          "score": -0.499025348,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15894,
+          "gene": "THAP6",
+          "score": -0.7007373840000001,
+          "hit": 0,
+          "round": 3
         }
       ]
     }

```
