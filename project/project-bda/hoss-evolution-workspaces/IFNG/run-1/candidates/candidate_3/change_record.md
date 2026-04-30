# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IFNG/run-1/best/current/harness
Generated at: 2026-04-30T06:46:04.437368

## Files Changed

- model.py: modified (added=6, deleted=6, delta=0)
- outputs/metrics.json: modified (added=2428, deleted=636, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -65,11 +65,11 @@
     for idx in candidate_scores:
         candidate_avg_scores[idx] = candidate_scores[idx] / candidate_counts[idx]
     
-    # Calculate total exploration count
-    total_counts = sum(candidate_counts.values())
+    # Calculate total number of observations for UCB exploration bonus
+    total_observations = len(history)
     
     # For each available candidate, calculate UCB score
-    # UCB = mean + sqrt(2 * ln(total_counts) / count)
+    # UCB = mean + sqrt(2 * ln(total_observations) / count)
     # For unexplored candidates, count = 1 for optimistic initialization
     ucb_scores = []
     
@@ -82,7 +82,7 @@
             # Explored candidate
             mean_score = candidate_avg_scores[idx]
             count = candidate_counts[idx]
-            exploration_bonus = np.sqrt(2 * np.log(total_counts) / count)
+            exploration_bonus = np.sqrt(2 * np.log(total_observations) / count) if total_observations > 0 else 0
             ucb = mean_score + exploration_bonus
         else:
             # Unexplored candidate - use optimistic initialization
@@ -92,8 +92,8 @@
                 # Bias exploration toward negative scores (hits are at -0.4 to -0.5)
                 ucb_negative = min_observed_score - 0.1 * abs(min_observed_score) if min_observed_score != 0 else -1.0
                 ucb_positive = max_observed_score + 0.1 * abs(max_observed_score) if max_observed_score != 0 else 1.0
-                # Blend: 70% weight on negative exploration (hits), 30% on positive
-                ucb = 0.7 * ucb_negative + 0.3 * ucb_positive
+                # Blend: 75% weight on negative exploration (hits), 25% on positive
+                ucb = 0.75 * ucb_negative + 0.25 * ucb_positive
             else:
                 ucb = -1.0  # Start with negative bias for unexplored
         ucb_scores.append((ucb, idx))

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18418,
-      "rounds": 2,
+      "rounds": 3,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 128,
-      "baseline_total_hits": 2,
+      "baseline_total_queries": 256,
+      "baseline_total_hits": 3,
       "delta_queries": 128,
-      "delta_hits": 1,
-      "total_queries": 256,
-      "total_hits": 3,
+      "delta_hits": 5,
+      "total_queries": 384,
+      "total_hits": 8,
       "top_k": 920,
       "hit_curve": {
         "queries": [
-          128,
-          256
+          256,
+          384
         ],
         "hits": [
-          2,
-          3
+          3,
+          8
         ]
       },
-      "auc": 320.0,
-      "auc_normalized": 0.001358695652173913,
-      "ncg": 0.14329897550565224,
+      "auc": 704.0,
+      "auc_normalized": 0.0019927536231884057,
+      "ncg": 0.16944364830290376,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 1,
-          "cumulative_hits": 3,
-          "precision_at_batch": 0.0078125,
+          "hits": 5,
+          "cumulative_hits": 8,
+          "precision_at_batch": 0.0390625,
           "selected": [
-            "ZNG1F",
-            "ZNRF4",
-            "ZNF852",
-            "ZNF846",
-            "ZPR1",
-            "ZNF784",
-            "ZNF823",
-            "ZNF845",
-            "ZNHIT1",
-            "ZNF814",
-            "ZSCAN1",
-            "ZNRF3",
-            "ZSCAN26",
-            "ZSCAN21",
-            "ZNF91",
-            "ZNF839",
-            "ZSWIM7",
-            "ZNF98",
-            "ZNF830",
-            "ZNRD2",
-            "ZSCAN4",
-            "ZNF84",
-            "ZSCAN22",
-            "ZNF821",
-            "ZRSR2",
-            "ZSCAN32",
-            "ZNHIT2",
-            "ZZZ3",
-            "ZP2",
-            "ZZEF1",
-            "ZNF787",
-            "ZSCAN29",
-            "ZRANB1",
-            "ZNF860",
-            "ZNF81",
-            "ZNF862",
-            "ZSCAN10",
-            "ZNF853",
-            "ZNF793",
-            "ZXDC",
-            "ZP1",
-            "ZSCAN31",
-            "ZSCAN25",
-            "ZNF804B",
-            "ZSCAN30",
-            "ZNF79",
-            "ZSCAN23",
-            "ZNF816",
-            "ZNF92",
-            "ZNFX1",
-            "ZNF883",
-            "ZYG11A",
-            "ZSCAN12",
-            "ZRANB2",
-            "ZUP1",
-            "ZPLD1",
-            "ZNF813",
-            "ZSWIM4",
-            "ZNF792",
-            "ZNF85",
-            "ZYG11B",
-            "ZNF837",
-            "ZNF843",
-            "ZW10",
-            "ZNF841",
-            "ZNF804A",
-            "ZNRF1",
-            "ZNF99",
-            "ZRANB3",
-            "ZNF8",
-            "ZNF836",
-            "ZNF878",
-            "ZNF83",
-            "ZNG1A",
-            "ZNF783",
-            "ZSCAN2",
-            "ZSCAN16",
-            "ZSCAN9",
-            "ZNF865",
-            "ZNF791",
-            "ZNF829",
-            "ZNF891",
-            "ZXDB",
-            "ZWINT",
-            "ZNF786",
-            "ZSCAN5A",
-            "ZNF808",
-            "ZSCAN20",
-            "ZNG1C",
-            "ZNF80",
-            "ZP4",
-            "ZSWIM5",
-            "ZNF800",
-            "ZNF805",
-            "ZSWIM1",
-            "ZNF799",
-            "ZSWIM2",
-            "ZPBP",
-            "ZSWIM6",
-            "ZSWIM8",
-            "ZXDA",
-            "ZSCAN5B",
-            "ZP3",
-            "ZNF806",
-            "ZNF835",
-            "ZNF93",
-            "ZNF875",
-            "ZNF790",
-            "ZNF90",
-            "ZNRF2",
-            "ZNG1B",
-            "ZYX",
-            "ZNF879",
-            "ZNG1E",
-            "ZNF880",
-            "ZNHIT6",
-            "ZSWIM9",
-            "ZNF827",
-            "ZNF785",
-            "ZNF850",
-            "ZPBP2",
-            "ZNHIT3",
-            "ZNF789",
-            "ZSWIM3",
-            "ZNF831",
-            "ZNF844",
-            "ZSCAN18",
-            "ZWILCH"
+            "ZNF655",
+            "ZNF703",
+            "ZNF658",
+            "ZNF608",
+            "ZNF618",
+            "ZNF605",
+            "ZNF681",
+            "ZNF771",
+            "ZNF687",
+            "ZNF682",
+            "ZNF609",
+            "ZNF606",
+            "ZNF730",
+            "ZNF689",
+            "ZNF649",
+            "ZNF70",
+            "ZNF671",
+            "ZNF607",
+            "ZNF69",
+            "ZNF701",
+            "ZNF766",
+            "ZNF74",
+            "ZNF684",
+            "ZNF678",
+            "ZNF670",
+            "ZNF621",
+            "ZNF705B",
+            "ZNF76",
+            "ZNF620",
+            "ZNF740",
+            "ZNF616",
+            "ZNF75A",
+            "ZNF749",
+            "ZNF775",
+            "ZNF746",
+            "ZNF677",
+            "ZNF654",
+            "ZNF705D",
+            "ZNF761",
+            "ZNF695",
+            "ZNF727",
+            "ZNF641",
+            "ZNF627",
+            "ZNF697",
+            "ZNF709",
+            "ZNF696",
+            "ZNF782",
+            "ZNF772",
+            "ZNF764",
+            "ZNF780B",
+            "ZNF705A",
+            "ZNF717",
+            "ZNF611",
+            "ZNF653",
+            "ZNF662",
+            "ZNF705G",
+            "ZNF736",
+            "ZNF735",
+            "ZNF660",
+            "ZNF652",
+            "ZNF668",
+            "ZNF639",
+            "ZNF672",
+            "ZNF700",
+            "ZNF679",
+            "ZNF708",
+            "ZNF713",
+            "ZNF629",
+            "ZNF704",
+            "ZNF777",
+            "ZNF776",
+            "ZNF732",
+            "ZNF729",
+            "ZNF765",
+            "ZNF644",
+            "ZNF747",
+            "ZNF7",
+            "ZNF699",
+            "ZNF667",
+            "ZNF706",
+            "ZNF710",
+            "ZNF778",
+            "ZNF615",
+            "ZNF675",
+            "ZNF77",
+            "ZNF716",
+            "ZNF728",
+            "ZNF622",
+            "ZNF638",
+            "ZNF774",
+            "ZNF625",
+            "ZNF619",
+            "ZNF623",
+            "ZNF676",
+            "ZNF726",
+            "ZNF711",
+            "ZNF773",
+            "ZNF71",
+            "ZNF714",
+            "ZNF669",
+            "ZNF628",
+            "ZNF648",
+            "ZNF705E",
+            "ZNF680",
+            "ZNF613",
+            "ZNF674",
+            "ZNF626",
+            "ZNF718",
+            "ZNF665",
+            "ZNF692",
+            "ZNF646",
+            "ZNF75D",
+            "ZNF770",
+            "ZNF781",
+            "ZNF683",
+            "ZNF610",
+            "ZNF614",
+            "ZNF780A",
+            "ZNF721",
+            "ZNF737",
+            "ZNF707",
+            "ZNF750",
+            "ZNF768",
+            "ZNF624",
+            "ZNF664",
+            "ZNF688",
+            "ZNF691",
+            "ZNF630"
           ],
           "selected_scores": [
-            0.02004,
-            -0.1326135,
-            0.082401,
-            0.241646,
-            0.060205,
-            0.1521965,
-            -0.0882665,
-            0.174269,
-            0.285865,
-            -0.002941,
-            0.0236465,
-            0.109025,
-            0.1452,
-            -0.06876,
-            0.072198,
-            0.058726,
-            0.04798,
-            0.1414345,
-            -0.385385,
-            0.022,
-            0.100399,
-            -0.1180885,
-            -0.0139586,
-            0.152965,
-            -0.105073,
-            -0.28131,
-            -0.104951,
-            0.16858,
-            -0.09089255,
-            0.2619375,
-            -0.025515,
-            0.320085,
-            0.32594,
-            -0.165498,
-            0.0681635,
-            0.0335655,
-            0.0282885,
-            0.0603453,
-            -0.21759,
-            0.10866015,
-            -0.1891195,
-            0.0142375,
-            0.04001,
-            0.0680285,
-            -0.0656345,
-            0.052601,
-            -0.179549,
-            0.155999,
-            -0.01364915,
-            -0.118895,
-            -0.19204,
-            0.14097,
-            0.31877,
-            0.17481,
-            -0.0774975,
-            0.26673,
-            0.1106155,
-            -0.2097455,
-            -0.290714,
-            -0.1081275,
-            -0.1208665,
-            -0.24985,
-            -0.21766,
-            -0.159709,
-            -0.245215,
-            0.1808675,
-            -0.1483935,
-            0.355344,
-            -0.1117185,
-            0.1183505,
-            -0.160919,
-            0.117919,
-            -0.2179175,
-            0.0520335,
-            0.0189365,
-            0.174456,
-            0.02777,
-            -0.176105,
-            0.19303416,
-            0.0412261,
-            -0.09893,
-            0.0954565,
-            -0.02779,
-            -0.123792,
-            0.1072135,
-            0.34555,
-            -0.113385,
-            -0.3234765,
-            -0.1444645,
-            0.06814,
-            0.06677535,
-            -0.090245,
-            -0.21139,
-            0.003305,
-            0.1066745,
-            -0.077053,
-            0.08891,
-            -0.208236,
-            -0.132565,
-            -0.034683,
-            -0.044888,
-            -0.043905,
-            0.179865,
-            0.2282205,
-            0.1356605,
-            -0.0982335,
-            -0.214485,
-            -0.144395,
-            4.8e-05,
-            0.058075,
-            -0.2631505,
-            0.222654,
-            0.2543,
-            -0.091448,
-            0.0219,
-            0.341157,
-            -0.25744,
-            0.2394125,
-            -0.2707485,
-            0.135435,
-            -0.0285285,
-            -0.1181735,
-            -0.105075,
-            -0.242955,
-            0.0346266,
-            -0.114665,
-            -0.49931,
-            -0.146465
+            -0.1833125,
+            -0.0852,
+            0.044175,
+            0.2987305,
+            -0.190475,
+            -0.13111839,
+            0.128045,
+            -0.149708,
+            -0.262595,
+            -0.199155,
+            -0.32101,
+            0.069635,
+            -0.06505,
+            -0.02664,
+            -0.091537,
+            -0.0901975,
+            0.09395745,
+            -0.0026525,
+            -0.1912095,
+            -0.391055,
+            0.07028355,
+            -0.443155,
+            0.113969,
+            0.1374395,
+            0.289355,
+            0.086152,
+            -0.059855,
+            0.013145,
+            -0.16560645,
+            0.1171905,
+            0.106625,
+            0.2089455,
+            0.027157,
+            -0.446395,
+            0.39508,
+            -0.044635,
+            -0.09401,
+            -0.2711,
+            -0.29709,
+            -0.0494725,
+            -0.08205,
+            -0.1801195,
+            0.006615,
+            0.33112,
+            0.0628615,
+            -0.005585,
+            -0.07841,
+            -0.227325,
+            0.14892,
+            -0.15895,
+            0.0939665,
+            0.251,
+            0.28251,
+            -0.146895,
+            -0.1954055,
+            0.05468,
+            -0.014509,
+            0.02091,
+            -0.12729,
+            0.1074805,
+            0.0942455,
+            -0.478455,
+            0.091869,
+            0.070234,
+            -0.029394,
+            0.0181625,
+            0.15265,
+            0.3354,
+            -0.093379,
+            0.1705515,
+            -0.00751,
+            0.1017415,
+            0.012581,
+            -0.389585,
+            0.280492,
+            -0.00157,
+            -0.0977735,
+            -0.1837,
+            0.03447775,
+            -0.02961,
+            0.09547,
+            0.1257655,
+            0.1941805,
+            0.31613,
+            0.158275,
+            0.006445,
+            0.1207145,
+            0.085554,
+            -0.156016,
+            0.0492925,
+            0.2007245,
+            0.227995,
+            -0.209705,
+            -0.0869881,
+            0.00325,
+            0.1338245,
+            0.130544,
+            -0.189513,
+            0.20327,
+            0.0332529,
+            0.02386,
+            0.239318,
+            -0.256575,
+            -0.0800905,
+            0.04389,
+            0.011945,
+            -0.145603,
+            -0.0575795,
+            -0.03955195,
+            0.29731,
+            0.1066445,
+            0.1355,
+            -0.0537535,
+            -0.31094,
+            0.0220375,
+            0.12294,
+            -0.05491,
+            0.1124055,
+            0.26879,
+            0.216225,
+            0.37715,
+            0.031711,
+            0.01482,
+            -0.127621,
+            0.0808805,
+            -0.0863065,
+            -0.1299145,
+            0.08269
           ],
           "selected_hits": [
             0,
@@ -320,114 +320,114 @@
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
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
             1,
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
             0
           ]
         }
