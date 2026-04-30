# Change Record — candidate_4

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IFNG/run-1/best/current/harness
Generated at: 2026-04-30T06:46:55.709988

## Files Changed

- model.py: modified (added=2, deleted=2, delta=0)
- outputs/metrics.json: modified (added=2362, deleted=570, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -92,8 +92,8 @@
                 # Bias exploration toward negative scores (hits are at -0.4 to -0.5)
                 ucb_negative = min_observed_score - 0.1 * abs(min_observed_score) if min_observed_score != 0 else -1.0
                 ucb_positive = max_observed_score + 0.1 * abs(max_observed_score) if max_observed_score != 0 else 1.0
-                # Blend: 75% weight on negative exploration (hits), 25% on positive
-                ucb = 0.75 * ucb_negative + 0.25 * ucb_positive
+                # Blend: 80% weight on negative exploration (hits), 20% on positive
+                ucb = 0.8 * ucb_negative + 0.2 * ucb_positive
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
-      "rounds": 3,
+      "rounds": 4,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 256,
-      "baseline_total_hits": 3,
+      "baseline_total_queries": 384,
+      "baseline_total_hits": 8,
       "delta_queries": 128,
-      "delta_hits": 5,
-      "total_queries": 384,
-      "total_hits": 8,
+      "delta_hits": 1,
+      "total_queries": 512,
+      "total_hits": 9,
       "top_k": 920,
       "hit_curve": {
         "queries": [
-          256,
-          384
+          384,
+          512
         ],
         "hits": [
-          3,
-          8
+          8,
+          9
         ]
       },
-      "auc": 704.0,
-      "auc_normalized": 0.0019927536231884057,
-      "ncg": 0.16944364830290376,
+      "auc": 1088.0,
+      "auc_normalized": 0.0023097826086956523,
+      "ncg": 0.18526733430524442,
       "round_details": [
         {
-          "round": 2,
+          "round": 3,
           "selected_count": 128,
-          "hits": 5,
-          "cumulative_hits": 8,
-          "precision_at_batch": 0.0390625,
+          "hits": 1,
+          "cumulative_hits": 9,
+          "precision_at_batch": 0.0078125,
           "selected": [
-            "ZNF655",
-            "ZNF703",
-            "ZNF658",
-            "ZNF608",
-            "ZNF618",
-            "ZNF605",
-            "ZNF681",
-            "ZNF771",
-            "ZNF687",
-            "ZNF682",
-            "ZNF609",
-            "ZNF606",
-            "ZNF730",
-            "ZNF689",
-            "ZNF649",
-            "ZNF70",
-            "ZNF671",
-            "ZNF607",
-            "ZNF69",
-            "ZNF701",
-            "ZNF766",
-            "ZNF74",
-            "ZNF684",
-            "ZNF678",
-            "ZNF670",
-            "ZNF621",
-            "ZNF705B",
-            "ZNF76",
-            "ZNF620",
-            "ZNF740",
-            "ZNF616",
-            "ZNF75A",
-            "ZNF749",
-            "ZNF775",
-            "ZNF746",
-            "ZNF677",
-            "ZNF654",
-            "ZNF705D",
-            "ZNF761",
-            "ZNF695",
-            "ZNF727",
-            "ZNF641",
-            "ZNF627",
-            "ZNF697",
-            "ZNF709",
-            "ZNF696",
-            "ZNF782",
-            "ZNF772",
-            "ZNF764",
-            "ZNF780B",
-            "ZNF705A",
-            "ZNF717",
-            "ZNF611",
-            "ZNF653",
-            "ZNF662",
-            "ZNF705G",
-            "ZNF736",
-            "ZNF735",
-            "ZNF660",
-            "ZNF652",
-            "ZNF668",
-            "ZNF639",
-            "ZNF672",
-            "ZNF700",
-            "ZNF679",
-            "ZNF708",
-            "ZNF713",
-            "ZNF629",
-            "ZNF704",
-            "ZNF777",
-            "ZNF776",
-            "ZNF732",
-            "ZNF729",
-            "ZNF765",
-            "ZNF644",
-            "ZNF747",
-            "ZNF7",
-            "ZNF699",
-            "ZNF667",
-            "ZNF706",
-            "ZNF710",
-            "ZNF778",
-            "ZNF615",
-            "ZNF675",
-            "ZNF77",
-            "ZNF716",
-            "ZNF728",
-            "ZNF622",
-            "ZNF638",
-            "ZNF774",
-            "ZNF625",
-            "ZNF619",
-            "ZNF623",
-            "ZNF676",
-            "ZNF726",
-            "ZNF711",
-            "ZNF773",
-            "ZNF71",
-            "ZNF714",
-            "ZNF669",
-            "ZNF628",
-            "ZNF648",
-            "ZNF705E",
-            "ZNF680",
-            "ZNF613",
-            "ZNF674",
-            "ZNF626",
-            "ZNF718",
-            "ZNF665",
-            "ZNF692",
-            "ZNF646",
-            "ZNF75D",
-            "ZNF770",
-            "ZNF781",
-            "ZNF683",
-            "ZNF610",
-            "ZNF614",
-            "ZNF780A",
-            "ZNF721",
-            "ZNF737",
-            "ZNF707",
-            "ZNF750",
-            "ZNF768",
-            "ZNF624",
-            "ZNF664",
-            "ZNF688",
-            "ZNF691",
-            "ZNF630"
+            "ZNF585A",
+            "ZNF524",
+            "ZNF552",
+            "ZNF449",
+            "ZNF500",
+            "ZNF431",
+            "ZNF496",
+            "ZNF436",
+            "ZNF530",
+            "ZNF471",
+            "ZNF511-PRAP1",
+            "ZNF550",
+            "ZNF569",
+            "ZNF577",
+            "ZNF534",
+            "ZNF443",
+            "ZNF490",
+            "ZNF548",
+            "ZNF445",
+            "ZNF511",
+            "ZNF582",
+            "ZNF486",
+            "ZNF492",
+            "ZNF512B",
+            "ZNF540",
+            "ZNF514",
+            "ZNF438",
+            "ZNF570",
+            "ZNF442",
+            "ZNF461",
+            "ZNF517",
+            "ZNF575",
+            "ZNF536",
+            "ZNF594",
+            "ZNF573",
+            "ZNF547",
+            "ZNF462",
+            "ZNF600",
+            "ZNF502",
+            "ZNF433",
+            "ZNF43",
+            "ZNF578",
+            "ZNF485",
+            "ZNF566",
+            "ZNF460",
+            "ZNF506",
+            "ZNF467",
+            "ZNF45",
+            "ZNF441",
+            "ZNF446",
+            "ZNF512",
+            "ZNF597",
+            "ZNF532",
+            "ZNF541",
+            "ZNF595",
+            "ZNF564",
+            "ZNF57",
+            "ZNF526",
+            "ZNF480",
+            "ZNF440",
+            "ZNF430",
+            "ZNF574",
+            "ZNF521",
+            "ZNF516",
+            "ZNF562",
+            "ZNF473",
+            "ZNF513",
+            "ZNF568",
+            "ZNF503",
+            "ZNF444",
+            "ZNF555",
+            "ZNF572",
+            "ZNF551",
+            "ZNF527",
+            "ZNF479",
+            "ZNF493",
+            "ZNF518B",
+            "ZNF519",
+            "ZNF549",
+            "ZNF497",
+            "ZNF557",
+            "ZNF439",
+            "ZNF586",
+            "ZNF469",
+            "ZNF585B",
+            "ZNF559",
+            "ZNF554",
+            "ZNF432",
+            "ZNF558",
+            "ZNF576",
+            "ZNF454",
+            "ZNF593",
+            "ZNF491",
+            "ZNF580",
+            "ZNF546",
+            "ZNF510",
+            "ZNF44",
+            "ZNF543",
+            "ZNF488",
+            "ZNF48",
+            "ZNF571",
+            "ZNF579",
+            "ZNF484",
+            "ZNF470",
+            "ZNF565",
+            "ZNF581",
+            "ZNF592",
+            "ZNF507",
+            "ZNF596",
+            "ZNF501",
+            "ZNF483",
+            "ZNF451",
+            "ZNF560",
+            "ZNF583",
+            "ZNF468",
+            "ZNF563",
+            "ZNF584",
+            "ZNF599",
+            "ZNF529",
+            "ZNF589",
+            "ZNF598",
+            "ZNF556",
+            "ZNF561",
+            "ZNF587",
+            "ZNF567",
+            "ZNF528",
+            "ZNF544",
+            "ZNF518A"
           ],
           "selected_scores": [
-            -0.1833125,
-            -0.0852,
-            0.044175,
-            0.2987305,
-            -0.190475,
-            -0.13111839,
-            0.128045,
-            -0.149708,
-            -0.262595,
-            -0.199155,
-            -0.32101,
-            0.069635,
-            -0.06505,
-            -0.02664,
-            -0.091537,
-            -0.0901975,
-            0.09395745,
-            -0.0026525,
-            -0.1912095,
-            -0.391055,
-            0.07028355,
-            -0.443155,
-            0.113969,
-            0.1374395,
-            0.289355,
-            0.086152,
-            -0.059855,
-            0.013145,
-            -0.16560645,
-            0.1171905,
-            0.106625,
-            0.2089455,
-            0.027157,
-            -0.446395,
-            0.39508,
-            -0.044635,
-            -0.09401,
-            -0.2711,
-            -0.29709,
-            -0.0494725,
-            -0.08205,
-            -0.1801195,
-            0.006615,
-            0.33112,
-            0.0628615,
-            -0.005585,
-            -0.07841,
-            -0.227325,
-            0.14892,
-            -0.15895,
-            0.0939665,
-            0.251,
-            0.28251,
-            -0.146895,
-            -0.1954055,
-            0.05468,
-            -0.014509,
-            0.02091,
-            -0.12729,
-            0.1074805,
-            0.0942455,
-            -0.478455,
-            0.091869,
-            0.070234,
-            -0.029394,
-            0.0181625,
-            0.15265,
-            0.3354,
-            -0.093379,
-            0.1705515,
-            -0.00751,
-            0.1017415,
-            0.012581,
-            -0.389585,
-            0.280492,
-            -0.00157,
-            -0.0977735,
-            -0.1837,
-            0.03447775,
-            -0.02961,
-            0.09547,
-            0.1257655,
-            0.1941805,
-            0.31613,
-            0.158275,
-            0.006445,
-            0.1207145,
-            0.085554,
-            -0.156016,
-            0.0492925,
-            0.2007245,
-            0.227995,
-            -0.209705,
-            -0.0869881,
-            0.00325,
-            0.1338245,
-            0.130544,
-            -0.189513,
-            0.20327,
-            0.0332529,
-            0.02386,
-            0.239318,
-            -0.256575,
-            -0.0800905,
-            0.04389,
-            0.011945,
-            -0.145603,
-            -0.0575795,
-            -0.03955195,
-            0.29731,
-            0.1066445,
-            0.1355,
-            -0.0537535,
-            -0.31094,
-            0.0220375,
-            0.12294,
-            -0.05491,
-            0.1124055,
-            0.26879,
-            0.216225,
-            0.37715,
-            0.031711,
-            0.01482,
-            -0.127621,
-            0.0808805,
-            -0.0863065,
-            -0.1299145,
-            0.08269
+            -0.029175,
+            0.1740205,
+            -0.18224,
+            0.02156985,
+            0.128354,
+            0.181045,
+            0.13378,
+            -0.22501,
+            0.111831,
+            0.16659,
+            0.101215,
+            0.0015315,
+            -0.2065345,
+            0.352155,
+            -0.1037915,
+            -0.1002155,
+            -0.0520515,
+            0.14674175,
+            0.185425,
+            -0.087807,
+            0.053413,
+            -0.01275,
+            0.2519605,
+            -0.13953,
+            0.096929,
+            0.0049065,
+            0.094816,
+            0.00226,
+            0.1677725,
+            -0.26366,
+            0.071871,
+            -0.32484,
+            0.201145,
+            -0.02139,
+            -0.1773585,
+            0.0528285,
+            -0.04815,
+            -0.13736,
+            0.009245,
+            -0.176507,
+            -0.1845355,
+            -0.15319,
+            0.271345,
+            -0.3362,
+            -0.092895,
+            -0.113433,
+            0.072695,
+            0.1424945,
+            -0.164674,
+            -0.061245,
+            -0.0526845,
+            -0.39098,
+            0.0522465,
+            -0.18417965,
+            -0.025711,
+            0.1820195,
+            0.103895,
+            0.137245,
+            0.24194,
+            -0.087465,
+            0.08786,
+            0.16361,
+            0.08589,
+            0.25173,
+            -0.3011635,
+            0.0156455,
+            0.01218,
+            0.0717735,
+            0.23489,
+            -0.0704355,
+            0.145655,
+            0.041181,
+            0.0350655,
+            0.0058345,
+            0.0278175,
+            0.009985,
+            0.31276,
+            -0.0857705,
+            0.22809,
+            0.000715,
+            0.264625,
+            -0.237145,
+            -0.198565,
+            0.051955,
+            -0.183071,
+            0.19544,
+            -0.250545,
+            -0.0355025,
+            0.006585,
+            0.389825,
+            0.11075185,
+            -0.0711965,
+            -0.035655,
+            0.234024,
+            -0.005505,
+            -0.184205,
+            -0.11366,
+            0.37438,
+            0.039261,
+            0.0807835,
+            0.077155,
+            0.026342,
+            -0.059251,
+            -0.1913,
+            -0.140035,
+            -0.0562255,
+            0.0864995,
+            0.037163,
+            0.376185,
+            -0.0899685,
+            0.1860085,
+            -0.06424,
+            0.0112985,
+            -0.05593,
+            -0.0068665,
+            0.168275,
+            0.337285,
+            -0.1666685,
+            -0.0121575,
+            -0.1166215,
+            -0.152225,
+            0.05136365,
+            0.29338,
+            0.052138,
+            0.03971,
+            0.037025,
+            -0.0599985,
+            -0.2550815
           ],
           "selected_hits": [
             0,
@@ -320,49 +320,49 @@
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
             1,
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
-            1,
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
-            1,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
             0,
             0,
             0,
@@ -2230,896 +2230,1792 @@
           "gene": "ZNF655",
           "score": -0.1833125,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18233,
           "gene": "ZNF703",
           "score": -0.0852,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18197,
           "gene": "ZNF658",
           "score": 0.044175,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18165,
           "gene": "ZNF608",
           "score": 0.2987305,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18173,
           "gene": "ZNF618",
           "score": -0.190475,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18162,
           "gene": "ZNF605",
           "score": -0.13111839,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18215,
           "gene": "ZNF681",
           "score": 0.128045,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18278,
           "gene": "ZNF771",
           "score": -0.149708,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18219,
           "gene": "ZNF687",
           "score": -0.262595,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18216,
           "gene": "ZNF682",
           "score": -0.199155,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18166,
           "gene": "ZNF609",
           "score": -0.32101,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18163,
           "gene": "ZNF606",
           "score": 0.069635,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18257,
           "gene": "ZNF730",
           "score": -0.06505,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18221,
           "gene": "ZNF689",
           "score": -0.02664,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18192,
           "gene": "ZNF649",
           "score": -0.091537,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18230,
           "gene": "ZNF70",
           "score": -0.0901975,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18206,
           "gene": "ZNF671",
           "score": 0.09395745,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18164,
           "gene": "ZNF607",
           "score": -0.0026525,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18222,
           "gene": "ZNF69",
           "score": -0.1912095,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18232,
           "gene": "ZNF701",
           "score": -0.391055,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18274,
           "gene": "ZNF766",
           "score": 0.07028355,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18262,
           "gene": "ZNF74",
           "score": -0.443155,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18218,
           "gene": "ZNF684",
           "score": 0.113969,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18212,
           "gene": "ZNF678",
           "score": 0.1374395,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18205,
           "gene": "ZNF670",
           "score": 0.289355,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18176,
           "gene": "ZNF621",
           "score": 0.086152,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18236,
           "gene": "ZNF705B",
           "score": -0.059855,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18270,
           "gene": "ZNF76",
           "score": 0.013145,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18175,
           "gene": "ZNF620",
           "score": -0.16560645,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18263,
           "gene": "ZNF740",
           "score": 0.1171905,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18172,
           "gene": "ZNF616",
           "score": 0.106625,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18268,
           "gene": "ZNF75A",
           "score": 0.2089455,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18266,
           "gene": "ZNF749",
           "score": 0.027157,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18282,
           "gene": "ZNF775",
           "score": -0.446395,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18264,
           "gene": "ZNF746",
           "score": 0.39508,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18211,
           "gene": "ZNF677",
           "score": -0.044635,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18195,
           "gene": "ZNF654",
           "score": -0.09401,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18237,
           "gene": "ZNF705D",
           "score": -0.2711,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18271,
           "gene": "ZNF761",
           "score": -0.29709,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18225,
           "gene": "ZNF695",
           "score": -0.0494725,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18254,
           "gene": "ZNF727",
           "score": -0.08205,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18188,
           "gene": "ZNF641",
           "score": -0.1801195,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18182,
           "gene": "ZNF627",
           "score": 0.006615,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18227,
           "gene": "ZNF697",
           "score": 0.33112,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18243,
           "gene": "ZNF709",
           "score": 0.0628615,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18226,
           "gene": "ZNF696",
           "score": -0.005585,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18289,
           "gene": "ZNF782",
           "score": -0.07841,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18279,
           "gene": "ZNF772",
           "score": -0.227325,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18272,
           "gene": "ZNF764",
           "score": 0.14892,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18287,
           "gene": "ZNF780B",
           "score": -0.15895,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18235,
           "gene": "ZNF705A",
           "score": 0.0939665,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18250,
           "gene": "ZNF717",
           "score": 0.251,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18168,
           "gene": "ZNF611",
           "score": 0.28251,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18194,
           "gene": "ZNF653",
           "score": -0.146895,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18199,
           "gene": "ZNF662",
           "score": -0.1954055,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18239,
           "gene": "ZNF705G",
           "score": 0.05468,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18260,
           "gene": "ZNF736",
           "score": -0.014509,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18259,
           "gene": "ZNF735",
           "score": 0.02091,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18198,
           "gene": "ZNF660",
           "score": -0.12729,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18193,
           "gene": "ZNF652",
           "score": 0.1074805,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18203,
           "gene": "ZNF668",
           "score": 0.0942455,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18187,
           "gene": "ZNF639",
           "score": -0.478455,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18207,
           "gene": "ZNF672",
           "score": 0.091869,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18231,
           "gene": "ZNF700",
           "score": 0.070234,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18213,
           "gene": "ZNF679",
           "score": -0.029394,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18242,
           "gene": "ZNF708",
           "score": 0.0181625,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18247,
           "gene": "ZNF713",
           "score": 0.15265,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18184,
           "gene": "ZNF629",
           "score": 0.3354,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18234,
           "gene": "ZNF704",
           "score": -0.093379,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18284,
           "gene": "ZNF777",
           "score": 0.1705515,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18283,
           "gene": "ZNF776",
           "score": -0.00751,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18258,
           "gene": "ZNF732",
           "score": 0.1017415,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18256,
           "gene": "ZNF729",
           "score": 0.012581,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18273,
           "gene": "ZNF765",
           "score": -0.389585,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18189,
           "gene": "ZNF644",
           "score": 0.280492,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18265,
           "gene": "ZNF747",
           "score": -0.00157,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18229,
           "gene": "ZNF7",
           "score": -0.0977735,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18228,
           "gene": "ZNF699",
           "score": -0.1837,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18202,
           "gene": "ZNF667",
           "score": 0.03447775,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18240,
           "gene": "ZNF706",
           "score": -0.02961,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18245,
           "gene": "ZNF710",
           "score": 0.09547,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18285,
           "gene": "ZNF778",
           "score": 0.1257655,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18171,
           "gene": "ZNF615",
           "score": 0.1941805,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18209,
           "gene": "ZNF675",
           "score": 0.31613,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18276,
           "gene": "ZNF77",
           "score": 0.158275,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18249,
           "gene": "ZNF716",
           "score": 0.006445,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18255,
           "gene": "ZNF728",
           "score": 0.1207145,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18177,
           "gene": "ZNF622",
           "score": 0.085554,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18186,
           "gene": "ZNF638",
           "score": -0.156016,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18281,
           "gene": "ZNF774",
           "score": 0.0492925,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18180,
           "gene": "ZNF625",
           "score": 0.2007245,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18174,
           "gene": "ZNF619",
           "score": 0.227995,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18178,
           "gene": "ZNF623",
           "score": -0.209705,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18210,
           "gene": "ZNF676",
           "score": -0.0869881,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18253,
           "gene": "ZNF726",
           "score": 0.00325,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18246,
           "gene": "ZNF711",
           "score": 0.1338245,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18280,
           "gene": "ZNF773",
           "score": 0.130544,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18244,
           "gene": "ZNF71",
           "score": -0.189513,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18248,
           "gene": "ZNF714",
           "score": 0.20327,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18204,
           "gene": "ZNF669",
           "score": 0.0332529,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18183,
           "gene": "ZNF628",
           "score": 0.02386,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18191,
           "gene": "ZNF648",
           "score": 0.239318,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18238,
           "gene": "ZNF705E",
           "score": -0.256575,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18214,
           "gene": "ZNF680",
           "score": -0.0800905,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18169,
           "gene": "ZNF613",
           "score": 0.04389,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18208,
           "gene": "ZNF674",
           "score": 0.011945,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18181,
           "gene": "ZNF626",
           "score": -0.145603,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18251,
           "gene": "ZNF718",
           "score": -0.0575795,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18201,
           "gene": "ZNF665",
           "score": -0.03955195,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18224,
           "gene": "ZNF692",
           "score": 0.29731,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18190,
           "gene": "ZNF646",
           "score": 0.1066445,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18269,
           "gene": "ZNF75D",
           "score": 0.1355,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18277,
           "gene": "ZNF770",
           "score": -0.0537535,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18288,
           "gene": "ZNF781",
           "score": -0.31094,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18217,
           "gene": "ZNF683",
           "score": 0.0220375,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18167,
           "gene": "ZNF610",
           "score": 0.12294,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18170,
           "gene": "ZNF614",
           "score": -0.05491,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18286,
           "gene": "ZNF780A",
           "score": 0.1124055,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18252,
           "gene": "ZNF721",
           "score": 0.26879,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18261,
           "gene": "ZNF737",
           "score": 0.216225,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18241,
           "gene": "ZNF707",
           "score": 0.37715,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18267,
           "gene": "ZNF750",
           "score": 0.031711,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18275,
           "gene": "ZNF768",
           "score": 0.01482,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18179,
           "gene": "ZNF624",
           "score": -0.127621,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18200,
           "gene": "ZNF664",
           "score": 0.0808805,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18220,
           "gene": "ZNF688",
           "score": -0.0863065,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18223,
           "gene": "ZNF691",
           "score": -0.1299145,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18185,
           "gene": "ZNF630",
           "score": 0.08269,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 18148,
+          "gene": "ZNF585A",
+          "score": -0.029175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18096,
+          "gene": "ZNF524",
+          "score": 0.1740205,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18115,
+          "gene": "ZNF552",
+          "score": -0.18224,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18050,
+          "gene": "ZNF449",
+          "score": 0.02156985,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18077,
+          "gene": "ZNF500",
+          "score": 0.128354,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18036,
+          "gene": "ZNF431",
+          "score": 0.181045,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18075,
+          "gene": "ZNF496",
+          "score": 0.13378,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18039,
+          "gene": "ZNF436",
+          "score": -0.22501,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18101,
+          "gene": "ZNF530",
+          "score": 0.111831,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18061,
+          "gene": "ZNF471",
+          "score": 0.16659,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18085,
+          "gene": "ZNF511-PRAP1",
+          "score": 0.101215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18113,
+          "gene": "ZNF550",
+          "score": 0.0015315,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18131,
+          "gene": "ZNF569",
+          "score": -0.2065345,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18140,
+          "gene": "ZNF577",
+          "score": 0.352155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18103,
+          "gene": "ZNF534",
+          "score": -0.1037915,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18046,
+          "gene": "ZNF443",
+          "score": -0.1002155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18071,
+          "gene": "ZNF490",
+          "score": -0.0520515,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18111,
+          "gene": "ZNF548",
+          "score": 0.14674175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18048,
+          "gene": "ZNF445",
+          "score": 0.185425,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18084,
+          "gene": "ZNF511",
+          "score": -0.087807,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18145,
+          "gene": "ZNF582",
+          "score": 0.053413,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18069,
+          "gene": "ZNF486",
+          "score": -0.01275,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18073,
+          "gene": "ZNF492",
+          "score": 0.2519605,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18087,
+          "gene": "ZNF512B",
+          "score": -0.13953,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18105,
+          "gene": "ZNF540",
+          "score": 0.096929,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18089,
+          "gene": "ZNF514",
+          "score": 0.0049065,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18040,
+          "gene": "ZNF438",
+          "score": 0.094816,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18133,
+          "gene": "ZNF570",
+          "score": 0.00226,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18045,
+          "gene": "ZNF442",
+          "score": 0.1677725,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18055,
+          "gene": "ZNF461",
+          "score": -0.26366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18091,
+          "gene": "ZNF517",
+          "score": 0.071871,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18138,
+          "gene": "ZNF575",
+          "score": -0.32484,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18104,
+          "gene": "ZNF536",
+          "score": 0.201145,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18155,
+          "gene": "ZNF594",
+          "score": -0.02139,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18136,
+          "gene": "ZNF573",
+          "score": -0.1773585,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18110,
+          "gene": "ZNF547",
+          "score": 0.0528285,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18056,
+          "gene": "ZNF462",
+          "score": -0.04815,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18161,
+          "gene": "ZNF600",
+          "score": -0.13736,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18079,
+          "gene": "ZNF502",
+          "score": 0.009245,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18038,
+          "gene": "ZNF433",
+          "score": -0.176507,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18034,
+          "gene": "ZNF43",
+          "score": -0.1845355,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18141,
+          "gene": "ZNF578",
+          "score": -0.15319,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18068,
+          "gene": "ZNF485",
+          "score": 0.271345,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18128,
+          "gene": "ZNF566",
+          "score": -0.3362,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18054,
+          "gene": "ZNF460",
+          "score": -0.092895,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18081,
+          "gene": "ZNF506",
+          "score": -0.113433,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18057,
+          "gene": "ZNF467",
+          "score": 0.072695,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18051,
+          "gene": "ZNF45",
+          "score": 0.1424945,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18044,
+          "gene": "ZNF441",
+          "score": -0.164674,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18049,
+          "gene": "ZNF446",
+          "score": -0.061245,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18086,
+          "gene": "ZNF512",
+          "score": -0.0526845,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18158,
+          "gene": "ZNF597",
+          "score": -0.39098,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18102,
+          "gene": "ZNF532",
+          "score": 0.0522465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18106,
+          "gene": "ZNF541",
+          "score": -0.18417965,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18156,
+          "gene": "ZNF595",
+          "score": -0.025711,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18126,
+          "gene": "ZNF564",
+          "score": 0.1820195,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18132,
+          "gene": "ZNF57",
+          "score": 0.103895,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18097,
+          "gene": "ZNF526",
+          "score": 0.137245,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18065,
+          "gene": "ZNF480",
+          "score": 0.24194,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18043,
+          "gene": "ZNF440",
+          "score": -0.087465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18035,
+          "gene": "ZNF430",
+          "score": 0.08786,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18137,
+          "gene": "ZNF574",
+          "score": 0.16361,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18095,
+          "gene": "ZNF521",
+          "score": 0.08589,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18090,
+          "gene": "ZNF516",
+          "score": 0.25173,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18124,
+          "gene": "ZNF562",
+          "score": -0.3011635,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18062,
+          "gene": "ZNF473",
+          "score": 0.0156455,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18088,
+          "gene": "ZNF513",
+          "score": 0.01218,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18130,
+          "gene": "ZNF568",
+          "score": 0.0717735,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18080,
+          "gene": "ZNF503",
+          "score": 0.23489,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18047,
+          "gene": "ZNF444",
+          "score": -0.0704355,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18117,
+          "gene": "ZNF555",
+          "score": 0.145655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18135,
+          "gene": "ZNF572",
+          "score": 0.041181,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18114,
+          "gene": "ZNF551",
+          "score": 0.0350655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18098,
+          "gene": "ZNF527",
+          "score": 0.0058345,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18063,
+          "gene": "ZNF479",
+          "score": 0.0278175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18074,
+          "gene": "ZNF493",
+          "score": 0.009985,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18093,
+          "gene": "ZNF518B",
+          "score": 0.31276,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18094,
+          "gene": "ZNF519",
+          "score": -0.0857705,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18112,
+          "gene": "ZNF549",
+          "score": 0.22809,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18076,
+          "gene": "ZNF497",
+          "score": 0.000715,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18119,
+          "gene": "ZNF557",
+          "score": 0.264625,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18041,
+          "gene": "ZNF439",
+          "score": -0.237145,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18150,
+          "gene": "ZNF586",
+          "score": -0.198565,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18059,
+          "gene": "ZNF469",
+          "score": 0.051955,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18149,
+          "gene": "ZNF585B",
+          "score": -0.183071,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18121,
+          "gene": "ZNF559",
+          "score": 0.19544,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18116,
+          "gene": "ZNF554",
+          "score": -0.250545,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18037,
+          "gene": "ZNF432",
+          "score": -0.0355025,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18120,
+          "gene": "ZNF558",
+          "score": 0.006585,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18139,
+          "gene": "ZNF576",
+          "score": 0.389825,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18053,
+          "gene": "ZNF454",
+          "score": 0.11075185,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18154,
+          "gene": "ZNF593",
+          "score": -0.0711965,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18072,
+          "gene": "ZNF491",
+          "score": -0.035655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18143,
+          "gene": "ZNF580",
+          "score": 0.234024,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18109,
+          "gene": "ZNF546",
+          "score": -0.005505,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18083,
+          "gene": "ZNF510",
+          "score": -0.184205,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18042,
+          "gene": "ZNF44",
+          "score": -0.11366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18107,
+          "gene": "ZNF543",
+          "score": 0.37438,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18070,
+          "gene": "ZNF488",
+          "score": 0.039261,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18064,
+          "gene": "ZNF48",
+          "score": 0.0807835,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18134,
+          "gene": "ZNF571",
+          "score": 0.077155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18142,
+          "gene": "ZNF579",
+          "score": 0.026342,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18067,
+          "gene": "ZNF484",
+          "score": -0.059251,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18060,
+          "gene": "ZNF470",
+          "score": -0.1913,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18127,
+          "gene": "ZNF565",
+          "score": -0.140035,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18144,
+          "gene": "ZNF581",
+          "score": -0.0562255,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18153,
+          "gene": "ZNF592",
+          "score": 0.0864995,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18082,
+          "gene": "ZNF507",
+          "score": 0.037163,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18157,
+          "gene": "ZNF596",
+          "score": 0.376185,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18078,
+          "gene": "ZNF501",
+          "score": -0.0899685,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18066,
+          "gene": "ZNF483",
+          "score": 0.1860085,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18052,
+          "gene": "ZNF451",
+          "score": -0.06424,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18122,
+          "gene": "ZNF560",
+          "score": 0.0112985,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18146,
+          "gene": "ZNF583",
+          "score": -0.05593,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18058,
+          "gene": "ZNF468",
+          "score": -0.0068665,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18125,
+          "gene": "ZNF563",
+          "score": 0.168275,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18147,
+          "gene": "ZNF584",
+          "score": 0.337285,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18160,
+          "gene": "ZNF599",
+          "score": -0.1666685,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18100,
+          "gene": "ZNF529",
+          "score": -0.0121575,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18152,
+          "gene": "ZNF589",
+          "score": -0.1166215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18159,
+          "gene": "ZNF598",
+          "score": -0.152225,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18118,
+          "gene": "ZNF556",
+          "score": 0.05136365,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18123,
+          "gene": "ZNF561",
+          "score": 0.29338,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18151,
+          "gene": "ZNF587",
+          "score": 0.052138,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18129,
+          "gene": "ZNF567",
+          "score": 0.03971,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18099,
+          "gene": "ZNF528",
+          "score": 0.037025,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18108,
+          "gene": "ZNF544",
+          "score": -0.0599985,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18092,
+          "gene": "ZNF518A",
+          "score": -0.2550815,
+          "hit": 0,
+          "round": 3
         }
       ],
       "queried_history": [
@@ -4920,896 +5816,1792 @@
           "gene": "ZNF655",
           "score": -0.1833125,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18233,
           "gene": "ZNF703",
           "score": -0.0852,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18197,
           "gene": "ZNF658",
           "score": 0.044175,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18165,
           "gene": "ZNF608",
           "score": 0.2987305,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18173,
           "gene": "ZNF618",
           "score": -0.190475,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18162,
           "gene": "ZNF605",
           "score": -0.13111839,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18215,
           "gene": "ZNF681",
           "score": 0.128045,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18278,
           "gene": "ZNF771",
           "score": -0.149708,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18219,
           "gene": "ZNF687",
           "score": -0.262595,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18216,
           "gene": "ZNF682",
           "score": -0.199155,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18166,
           "gene": "ZNF609",
           "score": -0.32101,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18163,
           "gene": "ZNF606",
           "score": 0.069635,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18257,
           "gene": "ZNF730",
           "score": -0.06505,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18221,
           "gene": "ZNF689",
           "score": -0.02664,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18192,
           "gene": "ZNF649",
           "score": -0.091537,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18230,
           "gene": "ZNF70",
           "score": -0.0901975,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18206,
           "gene": "ZNF671",
           "score": 0.09395745,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18164,
           "gene": "ZNF607",
           "score": -0.0026525,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18222,
           "gene": "ZNF69",
           "score": -0.1912095,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18232,
           "gene": "ZNF701",
           "score": -0.391055,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18274,
           "gene": "ZNF766",
           "score": 0.07028355,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18262,
           "gene": "ZNF74",
           "score": -0.443155,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18218,
           "gene": "ZNF684",
           "score": 0.113969,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18212,
           "gene": "ZNF678",
           "score": 0.1374395,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18205,
           "gene": "ZNF670",
           "score": 0.289355,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18176,
           "gene": "ZNF621",
           "score": 0.086152,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18236,
           "gene": "ZNF705B",
           "score": -0.059855,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18270,
           "gene": "ZNF76",
           "score": 0.013145,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18175,
           "gene": "ZNF620",
           "score": -0.16560645,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18263,
           "gene": "ZNF740",
           "score": 0.1171905,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18172,
           "gene": "ZNF616",
           "score": 0.106625,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18268,
           "gene": "ZNF75A",
           "score": 0.2089455,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18266,
           "gene": "ZNF749",
           "score": 0.027157,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18282,
           "gene": "ZNF775",
           "score": -0.446395,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18264,
           "gene": "ZNF746",
           "score": 0.39508,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18211,
           "gene": "ZNF677",
           "score": -0.044635,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18195,
           "gene": "ZNF654",
           "score": -0.09401,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18237,
           "gene": "ZNF705D",
           "score": -0.2711,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18271,
           "gene": "ZNF761",
           "score": -0.29709,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18225,
           "gene": "ZNF695",
           "score": -0.0494725,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18254,
           "gene": "ZNF727",
           "score": -0.08205,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18188,
           "gene": "ZNF641",
           "score": -0.1801195,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18182,
           "gene": "ZNF627",
           "score": 0.006615,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18227,
           "gene": "ZNF697",
           "score": 0.33112,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18243,
           "gene": "ZNF709",
           "score": 0.0628615,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18226,
           "gene": "ZNF696",
           "score": -0.005585,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18289,
           "gene": "ZNF782",
           "score": -0.07841,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18279,
           "gene": "ZNF772",
           "score": -0.227325,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18272,
           "gene": "ZNF764",
           "score": 0.14892,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18287,
           "gene": "ZNF780B",
           "score": -0.15895,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18235,
           "gene": "ZNF705A",
           "score": 0.0939665,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18250,
           "gene": "ZNF717",
           "score": 0.251,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18168,
           "gene": "ZNF611",
           "score": 0.28251,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18194,
           "gene": "ZNF653",
           "score": -0.146895,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18199,
           "gene": "ZNF662",
           "score": -0.1954055,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18239,
           "gene": "ZNF705G",
           "score": 0.05468,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18260,
           "gene": "ZNF736",
           "score": -0.014509,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18259,
           "gene": "ZNF735",
           "score": 0.02091,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18198,
           "gene": "ZNF660",
           "score": -0.12729,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18193,
           "gene": "ZNF652",
           "score": 0.1074805,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18203,
           "gene": "ZNF668",
           "score": 0.0942455,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18187,
           "gene": "ZNF639",
           "score": -0.478455,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18207,
           "gene": "ZNF672",
           "score": 0.091869,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18231,
           "gene": "ZNF700",
           "score": 0.070234,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18213,
           "gene": "ZNF679",
           "score": -0.029394,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18242,
           "gene": "ZNF708",
           "score": 0.0181625,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18247,
           "gene": "ZNF713",
           "score": 0.15265,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18184,
           "gene": "ZNF629",
           "score": 0.3354,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18234,
           "gene": "ZNF704",
           "score": -0.093379,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18284,
           "gene": "ZNF777",
           "score": 0.1705515,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18283,
           "gene": "ZNF776",
           "score": -0.00751,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18258,
           "gene": "ZNF732",
           "score": 0.1017415,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18256,
           "gene": "ZNF729",
           "score": 0.012581,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18273,
           "gene": "ZNF765",
           "score": -0.389585,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18189,
           "gene": "ZNF644",
           "score": 0.280492,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18265,
           "gene": "ZNF747",
           "score": -0.00157,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18229,
           "gene": "ZNF7",
           "score": -0.0977735,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18228,
           "gene": "ZNF699",
           "score": -0.1837,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18202,
           "gene": "ZNF667",
           "score": 0.03447775,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18240,
           "gene": "ZNF706",
           "score": -0.02961,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18245,
           "gene": "ZNF710",
           "score": 0.09547,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18285,
           "gene": "ZNF778",
           "score": 0.1257655,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18171,
           "gene": "ZNF615",
           "score": 0.1941805,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18209,
           "gene": "ZNF675",
           "score": 0.31613,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18276,
           "gene": "ZNF77",
           "score": 0.158275,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18249,
           "gene": "ZNF716",
           "score": 0.006445,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18255,
           "gene": "ZNF728",
           "score": 0.1207145,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18177,
           "gene": "ZNF622",
           "score": 0.085554,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18186,
           "gene": "ZNF638",
           "score": -0.156016,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18281,
           "gene": "ZNF774",
           "score": 0.0492925,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18180,
           "gene": "ZNF625",
           "score": 0.2007245,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18174,
           "gene": "ZNF619",
           "score": 0.227995,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18178,
           "gene": "ZNF623",
           "score": -0.209705,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18210,
           "gene": "ZNF676",
           "score": -0.0869881,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18253,
           "gene": "ZNF726",
           "score": 0.00325,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18246,
           "gene": "ZNF711",
           "score": 0.1338245,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18280,
           "gene": "ZNF773",
           "score": 0.130544,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18244,
           "gene": "ZNF71",
           "score": -0.189513,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18248,
           "gene": "ZNF714",
           "score": 0.20327,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18204,
           "gene": "ZNF669",
           "score": 0.0332529,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18183,
           "gene": "ZNF628",
           "score": 0.02386,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18191,
           "gene": "ZNF648",
           "score": 0.239318,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18238,
           "gene": "ZNF705E",
           "score": -0.256575,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18214,
           "gene": "ZNF680",
           "score": -0.0800905,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18169,
           "gene": "ZNF613",
           "score": 0.04389,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18208,
           "gene": "ZNF674",
           "score": 0.011945,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18181,
           "gene": "ZNF626",
           "score": -0.145603,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18251,
           "gene": "ZNF718",
           "score": -0.0575795,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18201,
           "gene": "ZNF665",
           "score": -0.03955195,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18224,
           "gene": "ZNF692",
           "score": 0.29731,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18190,
           "gene": "ZNF646",
           "score": 0.1066445,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18269,
           "gene": "ZNF75D",
           "score": 0.1355,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18277,
           "gene": "ZNF770",
           "score": -0.0537535,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18288,
           "gene": "ZNF781",
           "score": -0.31094,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18217,
           "gene": "ZNF683",
           "score": 0.0220375,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18167,
           "gene": "ZNF610",
           "score": 0.12294,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18170,
           "gene": "ZNF614",
           "score": -0.05491,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18286,
           "gene": "ZNF780A",
           "score": 0.1124055,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18252,
           "gene": "ZNF721",
           "score": 0.26879,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18261,
           "gene": "ZNF737",
           "score": 0.216225,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18241,
           "gene": "ZNF707",
           "score": 0.37715,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18267,
           "gene": "ZNF750",
           "score": 0.031711,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18275,
           "gene": "ZNF768",
           "score": 0.01482,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18179,
           "gene": "ZNF624",
           "score": -0.127621,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18200,
           "gene": "ZNF664",
           "score": 0.0808805,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18220,
           "gene": "ZNF688",
           "score": -0.0863065,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18223,
           "gene": "ZNF691",
           "score": -0.1299145,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18185,
           "gene": "ZNF630",
           "score": 0.08269,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 18148,
+          "gene": "ZNF585A",
+          "score": -0.029175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18096,
+          "gene": "ZNF524",
+          "score": 0.1740205,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18115,
+          "gene": "ZNF552",
+          "score": -0.18224,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18050,
+          "gene": "ZNF449",
+          "score": 0.02156985,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18077,
+          "gene": "ZNF500",
+          "score": 0.128354,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18036,
+          "gene": "ZNF431",
+          "score": 0.181045,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18075,
+          "gene": "ZNF496",
+          "score": 0.13378,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18039,
+          "gene": "ZNF436",
+          "score": -0.22501,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18101,
+          "gene": "ZNF530",
+          "score": 0.111831,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18061,
+          "gene": "ZNF471",
+          "score": 0.16659,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18085,
+          "gene": "ZNF511-PRAP1",
+          "score": 0.101215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18113,
+          "gene": "ZNF550",
+          "score": 0.0015315,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18131,
+          "gene": "ZNF569",
+          "score": -0.2065345,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18140,
+          "gene": "ZNF577",
+          "score": 0.352155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18103,
+          "gene": "ZNF534",
+          "score": -0.1037915,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18046,
+          "gene": "ZNF443",
+          "score": -0.1002155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18071,
+          "gene": "ZNF490",
+          "score": -0.0520515,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18111,
+          "gene": "ZNF548",
+          "score": 0.14674175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18048,
+          "gene": "ZNF445",
+          "score": 0.185425,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18084,
+          "gene": "ZNF511",
+          "score": -0.087807,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18145,
+          "gene": "ZNF582",
+          "score": 0.053413,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18069,
+          "gene": "ZNF486",
+          "score": -0.01275,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18073,
+          "gene": "ZNF492",
+          "score": 0.2519605,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18087,
+          "gene": "ZNF512B",
+          "score": -0.13953,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18105,
+          "gene": "ZNF540",
+          "score": 0.096929,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18089,
+          "gene": "ZNF514",
+          "score": 0.0049065,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18040,
+          "gene": "ZNF438",
+          "score": 0.094816,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18133,
+          "gene": "ZNF570",
+          "score": 0.00226,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18045,
+          "gene": "ZNF442",
+          "score": 0.1677725,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18055,
+          "gene": "ZNF461",
+          "score": -0.26366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18091,
+          "gene": "ZNF517",
+          "score": 0.071871,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18138,
+          "gene": "ZNF575",
+          "score": -0.32484,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18104,
+          "gene": "ZNF536",
+          "score": 0.201145,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18155,
+          "gene": "ZNF594",
+          "score": -0.02139,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18136,
+          "gene": "ZNF573",
+          "score": -0.1773585,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18110,
+          "gene": "ZNF547",
+          "score": 0.0528285,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18056,
+          "gene": "ZNF462",
+          "score": -0.04815,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18161,
+          "gene": "ZNF600",
+          "score": -0.13736,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18079,
+          "gene": "ZNF502",
+          "score": 0.009245,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18038,
+          "gene": "ZNF433",
+          "score": -0.176507,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18034,
+          "gene": "ZNF43",
+          "score": -0.1845355,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18141,
+          "gene": "ZNF578",
+          "score": -0.15319,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18068,
+          "gene": "ZNF485",
+          "score": 0.271345,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18128,
+          "gene": "ZNF566",
+          "score": -0.3362,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18054,
+          "gene": "ZNF460",
+          "score": -0.092895,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18081,
+          "gene": "ZNF506",
+          "score": -0.113433,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18057,
+          "gene": "ZNF467",
+          "score": 0.072695,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18051,
+          "gene": "ZNF45",
+          "score": 0.1424945,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18044,
+          "gene": "ZNF441",
+          "score": -0.164674,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18049,
+          "gene": "ZNF446",
+          "score": -0.061245,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18086,
+          "gene": "ZNF512",
+          "score": -0.0526845,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18158,
+          "gene": "ZNF597",
+          "score": -0.39098,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18102,
+          "gene": "ZNF532",
+          "score": 0.0522465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18106,
+          "gene": "ZNF541",
+          "score": -0.18417965,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18156,
+          "gene": "ZNF595",
+          "score": -0.025711,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18126,
+          "gene": "ZNF564",
+          "score": 0.1820195,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18132,
+          "gene": "ZNF57",
+          "score": 0.103895,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18097,
+          "gene": "ZNF526",
+          "score": 0.137245,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18065,
+          "gene": "ZNF480",
+          "score": 0.24194,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18043,
+          "gene": "ZNF440",
+          "score": -0.087465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18035,
+          "gene": "ZNF430",
+          "score": 0.08786,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18137,
+          "gene": "ZNF574",
+          "score": 0.16361,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18095,
+          "gene": "ZNF521",
+          "score": 0.08589,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18090,
+          "gene": "ZNF516",
+          "score": 0.25173,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18124,
+          "gene": "ZNF562",
+          "score": -0.3011635,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18062,
+          "gene": "ZNF473",
+          "score": 0.0156455,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18088,
+          "gene": "ZNF513",
+          "score": 0.01218,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18130,
+          "gene": "ZNF568",
+          "score": 0.0717735,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18080,
+          "gene": "ZNF503",
+          "score": 0.23489,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18047,
+          "gene": "ZNF444",
+          "score": -0.0704355,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18117,
+          "gene": "ZNF555",
+          "score": 0.145655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18135,
+          "gene": "ZNF572",
+          "score": 0.041181,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18114,
+          "gene": "ZNF551",
+          "score": 0.0350655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18098,
+          "gene": "ZNF527",
+          "score": 0.0058345,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18063,
+          "gene": "ZNF479",
+          "score": 0.0278175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18074,
+          "gene": "ZNF493",
+          "score": 0.009985,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18093,
+          "gene": "ZNF518B",
+          "score": 0.31276,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18094,
+          "gene": "ZNF519",
+          "score": -0.0857705,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18112,
+          "gene": "ZNF549",
+          "score": 0.22809,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18076,
+          "gene": "ZNF497",
+          "score": 0.000715,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18119,
+          "gene": "ZNF557",
+          "score": 0.264625,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18041,
+          "gene": "ZNF439",
+          "score": -0.237145,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18150,
+          "gene": "ZNF586",
+          "score": -0.198565,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18059,
+          "gene": "ZNF469",
+          "score": 0.051955,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18149,
+          "gene": "ZNF585B",
+          "score": -0.183071,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18121,
+          "gene": "ZNF559",
+          "score": 0.19544,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18116,
+          "gene": "ZNF554",
+          "score": -0.250545,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18037,
+          "gene": "ZNF432",
+          "score": -0.0355025,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18120,
+          "gene": "ZNF558",
+          "score": 0.006585,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18139,
+          "gene": "ZNF576",
+          "score": 0.389825,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18053,
+          "gene": "ZNF454",
+          "score": 0.11075185,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18154,
+          "gene": "ZNF593",
+          "score": -0.0711965,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18072,
+          "gene": "ZNF491",
+          "score": -0.035655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18143,
+          "gene": "ZNF580",
+          "score": 0.234024,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18109,
+          "gene": "ZNF546",
+          "score": -0.005505,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18083,
+          "gene": "ZNF510",
+          "score": -0.184205,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18042,
+          "gene": "ZNF44",
+          "score": -0.11366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18107,
+          "gene": "ZNF543",
+          "score": 0.37438,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18070,
+          "gene": "ZNF488",
+          "score": 0.039261,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18064,
+          "gene": "ZNF48",
+          "score": 0.0807835,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18134,
+          "gene": "ZNF571",
+          "score": 0.077155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18142,
+          "gene": "ZNF579",
+          "score": 0.026342,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18067,
+          "gene": "ZNF484",
+          "score": -0.059251,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18060,
+          "gene": "ZNF470",
+          "score": -0.1913,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18127,
+          "gene": "ZNF565",
+          "score": -0.140035,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18144,
+          "gene": "ZNF581",
+          "score": -0.0562255,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18153,
+          "gene": "ZNF592",
+          "score": 0.0864995,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18082,
+          "gene": "ZNF507",
+          "score": 0.037163,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18157,
+          "gene": "ZNF596",
+          "score": 0.376185,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18078,
+          "gene": "ZNF501",
+          "score": -0.0899685,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18066,
+          "gene": "ZNF483",
+          "score": 0.1860085,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18052,
+          "gene": "ZNF451",
+          "score": -0.06424,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18122,
+          "gene": "ZNF560",
+          "score": 0.0112985,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18146,
+          "gene": "ZNF583",
+          "score": -0.05593,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18058,
+          "gene": "ZNF468",
+          "score": -0.0068665,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18125,
+          "gene": "ZNF563",
+          "score": 0.168275,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18147,
+          "gene": "ZNF584",
+          "score": 0.337285,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18160,
+          "gene": "ZNF599",
+          "score": -0.1666685,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18100,
+          "gene": "ZNF529",
+          "score": -0.0121575,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18152,
+          "gene": "ZNF589",
+          "score": -0.1166215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18159,
+          "gene": "ZNF598",
+          "score": -0.152225,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18118,
+          "gene": "ZNF556",
+          "score": 0.05136365,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18123,
+          "gene": "ZNF561",
+          "score": 0.29338,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18151,
+          "gene": "ZNF587",
+          "score": 0.052138,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18129,
+          "gene": "ZNF567",
+          "score": 0.03971,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18099,
+          "gene": "ZNF528",
+          "score": 0.037025,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18108,
+          "gene": "ZNF544",
+          "score": -0.0599985,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18092,
+          "gene": "ZNF518A",
+          "score": -0.2550815,
+          "hit": 0,
+          "round": 3
         }
       ]
     }

```
