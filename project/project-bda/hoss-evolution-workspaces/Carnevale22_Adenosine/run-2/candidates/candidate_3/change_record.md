# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Carnevale22_Adenosine/run-2/best/current/harness
Generated at: 2026-04-30T07:15:27.570252

## Files Changed

- model.py: modified (added=4, deleted=2, delta=2)
- outputs/metrics.json: modified (added=2392, deleted=600, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -74,8 +74,10 @@
             # Exploitation term: absolute mean score (prioritize extreme effects)
             # Since hits are defined by large deviations in either direction
             exploitation = abs(mean_scores[idx])
-            # Exploration term: uncertainty bonus
-            exploration = np.sqrt(2 * np.log(total_pulls) / counts[idx])
+            # Exploration term: uncertainty bonus with tuned constant and epsilon regularization
+            # Use a slightly higher exploration constant (2.5 vs 2.0) to encourage more exploration
+            # Add small epsilon to prevent division by zero and handle low-count candidates
+            exploration = np.sqrt(2.5 * np.log(total_pulls + 1) / (counts[idx] + 1e-6))
             ucb = exploitation + exploration
         else:
             # Never-seen candidates get high priority for exploration

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18861,
-      "rounds": 2,
+      "rounds": 3,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 128,
-      "baseline_total_hits": 5,
+      "baseline_total_queries": 256,
+      "baseline_total_hits": 15,
       "delta_queries": 128,
-      "delta_hits": 10,
-      "total_queries": 256,
-      "total_hits": 15,
+      "delta_hits": 8,
+      "total_queries": 384,
+      "total_hits": 23,
       "top_k": 943,
       "hit_curve": {
         "queries": [
-          128,
-          256
+          256,
+          384
         ],
         "hits": [
-          5,
-          15
+          15,
+          23
         ]
       },
-      "auc": 1280.0,
-      "auc_normalized": 0.005302226935312832,
-      "ncg": 0.2674238651142878,
+      "auc": 2432.0,
+      "auc_normalized": 0.00671615411806292,
+      "ncg": 0.27770411319817906,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 10,
-          "cumulative_hits": 15,
-          "precision_at_batch": 0.078125,
+          "hits": 8,
+          "cumulative_hits": 23,
+          "precision_at_batch": 0.0625,
           "selected": [
-            "ZZZ3",
-            "ZZEF1",
-            "ZYX",
-            "ZYG11B",
-            "ZYG11A",
-            "ZXDC",
-            "ZXDB",
-            "ZXDA",
-            "ZWINT",
-            "ZWILCH",
-            "ZW10",
-            "ZUP1",
-            "ZSWIM9",
-            "ZSWIM8",
-            "ZSWIM7",
-            "ZSWIM6",
-            "ZSWIM5",
-            "ZSWIM4",
-            "ZSWIM3",
-            "ZSWIM2",
-            "ZSWIM1",
-            "ZSCAN9",
-            "ZSCAN5B",
-            "ZSCAN5A",
-            "ZSCAN4",
-            "ZSCAN32",
-            "ZSCAN31",
-            "ZSCAN30",
-            "ZSCAN29",
-            "ZSCAN26",
-            "ZSCAN25",
-            "ZSCAN23",
-            "ZSCAN22",
-            "ZSCAN21",
-            "ZSCAN20",
-            "ZSCAN2",
-            "ZSCAN18",
-            "ZSCAN16",
-            "ZSCAN12",
-            "ZSCAN10",
-            "ZSCAN1",
-            "ZRSR2",
-            "ZRANB3",
-            "ZRANB2",
-            "ZRANB1",
-            "ZPR1",
-            "ZPLD1",
-            "ZPBP2",
-            "ZPBP",
-            "ZP4",
-            "ZP3",
-            "ZP2",
-            "ZP1",
-            "ZNRF4",
-            "ZNRF3",
-            "ZNRF2",
-            "ZNRF1",
-            "ZNRD2",
-            "ZNHIT6",
-            "ZNHIT3",
-            "ZNHIT2",
-            "ZNHIT1",
-            "ZNG1F",
-            "ZNG1E",
-            "ZNG1C",
-            "ZNG1B",
-            "ZNG1A",
-            "ZNFX1",
-            "ZNF99",
-            "ZNF98",
-            "ZNF93",
-            "ZNF92",
-            "ZNF91",
-            "ZNF90",
-            "ZNF891",
-            "ZNF883",
-            "ZNF880",
-            "ZNF879",
-            "ZNF878",
-            "ZNF875",
-            "ZNF865",
-            "ZNF862",
-            "ZNF860",
-            "ZNF853",
-            "ZNF852",
-            "ZNF850",
-            "ZNF85",
-            "ZNF846",
-            "ZNF845",
-            "ZNF844",
-            "ZNF843",
-            "ZNF841",
-            "ZNF84",
-            "ZNF839",
-            "ZNF837",
-            "ZNF836",
-            "ZNF835",
-            "ZNF831",
-            "ZNF830",
-            "ZNF83",
-            "ZNF829",
-            "ZNF827",
-            "ZNF823",
-            "ZNF821",
-            "ZNF816-ZNF321P",
-            "ZNF816",
-            "ZNF814",
-            "ZNF813",
-            "ZNF812",
-            "ZNF81",
-            "ZNF808",
-            "ZNF806",
-            "ZNF805",
-            "ZNF804B",
-            "ZNF804A",
-            "ZNF800",
-            "ZNF80",
-            "ZNF8",
-            "ZNF799",
-            "ZNF793",
-            "ZNF792",
-            "ZNF791",
-            "ZNF790",
-            "ZNF79",
-            "ZNF789",
-            "ZNF787",
-            "ZNF786",
-            "ZNF785"
+            "ZNF784",
+            "ZNF783",
+            "ZNF782",
+            "ZNF781",
+            "ZNF780B",
+            "ZNF780A",
+            "ZNF778",
+            "ZNF777",
+            "ZNF776",
+            "ZNF775",
+            "ZNF774",
+            "ZNF773",
+            "ZNF772",
+            "ZNF771",
+            "ZNF770",
+            "ZNF77",
+            "ZNF768",
+            "ZNF766",
+            "ZNF765",
+            "ZNF764",
+            "ZNF763",
+            "ZNF761",
+            "ZNF76",
+            "ZNF75D",
+            "ZNF75A",
+            "ZNF750",
+            "ZNF749",
+            "ZNF747",
+            "ZNF746",
+            "ZNF740",
+            "ZNF74",
+            "ZNF737",
+            "ZNF736",
+            "ZNF735",
+            "ZNF732",
+            "ZNF730",
+            "ZNF729",
+            "ZNF728",
+            "ZNF727",
+            "ZNF726",
+            "ZNF721",
+            "ZNF718",
+            "ZNF717",
+            "ZNF716",
+            "ZNF714",
+            "ZNF713",
+            "ZNF711",
+            "ZNF710",
+            "ZNF71",
+            "ZNF709",
+            "ZNF708",
+            "ZNF707",
+            "ZNF706",
+            "ZNF705G",
+            "ZNF705E",
+            "ZNF705D",
+            "ZNF705B",
+            "ZNF705A",
+            "ZNF704",
+            "ZNF703",
+            "ZNF701",
+            "ZNF700",
+            "ZNF70",
+            "ZNF7",
+            "ZNF699",
+            "ZNF697",
+            "ZNF696",
+            "ZNF695",
+            "ZNF692",
+            "ZNF691",
+            "ZNF69",
+            "ZNF689",
+            "ZNF688",
+            "ZNF687",
+            "ZNF684",
+            "ZNF683",
+            "ZNF682",
+            "ZNF681",
+            "ZNF680",
+            "ZNF679",
+            "ZNF678",
+            "ZNF677",
+            "ZNF676",
+            "ZNF675",
+            "ZNF674",
+            "ZNF672",
+            "ZNF671",
+            "ZNF670",
+            "ZNF669",
+            "ZNF668",
+            "ZNF667",
+            "ZNF665",
+            "ZNF664-FAM101A",
+            "ZNF664",
+            "ZNF662",
+            "ZNF660",
+            "ZNF658",
+            "ZNF655",
+            "ZNF654",
+            "ZNF653",
+            "ZNF652",
+            "ZNF649",
+            "ZNF648",
+            "ZNF646",
+            "ZNF644",
+            "ZNF641",
+            "ZNF639",
+            "ZNF638",
+            "ZNF630",
+            "ZNF629",
+            "ZNF628",
+            "ZNF627",
+            "ZNF626",
+            "ZNF625",
+            "ZNF624",
+            "ZNF623",
+            "ZNF622",
+            "ZNF621",
+            "ZNF620",
+            "ZNF619",
+            "ZNF618",
+            "ZNF616",
+            "ZNF615",
+            "ZNF614",
+            "ZNF613",
+            "ZNF611",
+            "ZNF610",
+            "ZNF609"
           ],
           "selected_scores": [
-            0.0042296,
-            -0.025285,
-            -0.12133,
-            -0.17865,
-            -0.092959,
-            -0.34067,
-            0.23355,
-            0.046151,
-            0.2271,
-            -0.25147,
-            0.10344,
-            -0.18422,
-            -0.11507,
-            -0.30802,
-            0.0039042,
-            -0.10342,
-            0.12314,
-            -0.16708,
-            0.039048,
-            -0.052248,
-            0.29132,
-            -0.29343,
-            0.27484,
-            -0.18237,
-            0.11831,
-            0.051154,
-            -0.13807,
-            0.12307,
-            -0.19019,
-            0.25286,
-            0.048302,
-            0.22488,
-            -0.022625,
-            0.11542,
-            0.1752,
-            -0.066826,
-            -0.20931,
-            0.1603,
-            0.06866,
-            0.012773,
-            -0.29437,
-            -0.087505,
-            0.01562,
-            0.11397,
-            0.021138,
-            0.11386,
-            -0.36895,
-            0.1462,
-            -0.047664,
-            0.19443,
-            -0.11782,
-            0.20235,
-            -0.044293,
-            0.29151,
-            0.041693,
-            -0.089597,
-            0.12582,
-            0.26195,
-            -0.20291,
-            0.0056953,
-            -1.3601,
-            0.036511,
-            -0.038808,
-            0.14976,
-            0.37958,
-            -0.089569,
-            0.56598,
-            0.24159,
-            -0.27492,
-            -0.22855,
-            -0.15849,
-            -0.14714,
-            0.11351,
-            -0.040383,
-            0.21264,
-            0.14573,
-            0.19681,
-            -0.046847,
-            -0.064465,
-            0.25437,
-            -0.16523,
-            -0.20088,
-            0.12794,
-            -0.053904,
-            0.33108,
-            -0.01923,
-            -0.12341,
-            0.099597,
-            -0.013274,
-            0.26723,
-            0.0179,
-            4.0967e-06,
-            -0.042649,
-            0.13634,
-            -0.082197,
-            -0.044699,
-            0.22762,
-            0.30395,
-            -0.043654,
-            0.0444415,
-            -0.27861,
-            0.0040781,
-            0.3592,
-            0.34549,
-            0.011543,
-            -0.012604,
-            0.086018,
-            0.017173,
-            -0.050495,
-            -0.26963,
-            -0.021356,
-            0.33901,
-            0.052151,
-            -0.1854,
-            0.43123,
-            -0.0068465,
-            -0.058066,
-            0.10159,
-            -0.19427,
-            -0.0069571,
-            0.19458,
-            0.06026,
-            0.26988,
-            -0.013901,
-            -0.083043,
-            0.15997,
-            -0.074249,
-            0.57649
+            0.064117,
+            0.0060596,
+            0.031375,
+            0.061165,
+            0.10489,
+            0.046046,
+            0.12097,
+            0.15411,
+            -0.13952,
+            0.089403,
+            0.038457,
+            -0.15373,
+            0.2649,
+            -0.10739,
+            -0.077469,
+            0.14069,
+            -0.07904,
+            0.061603,
+            -0.083175,
+            0.29378,
+            -0.23285,
+            0.014376,
+            -0.61045,
+            0.26196,
+            -0.00086138,
+            0.063188,
+            0.08545,
+            -0.015003,
+            0.067608,
+            0.24155,
+            0.31314,
+            -0.090301,
+            -0.19433,
+            0.018026,
+            -0.067965,
+            0.087429,
+            -0.075084,
+            0.085004,
+            0.056405,
+            0.062063,
+            0.024887,
+            -0.14311,
+            -0.15785,
+            -0.27842,
+            0.15933,
+            -0.38127,
+            -0.20572,
+            -0.12781,
+            0.034771,
+            -0.17863,
+            0.33228,
+            0.24123,
+            -0.036214,
+            -0.045052,
+            -0.010156,
+            -0.17766,
+            0.13595,
+            -0.21217,
+            0.028186,
+            0.20221,
+            0.14396,
+            0.069497,
+            -0.051416,
+            -0.068836,
+            0.12067,
+            -0.39033,
+            0.15799,
+            -0.14239,
+            0.06298,
+            -0.089318,
+            -0.23795,
+            0.22088,
+            -0.058283,
+            -0.065126,
+            -0.12392,
+            0.12441,
+            -0.076369,
+            -0.1074,
+            0.11484,
+            -0.016099,
+            0.019563,
+            0.047365,
+            0.20676,
+            0.20089,
+            0.09181,
+            -0.010674,
+            0.3623,
+            0.021153,
+            0.001308,
+            0.33079,
+            0.083943,
+            -0.10005,
+            -0.16124,
+            -0.14921,
+            0.16768,
+            0.34349,
+            -0.11501,
+            0.34436,
+            -0.065974,
+            -0.052086,
+            -0.073012,
+            0.23818,
+            0.12368,
+            0.14022,
+            -0.056298,
+            0.27094,
+            0.10462,
+            -0.20538,
+            0.041454,
+            -0.0084088,
+            0.042279,
+            0.092429,
+            -0.17748,
+            -0.056479,
+            -0.23871,
+            0.10487,
+            0.053701,
+            0.11706,
+            0.16024,
+            0.46215,
+            -0.16295,
+            0.11379,
+            -0.37046,
+            0.073856,
+            -0.13374,
+            -0.028518,
+            0.066008,
+            -0.032282
           ],
           "selected_hits": [
             0,
@@ -306,6 +306,23 @@
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
             1,
             0,
             0,
@@ -329,24 +346,6 @@
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
             1,
             0,
             0,
@@ -361,74 +360,75 @@
             0,
             0,
             0,
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
-            0,
-            0,
-            0,
-            0,
-            0,
             1,
             0,
             0,
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
-            1
+            0,
+            0,
+            0
           ]
         }
       ],
