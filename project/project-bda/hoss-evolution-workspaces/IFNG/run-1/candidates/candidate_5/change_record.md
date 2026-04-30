# Change Record — candidate_5

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IFNG/run-1/best/current/harness
Generated at: 2026-04-30T06:48:15.718835

## Files Changed

- model.py: modified (added=57, deleted=48, delta=9)
- outputs/metrics.json: modified (added=2354, deleted=562, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -27,9 +27,10 @@
     Output:
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
     
-    Strategy: Upper Confidence Bound (UCB) for balancing exploration and exploitation.
+    Strategy: Thompson Sampling with Beta distribution for balancing exploration and exploitation.
     """
     rng = random.Random(seed)
+    np.random.seed(seed)
     
     # Get all candidate indices
     all_indices = list(range(len(candidates)))
@@ -40,67 +41,75 @@
     # Get available indices (not yet selected)
     available_indices = [i for i in all_indices if i not in selected_indices]
     
-    # If no history or all scores are equal, use random selection
+    # If no history, use random selection
     if not history:
         selected = available_indices[:batch_size]
         rng.shuffle(selected)
         return selected[:batch_size]
     
-    # Build score estimates for each candidate
-    # Group history by candidate index
-    candidate_scores = {}
-    candidate_counts = {}
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
     
     for h in history:
         idx = h['candidate_index']
         score = h['score']
-        if idx not in candidate_scores:
-            candidate_scores[idx] = 0.0
-            candidate_counts[idx] = 0
-        candidate_scores[idx] += score
-        candidate_counts[idx] += 1
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
     
-    # Calculate average scores for explored candidates
-    candidate_avg_scores = {}
-    for idx in candidate_scores:
-        candidate_avg_scores[idx] = candidate_scores[idx] / candidate_counts[idx]
-    
-    # Calculate total number of observations for UCB exploration bonus
-    total_observations = len(history)
-    
-    # For each available candidate, calculate UCB score
-    # UCB = mean + sqrt(2 * ln(total_observations) / count)
-    # For unexplored candidates, count = 1 for optimistic initialization
-    ucb_scores = []
-    
-    # Calculate min and max observed scores for exploration
-    min_observed_score = min(candidate_avg_scores.values()) if candidate_avg_scores else 0
-    max_observed_score = max(candidate_avg_scores.values()) if candidate_avg_scores else 0
+    # For Thompson Sampling, we sample from Beta(alpha, beta) for each candidate
+    # where alpha = successes + 1, beta = failures + 1 (add-1 smoothing for uninformed prior)
+    thompson_samples = []
     
     for idx in available_indices:
-        if idx in candidate_avg_scores:
-            # Explored candidate
-            mean_score = candidate_avg_scores[idx]
-            count = candidate_counts[idx]
-            exploration_bonus = np.sqrt(2 * np.log(total_observations) / count) if total_observations > 0 else 0
-            ucb = mean_score + exploration_bonus
+        if idx in candidate_successes:
+            # Explored candidate: use observed successes/failures
+            alpha = candidate_successes[idx] + 1
+            beta = candidate_failures[idx] + 1
         else:
-            # Unexplored candidate - use optimistic initialization
-            # Explore both extremes: favor candidates that could be very negative (hits) or very positive
-            # Use a mixture of min and max with higher weight on min since hits are negative
-            if candidate_avg_scores:
-                # Bias exploration toward negative scores (hits are at -0.4 to -0.5)
-                ucb_negative = min_observed_score - 0.1 * abs(min_observed_score) if min_observed_score != 0 else -1.0
-                ucb_positive = max_observed_score + 0.1 * abs(max_observed_score) if max_observed_score != 0 else 1.0
-                # Blend: 80% weight on negative exploration (hits), 20% on positive
-                ucb = 0.8 * ucb_negative + 0.2 * ucb_positive
-            else:
-                ucb = -1.0  # Start with negative bias for unexplored
-        ucb_scores.append((ucb, idx))
+            # Unexplored candidate: use optimistic prior
+            # Bias toward exploration of potentially good candidates (hits)
+            # Use alpha > beta to favor success (finding hits)
+            alpha = 3  # Higher alpha = more optimistic about success
+            beta = 1
+        
+        # Sample from Beta distribution
+        sample = np.random.beta(alpha, beta)
+        thompson_samples.append((sample, idx))
     
-    # Sort by UCB score (descending) and select top batch_size
-    ucb_scores.sort(reverse=True)
-    selected = [idx for _, idx in ucb_scores[:batch_size]]
+    # Sort by Thompson sample (descending) and select top batch_size
+    thompson_samples.sort(reverse=True)
+    selected = [idx for _, idx in thompson_samples[:batch_size]]
     
     # Shuffle to avoid bias in case of ties
     rng.shuffle(selected)

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18418,
-      "rounds": 4,
+      "rounds": 5,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 384,
-      "baseline_total_hits": 8,
+      "baseline_total_queries": 512,
+      "baseline_total_hits": 9,
       "delta_queries": 128,
-      "delta_hits": 1,
-      "total_queries": 512,
-      "total_hits": 9,
+      "delta_hits": 3,
+      "total_queries": 640,
+      "total_hits": 12,
       "top_k": 920,
       "hit_curve": {
         "queries": [
-          384,
-          512
+          512,
+          640
         ],
         "hits": [
-          8,
-          9
+          9,
+          12
         ]
       },
-      "auc": 1088.0,
-      "auc_normalized": 0.0023097826086956523,
-      "ncg": 0.18526733430524442,
+      "auc": 1344.0,
+      "auc_normalized": 0.002282608695652174,
+      "ncg": 0.20117929780159263,
       "round_details": [
         {
-          "round": 3,
+          "round": 4,
           "selected_count": 128,
-          "hits": 1,
-          "cumulative_hits": 9,
-          "precision_at_batch": 0.0078125,
+          "hits": 3,
+          "cumulative_hits": 12,
+          "precision_at_batch": 0.0234375,
           "selected": [
-            "ZNF585A",
-            "ZNF524",
-            "ZNF552",
-            "ZNF449",
-            "ZNF500",
-            "ZNF431",
-            "ZNF496",
-            "ZNF436",
-            "ZNF530",
-            "ZNF471",
-            "ZNF511-PRAP1",
-            "ZNF550",
-            "ZNF569",
-            "ZNF577",
-            "ZNF534",
-            "ZNF443",
-            "ZNF490",
-            "ZNF548",
-            "ZNF445",
-            "ZNF511",
-            "ZNF582",
-            "ZNF486",
-            "ZNF492",
-            "ZNF512B",
-            "ZNF540",
-            "ZNF514",
-            "ZNF438",
-            "ZNF570",
-            "ZNF442",
-            "ZNF461",
-            "ZNF517",
-            "ZNF575",
-            "ZNF536",
-            "ZNF594",
-            "ZNF573",
-            "ZNF547",
-            "ZNF462",
-            "ZNF600",
-            "ZNF502",
-            "ZNF433",
-            "ZNF43",
-            "ZNF578",
-            "ZNF485",
-            "ZNF566",
-            "ZNF460",
-            "ZNF506",
-            "ZNF467",
-            "ZNF45",
-            "ZNF441",
-            "ZNF446",
-            "ZNF512",
-            "ZNF597",
-            "ZNF532",
-            "ZNF541",
-            "ZNF595",
-            "ZNF564",
-            "ZNF57",
-            "ZNF526",
-            "ZNF480",
-            "ZNF440",
-            "ZNF430",
-            "ZNF574",
-            "ZNF521",
-            "ZNF516",
-            "ZNF562",
-            "ZNF473",
-            "ZNF513",
-            "ZNF568",
-            "ZNF503",
-            "ZNF444",
-            "ZNF555",
-            "ZNF572",
-            "ZNF551",
-            "ZNF527",
-            "ZNF479",
-            "ZNF493",
-            "ZNF518B",
-            "ZNF519",
-            "ZNF549",
-            "ZNF497",
-            "ZNF557",
-            "ZNF439",
-            "ZNF586",
-            "ZNF469",
-            "ZNF585B",
-            "ZNF559",
-            "ZNF554",
-            "ZNF432",
-            "ZNF558",
-            "ZNF576",
-            "ZNF454",
-            "ZNF593",
-            "ZNF491",
-            "ZNF580",
-            "ZNF546",
-            "ZNF510",
-            "ZNF44",
-            "ZNF543",
-            "ZNF488",
-            "ZNF48",
-            "ZNF571",
-            "ZNF579",
-            "ZNF484",
-            "ZNF470",
-            "ZNF565",
-            "ZNF581",
-            "ZNF592",
-            "ZNF507",
-            "ZNF596",
-            "ZNF501",
-            "ZNF483",
-            "ZNF451",
-            "ZNF560",
-            "ZNF583",
-            "ZNF468",
-            "ZNF563",
-            "ZNF584",
-            "ZNF599",
-            "ZNF529",
-            "ZNF589",
-            "ZNF598",
-            "ZNF556",
-            "ZNF561",
-            "ZNF587",
-            "ZNF567",
-            "ZNF528",
-            "ZNF544",
-            "ZNF518A"
+            "SCN3A",
+            "PIP4P2",
+            "EARS2",
+            "TMEM160",
+            "DLEU7",
+            "C5orf22",
+            "VRTN",
+            "P2RY6",
+            "RNASE12",
+            "CAT",
+            "MPC2",
+            "SPATA31C2",
+            "B4GALT5",
+            "PDCL3",
+            "FRRS1L",
+            "OR2T10",
+            "SLC1A7",
+            "ZMYND12",
+            "TAF3",
+            "PHKB",
+            "SDR42E2",
+            "IFNA4",
+            "PTPRA",
+            "DCUN1D1",
+            "CIRBP",
+            "ERI3",
+            "GALK2",
+            "CHMP5",
+            "PMP2",
+            "KCNA4",
+            "RAG1",
+            "FGR",
+            "FABP1",
+            "PCDHB4",
+            "CD14",
+            "PPM1G",
+            "PRKRA",
+            "RETNLB",
+            "PARPBP",
+            "TPCN1",
+            "TAC4",
+            "KRTAP5-7",
+            "PAQR5",
+            "OR2T29",
+            "SHQ1",
+            "ANKRD46",
+            "PTK2",
+            "PP2D1",
+            "UNC93B1",
+            "PAPSS2",
+            "SLC16A10",
+            "GCNT1",
+            "MAP3K9",
+            "MSTN",
+            "TNFRSF11B",
+            "OR4A47",
+            "RASSF8",
+            "IL31RA",
+            "FAM209B",
+            "DEUP1",
+            "PTER",
+            "LRIG1",
+            "KRTAP10-12",
+            "NEK8",
+            "PASD1",
+            "SEC61A1",
+            "FRMD6",
+            "VSX1",
+            "NGLY1",
+            "FKBP8",
+            "CBY2",
+            "APRT",
+            "ORM1",
+            "CCNB2",
+            "ITGA4",
+            "ZFTA",
+            "CFAP126",
+            "PPARD",
+            "OSGEPL1",
+            "SPINK5",
+            "DEFB119",
+            "PTGIS",
+            "DNAI4",
+            "RASSF3",
+            "RPIA",
+            "DRD1",
+            "RFLNA",
+            "KIR3DL3",
+            "OSGIN1",
+            "ANKRD24",
+            "PIK3IP1",
+            "ETF1",
+            "ATP11AUN",
+            "TFAP2D",
+            "TRIM5",
+            "GALNT8",
+            "CAPN15",
+            "POLE4",
+            "DMWD",
+            "C16orf54",
+            "TRIM69",
+            "PCDHB3",
+            "ADGRG2",
+            "STRN4",
+            "C2",
+            "SNX8",
+            "EIF2D",
+            "CCDC39",
+            "TDRD5",
+            "BNIPL",
+            "BUD31",
+            "ITLN1",
+            "MGAT5B",
+            "CHGA",
+            "TOR4A",
+            "MRPL51",
+            "MCL1",
+            "OR2A12",
+            "UMAD1",
+            "PPP1R2",
+            "OR14A16",
+            "HPSE2",
+            "RHOC",
+            "VSIG10L2",
+            "NT5DC1",
+            "MAPK13",
+            "DNAAF1",
+            "HACD3"
           ],
           "selected_scores": [
-            -0.029175,
-            0.1740205,
-            -0.18224,
-            0.02156985,
-            0.128354,
-            0.181045,
-            0.13378,
-            -0.22501,
-            0.111831,
-            0.16659,
-            0.101215,
-            0.0015315,
-            -0.2065345,
-            0.352155,
-            -0.1037915,
-            -0.1002155,
-            -0.0520515,
-            0.14674175,
-            0.185425,
-            -0.087807,
-            0.053413,
-            -0.01275,
-            0.2519605,
-            -0.13953,
-            0.096929,
-            0.0049065,
-            0.094816,
-            0.00226,
-            0.1677725,
-            -0.26366,
-            0.071871,
-            -0.32484,
-            0.201145,
-            -0.02139,
-            -0.1773585,
-            0.0528285,
-            -0.04815,
-            -0.13736,
-            0.009245,
-            -0.176507,
-            -0.1845355,
-            -0.15319,
-            0.271345,
-            -0.3362,
-            -0.092895,
-            -0.113433,
-            0.072695,
-            0.1424945,
-            -0.164674,
-            -0.061245,
-            -0.0526845,
-            -0.39098,
-            0.0522465,
-            -0.18417965,
-            -0.025711,
-            0.1820195,
-            0.103895,
-            0.137245,
-            0.24194,
-            -0.087465,
-            0.08786,
-            0.16361,
-            0.08589,
-            0.25173,
-            -0.3011635,
-            0.0156455,
-            0.01218,
-            0.0717735,
-            0.23489,
-            -0.0704355,
-            0.145655,
-            0.041181,
-            0.0350655,
-            0.0058345,
-            0.0278175,
-            0.009985,
-            0.31276,
-            -0.0857705,
-            0.22809,
-            0.000715,
-            0.264625,
-            -0.237145,
-            -0.198565,
-            0.051955,
-            -0.183071,
-            0.19544,
-            -0.250545,
-            -0.0355025,
-            0.006585,
-            0.389825,
-            0.11075185,
-            -0.0711965,
-            -0.035655,
-            0.234024,
-            -0.005505,
-            -0.184205,
-            -0.11366,
-            0.37438,
-            0.039261,
-            0.0807835,
-            0.077155,
-            0.026342,
-            -0.059251,
-            -0.1913,
-            -0.140035,
-            -0.0562255,
-            0.0864995,
-            0.037163,
-            0.376185,
-            -0.0899685,
-            0.1860085,
-            -0.06424,
-            0.0112985,
-            -0.05593,
-            -0.0068665,
-            0.168275,
-            0.337285,
-            -0.1666685,
-            -0.0121575,
-            -0.1166215,
-            -0.152225,
-            0.05136365,
-            0.29338,
-            0.052138,
-            0.03971,
-            0.037025,
-            -0.0599985,
-            -0.2550815
+            -0.329865,
+            -0.341205,
+            -0.09780015,
+            -0.2169725,
+            0.025105,
+            -0.22257,
+            0.0977705,
+            0.2081295,
+            0.010242834,
+            0.043525,
+            0.0071113,
+            0.2683855,
+            -0.348185,
+            0.06847715,
+            0.016505,
+            -0.0880425,
+            0.04237285,
+            -0.0982155,
+            0.020675,
+            0.013254,
+            -0.2481805,
+            -0.03555,
+            -0.04744875,
+            -0.0414515,
+            0.0841915,
+            0.183812,
+            -0.16022725,
+            0.42015,
+            -0.16301,
+            0.03668925,
+            0.03867,
+            0.32395,
+            -0.16277,
+            -0.51529,
+            -0.11622,
+            -0.0833035,
+            0.25402626,
+            0.05045863,
+            -0.131243,
+            0.08007,
+            -0.1659785,
+            -0.047770675,
+            0.1059,
+            -0.346245,
+            -0.03321,
+            0.353385,
+            -0.097984,
+            0.07194625,
+            -0.0559315,
+            0.0683462,
+            0.091323,
+            -0.05849,
+            3.5e-05,
+            0.21826,
+            -0.052113,
+            -0.189292,
+            0.113495,
+            0.02396,
+            -0.145942,
+            0.011269,
+            0.2438895,
+            0.3103475,
+            -0.357157,
+            0.045132,
+            0.0095975,
+            -1.24095,
+            0.17515,
+            -0.095107,
+            0.0902385,
+            -0.02692,
+            0.03145,
+            0.066691,
+            0.071057,
+            -0.106655,
+            0.0571885,
+            0.295155,
+            0.1851,
+            -0.1182605,
+            0.029674,
+            0.1756,
+            0.062365,
+            -0.09387,
+            -0.20582,
+            0.285485,
+            -0.03165,
+            -0.100129,
+            0.105329,
+            0.004392,
+            0.1050995,
+            -0.05942,
+            0.0774005,
+            -0.2975425,
+            -0.21638,
+            0.339235,
+            -0.238896,
+            -0.18248,
+            -0.0278715,
+            0.115658,
+            -0.1336994,
+            0.108705,
+            0.041445,
+            -0.032855,
+            0.384941,
+            0.09592,
+            -0.006035,
+            0.34474,
+            -0.16068,
+            0.093614,
+            0.168175,
+            0.03104265,
+            -0.0926225,
+            -0.0415915,
+            -0.0492,
+            -0.0912605,
+            -0.112765,
+            0.09959825,
+            -0.0620235,
+            0.13195,
+            0.161218,
+            -0.1042185,
+            0.050317,
+            0.112994,
+            -0.174285,
+            0.044635,
+            0.01987,
+            0.1460872,
+            -0.158985,
+            0.054218
           ],
           "selected_hits": [
             0,
@@ -328,45 +328,45 @@
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
             1,
             0,
             0,
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
+            1,
             0,
             0,
             0,
@@ -3126,896 +3126,1792 @@
           "gene": "ZNF585A",
           "score": -0.029175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18096,
           "gene": "ZNF524",
           "score": 0.1740205,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18115,
           "gene": "ZNF552",
           "score": -0.18224,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18050,
           "gene": "ZNF449",
           "score": 0.02156985,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18077,
           "gene": "ZNF500",
           "score": 0.128354,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18036,
           "gene": "ZNF431",
           "score": 0.181045,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18075,
           "gene": "ZNF496",
           "score": 0.13378,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18039,
           "gene": "ZNF436",
           "score": -0.22501,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18101,
           "gene": "ZNF530",
           "score": 0.111831,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18061,
           "gene": "ZNF471",
           "score": 0.16659,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18085,
           "gene": "ZNF511-PRAP1",
           "score": 0.101215,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18113,
           "gene": "ZNF550",
           "score": 0.0015315,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18131,
           "gene": "ZNF569",
           "score": -0.2065345,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18140,
           "gene": "ZNF577",
           "score": 0.352155,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18103,
           "gene": "ZNF534",
           "score": -0.1037915,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18046,
           "gene": "ZNF443",
           "score": -0.1002155,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18071,
           "gene": "ZNF490",
           "score": -0.0520515,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18111,
           "gene": "ZNF548",
           "score": 0.14674175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18048,
           "gene": "ZNF445",
           "score": 0.185425,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18084,
           "gene": "ZNF511",
           "score": -0.087807,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18145,
           "gene": "ZNF582",
           "score": 0.053413,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18069,
           "gene": "ZNF486",
           "score": -0.01275,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18073,
           "gene": "ZNF492",
           "score": 0.2519605,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18087,
           "gene": "ZNF512B",
           "score": -0.13953,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18105,
           "gene": "ZNF540",
           "score": 0.096929,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18089,
           "gene": "ZNF514",
           "score": 0.0049065,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18040,
           "gene": "ZNF438",
           "score": 0.094816,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18133,
           "gene": "ZNF570",
           "score": 0.00226,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18045,
           "gene": "ZNF442",
           "score": 0.1677725,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18055,
           "gene": "ZNF461",
           "score": -0.26366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18091,
           "gene": "ZNF517",
           "score": 0.071871,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18138,
           "gene": "ZNF575",
           "score": -0.32484,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18104,
           "gene": "ZNF536",
           "score": 0.201145,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18155,
           "gene": "ZNF594",
           "score": -0.02139,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18136,
           "gene": "ZNF573",
           "score": -0.1773585,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18110,
           "gene": "ZNF547",
           "score": 0.0528285,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18056,
           "gene": "ZNF462",
           "score": -0.04815,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18161,
           "gene": "ZNF600",
           "score": -0.13736,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18079,
           "gene": "ZNF502",
           "score": 0.009245,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18038,
           "gene": "ZNF433",
           "score": -0.176507,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18034,
           "gene": "ZNF43",
           "score": -0.1845355,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18141,
           "gene": "ZNF578",
           "score": -0.15319,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18068,
           "gene": "ZNF485",
           "score": 0.271345,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18128,
           "gene": "ZNF566",
           "score": -0.3362,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18054,
           "gene": "ZNF460",
           "score": -0.092895,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18081,
           "gene": "ZNF506",
           "score": -0.113433,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18057,
           "gene": "ZNF467",
           "score": 0.072695,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18051,
           "gene": "ZNF45",
           "score": 0.1424945,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18044,
           "gene": "ZNF441",
           "score": -0.164674,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18049,
           "gene": "ZNF446",
           "score": -0.061245,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18086,
           "gene": "ZNF512",
           "score": -0.0526845,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18158,
           "gene": "ZNF597",
           "score": -0.39098,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18102,
           "gene": "ZNF532",
           "score": 0.0522465,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18106,
           "gene": "ZNF541",
           "score": -0.18417965,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18156,
           "gene": "ZNF595",
           "score": -0.025711,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18126,
           "gene": "ZNF564",
           "score": 0.1820195,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18132,
           "gene": "ZNF57",
           "score": 0.103895,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18097,
           "gene": "ZNF526",
           "score": 0.137245,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18065,
           "gene": "ZNF480",
           "score": 0.24194,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18043,
           "gene": "ZNF440",
           "score": -0.087465,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18035,
           "gene": "ZNF430",
           "score": 0.08786,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18137,
           "gene": "ZNF574",
           "score": 0.16361,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18095,
           "gene": "ZNF521",
           "score": 0.08589,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18090,
           "gene": "ZNF516",
           "score": 0.25173,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18124,
           "gene": "ZNF562",
           "score": -0.3011635,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18062,
           "gene": "ZNF473",
           "score": 0.0156455,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18088,
           "gene": "ZNF513",
           "score": 0.01218,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18130,
           "gene": "ZNF568",
           "score": 0.0717735,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18080,
           "gene": "ZNF503",
           "score": 0.23489,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18047,
           "gene": "ZNF444",
           "score": -0.0704355,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18117,
           "gene": "ZNF555",
           "score": 0.145655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18135,
           "gene": "ZNF572",
           "score": 0.041181,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18114,
           "gene": "ZNF551",
           "score": 0.0350655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18098,
           "gene": "ZNF527",
           "score": 0.0058345,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18063,
           "gene": "ZNF479",
           "score": 0.0278175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18074,
           "gene": "ZNF493",
           "score": 0.009985,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18093,
           "gene": "ZNF518B",
           "score": 0.31276,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18094,
           "gene": "ZNF519",
           "score": -0.0857705,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18112,
           "gene": "ZNF549",
           "score": 0.22809,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18076,
           "gene": "ZNF497",
           "score": 0.000715,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18119,
           "gene": "ZNF557",
           "score": 0.264625,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18041,
           "gene": "ZNF439",
           "score": -0.237145,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18150,
           "gene": "ZNF586",
           "score": -0.198565,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18059,
           "gene": "ZNF469",
           "score": 0.051955,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18149,
           "gene": "ZNF585B",
           "score": -0.183071,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18121,
           "gene": "ZNF559",
           "score": 0.19544,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18116,
           "gene": "ZNF554",
           "score": -0.250545,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18037,
           "gene": "ZNF432",
           "score": -0.0355025,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18120,
           "gene": "ZNF558",
           "score": 0.006585,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18139,
           "gene": "ZNF576",
           "score": 0.389825,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18053,
           "gene": "ZNF454",
           "score": 0.11075185,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18154,
           "gene": "ZNF593",
           "score": -0.0711965,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18072,
           "gene": "ZNF491",
           "score": -0.035655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18143,
           "gene": "ZNF580",
           "score": 0.234024,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18109,
           "gene": "ZNF546",
           "score": -0.005505,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18083,
           "gene": "ZNF510",
           "score": -0.184205,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18042,
           "gene": "ZNF44",
           "score": -0.11366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18107,
           "gene": "ZNF543",
           "score": 0.37438,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18070,
           "gene": "ZNF488",
           "score": 0.039261,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18064,
           "gene": "ZNF48",
           "score": 0.0807835,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18134,
           "gene": "ZNF571",
           "score": 0.077155,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18142,
           "gene": "ZNF579",
           "score": 0.026342,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18067,
           "gene": "ZNF484",
           "score": -0.059251,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18060,
           "gene": "ZNF470",
           "score": -0.1913,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18127,
           "gene": "ZNF565",
           "score": -0.140035,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18144,
           "gene": "ZNF581",
           "score": -0.0562255,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18153,
           "gene": "ZNF592",
           "score": 0.0864995,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18082,
           "gene": "ZNF507",
           "score": 0.037163,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18157,
           "gene": "ZNF596",
           "score": 0.376185,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18078,
           "gene": "ZNF501",
           "score": -0.0899685,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18066,
           "gene": "ZNF483",
           "score": 0.1860085,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18052,
           "gene": "ZNF451",
           "score": -0.06424,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18122,
           "gene": "ZNF560",
           "score": 0.0112985,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18146,
           "gene": "ZNF583",
           "score": -0.05593,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18058,
           "gene": "ZNF468",
           "score": -0.0068665,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18125,
           "gene": "ZNF563",
           "score": 0.168275,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18147,
           "gene": "ZNF584",
           "score": 0.337285,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18160,
           "gene": "ZNF599",
           "score": -0.1666685,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18100,
           "gene": "ZNF529",
           "score": -0.0121575,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18152,
           "gene": "ZNF589",
           "score": -0.1166215,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18159,
           "gene": "ZNF598",
           "score": -0.152225,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18118,
           "gene": "ZNF556",
           "score": 0.05136365,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18123,
           "gene": "ZNF561",
           "score": 0.29338,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18151,
           "gene": "ZNF587",
           "score": 0.052138,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18129,
           "gene": "ZNF567",
           "score": 0.03971,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18099,
           "gene": "ZNF528",
           "score": 0.037025,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18108,
           "gene": "ZNF544",
           "score": -0.0599985,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18092,
           "gene": "ZNF518A",
           "score": -0.2550815,
           "hit": 0,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 13776,
+          "gene": "SCN3A",
+          "score": -0.329865,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11729,
+          "gene": "PIP4P2",
+          "score": -0.341205,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4520,
+          "gene": "EARS2",
+          "score": -0.09780015,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16114,
+          "gene": "TMEM160",
+          "score": -0.2169725,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4180,
+          "gene": "DLEU7",
+          "score": 0.025105,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1931,
+          "gene": "C5orf22",
+          "score": -0.22257,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17348,
+          "gene": "VRTN",
+          "score": 0.0977705,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11126,
+          "gene": "P2RY6",
+          "score": 0.2081295,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13248,
+          "gene": "RNASE12",
+          "score": 0.010242834,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2189,
+          "gene": "CAT",
+          "score": 0.043525,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9394,
+          "gene": "MPC2",
+          "score": 0.0071113,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14926,
+          "gene": "SPATA31C2",
+          "score": 0.2683855,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1352,
+          "gene": "B4GALT5",
+          "score": -0.348185,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11413,
+          "gene": "PDCL3",
+          "score": 0.06847715,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5645,
+          "gene": "FRRS1L",
+          "score": 0.016505,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10789,
+          "gene": "OR2T10",
+          "score": -0.0880425,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14286,
+          "gene": "SLC1A7",
+          "score": 0.04237285,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17850,
+          "gene": "ZMYND12",
+          "score": -0.0982155,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15506,
+          "gene": "TAF3",
+          "score": 0.020675,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11628,
+          "gene": "PHKB",
+          "score": 0.013254,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13832,
+          "gene": "SDR42E2",
+          "score": -0.2481805,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7118,
+          "gene": "IFNA4",
+          "score": -0.03555,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12620,
+          "gene": "PTPRA",
+          "score": -0.04744875,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3935,
+          "gene": "DCUN1D1",
+          "score": -0.0414515,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3022,
+          "gene": "CIRBP",
+          "score": 0.0841915,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4904,
+          "gene": "ERI3",
+          "score": 0.183812,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5780,
+          "gene": "GALK2",
+          "score": -0.16022725,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2929,
+          "gene": "CHMP5",
+          "score": 0.42015,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 11932,
+          "gene": "PMP2",
+          "score": -0.16301,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7622,
+          "gene": "KCNA4",
+          "score": 0.03668925,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12826,
+          "gene": "RAG1",
+          "score": 0.03867,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5450,
+          "gene": "FGR",
+          "score": 0.32395,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5052,
+          "gene": "FABP1",
+          "score": -0.16277,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11331,
+          "gene": "PCDHB4",
+          "score": -0.51529,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 2465,
+          "gene": "CD14",
+          "score": -0.11622,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12134,
+          "gene": "PPM1G",
+          "score": -0.0833035,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12326,
+          "gene": "PRKRA",
+          "score": 0.25402626,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13067,
+          "gene": "RETNLB",
+          "score": 0.05045863,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11246,
+          "gene": "PARPBP",
+          "score": -0.131243,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16465,
+          "gene": "TPCN1",
+          "score": 0.08007,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15481,
+          "gene": "TAC4",
+          "score": -0.1659785,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8117,
+          "gene": "KRTAP5-7",
+          "score": -0.047770675,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11218,
+          "gene": "PAQR5",
+          "score": 0.1059,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10794,
+          "gene": "OR2T29",
+          "score": -0.346245,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14141,
+          "gene": "SHQ1",
+          "score": -0.03321,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 715,
+          "gene": "ANKRD46",
+          "score": 0.353385,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12590,
+          "gene": "PTK2",
+          "score": -0.097984,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12087,
+          "gene": "PP2D1",
+          "score": 0.07194625,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17101,
+          "gene": "UNC93B1",
+          "score": -0.0559315,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11215,
+          "gene": "PAPSS2",
+          "score": 0.0683462,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14252,
+          "gene": "SLC16A10",
+          "score": 0.091323,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5884,
+          "gene": "GCNT1",
+          "score": -0.05849,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8904,
+          "gene": "MAP3K9",
+          "score": 3.5e-05,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9579,
+          "gene": "MSTN",
+          "score": 0.21826,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16346,
+          "gene": "TNFRSF11B",
+          "score": -0.052113,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10814,
+          "gene": "OR4A47",
+          "score": -0.189292,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12913,
+          "gene": "RASSF8",
+          "score": 0.113495,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7274,
+          "gene": "IL31RA",
+          "score": 0.02396,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5156,
+          "gene": "FAM209B",
+          "score": -0.145942,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4082,
+          "gene": "DEUP1",
+          "score": 0.011269,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12564,
+          "gene": "PTER",
+          "score": 0.2438895,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8558,
+          "gene": "LRIG1",
+          "score": 0.3103475,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8052,
+          "gene": "KRTAP10-12",
+          "score": -0.357157,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10053,
+          "gene": "NEK8",
+          "score": 0.045132,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11251,
+          "gene": "PASD1",
+          "score": 0.0095975,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13859,
+          "gene": "SEC61A1",
+          "score": -1.24095,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 5637,
+          "gene": "FRMD6",
+          "score": 0.17515,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17364,
+          "gene": "VSX1",
+          "score": -0.095107,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10129,
+          "gene": "NGLY1",
+          "score": 0.0902385,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5492,
+          "gene": "FKBP8",
+          "score": -0.02692,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2233,
+          "gene": "CBY2",
+          "score": 0.03145,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 872,
+          "gene": "APRT",
+          "score": 0.066691,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11034,
+          "gene": "ORM1",
+          "score": 0.071057,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2412,
+          "gene": "CCNB2",
+          "score": -0.106655,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7476,
+          "gene": "ITGA4",
+          "score": 0.0571885,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17799,
+          "gene": "ZFTA",
+          "score": 0.295155,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2808,
+          "gene": "CFAP126",
+          "score": 0.1851,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12093,
+          "gene": "PPARD",
+          "score": -0.1182605,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11056,
+          "gene": "OSGEPL1",
+          "score": 0.029674,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14992,
+          "gene": "SPINK5",
+          "score": 0.1756,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4027,
+          "gene": "DEFB119",
+          "score": 0.062365,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12580,
+          "gene": "PTGIS",
+          "score": -0.09387,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4249,
+          "gene": "DNAI4",
+          "score": -0.20582,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12909,
+          "gene": "RASSF3",
+          "score": 0.285485,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13391,
+          "gene": "RPIA",
+          "score": -0.03165,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4398,
+          "gene": "DRD1",
+          "score": -0.100129,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13086,
+          "gene": "RFLNA",
+          "score": 0.105329,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7851,
+          "gene": "KIR3DL3",
+          "score": 0.004392,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11057,
+          "gene": "OSGIN1",
+          "score": 0.1050995,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 692,
+          "gene": "ANKRD24",
+          "score": -0.05942,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11706,
+          "gene": "PIK3IP1",
+          "score": 0.0774005,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4954,
+          "gene": "ETF1",
+          "score": -0.2975425,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1198,
+          "gene": "ATP11AUN",
+          "score": -0.21638,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15816,
+          "gene": "TFAP2D",
+          "score": 0.339235,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16607,
+          "gene": "TRIM5",
+          "score": -0.238896,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5796,
+          "gene": "GALNT8",
+          "score": -0.18248,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2128,
+          "gene": "CAPN15",
+          "score": -0.0278715,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11998,
+          "gene": "POLE4",
+          "score": 0.115658,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4219,
+          "gene": "DMWD",
+          "score": -0.1336994,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1748,
+          "gene": "C16orf54",
+          "score": 0.108705,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16628,
+          "gene": "TRIM69",
+          "score": 0.041445,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11330,
+          "gene": "PCDHB3",
+          "score": -0.032855,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 330,
+          "gene": "ADGRG2",
+          "score": 0.384941,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15297,
+          "gene": "STRN4",
+          "score": 0.09592,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1851,
+          "gene": "C2",
+          "score": -0.006035,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14808,
+          "gene": "SNX8",
+          "score": 0.34474,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4657,
+          "gene": "EIF2D",
+          "score": -0.16068,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2319,
+          "gene": "CCDC39",
+          "score": 0.093614,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15727,
+          "gene": "TDRD5",
+          "score": 0.168175,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1566,
+          "gene": "BNIPL",
+          "score": 0.03104265,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1676,
+          "gene": "BUD31",
+          "score": -0.0926225,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7507,
+          "gene": "ITLN1",
+          "score": -0.0415915,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9214,
+          "gene": "MGAT5B",
+          "score": -0.0492,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2908,
+          "gene": "CHGA",
+          "score": -0.0912605,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16443,
+          "gene": "TOR4A",
+          "score": -0.112765,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9495,
+          "gene": "MRPL51",
+          "score": 0.09959825,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9037,
+          "gene": "MCL1",
+          "score": -0.0620235,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10746,
+          "gene": "OR2A12",
+          "score": 0.13195,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17080,
+          "gene": "UMAD1",
+          "score": 0.161218,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12165,
+          "gene": "PPP1R2",
+          "score": -0.1042185,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10715,
+          "gene": "OR14A16",
+          "score": 0.050317,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6922,
+          "gene": "HPSE2",
+          "score": 0.112994,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13170,
+          "gene": "RHOC",
+          "score": -0.174285,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17352,
+          "gene": "VSIG10L2",
+          "score": 0.044635,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10449,
+          "gene": "NT5DC1",
+          "score": 0.01987,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8922,
+          "gene": "MAPK13",
+          "score": 0.1460872,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4223,
+          "gene": "DNAAF1",
+          "score": -0.158985,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6584,
+          "gene": "HACD3",
+          "score": 0.054218,
+          "hit": 0,
+          "round": 4
         }
       ],
       "queried_history": [
@@ -6712,896 +7608,1792 @@
           "gene": "ZNF585A",
           "score": -0.029175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18096,
           "gene": "ZNF524",
           "score": 0.1740205,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18115,
           "gene": "ZNF552",
           "score": -0.18224,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18050,
           "gene": "ZNF449",
           "score": 0.02156985,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18077,
           "gene": "ZNF500",
           "score": 0.128354,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18036,
           "gene": "ZNF431",
           "score": 0.181045,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18075,
           "gene": "ZNF496",
           "score": 0.13378,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18039,
           "gene": "ZNF436",
           "score": -0.22501,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18101,
           "gene": "ZNF530",
           "score": 0.111831,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18061,
           "gene": "ZNF471",
           "score": 0.16659,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18085,
           "gene": "ZNF511-PRAP1",
           "score": 0.101215,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18113,
           "gene": "ZNF550",
           "score": 0.0015315,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18131,
           "gene": "ZNF569",
           "score": -0.2065345,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18140,
           "gene": "ZNF577",
           "score": 0.352155,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18103,
           "gene": "ZNF534",
           "score": -0.1037915,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18046,
           "gene": "ZNF443",
           "score": -0.1002155,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18071,
           "gene": "ZNF490",
           "score": -0.0520515,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18111,
           "gene": "ZNF548",
           "score": 0.14674175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18048,
           "gene": "ZNF445",
           "score": 0.185425,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18084,
           "gene": "ZNF511",
           "score": -0.087807,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18145,
           "gene": "ZNF582",
           "score": 0.053413,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18069,
           "gene": "ZNF486",
           "score": -0.01275,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18073,
           "gene": "ZNF492",
           "score": 0.2519605,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18087,
           "gene": "ZNF512B",
           "score": -0.13953,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18105,
           "gene": "ZNF540",
           "score": 0.096929,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18089,
           "gene": "ZNF514",
           "score": 0.0049065,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18040,
           "gene": "ZNF438",
           "score": 0.094816,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18133,
           "gene": "ZNF570",
           "score": 0.00226,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18045,
           "gene": "ZNF442",
           "score": 0.1677725,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18055,
           "gene": "ZNF461",
           "score": -0.26366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18091,
           "gene": "ZNF517",
           "score": 0.071871,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18138,
           "gene": "ZNF575",
           "score": -0.32484,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18104,
           "gene": "ZNF536",
           "score": 0.201145,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18155,
           "gene": "ZNF594",
           "score": -0.02139,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18136,
           "gene": "ZNF573",
           "score": -0.1773585,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18110,
           "gene": "ZNF547",
           "score": 0.0528285,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18056,
           "gene": "ZNF462",
           "score": -0.04815,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18161,
           "gene": "ZNF600",
           "score": -0.13736,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18079,
           "gene": "ZNF502",
           "score": 0.009245,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18038,
           "gene": "ZNF433",
           "score": -0.176507,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18034,
           "gene": "ZNF43",
           "score": -0.1845355,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18141,
           "gene": "ZNF578",
           "score": -0.15319,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18068,
           "gene": "ZNF485",
           "score": 0.271345,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18128,
           "gene": "ZNF566",
           "score": -0.3362,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18054,
           "gene": "ZNF460",
           "score": -0.092895,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18081,
           "gene": "ZNF506",
           "score": -0.113433,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18057,
           "gene": "ZNF467",
           "score": 0.072695,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18051,
           "gene": "ZNF45",
           "score": 0.1424945,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18044,
           "gene": "ZNF441",
           "score": -0.164674,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18049,
           "gene": "ZNF446",
           "score": -0.061245,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18086,
           "gene": "ZNF512",
           "score": -0.0526845,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18158,
           "gene": "ZNF597",
           "score": -0.39098,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18102,
           "gene": "ZNF532",
           "score": 0.0522465,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18106,
           "gene": "ZNF541",
           "score": -0.18417965,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18156,
           "gene": "ZNF595",
           "score": -0.025711,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18126,
           "gene": "ZNF564",
           "score": 0.1820195,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18132,
           "gene": "ZNF57",
           "score": 0.103895,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18097,
           "gene": "ZNF526",
           "score": 0.137245,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18065,
           "gene": "ZNF480",
           "score": 0.24194,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18043,
           "gene": "ZNF440",
           "score": -0.087465,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18035,
           "gene": "ZNF430",
           "score": 0.08786,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18137,
           "gene": "ZNF574",
           "score": 0.16361,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18095,
           "gene": "ZNF521",
           "score": 0.08589,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18090,
           "gene": "ZNF516",
           "score": 0.25173,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18124,
           "gene": "ZNF562",
           "score": -0.3011635,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18062,
           "gene": "ZNF473",
           "score": 0.0156455,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18088,
           "gene": "ZNF513",
           "score": 0.01218,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18130,
           "gene": "ZNF568",
           "score": 0.0717735,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18080,
           "gene": "ZNF503",
           "score": 0.23489,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18047,
           "gene": "ZNF444",
           "score": -0.0704355,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18117,
           "gene": "ZNF555",
           "score": 0.145655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18135,
           "gene": "ZNF572",
           "score": 0.041181,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18114,
           "gene": "ZNF551",
           "score": 0.0350655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18098,
           "gene": "ZNF527",
           "score": 0.0058345,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18063,
           "gene": "ZNF479",
           "score": 0.0278175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18074,
           "gene": "ZNF493",
           "score": 0.009985,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18093,
           "gene": "ZNF518B",
           "score": 0.31276,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18094,
           "gene": "ZNF519",
           "score": -0.0857705,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18112,
           "gene": "ZNF549",
           "score": 0.22809,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18076,
           "gene": "ZNF497",
           "score": 0.000715,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18119,
           "gene": "ZNF557",
           "score": 0.264625,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18041,
           "gene": "ZNF439",
           "score": -0.237145,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18150,
           "gene": "ZNF586",
           "score": -0.198565,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18059,
           "gene": "ZNF469",
           "score": 0.051955,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18149,
           "gene": "ZNF585B",
           "score": -0.183071,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18121,
           "gene": "ZNF559",
           "score": 0.19544,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18116,
           "gene": "ZNF554",
           "score": -0.250545,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18037,
           "gene": "ZNF432",
           "score": -0.0355025,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18120,
           "gene": "ZNF558",
           "score": 0.006585,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18139,
           "gene": "ZNF576",
           "score": 0.389825,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18053,
           "gene": "ZNF454",
           "score": 0.11075185,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18154,
           "gene": "ZNF593",
           "score": -0.0711965,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18072,
           "gene": "ZNF491",
           "score": -0.035655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18143,
           "gene": "ZNF580",
           "score": 0.234024,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18109,
           "gene": "ZNF546",
           "score": -0.005505,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18083,
           "gene": "ZNF510",
           "score": -0.184205,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18042,
           "gene": "ZNF44",
           "score": -0.11366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18107,
           "gene": "ZNF543",
           "score": 0.37438,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18070,
           "gene": "ZNF488",
           "score": 0.039261,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18064,
           "gene": "ZNF48",
           "score": 0.0807835,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18134,
           "gene": "ZNF571",
           "score": 0.077155,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18142,
           "gene": "ZNF579",
           "score": 0.026342,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18067,
           "gene": "ZNF484",
           "score": -0.059251,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18060,
           "gene": "ZNF470",
           "score": -0.1913,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18127,
           "gene": "ZNF565",
           "score": -0.140035,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18144,
           "gene": "ZNF581",
           "score": -0.0562255,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18153,
           "gene": "ZNF592",
           "score": 0.0864995,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18082,
           "gene": "ZNF507",
           "score": 0.037163,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18157,
           "gene": "ZNF596",
           "score": 0.376185,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18078,
           "gene": "ZNF501",
           "score": -0.0899685,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18066,
           "gene": "ZNF483",
           "score": 0.1860085,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18052,
           "gene": "ZNF451",
           "score": -0.06424,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18122,
           "gene": "ZNF560",
           "score": 0.0112985,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18146,
           "gene": "ZNF583",
           "score": -0.05593,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18058,
           "gene": "ZNF468",
           "score": -0.0068665,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18125,
           "gene": "ZNF563",
           "score": 0.168275,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18147,
           "gene": "ZNF584",
           "score": 0.337285,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18160,
           "gene": "ZNF599",
           "score": -0.1666685,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18100,
           "gene": "ZNF529",
           "score": -0.0121575,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18152,
           "gene": "ZNF589",
           "score": -0.1166215,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18159,
           "gene": "ZNF598",
           "score": -0.152225,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18118,
           "gene": "ZNF556",
           "score": 0.05136365,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18123,
           "gene": "ZNF561",
           "score": 0.29338,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18151,
           "gene": "ZNF587",
           "score": 0.052138,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18129,
           "gene": "ZNF567",
           "score": 0.03971,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18099,
           "gene": "ZNF528",
           "score": 0.037025,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18108,
           "gene": "ZNF544",
           "score": -0.0599985,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18092,
           "gene": "ZNF518A",
           "score": -0.2550815,
           "hit": 0,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 13776,
+          "gene": "SCN3A",
+          "score": -0.329865,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11729,
+          "gene": "PIP4P2",
+          "score": -0.341205,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4520,
+          "gene": "EARS2",
+          "score": -0.09780015,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16114,
+          "gene": "TMEM160",
+          "score": -0.2169725,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4180,
+          "gene": "DLEU7",
+          "score": 0.025105,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1931,
+          "gene": "C5orf22",
+          "score": -0.22257,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17348,
+          "gene": "VRTN",
+          "score": 0.0977705,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11126,
+          "gene": "P2RY6",
+          "score": 0.2081295,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13248,
+          "gene": "RNASE12",
+          "score": 0.010242834,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2189,
+          "gene": "CAT",
+          "score": 0.043525,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9394,
+          "gene": "MPC2",
+          "score": 0.0071113,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14926,
+          "gene": "SPATA31C2",
+          "score": 0.2683855,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1352,
+          "gene": "B4GALT5",
+          "score": -0.348185,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11413,
+          "gene": "PDCL3",
+          "score": 0.06847715,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5645,
+          "gene": "FRRS1L",
+          "score": 0.016505,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10789,
+          "gene": "OR2T10",
+          "score": -0.0880425,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14286,
+          "gene": "SLC1A7",
+          "score": 0.04237285,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17850,
+          "gene": "ZMYND12",
+          "score": -0.0982155,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15506,
+          "gene": "TAF3",
+          "score": 0.020675,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11628,
+          "gene": "PHKB",
+          "score": 0.013254,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13832,
+          "gene": "SDR42E2",
+          "score": -0.2481805,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7118,
+          "gene": "IFNA4",
+          "score": -0.03555,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12620,
+          "gene": "PTPRA",
+          "score": -0.04744875,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3935,
+          "gene": "DCUN1D1",
+          "score": -0.0414515,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3022,
+          "gene": "CIRBP",
+          "score": 0.0841915,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4904,
+          "gene": "ERI3",
+          "score": 0.183812,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5780,
+          "gene": "GALK2",
+          "score": -0.16022725,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2929,
+          "gene": "CHMP5",
+          "score": 0.42015,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 11932,
+          "gene": "PMP2",
+          "score": -0.16301,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7622,
+          "gene": "KCNA4",
+          "score": 0.03668925,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12826,
+          "gene": "RAG1",
+          "score": 0.03867,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5450,
+          "gene": "FGR",
+          "score": 0.32395,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5052,
+          "gene": "FABP1",
+          "score": -0.16277,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11331,
+          "gene": "PCDHB4",
+          "score": -0.51529,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 2465,
+          "gene": "CD14",
+          "score": -0.11622,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12134,
+          "gene": "PPM1G",
+          "score": -0.0833035,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12326,
+          "gene": "PRKRA",
+          "score": 0.25402626,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13067,
+          "gene": "RETNLB",
+          "score": 0.05045863,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11246,
+          "gene": "PARPBP",
+          "score": -0.131243,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16465,
+          "gene": "TPCN1",
+          "score": 0.08007,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15481,
+          "gene": "TAC4",
+          "score": -0.1659785,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8117,
+          "gene": "KRTAP5-7",
+          "score": -0.047770675,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11218,
+          "gene": "PAQR5",
+          "score": 0.1059,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10794,
+          "gene": "OR2T29",
+          "score": -0.346245,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14141,
+          "gene": "SHQ1",
+          "score": -0.03321,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 715,
+          "gene": "ANKRD46",
+          "score": 0.353385,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12590,
+          "gene": "PTK2",
+          "score": -0.097984,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12087,
+          "gene": "PP2D1",
+          "score": 0.07194625,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17101,
+          "gene": "UNC93B1",
+          "score": -0.0559315,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11215,
+          "gene": "PAPSS2",
+          "score": 0.0683462,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14252,
+          "gene": "SLC16A10",
+          "score": 0.091323,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5884,
+          "gene": "GCNT1",
+          "score": -0.05849,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8904,
+          "gene": "MAP3K9",
+          "score": 3.5e-05,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9579,
+          "gene": "MSTN",
+          "score": 0.21826,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16346,
+          "gene": "TNFRSF11B",
+          "score": -0.052113,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10814,
+          "gene": "OR4A47",
+          "score": -0.189292,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12913,
+          "gene": "RASSF8",
+          "score": 0.113495,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7274,
+          "gene": "IL31RA",
+          "score": 0.02396,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5156,
+          "gene": "FAM209B",
+          "score": -0.145942,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4082,
+          "gene": "DEUP1",
+          "score": 0.011269,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12564,
+          "gene": "PTER",
+          "score": 0.2438895,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8558,
+          "gene": "LRIG1",
+          "score": 0.3103475,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8052,
+          "gene": "KRTAP10-12",
+          "score": -0.357157,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10053,
+          "gene": "NEK8",
+          "score": 0.045132,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11251,
+          "gene": "PASD1",
+          "score": 0.0095975,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13859,
+          "gene": "SEC61A1",
+          "score": -1.24095,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 5637,
+          "gene": "FRMD6",
+          "score": 0.17515,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17364,
+          "gene": "VSX1",
+          "score": -0.095107,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10129,
+          "gene": "NGLY1",
+          "score": 0.0902385,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5492,
+          "gene": "FKBP8",
+          "score": -0.02692,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2233,
+          "gene": "CBY2",
+          "score": 0.03145,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 872,
+          "gene": "APRT",
+          "score": 0.066691,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11034,
+          "gene": "ORM1",
+          "score": 0.071057,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2412,
+          "gene": "CCNB2",
+          "score": -0.106655,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7476,
+          "gene": "ITGA4",
+          "score": 0.0571885,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17799,
+          "gene": "ZFTA",
+          "score": 0.295155,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2808,
+          "gene": "CFAP126",
+          "score": 0.1851,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12093,
+          "gene": "PPARD",
+          "score": -0.1182605,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11056,
+          "gene": "OSGEPL1",
+          "score": 0.029674,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14992,
+          "gene": "SPINK5",
+          "score": 0.1756,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4027,
+          "gene": "DEFB119",
+          "score": 0.062365,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12580,
+          "gene": "PTGIS",
+          "score": -0.09387,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4249,
+          "gene": "DNAI4",
+          "score": -0.20582,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12909,
+          "gene": "RASSF3",
+          "score": 0.285485,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13391,
+          "gene": "RPIA",
+          "score": -0.03165,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4398,
+          "gene": "DRD1",
+          "score": -0.100129,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13086,
+          "gene": "RFLNA",
+          "score": 0.105329,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7851,
+          "gene": "KIR3DL3",
+          "score": 0.004392,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11057,
+          "gene": "OSGIN1",
+          "score": 0.1050995,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 692,
+          "gene": "ANKRD24",
+          "score": -0.05942,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11706,
+          "gene": "PIK3IP1",
+          "score": 0.0774005,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4954,
+          "gene": "ETF1",
+          "score": -0.2975425,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1198,
+          "gene": "ATP11AUN",
+          "score": -0.21638,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15816,
+          "gene": "TFAP2D",
+          "score": 0.339235,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16607,
+          "gene": "TRIM5",
+          "score": -0.238896,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5796,
+          "gene": "GALNT8",
+          "score": -0.18248,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2128,
+          "gene": "CAPN15",
+          "score": -0.0278715,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11998,
+          "gene": "POLE4",
+          "score": 0.115658,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4219,
+          "gene": "DMWD",
+          "score": -0.1336994,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1748,
+          "gene": "C16orf54",
+          "score": 0.108705,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16628,
+          "gene": "TRIM69",
+          "score": 0.041445,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11330,
+          "gene": "PCDHB3",
+          "score": -0.032855,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 330,
+          "gene": "ADGRG2",
+          "score": 0.384941,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15297,
+          "gene": "STRN4",
+          "score": 0.09592,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1851,
+          "gene": "C2",
+          "score": -0.006035,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14808,
+          "gene": "SNX8",
+          "score": 0.34474,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4657,
+          "gene": "EIF2D",
+          "score": -0.16068,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2319,
+          "gene": "CCDC39",
+          "score": 0.093614,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15727,
+          "gene": "TDRD5",
+          "score": 0.168175,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1566,
+          "gene": "BNIPL",
+          "score": 0.03104265,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1676,
+          "gene": "BUD31",
+          "score": -0.0926225,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7507,
+          "gene": "ITLN1",
+          "score": -0.0415915,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9214,
+          "gene": "MGAT5B",
+          "score": -0.0492,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2908,
+          "gene": "CHGA",
+          "score": -0.0912605,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16443,
+          "gene": "TOR4A",
+          "score": -0.112765,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9495,
+          "gene": "MRPL51",
+          "score": 0.09959825,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9037,
+          "gene": "MCL1",
+          "score": -0.0620235,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10746,
+          "gene": "OR2A12",
+          "score": 0.13195,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17080,
+          "gene": "UMAD1",
+          "score": 0.161218,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12165,
+          "gene": "PPP1R2",
+          "score": -0.1042185,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10715,
+          "gene": "OR14A16",
+          "score": 0.050317,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6922,
+          "gene": "HPSE2",
+          "score": 0.112994,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13170,
+          "gene": "RHOC",
+          "score": -0.174285,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17352,
+          "gene": "VSIG10L2",
+          "score": 0.044635,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10449,
+          "gene": "NT5DC1",
+          "score": 0.01987,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8922,
+          "gene": "MAPK13",
+          "score": 0.1460872,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4223,
+          "gene": "DNAAF1",
+          "score": -0.158985,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6584,
+          "gene": "HACD3",
+          "score": 0.054218,
+          "hit": 0,
+          "round": 4
         }
       ]
     }

```
