# Change Record — candidate_5

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Carnevale22_Adenosine/run-2/best/current/harness
Generated at: 2026-04-30T07:19:28.267349

## Files Changed

- model.py: modified (added=59, deleted=60, delta=-1)
- outputs/metrics.json: modified (added=2382, deleted=590, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -42,84 +42,83 @@
     selected_indices = {h['candidate_index'] for h in history}
     available_indices = [i for i in candidate_indices if i not in selected_indices]
     
-    # If no history (first round), use random selection with some diversity
+    # If no history (first round), use random selection
     if not history:
-        # Simple random sampling for the first batch
         selected = rng.choice(available_indices, size=min(batch_size, len(available_indices)), replace=False)
         return selected.tolist()
     
-    # Build statistics from history
-    # Track mean score and count for each candidate
-    scores = {}
-    counts = {}
+    # Thompson Sampling with Beta-Bernoulli model
+    # Model hit (extreme outcome) as Bernoulli event with Beta prior
+    # Beta(alpha, beta) where:
+    # - alpha = 1 + number_of_hits (Jeffreys prior + successes)
+    # - beta = 1 + number_of_trials - number_of_hits (Jeffreys prior + failures)
+    
+    # Track hits and trials for each candidate
+    hits = {}
+    trials = {}
     
     for h in history:
         idx = h['candidate_index']
-        score = h['score']
-        if idx not in scores:
-            scores[idx] = 0.0
-            counts[idx] = 0
-        scores[idx] += score
-        counts[idx] += 1
+        is_hit = h.get('hit', 0)
+        
+        if idx not in hits:
+            hits[idx] = 0
+            trials[idx] = 0
+        
+        hits[idx] += is_hit
+        trials[idx] += 1
     
-    # Calculate mean scores
-    mean_scores = {idx: scores[idx] / counts[idx] for idx in scores}
+    # Calculate gene family hit rates for prior strengthening
+    # Genes from families with high hit rates get boosted priors
+    family_hits = {}
+    family_trials = {}
     
-    # Calculate gene family bonuses based on historical extreme effects
-    # Genes from families with high absolute scores get a bonus
-    family_scores = {}
-    family_counts = {}
+    for idx in hits:
+        gene_name = candidates[idx].get('gene', '')
+        family = gene_name.split('_')[0].split('-')[0]
+        
+        if family not in family_hits:
+            family_hits[family] = 0
+            family_trials[family] = 0
+        
+        family_hits[family] += hits[idx]
+        family_trials[family] += trials[idx]
     
-    for idx, score in mean_scores.items():
-        gene_name = candidates[idx].get('gene', '')
-        # Extract gene family prefix (e.g., "ZNF" from "ZNF123", "ATP" from "ATP6V0D1")
-        family = gene_name.split('_')[0]  # Handle cases like "ZNF816-ZNF321P"
-        # Take first part before any hyphen
-        family = family.split('-')[0]
-        
-        if family not in family_scores:
-            family_scores[family] = 0.0
-            family_counts[family] = 0
-        family_scores[family] += abs(score)
-        family_counts[family] += 1
-    
-    # Calculate average absolute score per family
-    family_avg_abs = {}
-    for family in family_scores:
-        family_avg_abs[family] = family_scores[family] / family_counts[family]
-    
-    # UCB algorithm: balance mean reward vs exploration bonus vs family bonus
-    total_pulls = len(history)
-    ucb_scores = []
+    # Sample from posterior for each available candidate
+    sampled_probs = []
     
     for idx in available_indices:
         gene_name = candidates[idx].get('gene', '')
         family = gene_name.split('_')[0].split('-')[0]
         
-        if idx in mean_scores:
-            # Exploitation term: absolute mean score (prioritize extreme effects)
-            # Since hits are defined by large deviations in either direction
-            exploitation = abs(mean_scores[idx])
-            # Exploration term: uncertainty bonus with tuned constant and epsilon regularization
-            # Use a slightly higher exploration constant (2.5 vs 2.0) to encourage more exploration
-            # Add small epsilon to prevent division by zero and handle low-count candidates
-            exploration = np.sqrt(2.5 * np.log(total_pulls + 1) / (counts[idx] + 1e-6))
-            # Family bonus: prioritize genes from families with historically extreme effects
-            # Weight: 0.3 * family_avg_abs (moderate influence, tuned empirically)
-            family_bonus = 0.3 * family_avg_abs.get(family, 0.0)
-            ucb = exploitation + exploration + family_bonus
+        if idx in hits:
+            # Candidate has been tried before
+            # Use Beta posterior: Beta(1 + hits, 1 + trials - hits)
+            alpha = 1 + hits[idx]
+            beta = 1 + trials[idx] - hits[idx]
         else:
-            # Never-seen candidates get high priority for exploration
-            # But also consider family bonus for never-seen candidates
-            family_bonus = 0.3 * family_avg_abs.get(family, 0.0)
-            ucb = float('inf') + family_bonus
-        ucb_scores.append((ucb, idx))
+            # Never-seen candidate - use informed prior based on family
+            if family in family_hits and family_trials[family] > 0:
+                # Use family statistics to create informed prior
+                # More conservative: weight family evidence less for never-seen
+                family_hit_rate = family_hits[family] / family_trials[family]
+                # Scale down family influence for never-seen (pseudo-counts approach)
+                alpha = 1 + 0.5 * family_hits[family]
+                beta = 1 + 0.5 * (family_trials[family] - family_hits[family])
+            else:
+                # No family info - use uniform Jeffreys prior
+                alpha = 1
+                beta = 1
+        
+        # Sample from Beta posterior
+        sampled_prob = rng.beta(alpha, beta)
+        sampled_probs.append((sampled_prob, idx))
     
-    # Sort by UCB score (descending) and select top candidates
-    ucb_scores.sort(reverse=True)
-    selected = [idx for _, idx in ucb_scores[:batch_size]]
+    # Sort by sampled probability (descending) and select top candidates
+    sampled_probs.sort(reverse=True)
+    selected = [idx for _, idx in sampled_probs[:batch_size]]
     
-    # If we don't have enough high-UCB candidates, fill with random unexplored ones
+    # If we don't have enough candidates, fill with random unexplored ones
     if len(selected) < batch_size:
         remaining = [idx for idx in available_indices if idx not in selected]
         needed = batch_size - len(selected)

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18861,
-      "rounds": 4,
+      "rounds": 5,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 384,
-      "baseline_total_hits": 23,
+      "baseline_total_queries": 512,
+      "baseline_total_hits": 34,
       "delta_queries": 128,
-      "delta_hits": 11,
-      "total_queries": 512,
-      "total_hits": 34,
+      "delta_hits": 3,
+      "total_queries": 640,
+      "total_hits": 37,
       "top_k": 943,
       "hit_curve": {
         "queries": [
-          384,
-          512
+          512,
+          640
         ],
         "hits": [
-          23,
-          34
+          34,
+          37
         ]
       },
-      "auc": 3648.0,
-      "auc_normalized": 0.007555673382820784,
-      "ncg": 0.2941334834709887,
+      "auc": 4544.0,
+      "auc_normalized": 0.00752916224814422,
+      "ncg": 0.2992533768830617,
       "round_details": [
         {
-          "round": 3,
+          "round": 4,
           "selected_count": 128,
-          "hits": 11,
-          "cumulative_hits": 34,
-          "precision_at_batch": 0.0859375,
+          "hits": 3,
+          "cumulative_hits": 37,
+          "precision_at_batch": 0.0234375,
           "selected": [
-            "ZNF608",
-            "ZNF607",
-            "ZNF606",
-            "ZNF605",
-            "ZNF600",
-            "ZNF599",
-            "ZNF598",
-            "ZNF597",
-            "ZNF596",
-            "ZNF595",
-            "ZNF594",
-            "ZNF593",
-            "ZNF592",
-            "ZNF589",
-            "ZNF587B",
-            "ZNF587",
-            "ZNF586",
-            "ZNF585B",
-            "ZNF585A",
-            "ZNF584",
-            "ZNF583",
-            "ZNF582",
-            "ZNF581",
-            "ZNF580",
-            "ZNF579",
-            "ZNF578",
-            "ZNF577",
-            "ZNF576",
-            "ZNF575",
-            "ZNF574",
-            "ZNF573",
-            "ZNF572",
-            "ZNF571",
-            "ZNF570",
-            "ZNF57",
-            "ZNF569",
-            "ZNF568",
-            "ZNF567",
-            "ZNF566",
-            "ZNF565",
-            "ZNF564",
-            "ZNF563",
-            "ZNF562",
-            "ZNF561",
-            "ZNF560",
-            "ZNF559-ZNF177",
-            "ZNF559",
-            "ZNF558",
-            "ZNF557",
-            "ZNF556",
-            "ZNF555",
-            "ZNF554",
-            "ZNF552",
-            "ZNF551",
-            "ZNF550",
-            "ZNF549",
-            "ZNF548",
-            "ZNF547",
-            "ZNF546",
-            "ZNF544",
-            "ZNF543",
-            "ZNF541",
-            "ZNF540",
-            "ZNF536",
-            "ZNF534",
-            "ZNF532",
-            "ZNF530",
-            "ZNF529",
-            "ZNF528",
-            "ZNF527",
-            "ZNF526",
-            "ZNF524",
-            "ZNF521",
-            "ZNF519",
-            "ZNF518B",
-            "ZNF518A",
-            "ZNF517",
-            "ZNF516",
-            "ZNF514",
-            "ZNF513",
-            "ZNF512B",
-            "ZNF512",
-            "ZNF511",
-            "ZNF510",
-            "ZNF507",
-            "ZNF506",
-            "ZNF503",
-            "ZNF502",
-            "ZNF501",
-            "ZNF500",
-            "ZNF497",
-            "ZNF496",
-            "ZNF493",
-            "ZNF492",
-            "ZNF491",
-            "ZNF490",
-            "ZNF488",
-            "ZNF486",
-            "ZNF485",
-            "ZNF484",
-            "ZNF483",
-            "ZNF480",
-            "ZNF48",
-            "ZNF479",
-            "ZNF473",
-            "ZNF471",
-            "ZNF470",
-            "ZNF469",
-            "ZNF468",
-            "ZNF467",
-            "ZNF462",
-            "ZNF461",
-            "ZNF460",
-            "ZNF454",
-            "ZNF451",
-            "ZNF45",
-            "ZNF449",
-            "ZNF446",
-            "ZNF445",
-            "ZNF444",
-            "ZNF443",
-            "ZNF442",
-            "ZNF441",
-            "ZNF440",
-            "ZNF44",
-            "ZNF439",
-            "ZNF438",
-            "ZNF436"
+            "ARMCX5",
+            "DENND2D",
+            "VAC14",
+            "PHF21A",
+            "ZNF22",
+            "C9orf92",
+            "OR5A2",
+            "OTOL1",
+            "ITPR3",
+            "STAM2",
+            "KCTD2",
+            "FBXO42",
+            "SPAG17",
+            "FBXO22",
+            "AKAP5",
+            "CLPTM1L",
+            "GMPR",
+            "BCL2L12",
+            "GSTO2",
+            "DEFB134",
+            "IL2RG",
+            "ABCA7",
+            "CTLA4",
+            "NOXRED1",
+            "ST3GAL5",
+            "EEF1D",
+            "UBE2QL1",
+            "BLK",
+            "ECE1",
+            "ALOX15",
+            "NonTarget.CTRL194",
+            "TBK1",
+            "AJUBA",
+            "OR10G3",
+            "PCDHA7",
+            "IRF1",
+            "SLC36A1",
+            "H4C13",
+            "C19orf25",
+            "GLTPD2",
+            "TMCO2",
+            "DSC3",
+            "TWNK",
+            "POLR3G",
+            "RBBP7",
+            "CMAS",
+            "ATP1A4",
+            "PHF20",
+            "EBF2",
+            "FIGNL2",
+            "ACSM6",
+            "PROKR2",
+            "PDGFC",
+            "RFX2",
+            "ARK2N",
+            "ZNF177",
+            "ETV7",
+            "HSPB7",
+            "TMEM263",
+            "IGIP",
+            "PRTN3",
+            "TMEM94",
+            "PTPN23",
+            "FAM20B",
+            "NonTarget.CTRL3",
+            "CD300C",
+            "MCRS1",
+            "CTHRC1",
+            "TMEM132A",
+            "TAAR1",
+            "LY9",
+            "PRR29",
+            "CCNY",
+            "RIOK2",
+            "SLC22A18",
+            "PLP1",
+            "PPM1K",
+            "POFUT1",
+            "OR13C3",
+            "CGNL1",
+            "COX6A1",
+            "ASPA",
+            "CNIH2",
+            "SFXN4",
+            "CYP8B1",
+            "CSKMT",
+            "SASH3",
+            "MRPS5",
+            "TESK2",
+            "PPP1R26",
+            "SLC25A14",
+            "MEDAG",
+            "PTAR1",
+            "RIDA",
+            "SPIRE2",
+            "B3GNTL1",
+            "GRIFIN",
+            "HBG2",
+            "BUB3",
+            "PIEZO2",
+            "ENY2",
+            "SPINT4",
+            "H2AP",
+            "AQR",
+            "SYNJ2",
+            "PDE8A",
+            "YY1",
+            "TMEM62",
+            "CCDC166",
+            "CYTIP",
+            "CCM2L",
+            "WDR88",
+            "SLC10A1",
+            "PPP1R35",
+            "ZNF419",
+            "INSL4",
+            "PLET1",
+            "SNUPN",
+            "MED6",
+            "CASKIN2",
+            "CCR5",
+            "PXMP4",
+            "OCEL1",
+            "AAMP",
+            "DHRS4L2",
+            "HYAL4",
+            "PPP1R8",
+            "SLC34A3"
           ],
           "selected_scores": [
-            0.12688,
-            0.072299,
-            0.043496,
-            0.013934,
-            0.083798,
-            -0.26203,
-            0.15653,
-            -0.12037,
-            -0.19227,
-            0.073366,
-            0.37002,
-            0.031148,
-            -0.26199,
-            -0.47131,
-            -0.0036534,
-            -0.016915,
-            0.050891,
-            -0.10684,
-            0.11733,
-            -0.13782,
-            0.18765,
-            -0.015977,
-            -0.051373,
-            0.27375,
-            0.083199,
-            -0.28973,
-            -0.28492,
-            -0.10189,
-            0.29304,
-            0.082974,
-            0.01173,
-            0.1097,
-            -0.29187,
-            -0.048904,
-            0.054145,
-            -0.14599,
-            -0.084297,
-            0.1728,
-            0.11916,
-            0.046647,
-            0.043877,
-            -0.19572,
-            0.0037033,
-            -0.2972,
-            -0.1161,
-            -0.035171,
-            0.12576,
-            0.20418,
-            -0.41338,
-            0.12917,
-            -0.075628,
-            -0.047888,
-            0.2297,
-            -0.060688,
-            -0.025795,
-            -0.016808,
-            -0.049671,
-            0.10727,
-            -0.013879,
-            -0.012014,
-            0.12739,
-            -0.10405,
-            0.20023,
-            0.20535,
-            -0.0011927,
-            -0.065848,
-            -0.092644,
-            -0.28892,
-            0.070663,
-            -0.04451,
-            -0.23212,
-            -0.13637,
-            -0.15231,
-            -0.088078,
-            -0.036369,
-            -0.016586,
-            0.1061,
-            -0.15165,
-            0.15989,
-            -0.075366,
-            0.12756,
-            -0.13474,
-            0.31078,
-            -0.1862,
-            0.05839,
-            0.49766,
-            0.13902,
-            0.083177,
-            0.16282,
-            -0.040884,
-            0.0020353,
-            -0.42909,
-            -0.34255,
-            0.53004,
-            -0.20654,
-            0.30996,
-            0.30129,
-            -0.35845,
-            -0.074194,
-            -0.15525,
-            -0.064107,
-            0.079031,
-            0.040223,
-            -0.18857,
-            0.11782,
-            -0.10068,
-            0.13604,
-            -0.051998,
-            0.26556,
-            0.21092,
-            -0.23175,
-            -0.01324,
-            -0.11387,
-            0.15656,
-            0.1581,
-            0.18164,
-            0.0080712,
-            0.44891,
-            -0.21726,
-            0.10247,
-            0.017261,
-            0.35702,
-            -0.028326,
-            -0.045372,
-            0.051431,
-            -0.074874,
-            0.051488,
-            0.33876
+            0.079172,
+            0.052524,
+            -0.070281,
+            -0.18496,
+            0.099706,
+            -0.33098,
+            0.23934,
+            0.042275,
+            -0.18851,
+            -0.21057,
+            -0.059414,
+            0.29237,
+            0.017603,
+            0.1491,
+            -0.16348,
+            0.054154,
+            -0.045694,
+            0.067577,
+            0.047835,
+            0.11669,
+            0.25489,
+            -0.086483,
+            0.052611,
+            -0.21094,
+            -0.071085,
+            -0.056527,
+            -0.26317,
+            -0.011389,
+            -0.078588,
+            -0.0073389,
+            -0.0068882,
+            0.064703,
+            -0.12662,
+            -0.19135,
+            -0.16991,
+            -0.057996,
+            0.0062899,
+            -0.10299,
+            -0.16354,
+            -0.30143,
+            -0.13777,
+            0.003556,
+            0.036641,
+            -0.062667,
+            0.11243,
+            0.0097112,
+            0.10274,
+            0.12324,
+            0.019827,
+            -0.157,
+            0.22588,
+            -0.22557,
+            0.35243,
+            0.055279,
+            -0.019368,
+            -0.42213,
+            0.20274,
+            0.076501,
+            -0.047598,
+            0.041687,
+            -0.06259,
+            0.040703,
+            0.073748,
+            -0.23095,
+            0.10059,
+            -0.2057,
+            -0.011183,
+            -0.20672,
+            0.096844,
+            0.14204,
+            0.018889,
+            0.12653,
+            -0.44482,
+            0.052317,
+            0.20263,
+            -0.30074,
+            0.18101,
+            0.13927,
+            0.082765,
+            0.19489,
+            0.1119,
+            -0.22456,
+            -0.14124,
+            0.088048,
+            0.043215,
+            -0.3039,
+            0.12246,
+            0.1275,
+            -0.036482,
+            0.17773,
+            0.0046482,
+            0.064143,
+            -0.26585,
+            -0.25047,
+            -0.017158,
+            0.0625085,
+            -0.18217,
+            0.16415,
+            0.21887,
+            0.0043525,
+            -0.21481,
+            0.23442,
+            0.051486,
+            0.11593,
+            0.035979,
+            -0.044873,
+            -0.10208,
+            0.096311,
+            -0.034049,
+            -0.0025065,
+            -0.081227,
+            -0.15478,
+            -0.15369,
+            -0.08237,
+            -0.041417,
+            -0.08216,
+            -0.08709,
+            0.01426,
+            -0.1367,
+            -0.070451,
+            0.044152,
+            0.16473,
+            -0.083103,
+            -0.1705,
+            -0.13034,
+            -0.16579,
+            -0.19875,
+            -0.23035
           ],
           "selected_hits": [
             0,
@@ -311,6 +311,48 @@
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
             1,
             0,
             0,
@@ -331,24 +373,6 @@
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
@@ -386,49 +410,25 @@
             0,
             0,
             0,
-            1,
-            0,
-            0,
-            0,
-            0,
-            0,
-            1,
-            1,
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
-            1
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
           ]
         }
       ],
@@ -3126,896 +3126,1792 @@
           "gene": "ZNF608",
           "score": 0.12688,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18603,
           "gene": "ZNF607",
           "score": 0.072299,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18602,
           "gene": "ZNF606",
           "score": 0.043496,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18601,
           "gene": "ZNF605",
           "score": 0.013934,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18600,
           "gene": "ZNF600",
           "score": 0.083798,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18599,
           "gene": "ZNF599",
           "score": -0.26203,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18598,
           "gene": "ZNF598",
           "score": 0.15653,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18597,
           "gene": "ZNF597",
           "score": -0.12037,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18596,
           "gene": "ZNF596",
           "score": -0.19227,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18595,
           "gene": "ZNF595",
           "score": 0.073366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18594,
           "gene": "ZNF594",
           "score": 0.37002,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18593,
           "gene": "ZNF593",
           "score": 0.031148,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18592,
           "gene": "ZNF592",
           "score": -0.26199,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18591,
           "gene": "ZNF589",
           "score": -0.47131,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18590,
           "gene": "ZNF587B",
           "score": -0.0036534,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18589,
           "gene": "ZNF587",
           "score": -0.016915,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18588,
           "gene": "ZNF586",
           "score": 0.050891,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18587,
           "gene": "ZNF585B",
           "score": -0.10684,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18586,
           "gene": "ZNF585A",
           "score": 0.11733,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18585,
           "gene": "ZNF584",
           "score": -0.13782,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18584,
           "gene": "ZNF583",
           "score": 0.18765,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18583,
           "gene": "ZNF582",
           "score": -0.015977,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18582,
           "gene": "ZNF581",
           "score": -0.051373,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18581,
           "gene": "ZNF580",
           "score": 0.27375,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18580,
           "gene": "ZNF579",
           "score": 0.083199,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18579,
           "gene": "ZNF578",
           "score": -0.28973,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18578,
           "gene": "ZNF577",
           "score": -0.28492,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18577,
           "gene": "ZNF576",
           "score": -0.10189,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18576,
           "gene": "ZNF575",
           "score": 0.29304,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18575,
           "gene": "ZNF574",
           "score": 0.082974,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18574,
           "gene": "ZNF573",
           "score": 0.01173,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18573,
           "gene": "ZNF572",
           "score": 0.1097,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18572,
           "gene": "ZNF571",
           "score": -0.29187,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18571,
           "gene": "ZNF570",
           "score": -0.048904,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18570,
           "gene": "ZNF57",
           "score": 0.054145,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18569,
           "gene": "ZNF569",
           "score": -0.14599,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18568,
           "gene": "ZNF568",
           "score": -0.084297,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18567,
           "gene": "ZNF567",
           "score": 0.1728,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18566,
           "gene": "ZNF566",
           "score": 0.11916,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18565,
           "gene": "ZNF565",
           "score": 0.046647,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18564,
           "gene": "ZNF564",
           "score": 0.043877,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18563,
           "gene": "ZNF563",
           "score": -0.19572,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18562,
           "gene": "ZNF562",
           "score": 0.0037033,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18561,
           "gene": "ZNF561",
           "score": -0.2972,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18560,
           "gene": "ZNF560",
           "score": -0.1161,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18559,
           "gene": "ZNF559-ZNF177",
           "score": -0.035171,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18558,
           "gene": "ZNF559",
           "score": 0.12576,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18557,
           "gene": "ZNF558",
           "score": 0.20418,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18556,
           "gene": "ZNF557",
           "score": -0.41338,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18555,
           "gene": "ZNF556",
           "score": 0.12917,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18554,
           "gene": "ZNF555",
           "score": -0.075628,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18553,
           "gene": "ZNF554",
           "score": -0.047888,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18552,
           "gene": "ZNF552",
           "score": 0.2297,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18551,
           "gene": "ZNF551",
           "score": -0.060688,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18550,
           "gene": "ZNF550",
           "score": -0.025795,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18549,
           "gene": "ZNF549",
           "score": -0.016808,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18548,
           "gene": "ZNF548",
           "score": -0.049671,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18547,
           "gene": "ZNF547",
           "score": 0.10727,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18546,
           "gene": "ZNF546",
           "score": -0.013879,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18545,
           "gene": "ZNF544",
           "score": -0.012014,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18544,
           "gene": "ZNF543",
           "score": 0.12739,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18543,
           "gene": "ZNF541",
           "score": -0.10405,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18542,
           "gene": "ZNF540",
           "score": 0.20023,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18541,
           "gene": "ZNF536",
           "score": 0.20535,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18540,
           "gene": "ZNF534",
           "score": -0.0011927,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18539,
           "gene": "ZNF532",
           "score": -0.065848,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18538,
           "gene": "ZNF530",
           "score": -0.092644,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18537,
           "gene": "ZNF529",
           "score": -0.28892,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18536,
           "gene": "ZNF528",
           "score": 0.070663,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18535,
           "gene": "ZNF527",
           "score": -0.04451,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18534,
           "gene": "ZNF526",
           "score": -0.23212,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18533,
           "gene": "ZNF524",
           "score": -0.13637,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18532,
           "gene": "ZNF521",
           "score": -0.15231,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18531,
           "gene": "ZNF519",
           "score": -0.088078,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18530,
           "gene": "ZNF518B",
           "score": -0.036369,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18529,
           "gene": "ZNF518A",
           "score": -0.016586,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18528,
           "gene": "ZNF517",
           "score": 0.1061,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18527,
           "gene": "ZNF516",
           "score": -0.15165,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18526,
           "gene": "ZNF514",
           "score": 0.15989,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18525,
           "gene": "ZNF513",
           "score": -0.075366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18524,
           "gene": "ZNF512B",
           "score": 0.12756,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18523,
           "gene": "ZNF512",
           "score": -0.13474,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18522,
           "gene": "ZNF511",
           "score": 0.31078,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18521,
           "gene": "ZNF510",
           "score": -0.1862,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18520,
           "gene": "ZNF507",
           "score": 0.05839,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18519,
           "gene": "ZNF506",
           "score": 0.49766,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18518,
           "gene": "ZNF503",
           "score": 0.13902,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18517,
           "gene": "ZNF502",
           "score": 0.083177,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18516,
           "gene": "ZNF501",
           "score": 0.16282,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18515,
           "gene": "ZNF500",
           "score": -0.040884,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18514,
           "gene": "ZNF497",
           "score": 0.0020353,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18513,
           "gene": "ZNF496",
           "score": -0.42909,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18512,
           "gene": "ZNF493",
           "score": -0.34255,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18511,
           "gene": "ZNF492",
           "score": 0.53004,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18510,
           "gene": "ZNF491",
           "score": -0.20654,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18509,
           "gene": "ZNF490",
           "score": 0.30996,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18508,
           "gene": "ZNF488",
           "score": 0.30129,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18507,
           "gene": "ZNF486",
           "score": -0.35845,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18506,
           "gene": "ZNF485",
           "score": -0.074194,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18505,
           "gene": "ZNF484",
           "score": -0.15525,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18504,
           "gene": "ZNF483",
           "score": -0.064107,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18503,
           "gene": "ZNF480",
           "score": 0.079031,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18502,
           "gene": "ZNF48",
           "score": 0.040223,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18501,
           "gene": "ZNF479",
           "score": -0.18857,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18500,
           "gene": "ZNF473",
           "score": 0.11782,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18499,
           "gene": "ZNF471",
           "score": -0.10068,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18498,
           "gene": "ZNF470",
           "score": 0.13604,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18497,
           "gene": "ZNF469",
           "score": -0.051998,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18496,
           "gene": "ZNF468",
           "score": 0.26556,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18495,
           "gene": "ZNF467",
           "score": 0.21092,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18494,
           "gene": "ZNF462",
           "score": -0.23175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18493,
           "gene": "ZNF461",
           "score": -0.01324,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18492,
           "gene": "ZNF460",
           "score": -0.11387,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18491,
           "gene": "ZNF454",
           "score": 0.15656,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18490,
           "gene": "ZNF451",
           "score": 0.1581,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18489,
           "gene": "ZNF45",
           "score": 0.18164,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18488,
           "gene": "ZNF449",
           "score": 0.0080712,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18487,
           "gene": "ZNF446",
           "score": 0.44891,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18486,
           "gene": "ZNF445",
           "score": -0.21726,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18485,
           "gene": "ZNF444",
           "score": 0.10247,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18484,
           "gene": "ZNF443",
           "score": 0.017261,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18483,
           "gene": "ZNF442",
           "score": 0.35702,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18482,
           "gene": "ZNF441",
           "score": -0.028326,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18481,
           "gene": "ZNF440",
           "score": -0.045372,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18480,
           "gene": "ZNF44",
           "score": 0.051431,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18479,
           "gene": "ZNF439",
           "score": -0.074874,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18478,
           "gene": "ZNF438",
           "score": 0.051488,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18477,
           "gene": "ZNF436",
           "score": 0.33876,
           "hit": 1,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 1035,
+          "gene": "ARMCX5",
+          "score": 0.079172,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4109,
+          "gene": "DENND2D",
+          "score": 0.052524,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17667,
+          "gene": "VAC14",
+          "score": -0.070281,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11964,
+          "gene": "PHF21A",
+          "score": -0.18496,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18349,
+          "gene": "ZNF22",
+          "score": 0.099706,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2019,
+          "gene": "C9orf92",
+          "score": -0.33098,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11253,
+          "gene": "OR5A2",
+          "score": 0.23934,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11415,
+          "gene": "OTOL1",
+          "score": 0.042275,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7609,
+          "gene": "ITPR3",
+          "score": -0.18851,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15610,
+          "gene": "STAM2",
+          "score": -0.21057,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7814,
+          "gene": "KCTD2",
+          "score": -0.059414,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5397,
+          "gene": "FBXO42",
+          "score": 0.29237,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15288,
+          "gene": "SPAG17",
+          "score": 0.017603,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5380,
+          "gene": "FBXO22",
+          "score": 0.1491,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 497,
+          "gene": "AKAP5",
+          "score": -0.16348,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3180,
+          "gene": "CLPTM1L",
+          "score": 0.054154,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6158,
+          "gene": "GMPR",
+          "score": -0.045694,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1447,
+          "gene": "BCL2L12",
+          "score": 0.067577,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6500,
+          "gene": "GSTO2",
+          "score": 0.047835,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4092,
+          "gene": "DEFB134",
+          "score": 0.11669,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7358,
+          "gene": "IL2RG",
+          "score": 0.25489,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 39,
+          "gene": "ABCA7",
+          "score": -0.086483,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3689,
+          "gene": "CTLA4",
+          "score": 0.052611,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10382,
+          "gene": "NOXRED1",
+          "score": -0.21094,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15585,
+          "gene": "ST3GAL5",
+          "score": -0.071085,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4634,
+          "gene": "EEF1D",
+          "score": -0.056527,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17392,
+          "gene": "UBE2QL1",
+          "score": -0.26317,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1529,
+          "gene": "BLK",
+          "score": -0.011389,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4589,
+          "gene": "ECE1",
+          "score": -0.078588,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 581,
+          "gene": "ALOX15",
+          "score": -0.0073389,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10758,
+          "gene": "NonTarget.CTRL194",
+          "score": -0.0068882,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16044,
+          "gene": "TBK1",
+          "score": 0.064703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 478,
+          "gene": "AJUBA",
+          "score": -0.12662,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11006,
+          "gene": "OR10G3",
+          "score": -0.19135,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11660,
+          "gene": "PCDHA7",
+          "score": -0.16991,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7515,
+          "gene": "IRF1",
+          "score": -0.057996,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14851,
+          "gene": "SLC36A1",
+          "score": 0.0062899,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6650,
+          "gene": "H4C13",
+          "score": -0.10299,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1797,
+          "gene": "C19orf25",
+          "score": -0.16354,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6135,
+          "gene": "GLTPD2",
+          "score": -0.30143,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16450,
+          "gene": "TMCO2",
+          "score": -0.13777,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4465,
+          "gene": "DSC3",
+          "score": 0.003556,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17304,
+          "gene": "TWNK",
+          "score": 0.036641,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12399,
+          "gene": "POLR3G",
+          "score": -0.062667,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13313,
+          "gene": "RBBP7",
+          "score": 0.11243,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3203,
+          "gene": "CMAS",
+          "score": 0.0097112,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1217,
+          "gene": "ATP1A4",
+          "score": 0.10274,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11962,
+          "gene": "PHF20",
+          "score": 0.12324,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4581,
+          "gene": "EBF2",
+          "score": 0.019827,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5539,
+          "gene": "FIGNL2",
+          "score": -0.157,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 195,
+          "gene": "ACSM6",
+          "score": 0.22588,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12728,
+          "gene": "PROKR2",
+          "score": -0.22557,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11790,
+          "gene": "PDGFC",
+          "score": 0.35243,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 13491,
+          "gene": "RFX2",
+          "score": 0.055279,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 992,
+          "gene": "ARK2N",
+          "score": -0.019368,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18325,
+          "gene": "ZNF177",
+          "score": -0.42213,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 5037,
+          "gene": "ETV7",
+          "score": 0.20274,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7087,
+          "gene": "HSPB7",
+          "score": 0.076501,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16630,
+          "gene": "TMEM263",
+          "score": -0.047598,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7273,
+          "gene": "IGIP",
+          "score": 0.041687,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12841,
+          "gene": "PRTN3",
+          "score": -0.06259,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16697,
+          "gene": "TMEM94",
+          "score": 0.040703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12995,
+          "gene": "PTPN23",
+          "score": 0.073748,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5224,
+          "gene": "FAM20B",
+          "score": -0.23095,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10826,
+          "gene": "NonTarget.CTRL3",
+          "score": 0.10059,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2517,
+          "gene": "CD300C",
+          "score": -0.2057,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9124,
+          "gene": "MCRS1",
+          "score": -0.011183,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3687,
+          "gene": "CTHRC1",
+          "score": -0.20672,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16499,
+          "gene": "TMEM132A",
+          "score": 0.096844,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15878,
+          "gene": "TAAR1",
+          "score": 0.14204,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8810,
+          "gene": "LY9",
+          "score": 0.018889,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12786,
+          "gene": "PRR29",
+          "score": 0.12653,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2454,
+          "gene": "CCNY",
+          "score": -0.44482,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 13606,
+          "gene": "RIOK2",
+          "score": 0.052317,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14693,
+          "gene": "SLC22A18",
+          "score": 0.20263,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12249,
+          "gene": "PLP1",
+          "score": -0.30074,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12510,
+          "gene": "PPM1K",
+          "score": 0.18101,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12344,
+          "gene": "POFUT1",
+          "score": 0.13927,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11042,
+          "gene": "OR13C3",
+          "score": 0.082765,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2900,
+          "gene": "CGNL1",
+          "score": 0.19489,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3427,
+          "gene": "COX6A1",
+          "score": 0.1119,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1132,
+          "gene": "ASPA",
+          "score": -0.22456,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3239,
+          "gene": "CNIH2",
+          "score": -0.14124,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14432,
+          "gene": "SFXN4",
+          "score": 0.088048,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3866,
+          "gene": "CYP8B1",
+          "score": 0.043215,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3600,
+          "gene": "CSKMT",
+          "score": -0.3039,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14094,
+          "gene": "SASH3",
+          "score": 0.12246,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9604,
+          "gene": "MRPS5",
+          "score": 0.1275,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16192,
+          "gene": "TESK2",
+          "score": -0.036482,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12540,
+          "gene": "PPP1R26",
+          "score": 0.17773,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14721,
+          "gene": "SLC25A14",
+          "score": 0.0046482,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9181,
+          "gene": "MEDAG",
+          "score": 0.064143,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12930,
+          "gene": "PTAR1",
+          "score": -0.26585,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13584,
+          "gene": "RIDA",
+          "score": -0.25047,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15407,
+          "gene": "SPIRE2",
+          "score": -0.017158,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1352,
+          "gene": "B3GNTL1",
+          "score": 0.0625085,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6432,
+          "gene": "GRIFIN",
+          "score": -0.18217,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6712,
+          "gene": "HBG2",
+          "score": 0.16415,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1687,
+          "gene": "BUB3",
+          "score": 0.21887,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12022,
+          "gene": "PIEZO2",
+          "score": 0.0043525,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4876,
+          "gene": "ENY2",
+          "score": -0.21481,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15405,
+          "gene": "SPINT4",
+          "score": 0.23442,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6606,
+          "gene": "H2AP",
+          "score": 0.051486,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 892,
+          "gene": "AQR",
+          "score": 0.11593,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15840,
+          "gene": "SYNJ2",
+          "score": 0.035979,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11785,
+          "gene": "PDE8A",
+          "score": -0.044873,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18073,
+          "gene": "YY1",
+          "score": -0.10208,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16668,
+          "gene": "TMEM62",
+          "score": 0.096311,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2298,
+          "gene": "CCDC166",
+          "score": -0.034049,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3879,
+          "gene": "CYTIP",
+          "score": -0.0025065,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2420,
+          "gene": "CCM2L",
+          "score": -0.081227,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17900,
+          "gene": "WDR88",
+          "score": -0.15478,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14616,
+          "gene": "SLC10A1",
+          "score": -0.15369,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12542,
+          "gene": "PPP1R35",
+          "score": -0.08237,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18465,
+          "gene": "ZNF419",
+          "score": -0.041417,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7443,
+          "gene": "INSL4",
+          "score": -0.08216,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12229,
+          "gene": "PLET1",
+          "score": -0.08709,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15179,
+          "gene": "SNUPN",
+          "score": 0.01426,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9177,
+          "gene": "MED6",
+          "score": -0.1367,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2183,
+          "gene": "CASKIN2",
+          "score": -0.070451,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2461,
+          "gene": "CCR5",
+          "score": 0.044152,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13057,
+          "gene": "PXMP4",
+          "score": 0.16473,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10920,
+          "gene": "OCEL1",
+          "score": -0.083103,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17,
+          "gene": "AAMP",
+          "score": -0.1705,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4174,
+          "gene": "DHRS4L2",
+          "score": -0.13034,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7129,
+          "gene": "HYAL4",
+          "score": -0.16579,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12554,
+          "gene": "PPP1R8",
+          "score": -0.19875,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14819,
+          "gene": "SLC34A3",
+          "score": -0.23035,
+          "hit": 0,
+          "round": 4
         }
       ],
       "queried_history": [
@@ -6712,896 +7608,1792 @@
           "gene": "ZNF608",
           "score": 0.12688,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18603,
           "gene": "ZNF607",
           "score": 0.072299,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18602,
           "gene": "ZNF606",
           "score": 0.043496,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18601,
           "gene": "ZNF605",
           "score": 0.013934,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18600,
           "gene": "ZNF600",
           "score": 0.083798,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18599,
           "gene": "ZNF599",
           "score": -0.26203,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18598,
           "gene": "ZNF598",
           "score": 0.15653,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18597,
           "gene": "ZNF597",
           "score": -0.12037,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18596,
           "gene": "ZNF596",
           "score": -0.19227,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18595,
           "gene": "ZNF595",
           "score": 0.073366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18594,
           "gene": "ZNF594",
           "score": 0.37002,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18593,
           "gene": "ZNF593",
           "score": 0.031148,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18592,
           "gene": "ZNF592",
           "score": -0.26199,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18591,
           "gene": "ZNF589",
           "score": -0.47131,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18590,
           "gene": "ZNF587B",
           "score": -0.0036534,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18589,
           "gene": "ZNF587",
           "score": -0.016915,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18588,
           "gene": "ZNF586",
           "score": 0.050891,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18587,
           "gene": "ZNF585B",
           "score": -0.10684,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18586,
           "gene": "ZNF585A",
           "score": 0.11733,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18585,
           "gene": "ZNF584",
           "score": -0.13782,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18584,
           "gene": "ZNF583",
           "score": 0.18765,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18583,
           "gene": "ZNF582",
           "score": -0.015977,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18582,
           "gene": "ZNF581",
           "score": -0.051373,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18581,
           "gene": "ZNF580",
           "score": 0.27375,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18580,
           "gene": "ZNF579",
           "score": 0.083199,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18579,
           "gene": "ZNF578",
           "score": -0.28973,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18578,
           "gene": "ZNF577",
           "score": -0.28492,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18577,
           "gene": "ZNF576",
           "score": -0.10189,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18576,
           "gene": "ZNF575",
           "score": 0.29304,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18575,
           "gene": "ZNF574",
           "score": 0.082974,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18574,
           "gene": "ZNF573",
           "score": 0.01173,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18573,
           "gene": "ZNF572",
           "score": 0.1097,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18572,
           "gene": "ZNF571",
           "score": -0.29187,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18571,
           "gene": "ZNF570",
           "score": -0.048904,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18570,
           "gene": "ZNF57",
           "score": 0.054145,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18569,
           "gene": "ZNF569",
           "score": -0.14599,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18568,
           "gene": "ZNF568",
           "score": -0.084297,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18567,
           "gene": "ZNF567",
           "score": 0.1728,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18566,
           "gene": "ZNF566",
           "score": 0.11916,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18565,
           "gene": "ZNF565",
           "score": 0.046647,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18564,
           "gene": "ZNF564",
           "score": 0.043877,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18563,
           "gene": "ZNF563",
           "score": -0.19572,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18562,
           "gene": "ZNF562",
           "score": 0.0037033,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18561,
           "gene": "ZNF561",
           "score": -0.2972,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18560,
           "gene": "ZNF560",
           "score": -0.1161,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18559,
           "gene": "ZNF559-ZNF177",
           "score": -0.035171,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18558,
           "gene": "ZNF559",
           "score": 0.12576,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18557,
           "gene": "ZNF558",
           "score": 0.20418,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18556,
           "gene": "ZNF557",
           "score": -0.41338,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18555,
           "gene": "ZNF556",
           "score": 0.12917,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18554,
           "gene": "ZNF555",
           "score": -0.075628,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18553,
           "gene": "ZNF554",
           "score": -0.047888,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18552,
           "gene": "ZNF552",
           "score": 0.2297,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18551,
           "gene": "ZNF551",
           "score": -0.060688,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18550,
           "gene": "ZNF550",
           "score": -0.025795,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18549,
           "gene": "ZNF549",
           "score": -0.016808,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18548,
           "gene": "ZNF548",
           "score": -0.049671,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18547,
           "gene": "ZNF547",
           "score": 0.10727,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18546,
           "gene": "ZNF546",
           "score": -0.013879,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18545,
           "gene": "ZNF544",
           "score": -0.012014,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18544,
           "gene": "ZNF543",
           "score": 0.12739,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18543,
           "gene": "ZNF541",
           "score": -0.10405,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18542,
           "gene": "ZNF540",
           "score": 0.20023,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18541,
           "gene": "ZNF536",
           "score": 0.20535,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18540,
           "gene": "ZNF534",
           "score": -0.0011927,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18539,
           "gene": "ZNF532",
           "score": -0.065848,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18538,
           "gene": "ZNF530",
           "score": -0.092644,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18537,
           "gene": "ZNF529",
           "score": -0.28892,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18536,
           "gene": "ZNF528",
           "score": 0.070663,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18535,
           "gene": "ZNF527",
           "score": -0.04451,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18534,
           "gene": "ZNF526",
           "score": -0.23212,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18533,
           "gene": "ZNF524",
           "score": -0.13637,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18532,
           "gene": "ZNF521",
           "score": -0.15231,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18531,
           "gene": "ZNF519",
           "score": -0.088078,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18530,
           "gene": "ZNF518B",
           "score": -0.036369,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18529,
           "gene": "ZNF518A",
           "score": -0.016586,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18528,
           "gene": "ZNF517",
           "score": 0.1061,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18527,
           "gene": "ZNF516",
           "score": -0.15165,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18526,
           "gene": "ZNF514",
           "score": 0.15989,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18525,
           "gene": "ZNF513",
           "score": -0.075366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18524,
           "gene": "ZNF512B",
           "score": 0.12756,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18523,
           "gene": "ZNF512",
           "score": -0.13474,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18522,
           "gene": "ZNF511",
           "score": 0.31078,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18521,
           "gene": "ZNF510",
           "score": -0.1862,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18520,
           "gene": "ZNF507",
           "score": 0.05839,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18519,
           "gene": "ZNF506",
           "score": 0.49766,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18518,
           "gene": "ZNF503",
           "score": 0.13902,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18517,
           "gene": "ZNF502",
           "score": 0.083177,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18516,
           "gene": "ZNF501",
           "score": 0.16282,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18515,
           "gene": "ZNF500",
           "score": -0.040884,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18514,
           "gene": "ZNF497",
           "score": 0.0020353,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18513,
           "gene": "ZNF496",
           "score": -0.42909,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18512,
           "gene": "ZNF493",
           "score": -0.34255,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18511,
           "gene": "ZNF492",
           "score": 0.53004,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18510,
           "gene": "ZNF491",
           "score": -0.20654,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18509,
           "gene": "ZNF490",
           "score": 0.30996,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18508,
           "gene": "ZNF488",
           "score": 0.30129,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18507,
           "gene": "ZNF486",
           "score": -0.35845,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18506,
           "gene": "ZNF485",
           "score": -0.074194,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18505,
           "gene": "ZNF484",
           "score": -0.15525,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18504,
           "gene": "ZNF483",
           "score": -0.064107,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18503,
           "gene": "ZNF480",
           "score": 0.079031,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18502,
           "gene": "ZNF48",
           "score": 0.040223,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18501,
           "gene": "ZNF479",
           "score": -0.18857,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18500,
           "gene": "ZNF473",
           "score": 0.11782,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18499,
           "gene": "ZNF471",
           "score": -0.10068,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18498,
           "gene": "ZNF470",
           "score": 0.13604,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18497,
           "gene": "ZNF469",
           "score": -0.051998,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18496,
           "gene": "ZNF468",
           "score": 0.26556,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18495,
           "gene": "ZNF467",
           "score": 0.21092,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18494,
           "gene": "ZNF462",
           "score": -0.23175,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18493,
           "gene": "ZNF461",
           "score": -0.01324,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18492,
           "gene": "ZNF460",
           "score": -0.11387,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18491,
           "gene": "ZNF454",
           "score": 0.15656,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18490,
           "gene": "ZNF451",
           "score": 0.1581,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18489,
           "gene": "ZNF45",
           "score": 0.18164,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18488,
           "gene": "ZNF449",
           "score": 0.0080712,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18487,
           "gene": "ZNF446",
           "score": 0.44891,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18486,
           "gene": "ZNF445",
           "score": -0.21726,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18485,
           "gene": "ZNF444",
           "score": 0.10247,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18484,
           "gene": "ZNF443",
           "score": 0.017261,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18483,
           "gene": "ZNF442",
           "score": 0.35702,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18482,
           "gene": "ZNF441",
           "score": -0.028326,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18481,
           "gene": "ZNF440",
           "score": -0.045372,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18480,
           "gene": "ZNF44",
           "score": 0.051431,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18479,
           "gene": "ZNF439",
           "score": -0.074874,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18478,
           "gene": "ZNF438",
           "score": 0.051488,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18477,
           "gene": "ZNF436",
           "score": 0.33876,
           "hit": 1,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 1035,
+          "gene": "ARMCX5",
+          "score": 0.079172,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4109,
+          "gene": "DENND2D",
+          "score": 0.052524,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17667,
+          "gene": "VAC14",
+          "score": -0.070281,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11964,
+          "gene": "PHF21A",
+          "score": -0.18496,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18349,
+          "gene": "ZNF22",
+          "score": 0.099706,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2019,
+          "gene": "C9orf92",
+          "score": -0.33098,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11253,
+          "gene": "OR5A2",
+          "score": 0.23934,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11415,
+          "gene": "OTOL1",
+          "score": 0.042275,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7609,
+          "gene": "ITPR3",
+          "score": -0.18851,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15610,
+          "gene": "STAM2",
+          "score": -0.21057,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7814,
+          "gene": "KCTD2",
+          "score": -0.059414,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5397,
+          "gene": "FBXO42",
+          "score": 0.29237,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15288,
+          "gene": "SPAG17",
+          "score": 0.017603,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5380,
+          "gene": "FBXO22",
+          "score": 0.1491,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 497,
+          "gene": "AKAP5",
+          "score": -0.16348,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3180,
+          "gene": "CLPTM1L",
+          "score": 0.054154,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6158,
+          "gene": "GMPR",
+          "score": -0.045694,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1447,
+          "gene": "BCL2L12",
+          "score": 0.067577,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6500,
+          "gene": "GSTO2",
+          "score": 0.047835,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4092,
+          "gene": "DEFB134",
+          "score": 0.11669,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7358,
+          "gene": "IL2RG",
+          "score": 0.25489,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 39,
+          "gene": "ABCA7",
+          "score": -0.086483,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3689,
+          "gene": "CTLA4",
+          "score": 0.052611,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10382,
+          "gene": "NOXRED1",
+          "score": -0.21094,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15585,
+          "gene": "ST3GAL5",
+          "score": -0.071085,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4634,
+          "gene": "EEF1D",
+          "score": -0.056527,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17392,
+          "gene": "UBE2QL1",
+          "score": -0.26317,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1529,
+          "gene": "BLK",
+          "score": -0.011389,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4589,
+          "gene": "ECE1",
+          "score": -0.078588,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 581,
+          "gene": "ALOX15",
+          "score": -0.0073389,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10758,
+          "gene": "NonTarget.CTRL194",
+          "score": -0.0068882,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16044,
+          "gene": "TBK1",
+          "score": 0.064703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 478,
+          "gene": "AJUBA",
+          "score": -0.12662,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11006,
+          "gene": "OR10G3",
+          "score": -0.19135,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11660,
+          "gene": "PCDHA7",
+          "score": -0.16991,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7515,
+          "gene": "IRF1",
+          "score": -0.057996,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14851,
+          "gene": "SLC36A1",
+          "score": 0.0062899,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6650,
+          "gene": "H4C13",
+          "score": -0.10299,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1797,
+          "gene": "C19orf25",
+          "score": -0.16354,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6135,
+          "gene": "GLTPD2",
+          "score": -0.30143,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16450,
+          "gene": "TMCO2",
+          "score": -0.13777,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4465,
+          "gene": "DSC3",
+          "score": 0.003556,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17304,
+          "gene": "TWNK",
+          "score": 0.036641,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12399,
+          "gene": "POLR3G",
+          "score": -0.062667,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13313,
+          "gene": "RBBP7",
+          "score": 0.11243,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3203,
+          "gene": "CMAS",
+          "score": 0.0097112,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1217,
+          "gene": "ATP1A4",
+          "score": 0.10274,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11962,
+          "gene": "PHF20",
+          "score": 0.12324,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4581,
+          "gene": "EBF2",
+          "score": 0.019827,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5539,
+          "gene": "FIGNL2",
+          "score": -0.157,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 195,
+          "gene": "ACSM6",
+          "score": 0.22588,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12728,
+          "gene": "PROKR2",
+          "score": -0.22557,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11790,
+          "gene": "PDGFC",
+          "score": 0.35243,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 13491,
+          "gene": "RFX2",
+          "score": 0.055279,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 992,
+          "gene": "ARK2N",
+          "score": -0.019368,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18325,
+          "gene": "ZNF177",
+          "score": -0.42213,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 5037,
+          "gene": "ETV7",
+          "score": 0.20274,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7087,
+          "gene": "HSPB7",
+          "score": 0.076501,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16630,
+          "gene": "TMEM263",
+          "score": -0.047598,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7273,
+          "gene": "IGIP",
+          "score": 0.041687,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12841,
+          "gene": "PRTN3",
+          "score": -0.06259,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16697,
+          "gene": "TMEM94",
+          "score": 0.040703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12995,
+          "gene": "PTPN23",
+          "score": 0.073748,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5224,
+          "gene": "FAM20B",
+          "score": -0.23095,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10826,
+          "gene": "NonTarget.CTRL3",
+          "score": 0.10059,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2517,
+          "gene": "CD300C",
+          "score": -0.2057,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9124,
+          "gene": "MCRS1",
+          "score": -0.011183,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3687,
+          "gene": "CTHRC1",
+          "score": -0.20672,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16499,
+          "gene": "TMEM132A",
+          "score": 0.096844,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15878,
+          "gene": "TAAR1",
+          "score": 0.14204,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8810,
+          "gene": "LY9",
+          "score": 0.018889,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12786,
+          "gene": "PRR29",
+          "score": 0.12653,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2454,
+          "gene": "CCNY",
+          "score": -0.44482,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 13606,
+          "gene": "RIOK2",
+          "score": 0.052317,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14693,
+          "gene": "SLC22A18",
+          "score": 0.20263,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12249,
+          "gene": "PLP1",
+          "score": -0.30074,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12510,
+          "gene": "PPM1K",
+          "score": 0.18101,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12344,
+          "gene": "POFUT1",
+          "score": 0.13927,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11042,
+          "gene": "OR13C3",
+          "score": 0.082765,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2900,
+          "gene": "CGNL1",
+          "score": 0.19489,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3427,
+          "gene": "COX6A1",
+          "score": 0.1119,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1132,
+          "gene": "ASPA",
+          "score": -0.22456,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3239,
+          "gene": "CNIH2",
+          "score": -0.14124,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14432,
+          "gene": "SFXN4",
+          "score": 0.088048,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3866,
+          "gene": "CYP8B1",
+          "score": 0.043215,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3600,
+          "gene": "CSKMT",
+          "score": -0.3039,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14094,
+          "gene": "SASH3",
+          "score": 0.12246,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9604,
+          "gene": "MRPS5",
+          "score": 0.1275,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16192,
+          "gene": "TESK2",
+          "score": -0.036482,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12540,
+          "gene": "PPP1R26",
+          "score": 0.17773,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14721,
+          "gene": "SLC25A14",
+          "score": 0.0046482,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9181,
+          "gene": "MEDAG",
+          "score": 0.064143,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12930,
+          "gene": "PTAR1",
+          "score": -0.26585,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13584,
+          "gene": "RIDA",
+          "score": -0.25047,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15407,
+          "gene": "SPIRE2",
+          "score": -0.017158,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1352,
+          "gene": "B3GNTL1",
+          "score": 0.0625085,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6432,
+          "gene": "GRIFIN",
+          "score": -0.18217,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6712,
+          "gene": "HBG2",
+          "score": 0.16415,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1687,
+          "gene": "BUB3",
+          "score": 0.21887,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12022,
+          "gene": "PIEZO2",
+          "score": 0.0043525,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4876,
+          "gene": "ENY2",
+          "score": -0.21481,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15405,
+          "gene": "SPINT4",
+          "score": 0.23442,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6606,
+          "gene": "H2AP",
+          "score": 0.051486,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 892,
+          "gene": "AQR",
+          "score": 0.11593,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15840,
+          "gene": "SYNJ2",
+          "score": 0.035979,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11785,
+          "gene": "PDE8A",
+          "score": -0.044873,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18073,
+          "gene": "YY1",
+          "score": -0.10208,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16668,
+          "gene": "TMEM62",
+          "score": 0.096311,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2298,
+          "gene": "CCDC166",
+          "score": -0.034049,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3879,
+          "gene": "CYTIP",
+          "score": -0.0025065,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2420,
+          "gene": "CCM2L",
+          "score": -0.081227,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17900,
+          "gene": "WDR88",
+          "score": -0.15478,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14616,
+          "gene": "SLC10A1",
+          "score": -0.15369,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12542,
+          "gene": "PPP1R35",
+          "score": -0.08237,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18465,
+          "gene": "ZNF419",
+          "score": -0.041417,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7443,
+          "gene": "INSL4",
+          "score": -0.08216,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12229,
+          "gene": "PLET1",
+          "score": -0.08709,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15179,
+          "gene": "SNUPN",
+          "score": 0.01426,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9177,
+          "gene": "MED6",
+          "score": -0.1367,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2183,
+          "gene": "CASKIN2",
+          "score": -0.070451,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2461,
+          "gene": "CCR5",
+          "score": 0.044152,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13057,
+          "gene": "PXMP4",
+          "score": 0.16473,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10920,
+          "gene": "OCEL1",
+          "score": -0.083103,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17,
+          "gene": "AAMP",
+          "score": -0.1705,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4174,
+          "gene": "DHRS4L2",
+          "score": -0.13034,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7129,
+          "gene": "HYAL4",
+          "score": -0.16579,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12554,
+          "gene": "PPP1R8",
+          "score": -0.19875,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14819,
+          "gene": "SLC34A3",
+          "score": -0.23035,
+          "hit": 0,
+          "round": 4
         }
       ]
     }

```