@@ -1334,896 +1334,1792 @@
           "gene": "ZZZ3",
           "score": 0.0042296,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18859,
           "gene": "ZZEF1",
           "score": -0.025285,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18858,
           "gene": "ZYX",
           "score": -0.12133,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18857,
           "gene": "ZYG11B",
           "score": -0.17865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18856,
           "gene": "ZYG11A",
           "score": -0.092959,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18855,
           "gene": "ZXDC",
           "score": -0.34067,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18854,
           "gene": "ZXDB",
           "score": 0.23355,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18853,
           "gene": "ZXDA",
           "score": 0.046151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18852,
           "gene": "ZWINT",
           "score": 0.2271,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18851,
           "gene": "ZWILCH",
           "score": -0.25147,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18850,
           "gene": "ZW10",
           "score": 0.10344,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18849,
           "gene": "ZUP1",
           "score": -0.18422,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18848,
           "gene": "ZSWIM9",
           "score": -0.11507,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18847,
           "gene": "ZSWIM8",
           "score": -0.30802,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18846,
           "gene": "ZSWIM7",
           "score": 0.0039042,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18845,
           "gene": "ZSWIM6",
           "score": -0.10342,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18844,
           "gene": "ZSWIM5",
           "score": 0.12314,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18843,
           "gene": "ZSWIM4",
           "score": -0.16708,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18842,
           "gene": "ZSWIM3",
           "score": 0.039048,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18841,
           "gene": "ZSWIM2",
           "score": -0.052248,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18840,
           "gene": "ZSWIM1",
           "score": 0.29132,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18839,
           "gene": "ZSCAN9",
           "score": -0.29343,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18838,
           "gene": "ZSCAN5B",
           "score": 0.27484,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18837,
           "gene": "ZSCAN5A",
           "score": -0.18237,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18836,
           "gene": "ZSCAN4",
           "score": 0.11831,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18835,
           "gene": "ZSCAN32",
           "score": 0.051154,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18834,
           "gene": "ZSCAN31",
           "score": -0.13807,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18833,
           "gene": "ZSCAN30",
           "score": 0.12307,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18832,
           "gene": "ZSCAN29",
           "score": -0.19019,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18831,
           "gene": "ZSCAN26",
           "score": 0.25286,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18830,
           "gene": "ZSCAN25",
           "score": 0.048302,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18829,
           "gene": "ZSCAN23",
           "score": 0.22488,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18828,
           "gene": "ZSCAN22",
           "score": -0.022625,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18827,
           "gene": "ZSCAN21",
           "score": 0.11542,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18826,
           "gene": "ZSCAN20",
           "score": 0.1752,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18825,
           "gene": "ZSCAN2",
           "score": -0.066826,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18824,
           "gene": "ZSCAN18",
           "score": -0.20931,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18823,
           "gene": "ZSCAN16",
           "score": 0.1603,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18822,
           "gene": "ZSCAN12",
           "score": 0.06866,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18821,
           "gene": "ZSCAN10",
           "score": 0.012773,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18820,
           "gene": "ZSCAN1",
           "score": -0.29437,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18819,
           "gene": "ZRSR2",
           "score": -0.087505,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18818,
           "gene": "ZRANB3",
           "score": 0.01562,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18817,
           "gene": "ZRANB2",
           "score": 0.11397,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18816,
           "gene": "ZRANB1",
           "score": 0.021138,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18815,
           "gene": "ZPR1",
           "score": 0.11386,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18814,
           "gene": "ZPLD1",
           "score": -0.36895,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18813,
           "gene": "ZPBP2",
           "score": 0.1462,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18812,
           "gene": "ZPBP",
           "score": -0.047664,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18811,
           "gene": "ZP4",
           "score": 0.19443,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18810,
           "gene": "ZP3",
           "score": -0.11782,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18809,
           "gene": "ZP2",
           "score": 0.20235,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18808,
           "gene": "ZP1",
           "score": -0.044293,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18807,
           "gene": "ZNRF4",
           "score": 0.29151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18806,
           "gene": "ZNRF3",
           "score": 0.041693,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18805,
           "gene": "ZNRF2",
           "score": -0.089597,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18804,
           "gene": "ZNRF1",
           "score": 0.12582,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18803,
           "gene": "ZNRD2",
           "score": 0.26195,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18802,
           "gene": "ZNHIT6",
           "score": -0.20291,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18801,
           "gene": "ZNHIT3",
           "score": 0.0056953,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18800,
           "gene": "ZNHIT2",
           "score": -1.3601,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18799,
           "gene": "ZNHIT1",
           "score": 0.036511,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18798,
           "gene": "ZNG1F",
           "score": -0.038808,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18797,
           "gene": "ZNG1E",
           "score": 0.14976,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18796,
           "gene": "ZNG1C",
           "score": 0.37958,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18795,
           "gene": "ZNG1B",
           "score": -0.089569,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18794,
           "gene": "ZNG1A",
           "score": 0.56598,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18793,
           "gene": "ZNFX1",
           "score": 0.24159,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18792,
           "gene": "ZNF99",
           "score": -0.27492,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18791,
           "gene": "ZNF98",
           "score": -0.22855,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18790,
           "gene": "ZNF93",
           "score": -0.15849,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18789,
           "gene": "ZNF92",
           "score": -0.14714,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18788,
           "gene": "ZNF91",
           "score": 0.11351,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18787,
           "gene": "ZNF90",
           "score": -0.040383,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18786,
           "gene": "ZNF891",
           "score": 0.21264,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18785,
           "gene": "ZNF883",
           "score": 0.14573,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18784,
           "gene": "ZNF880",
           "score": 0.19681,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18783,
           "gene": "ZNF879",
           "score": -0.046847,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18782,
           "gene": "ZNF878",
           "score": -0.064465,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18781,
           "gene": "ZNF875",
           "score": 0.25437,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18780,
           "gene": "ZNF865",
           "score": -0.16523,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18779,
           "gene": "ZNF862",
           "score": -0.20088,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18778,
           "gene": "ZNF860",
           "score": 0.12794,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18777,
           "gene": "ZNF853",
           "score": -0.053904,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18776,
           "gene": "ZNF852",
           "score": 0.33108,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18775,
           "gene": "ZNF850",
           "score": -0.01923,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18774,
           "gene": "ZNF85",
           "score": -0.12341,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18773,
           "gene": "ZNF846",
           "score": 0.099597,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18772,
           "gene": "ZNF845",
           "score": -0.013274,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18771,
           "gene": "ZNF844",
           "score": 0.26723,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18770,
           "gene": "ZNF843",
           "score": 0.0179,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18769,
           "gene": "ZNF841",
           "score": 4.0967e-06,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18768,
           "gene": "ZNF84",
           "score": -0.042649,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18767,
           "gene": "ZNF839",
           "score": 0.13634,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18766,
           "gene": "ZNF837",
           "score": -0.082197,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18765,
           "gene": "ZNF836",
           "score": -0.044699,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18764,
           "gene": "ZNF835",
           "score": 0.22762,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18763,
           "gene": "ZNF831",
           "score": 0.30395,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18762,
           "gene": "ZNF830",
           "score": -0.043654,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18761,
           "gene": "ZNF83",
           "score": 0.0444415,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18760,
           "gene": "ZNF829",
           "score": -0.27861,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18759,
           "gene": "ZNF827",
           "score": 0.0040781,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18758,
           "gene": "ZNF823",
           "score": 0.3592,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18757,
           "gene": "ZNF821",
           "score": 0.34549,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18756,
           "gene": "ZNF816-ZNF321P",
           "score": 0.011543,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18755,
           "gene": "ZNF816",
           "score": -0.012604,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18754,
           "gene": "ZNF814",
           "score": 0.086018,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18753,
           "gene": "ZNF813",
           "score": 0.017173,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18752,
           "gene": "ZNF812",
           "score": -0.050495,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18751,
           "gene": "ZNF81",
           "score": -0.26963,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18750,
           "gene": "ZNF808",
           "score": -0.021356,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18749,
           "gene": "ZNF806",
           "score": 0.33901,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18748,
           "gene": "ZNF805",
           "score": 0.052151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18747,
           "gene": "ZNF804B",
           "score": -0.1854,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18746,
           "gene": "ZNF804A",
           "score": 0.43123,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18745,
           "gene": "ZNF800",
           "score": -0.0068465,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18744,
           "gene": "ZNF80",
           "score": -0.058066,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18743,
           "gene": "ZNF8",
           "score": 0.10159,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18742,
           "gene": "ZNF799",
           "score": -0.19427,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18741,
           "gene": "ZNF793",
           "score": -0.0069571,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18740,
           "gene": "ZNF792",
           "score": 0.19458,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18739,
           "gene": "ZNF791",
           "score": 0.06026,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18738,
           "gene": "ZNF790",
           "score": 0.26988,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18737,
           "gene": "ZNF79",
           "score": -0.013901,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18736,
           "gene": "ZNF789",
           "score": -0.083043,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18735,
           "gene": "ZNF787",
           "score": 0.15997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18734,
           "gene": "ZNF786",
           "score": -0.074249,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18733,
           "gene": "ZNF785",
           "score": 0.57649,
           "hit": 1,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 18732,