@@ -1334,896 +1334,1792 @@
           "gene": "ZNG1F",
           "score": 0.02004,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18364,
           "gene": "ZNRF4",
           "score": -0.1326135,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18333,
           "gene": "ZNF852",
           "score": 0.082401,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18330,
           "gene": "ZNF846",
           "score": 0.241646,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18372,
           "gene": "ZPR1",
           "score": 0.060205,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18291,
           "gene": "ZNF784",
           "score": 0.1521965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18315,
           "gene": "ZNF823",
           "score": -0.0882665,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18329,
           "gene": "ZNF845",
           "score": 0.174269,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18356,
           "gene": "ZNHIT1",
           "score": 0.285865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18312,
           "gene": "ZNF814",
           "score": -0.002941,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18377,
           "gene": "ZSCAN1",
           "score": 0.0236465,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18363,
           "gene": "ZNRF3",
           "score": 0.109025,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18388,
           "gene": "ZSCAN26",
           "score": 0.1452,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18384,
           "gene": "ZSCAN21",
           "score": -0.06876,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18345,
           "gene": "ZNF91",
           "score": 0.072198,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18324,
           "gene": "ZNF839",
           "score": 0.058726,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18403,
           "gene": "ZSWIM7",
           "score": 0.04798,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18348,
           "gene": "ZNF98",
           "score": 0.1414345,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18319,
           "gene": "ZNF830",
           "score": -0.385385,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18360,
           "gene": "ZNRD2",
           "score": 0.022,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18393,
           "gene": "ZSCAN4",
           "score": 0.100399,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18325,
           "gene": "ZNF84",
           "score": -0.1180885,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18385,
           "gene": "ZSCAN22",
           "score": -0.0139586,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18314,
           "gene": "ZNF821",
           "score": 0.152965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18376,
           "gene": "ZRSR2",
           "score": -0.105073,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18392,
           "gene": "ZSCAN32",
           "score": -0.28131,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18357,
           "gene": "ZNHIT2",
           "score": -0.104951,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18417,
           "gene": "ZZZ3",
           "score": 0.16858,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18366,
           "gene": "ZP2",
           "score": -0.09089255,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18416,
           "gene": "ZZEF1",
           "score": 0.2619375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18294,
           "gene": "ZNF787",
           "score": -0.025515,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18389,
           "gene": "ZSCAN29",
           "score": 0.320085,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18373,
           "gene": "ZRANB1",
           "score": 0.32594,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18335,
           "gene": "ZNF860",
           "score": -0.165498,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18310,
           "gene": "ZNF81",
           "score": 0.0681635,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18336,
           "gene": "ZNF862",
           "score": 0.0335655,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18378,
           "gene": "ZSCAN10",
           "score": 0.0282885,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18334,
           "gene": "ZNF853",
           "score": 0.0603453,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18300,
           "gene": "ZNF793",
           "score": -0.21759,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18412,
           "gene": "ZXDC",
           "score": 0.10866015,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18365,
           "gene": "ZP1",
           "score": -0.1891195,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18391,
           "gene": "ZSCAN31",
           "score": 0.0142375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18387,
           "gene": "ZSCAN25",
           "score": 0.04001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18306,
           "gene": "ZNF804B",
           "score": 0.0680285,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18390,
           "gene": "ZSCAN30",
           "score": -0.0656345,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18296,
           "gene": "ZNF79",
           "score": 0.052601,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18386,
           "gene": "ZSCAN23",
           "score": -0.179549,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18313,
           "gene": "ZNF816",
           "score": 0.155999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18346,
           "gene": "ZNF92",
           "score": -0.01364915,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18350,
           "gene": "ZNFX1",
           "score": -0.118895,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18342,
           "gene": "ZNF883",
           "score": -0.19204,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18413,
           "gene": "ZYG11A",
           "score": 0.14097,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18379,
           "gene": "ZSCAN12",
           "score": 0.31877,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18374,
           "gene": "ZRANB2",
           "score": 0.17481,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18406,
           "gene": "ZUP1",
           "score": -0.0774975,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18371,
           "gene": "ZPLD1",
           "score": 0.26673,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18311,
           "gene": "ZNF813",
           "score": 0.1106155,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18400,
           "gene": "ZSWIM4",
           "score": -0.2097455,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18299,
           "gene": "ZNF792",
           "score": -0.290714,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18331,
           "gene": "ZNF85",
           "score": -0.1081275,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18414,
           "gene": "ZYG11B",
           "score": -0.1208665,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18323,
           "gene": "ZNF837",
           "score": -0.24985,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18327,
           "gene": "ZNF843",
           "score": -0.21766,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18407,
           "gene": "ZW10",
           "score": -0.159709,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18326,
           "gene": "ZNF841",
           "score": -0.245215,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18305,
           "gene": "ZNF804A",
           "score": 0.1808675,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18361,
           "gene": "ZNRF1",
           "score": -0.1483935,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18349,
           "gene": "ZNF99",
           "score": 0.355344,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18375,
           "gene": "ZRANB3",
           "score": -0.1117185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18302,
           "gene": "ZNF8",
           "score": 0.1183505,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18322,
           "gene": "ZNF836",
           "score": -0.160919,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18339,
           "gene": "ZNF878",
           "score": 0.117919,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18318,
           "gene": "ZNF83",
           "score": -0.2179175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18351,
           "gene": "ZNG1A",
           "score": 0.0520335,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18290,
           "gene": "ZNF783",
           "score": 0.0189365,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18382,
           "gene": "ZSCAN2",
           "score": 0.174456,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18380,
           "gene": "ZSCAN16",
           "score": 0.02777,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18396,
           "gene": "ZSCAN9",
           "score": -0.176105,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18337,
           "gene": "ZNF865",
           "score": 0.19303416,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18298,
           "gene": "ZNF791",
           "score": 0.0412261,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18317,
           "gene": "ZNF829",
           "score": -0.09893,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18343,
           "gene": "ZNF891",
           "score": 0.0954565,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18411,
           "gene": "ZXDB",
           "score": -0.02779,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18409,
           "gene": "ZWINT",
           "score": -0.123792,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18293,
           "gene": "ZNF786",
           "score": 0.1072135,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18394,
           "gene": "ZSCAN5A",
           "score": 0.34555,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18309,
           "gene": "ZNF808",
           "score": -0.113385,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18383,
           "gene": "ZSCAN20",
           "score": -0.3234765,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18353,
           "gene": "ZNG1C",
           "score": -0.1444645,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18303,
           "gene": "ZNF80",
           "score": 0.06814,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18368,
           "gene": "ZP4",
           "score": 0.06677535,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18401,
           "gene": "ZSWIM5",
           "score": -0.090245,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18304,
           "gene": "ZNF800",
           "score": -0.21139,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18307,
           "gene": "ZNF805",
           "score": 0.003305,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18397,
           "gene": "ZSWIM1",
           "score": 0.1066745,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18301,
           "gene": "ZNF799",
           "score": -0.077053,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18398,
           "gene": "ZSWIM2",
           "score": 0.08891,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18369,
           "gene": "ZPBP",
           "score": -0.208236,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18402,
           "gene": "ZSWIM6",
           "score": -0.132565,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18404,
           "gene": "ZSWIM8",
           "score": -0.034683,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18410,
           "gene": "ZXDA",
           "score": -0.044888,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18395,
           "gene": "ZSCAN5B",
           "score": -0.043905,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18367,
           "gene": "ZP3",
           "score": 0.179865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18308,
           "gene": "ZNF806",
           "score": 0.2282205,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18321,
           "gene": "ZNF835",
           "score": 0.1356605,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18347,
           "gene": "ZNF93",
           "score": -0.0982335,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18338,
           "gene": "ZNF875",
           "score": -0.214485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18297,
           "gene": "ZNF790",
           "score": -0.144395,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18344,
           "gene": "ZNF90",
           "score": 4.8e-05,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18362,
           "gene": "ZNRF2",
           "score": 0.058075,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18352,
           "gene": "ZNG1B",
           "score": -0.2631505,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18415,
           "gene": "ZYX",
           "score": 0.222654,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18340,
           "gene": "ZNF879",
           "score": 0.2543,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18354,
           "gene": "ZNG1E",
           "score": -0.091448,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18341,
           "gene": "ZNF880",
           "score": 0.0219,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18359,
           "gene": "ZNHIT6",
           "score": 0.341157,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18405,
           "gene": "ZSWIM9",
           "score": -0.25744,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18316,
           "gene": "ZNF827",
           "score": 0.2394125,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18292,
           "gene": "ZNF785",
           "score": -0.2707485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18332,
           "gene": "ZNF850",
           "score": 0.135435,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18370,
           "gene": "ZPBP2",
           "score": -0.0285285,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18358,
           "gene": "ZNHIT3",
           "score": -0.1181735,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18295,
           "gene": "ZNF789",
           "score": -0.105075,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18399,
           "gene": "ZSWIM3",
           "score": -0.242955,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18320,
           "gene": "ZNF831",
           "score": 0.0346266,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18328,
           "gene": "ZNF844",
           "score": -0.114665,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18381,
           "gene": "ZSCAN18",
           "score": -0.49931,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18408,
           "gene": "ZWILCH",
           "score": -0.146465,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 18196,
