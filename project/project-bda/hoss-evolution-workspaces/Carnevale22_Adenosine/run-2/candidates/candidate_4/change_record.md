# Change Record — candidate_4

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Carnevale22_Adenosine/run-2/best/current/harness
Generated at: 2026-04-30T07:16:35.037721

## Files Changed

- model.py: modified (added=34, deleted=3, delta=31)
- outputs/metrics.json: modified (added=2379, deleted=587, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -65,11 +65,37 @@
     # Calculate mean scores
     mean_scores = {idx: scores[idx] / counts[idx] for idx in scores}
     
-    # UCB algorithm: balance mean reward vs exploration bonus
+    # Calculate gene family bonuses based on historical extreme effects
+    # Genes from families with high absolute scores get a bonus
+    family_scores = {}
+    family_counts = {}
+    
+    for idx, score in mean_scores.items():
+        gene_name = candidates[idx].get('gene', '')
+        # Extract gene family prefix (e.g., "ZNF" from "ZNF123", "ATP" from "ATP6V0D1")
+        family = gene_name.split('_')[0]  # Handle cases like "ZNF816-ZNF321P"
+        # Take first part before any hyphen
+        family = family.split('-')[0]
+        
+        if family not in family_scores:
+            family_scores[family] = 0.0
+            family_counts[family] = 0
+        family_scores[family] += abs(score)
+        family_counts[family] += 1
+    
+    # Calculate average absolute score per family
+    family_avg_abs = {}
+    for family in family_scores:
+        family_avg_abs[family] = family_scores[family] / family_counts[family]
+    
+    # UCB algorithm: balance mean reward vs exploration bonus vs family bonus
     total_pulls = len(history)
     ucb_scores = []
     
     for idx in available_indices:
+        gene_name = candidates[idx].get('gene', '')
+        family = gene_name.split('_')[0].split('-')[0]
+        
         if idx in mean_scores:
             # Exploitation term: absolute mean score (prioritize extreme effects)
             # Since hits are defined by large deviations in either direction
@@ -78,10 +104,15 @@
             # Use a slightly higher exploration constant (2.5 vs 2.0) to encourage more exploration
             # Add small epsilon to prevent division by zero and handle low-count candidates
             exploration = np.sqrt(2.5 * np.log(total_pulls + 1) / (counts[idx] + 1e-6))
-            ucb = exploitation + exploration
+            # Family bonus: prioritize genes from families with historically extreme effects
+            # Weight: 0.3 * family_avg_abs (moderate influence, tuned empirically)
+            family_bonus = 0.3 * family_avg_abs.get(family, 0.0)
+            ucb = exploitation + exploration + family_bonus
         else:
             # Never-seen candidates get high priority for exploration
-            ucb = float('inf')
+            # But also consider family bonus for never-seen candidates
+            family_bonus = 0.3 * family_avg_abs.get(family, 0.0)
+            ucb = float('inf') + family_bonus
         ucb_scores.append((ucb, idx))
     
     # Sort by UCB score (descending) and select top candidates

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18861,
-      "rounds": 3,
+      "rounds": 4,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 256,
-      "baseline_total_hits": 15,
+      "baseline_total_queries": 384,
+      "baseline_total_hits": 23,
       "delta_queries": 128,
-      "delta_hits": 8,
-      "total_queries": 384,
-      "total_hits": 23,
+      "delta_hits": 11,
+      "total_queries": 512,
+      "total_hits": 34,
       "top_k": 943,
       "hit_curve": {
         "queries": [
-          256,
-          384
+          384,
+          512
         ],
         "hits": [
-          15,
-          23
+          23,
+          34
         ]
       },
-      "auc": 2432.0,
-      "auc_normalized": 0.00671615411806292,
-      "ncg": 0.27770411319817906,
+      "auc": 3648.0,
+      "auc_normalized": 0.007555673382820784,
+      "ncg": 0.2941334834709887,
       "round_details": [
         {
-          "round": 2,
+          "round": 3,
           "selected_count": 128,
-          "hits": 8,
-          "cumulative_hits": 23,
-          "precision_at_batch": 0.0625,
+          "hits": 11,
+          "cumulative_hits": 34,
+          "precision_at_batch": 0.0859375,
           "selected": [
-            "ZNF784",
-            "ZNF783",
-            "ZNF782",
-            "ZNF781",
-            "ZNF780B",
-            "ZNF780A",
-            "ZNF778",
-            "ZNF777",
-            "ZNF776",
-            "ZNF775",
-            "ZNF774",
-            "ZNF773",
-            "ZNF772",
-            "ZNF771",
-            "ZNF770",
-            "ZNF77",
-            "ZNF768",
-            "ZNF766",
-            "ZNF765",
-            "ZNF764",
-            "ZNF763",
-            "ZNF761",
-            "ZNF76",
-            "ZNF75D",
-            "ZNF75A",
-            "ZNF750",
-            "ZNF749",
-            "ZNF747",
-            "ZNF746",
-            "ZNF740",
-            "ZNF74",
-            "ZNF737",
-            "ZNF736",
-            "ZNF735",
-            "ZNF732",
-            "ZNF730",
-            "ZNF729",
-            "ZNF728",
-            "ZNF727",
-            "ZNF726",
-            "ZNF721",
-            "ZNF718",
-            "ZNF717",
-            "ZNF716",
-            "ZNF714",
-            "ZNF713",
-            "ZNF711",
-            "ZNF710",
-            "ZNF71",
-            "ZNF709",
-            "ZNF708",
-            "ZNF707",
-            "ZNF706",
-            "ZNF705G",
-            "ZNF705E",
-            "ZNF705D",
-            "ZNF705B",
-            "ZNF705A",
-            "ZNF704",
-            "ZNF703",
-            "ZNF701",
-            "ZNF700",
-            "ZNF70",
-            "ZNF7",
-            "ZNF699",
-            "ZNF697",
-            "ZNF696",
-            "ZNF695",
-            "ZNF692",
-            "ZNF691",
-            "ZNF69",
-            "ZNF689",
-            "ZNF688",
-            "ZNF687",
-            "ZNF684",
-            "ZNF683",
-            "ZNF682",
-            "ZNF681",
-            "ZNF680",
-            "ZNF679",
-            "ZNF678",
-            "ZNF677",
-            "ZNF676",
-            "ZNF675",
-            "ZNF674",
-            "ZNF672",
-            "ZNF671",
-            "ZNF670",
-            "ZNF669",
-            "ZNF668",
-            "ZNF667",
-            "ZNF665",
-            "ZNF664-FAM101A",
-            "ZNF664",
-            "ZNF662",
-            "ZNF660",
-            "ZNF658",
-            "ZNF655",
-            "ZNF654",
-            "ZNF653",
-            "ZNF652",
-            "ZNF649",
-            "ZNF648",
-            "ZNF646",
-            "ZNF644",
-            "ZNF641",
-            "ZNF639",
-            "ZNF638",
-            "ZNF630",
-            "ZNF629",
-            "ZNF628",
-            "ZNF627",
-            "ZNF626",
-            "ZNF625",
-            "ZNF624",
-            "ZNF623",
-            "ZNF622",
-            "ZNF621",
-            "ZNF620",
-            "ZNF619",
-            "ZNF618",
-            "ZNF616",
-            "ZNF615",
-            "ZNF614",
-            "ZNF613",
-            "ZNF611",
-            "ZNF610",
-            "ZNF609"
+            "ZNF608",
+            "ZNF607",
+            "ZNF606",
+            "ZNF605",
+            "ZNF600",
+            "ZNF599",
+            "ZNF598",
+            "ZNF597",
+            "ZNF596",
+            "ZNF595",
+            "ZNF594",
+            "ZNF593",
+            "ZNF592",
+            "ZNF589",
+            "ZNF587B",
+            "ZNF587",
+            "ZNF586",
+            "ZNF585B",
+            "ZNF585A",
+            "ZNF584",
+            "ZNF583",
+            "ZNF582",
+            "ZNF581",
+            "ZNF580",
+            "ZNF579",
+            "ZNF578",
+            "ZNF577",
+            "ZNF576",
+            "ZNF575",
+            "ZNF574",
+            "ZNF573",
+            "ZNF572",
+            "ZNF571",
+            "ZNF570",
+            "ZNF57",
+            "ZNF569",
+            "ZNF568",
+            "ZNF567",
+            "ZNF566",
+            "ZNF565",
+            "ZNF564",
+            "ZNF563",
+            "ZNF562",
+            "ZNF561",
+            "ZNF560",
+            "ZNF559-ZNF177",
+            "ZNF559",
+            "ZNF558",
+            "ZNF557",
+            "ZNF556",
+            "ZNF555",
+            "ZNF554",
+            "ZNF552",
+            "ZNF551",
+            "ZNF550",
+            "ZNF549",
+            "ZNF548",
+            "ZNF547",
+            "ZNF546",
+            "ZNF544",
+            "ZNF543",
+            "ZNF541",
+            "ZNF540",
+            "ZNF536",
+            "ZNF534",
+            "ZNF532",
+            "ZNF530",
+            "ZNF529",
+            "ZNF528",
+            "ZNF527",
+            "ZNF526",
+            "ZNF524",
+            "ZNF521",
+            "ZNF519",
+            "ZNF518B",
+            "ZNF518A",
+            "ZNF517",
+            "ZNF516",
+            "ZNF514",
+            "ZNF513",
+            "ZNF512B",
+            "ZNF512",
+            "ZNF511",
+            "ZNF510",
+            "ZNF507",
+            "ZNF506",
+            "ZNF503",
+            "ZNF502",
+            "ZNF501",
+            "ZNF500",
+            "ZNF497",
+            "ZNF496",
+            "ZNF493",
+            "ZNF492",
+            "ZNF491",
+            "ZNF490",
+            "ZNF488",
+            "ZNF486",
+            "ZNF485",
+            "ZNF484",
+            "ZNF483",
+            "ZNF480",
+            "ZNF48",
+            "ZNF479",
+            "ZNF473",
+            "ZNF471",
+            "ZNF470",
+            "ZNF469",
+            "ZNF468",
+            "ZNF467",
+            "ZNF462",
+            "ZNF461",
+            "ZNF460",
+            "ZNF454",
+            "ZNF451",
+            "ZNF45",
+            "ZNF449",
+            "ZNF446",
+            "ZNF445",
+            "ZNF444",
+            "ZNF443",
+            "ZNF442",
+            "ZNF441",
+            "ZNF440",
+            "ZNF44",
+            "ZNF439",
+            "ZNF438",
+            "ZNF436"
           ],
           "selected_scores": [
-            0.064117,
-            0.0060596,
-            0.031375,
-            0.061165,
-            0.10489,
-            0.046046,
-            0.12097,
-            0.15411,
-            -0.13952,
-            0.089403,
-            0.038457,
-            -0.15373,
-            0.2649,
-            -0.10739,
-            -0.077469,
-            0.14069,
-            -0.07904,
-            0.061603,
-            -0.083175,
-            0.29378,
-            -0.23285,
-            0.014376,
-            -0.61045,
-            0.26196,
-            -0.00086138,
-            0.063188,
-            0.08545,
-            -0.015003,
-            0.067608,
-            0.24155,
-            0.31314,
-            -0.090301,
-            -0.19433,
-            0.018026,
-            -0.067965,
-            0.087429,
-            -0.075084,
-            0.085004,
-            0.056405,
-            0.062063,
-            0.024887,
-            -0.14311,
-            -0.15785,
-            -0.27842,
-            0.15933,
-            -0.38127,
-            -0.20572,
-            -0.12781,
-            0.034771,
-            -0.17863,
-            0.33228,
-            0.24123,
-            -0.036214,
-            -0.045052,
-            -0.010156,
-            -0.17766,
-            0.13595,
-            -0.21217,
-            0.028186,
-            0.20221,
-            0.14396,
-            0.069497,
-            -0.051416,
-            -0.068836,
-            0.12067,
-            -0.39033,
-            0.15799,
-            -0.14239,
-            0.06298,
-            -0.089318,
-            -0.23795,
-            0.22088,
-            -0.058283,
-            -0.065126,
-            -0.12392,
-            0.12441,
-            -0.076369,
-            -0.1074,
-            0.11484,
-            -0.016099,
-            0.019563,
-            0.047365,
-            0.20676,
-            0.20089,
-            0.09181,
-            -0.010674,
-            0.3623,
-            0.021153,
-            0.001308,
-            0.33079,
-            0.083943,
-            -0.10005,
-            -0.16124,
-            -0.14921,
-            0.16768,
-            0.34349,
-            -0.11501,
-            0.34436,
-            -0.065974,
-            -0.052086,
-            -0.073012,
-            0.23818,
-            0.12368,
-            0.14022,
-            -0.056298,
-            0.27094,
-            0.10462,
-            -0.20538,
-            0.041454,
-            -0.0084088,
-            0.042279,
-            0.092429,
-            -0.17748,
-            -0.056479,
-            -0.23871,
-            0.10487,
-            0.053701,
-            0.11706,
-            0.16024,
-            0.46215,
-            -0.16295,
-            0.11379,
-            -0.37046,
-            0.073856,
-            -0.13374,
-            -0.028518,
-            0.066008,
-            -0.032282
+            0.12688,
+            0.072299,
+            0.043496,
+            0.013934,
+            0.083798,
+            -0.26203,
+            0.15653,
+            -0.12037,
+            -0.19227,
+            0.073366,
+            0.37002,
+            0.031148,
+            -0.26199,
+            -0.47131,
+            -0.0036534,
+            -0.016915,
+            0.050891,
+            -0.10684,
+            0.11733,
+            -0.13782,
+            0.18765,
+            -0.015977,
+            -0.051373,
+            0.27375,
+            0.083199,
+            -0.28973,
+            -0.28492,
+            -0.10189,
+            0.29304,
+            0.082974,
+            0.01173,
+            0.1097,
+            -0.29187,
+            -0.048904,
+            0.054145,
+            -0.14599,
+            -0.084297,
+            0.1728,
+            0.11916,
+            0.046647,
+            0.043877,
+            -0.19572,
+            0.0037033,
+            -0.2972,
+            -0.1161,
+            -0.035171,
+            0.12576,
+            0.20418,
+            -0.41338,
+            0.12917,
+            -0.075628,
+            -0.047888,
+            0.2297,
+            -0.060688,
+            -0.025795,
+            -0.016808,
+            -0.049671,
+            0.10727,
+            -0.013879,
+            -0.012014,
+            0.12739,
+            -0.10405,
+            0.20023,
+            0.20535,
+            -0.0011927,
+            -0.065848,
+            -0.092644,
+            -0.28892,
+            0.070663,
+            -0.04451,
+            -0.23212,
+            -0.13637,
+            -0.15231,
+            -0.088078,
+            -0.036369,
+            -0.016586,
+            0.1061,
+            -0.15165,
+            0.15989,
+            -0.075366,
+            0.12756,
+            -0.13474,
+            0.31078,
+            -0.1862,
+            0.05839,
+            0.49766,
+            0.13902,
+            0.083177,
+            0.16282,
+            -0.040884,
+            0.0020353,
+            -0.42909,
+            -0.34255,
+            0.53004,
+            -0.20654,
+            0.30996,
+            0.30129,
+            -0.35845,
+            -0.074194,
+            -0.15525,
+            -0.064107,
+            0.079031,
+            0.040223,
+            -0.18857,
+            0.11782,
+            -0.10068,
+            0.13604,
+            -0.051998,
+            0.26556,
+            0.21092,
+            -0.23175,
+            -0.01324,
+            -0.11387,
+            0.15656,
+            0.1581,
+            0.18164,
+            0.0080712,
+            0.44891,
+            -0.21726,
+            0.10247,
+            0.017261,
+            0.35702,
+            -0.028326,
+            -0.045372,
+            0.051431,
+            -0.074874,
+            0.051488,
+            0.33876
           ],
           "selected_hits": [
             0,
@@ -311,41 +311,9 @@
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
             1,
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
             1,
             0,
             0,
@@ -366,6 +334,21 @@
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
             1,
             0,
             0,
@@ -387,48 +370,65 @@
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
             1,
             0,
             0,
             0,
             0,
             0,
-            0,
-            0,
-            0,
             1,
-            0,
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
             1,
             0,
             0,
+            0,
             1,
             0,
             0,
             0,
             0,
-            0
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
+            1,
+            0,
+            0,
+            0,
+            0,
+            0,
+            1
           ]
         }
       ],
@@ -2230,896 +2230,1792 @@
           "gene": "ZNF784",
           "score": 0.064117,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18731,
           "gene": "ZNF783",
           "score": 0.0060596,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18730,
           "gene": "ZNF782",
           "score": 0.031375,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18729,
           "gene": "ZNF781",
           "score": 0.061165,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18728,
           "gene": "ZNF780B",
           "score": 0.10489,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18727,
           "gene": "ZNF780A",
           "score": 0.046046,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18726,
           "gene": "ZNF778",
           "score": 0.12097,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18725,
           "gene": "ZNF777",
           "score": 0.15411,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18724,
           "gene": "ZNF776",
           "score": -0.13952,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18723,
           "gene": "ZNF775",
           "score": 0.089403,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18722,
           "gene": "ZNF774",
           "score": 0.038457,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18721,
           "gene": "ZNF773",
           "score": -0.15373,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18720,
           "gene": "ZNF772",
           "score": 0.2649,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18719,
           "gene": "ZNF771",
           "score": -0.10739,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18718,
           "gene": "ZNF770",
           "score": -0.077469,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18717,
           "gene": "ZNF77",
           "score": 0.14069,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18716,
           "gene": "ZNF768",
           "score": -0.07904,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18715,
           "gene": "ZNF766",
           "score": 0.061603,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18714,
           "gene": "ZNF765",
           "score": -0.083175,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18713,
           "gene": "ZNF764",
           "score": 0.29378,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18712,
           "gene": "ZNF763",
           "score": -0.23285,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18711,
           "gene": "ZNF761",
           "score": 0.014376,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18710,
           "gene": "ZNF76",
           "score": -0.61045,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18709,
           "gene": "ZNF75D",
           "score": 0.26196,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18708,
           "gene": "ZNF75A",
           "score": -0.00086138,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18707,
           "gene": "ZNF750",
           "score": 0.063188,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18706,
           "gene": "ZNF749",
           "score": 0.08545,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18705,
           "gene": "ZNF747",
           "score": -0.015003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18704,
           "gene": "ZNF746",
           "score": 0.067608,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18703,
           "gene": "ZNF740",
           "score": 0.24155,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18702,
           "gene": "ZNF74",
           "score": 0.31314,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18701,
           "gene": "ZNF737",
           "score": -0.090301,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18700,
           "gene": "ZNF736",
           "score": -0.19433,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18699,
           "gene": "ZNF735",
           "score": 0.018026,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18698,
           "gene": "ZNF732",
           "score": -0.067965,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18697,
           "gene": "ZNF730",
           "score": 0.087429,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18696,
           "gene": "ZNF729",
           "score": -0.075084,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18695,
           "gene": "ZNF728",
           "score": 0.085004,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18694,
           "gene": "ZNF727",
           "score": 0.056405,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18693,
           "gene": "ZNF726",
           "score": 0.062063,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18692,
           "gene": "ZNF721",
           "score": 0.024887,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18691,
           "gene": "ZNF718",
           "score": -0.14311,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18690,
           "gene": "ZNF717",
           "score": -0.15785,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18689,
           "gene": "ZNF716",
           "score": -0.27842,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18688,
           "gene": "ZNF714",
           "score": 0.15933,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18687,
           "gene": "ZNF713",
           "score": -0.38127,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18686,
           "gene": "ZNF711",
           "score": -0.20572,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18685,
           "gene": "ZNF710",
           "score": -0.12781,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18684,
           "gene": "ZNF71",
           "score": 0.034771,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18683,
           "gene": "ZNF709",
           "score": -0.17863,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18682,
           "gene": "ZNF708",
           "score": 0.33228,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18681,
           "gene": "ZNF707",
           "score": 0.24123,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18680,
           "gene": "ZNF706",
           "score": -0.036214,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18679,
           "gene": "ZNF705G",
           "score": -0.045052,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18678,
           "gene": "ZNF705E",
           "score": -0.010156,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18677,
           "gene": "ZNF705D",
           "score": -0.17766,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18676,
           "gene": "ZNF705B",
           "score": 0.13595,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18675,
           "gene": "ZNF705A",
           "score": -0.21217,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18674,
           "gene": "ZNF704",
           "score": 0.028186,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18673,
           "gene": "ZNF703",
           "score": 0.20221,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18672,
           "gene": "ZNF701",
           "score": 0.14396,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18671,
           "gene": "ZNF700",
           "score": 0.069497,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18670,
           "gene": "ZNF70",
           "score": -0.051416,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18669,
           "gene": "ZNF7",
           "score": -0.068836,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18668,
           "gene": "ZNF699",
           "score": 0.12067,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18667,
           "gene": "ZNF697",
           "score": -0.39033,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18666,
           "gene": "ZNF696",
           "score": 0.15799,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18665,
           "gene": "ZNF695",
           "score": -0.14239,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18664,
           "gene": "ZNF692",
           "score": 0.06298,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18663,
           "gene": "ZNF691",
           "score": -0.089318,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18662,
           "gene": "ZNF69",
           "score": -0.23795,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18661,
           "gene": "ZNF689",
           "score": 0.22088,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18660,
           "gene": "ZNF688",
           "score": -0.058283,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18659,
           "gene": "ZNF687",
           "score": -0.065126,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18658,
           "gene": "ZNF684",
           "score": -0.12392,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18657,
           "gene": "ZNF683",
           "score": 0.12441,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18656,
           "gene": "ZNF682",
           "score": -0.076369,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18655,
           "gene": "ZNF681",
           "score": -0.1074,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18654,
           "gene": "ZNF680",
           "score": 0.11484,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18653,
           "gene": "ZNF679",
           "score": -0.016099,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18652,
           "gene": "ZNF678",
           "score": 0.019563,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18651,
           "gene": "ZNF677",
           "score": 0.047365,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18650,
           "gene": "ZNF676",
           "score": 0.20676,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18649,
           "gene": "ZNF675",
           "score": 0.20089,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18648,
           "gene": "ZNF674",
           "score": 0.09181,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18647,
           "gene": "ZNF672",
           "score": -0.010674,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18646,
           "gene": "ZNF671",
           "score": 0.3623,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18645,
           "gene": "ZNF670",
           "score": 0.021153,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18644,
           "gene": "ZNF669",
           "score": 0.001308,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18643,
           "gene": "ZNF668",
           "score": 0.33079,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18642,
           "gene": "ZNF667",
           "score": 0.083943,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18641,
           "gene": "ZNF665",
           "score": -0.10005,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18640,
           "gene": "ZNF664-FAM101A",
           "score": -0.16124,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18639,
           "gene": "ZNF664",
           "score": -0.14921,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18638,
           "gene": "ZNF662",
           "score": 0.16768,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18637,
           "gene": "ZNF660",
           "score": 0.34349,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18636,
           "gene": "ZNF658",
           "score": -0.11501,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18635,
           "gene": "ZNF655",
           "score": 0.34436,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18634,
           "gene": "ZNF654",
           "score": -0.065974,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18633,
           "gene": "ZNF653",
           "score": -0.052086,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18632,
           "gene": "ZNF652",
           "score": -0.073012,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18631,
           "gene": "ZNF649",
           "score": 0.23818,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18630,
           "gene": "ZNF648",
           "score": 0.12368,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18629,
           "gene": "ZNF646",
           "score": 0.14022,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18628,
           "gene": "ZNF644",
           "score": -0.056298,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18627,
           "gene": "ZNF641",
           "score": 0.27094,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18626,
           "gene": "ZNF639",
           "score": 0.10462,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18625,
           "gene": "ZNF638",
           "score": -0.20538,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18624,
           "gene": "ZNF630",
           "score": 0.041454,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18623,
           "gene": "ZNF629",
           "score": -0.0084088,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18622,
           "gene": "ZNF628",
           "score": 0.042279,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18621,
           "gene": "ZNF627",
           "score": 0.092429,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18620,
           "gene": "ZNF626",
           "score": -0.17748,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18619,
           "gene": "ZNF625",
           "score": -0.056479,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18618,
           "gene": "ZNF624",
           "score": -0.23871,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18617,
           "gene": "ZNF623",
           "score": 0.10487,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18616,
           "gene": "ZNF622",
           "score": 0.053701,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18615,
           "gene": "ZNF621",
           "score": 0.11706,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18614,
           "gene": "ZNF620",
           "score": 0.16024,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18613,
           "gene": "ZNF619",
           "score": 0.46215,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18612,
           "gene": "ZNF618",
           "score": -0.16295,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18611,
           "gene": "ZNF616",
           "score": 0.11379,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18610,
           "gene": "ZNF615",
           "score": -0.37046,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18609,
           "gene": "ZNF614",
           "score": 0.073856,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18608,
           "gene": "ZNF613",
           "score": -0.13374,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18607,
           "gene": "ZNF611",
           "score": -0.028518,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18606,
           "gene": "ZNF610",
           "score": 0.066008,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18605,
           "gene": "ZNF609",
           "score": -0.032282,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 18604,
+          "gene": "ZNF608",
+          "score": 0.12688,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18603,
+          "gene": "ZNF607",
+          "score": 0.072299,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18602,
+          "gene": "ZNF606",
+          "score": 0.043496,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18601,
+          "gene": "ZNF605",
+          "score": 0.013934,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18600,
+          "gene": "ZNF600",
+          "score": 0.083798,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18599,
+          "gene": "ZNF599",
+          "score": -0.26203,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18598,
+          "gene": "ZNF598",
+          "score": 0.15653,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18597,
+          "gene": "ZNF597",
+          "score": -0.12037,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18596,
+          "gene": "ZNF596",
+          "score": -0.19227,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18595,
+          "gene": "ZNF595",
+          "score": 0.073366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18594,
+          "gene": "ZNF594",
+          "score": 0.37002,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18593,
+          "gene": "ZNF593",
+          "score": 0.031148,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18592,
+          "gene": "ZNF592",
+          "score": -0.26199,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18591,
+          "gene": "ZNF589",
+          "score": -0.47131,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18590,
+          "gene": "ZNF587B",
+          "score": -0.0036534,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18589,
+          "gene": "ZNF587",
+          "score": -0.016915,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18588,
+          "gene": "ZNF586",
+          "score": 0.050891,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18587,
+          "gene": "ZNF585B",
+          "score": -0.10684,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18586,
+          "gene": "ZNF585A",
+          "score": 0.11733,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18585,
+          "gene": "ZNF584",
+          "score": -0.13782,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18584,
+          "gene": "ZNF583",
+          "score": 0.18765,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18583,
+          "gene": "ZNF582",
+          "score": -0.015977,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18582,
+          "gene": "ZNF581",
+          "score": -0.051373,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18581,
+          "gene": "ZNF580",
+          "score": 0.27375,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18580,
+          "gene": "ZNF579",
+          "score": 0.083199,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18579,
+          "gene": "ZNF578",
+          "score": -0.28973,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18578,
+          "gene": "ZNF577",
+          "score": -0.28492,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18577,
+          "gene": "ZNF576",
+          "score": -0.10189,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18576,
+          "gene": "ZNF575",
+          "score": 0.29304,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18575,
+          "gene": "ZNF574",
+          "score": 0.082974,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18574,
+          "gene": "ZNF573",
+          "score": 0.01173,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18573,
+          "gene": "ZNF572",
+          "score": 0.1097,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18572,
+          "gene": "ZNF571",
+          "score": -0.29187,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18571,
+          "gene": "ZNF570",
+          "score": -0.048904,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18570,
+          "gene": "ZNF57",
+          "score": 0.054145,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18569,
+          "gene": "ZNF569",
+          "score": -0.14599,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18568,
+          "gene": "ZNF568",
+          "score": -0.084297,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18567,
+          "gene": "ZNF567",
+          "score": 0.1728,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18566,
+          "gene": "ZNF566",
+          "score": 0.11916,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18565,
+          "gene": "ZNF565",
+          "score": 0.046647,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18564,
+          "gene": "ZNF564",
+          "score": 0.043877,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18563,
+          "gene": "ZNF563",
+          "score": -0.19572,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18562,
+          "gene": "ZNF562",
+          "score": 0.0037033,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18561,
+          "gene": "ZNF561",
+          "score": -0.2972,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18560,
+          "gene": "ZNF560",
+          "score": -0.1161,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18559,
+          "gene": "ZNF559-ZNF177",
+          "score": -0.035171,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18558,
+          "gene": "ZNF559",
+          "score": 0.12576,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18557,
+          "gene": "ZNF558",
+          "score": 0.20418,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18556,
+          "gene": "ZNF557",
+          "score": -0.41338,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18555,
+          "gene": "ZNF556",
+          "score": 0.12917,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18554,
+          "gene": "ZNF555",
+          "score": -0.075628,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18553,
+          "gene": "ZNF554",
+          "score": -0.047888,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18552,
+          "gene": "ZNF552",
+          "score": 0.2297,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18551,
+          "gene": "ZNF551",
+          "score": -0.060688,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18550,
+          "gene": "ZNF550",
+          "score": -0.025795,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18549,
+          "gene": "ZNF549",
+          "score": -0.016808,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18548,
+          "gene": "ZNF548",
+          "score": -0.049671,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18547,
+          "gene": "ZNF547",
+          "score": 0.10727,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18546,
+          "gene": "ZNF546",
+          "score": -0.013879,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18545,
+          "gene": "ZNF544",
+          "score": -0.012014,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18544,
+          "gene": "ZNF543",
+          "score": 0.12739,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18543,
+          "gene": "ZNF541",
+          "score": -0.10405,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18542,
+          "gene": "ZNF540",
+          "score": 0.20023,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18541,
+          "gene": "ZNF536",
+          "score": 0.20535,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18540,
+          "gene": "ZNF534",
+          "score": -0.0011927,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18539,
+          "gene": "ZNF532",
+          "score": -0.065848,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18538,
+          "gene": "ZNF530",
+          "score": -0.092644,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18537,
+          "gene": "ZNF529",
+          "score": -0.28892,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18536,
+          "gene": "ZNF528",
+          "score": 0.070663,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18535,
+          "gene": "ZNF527",
+          "score": -0.04451,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18534,
+          "gene": "ZNF526",
+          "score": -0.23212,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18533,
+          "gene": "ZNF524",
+          "score": -0.13637,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18532,
+          "gene": "ZNF521",
+          "score": -0.15231,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18531,
+          "gene": "ZNF519",
+          "score": -0.088078,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18530,
+          "gene": "ZNF518B",
+          "score": -0.036369,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18529,
+          "gene": "ZNF518A",
+          "score": -0.016586,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18528,
+          "gene": "ZNF517",
+          "score": 0.1061,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18527,
+          "gene": "ZNF516",
+          "score": -0.15165,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18526,
+          "gene": "ZNF514",
+          "score": 0.15989,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18525,
+          "gene": "ZNF513",
+          "score": -0.075366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18524,
+          "gene": "ZNF512B",
+          "score": 0.12756,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18523,
+          "gene": "ZNF512",
+          "score": -0.13474,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18522,
+          "gene": "ZNF511",
+          "score": 0.31078,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18521,
+          "gene": "ZNF510",
+          "score": -0.1862,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18520,
+          "gene": "ZNF507",
+          "score": 0.05839,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18519,
+          "gene": "ZNF506",
+          "score": 0.49766,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18518,
+          "gene": "ZNF503",
+          "score": 0.13902,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18517,
+          "gene": "ZNF502",
+          "score": 0.083177,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18516,
+          "gene": "ZNF501",
+          "score": 0.16282,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18515,
+          "gene": "ZNF500",
+          "score": -0.040884,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18514,
+          "gene": "ZNF497",
+          "score": 0.0020353,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18513,
+          "gene": "ZNF496",
+          "score": -0.42909,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18512,
+          "gene": "ZNF493",
+          "score": -0.34255,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18511,
+          "gene": "ZNF492",
+          "score": 0.53004,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18510,
+          "gene": "ZNF491",
+          "score": -0.20654,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18509,
+          "gene": "ZNF490",
+          "score": 0.30996,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18508,
+          "gene": "ZNF488",
+          "score": 0.30129,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18507,
+          "gene": "ZNF486",
+          "score": -0.35845,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18506,
+          "gene": "ZNF485",
+          "score": -0.074194,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18505,
+          "gene": "ZNF484",
+          "score": -0.15525,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18504,
+          "gene": "ZNF483",
+          "score": -0.064107,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18503,
+          "gene": "ZNF480",
+          "score": 0.079031,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18502,
+          "gene": "ZNF48",
+          "score": 0.040223,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18501,
+          "gene": "ZNF479",
+          "score": -0.18857,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18500,
+          "gene": "ZNF473",
+          "score": 0.11782,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18499,
+          "gene": "ZNF471",
+          "score": -0.10068,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18498,
+          "gene": "ZNF470",
+          "score": 0.13604,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18497,
+          "gene": "ZNF469",
+          "score": -0.051998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18496,
+          "gene": "ZNF468",
+          "score": 0.26556,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18495,
+          "gene": "ZNF467",
+          "score": 0.21092,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18494,
+          "gene": "ZNF462",
+          "score": -0.23175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18493,
+          "gene": "ZNF461",
+          "score": -0.01324,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18492,
+          "gene": "ZNF460",
+          "score": -0.11387,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18491,
+          "gene": "ZNF454",
+          "score": 0.15656,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18490,
+          "gene": "ZNF451",
+          "score": 0.1581,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18489,
+          "gene": "ZNF45",
+          "score": 0.18164,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18488,
+          "gene": "ZNF449",
+          "score": 0.0080712,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18487,
+          "gene": "ZNF446",
+          "score": 0.44891,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18486,
+          "gene": "ZNF445",
+          "score": -0.21726,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18485,
+          "gene": "ZNF444",
+          "score": 0.10247,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18484,
+          "gene": "ZNF443",
+          "score": 0.017261,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18483,
+          "gene": "ZNF442",
+          "score": 0.35702,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18482,
+          "gene": "ZNF441",
+          "score": -0.028326,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18481,
+          "gene": "ZNF440",
+          "score": -0.045372,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18480,
+          "gene": "ZNF44",
+          "score": 0.051431,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18479,
+          "gene": "ZNF439",
+          "score": -0.074874,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18478,
+          "gene": "ZNF438",
+          "score": 0.051488,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18477,
+          "gene": "ZNF436",
+          "score": 0.33876,
+          "hit": 1,
+          "round": 3
         }
       ],
       "queried_history": [
@@ -4920,896 +5816,1792 @@
           "gene": "ZNF784",
           "score": 0.064117,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18731,
           "gene": "ZNF783",
           "score": 0.0060596,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18730,
           "gene": "ZNF782",
           "score": 0.031375,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18729,
           "gene": "ZNF781",
           "score": 0.061165,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18728,
           "gene": "ZNF780B",
           "score": 0.10489,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18727,
           "gene": "ZNF780A",
           "score": 0.046046,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18726,
           "gene": "ZNF778",
           "score": 0.12097,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18725,
           "gene": "ZNF777",
           "score": 0.15411,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18724,
           "gene": "ZNF776",
           "score": -0.13952,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18723,
           "gene": "ZNF775",
           "score": 0.089403,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18722,
           "gene": "ZNF774",
           "score": 0.038457,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18721,
           "gene": "ZNF773",
           "score": -0.15373,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18720,
           "gene": "ZNF772",
           "score": 0.2649,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18719,
           "gene": "ZNF771",
           "score": -0.10739,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18718,
           "gene": "ZNF770",
           "score": -0.077469,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18717,
           "gene": "ZNF77",
           "score": 0.14069,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18716,
           "gene": "ZNF768",
           "score": -0.07904,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18715,
           "gene": "ZNF766",
           "score": 0.061603,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18714,
           "gene": "ZNF765",
           "score": -0.083175,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18713,
           "gene": "ZNF764",
           "score": 0.29378,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18712,
           "gene": "ZNF763",
           "score": -0.23285,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18711,
           "gene": "ZNF761",
           "score": 0.014376,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18710,
           "gene": "ZNF76",
           "score": -0.61045,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18709,
           "gene": "ZNF75D",
           "score": 0.26196,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18708,
           "gene": "ZNF75A",
           "score": -0.00086138,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18707,
           "gene": "ZNF750",
           "score": 0.063188,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18706,
           "gene": "ZNF749",
           "score": 0.08545,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18705,
           "gene": "ZNF747",
           "score": -0.015003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18704,
           "gene": "ZNF746",
           "score": 0.067608,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18703,
           "gene": "ZNF740",
           "score": 0.24155,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18702,
           "gene": "ZNF74",
           "score": 0.31314,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18701,
           "gene": "ZNF737",
           "score": -0.090301,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18700,
           "gene": "ZNF736",
           "score": -0.19433,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18699,
           "gene": "ZNF735",
           "score": 0.018026,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18698,
           "gene": "ZNF732",
           "score": -0.067965,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18697,
           "gene": "ZNF730",
           "score": 0.087429,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18696,
           "gene": "ZNF729",
           "score": -0.075084,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18695,
           "gene": "ZNF728",
           "score": 0.085004,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18694,
           "gene": "ZNF727",
           "score": 0.056405,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18693,
           "gene": "ZNF726",
           "score": 0.062063,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18692,
           "gene": "ZNF721",
           "score": 0.024887,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18691,
           "gene": "ZNF718",
           "score": -0.14311,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18690,
           "gene": "ZNF717",
           "score": -0.15785,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18689,
           "gene": "ZNF716",
           "score": -0.27842,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18688,
           "gene": "ZNF714",
           "score": 0.15933,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18687,
           "gene": "ZNF713",
           "score": -0.38127,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18686,
           "gene": "ZNF711",
           "score": -0.20572,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18685,
           "gene": "ZNF710",
           "score": -0.12781,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18684,
           "gene": "ZNF71",
           "score": 0.034771,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18683,
           "gene": "ZNF709",
           "score": -0.17863,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18682,
           "gene": "ZNF708",
           "score": 0.33228,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18681,
           "gene": "ZNF707",
           "score": 0.24123,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18680,
           "gene": "ZNF706",
           "score": -0.036214,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18679,
           "gene": "ZNF705G",
           "score": -0.045052,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18678,
           "gene": "ZNF705E",
           "score": -0.010156,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18677,
           "gene": "ZNF705D",
           "score": -0.17766,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18676,
           "gene": "ZNF705B",
           "score": 0.13595,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18675,
           "gene": "ZNF705A",
           "score": -0.21217,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18674,
           "gene": "ZNF704",
           "score": 0.028186,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18673,
           "gene": "ZNF703",
           "score": 0.20221,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18672,
           "gene": "ZNF701",
           "score": 0.14396,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18671,
           "gene": "ZNF700",
           "score": 0.069497,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18670,
           "gene": "ZNF70",
           "score": -0.051416,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18669,
           "gene": "ZNF7",
           "score": -0.068836,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18668,
           "gene": "ZNF699",
           "score": 0.12067,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18667,
           "gene": "ZNF697",
           "score": -0.39033,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18666,
           "gene": "ZNF696",
           "score": 0.15799,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18665,
           "gene": "ZNF695",
           "score": -0.14239,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18664,
           "gene": "ZNF692",
           "score": 0.06298,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18663,
           "gene": "ZNF691",
           "score": -0.089318,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18662,
           "gene": "ZNF69",
           "score": -0.23795,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18661,
           "gene": "ZNF689",
           "score": 0.22088,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18660,
           "gene": "ZNF688",
           "score": -0.058283,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18659,
           "gene": "ZNF687",
           "score": -0.065126,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18658,
           "gene": "ZNF684",
           "score": -0.12392,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18657,
           "gene": "ZNF683",
           "score": 0.12441,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18656,
           "gene": "ZNF682",
           "score": -0.076369,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18655,
           "gene": "ZNF681",
           "score": -0.1074,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18654,
           "gene": "ZNF680",
           "score": 0.11484,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18653,
           "gene": "ZNF679",
           "score": -0.016099,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18652,
           "gene": "ZNF678",
           "score": 0.019563,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18651,
           "gene": "ZNF677",
           "score": 0.047365,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18650,
           "gene": "ZNF676",
           "score": 0.20676,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18649,
           "gene": "ZNF675",
           "score": 0.20089,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18648,
           "gene": "ZNF674",
           "score": 0.09181,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18647,
           "gene": "ZNF672",
           "score": -0.010674,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18646,
           "gene": "ZNF671",
           "score": 0.3623,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18645,
           "gene": "ZNF670",
           "score": 0.021153,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18644,
           "gene": "ZNF669",
           "score": 0.001308,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18643,
           "gene": "ZNF668",
           "score": 0.33079,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18642,
           "gene": "ZNF667",
           "score": 0.083943,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18641,
           "gene": "ZNF665",
           "score": -0.10005,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18640,
           "gene": "ZNF664-FAM101A",
           "score": -0.16124,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18639,
           "gene": "ZNF664",
           "score": -0.14921,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18638,
           "gene": "ZNF662",
           "score": 0.16768,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18637,
           "gene": "ZNF660",
           "score": 0.34349,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18636,
           "gene": "ZNF658",
           "score": -0.11501,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18635,
           "gene": "ZNF655",
           "score": 0.34436,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18634,
           "gene": "ZNF654",
           "score": -0.065974,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18633,
           "gene": "ZNF653",
           "score": -0.052086,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18632,
           "gene": "ZNF652",
           "score": -0.073012,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18631,
           "gene": "ZNF649",
           "score": 0.23818,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18630,
           "gene": "ZNF648",
           "score": 0.12368,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18629,
           "gene": "ZNF646",
           "score": 0.14022,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18628,
           "gene": "ZNF644",
           "score": -0.056298,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18627,
           "gene": "ZNF641",
           "score": 0.27094,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18626,
           "gene": "ZNF639",
           "score": 0.10462,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18625,
           "gene": "ZNF638",
           "score": -0.20538,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18624,
           "gene": "ZNF630",
           "score": 0.041454,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18623,
           "gene": "ZNF629",
           "score": -0.0084088,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18622,
           "gene": "ZNF628",
           "score": 0.042279,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18621,
           "gene": "ZNF627",
           "score": 0.092429,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18620,
           "gene": "ZNF626",
           "score": -0.17748,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18619,
           "gene": "ZNF625",
           "score": -0.056479,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18618,
           "gene": "ZNF624",
           "score": -0.23871,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18617,
           "gene": "ZNF623",
           "score": 0.10487,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18616,
           "gene": "ZNF622",
           "score": 0.053701,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18615,
           "gene": "ZNF621",
           "score": 0.11706,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18614,
           "gene": "ZNF620",
           "score": 0.16024,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18613,
           "gene": "ZNF619",
           "score": 0.46215,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18612,
           "gene": "ZNF618",
           "score": -0.16295,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18611,
           "gene": "ZNF616",
           "score": 0.11379,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18610,
           "gene": "ZNF615",
           "score": -0.37046,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18609,
           "gene": "ZNF614",
           "score": 0.073856,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18608,
           "gene": "ZNF613",
           "score": -0.13374,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18607,
           "gene": "ZNF611",
           "score": -0.028518,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18606,
           "gene": "ZNF610",
           "score": 0.066008,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18605,
           "gene": "ZNF609",
           "score": -0.032282,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 18604,
+          "gene": "ZNF608",
+          "score": 0.12688,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18603,
+          "gene": "ZNF607",
+          "score": 0.072299,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18602,
+          "gene": "ZNF606",
+          "score": 0.043496,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18601,
+          "gene": "ZNF605",
+          "score": 0.013934,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18600,
+          "gene": "ZNF600",
+          "score": 0.083798,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18599,
+          "gene": "ZNF599",
+          "score": -0.26203,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18598,
+          "gene": "ZNF598",
+          "score": 0.15653,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18597,
+          "gene": "ZNF597",
+          "score": -0.12037,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18596,
+          "gene": "ZNF596",
+          "score": -0.19227,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18595,
+          "gene": "ZNF595",
+          "score": 0.073366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18594,
+          "gene": "ZNF594",
+          "score": 0.37002,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18593,
+          "gene": "ZNF593",
+          "score": 0.031148,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18592,
+          "gene": "ZNF592",
+          "score": -0.26199,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18591,
+          "gene": "ZNF589",
+          "score": -0.47131,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18590,
+          "gene": "ZNF587B",
+          "score": -0.0036534,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18589,
+          "gene": "ZNF587",
+          "score": -0.016915,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18588,
+          "gene": "ZNF586",
+          "score": 0.050891,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18587,
+          "gene": "ZNF585B",
+          "score": -0.10684,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18586,
+          "gene": "ZNF585A",
+          "score": 0.11733,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18585,
+          "gene": "ZNF584",
+          "score": -0.13782,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18584,
+          "gene": "ZNF583",
+          "score": 0.18765,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18583,
+          "gene": "ZNF582",
+          "score": -0.015977,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18582,
+          "gene": "ZNF581",
+          "score": -0.051373,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18581,
+          "gene": "ZNF580",
+          "score": 0.27375,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18580,
+          "gene": "ZNF579",
+          "score": 0.083199,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18579,
+          "gene": "ZNF578",
+          "score": -0.28973,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18578,
+          "gene": "ZNF577",
+          "score": -0.28492,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18577,
+          "gene": "ZNF576",
+          "score": -0.10189,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18576,
+          "gene": "ZNF575",
+          "score": 0.29304,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18575,
+          "gene": "ZNF574",
+          "score": 0.082974,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18574,
+          "gene": "ZNF573",
+          "score": 0.01173,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18573,
+          "gene": "ZNF572",
+          "score": 0.1097,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18572,
+          "gene": "ZNF571",
+          "score": -0.29187,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18571,
+          "gene": "ZNF570",
+          "score": -0.048904,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18570,
+          "gene": "ZNF57",
+          "score": 0.054145,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18569,
+          "gene": "ZNF569",
+          "score": -0.14599,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18568,
+          "gene": "ZNF568",
+          "score": -0.084297,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18567,
+          "gene": "ZNF567",
+          "score": 0.1728,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18566,
+          "gene": "ZNF566",
+          "score": 0.11916,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18565,
+          "gene": "ZNF565",
+          "score": 0.046647,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18564,
+          "gene": "ZNF564",
+          "score": 0.043877,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18563,
+          "gene": "ZNF563",
+          "score": -0.19572,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18562,
+          "gene": "ZNF562",
+          "score": 0.0037033,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18561,
+          "gene": "ZNF561",
+          "score": -0.2972,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18560,
+          "gene": "ZNF560",
+          "score": -0.1161,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18559,
+          "gene": "ZNF559-ZNF177",
+          "score": -0.035171,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18558,
+          "gene": "ZNF559",
+          "score": 0.12576,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18557,
+          "gene": "ZNF558",
+          "score": 0.20418,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18556,
+          "gene": "ZNF557",
+          "score": -0.41338,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18555,
+          "gene": "ZNF556",
+          "score": 0.12917,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18554,
+          "gene": "ZNF555",
+          "score": -0.075628,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18553,
+          "gene": "ZNF554",
+          "score": -0.047888,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18552,
+          "gene": "ZNF552",
+          "score": 0.2297,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18551,
+          "gene": "ZNF551",
+          "score": -0.060688,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18550,
+          "gene": "ZNF550",
+          "score": -0.025795,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18549,
+          "gene": "ZNF549",
+          "score": -0.016808,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18548,
+          "gene": "ZNF548",
+          "score": -0.049671,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18547,
+          "gene": "ZNF547",
+          "score": 0.10727,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18546,
+          "gene": "ZNF546",
+          "score": -0.013879,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18545,
+          "gene": "ZNF544",
+          "score": -0.012014,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18544,
+          "gene": "ZNF543",
+          "score": 0.12739,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18543,
+          "gene": "ZNF541",
+          "score": -0.10405,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18542,
+          "gene": "ZNF540",
+          "score": 0.20023,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18541,
+          "gene": "ZNF536",
+          "score": 0.20535,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18540,
+          "gene": "ZNF534",
+          "score": -0.0011927,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18539,
+          "gene": "ZNF532",
+          "score": -0.065848,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18538,
+          "gene": "ZNF530",
+          "score": -0.092644,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18537,
+          "gene": "ZNF529",
+          "score": -0.28892,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18536,
+          "gene": "ZNF528",
+          "score": 0.070663,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18535,
+          "gene": "ZNF527",
+          "score": -0.04451,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18534,
+          "gene": "ZNF526",
+          "score": -0.23212,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18533,
+          "gene": "ZNF524",
+          "score": -0.13637,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18532,
+          "gene": "ZNF521",
+          "score": -0.15231,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18531,
+          "gene": "ZNF519",
+          "score": -0.088078,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18530,
+          "gene": "ZNF518B",
+          "score": -0.036369,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18529,
+          "gene": "ZNF518A",
+          "score": -0.016586,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18528,
+          "gene": "ZNF517",
+          "score": 0.1061,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18527,
+          "gene": "ZNF516",
+          "score": -0.15165,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18526,
+          "gene": "ZNF514",
+          "score": 0.15989,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18525,
+          "gene": "ZNF513",
+          "score": -0.075366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18524,
+          "gene": "ZNF512B",
+          "score": 0.12756,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18523,
+          "gene": "ZNF512",
+          "score": -0.13474,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18522,
+          "gene": "ZNF511",
+          "score": 0.31078,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18521,
+          "gene": "ZNF510",
+          "score": -0.1862,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18520,
+          "gene": "ZNF507",
+          "score": 0.05839,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18519,
+          "gene": "ZNF506",
+          "score": 0.49766,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18518,
+          "gene": "ZNF503",
+          "score": 0.13902,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18517,
+          "gene": "ZNF502",
+          "score": 0.083177,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18516,
+          "gene": "ZNF501",
+          "score": 0.16282,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18515,
+          "gene": "ZNF500",
+          "score": -0.040884,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18514,
+          "gene": "ZNF497",
+          "score": 0.0020353,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18513,
+          "gene": "ZNF496",
+          "score": -0.42909,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18512,
+          "gene": "ZNF493",
+          "score": -0.34255,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18511,
+          "gene": "ZNF492",
+          "score": 0.53004,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18510,
+          "gene": "ZNF491",
+          "score": -0.20654,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18509,
+          "gene": "ZNF490",
+          "score": 0.30996,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18508,
+          "gene": "ZNF488",
+          "score": 0.30129,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18507,
+          "gene": "ZNF486",
+          "score": -0.35845,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18506,
+          "gene": "ZNF485",
+          "score": -0.074194,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18505,
+          "gene": "ZNF484",
+          "score": -0.15525,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18504,
+          "gene": "ZNF483",
+          "score": -0.064107,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18503,
+          "gene": "ZNF480",
+          "score": 0.079031,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18502,
+          "gene": "ZNF48",
+          "score": 0.040223,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18501,
+          "gene": "ZNF479",
+          "score": -0.18857,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18500,
+          "gene": "ZNF473",
+          "score": 0.11782,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18499,
+          "gene": "ZNF471",
+          "score": -0.10068,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18498,
+          "gene": "ZNF470",
+          "score": 0.13604,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18497,
+          "gene": "ZNF469",
+          "score": -0.051998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18496,
+          "gene": "ZNF468",
+          "score": 0.26556,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18495,
+          "gene": "ZNF467",
+          "score": 0.21092,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18494,
+          "gene": "ZNF462",
+          "score": -0.23175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18493,
+          "gene": "ZNF461",
+          "score": -0.01324,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18492,
+          "gene": "ZNF460",
+          "score": -0.11387,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18491,
+          "gene": "ZNF454",
+          "score": 0.15656,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18490,
+          "gene": "ZNF451",
+          "score": 0.1581,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18489,
+          "gene": "ZNF45",
+          "score": 0.18164,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18488,
+          "gene": "ZNF449",
+          "score": 0.0080712,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18487,
+          "gene": "ZNF446",
+          "score": 0.44891,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18486,
+          "gene": "ZNF445",
+          "score": -0.21726,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18485,
+          "gene": "ZNF444",
+          "score": 0.10247,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18484,
+          "gene": "ZNF443",
+          "score": 0.017261,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18483,
+          "gene": "ZNF442",
+          "score": 0.35702,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18482,
+          "gene": "ZNF441",
+          "score": -0.028326,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18481,
+          "gene": "ZNF440",
+          "score": -0.045372,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18480,
+          "gene": "ZNF44",
+          "score": 0.051431,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18479,
+          "gene": "ZNF439",
+          "score": -0.074874,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18478,
+          "gene": "ZNF438",
+          "score": 0.051488,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18477,
+          "gene": "ZNF436",
+          "score": 0.33876,
+          "hit": 1,
+          "round": 3
         }
       ]
     }

```