+          "gene": "ZNF784",
+          "score": 0.064117,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18731,
+          "gene": "ZNF783",
+          "score": 0.0060596,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18730,
+          "gene": "ZNF782",
+          "score": 0.031375,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18729,
+          "gene": "ZNF781",
+          "score": 0.061165,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18728,
+          "gene": "ZNF780B",
+          "score": 0.10489,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18727,
+          "gene": "ZNF780A",
+          "score": 0.046046,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18726,
+          "gene": "ZNF778",
+          "score": 0.12097,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18725,
+          "gene": "ZNF777",
+          "score": 0.15411,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18724,
+          "gene": "ZNF776",
+          "score": -0.13952,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18723,
+          "gene": "ZNF775",
+          "score": 0.089403,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18722,
+          "gene": "ZNF774",
+          "score": 0.038457,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18721,
+          "gene": "ZNF773",
+          "score": -0.15373,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18720,
+          "gene": "ZNF772",
+          "score": 0.2649,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18719,
+          "gene": "ZNF771",
+          "score": -0.10739,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18718,
+          "gene": "ZNF770",
+          "score": -0.077469,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18717,
+          "gene": "ZNF77",
+          "score": 0.14069,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18716,
+          "gene": "ZNF768",
+          "score": -0.07904,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18715,
+          "gene": "ZNF766",
+          "score": 0.061603,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18714,
+          "gene": "ZNF765",
+          "score": -0.083175,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18713,
+          "gene": "ZNF764",
+          "score": 0.29378,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18712,
+          "gene": "ZNF763",
+          "score": -0.23285,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18711,
+          "gene": "ZNF761",
+          "score": 0.014376,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18710,
+          "gene": "ZNF76",
+          "score": -0.61045,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18709,
+          "gene": "ZNF75D",
+          "score": 0.26196,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18708,
+          "gene": "ZNF75A",
+          "score": -0.00086138,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18707,
+          "gene": "ZNF750",
+          "score": 0.063188,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18706,
+          "gene": "ZNF749",
+          "score": 0.08545,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18705,
+          "gene": "ZNF747",
+          "score": -0.015003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18704,
+          "gene": "ZNF746",
+          "score": 0.067608,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18703,
+          "gene": "ZNF740",
+          "score": 0.24155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18702,
+          "gene": "ZNF74",
+          "score": 0.31314,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18701,
+          "gene": "ZNF737",
+          "score": -0.090301,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18700,
+          "gene": "ZNF736",
+          "score": -0.19433,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18699,
+          "gene": "ZNF735",
+          "score": 0.018026,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18698,
+          "gene": "ZNF732",
+          "score": -0.067965,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18697,
+          "gene": "ZNF730",
+          "score": 0.087429,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18696,
+          "gene": "ZNF729",
+          "score": -0.075084,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18695,
+          "gene": "ZNF728",
+          "score": 0.085004,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18694,
+          "gene": "ZNF727",
+          "score": 0.056405,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18693,
+          "gene": "ZNF726",
+          "score": 0.062063,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18692,
+          "gene": "ZNF721",
+          "score": 0.024887,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18691,
+          "gene": "ZNF718",
+          "score": -0.14311,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18690,
+          "gene": "ZNF717",
+          "score": -0.15785,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18689,
+          "gene": "ZNF716",
+          "score": -0.27842,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18688,
+          "gene": "ZNF714",
+          "score": 0.15933,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18687,
+          "gene": "ZNF713",
+          "score": -0.38127,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18686,
+          "gene": "ZNF711",
+          "score": -0.20572,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18685,
+          "gene": "ZNF710",
+          "score": -0.12781,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18684,
+          "gene": "ZNF71",
+          "score": 0.034771,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18683,
+          "gene": "ZNF709",
+          "score": -0.17863,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18682,
+          "gene": "ZNF708",
+          "score": 0.33228,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18681,
+          "gene": "ZNF707",
+          "score": 0.24123,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18680,
+          "gene": "ZNF706",
+          "score": -0.036214,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18679,
+          "gene": "ZNF705G",
+          "score": -0.045052,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18678,
+          "gene": "ZNF705E",
+          "score": -0.010156,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18677,
+          "gene": "ZNF705D",
+          "score": -0.17766,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18676,
+          "gene": "ZNF705B",
+          "score": 0.13595,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18675,
+          "gene": "ZNF705A",
+          "score": -0.21217,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18674,
+          "gene": "ZNF704",
+          "score": 0.028186,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18673,
+          "gene": "ZNF703",
+          "score": 0.20221,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18672,
+          "gene": "ZNF701",
+          "score": 0.14396,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18671,
+          "gene": "ZNF700",
+          "score": 0.069497,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18670,
+          "gene": "ZNF70",
+          "score": -0.051416,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18669,
+          "gene": "ZNF7",
+          "score": -0.068836,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18668,
+          "gene": "ZNF699",
+          "score": 0.12067,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18667,
+          "gene": "ZNF697",
+          "score": -0.39033,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18666,
+          "gene": "ZNF696",
+          "score": 0.15799,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18665,
+          "gene": "ZNF695",
+          "score": -0.14239,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18664,
+          "gene": "ZNF692",
+          "score": 0.06298,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18663,
+          "gene": "ZNF691",
+          "score": -0.089318,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18662,
+          "gene": "ZNF69",
+          "score": -0.23795,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18661,
+          "gene": "ZNF689",
+          "score": 0.22088,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18660,
+          "gene": "ZNF688",
+          "score": -0.058283,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18659,
+          "gene": "ZNF687",
+          "score": -0.065126,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18658,
+          "gene": "ZNF684",
+          "score": -0.12392,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18657,
+          "gene": "ZNF683",
+          "score": 0.12441,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18656,
+          "gene": "ZNF682",
+          "score": -0.076369,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18655,
+          "gene": "ZNF681",
+          "score": -0.1074,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18654,
+          "gene": "ZNF680",
+          "score": 0.11484,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18653,
+          "gene": "ZNF679",
+          "score": -0.016099,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18652,
+          "gene": "ZNF678",
+          "score": 0.019563,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18651,
+          "gene": "ZNF677",
+          "score": 0.047365,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18650,
+          "gene": "ZNF676",
+          "score": 0.20676,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18649,
+          "gene": "ZNF675",
+          "score": 0.20089,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18648,
+          "gene": "ZNF674",
+          "score": 0.09181,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18647,
+          "gene": "ZNF672",
+          "score": -0.010674,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18646,
+          "gene": "ZNF671",
+          "score": 0.3623,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18645,
+          "gene": "ZNF670",
+          "score": 0.021153,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18644,
+          "gene": "ZNF669",
+          "score": 0.001308,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18643,
+          "gene": "ZNF668",
+          "score": 0.33079,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18642,
+          "gene": "ZNF667",
+          "score": 0.083943,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18641,
+          "gene": "ZNF665",
+          "score": -0.10005,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18640,
+          "gene": "ZNF664-FAM101A",
+          "score": -0.16124,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18639,
+          "gene": "ZNF664",
+          "score": -0.14921,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18638,
+          "gene": "ZNF662",
+          "score": 0.16768,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18637,
+          "gene": "ZNF660",
+          "score": 0.34349,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18636,
+          "gene": "ZNF658",
+          "score": -0.11501,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18635,
+          "gene": "ZNF655",
+          "score": 0.34436,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18634,
+          "gene": "ZNF654",
+          "score": -0.065974,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18633,
+          "gene": "ZNF653",
+          "score": -0.052086,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18632,
+          "gene": "ZNF652",
+          "score": -0.073012,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18631,
+          "gene": "ZNF649",
+          "score": 0.23818,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18630,
+          "gene": "ZNF648",
+          "score": 0.12368,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18629,
+          "gene": "ZNF646",
+          "score": 0.14022,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18628,
+          "gene": "ZNF644",
+          "score": -0.056298,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18627,
+          "gene": "ZNF641",
+          "score": 0.27094,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18626,
+          "gene": "ZNF639",
+          "score": 0.10462,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18625,
+          "gene": "ZNF638",
+          "score": -0.20538,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18624,
+          "gene": "ZNF630",
+          "score": 0.041454,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18623,
+          "gene": "ZNF629",
+          "score": -0.0084088,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18622,
+          "gene": "ZNF628",
+          "score": 0.042279,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18621,
+          "gene": "ZNF627",
+          "score": 0.092429,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18620,
+          "gene": "ZNF626",
+          "score": -0.17748,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18619,
+          "gene": "ZNF625",
+          "score": -0.056479,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18618,
+          "gene": "ZNF624",
+          "score": -0.23871,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18617,
+          "gene": "ZNF623",
+          "score": 0.10487,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18616,
+          "gene": "ZNF622",
+          "score": 0.053701,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18615,
+          "gene": "ZNF621",
+          "score": 0.11706,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18614,
+          "gene": "ZNF620",
+          "score": 0.16024,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18613,
+          "gene": "ZNF619",
+          "score": 0.46215,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18612,
+          "gene": "ZNF618",
+          "score": -0.16295,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18611,
+          "gene": "ZNF616",
+          "score": 0.11379,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18610,
+          "gene": "ZNF615",
+          "score": -0.37046,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18609,
+          "gene": "ZNF614",
+          "score": 0.073856,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18608,
+          "gene": "ZNF613",
+          "score": -0.13374,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18607,
+          "gene": "ZNF611",
+          "score": -0.028518,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18606,
+          "gene": "ZNF610",
+          "score": 0.066008,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18605,
+          "gene": "ZNF609",
+          "score": -0.032282,
+          "hit": 0,
+          "round": 2
         }
       ],
       "queried_history": [
@@ -3128,896 +4024,1792 @@
           "gene": "ZZZ3",
           "score": 0.0042296,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18859,
           "gene": "ZZEF1",
           "score": -0.025285,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18858,
           "gene": "ZYX",
           "score": -0.12133,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18857,
           "gene": "ZYG11B",
           "score": -0.17865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18856,
           "gene": "ZYG11A",
           "score": -0.092959,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18855,
           "gene": "ZXDC",
           "score": -0.34067,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18854,
           "gene": "ZXDB",
           "score": 0.23355,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18853,
           "gene": "ZXDA",
           "score": 0.046151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18852,
           "gene": "ZWINT",
           "score": 0.2271,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18851,
           "gene": "ZWILCH",
           "score": -0.25147,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18850,
           "gene": "ZW10",
           "score": 0.10344,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18849,
           "gene": "ZUP1",
           "score": -0.18422,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18848,
           "gene": "ZSWIM9",
           "score": -0.11507,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18847,
           "gene": "ZSWIM8",
           "score": -0.30802,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18846,
           "gene": "ZSWIM7",
           "score": 0.0039042,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18845,
           "gene": "ZSWIM6",
           "score": -0.10342,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18844,
           "gene": "ZSWIM5",
           "score": 0.12314,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18843,
           "gene": "ZSWIM4",
           "score": -0.16708,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18842,
           "gene": "ZSWIM3",
           "score": 0.039048,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18841,
           "gene": "ZSWIM2",
           "score": -0.052248,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18840,
           "gene": "ZSWIM1",
           "score": 0.29132,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18839,
           "gene": "ZSCAN9",
           "score": -0.29343,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18838,
           "gene": "ZSCAN5B",
           "score": 0.27484,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18837,
           "gene": "ZSCAN5A",
           "score": -0.18237,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18836,
           "gene": "ZSCAN4",
           "score": 0.11831,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18835,
           "gene": "ZSCAN32",
           "score": 0.051154,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18834,
           "gene": "ZSCAN31",
           "score": -0.13807,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18833,
           "gene": "ZSCAN30",
           "score": 0.12307,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18832,
           "gene": "ZSCAN29",
           "score": -0.19019,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18831,
           "gene": "ZSCAN26",
           "score": 0.25286,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18830,
           "gene": "ZSCAN25",
           "score": 0.048302,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18829,
           "gene": "ZSCAN23",
           "score": 0.22488,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18828,
           "gene": "ZSCAN22",
           "score": -0.022625,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18827,
           "gene": "ZSCAN21",
           "score": 0.11542,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18826,
           "gene": "ZSCAN20",
           "score": 0.1752,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18825,
           "gene": "ZSCAN2",
           "score": -0.066826,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18824,
           "gene": "ZSCAN18",
           "score": -0.20931,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18823,
           "gene": "ZSCAN16",
           "score": 0.1603,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18822,
           "gene": "ZSCAN12",
           "score": 0.06866,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18821,
           "gene": "ZSCAN10",
           "score": 0.012773,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18820,
           "gene": "ZSCAN1",
           "score": -0.29437,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18819,
           "gene": "ZRSR2",
           "score": -0.087505,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18818,
           "gene": "ZRANB3",
           "score": 0.01562,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18817,
           "gene": "ZRANB2",
           "score": 0.11397,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18816,
           "gene": "ZRANB1",
           "score": 0.021138,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18815,
           "gene": "ZPR1",
           "score": 0.11386,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18814,
           "gene": "ZPLD1",
           "score": -0.36895,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18813,
           "gene": "ZPBP2",
           "score": 0.1462,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18812,
           "gene": "ZPBP",
           "score": -0.047664,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18811,
           "gene": "ZP4",
           "score": 0.19443,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18810,
           "gene": "ZP3",
           "score": -0.11782,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18809,
           "gene": "ZP2",
           "score": 0.20235,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18808,
           "gene": "ZP1",
           "score": -0.044293,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18807,
           "gene": "ZNRF4",
           "score": 0.29151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18806,
           "gene": "ZNRF3",
           "score": 0.041693,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18805,
           "gene": "ZNRF2",
           "score": -0.089597,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18804,
           "gene": "ZNRF1",
           "score": 0.12582,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18803,
           "gene": "ZNRD2",
           "score": 0.26195,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18802,
           "gene": "ZNHIT6",
           "score": -0.20291,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18801,
           "gene": "ZNHIT3",
           "score": 0.0056953,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18800,
           "gene": "ZNHIT2",
           "score": -1.3601,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18799,
           "gene": "ZNHIT1",
           "score": 0.036511,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18798,
           "gene": "ZNG1F",
           "score": -0.038808,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18797,
           "gene": "ZNG1E",
           "score": 0.14976,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18796,
           "gene": "ZNG1C",
           "score": 0.37958,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18795,
           "gene": "ZNG1B",
           "score": -0.089569,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18794,
           "gene": "ZNG1A",
           "score": 0.56598,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18793,
           "gene": "ZNFX1",
           "score": 0.24159,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18792,
           "gene": "ZNF99",
           "score": -0.27492,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18791,
           "gene": "ZNF98",
           "score": -0.22855,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18790,
           "gene": "ZNF93",
           "score": -0.15849,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18789,
           "gene": "ZNF92",
           "score": -0.14714,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18788,
           "gene": "ZNF91",
           "score": 0.11351,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18787,
           "gene": "ZNF90",
           "score": -0.040383,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18786,
           "gene": "ZNF891",
           "score": 0.21264,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18785,
           "gene": "ZNF883",
           "score": 0.14573,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18784,
           "gene": "ZNF880",
           "score": 0.19681,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18783,
           "gene": "ZNF879",
           "score": -0.046847,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18782,
           "gene": "ZNF878",
           "score": -0.064465,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18781,
           "gene": "ZNF875",
           "score": 0.25437,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18780,
           "gene": "ZNF865",
           "score": -0.16523,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18779,
           "gene": "ZNF862",
           "score": -0.20088,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18778,
           "gene": "ZNF860",
           "score": 0.12794,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18777,
           "gene": "ZNF853",
           "score": -0.053904,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18776,
           "gene": "ZNF852",
           "score": 0.33108,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18775,
           "gene": "ZNF850",
           "score": -0.01923,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18774,
           "gene": "ZNF85",
           "score": -0.12341,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18773,
           "gene": "ZNF846",
           "score": 0.099597,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18772,
           "gene": "ZNF845",
           "score": -0.013274,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18771,
           "gene": "ZNF844",
           "score": 0.26723,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18770,
           "gene": "ZNF843",
           "score": 0.0179,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18769,
           "gene": "ZNF841",
           "score": 4.0967e-06,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18768,
           "gene": "ZNF84",
           "score": -0.042649,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18767,
           "gene": "ZNF839",
           "score": 0.13634,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18766,
           "gene": "ZNF837",
           "score": -0.082197,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18765,
           "gene": "ZNF836",
           "score": -0.044699,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18764,
           "gene": "ZNF835",
           "score": 0.22762,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18763,
           "gene": "ZNF831",
           "score": 0.30395,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18762,
           "gene": "ZNF830",
           "score": -0.043654,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18761,
           "gene": "ZNF83",
           "score": 0.0444415,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18760,
           "gene": "ZNF829",
           "score": -0.27861,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18759,
           "gene": "ZNF827",
           "score": 0.0040781,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18758,
           "gene": "ZNF823",
           "score": 0.3592,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18757,
           "gene": "ZNF821",
           "score": 0.34549,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18756,
           "gene": "ZNF816-ZNF321P",
           "score": 0.011543,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18755,
           "gene": "ZNF816",
           "score": -0.012604,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18754,
           "gene": "ZNF814",
           "score": 0.086018,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18753,
           "gene": "ZNF813",
           "score": 0.017173,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18752,
           "gene": "ZNF812",
           "score": -0.050495,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18751,
           "gene": "ZNF81",
           "score": -0.26963,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18750,
           "gene": "ZNF808",
           "score": -0.021356,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18749,
           "gene": "ZNF806",
           "score": 0.33901,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18748,
           "gene": "ZNF805",
           "score": 0.052151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18747,
           "gene": "ZNF804B",
           "score": -0.1854,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18746,
           "gene": "ZNF804A",
           "score": 0.43123,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18745,
           "gene": "ZNF800",
           "score": -0.0068465,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18744,
           "gene": "ZNF80",
           "score": -0.058066,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18743,
           "gene": "ZNF8",
           "score": 0.10159,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18742,
           "gene": "ZNF799",
           "score": -0.19427,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18741,
           "gene": "ZNF793",
           "score": -0.0069571,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18740,
           "gene": "ZNF792",
           "score": 0.19458,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18739,
           "gene": "ZNF791",
           "score": 0.06026,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18738,
           "gene": "ZNF790",
           "score": 0.26988,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18737,
           "gene": "ZNF79",
           "score": -0.013901,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18736,
           "gene": "ZNF789",
           "score": -0.083043,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18735,
           "gene": "ZNF787",
           "score": 0.15997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18734,
           "gene": "ZNF786",
           "score": -0.074249,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18733,
           "gene": "ZNF785",
           "score": 0.57649,
           "hit": 1,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 18732,
+          "gene": "ZNF784",
+          "score": 0.064117,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18731,
+          "gene": "ZNF783",
+          "score": 0.0060596,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18730,
+          "gene": "ZNF782",
+          "score": 0.031375,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18729,
+          "gene": "ZNF781",
+          "score": 0.061165,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18728,
+          "gene": "ZNF780B",
+          "score": 0.10489,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18727,
+          "gene": "ZNF780A",
+          "score": 0.046046,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18726,
+          "gene": "ZNF778",
+          "score": 0.12097,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18725,
+          "gene": "ZNF777",
+          "score": 0.15411,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18724,
+          "gene": "ZNF776",
+          "score": -0.13952,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18723,
+          "gene": "ZNF775",
+          "score": 0.089403,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18722,
+          "gene": "ZNF774",
+          "score": 0.038457,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18721,
+          "gene": "ZNF773",
+          "score": -0.15373,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18720,
+          "gene": "ZNF772",
+          "score": 0.2649,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18719,
+          "gene": "ZNF771",
+          "score": -0.10739,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18718,
+          "gene": "ZNF770",
+          "score": -0.077469,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18717,
+          "gene": "ZNF77",
+          "score": 0.14069,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18716,
+          "gene": "ZNF768",
+          "score": -0.07904,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18715,
+          "gene": "ZNF766",
+          "score": 0.061603,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18714,
+          "gene": "ZNF765",
+          "score": -0.083175,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18713,
+          "gene": "ZNF764",
+          "score": 0.29378,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18712,
+          "gene": "ZNF763",
+          "score": -0.23285,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18711,
+          "gene": "ZNF761",
+          "score": 0.014376,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18710,
+          "gene": "ZNF76",
+          "score": -0.61045,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18709,
+          "gene": "ZNF75D",
+          "score": 0.26196,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18708,
+          "gene": "ZNF75A",
+          "score": -0.00086138,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18707,
+          "gene": "ZNF750",
+          "score": 0.063188,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18706,
+          "gene": "ZNF749",
+          "score": 0.08545,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18705,
+          "gene": "ZNF747",
+          "score": -0.015003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18704,
+          "gene": "ZNF746",
+          "score": 0.067608,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18703,
+          "gene": "ZNF740",
+          "score": 0.24155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18702,
+          "gene": "ZNF74",
+          "score": 0.31314,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18701,
+          "gene": "ZNF737",
+          "score": -0.090301,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18700,
+          "gene": "ZNF736",
+          "score": -0.19433,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18699,
+          "gene": "ZNF735",
+          "score": 0.018026,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18698,
+          "gene": "ZNF732",
+          "score": -0.067965,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18697,
+          "gene": "ZNF730",
+          "score": 0.087429,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18696,
+          "gene": "ZNF729",
+          "score": -0.075084,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18695,
+          "gene": "ZNF728",
+          "score": 0.085004,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18694,
+          "gene": "ZNF727",
+          "score": 0.056405,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18693,
+          "gene": "ZNF726",
+          "score": 0.062063,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18692,
+          "gene": "ZNF721",
+          "score": 0.024887,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18691,
+          "gene": "ZNF718",
+          "score": -0.14311,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18690,
+          "gene": "ZNF717",
+          "score": -0.15785,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18689,
+          "gene": "ZNF716",
+          "score": -0.27842,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18688,
+          "gene": "ZNF714",
+          "score": 0.15933,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18687,
+          "gene": "ZNF713",
+          "score": -0.38127,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18686,
+          "gene": "ZNF711",
+          "score": -0.20572,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18685,
+          "gene": "ZNF710",
+          "score": -0.12781,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18684,
+          "gene": "ZNF71",
+          "score": 0.034771,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18683,
+          "gene": "ZNF709",
+          "score": -0.17863,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18682,
+          "gene": "ZNF708",
+          "score": 0.33228,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18681,
+          "gene": "ZNF707",
+          "score": 0.24123,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18680,
+          "gene": "ZNF706",
+          "score": -0.036214,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18679,
+          "gene": "ZNF705G",
+          "score": -0.045052,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18678,
+          "gene": "ZNF705E",
+          "score": -0.010156,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18677,
+          "gene": "ZNF705D",
+          "score": -0.17766,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18676,
+          "gene": "ZNF705B",
+          "score": 0.13595,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18675,
+          "gene": "ZNF705A",
+          "score": -0.21217,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18674,
+          "gene": "ZNF704",
+          "score": 0.028186,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18673,
+          "gene": "ZNF703",
+          "score": 0.20221,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18672,
+          "gene": "ZNF701",
+          "score": 0.14396,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18671,
+          "gene": "ZNF700",
+          "score": 0.069497,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18670,
+          "gene": "ZNF70",
+          "score": -0.051416,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18669,
+          "gene": "ZNF7",
+          "score": -0.068836,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18668,
+          "gene": "ZNF699",
+          "score": 0.12067,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18667,
+          "gene": "ZNF697",
+          "score": -0.39033,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18666,
+          "gene": "ZNF696",
+          "score": 0.15799,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18665,
+          "gene": "ZNF695",
+          "score": -0.14239,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18664,
+          "gene": "ZNF692",
+          "score": 0.06298,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18663,
+          "gene": "ZNF691",
+          "score": -0.089318,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18662,
+          "gene": "ZNF69",
+          "score": -0.23795,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18661,
+          "gene": "ZNF689",
+          "score": 0.22088,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18660,
+          "gene": "ZNF688",
+          "score": -0.058283,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18659,
+          "gene": "ZNF687",
+          "score": -0.065126,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18658,
+          "gene": "ZNF684",
+          "score": -0.12392,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18657,
+          "gene": "ZNF683",
+          "score": 0.12441,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18656,
+          "gene": "ZNF682",
+          "score": -0.076369,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18655,
+          "gene": "ZNF681",
+          "score": -0.1074,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18654,
+          "gene": "ZNF680",
+          "score": 0.11484,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18653,
+          "gene": "ZNF679",
+          "score": -0.016099,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18652,
+          "gene": "ZNF678",
+          "score": 0.019563,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18651,
+          "gene": "ZNF677",
+          "score": 0.047365,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18650,
+          "gene": "ZNF676",
+          "score": 0.20676,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18649,
+          "gene": "ZNF675",
+          "score": 0.20089,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18648,
+          "gene": "ZNF674",
+          "score": 0.09181,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18647,
+          "gene": "ZNF672",
+          "score": -0.010674,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18646,
+          "gene": "ZNF671",
+          "score": 0.3623,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18645,
+          "gene": "ZNF670",
+          "score": 0.021153,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18644,
+          "gene": "ZNF669",
+          "score": 0.001308,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18643,
+          "gene": "ZNF668",
+          "score": 0.33079,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18642,
+          "gene": "ZNF667",
+          "score": 0.083943,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18641,
+          "gene": "ZNF665",
+          "score": -0.10005,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18640,
+          "gene": "ZNF664-FAM101A",
+          "score": -0.16124,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18639,
+          "gene": "ZNF664",
+          "score": -0.14921,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18638,
+          "gene": "ZNF662",
+          "score": 0.16768,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18637,
+          "gene": "ZNF660",
+          "score": 0.34349,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18636,
+          "gene": "ZNF658",
+          "score": -0.11501,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18635,
+          "gene": "ZNF655",
+          "score": 0.34436,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18634,
+          "gene": "ZNF654",
+          "score": -0.065974,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18633,
+          "gene": "ZNF653",
+          "score": -0.052086,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18632,
+          "gene": "ZNF652",
+          "score": -0.073012,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18631,
+          "gene": "ZNF649",
+          "score": 0.23818,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18630,
+          "gene": "ZNF648",
+          "score": 0.12368,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18629,
+          "gene": "ZNF646",
+          "score": 0.14022,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18628,
+          "gene": "ZNF644",
+          "score": -0.056298,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18627,
+          "gene": "ZNF641",
+          "score": 0.27094,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18626,
+          "gene": "ZNF639",
+          "score": 0.10462,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18625,
+          "gene": "ZNF638",
+          "score": -0.20538,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18624,
+          "gene": "ZNF630",
+          "score": 0.041454,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18623,
+          "gene": "ZNF629",
+          "score": -0.0084088,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18622,
+          "gene": "ZNF628",
+          "score": 0.042279,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18621,
+          "gene": "ZNF627",
+          "score": 0.092429,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18620,
+          "gene": "ZNF626",
+          "score": -0.17748,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18619,
+          "gene": "ZNF625",
+          "score": -0.056479,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18618,
+          "gene": "ZNF624",
+          "score": -0.23871,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18617,
+          "gene": "ZNF623",
+          "score": 0.10487,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18616,
+          "gene": "ZNF622",
+          "score": 0.053701,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18615,
+          "gene": "ZNF621",
+          "score": 0.11706,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18614,
+          "gene": "ZNF620",
+          "score": 0.16024,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18613,
+          "gene": "ZNF619",
+          "score": 0.46215,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18612,
+          "gene": "ZNF618",
+          "score": -0.16295,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18611,
+          "gene": "ZNF616",
+          "score": 0.11379,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18610,
+          "gene": "ZNF615",
+          "score": -0.37046,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 18609,
+          "gene": "ZNF614",
+          "score": 0.073856,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18608,
+          "gene": "ZNF613",
+          "score": -0.13374,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18607,
+          "gene": "ZNF611",
+          "score": -0.028518,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18606,
+          "gene": "ZNF610",
+          "score": 0.066008,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18605,
+          "gene": "ZNF609",
+          "score": -0.032282,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