+          "gene": "ZNF655",
+          "score": -0.1833125,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18233,
+          "gene": "ZNF703",
+          "score": -0.0852,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18197,
+          "gene": "ZNF658",
+          "score": 0.044175,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18165,
+          "gene": "ZNF608",
+          "score": 0.2987305,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18173,
+          "gene": "ZNF618",
+          "score": -0.190475,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18162,
+          "gene": "ZNF605",
+          "score": -0.13111839,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18215,
+          "gene": "ZNF681",
+          "score": 0.128045,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18278,
+          "gene": "ZNF771",
+          "score": -0.149708,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18219,
+          "gene": "ZNF687",
+          "score": -0.262595,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18216,
+          "gene": "ZNF682",
+          "score": -0.199155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18166,
+          "gene": "ZNF609",
+          "score": -0.32101,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18163,
+          "gene": "ZNF606",
+          "score": 0.069635,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18257,
+          "gene": "ZNF730",
+          "score": -0.06505,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18221,
+          "gene": "ZNF689",
+          "score": -0.02664,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18192,
+          "gene": "ZNF649",
+          "score": -0.091537,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18230,
+          "gene": "ZNF70",
+          "score": -0.0901975,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18206,
+          "gene": "ZNF671",
+          "score": 0.09395745,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18164,
+          "gene": "ZNF607",
+          "score": -0.0026525,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18222,
+          "gene": "ZNF69",
+          "score": -0.1912095,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18232,
+          "gene": "ZNF701",
+          "score": -0.391055,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18274,
+          "gene": "ZNF766",
+          "score": 0.07028355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18262,
+          "gene": "ZNF74",
+          "score": -0.443155,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18218,
+          "gene": "ZNF684",
+          "score": 0.113969,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18212,
+          "gene": "ZNF678",
+          "score": 0.1374395,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18205,
+          "gene": "ZNF670",
+          "score": 0.289355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18176,
+          "gene": "ZNF621",
+          "score": 0.086152,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18236,
+          "gene": "ZNF705B",
+          "score": -0.059855,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18270,
+          "gene": "ZNF76",
+          "score": 0.013145,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18175,
+          "gene": "ZNF620",
+          "score": -0.16560645,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18263,
+          "gene": "ZNF740",
+          "score": 0.1171905,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18172,
+          "gene": "ZNF616",
+          "score": 0.106625,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18268,
+          "gene": "ZNF75A",
+          "score": 0.2089455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18266,
+          "gene": "ZNF749",
+          "score": 0.027157,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18282,
+          "gene": "ZNF775",
+          "score": -0.446395,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18264,
+          "gene": "ZNF746",
+          "score": 0.39508,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18211,
+          "gene": "ZNF677",
+          "score": -0.044635,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18195,
+          "gene": "ZNF654",
+          "score": -0.09401,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18237,
+          "gene": "ZNF705D",
+          "score": -0.2711,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18271,
+          "gene": "ZNF761",
+          "score": -0.29709,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18225,
+          "gene": "ZNF695",
+          "score": -0.0494725,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18254,
+          "gene": "ZNF727",
+          "score": -0.08205,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18188,
+          "gene": "ZNF641",
+          "score": -0.1801195,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18182,
+          "gene": "ZNF627",
+          "score": 0.006615,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18227,
+          "gene": "ZNF697",
+          "score": 0.33112,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18243,
+          "gene": "ZNF709",
+          "score": 0.0628615,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18226,
+          "gene": "ZNF696",
+          "score": -0.005585,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18289,
+          "gene": "ZNF782",
+          "score": -0.07841,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18279,
+          "gene": "ZNF772",
+          "score": -0.227325,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18272,
+          "gene": "ZNF764",
+          "score": 0.14892,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18287,
+          "gene": "ZNF780B",
+          "score": -0.15895,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18235,
+          "gene": "ZNF705A",
+          "score": 0.0939665,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18250,
+          "gene": "ZNF717",
+          "score": 0.251,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18168,
+          "gene": "ZNF611",
+          "score": 0.28251,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18194,
+          "gene": "ZNF653",
+          "score": -0.146895,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18199,
+          "gene": "ZNF662",
+          "score": -0.1954055,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18239,
+          "gene": "ZNF705G",
+          "score": 0.05468,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18260,
+          "gene": "ZNF736",
+          "score": -0.014509,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18259,
+          "gene": "ZNF735",
+          "score": 0.02091,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18198,
+          "gene": "ZNF660",
+          "score": -0.12729,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18193,
+          "gene": "ZNF652",
+          "score": 0.1074805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18203,
+          "gene": "ZNF668",
+          "score": 0.0942455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18187,
+          "gene": "ZNF639",
+          "score": -0.478455,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18207,
+          "gene": "ZNF672",
+          "score": 0.091869,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18231,
+          "gene": "ZNF700",
+          "score": 0.070234,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18213,
+          "gene": "ZNF679",
+          "score": -0.029394,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18242,
+          "gene": "ZNF708",
+          "score": 0.0181625,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18247,
+          "gene": "ZNF713",
+          "score": 0.15265,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18184,
+          "gene": "ZNF629",
+          "score": 0.3354,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18234,
+          "gene": "ZNF704",
+          "score": -0.093379,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18284,
+          "gene": "ZNF777",
+          "score": 0.1705515,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18283,
+          "gene": "ZNF776",
+          "score": -0.00751,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18258,
+          "gene": "ZNF732",
+          "score": 0.1017415,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18256,
+          "gene": "ZNF729",
+          "score": 0.012581,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18273,
+          "gene": "ZNF765",
+          "score": -0.389585,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18189,
+          "gene": "ZNF644",
+          "score": 0.280492,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18265,
+          "gene": "ZNF747",
+          "score": -0.00157,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18229,
+          "gene": "ZNF7",
+          "score": -0.0977735,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18228,
+          "gene": "ZNF699",
+          "score": -0.1837,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18202,
+          "gene": "ZNF667",
+          "score": 0.03447775,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18240,
+          "gene": "ZNF706",
+          "score": -0.02961,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18245,
+          "gene": "ZNF710",
+          "score": 0.09547,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18285,
+          "gene": "ZNF778",
+          "score": 0.1257655,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18171,
+          "gene": "ZNF615",
+          "score": 0.1941805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18209,
+          "gene": "ZNF675",
+          "score": 0.31613,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18276,
+          "gene": "ZNF77",
+          "score": 0.158275,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18249,
+          "gene": "ZNF716",
+          "score": 0.006445,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18255,
+          "gene": "ZNF728",
+          "score": 0.1207145,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18177,
+          "gene": "ZNF622",
+          "score": 0.085554,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18186,
+          "gene": "ZNF638",
+          "score": -0.156016,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18281,
+          "gene": "ZNF774",
+          "score": 0.0492925,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18180,
+          "gene": "ZNF625",
+          "score": 0.2007245,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18174,
+          "gene": "ZNF619",
+          "score": 0.227995,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18178,
+          "gene": "ZNF623",
+          "score": -0.209705,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18210,
+          "gene": "ZNF676",
+          "score": -0.0869881,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18253,
+          "gene": "ZNF726",
+          "score": 0.00325,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18246,
+          "gene": "ZNF711",
+          "score": 0.1338245,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18280,
+          "gene": "ZNF773",
+          "score": 0.130544,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18244,
+          "gene": "ZNF71",
+          "score": -0.189513,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18248,
+          "gene": "ZNF714",
+          "score": 0.20327,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18204,
+          "gene": "ZNF669",
+          "score": 0.0332529,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18183,
+          "gene": "ZNF628",
+          "score": 0.02386,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18191,
+          "gene": "ZNF648",
+          "score": 0.239318,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18238,
+          "gene": "ZNF705E",
+          "score": -0.256575,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18214,
+          "gene": "ZNF680",
+          "score": -0.0800905,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18169,
+          "gene": "ZNF613",
+          "score": 0.04389,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18208,
+          "gene": "ZNF674",
+          "score": 0.011945,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18181,
+          "gene": "ZNF626",
+          "score": -0.145603,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18251,
+          "gene": "ZNF718",
+          "score": -0.0575795,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18201,
+          "gene": "ZNF665",
+          "score": -0.03955195,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18224,
+          "gene": "ZNF692",
+          "score": 0.29731,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18190,
+          "gene": "ZNF646",
+          "score": 0.1066445,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18269,
+          "gene": "ZNF75D",
+          "score": 0.1355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18277,
+          "gene": "ZNF770",
+          "score": -0.0537535,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18288,
+          "gene": "ZNF781",
+          "score": -0.31094,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18217,
+          "gene": "ZNF683",
+          "score": 0.0220375,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18167,
+          "gene": "ZNF610",
+          "score": 0.12294,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18170,
+          "gene": "ZNF614",
+          "score": -0.05491,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18286,
+          "gene": "ZNF780A",
+          "score": 0.1124055,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18252,
+          "gene": "ZNF721",
+          "score": 0.26879,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18261,
+          "gene": "ZNF737",
+          "score": 0.216225,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18241,
+          "gene": "ZNF707",
+          "score": 0.37715,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18267,
+          "gene": "ZNF750",
+          "score": 0.031711,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18275,
+          "gene": "ZNF768",
+          "score": 0.01482,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18179,
+          "gene": "ZNF624",
+          "score": -0.127621,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18200,
+          "gene": "ZNF664",
+          "score": 0.0808805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18220,
+          "gene": "ZNF688",
+          "score": -0.0863065,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18223,
+          "gene": "ZNF691",
+          "score": -0.1299145,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18185,
+          "gene": "ZNF630",
+          "score": 0.08269,
+          "hit": 0,
+          "round": 2
         }
       ],
       "queried_history": [
@@ -3128,896 +4024,1792 @@
           "gene": "ZNG1F",
           "score": 0.02004,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18364,
           "gene": "ZNRF4",
           "score": -0.1326135,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18333,
           "gene": "ZNF852",
           "score": 0.082401,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18330,
           "gene": "ZNF846",
           "score": 0.241646,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18372,
           "gene": "ZPR1",
           "score": 0.060205,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18291,
           "gene": "ZNF784",
           "score": 0.1521965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18315,
           "gene": "ZNF823",
           "score": -0.0882665,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18329,
           "gene": "ZNF845",
           "score": 0.174269,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18356,
           "gene": "ZNHIT1",
           "score": 0.285865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18312,
           "gene": "ZNF814",
           "score": -0.002941,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18377,
           "gene": "ZSCAN1",
           "score": 0.0236465,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18363,
           "gene": "ZNRF3",
           "score": 0.109025,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18388,
           "gene": "ZSCAN26",
           "score": 0.1452,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18384,
           "gene": "ZSCAN21",
           "score": -0.06876,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18345,
           "gene": "ZNF91",
           "score": 0.072198,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18324,
           "gene": "ZNF839",
           "score": 0.058726,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18403,
           "gene": "ZSWIM7",
           "score": 0.04798,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18348,
           "gene": "ZNF98",
           "score": 0.1414345,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18319,
           "gene": "ZNF830",
           "score": -0.385385,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18360,
           "gene": "ZNRD2",
           "score": 0.022,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18393,
           "gene": "ZSCAN4",
           "score": 0.100399,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18325,
           "gene": "ZNF84",
           "score": -0.1180885,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18385,
           "gene": "ZSCAN22",
           "score": -0.0139586,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18314,
           "gene": "ZNF821",
           "score": 0.152965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18376,
           "gene": "ZRSR2",
           "score": -0.105073,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18392,
           "gene": "ZSCAN32",
           "score": -0.28131,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18357,
           "gene": "ZNHIT2",
           "score": -0.104951,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18417,
           "gene": "ZZZ3",
           "score": 0.16858,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18366,
           "gene": "ZP2",
           "score": -0.09089255,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18416,
           "gene": "ZZEF1",
           "score": 0.2619375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18294,
           "gene": "ZNF787",
           "score": -0.025515,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18389,
           "gene": "ZSCAN29",
           "score": 0.320085,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18373,
           "gene": "ZRANB1",
           "score": 0.32594,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18335,
           "gene": "ZNF860",
           "score": -0.165498,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18310,
           "gene": "ZNF81",
           "score": 0.0681635,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18336,
           "gene": "ZNF862",
           "score": 0.0335655,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18378,
           "gene": "ZSCAN10",
           "score": 0.0282885,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18334,
           "gene": "ZNF853",
           "score": 0.0603453,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18300,
           "gene": "ZNF793",
           "score": -0.21759,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18412,
           "gene": "ZXDC",
           "score": 0.10866015,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18365,
           "gene": "ZP1",
           "score": -0.1891195,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18391,
           "gene": "ZSCAN31",
           "score": 0.0142375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18387,
           "gene": "ZSCAN25",
           "score": 0.04001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18306,
           "gene": "ZNF804B",
           "score": 0.0680285,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18390,
           "gene": "ZSCAN30",
           "score": -0.0656345,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18296,
           "gene": "ZNF79",
           "score": 0.052601,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18386,
           "gene": "ZSCAN23",
           "score": -0.179549,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18313,
           "gene": "ZNF816",
           "score": 0.155999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18346,
           "gene": "ZNF92",
           "score": -0.01364915,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18350,
           "gene": "ZNFX1",
           "score": -0.118895,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18342,
           "gene": "ZNF883",
           "score": -0.19204,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18413,
           "gene": "ZYG11A",
           "score": 0.14097,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18379,
           "gene": "ZSCAN12",
           "score": 0.31877,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18374,
           "gene": "ZRANB2",
           "score": 0.17481,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18406,
           "gene": "ZUP1",
           "score": -0.0774975,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18371,
           "gene": "ZPLD1",
           "score": 0.26673,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18311,
           "gene": "ZNF813",
           "score": 0.1106155,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18400,
           "gene": "ZSWIM4",
           "score": -0.2097455,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18299,
           "gene": "ZNF792",
           "score": -0.290714,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18331,
           "gene": "ZNF85",
           "score": -0.1081275,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18414,
           "gene": "ZYG11B",
           "score": -0.1208665,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18323,
           "gene": "ZNF837",
           "score": -0.24985,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18327,
           "gene": "ZNF843",
           "score": -0.21766,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18407,
           "gene": "ZW10",
           "score": -0.159709,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18326,
           "gene": "ZNF841",
           "score": -0.245215,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18305,
           "gene": "ZNF804A",
           "score": 0.1808675,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18361,
           "gene": "ZNRF1",
           "score": -0.1483935,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18349,
           "gene": "ZNF99",
           "score": 0.355344,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18375,
           "gene": "ZRANB3",
           "score": -0.1117185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18302,
           "gene": "ZNF8",
           "score": 0.1183505,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18322,
           "gene": "ZNF836",
           "score": -0.160919,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18339,
           "gene": "ZNF878",
           "score": 0.117919,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18318,
           "gene": "ZNF83",
           "score": -0.2179175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18351,
           "gene": "ZNG1A",
           "score": 0.0520335,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18290,
           "gene": "ZNF783",
           "score": 0.0189365,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18382,
           "gene": "ZSCAN2",
           "score": 0.174456,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18380,
           "gene": "ZSCAN16",
           "score": 0.02777,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18396,
           "gene": "ZSCAN9",
           "score": -0.176105,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18337,
           "gene": "ZNF865",
           "score": 0.19303416,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18298,
           "gene": "ZNF791",
           "score": 0.0412261,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18317,
           "gene": "ZNF829",
           "score": -0.09893,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18343,
           "gene": "ZNF891",
           "score": 0.0954565,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18411,
           "gene": "ZXDB",
           "score": -0.02779,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18409,
           "gene": "ZWINT",
           "score": -0.123792,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18293,
           "gene": "ZNF786",
           "score": 0.1072135,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18394,
           "gene": "ZSCAN5A",
           "score": 0.34555,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18309,
           "gene": "ZNF808",
           "score": -0.113385,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18383,
           "gene": "ZSCAN20",
           "score": -0.3234765,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18353,
           "gene": "ZNG1C",
           "score": -0.1444645,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18303,
           "gene": "ZNF80",
           "score": 0.06814,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18368,
           "gene": "ZP4",
           "score": 0.06677535,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18401,
           "gene": "ZSWIM5",
           "score": -0.090245,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18304,
           "gene": "ZNF800",
           "score": -0.21139,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18307,
           "gene": "ZNF805",
           "score": 0.003305,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18397,
           "gene": "ZSWIM1",
           "score": 0.1066745,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18301,
           "gene": "ZNF799",
           "score": -0.077053,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18398,
           "gene": "ZSWIM2",
           "score": 0.08891,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18369,
           "gene": "ZPBP",
           "score": -0.208236,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18402,
           "gene": "ZSWIM6",
           "score": -0.132565,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18404,
           "gene": "ZSWIM8",
           "score": -0.034683,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18410,
           "gene": "ZXDA",
           "score": -0.044888,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18395,
           "gene": "ZSCAN5B",
           "score": -0.043905,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18367,
           "gene": "ZP3",
           "score": 0.179865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18308,
           "gene": "ZNF806",
           "score": 0.2282205,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18321,
           "gene": "ZNF835",
           "score": 0.1356605,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18347,
           "gene": "ZNF93",
           "score": -0.0982335,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18338,
           "gene": "ZNF875",
           "score": -0.214485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18297,
           "gene": "ZNF790",
           "score": -0.144395,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18344,
           "gene": "ZNF90",
           "score": 4.8e-05,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18362,
           "gene": "ZNRF2",
           "score": 0.058075,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18352,
           "gene": "ZNG1B",
           "score": -0.2631505,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18415,
           "gene": "ZYX",
           "score": 0.222654,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18340,
           "gene": "ZNF879",
           "score": 0.2543,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18354,
           "gene": "ZNG1E",
           "score": -0.091448,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18341,
           "gene": "ZNF880",
           "score": 0.0219,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18359,
           "gene": "ZNHIT6",
           "score": 0.341157,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18405,
           "gene": "ZSWIM9",
           "score": -0.25744,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18316,
           "gene": "ZNF827",
           "score": 0.2394125,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18292,
           "gene": "ZNF785",
           "score": -0.2707485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18332,
           "gene": "ZNF850",
           "score": 0.135435,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18370,
           "gene": "ZPBP2",
           "score": -0.0285285,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18358,
           "gene": "ZNHIT3",
           "score": -0.1181735,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18295,
           "gene": "ZNF789",
           "score": -0.105075,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18399,
           "gene": "ZSWIM3",
           "score": -0.242955,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18320,
           "gene": "ZNF831",
           "score": 0.0346266,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18328,
           "gene": "ZNF844",
           "score": -0.114665,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18381,
           "gene": "ZSCAN18",
           "score": -0.49931,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18408,
           "gene": "ZWILCH",
           "score": -0.146465,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 18196,
+          "gene": "ZNF655",
+          "score": -0.1833125,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18233,
+          "gene": "ZNF703",
+          "score": -0.0852,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18197,
+          "gene": "ZNF658",
+          "score": 0.044175,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18165,
+          "gene": "ZNF608",
+          "score": 0.2987305,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18173,
+          "gene": "ZNF618",
+          "score": -0.190475,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18162,
+          "gene": "ZNF605",
+          "score": -0.13111839,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18215,
+          "gene": "ZNF681",
+          "score": 0.128045,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18278,
+          "gene": "ZNF771",
+          "score": -0.149708,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18219,
+          "gene": "ZNF687",
+          "score": -0.262595,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18216,
+          "gene": "ZNF682",
+          "score": -0.199155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18166,
+          "gene": "ZNF609",
+          "score": -0.32101,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18163,
+          "gene": "ZNF606",
+          "score": 0.069635,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18257,
+          "gene": "ZNF730",
+          "score": -0.06505,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18221,
+          "gene": "ZNF689",
+          "score": -0.02664,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18192,
+          "gene": "ZNF649",
+          "score": -0.091537,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18230,
+          "gene": "ZNF70",
+          "score": -0.0901975,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18206,
+          "gene": "ZNF671",
+          "score": 0.09395745,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18164,
+          "gene": "ZNF607",
+          "score": -0.0026525,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18222,
+          "gene": "ZNF69",
+          "score": -0.1912095,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18232,
+          "gene": "ZNF701",
+          "score": -0.391055,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18274,
+          "gene": "ZNF766",
+          "score": 0.07028355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18262,
+          "gene": "ZNF74",
+          "score": -0.443155,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18218,
+          "gene": "ZNF684",
+          "score": 0.113969,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18212,
+          "gene": "ZNF678",
+          "score": 0.1374395,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18205,
+          "gene": "ZNF670",
+          "score": 0.289355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18176,
+          "gene": "ZNF621",
+          "score": 0.086152,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18236,
+          "gene": "ZNF705B",
+          "score": -0.059855,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18270,
+          "gene": "ZNF76",
+          "score": 0.013145,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18175,
+          "gene": "ZNF620",
+          "score": -0.16560645,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18263,
+          "gene": "ZNF740",
+          "score": 0.1171905,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18172,
+          "gene": "ZNF616",
+          "score": 0.106625,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18268,
+          "gene": "ZNF75A",
+          "score": 0.2089455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18266,
+          "gene": "ZNF749",
+          "score": 0.027157,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18282,
+          "gene": "ZNF775",
+          "score": -0.446395,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18264,
+          "gene": "ZNF746",
+          "score": 0.39508,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18211,
+          "gene": "ZNF677",
+          "score": -0.044635,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18195,
+          "gene": "ZNF654",
+          "score": -0.09401,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18237,
+          "gene": "ZNF705D",
+          "score": -0.2711,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18271,
+          "gene": "ZNF761",
+          "score": -0.29709,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18225,
+          "gene": "ZNF695",
+          "score": -0.0494725,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18254,
+          "gene": "ZNF727",
+          "score": -0.08205,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18188,
+          "gene": "ZNF641",
+          "score": -0.1801195,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18182,
+          "gene": "ZNF627",
+          "score": 0.006615,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18227,
+          "gene": "ZNF697",
+          "score": 0.33112,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18243,
+          "gene": "ZNF709",
+          "score": 0.0628615,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18226,
+          "gene": "ZNF696",
+          "score": -0.005585,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18289,
+          "gene": "ZNF782",
+          "score": -0.07841,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18279,
+          "gene": "ZNF772",
+          "score": -0.227325,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18272,
+          "gene": "ZNF764",
+          "score": 0.14892,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18287,
+          "gene": "ZNF780B",
+          "score": -0.15895,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18235,
+          "gene": "ZNF705A",
+          "score": 0.0939665,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18250,
+          "gene": "ZNF717",
+          "score": 0.251,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18168,
+          "gene": "ZNF611",
+          "score": 0.28251,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18194,
+          "gene": "ZNF653",
+          "score": -0.146895,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18199,
+          "gene": "ZNF662",
+          "score": -0.1954055,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18239,
+          "gene": "ZNF705G",
+          "score": 0.05468,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18260,
+          "gene": "ZNF736",
+          "score": -0.014509,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18259,
+          "gene": "ZNF735",
+          "score": 0.02091,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18198,
+          "gene": "ZNF660",
+          "score": -0.12729,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18193,
+          "gene": "ZNF652",
+          "score": 0.1074805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18203,
+          "gene": "ZNF668",
+          "score": 0.0942455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18187,
+          "gene": "ZNF639",
+          "score": -0.478455,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18207,
+          "gene": "ZNF672",
+          "score": 0.091869,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18231,
+          "gene": "ZNF700",
+          "score": 0.070234,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18213,
+          "gene": "ZNF679",
+          "score": -0.029394,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18242,
+          "gene": "ZNF708",
+          "score": 0.0181625,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18247,
+          "gene": "ZNF713",
+          "score": 0.15265,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18184,
+          "gene": "ZNF629",
+          "score": 0.3354,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18234,
+          "gene": "ZNF704",
+          "score": -0.093379,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18284,
+          "gene": "ZNF777",
+          "score": 0.1705515,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18283,
+          "gene": "ZNF776",
+          "score": -0.00751,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18258,
+          "gene": "ZNF732",
+          "score": 0.1017415,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18256,
+          "gene": "ZNF729",
+          "score": 0.012581,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18273,
+          "gene": "ZNF765",
+          "score": -0.389585,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18189,
+          "gene": "ZNF644",
+          "score": 0.280492,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18265,
+          "gene": "ZNF747",
+          "score": -0.00157,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18229,
+          "gene": "ZNF7",
+          "score": -0.0977735,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18228,
+          "gene": "ZNF699",
+          "score": -0.1837,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18202,
+          "gene": "ZNF667",
+          "score": 0.03447775,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18240,
+          "gene": "ZNF706",
+          "score": -0.02961,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18245,
+          "gene": "ZNF710",
+          "score": 0.09547,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18285,
+          "gene": "ZNF778",
+          "score": 0.1257655,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18171,
+          "gene": "ZNF615",
+          "score": 0.1941805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18209,
+          "gene": "ZNF675",
+          "score": 0.31613,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18276,
+          "gene": "ZNF77",
+          "score": 0.158275,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18249,
+          "gene": "ZNF716",
+          "score": 0.006445,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18255,
+          "gene": "ZNF728",
+          "score": 0.1207145,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18177,
+          "gene": "ZNF622",
+          "score": 0.085554,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18186,
+          "gene": "ZNF638",
+          "score": -0.156016,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18281,
+          "gene": "ZNF774",
+          "score": 0.0492925,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18180,
+          "gene": "ZNF625",
+          "score": 0.2007245,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18174,
+          "gene": "ZNF619",
+          "score": 0.227995,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18178,
+          "gene": "ZNF623",
+          "score": -0.209705,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18210,
+          "gene": "ZNF676",
+          "score": -0.0869881,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18253,
+          "gene": "ZNF726",
+          "score": 0.00325,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18246,
+          "gene": "ZNF711",
+          "score": 0.1338245,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18280,
+          "gene": "ZNF773",
+          "score": 0.130544,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18244,
+          "gene": "ZNF71",
+          "score": -0.189513,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18248,
+          "gene": "ZNF714",
+          "score": 0.20327,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18204,
+          "gene": "ZNF669",
+          "score": 0.0332529,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18183,
+          "gene": "ZNF628",
+          "score": 0.02386,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18191,
+          "gene": "ZNF648",
+          "score": 0.239318,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18238,
+          "gene": "ZNF705E",
+          "score": -0.256575,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18214,
+          "gene": "ZNF680",
+          "score": -0.0800905,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18169,
+          "gene": "ZNF613",
+          "score": 0.04389,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18208,
+          "gene": "ZNF674",
+          "score": 0.011945,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18181,
+          "gene": "ZNF626",
+          "score": -0.145603,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18251,
+          "gene": "ZNF718",
+          "score": -0.0575795,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18201,
+          "gene": "ZNF665",
+          "score": -0.03955195,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18224,
+          "gene": "ZNF692",
+          "score": 0.29731,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18190,
+          "gene": "ZNF646",
+          "score": 0.1066445,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18269,
+          "gene": "ZNF75D",
+          "score": 0.1355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18277,
+          "gene": "ZNF770",
+          "score": -0.0537535,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18288,
+          "gene": "ZNF781",
+          "score": -0.31094,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18217,
+          "gene": "ZNF683",
+          "score": 0.0220375,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18167,
+          "gene": "ZNF610",
+          "score": 0.12294,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18170,
+          "gene": "ZNF614",
+          "score": -0.05491,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18286,
+          "gene": "ZNF780A",
+          "score": 0.1124055,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18252,
+          "gene": "ZNF721",
+          "score": 0.26879,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18261,
+          "gene": "ZNF737",
+          "score": 0.216225,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18241,
+          "gene": "ZNF707",
+          "score": 0.37715,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18267,
+          "gene": "ZNF750",
+          "score": 0.031711,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18275,
+          "gene": "ZNF768",
+          "score": 0.01482,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18179,
+          "gene": "ZNF624",
+          "score": -0.127621,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18200,
+          "gene": "ZNF664",
+          "score": 0.0808805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18220,
+          "gene": "ZNF688",
+          "score": -0.0863065,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18223,
+          "gene": "ZNF691",
+          "score": -0.1299145,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18185,
+          "gene": "ZNF630",
+          "score": 0.08269,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
