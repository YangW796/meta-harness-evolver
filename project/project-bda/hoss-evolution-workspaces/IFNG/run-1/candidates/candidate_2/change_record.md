# Change Record — candidate_2

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IFNG/run-1/best/current/harness
Generated at: 2026-04-30T06:45:15.881421

## Files Changed

- model.py: modified (added=12, deleted=4, delta=8)
- outputs/metrics.json: modified (added=2180, deleted=388, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -73,6 +73,10 @@
     # For unexplored candidates, count = 1 for optimistic initialization
     ucb_scores = []
     
+    # Calculate min and max observed scores for exploration
+    min_observed_score = min(candidate_avg_scores.values()) if candidate_avg_scores else 0
+    max_observed_score = max(candidate_avg_scores.values()) if candidate_avg_scores else 0
+    
     for idx in available_indices:
         if idx in candidate_avg_scores:
             # Explored candidate
@@ -82,12 +86,16 @@
             ucb = mean_score + exploration_bonus
         else:
             # Unexplored candidate - use optimistic initialization
-            # Use the maximum observed score + small bonus as initial estimate
+            # Explore both extremes: favor candidates that could be very negative (hits) or very positive
+            # Use a mixture of min and max with higher weight on min since hits are negative
             if candidate_avg_scores:
-                max_score = max(candidate_avg_scores.values())
-                ucb = max_score + 0.1 * abs(max_score) if max_score != 0 else 1.0
+                # Bias exploration toward negative scores (hits are at -0.4 to -0.5)
+                ucb_negative = min_observed_score - 0.1 * abs(min_observed_score) if min_observed_score != 0 else -1.0
+                ucb_positive = max_observed_score + 0.1 * abs(max_observed_score) if max_observed_score != 0 else 1.0
+                # Blend: 70% weight on negative exploration (hits), 30% on positive
+                ucb = 0.7 * ucb_negative + 0.3 * ucb_positive
             else:
-                ucb = 1.0
+                ucb = -1.0  # Start with negative bias for unexplored
         ucb_scores.append((ucb, idx))
     
     # Sort by UCB score (descending) and select top batch_size

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18418,
-      "rounds": 1,
+      "rounds": 2,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 0,
-      "baseline_total_hits": 0,
+      "baseline_total_queries": 128,
+      "baseline_total_hits": 2,
       "delta_queries": 128,
-      "delta_hits": 2,
-      "total_queries": 128,
-      "total_hits": 2,
+      "delta_hits": 1,
+      "total_queries": 256,
+      "total_hits": 3,
       "top_k": 920,
       "hit_curve": {
         "queries": [
-          0,
-          128
+          128,
+          256
         ],
         "hits": [
-          0,
-          2
+          2,
+          3
         ]
       },
-      "auc": 128.0,
-      "auc_normalized": 0.0010869565217391304,
-      "ncg": 0.10533733408464835,
+      "auc": 320.0,
+      "auc_normalized": 0.001358695652173913,
+      "ncg": 0.14329897550565224,
       "round_details": [
         {
-          "round": 0,
+          "round": 1,
           "selected_count": 128,
-          "hits": 2,
-          "cumulative_hits": 2,
-          "precision_at_batch": 0.015625,
+          "hits": 1,
+          "cumulative_hits": 3,
+          "precision_at_batch": 0.0078125,
           "selected": [
-            "AADAC",
-            "ABHD5",
-            "ABLIM1",
-            "ABHD10",
-            "ABCB8",
-            "AAMDC",
-            "ABCD1",
-            "ABLIM2",
-            "ABLIM3",
-            "ABHD14B",
-            "ABCB6",
-            "AARS1",
-            "ABCA1",
-            "ACACB",
-            "ABCA12",
-            "ABCB9",
-            "ABCD2",
-            "ACADL",
-            "ABI2",
-            "AANAT",
-            "ABCG8",
-            "A2M",
-            "ABCE1",
-            "ABHD13",
-            "ABCA4",
-            "ABHD16B",
-            "AAAS",
-            "A1CF",
-            "ABHD17B",
-            "ABHD12B",
-            "AASS",
-            "ABL2",
-            "ABCC8",
-            "ABCG5",
-            "ABI1",
-            "ABCC6",
-            "ABCA7",
-            "ABCG4",
-            "ABCA2",
-            "ABCC1",
-            "ABCC9",
-            "ABCA6",
-            "ABT1",
-            "ABCA9",
-            "ABHD16A",
-            "ABHD12",
-            "ABCC3",
-            "ABCB1",
-            "ABL1",
-            "AARS2",
-            "ABCC10",
-            "ABCG1",
-            "AARSD1",
-            "ABI3",
-            "ABCA8",
-            "ABR",
-            "ACAD8",
-            "ABCF1",
-            "A4GNT",
-            "ABCC2",
-            "AAGAB",
-            "ABHD3",
-            "ABCD4",
-            "ABI3BP",
-            "ABRA",
-            "ACACA",
-            "AACS",
-            "AASDH",
-            "ABCB5",
-            "ABCA5",
-            "AADACL2",
-            "ABHD14A",
-            "AAK1",
-            "ABCF2",
-            "ABCC5",
-            "A4GALT",
-            "ABCA13",
-            "ABO",
-            "ABCB11",
-            "ABCB4",
-            "AADACL4",
-            "ABCB7",
-            "ABRAXAS1",
-            "ACAD10",
-            "ABHD17C",
-            "ABRACL",
-            "AAR2",
-            "ABHD6",
-            "ABCB10",
-            "ABTB1",
-            "ABITRAM",
-            "AARD",
-            "A1BG",
-            "ACADM",
-            "ABTB2",
-            "ABCC4",
-            "ACAD9",
-            "ABCC11",
-            "ACAA1",
-            "ABHD2",
-            "ABHD15",
-            "ABHD4",
-            "AASDHPPT",
-            "ABCG2",
-            "ABRAXAS2",
-            "ABHD11",
-            "ABCD3",
-            "ABAT",
-            "AATF",
-            "ACAA2",
-            "ACADSB",
-            "A3GALT2",
-            "ABCC12",
-            "ABHD1",
-            "AADACL3",
-            "ABCF3",
-            "ABTB3",
-            "ACAD11",
-            "ABHD17A",
-            "AADAT",
-            "ACADS",
-            "AAMP",
-            "ACADVL",
-            "ABCA10",
-            "ABCA3",
-            "ABHD8",
-            "A2ML1",
-            "AATK"
+            "ZNG1F",
+            "ZNRF4",
+            "ZNF852",
+            "ZNF846",
+            "ZPR1",
+            "ZNF784",
+            "ZNF823",
+            "ZNF845",
+            "ZNHIT1",
+            "ZNF814",
+            "ZSCAN1",
+            "ZNRF3",
+            "ZSCAN26",
+            "ZSCAN21",
+            "ZNF91",
+            "ZNF839",
+            "ZSWIM7",
+            "ZNF98",
+            "ZNF830",
+            "ZNRD2",
+            "ZSCAN4",
+            "ZNF84",
+            "ZSCAN22",
+            "ZNF821",
+            "ZRSR2",
+            "ZSCAN32",
+            "ZNHIT2",
+            "ZZZ3",
+            "ZP2",
+            "ZZEF1",
+            "ZNF787",
+            "ZSCAN29",
+            "ZRANB1",
+            "ZNF860",
+            "ZNF81",
+            "ZNF862",
+            "ZSCAN10",
+            "ZNF853",
+            "ZNF793",
+            "ZXDC",
+            "ZP1",
+            "ZSCAN31",
+            "ZSCAN25",
+            "ZNF804B",
+            "ZSCAN30",
+            "ZNF79",
+            "ZSCAN23",
+            "ZNF816",
+            "ZNF92",
+            "ZNFX1",
+            "ZNF883",
+            "ZYG11A",
+            "ZSCAN12",
+            "ZRANB2",
+            "ZUP1",
+            "ZPLD1",
+            "ZNF813",
+            "ZSWIM4",
+            "ZNF792",
+            "ZNF85",
+            "ZYG11B",
+            "ZNF837",
+            "ZNF843",
+            "ZW10",
+            "ZNF841",
+            "ZNF804A",
+            "ZNRF1",
+            "ZNF99",
+            "ZRANB3",
+            "ZNF8",
+            "ZNF836",
+            "ZNF878",
+            "ZNF83",
+            "ZNG1A",
+            "ZNF783",
+            "ZSCAN2",
+            "ZSCAN16",
+            "ZSCAN9",
+            "ZNF865",
+            "ZNF791",
+            "ZNF829",
+            "ZNF891",
+            "ZXDB",
+            "ZWINT",
+            "ZNF786",
+            "ZSCAN5A",
+            "ZNF808",
+            "ZSCAN20",
+            "ZNG1C",
+            "ZNF80",
+            "ZP4",
+            "ZSWIM5",
+            "ZNF800",
+            "ZNF805",
+            "ZSWIM1",
+            "ZNF799",
+            "ZSWIM2",
+            "ZPBP",
+            "ZSWIM6",
+            "ZSWIM8",
+            "ZXDA",
+            "ZSCAN5B",
+            "ZP3",
+            "ZNF806",
+            "ZNF835",
+            "ZNF93",
+            "ZNF875",
+            "ZNF790",
+            "ZNF90",
+            "ZNRF2",
+            "ZNG1B",
+            "ZYX",
+            "ZNF879",
+            "ZNG1E",
+            "ZNF880",
+            "ZNHIT6",
+            "ZSWIM9",
+            "ZNF827",
+            "ZNF785",
+            "ZNF850",
+            "ZPBP2",
+            "ZNHIT3",
+            "ZNF789",
+            "ZSWIM3",
+            "ZNF831",
+            "ZNF844",
+            "ZSCAN18",
+            "ZWILCH"
           ],
           "selected_scores": [
-            0.09700375,
-            -0.123051,
-            -0.095673,
-            -0.083665,
-            -0.009105,
-            0.01205,
-            -0.0909125,
-            -0.220065,
-            0.131625,
-            0.025335,
-            -0.042354,
-            -0.40020835,
-            0.1342295,
-            0.018345,
-            -0.108835,
-            0.21014065,
-            0.00524,
-            0.147555,
-            -0.22205,
-            0.14409,
-            -0.038225,
-            -0.18934,
-            0.359895,
-            0.022985,
-            -0.159105,
-            -0.002058,
-            0.130627,
-            0.129081,
-            0.23368,
-            -0.01068,
-            -0.085326,
-            0.11353,
-            0.051595,
-            0.103443,
-            0.0107805,
-            0.307105,
-            -0.01946,
-            0.25585085,
-            -0.2907179,
-            -0.165605,
-            0.19773,
-            -0.1365005,
-            0.0858425,
-            0.27268896,
-            -0.1640935,
-            0.1263665,
-            -0.0762865,
-            -0.266345,
-            0.0765485,
-            0.03688,
-            -0.1349245,
-            0.04291255,
-            -0.007871,
-            -0.1086473,
-            0.0039675,
-            0.339915,
-            0.02707,
-            -0.105515,
-            0.029995,
-            -0.1535965,
-            -0.31044,
-            0.071691,
-            -0.04102,
-            -0.12602566,
-            0.031534,
-            0.035085,
-            0.19899,
-            0.140285,
-            0.0766415,
-            0.09411,
-            0.180098,
-            -0.0982965,
-            -0.144225,
-            -0.1052725,
-            0.16644,
-            0.15113,
-            -0.01498,
-            0.016455,
-            0.09610045,
-            0.2502,
-            -0.165411,
-            -0.505255,
-            0.02837,
-            0.037576,
-            -0.0872855,
-            -0.0995285,
-            0.17943,
-            -0.01869,
-            -0.091724,
-            0.0953785,
-            0.18748,
-            0.0074185,
-            -0.161214,
-            -0.17399,
-            -0.15948,
-            0.07494,
-            0.0464,
-            -0.1653245,
-            0.27926,
-            -0.033632,
-            0.054218,
-            -0.015138,
-            0.0825805,
-            -0.000475,
-            -0.240335,
-            0.178475,
-            -0.367169,
-            -0.01351,
-            0.3854245,
-            -0.0323105,
-            0.0369245,
-            0.183225,
-            -0.09262565,
-            0.09580065,
-            -0.217905,
-            0.0637145,
-            0.33209,
-            0.184825,
-            -0.35325,
-            0.23516,
-            0.243119,
-            0.1659475,
-            0.0484775,
-            -0.00779,
-            0.20382,
-            -0.239638,
-            0.005275,
-            -0.027445
+            0.02004,
+            -0.1326135,
+            0.082401,
+            0.241646,
+            0.060205,
+            0.1521965,
+            -0.0882665,
+            0.174269,
+            0.285865,
+            -0.002941,
+            0.0236465,
+            0.109025,
+            0.1452,
+            -0.06876,
+            0.072198,
+            0.058726,
+            0.04798,
+            0.1414345,
+            -0.385385,
+            0.022,
+            0.100399,
+            -0.1180885,
+            -0.0139586,
+            0.152965,
+            -0.105073,
+            -0.28131,
+            -0.104951,
+            0.16858,
+            -0.09089255,
+            0.2619375,
+            -0.025515,
+            0.320085,
+            0.32594,
+            -0.165498,
+            0.0681635,
+            0.0335655,
+            0.0282885,
+            0.0603453,
+            -0.21759,
+            0.10866015,
+            -0.1891195,
+            0.0142375,
+            0.04001,
+            0.0680285,
+            -0.0656345,
+            0.052601,
+            -0.179549,
+            0.155999,
+            -0.01364915,
+            -0.118895,
+            -0.19204,
+            0.14097,
+            0.31877,
+            0.17481,
+            -0.0774975,
+            0.26673,
+            0.1106155,
+            -0.2097455,
+            -0.290714,
+            -0.1081275,
+            -0.1208665,
+            -0.24985,
+            -0.21766,
+            -0.159709,
+            -0.245215,
+            0.1808675,
+            -0.1483935,
+            0.355344,
+            -0.1117185,
+            0.1183505,
+            -0.160919,
+            0.117919,
+            -0.2179175,
+            0.0520335,
+            0.0189365,
+            0.174456,
+            0.02777,
+            -0.176105,
+            0.19303416,
+            0.0412261,
+            -0.09893,
+            0.0954565,
+            -0.02779,
+            -0.123792,
+            0.1072135,
+            0.34555,
+            -0.113385,
+            -0.3234765,
+            -0.1444645,
+            0.06814,
+            0.06677535,
+            -0.090245,
+            -0.21139,
+            0.003305,
+            0.1066745,
+            -0.077053,
+            0.08891,
+            -0.208236,
+            -0.132565,
+            -0.034683,
+            -0.044888,
+            -0.043905,
+            0.179865,
+            0.2282205,
+            0.1356605,
+            -0.0982335,
+            -0.214485,
+            -0.144395,
+            4.8e-05,
+            0.058075,
+            -0.2631505,
+            0.222654,
+            0.2543,
+            -0.091448,
+            0.0219,
+            0.341157,
+            -0.25744,
+            0.2394125,
+            -0.2707485,
+            0.135435,
+            -0.0285285,
+            -0.1181735,
+            -0.105075,
+            -0.242955,
+            0.0346266,
+            -0.114665,
+            -0.49931,
+            -0.146465
           ],
           "selected_hits": [
             0,
@@ -312,122 +312,122 @@
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
             0
           ]
         }
@@ -1328,6 +1328,902 @@
           "score": -0.027445,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 18355,
+          "gene": "ZNG1F",
+          "score": 0.02004,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18364,
+          "gene": "ZNRF4",
+          "score": -0.1326135,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18333,
+          "gene": "ZNF852",
+          "score": 0.082401,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18330,
+          "gene": "ZNF846",
+          "score": 0.241646,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18372,
+          "gene": "ZPR1",
+          "score": 0.060205,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18291,
+          "gene": "ZNF784",
+          "score": 0.1521965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18315,
+          "gene": "ZNF823",
+          "score": -0.0882665,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18329,
+          "gene": "ZNF845",
+          "score": 0.174269,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18356,
+          "gene": "ZNHIT1",
+          "score": 0.285865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18312,
+          "gene": "ZNF814",
+          "score": -0.002941,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18377,
+          "gene": "ZSCAN1",
+          "score": 0.0236465,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18363,
+          "gene": "ZNRF3",
+          "score": 0.109025,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18388,
+          "gene": "ZSCAN26",
+          "score": 0.1452,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18384,
+          "gene": "ZSCAN21",
+          "score": -0.06876,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18345,
+          "gene": "ZNF91",
+          "score": 0.072198,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18324,
+          "gene": "ZNF839",
+          "score": 0.058726,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18403,
+          "gene": "ZSWIM7",
+          "score": 0.04798,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18348,
+          "gene": "ZNF98",
+          "score": 0.1414345,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18319,
+          "gene": "ZNF830",
+          "score": -0.385385,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18360,
+          "gene": "ZNRD2",
+          "score": 0.022,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18393,
+          "gene": "ZSCAN4",
+          "score": 0.100399,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18325,
+          "gene": "ZNF84",
+          "score": -0.1180885,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18385,
+          "gene": "ZSCAN22",
+          "score": -0.0139586,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18314,
+          "gene": "ZNF821",
+          "score": 0.152965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18376,
+          "gene": "ZRSR2",
+          "score": -0.105073,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18392,
+          "gene": "ZSCAN32",
+          "score": -0.28131,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18357,
+          "gene": "ZNHIT2",
+          "score": -0.104951,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18417,
+          "gene": "ZZZ3",
+          "score": 0.16858,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18366,
+          "gene": "ZP2",
+          "score": -0.09089255,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18416,
+          "gene": "ZZEF1",
+          "score": 0.2619375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18294,
+          "gene": "ZNF787",
+          "score": -0.025515,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18389,
+          "gene": "ZSCAN29",
+          "score": 0.320085,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18373,
+          "gene": "ZRANB1",
+          "score": 0.32594,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18335,
+          "gene": "ZNF860",
+          "score": -0.165498,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18310,
+          "gene": "ZNF81",
+          "score": 0.0681635,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18336,
+          "gene": "ZNF862",
+          "score": 0.0335655,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18378,
+          "gene": "ZSCAN10",
+          "score": 0.0282885,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18334,
+          "gene": "ZNF853",
+          "score": 0.0603453,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18300,
+          "gene": "ZNF793",
+          "score": -0.21759,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18412,
+          "gene": "ZXDC",
+          "score": 0.10866015,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18365,
+          "gene": "ZP1",
+          "score": -0.1891195,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18391,
+          "gene": "ZSCAN31",
+          "score": 0.0142375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18387,
+          "gene": "ZSCAN25",
+          "score": 0.04001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18306,
+          "gene": "ZNF804B",
+          "score": 0.0680285,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18390,
+          "gene": "ZSCAN30",
+          "score": -0.0656345,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18296,
+          "gene": "ZNF79",
+          "score": 0.052601,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18386,
+          "gene": "ZSCAN23",
+          "score": -0.179549,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18313,
+          "gene": "ZNF816",
+          "score": 0.155999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18346,
+          "gene": "ZNF92",
+          "score": -0.01364915,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18350,
+          "gene": "ZNFX1",
+          "score": -0.118895,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18342,
+          "gene": "ZNF883",
+          "score": -0.19204,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18413,
+          "gene": "ZYG11A",
+          "score": 0.14097,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18379,
+          "gene": "ZSCAN12",
+          "score": 0.31877,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18374,
+          "gene": "ZRANB2",
+          "score": 0.17481,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18406,
+          "gene": "ZUP1",
+          "score": -0.0774975,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18371,
+          "gene": "ZPLD1",
+          "score": 0.26673,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18311,
+          "gene": "ZNF813",
+          "score": 0.1106155,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18400,
+          "gene": "ZSWIM4",
+          "score": -0.2097455,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18299,
+          "gene": "ZNF792",
+          "score": -0.290714,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18331,
+          "gene": "ZNF85",
+          "score": -0.1081275,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18414,
+          "gene": "ZYG11B",
+          "score": -0.1208665,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18323,
+          "gene": "ZNF837",
+          "score": -0.24985,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18327,
+          "gene": "ZNF843",
+          "score": -0.21766,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18407,
+          "gene": "ZW10",
+          "score": -0.159709,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18326,
+          "gene": "ZNF841",
+          "score": -0.245215,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18305,
+          "gene": "ZNF804A",
+          "score": 0.1808675,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18361,
+          "gene": "ZNRF1",
+          "score": -0.1483935,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18349,
+          "gene": "ZNF99",
+          "score": 0.355344,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18375,
+          "gene": "ZRANB3",
+          "score": -0.1117185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18302,
+          "gene": "ZNF8",
+          "score": 0.1183505,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18322,
+          "gene": "ZNF836",
+          "score": -0.160919,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18339,
+          "gene": "ZNF878",
+          "score": 0.117919,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18318,
+          "gene": "ZNF83",
+          "score": -0.2179175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18351,
+          "gene": "ZNG1A",
+          "score": 0.0520335,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18290,
+          "gene": "ZNF783",
+          "score": 0.0189365,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18382,
+          "gene": "ZSCAN2",
+          "score": 0.174456,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18380,
+          "gene": "ZSCAN16",
+          "score": 0.02777,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18396,
+          "gene": "ZSCAN9",
+          "score": -0.176105,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18337,
+          "gene": "ZNF865",
+          "score": 0.19303416,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18298,
+          "gene": "ZNF791",
+          "score": 0.0412261,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18317,
+          "gene": "ZNF829",
+          "score": -0.09893,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18343,
+          "gene": "ZNF891",
+          "score": 0.0954565,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18411,
+          "gene": "ZXDB",
+          "score": -0.02779,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18409,
+          "gene": "ZWINT",
+          "score": -0.123792,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18293,
+          "gene": "ZNF786",
+          "score": 0.1072135,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18394,
+          "gene": "ZSCAN5A",
+          "score": 0.34555,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18309,
+          "gene": "ZNF808",
+          "score": -0.113385,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18383,
+          "gene": "ZSCAN20",
+          "score": -0.3234765,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18353,
+          "gene": "ZNG1C",
+          "score": -0.1444645,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18303,
+          "gene": "ZNF80",
+          "score": 0.06814,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18368,
+          "gene": "ZP4",
+          "score": 0.06677535,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18401,
+          "gene": "ZSWIM5",
+          "score": -0.090245,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18304,
+          "gene": "ZNF800",
+          "score": -0.21139,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18307,
+          "gene": "ZNF805",
+          "score": 0.003305,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18397,
+          "gene": "ZSWIM1",
+          "score": 0.1066745,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18301,
+          "gene": "ZNF799",
+          "score": -0.077053,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18398,
+          "gene": "ZSWIM2",
+          "score": 0.08891,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18369,
+          "gene": "ZPBP",
+          "score": -0.208236,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18402,
+          "gene": "ZSWIM6",
+          "score": -0.132565,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18404,
+          "gene": "ZSWIM8",
+          "score": -0.034683,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18410,
+          "gene": "ZXDA",
+          "score": -0.044888,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18395,
+          "gene": "ZSCAN5B",
+          "score": -0.043905,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18367,
+          "gene": "ZP3",
+          "score": 0.179865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18308,
+          "gene": "ZNF806",
+          "score": 0.2282205,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18321,
+          "gene": "ZNF835",
+          "score": 0.1356605,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18347,
+          "gene": "ZNF93",
+          "score": -0.0982335,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18338,
+          "gene": "ZNF875",
+          "score": -0.214485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18297,
+          "gene": "ZNF790",
+          "score": -0.144395,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18344,
+          "gene": "ZNF90",
+          "score": 4.8e-05,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18362,
+          "gene": "ZNRF2",
+          "score": 0.058075,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18352,
+          "gene": "ZNG1B",
+          "score": -0.2631505,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18415,
+          "gene": "ZYX",
+          "score": 0.222654,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18340,
+          "gene": "ZNF879",
+          "score": 0.2543,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18354,
+          "gene": "ZNG1E",
+          "score": -0.091448,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18341,
+          "gene": "ZNF880",
+          "score": 0.0219,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18359,
+          "gene": "ZNHIT6",
+          "score": 0.341157,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18405,
+          "gene": "ZSWIM9",
+          "score": -0.25744,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18316,
+          "gene": "ZNF827",
+          "score": 0.2394125,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18292,
+          "gene": "ZNF785",
+          "score": -0.2707485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18332,
+          "gene": "ZNF850",
+          "score": 0.135435,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18370,
+          "gene": "ZPBP2",
+          "score": -0.0285285,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18358,
+          "gene": "ZNHIT3",
+          "score": -0.1181735,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18295,
+          "gene": "ZNF789",
+          "score": -0.105075,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18399,
+          "gene": "ZSWIM3",
+          "score": -0.242955,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18320,
+          "gene": "ZNF831",
+          "score": 0.0346266,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18328,
+          "gene": "ZNF844",
+          "score": -0.114665,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18381,
+          "gene": "ZSCAN18",
+          "score": -0.49931,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18408,
+          "gene": "ZWILCH",
+          "score": -0.146465,
+          "hit": 0,
+          "round": 1
         }
       ],
       "queried_history": [
@@ -2226,6 +3122,902 @@
           "score": -0.027445,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 18355,
+          "gene": "ZNG1F",
+          "score": 0.02004,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18364,
+          "gene": "ZNRF4",
+          "score": -0.1326135,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18333,
+          "gene": "ZNF852",
+          "score": 0.082401,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18330,
+          "gene": "ZNF846",
+          "score": 0.241646,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18372,
+          "gene": "ZPR1",
+          "score": 0.060205,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18291,
+          "gene": "ZNF784",
+          "score": 0.1521965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18315,
+          "gene": "ZNF823",
+          "score": -0.0882665,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18329,
+          "gene": "ZNF845",
+          "score": 0.174269,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18356,
+          "gene": "ZNHIT1",
+          "score": 0.285865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18312,
+          "gene": "ZNF814",
+          "score": -0.002941,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18377,
+          "gene": "ZSCAN1",
+          "score": 0.0236465,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18363,
+          "gene": "ZNRF3",
+          "score": 0.109025,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18388,
+          "gene": "ZSCAN26",
+          "score": 0.1452,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18384,
+          "gene": "ZSCAN21",
+          "score": -0.06876,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18345,
+          "gene": "ZNF91",
+          "score": 0.072198,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18324,
+          "gene": "ZNF839",
+          "score": 0.058726,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18403,
+          "gene": "ZSWIM7",
+          "score": 0.04798,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18348,
+          "gene": "ZNF98",
+          "score": 0.1414345,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18319,
+          "gene": "ZNF830",
+          "score": -0.385385,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18360,
+          "gene": "ZNRD2",
+          "score": 0.022,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18393,
+          "gene": "ZSCAN4",
+          "score": 0.100399,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18325,
+          "gene": "ZNF84",
+          "score": -0.1180885,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18385,
+          "gene": "ZSCAN22",
+          "score": -0.0139586,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18314,
+          "gene": "ZNF821",
+          "score": 0.152965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18376,
+          "gene": "ZRSR2",
+          "score": -0.105073,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18392,
+          "gene": "ZSCAN32",
+          "score": -0.28131,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18357,
+          "gene": "ZNHIT2",
+          "score": -0.104951,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18417,
+          "gene": "ZZZ3",
+          "score": 0.16858,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18366,
+          "gene": "ZP2",
+          "score": -0.09089255,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18416,
+          "gene": "ZZEF1",
+          "score": 0.2619375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18294,
+          "gene": "ZNF787",
+          "score": -0.025515,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18389,
+          "gene": "ZSCAN29",
+          "score": 0.320085,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18373,
+          "gene": "ZRANB1",
+          "score": 0.32594,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18335,
+          "gene": "ZNF860",
+          "score": -0.165498,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18310,
+          "gene": "ZNF81",
+          "score": 0.0681635,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18336,
+          "gene": "ZNF862",
+          "score": 0.0335655,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18378,
+          "gene": "ZSCAN10",
+          "score": 0.0282885,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18334,
+          "gene": "ZNF853",
+          "score": 0.0603453,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18300,
+          "gene": "ZNF793",
+          "score": -0.21759,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18412,
+          "gene": "ZXDC",
+          "score": 0.10866015,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18365,
+          "gene": "ZP1",
+          "score": -0.1891195,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18391,
+          "gene": "ZSCAN31",
+          "score": 0.0142375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18387,
+          "gene": "ZSCAN25",
+          "score": 0.04001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18306,
+          "gene": "ZNF804B",
+          "score": 0.0680285,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18390,
+          "gene": "ZSCAN30",
+          "score": -0.0656345,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18296,
+          "gene": "ZNF79",
+          "score": 0.052601,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18386,
+          "gene": "ZSCAN23",
+          "score": -0.179549,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18313,
+          "gene": "ZNF816",
+          "score": 0.155999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18346,
+          "gene": "ZNF92",
+          "score": -0.01364915,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18350,
+          "gene": "ZNFX1",
+          "score": -0.118895,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18342,
+          "gene": "ZNF883",
+          "score": -0.19204,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18413,
+          "gene": "ZYG11A",
+          "score": 0.14097,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18379,
+          "gene": "ZSCAN12",
+          "score": 0.31877,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18374,
+          "gene": "ZRANB2",
+          "score": 0.17481,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18406,
+          "gene": "ZUP1",
+          "score": -0.0774975,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18371,
+          "gene": "ZPLD1",
+          "score": 0.26673,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18311,
+          "gene": "ZNF813",
+          "score": 0.1106155,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18400,
+          "gene": "ZSWIM4",
+          "score": -0.2097455,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18299,
+          "gene": "ZNF792",
+          "score": -0.290714,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18331,
+          "gene": "ZNF85",
+          "score": -0.1081275,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18414,
+          "gene": "ZYG11B",
+          "score": -0.1208665,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18323,
+          "gene": "ZNF837",
+          "score": -0.24985,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18327,
+          "gene": "ZNF843",
+          "score": -0.21766,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18407,
+          "gene": "ZW10",
+          "score": -0.159709,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18326,
+          "gene": "ZNF841",
+          "score": -0.245215,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18305,
+          "gene": "ZNF804A",
+          "score": 0.1808675,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18361,
+          "gene": "ZNRF1",
+          "score": -0.1483935,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18349,
+          "gene": "ZNF99",
+          "score": 0.355344,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18375,
+          "gene": "ZRANB3",
+          "score": -0.1117185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18302,
+          "gene": "ZNF8",
+          "score": 0.1183505,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18322,
+          "gene": "ZNF836",
+          "score": -0.160919,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18339,
+          "gene": "ZNF878",
+          "score": 0.117919,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18318,
+          "gene": "ZNF83",
+          "score": -0.2179175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18351,
+          "gene": "ZNG1A",
+          "score": 0.0520335,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18290,
+          "gene": "ZNF783",
+          "score": 0.0189365,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18382,
+          "gene": "ZSCAN2",
+          "score": 0.174456,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18380,
+          "gene": "ZSCAN16",
+          "score": 0.02777,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18396,
+          "gene": "ZSCAN9",
+          "score": -0.176105,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18337,
+          "gene": "ZNF865",
+          "score": 0.19303416,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18298,
+          "gene": "ZNF791",
+          "score": 0.0412261,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18317,
+          "gene": "ZNF829",
+          "score": -0.09893,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18343,
+          "gene": "ZNF891",
+          "score": 0.0954565,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18411,
+          "gene": "ZXDB",
+          "score": -0.02779,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18409,
+          "gene": "ZWINT",
+          "score": -0.123792,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18293,
+          "gene": "ZNF786",
+          "score": 0.1072135,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18394,
+          "gene": "ZSCAN5A",
+          "score": 0.34555,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18309,
+          "gene": "ZNF808",
+          "score": -0.113385,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18383,
+          "gene": "ZSCAN20",
+          "score": -0.3234765,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18353,
+          "gene": "ZNG1C",
+          "score": -0.1444645,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18303,
+          "gene": "ZNF80",
+          "score": 0.06814,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18368,
+          "gene": "ZP4",
+          "score": 0.06677535,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18401,
+          "gene": "ZSWIM5",
+          "score": -0.090245,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18304,
+          "gene": "ZNF800",
+          "score": -0.21139,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18307,
+          "gene": "ZNF805",
+          "score": 0.003305,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18397,
+          "gene": "ZSWIM1",
+          "score": 0.1066745,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18301,
+          "gene": "ZNF799",
+          "score": -0.077053,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18398,
+          "gene": "ZSWIM2",
+          "score": 0.08891,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18369,
+          "gene": "ZPBP",
+          "score": -0.208236,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18402,
+          "gene": "ZSWIM6",
+          "score": -0.132565,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18404,
+          "gene": "ZSWIM8",
+          "score": -0.034683,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18410,
+          "gene": "ZXDA",
+          "score": -0.044888,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18395,
+          "gene": "ZSCAN5B",
+          "score": -0.043905,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18367,
+          "gene": "ZP3",
+          "score": 0.179865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18308,
+          "gene": "ZNF806",
+          "score": 0.2282205,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18321,
+          "gene": "ZNF835",
+          "score": 0.1356605,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18347,
+          "gene": "ZNF93",
+          "score": -0.0982335,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18338,
+          "gene": "ZNF875",
+          "score": -0.214485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18297,
+          "gene": "ZNF790",
+          "score": -0.144395,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18344,
+          "gene": "ZNF90",
+          "score": 4.8e-05,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18362,
+          "gene": "ZNRF2",
+          "score": 0.058075,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18352,
+          "gene": "ZNG1B",
+          "score": -0.2631505,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18415,
+          "gene": "ZYX",
+          "score": 0.222654,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18340,
+          "gene": "ZNF879",
+          "score": 0.2543,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18354,
+          "gene": "ZNG1E",
+          "score": -0.091448,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18341,
+          "gene": "ZNF880",
+          "score": 0.0219,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18359,
+          "gene": "ZNHIT6",
+          "score": 0.341157,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18405,
+          "gene": "ZSWIM9",
+          "score": -0.25744,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18316,
+          "gene": "ZNF827",
+          "score": 0.2394125,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18292,
+          "gene": "ZNF785",
+          "score": -0.2707485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18332,
+          "gene": "ZNF850",
+          "score": 0.135435,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18370,
+          "gene": "ZPBP2",
+          "score": -0.0285285,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18358,
+          "gene": "ZNHIT3",
+          "score": -0.1181735,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18295,
+          "gene": "ZNF789",
+          "score": -0.105075,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18399,
+          "gene": "ZSWIM3",
+          "score": -0.242955,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18320,
+          "gene": "ZNF831",
+          "score": 0.0346266,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18328,
+          "gene": "ZNF844",
+          "score": -0.114665,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18381,
+          "gene": "ZSCAN18",
+          "score": -0.49931,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18408,
+          "gene": "ZWILCH",
+          "score": -0.146465,
+          "hit": 0,
+          "round": 1
         }
       ]
     }

```
