# Change Record — candidate_5

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Carnevale22_Adenosine/run-1/best/current/harness
Generated at: 2026-04-30T06:52:16.590417

## Files Changed

- model.py: modified (added=33, deleted=21, delta=12)
- outputs/metrics.json: modified (added=2394, deleted=602, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -72,32 +72,44 @@
             sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
             top_performers = [h['candidate_index'] for h in sorted_history[:min(50, len(sorted_history))]]
         
-        # Find candidates similar to top performers (if gene search available)
+        # Thompson Sampling for exploitation: Bayesian bandit algorithm
+        # Maintains Beta distributions for each candidate and samples from posteriors
         exploit_candidates = set()
         remaining_avail = [i for i in available if i not in explore_indices]
         
-        if len(remaining_avail) > 0:
-            # If we have top performers and gene search might be available, use it
-            # Otherwise, sample from remaining with slight bias toward higher indices
-            # (assuming some clustering in the candidate list)
+        if len(remaining_avail) > 0 and len(history) > 0:
+            # Build hit/miss counts for each candidate
+            candidate_successes = {}
+            candidate_trials = {}
             
-            # Simple strategy: weighted sampling based on position (crude diversity)
-            weights = np.abs(np.linspace(-1, 1, len(remaining_avail))) + 0.1
-            weights = weights / weights.sum()
+            for h in history:
+                idx = h['candidate_index']
+                if idx not in candidate_trials:
+                    candidate_successes[idx] = 0
+                    candidate_trials[idx] = 0
+                candidate_trials[idx] += 1
+                if h.get('hit', 0) == 1:
+                    candidate_successes[idx] += 1
             
-            try:
-                exploit_indices = rng.choices(
-                    remaining_avail, 
-                    k=min(num_exploit, len(remaining_avail)),
-                    weights=weights
-                )
-                exploit_candidates = set(exploit_indices)
-            except:
-                # Fallback to uniform sampling
-                exploit_candidates = set(rng.sample(
-                    remaining_avail, 
-                    min(num_exploit, len(remaining_avail))
-                ))
+            # For candidates with no history, use optimistic initialization
+            # For candidates with history, sample from Beta(successes + 1, failures + 1)
+            ts_scores = []
+            for idx in remaining_avail:
+                if idx in candidate_trials:
+                    successes = candidate_successes.get(idx, 0)
+                    failures = candidate_trials[idx] - successes
+                    # Sample from Beta posterior
+                    sampled_prob = rng.betavariate(successes + 1, failures + 1)
+                else:
+                    # Optimistic initialization for unexplored candidates
+                    # Use a high value to encourage exploration
+                    sampled_prob = 0.7 + 0.3 * rng.random()
+                ts_scores.append((idx, sampled_prob))
+            
+            # Select top candidates by Thompson Sampling score
+            ts_scores.sort(key=lambda x: x[1], reverse=True)
+            exploit_indices = [idx for idx, _ in ts_scores[:min(num_exploit, len(ts_scores))]]
+            exploit_candidates = set(exploit_indices)
         
         selected_indices = list(explore_indices) + list(exploit_candidates)
     else:

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
-      "baseline_total_hits": 7,
+      "baseline_total_queries": 384,
+      "baseline_total_hits": 15,
       "delta_queries": 128,
-      "delta_hits": 8,
-      "total_queries": 384,
-      "total_hits": 15,
+      "delta_hits": 2,
+      "total_queries": 512,
+      "total_hits": 17,
       "top_k": 943,
       "hit_curve": {
         "queries": [
-          256,
-          384
+          384,
+          512
         ],
         "hits": [
-          7,
-          15
+          15,
+          17
         ]
       },
-      "auc": 1408.0,
-      "auc_normalized": 0.003888299752562743,
-      "ncg": 0.25772253765769115,
+      "auc": 2048.0,
+      "auc_normalized": 0.0042417815482502655,
+      "ncg": 0.26512419355997113,
       "round_details": [
         {
-          "round": 2,
+          "round": 3,
           "selected_count": 128,
-          "hits": 8,
-          "cumulative_hits": 15,
-          "precision_at_batch": 0.0625,
+          "hits": 2,
+          "cumulative_hits": 17,
+          "precision_at_batch": 0.015625,
           "selected": [
-            "RHOT2",
-            "TUBAL3",
-            "XKRY2",
-            "DAB2IP",
-            "GAPT",
-            "PRAMEF2",
-            "IQCF3",
-            "MSANTD3-TMEFF1",
-            "ARHGEF2",
-            "IPO13",
-            "ADARB1",
-            "COL4A4",
-            "FAM209A",
-            "TRIML2",
-            "NDUFB1",
-            "PPP3CB",
-            "RERGL",
-            "NonTarget.CTRL38",
-            "PGA3",
-            "CCNJL",
-            "OR5AN1",
-            "MMP16",
-            "FAM98B",
-            "CUL3",
-            "TREML4",
-            "CCDC28B",
-            "CLIC2",
-            "MAP3K3",
-            "NRG4",
-            "CSF2",
-            "MSH3",
-            "ATAT1",
-            "OXCT2",
-            "PRSS33",
-            "CLTRN",
-            "SYT1",
-            "SYCP2",
-            "GPR25",
-            "GPC2",
-            "DNAJC2",
-            "LOC729159",
-            "LAD1",
-            "BRMS1L",
-            "BCL11A",
-            "SH3TC1",
-            "ATP6AP1",
-            "OCA2",
-            "PLXDC1",
-            "STH",
-            "SMDT1",
-            "WNT8A",
-            "ESYT3",
-            "KCNJ3",
-            "TBRG1",
-            "SNAP29",
-            "PABPC3",
-            "BCL2L11",
-            "METTL6",
-            "FAM227B",
-            "ADCY9",
-            "INO80E",
-            "AK7",
-            "ZNF428",
-            "YIF1B",
-            "PMEL",
-            "TLCD3B",
-            "ANAPC4",
-            "TBC1D15",
-            "SDHA",
-            "SLC25A19",
-            "HERC3",
-            "ZSCAN20",
-            "LRRC7",
-            "YTHDF3",
-            "EP400",
-            "STC2",
-            "MUC13",
-            "FZD1",
-            "AP1S2",
-            "GUK1",
-            "ANKFY1",
-            "ZNF586",
-            "USH1G",
-            "HSPA12B",
-            "ZW10",
-            "KDR",
-            "CRACR2A",
-            "SUSD6",
-            "BCL7B",
-            "ODAD2",
-            "COPG1",
-            "BORCS5",
-            "ABCC12",
-            "ANKRD20A2",
-            "BCO2",
-            "BCOR",
-            "LMOD2",
-            "ZNF805",
-            "HOXC13",
-            "DNAH14",
-            "BEND3",
-            "UBA3",
-            "ATP2A3",
-            "LAMTOR1",
-            "ZNF654",
-            "FRMD6",
-            "ZNF669",
-            "CDK12",
-            "FMN2",
-            "DZIP1L",
-            "PRDM2",
-            "ZC3H13",
-            "SLC22A10",
-            "XPOT",
-            "ZMAT5",
-            "CEP43",
-            "DEFB112",
-            "ADNP",
-            "SLC6A6",
-            "CYP26C1",
-            "CAB39L",
-            "TMEM141",
-            "MYO1E",
-            "TUBB8",
-            "SPDL1",
-            "SYT9",
-            "ENSA",
-            "PPP4R2"
+            "MCM3AP",
+            "RTL9",
+            "THRA",
+            "LRCH4",
+            "CENPF",
+            "NEURL1",
+            "OR7D2",
+            "ANKRD50",
+            "CCNB1IP1",
+            "TERT",
+            "ADPGK",
+            "CYP51A1",
+            "MRGPRD",
+            "DCHS2",
+            "NPIPB3",
+            "ATOH1",
+            "CBS",
+            "DYNC1I1",
+            "MCEMP1",
+            "FAM157A",
+            "HSPA4",
+            "SEPTIN5",
+            "CD300A",
+            "RNASE6",
+            "ELP4",
+            "C3orf20",
+            "ART4",
+            "FZD6",
+            "NonTarget.CTRL169",
+            "LIMA1",
+            "PGLYRP1",
+            "NonTarget.CTRL15",
+            "CLHC1",
+            "ROBO4",
+            "CIAO1",
+            "ANKRD34C",
+            "OPRM1",
+            "NUP50",
+            "PTCHD1",
+            "VN1R4",
+            "WNT4",
+            "LOC100129083",
+            "C9orf139",
+            "TMEM104",
+            "NKAIN4",
+            "UBR3",
+            "ARMC12",
+            "HARBI1",
+            "PNPLA2",
+            "TAF4B",
+            "CDCA7L",
+            "GNPDA1",
+            "DHPS",
+            "CAMKK1",
+            "TRIB3",
+            "TRIM10",
+            "TRIM15",
+            "DHX35",
+            "EID2B",
+            "SLC6A14",
+            "CDK6",
+            "MYLK",
+            "DIP2B",
+            "REEP2",
+            "FUBP1",
+            "FAM47E-STBD1",
+            "PTGDR2",
+            "ZAR1",
+            "DMD",
+            "TRIT1",
+            "RUVBL2",
+            "NPRL2",
+            "LGALS13",
+            "SMAGP",
+            "TBX3",
+            "SSR1",
+            "GPR33",
+            "USP36",
+            "CYB5R4",
+            "DNAJB11",
+            "EMP3",
+            "KIF21A",
+            "ATP6V0E2",
+            "COL11A2",
+            "PADI4",
+            "FBXL2",
+            "C17orf58",
+            "NCAPH2",
+            "MAP3K15",
+            "ADAMTS15",
+            "ZFC3H1",
+            "AVIL",
+            "MAP9",
+            "NTAN1",
+            "NDE1",
+            "MAPK7",
+            "LMNB2",
+            "LNPK",
+            "STON2",
+            "NUDT14",
+            "DPYD",
+            "C2CD2",
+            "C2orf27A",
+            "ZNG1B",
+            "DRG2",
+            "RAB6C",
+            "GFOD2",
+            "BAZ1A",
+            "TNFRSF17",
+            "PCDHA10",
+            "MS4A6A",
+            "RAET1L",
+            "MCOLN2",
+            "SP140",
+            "ETV2",
+            "AGMAT",
+            "GZMB",
+            "CD109",
+            "FKBPL",
+            "H2AC17",
+            "NFKBID",
+            "UBE2K",
+            "ECE1",
+            "JPH4",
+            "TINAG",
+            "ZNF326",
+            "CABP4",
+            "CD82"
           ],
           "selected_scores": [
-            0.15184,
-            0.080271,
-            -0.2123,
-            0.044769,
-            -0.011911,
-            0.20294,
-            -0.044255,
-            -0.09824,
-            -0.034241,
-            -0.089332,
-            0.0072941,
-            0.079952,
-            -0.048248,
-            -0.011292,
-            -0.010165,
-            -0.011778,
-            0.14828,
-            -0.069151,
-            0.17943,
-            0.14958,
-            0.35942,
-            0.052122,
-            0.16907,
-            0.14949,
-            -0.4477,
-            0.37577,
-            0.18831,
-            0.066618,
-            0.041164,
-            -0.050149,
-            -0.20566,
-            0.31263,
-            0.33819,
-            -0.22276,
-            -0.13725,
-            -0.15675,
-            0.02306,
-            0.018811,
-            0.29964,
-            0.40151,
-            -0.24846,
-            0.33505,
-            -0.018266,
-            0.21109,
-            -0.3089,
-            0.30095,
-            -0.049326,
-            -0.2769,
-            -0.02723,
-            0.16957,
-            0.057329,
-            -0.30907,
-            -0.016158,
-            -0.21505,
-            -0.23827,
-            -0.21966,
-            0.33719,
-            -0.2162,
-            -0.18169,
-            0.15946,
-            -0.12583,
-            -0.053844,
-            0.043155,
-            -0.14187,
-            0.0077955,
-            -0.22864,
-            0.13634,
-            -0.044763,
-            0.19929,
-            0.008568,
-            -0.01863,
-            0.1752,
-            -0.064914,
-            -0.062509,
-            -0.071699,
-            -0.059057,
-            0.14463,
-            -0.1079,
-            -0.37582,
-            0.53392,
-            0.1186,
-            0.050891,
-            -0.035439,
-            -0.1018,
-            0.10344,
-            0.085495,
-            0.028925,
-            0.068816,
-            0.095651,
-            0.29212,
-            0.16188,
-            -0.090122,
-            0.068198,
-            0.19531,
-            0.27607,
-            -0.2411,
-            -0.0378,
-            0.052151,
-            -0.13105,
-            0.10655,
-            -0.1477,
-            0.075581,
-            -0.21116,
-            0.14123,
-            -0.065974,
-            0.074162,
-            0.001308,
-            -0.014396,
-            -0.17091,
-            -0.052318,
-            0.09734,
-            0.054432,
-            0.094775,
-            -0.084016,
-            0.11764,
-            0.063922,
-            -0.019297,
-            -0.085647,
-            0.065536,
-            0.27422,
-            0.33077,
-            0.22945,
-            -0.026485667,
-            -0.28545,
-            0.12938,
-            -0.10176,
-            -0.18372,
-            -0.061497
+            -0.00063426,
+            0.17401,
+            -0.074542,
+            0.10734145,
+            -0.18355,
+            0.16434,
+            -0.38256,
+            -0.11363,
+            -0.28364,
+            0.040836,
+            0.044493,
+            0.072361,
+            0.073169,
+            0.05212,
+            0.050308,
+            0.12806,
+            0.18808,
+            0.24858,
+            -0.30723,
+            0.032134,
+            0.023713,
+            -0.066519,
+            0.13193,
+            0.088345,
+            -0.14311,
+            0.064214,
+            -0.1008235,
+            -0.030256,
+            0.018037,
+            0.018931,
+            -0.099904,
+            0.032215,
+            -0.0094774,
+            0.064095,
+            -0.10199,
+            0.214,
+            -0.1572,
+            0.16105,
+            -0.040209,
+            -0.13521,
+            -0.19902,
+            -0.30715,
+            -0.094607,
+            -0.028552,
+            -0.074582,
+            0.19457,
+            -0.071949,
+            -0.20856,
+            -0.16671,
+            -0.054785,
+            0.16011,
+            0.013369666,
+            0.33435,
+            -0.0064197,
+            -0.067502,
+            -0.036856,
+            -0.14994,
+            0.0056604,
+            0.2206,
+            -0.19918,
+            -0.25727,
+            0.20458,
+            0.033532,
+            -0.11722,
+            0.073863,
+            0.034035,
+            -0.17351,
+            -0.11831,
+            0.070553,
+            -0.22555,
+            -0.077556,
+            -0.089705,
+            0.0588155,
+            0.096038,
+            0.036567,
+            0.2042,
+            0.029664,
+            0.032612,
+            -0.14378,
+            -0.0087313,
+            -0.12325,
+            -0.12553,
+            -0.025111,
+            -0.34684,
+            0.090213,
+            0.090778,
+            0.17802,
+            -0.13073,
+            0.19461,
+            0.1399,
+            0.17893,
+            -0.061272,
+            -0.1395,
+            0.24579,
+            -0.16463,
+            -0.048403,
+            0.16676,
+            0.05208,
+            -0.10289,
+            -0.27943,
+            0.19486,
+            0.16108,
+            0.11556,
+            -0.089569,
+            0.044216,
+            0.0051738,
+            -0.27863,
+            -0.040676,
+            0.33457,
+            -0.12432,
+            0.015818,
+            -0.19668,
+            0.059327,
+            0.0099601,
+            0.047709,
+            -0.017216,
+            0.042465,
+            0.1115,
+            0.16742,
+            -0.13082,
+            -0.024433,
+            0.10422,
+            -0.078588,
+            0.0058785,
+            -0.020883,
+            0.16015,
+            0.19779,
+            -0.30431
           ],
           "selected_hits": [
             0,
@@ -307,84 +307,84 @@
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
-            1,
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
-            1,
-            1,
-            0,
-            0,
-            0,
-            0,
             0,
             0,
             0,
@@ -2230,896 +2230,1792 @@
           "gene": "RHOT2",
           "score": 0.15184,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17267,
           "gene": "TUBAL3",
           "score": 0.080271,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18001,
           "gene": "XKRY2",
           "score": -0.2123,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3888,
           "gene": "DAB2IP",
           "score": 0.044769,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5887,
           "gene": "GAPT",
           "score": -0.011911,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12611,
           "gene": "PRAMEF2",
           "score": 0.20294,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7493,
           "gene": "IQCF3",
           "score": -0.044255,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9628,
           "gene": "MSANTD3-TMEFF1",
           "score": -0.09824,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 962,
           "gene": "ARHGEF2",
           "score": -0.034241,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7477,
           "gene": "IPO13",
           "score": -0.089332,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 292,
           "gene": "ADARB1",
           "score": 0.0072941,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3337,
           "gene": "COL4A4",
           "score": 0.079952,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5221,
           "gene": "FAM209A",
           "score": -0.048248,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17058,
           "gene": "TRIML2",
           "score": -0.011292,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10071,
           "gene": "NDUFB1",
           "score": -0.010165,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12573,
           "gene": "PPP3CB",
           "score": -0.011778,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13454,
           "gene": "RERGL",
           "score": 0.14828,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10835,
           "gene": "NonTarget.CTRL38",
           "score": -0.069151,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11901,
           "gene": "PGA3",
           "score": 0.17943,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2446,
           "gene": "CCNJL",
           "score": 0.14958,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11256,
           "gene": "OR5AN1",
           "score": 0.35942,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9401,
           "gene": "MMP16",
           "score": 0.052122,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5300,
           "gene": "FAM98B",
           "score": 0.16907,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3734,
           "gene": "CUL3",
           "score": 0.14949,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16969,
           "gene": "TREML4",
           "score": -0.4477,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2329,
           "gene": "CCDC28B",
           "score": 0.37577,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3150,
           "gene": "CLIC2",
           "score": 0.18831,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8977,
           "gene": "MAP3K3",
           "score": 0.066618,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10482,
           "gene": "NRG4",
           "score": 0.041164,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3589,
           "gene": "CSF2",
           "score": -0.050149,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9633,
           "gene": "MSH3",
           "score": -0.20566,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1159,
           "gene": "ATAT1",
           "score": 0.31263,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11445,
           "gene": "OXCT2",
           "score": 0.33819,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12821,
           "gene": "PRSS33",
           "score": -0.22276,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3193,
           "gene": "CLTRN",
           "score": -0.13725,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15853,
           "gene": "SYT1",
           "score": -0.15675,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15815,
           "gene": "SYCP2",
           "score": 0.02306,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6347,
           "gene": "GPR25",
           "score": 0.018811,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6281,
           "gene": "GPC2",
           "score": 0.29964,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4335,
           "gene": "DNAJC2",
           "score": 0.40151,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8587,
           "gene": "LOC729159",
           "score": -0.24846,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8246,
           "gene": "LAD1",
           "score": 0.33505,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1632,
           "gene": "BRMS1L",
           "score": -0.018266,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1440,
           "gene": "BCL11A",
           "score": 0.21109,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14493,
           "gene": "SH3TC1",
           "score": -0.3089,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1253,
           "gene": "ATP6AP1",
           "score": 0.30095,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10919,
           "gene": "OCA2",
           "score": -0.049326,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12274,
           "gene": "PLXDC1",
           "score": -0.2769,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15643,
           "gene": "STH",
           "score": -0.02723,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15068,
           "gene": "SMDT1",
           "score": 0.16957,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17954,
           "gene": "WNT8A",
           "score": 0.057329,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5016,
           "gene": "ESYT3",
           "score": -0.30907,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7761,
           "gene": "KCNJ3",
           "score": -0.016158,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16055,
           "gene": "TBRG1",
           "score": -0.21505,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15133,
           "gene": "SNAP29",
           "score": -0.23827,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11489,
           "gene": "PABPC3",
           "score": -0.21966,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1446,
           "gene": "BCL2L11",
           "score": 0.33719,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9244,
           "gene": "METTL6",
           "score": -0.2162,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5241,
           "gene": "FAM227B",
           "score": -0.18169,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 308,
           "gene": "ADCY9",
           "score": 0.15946,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7426,
           "gene": "INO80E",
           "score": -0.12583,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 483,
           "gene": "AK7",
           "score": -0.053844,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18470,
           "gene": "ZNF428",
           "score": 0.043155,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18041,
           "gene": "YIF1B",
           "score": -0.14187,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12289,
           "gene": "PMEL",
           "score": 0.0077955,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16386,
           "gene": "TLCD3B",
           "score": -0.22864,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 643,
           "gene": "ANAPC4",
           "score": 0.13634,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16004,
           "gene": "TBC1D15",
           "score": -0.044763,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14212,
           "gene": "SDHA",
           "score": 0.19929,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14726,
           "gene": "SLC25A19",
           "score": 0.008568,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6788,
           "gene": "HERC3",
           "score": -0.01863,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18826,
           "gene": "ZSCAN20",
           "score": 0.1752,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8714,
           "gene": "LRRC7",
           "score": -0.064914,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18066,
           "gene": "YTHDF3",
           "score": -0.062509,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4882,
           "gene": "EP400",
           "score": -0.071699,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15636,
           "gene": "STC2",
           "score": -0.059057,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9749,
           "gene": "MUC13",
           "score": 0.14463,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5784,
           "gene": "FZD1",
           "score": -0.1079,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 792,
           "gene": "AP1S2",
           "score": -0.37582,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6556,
           "gene": "GUK1",
           "score": 0.53392,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 669,
           "gene": "ANKFY1",
           "score": 0.1186,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18588,
           "gene": "ZNF586",
           "score": 0.050891,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17567,
           "gene": "USH1G",
           "score": -0.035439,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7070,
           "gene": "HSPA12B",
           "score": -0.1018,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18850,
           "gene": "ZW10",
           "score": 0.10344,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7847,
           "gene": "KDR",
           "score": 0.085495,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3497,
           "gene": "CRACR2A",
           "score": 0.028925,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15790,
           "gene": "SUSD6",
           "score": 0.068816,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1457,
           "gene": "BCL7B",
           "score": 0.095651,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10930,
           "gene": "ODAD2",
           "score": 0.29212,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3379,
           "gene": "COPG1",
           "score": 0.16188,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1589,
           "gene": "BORCS5",
           "score": -0.090122,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 54,
           "gene": "ABCC12",
           "score": 0.068198,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 694,
           "gene": "ANKRD20A2",
           "score": 0.19531,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1464,
           "gene": "BCO2",
           "score": 0.27607,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1465,
           "gene": "BCOR",
           "score": -0.2411,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8507,
           "gene": "LMOD2",
           "score": -0.0378,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18748,
           "gene": "ZNF805",
           "score": 0.052151,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6980,
           "gene": "HOXC13",
           "score": -0.13105,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4293,
           "gene": "DNAH14",
           "score": 0.10655,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1478,
           "gene": "BEND3",
           "score": -0.1477,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17348,
           "gene": "UBA3",
           "score": 0.075581,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1225,
           "gene": "ATP2A3",
           "score": -0.21116,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8266,
           "gene": "LAMTOR1",
           "score": 0.14123,
           "hit": 0,
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
           "candidate_index": 5707,
           "gene": "FRMD6",
           "score": 0.074162,
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
           "candidate_index": 2645,
           "gene": "CDK12",
           "score": -0.014396,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5590,
           "gene": "FMN2",
           "score": -0.17091,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4565,
           "gene": "DZIP1L",
           "score": -0.052318,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12635,
           "gene": "PRDM2",
           "score": 0.09734,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18140,
           "gene": "ZC3H13",
           "score": 0.054432,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14685,
           "gene": "SLC22A10",
           "score": 0.094775,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18012,
           "gene": "XPOT",
           "score": -0.084016,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18274,
           "gene": "ZMAT5",
           "score": 0.11764,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2790,
           "gene": "CEP43",
           "score": 0.063922,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4073,
           "gene": "DEFB112",
           "score": -0.019297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 362,
           "gene": "ADNP",
           "score": -0.085647,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14955,
           "gene": "SLC6A6",
           "score": 0.065536,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3824,
           "gene": "CYP26C1",
           "score": 0.27422,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2036,
           "gene": "CAB39L",
           "score": 0.33077,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16509,
           "gene": "TMEM141",
           "score": 0.22945,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9850,
           "gene": "MYO1E",
           "score": -0.026485667,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17275,
           "gene": "TUBB8",
           "score": -0.28545,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15356,
           "gene": "SPDL1",
           "score": 0.12938,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15869,
           "gene": "SYT9",
           "score": -0.10176,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4862,
           "gene": "ENSA",
           "score": -0.18372,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12579,
           "gene": "PPP4R2",
           "score": -0.061497,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 9109,
+          "gene": "MCM3AP",
+          "score": -0.00063426,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13964,
+          "gene": "RTL9",
+          "score": 0.17401,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16312,
+          "gene": "THRA",
+          "score": -0.074542,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8630,
+          "gene": "LRCH4",
+          "score": 0.10734145,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2751,
+          "gene": "CENPF",
+          "score": -0.18355,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10150,
+          "gene": "NEURL1",
+          "score": 0.16434,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11332,
+          "gene": "OR7D2",
+          "score": -0.38256,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 722,
+          "gene": "ANKRD50",
+          "score": -0.11363,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2429,
+          "gene": "CCNB1IP1",
+          "score": -0.28364,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16188,
+          "gene": "TERT",
+          "score": 0.040836,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 369,
+          "gene": "ADPGK",
+          "score": 0.044493,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3863,
+          "gene": "CYP51A1",
+          "score": 0.072361,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9508,
+          "gene": "MRGPRD",
+          "score": 0.073169,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3958,
+          "gene": "DCHS2",
+          "score": 0.05212,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10412,
+          "gene": "NPIPB3",
+          "score": 0.050308,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1195,
+          "gene": "ATOH1",
+          "score": 0.12806,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2237,
+          "gene": "CBS",
+          "score": 0.18808,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4538,
+          "gene": "DYNC1I1",
+          "score": 0.24858,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9098,
+          "gene": "MCEMP1",
+          "score": -0.30723,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5178,
+          "gene": "FAM157A",
+          "score": 0.032134,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7077,
+          "gene": "HSPA4",
+          "score": 0.023713,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14319,
+          "gene": "SEPTIN5",
+          "score": -0.066519,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2516,
+          "gene": "CD300A",
+          "score": 0.13193,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13646,
+          "gene": "RNASE6",
+          "score": 0.088345,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4799,
+          "gene": "ELP4",
+          "score": -0.14311,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1918,
+          "gene": "C3orf20",
+          "score": 0.064214,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1077,
+          "gene": "ART4",
+          "score": -0.1008235,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5789,
+          "gene": "FZD6",
+          "score": -0.030256,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10730,
+          "gene": "NonTarget.CTRL169",
+          "score": 0.018037,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8437,
+          "gene": "LIMA1",
+          "score": 0.018931,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11925,
+          "gene": "PGLYRP1",
+          "score": -0.099904,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10709,
+          "gene": "NonTarget.CTRL15",
+          "score": 0.032215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3148,
+          "gene": "CLHC1",
+          "score": -0.0094774,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13755,
+          "gene": "ROBO4",
+          "score": 0.064095,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3016,
+          "gene": "CIAO1",
+          "score": -0.10199,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 710,
+          "gene": "ANKRD34C",
+          "score": 0.214,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10992,
+          "gene": "OPRM1",
+          "score": -0.1572,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10609,
+          "gene": "NUP50",
+          "score": 0.16105,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12939,
+          "gene": "PTCHD1",
+          "score": -0.040209,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17739,
+          "gene": "VN1R4",
+          "score": -0.13521,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17948,
+          "gene": "WNT4",
+          "score": -0.19902,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8517,
+          "gene": "LOC100129083",
+          "score": -0.30715,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2005,
+          "gene": "C9orf139",
+          "score": -0.094607,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16470,
+          "gene": "TMEM104",
+          "score": -0.028552,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10251,
+          "gene": "NKAIN4",
+          "score": -0.074582,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17425,
+          "gene": "UBR3",
+          "score": 0.19457,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1023,
+          "gene": "ARMC12",
+          "score": -0.071949,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6687,
+          "gene": "HARBI1",
+          "score": -0.20856,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12324,
+          "gene": "PNPLA2",
+          "score": -0.16671,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15915,
+          "gene": "TAF4B",
+          "score": -0.054785,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2609,
+          "gene": "CDCA7L",
+          "score": 0.16011,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6203,
+          "gene": "GNPDA1",
+          "score": 0.013369666,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4165,
+          "gene": "DHPS",
+          "score": 0.33435,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2121,
+          "gene": "CAMKK1",
+          "score": -0.0064197,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16979,
+          "gene": "TRIB3",
+          "score": -0.067502,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16981,
+          "gene": "TRIM10",
+          "score": -0.036856,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16985,
+          "gene": "TRIM15",
+          "score": -0.14994,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4188,
+          "gene": "DHX35",
+          "score": 0.0056604,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4701,
+          "gene": "EID2B",
+          "score": 0.2206,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14945,
+          "gene": "SLC6A14",
+          "score": -0.19918,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2665,
+          "gene": "CDK6",
+          "score": -0.25727,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9835,
+          "gene": "MYLK",
+          "score": 0.20458,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4207,
+          "gene": "DIP2B",
+          "score": 0.033532,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13426,
+          "gene": "REEP2",
+          "score": -0.11722,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5747,
+          "gene": "FUBP1",
+          "score": 0.073863,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5267,
+          "gene": "FAM47E-STBD1",
+          "score": 0.034035,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12949,
+          "gene": "PTGDR2",
+          "score": -0.17351,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18079,
+          "gene": "ZAR1",
+          "score": -0.11831,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4260,
+          "gene": "DMD",
+          "score": 0.070553,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17069,
+          "gene": "TRIT1",
+          "score": -0.22555,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13998,
+          "gene": "RUVBL2",
+          "score": -0.077556,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10426,
+          "gene": "NPRL2",
+          "score": -0.089705,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8381,
+          "gene": "LGALS13",
+          "score": 0.0588155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15039,
+          "gene": "SMAGP",
+          "score": 0.096038,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16066,
+          "gene": "TBX3",
+          "score": 0.036567,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15554,
+          "gene": "SSR1",
+          "score": 0.2042,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6353,
+          "gene": "GPR33",
+          "score": 0.029664,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17619,
+          "gene": "USP36",
+          "score": 0.032612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3797,
+          "gene": "CYB5R4",
+          "score": -0.14378,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4312,
+          "gene": "DNAJB11",
+          "score": -0.0087313,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4828,
+          "gene": "EMP3",
+          "score": -0.12325,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7905,
+          "gene": "KIF21A",
+          "score": -0.12553,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1264,
+          "gene": "ATP6V0E2",
+          "score": -0.025111,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3312,
+          "gene": "COL11A2",
+          "score": -0.34684,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 11506,
+          "gene": "PADI4",
+          "score": 0.090213,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5363,
+          "gene": "FBXL2",
+          "score": 0.090778,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1782,
+          "gene": "C17orf58",
+          "score": 0.17802,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9995,
+          "gene": "NCAPH2",
+          "score": -0.13073,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8972,
+          "gene": "MAP3K15",
+          "score": 0.19461,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 270,
+          "gene": "ADAMTS15",
+          "score": 0.1399,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18205,
+          "gene": "ZFC3H1",
+          "score": 0.17893,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1317,
+          "gene": "AVIL",
+          "score": -0.061272,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8997,
+          "gene": "MAP9",
+          "score": -0.1395,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10534,
+          "gene": "NTAN1",
+          "score": 0.24579,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10032,
+          "gene": "NDE1",
+          "score": -0.16463,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9009,
+          "gene": "MAPK7",
+          "score": -0.048403,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8497,
+          "gene": "LMNB2",
+          "score": 0.16676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8514,
+          "gene": "LNPK",
+          "score": 0.05208,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15684,
+          "gene": "STON2",
+          "score": -0.10289,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10571,
+          "gene": "NUDT14",
+          "score": -0.27943,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4442,
+          "gene": "DPYD",
+          "score": 0.19486,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1886,
+          "gene": "C2CD2",
+          "score": 0.16108,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1897,
+          "gene": "C2orf27A",
+          "score": 0.11556,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18795,
+          "gene": "ZNG1B",
+          "score": -0.089569,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4461,
+          "gene": "DRG2",
+          "score": 0.044216,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13165,
+          "gene": "RAB6C",
+          "score": 0.0051738,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6010,
+          "gene": "GFOD2",
+          "score": -0.27863,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1404,
+          "gene": "BAZ1A",
+          "score": -0.040676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16767,
+          "gene": "TNFRSF17",
+          "score": 0.33457,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11651,
+          "gene": "PCDHA10",
+          "score": -0.12432,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9623,
+          "gene": "MS4A6A",
+          "score": 0.015818,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13213,
+          "gene": "RAET1L",
+          "score": -0.19668,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9119,
+          "gene": "MCOLN2",
+          "score": 0.059327,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15265,
+          "gene": "SP140",
+          "score": 0.0099601,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5031,
+          "gene": "ETV2",
+          "score": 0.047709,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 426,
+          "gene": "AGMAT",
+          "score": -0.017216,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6571,
+          "gene": "GZMB",
+          "score": 0.042465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2482,
+          "gene": "CD109",
+          "score": 0.1115,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5561,
+          "gene": "FKBPL",
+          "score": 0.16742,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6595,
+          "gene": "H2AC17",
+          "score": -0.13082,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10188,
+          "gene": "NFKBID",
+          "score": -0.024433,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17383,
+          "gene": "UBE2K",
+          "score": 0.10422,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4589,
+          "gene": "ECE1",
+          "score": -0.078588,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7661,
+          "gene": "JPH4",
+          "score": 0.0058785,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16367,
+          "gene": "TINAG",
+          "score": -0.020883,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18416,
+          "gene": "ZNF326",
+          "score": 0.16015,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2042,
+          "gene": "CABP4",
+          "score": 0.19779,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2559,
+          "gene": "CD82",
+          "score": -0.30431,
+          "hit": 0,
+          "round": 3
         }
       ],
       "queried_history": [
@@ -4920,896 +5816,1792 @@
           "gene": "RHOT2",
           "score": 0.15184,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17267,
           "gene": "TUBAL3",
           "score": 0.080271,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18001,
           "gene": "XKRY2",
           "score": -0.2123,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3888,
           "gene": "DAB2IP",
           "score": 0.044769,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5887,
           "gene": "GAPT",
           "score": -0.011911,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12611,
           "gene": "PRAMEF2",
           "score": 0.20294,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7493,
           "gene": "IQCF3",
           "score": -0.044255,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9628,
           "gene": "MSANTD3-TMEFF1",
           "score": -0.09824,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 962,
           "gene": "ARHGEF2",
           "score": -0.034241,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7477,
           "gene": "IPO13",
           "score": -0.089332,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 292,
           "gene": "ADARB1",
           "score": 0.0072941,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3337,
           "gene": "COL4A4",
           "score": 0.079952,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5221,
           "gene": "FAM209A",
           "score": -0.048248,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17058,
           "gene": "TRIML2",
           "score": -0.011292,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10071,
           "gene": "NDUFB1",
           "score": -0.010165,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12573,
           "gene": "PPP3CB",
           "score": -0.011778,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13454,
           "gene": "RERGL",
           "score": 0.14828,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10835,
           "gene": "NonTarget.CTRL38",
           "score": -0.069151,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11901,
           "gene": "PGA3",
           "score": 0.17943,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2446,
           "gene": "CCNJL",
           "score": 0.14958,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11256,
           "gene": "OR5AN1",
           "score": 0.35942,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9401,
           "gene": "MMP16",
           "score": 0.052122,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5300,
           "gene": "FAM98B",
           "score": 0.16907,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3734,
           "gene": "CUL3",
           "score": 0.14949,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16969,
           "gene": "TREML4",
           "score": -0.4477,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2329,
           "gene": "CCDC28B",
           "score": 0.37577,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3150,
           "gene": "CLIC2",
           "score": 0.18831,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8977,
           "gene": "MAP3K3",
           "score": 0.066618,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10482,
           "gene": "NRG4",
           "score": 0.041164,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3589,
           "gene": "CSF2",
           "score": -0.050149,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9633,
           "gene": "MSH3",
           "score": -0.20566,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1159,
           "gene": "ATAT1",
           "score": 0.31263,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11445,
           "gene": "OXCT2",
           "score": 0.33819,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12821,
           "gene": "PRSS33",
           "score": -0.22276,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3193,
           "gene": "CLTRN",
           "score": -0.13725,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15853,
           "gene": "SYT1",
           "score": -0.15675,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15815,
           "gene": "SYCP2",
           "score": 0.02306,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6347,
           "gene": "GPR25",
           "score": 0.018811,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6281,
           "gene": "GPC2",
           "score": 0.29964,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4335,
           "gene": "DNAJC2",
           "score": 0.40151,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8587,
           "gene": "LOC729159",
           "score": -0.24846,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8246,
           "gene": "LAD1",
           "score": 0.33505,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1632,
           "gene": "BRMS1L",
           "score": -0.018266,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1440,
           "gene": "BCL11A",
           "score": 0.21109,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14493,
           "gene": "SH3TC1",
           "score": -0.3089,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1253,
           "gene": "ATP6AP1",
           "score": 0.30095,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10919,
           "gene": "OCA2",
           "score": -0.049326,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12274,
           "gene": "PLXDC1",
           "score": -0.2769,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15643,
           "gene": "STH",
           "score": -0.02723,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15068,
           "gene": "SMDT1",
           "score": 0.16957,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17954,
           "gene": "WNT8A",
           "score": 0.057329,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5016,
           "gene": "ESYT3",
           "score": -0.30907,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7761,
           "gene": "KCNJ3",
           "score": -0.016158,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16055,
           "gene": "TBRG1",
           "score": -0.21505,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15133,
           "gene": "SNAP29",
           "score": -0.23827,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11489,
           "gene": "PABPC3",
           "score": -0.21966,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1446,
           "gene": "BCL2L11",
           "score": 0.33719,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9244,
           "gene": "METTL6",
           "score": -0.2162,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5241,
           "gene": "FAM227B",
           "score": -0.18169,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 308,
           "gene": "ADCY9",
           "score": 0.15946,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7426,
           "gene": "INO80E",
           "score": -0.12583,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 483,
           "gene": "AK7",
           "score": -0.053844,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18470,
           "gene": "ZNF428",
           "score": 0.043155,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18041,
           "gene": "YIF1B",
           "score": -0.14187,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12289,
           "gene": "PMEL",
           "score": 0.0077955,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16386,
           "gene": "TLCD3B",
           "score": -0.22864,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 643,
           "gene": "ANAPC4",
           "score": 0.13634,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16004,
           "gene": "TBC1D15",
           "score": -0.044763,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14212,
           "gene": "SDHA",
           "score": 0.19929,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14726,
           "gene": "SLC25A19",
           "score": 0.008568,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6788,
           "gene": "HERC3",
           "score": -0.01863,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18826,
           "gene": "ZSCAN20",
           "score": 0.1752,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8714,
           "gene": "LRRC7",
           "score": -0.064914,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18066,
           "gene": "YTHDF3",
           "score": -0.062509,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4882,
           "gene": "EP400",
           "score": -0.071699,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15636,
           "gene": "STC2",
           "score": -0.059057,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9749,
           "gene": "MUC13",
           "score": 0.14463,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5784,
           "gene": "FZD1",
           "score": -0.1079,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 792,
           "gene": "AP1S2",
           "score": -0.37582,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6556,
           "gene": "GUK1",
           "score": 0.53392,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 669,
           "gene": "ANKFY1",
           "score": 0.1186,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18588,
           "gene": "ZNF586",
           "score": 0.050891,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17567,
           "gene": "USH1G",
           "score": -0.035439,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7070,
           "gene": "HSPA12B",
           "score": -0.1018,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18850,
           "gene": "ZW10",
           "score": 0.10344,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7847,
           "gene": "KDR",
           "score": 0.085495,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3497,
           "gene": "CRACR2A",
           "score": 0.028925,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15790,
           "gene": "SUSD6",
           "score": 0.068816,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1457,
           "gene": "BCL7B",
           "score": 0.095651,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10930,
           "gene": "ODAD2",
           "score": 0.29212,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3379,
           "gene": "COPG1",
           "score": 0.16188,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1589,
           "gene": "BORCS5",
           "score": -0.090122,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 54,
           "gene": "ABCC12",
           "score": 0.068198,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 694,
           "gene": "ANKRD20A2",
           "score": 0.19531,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1464,
           "gene": "BCO2",
           "score": 0.27607,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1465,
           "gene": "BCOR",
           "score": -0.2411,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8507,
           "gene": "LMOD2",
           "score": -0.0378,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18748,
           "gene": "ZNF805",
           "score": 0.052151,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6980,
           "gene": "HOXC13",
           "score": -0.13105,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4293,
           "gene": "DNAH14",
           "score": 0.10655,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1478,
           "gene": "BEND3",
           "score": -0.1477,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17348,
           "gene": "UBA3",
           "score": 0.075581,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1225,
           "gene": "ATP2A3",
           "score": -0.21116,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8266,
           "gene": "LAMTOR1",
           "score": 0.14123,
           "hit": 0,
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
           "candidate_index": 5707,
           "gene": "FRMD6",
           "score": 0.074162,
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
           "candidate_index": 2645,
           "gene": "CDK12",
           "score": -0.014396,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5590,
           "gene": "FMN2",
           "score": -0.17091,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4565,
           "gene": "DZIP1L",
           "score": -0.052318,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12635,
           "gene": "PRDM2",
           "score": 0.09734,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18140,
           "gene": "ZC3H13",
           "score": 0.054432,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14685,
           "gene": "SLC22A10",
           "score": 0.094775,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18012,
           "gene": "XPOT",
           "score": -0.084016,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18274,
           "gene": "ZMAT5",
           "score": 0.11764,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2790,
           "gene": "CEP43",
           "score": 0.063922,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4073,
           "gene": "DEFB112",
           "score": -0.019297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 362,
           "gene": "ADNP",
           "score": -0.085647,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14955,
           "gene": "SLC6A6",
           "score": 0.065536,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3824,
           "gene": "CYP26C1",
           "score": 0.27422,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2036,
           "gene": "CAB39L",
           "score": 0.33077,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16509,
           "gene": "TMEM141",
           "score": 0.22945,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9850,
           "gene": "MYO1E",
           "score": -0.026485667,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17275,
           "gene": "TUBB8",
           "score": -0.28545,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15356,
           "gene": "SPDL1",
           "score": 0.12938,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15869,
           "gene": "SYT9",
           "score": -0.10176,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4862,
           "gene": "ENSA",
           "score": -0.18372,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12579,
           "gene": "PPP4R2",
           "score": -0.061497,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 9109,
+          "gene": "MCM3AP",
+          "score": -0.00063426,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13964,
+          "gene": "RTL9",
+          "score": 0.17401,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16312,
+          "gene": "THRA",
+          "score": -0.074542,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8630,
+          "gene": "LRCH4",
+          "score": 0.10734145,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2751,
+          "gene": "CENPF",
+          "score": -0.18355,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10150,
+          "gene": "NEURL1",
+          "score": 0.16434,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11332,
+          "gene": "OR7D2",
+          "score": -0.38256,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 722,
+          "gene": "ANKRD50",
+          "score": -0.11363,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2429,
+          "gene": "CCNB1IP1",
+          "score": -0.28364,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16188,
+          "gene": "TERT",
+          "score": 0.040836,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 369,
+          "gene": "ADPGK",
+          "score": 0.044493,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3863,
+          "gene": "CYP51A1",
+          "score": 0.072361,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9508,
+          "gene": "MRGPRD",
+          "score": 0.073169,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3958,
+          "gene": "DCHS2",
+          "score": 0.05212,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10412,
+          "gene": "NPIPB3",
+          "score": 0.050308,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1195,
+          "gene": "ATOH1",
+          "score": 0.12806,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2237,
+          "gene": "CBS",
+          "score": 0.18808,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4538,
+          "gene": "DYNC1I1",
+          "score": 0.24858,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9098,
+          "gene": "MCEMP1",
+          "score": -0.30723,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5178,
+          "gene": "FAM157A",
+          "score": 0.032134,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7077,
+          "gene": "HSPA4",
+          "score": 0.023713,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14319,
+          "gene": "SEPTIN5",
+          "score": -0.066519,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2516,
+          "gene": "CD300A",
+          "score": 0.13193,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13646,
+          "gene": "RNASE6",
+          "score": 0.088345,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4799,
+          "gene": "ELP4",
+          "score": -0.14311,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1918,
+          "gene": "C3orf20",
+          "score": 0.064214,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1077,
+          "gene": "ART4",
+          "score": -0.1008235,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5789,
+          "gene": "FZD6",
+          "score": -0.030256,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10730,
+          "gene": "NonTarget.CTRL169",
+          "score": 0.018037,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8437,
+          "gene": "LIMA1",
+          "score": 0.018931,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11925,
+          "gene": "PGLYRP1",
+          "score": -0.099904,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10709,
+          "gene": "NonTarget.CTRL15",
+          "score": 0.032215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3148,
+          "gene": "CLHC1",
+          "score": -0.0094774,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13755,
+          "gene": "ROBO4",
+          "score": 0.064095,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3016,
+          "gene": "CIAO1",
+          "score": -0.10199,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 710,
+          "gene": "ANKRD34C",
+          "score": 0.214,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10992,
+          "gene": "OPRM1",
+          "score": -0.1572,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10609,
+          "gene": "NUP50",
+          "score": 0.16105,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12939,
+          "gene": "PTCHD1",
+          "score": -0.040209,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17739,
+          "gene": "VN1R4",
+          "score": -0.13521,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17948,
+          "gene": "WNT4",
+          "score": -0.19902,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8517,
+          "gene": "LOC100129083",
+          "score": -0.30715,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2005,
+          "gene": "C9orf139",
+          "score": -0.094607,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16470,
+          "gene": "TMEM104",
+          "score": -0.028552,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10251,
+          "gene": "NKAIN4",
+          "score": -0.074582,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17425,
+          "gene": "UBR3",
+          "score": 0.19457,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1023,
+          "gene": "ARMC12",
+          "score": -0.071949,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6687,
+          "gene": "HARBI1",
+          "score": -0.20856,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12324,
+          "gene": "PNPLA2",
+          "score": -0.16671,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15915,
+          "gene": "TAF4B",
+          "score": -0.054785,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2609,
+          "gene": "CDCA7L",
+          "score": 0.16011,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6203,
+          "gene": "GNPDA1",
+          "score": 0.013369666,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4165,
+          "gene": "DHPS",
+          "score": 0.33435,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2121,
+          "gene": "CAMKK1",
+          "score": -0.0064197,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16979,
+          "gene": "TRIB3",
+          "score": -0.067502,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16981,
+          "gene": "TRIM10",
+          "score": -0.036856,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16985,
+          "gene": "TRIM15",
+          "score": -0.14994,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4188,
+          "gene": "DHX35",
+          "score": 0.0056604,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4701,
+          "gene": "EID2B",
+          "score": 0.2206,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14945,
+          "gene": "SLC6A14",
+          "score": -0.19918,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2665,
+          "gene": "CDK6",
+          "score": -0.25727,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9835,
+          "gene": "MYLK",
+          "score": 0.20458,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4207,
+          "gene": "DIP2B",
+          "score": 0.033532,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13426,
+          "gene": "REEP2",
+          "score": -0.11722,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5747,
+          "gene": "FUBP1",
+          "score": 0.073863,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5267,
+          "gene": "FAM47E-STBD1",
+          "score": 0.034035,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12949,
+          "gene": "PTGDR2",
+          "score": -0.17351,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18079,
+          "gene": "ZAR1",
+          "score": -0.11831,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4260,
+          "gene": "DMD",
+          "score": 0.070553,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17069,
+          "gene": "TRIT1",
+          "score": -0.22555,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13998,
+          "gene": "RUVBL2",
+          "score": -0.077556,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10426,
+          "gene": "NPRL2",
+          "score": -0.089705,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8381,
+          "gene": "LGALS13",
+          "score": 0.0588155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15039,
+          "gene": "SMAGP",
+          "score": 0.096038,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16066,
+          "gene": "TBX3",
+          "score": 0.036567,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15554,
+          "gene": "SSR1",
+          "score": 0.2042,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6353,
+          "gene": "GPR33",
+          "score": 0.029664,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17619,
+          "gene": "USP36",
+          "score": 0.032612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3797,
+          "gene": "CYB5R4",
+          "score": -0.14378,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4312,
+          "gene": "DNAJB11",
+          "score": -0.0087313,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4828,
+          "gene": "EMP3",
+          "score": -0.12325,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7905,
+          "gene": "KIF21A",
+          "score": -0.12553,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1264,
+          "gene": "ATP6V0E2",
+          "score": -0.025111,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3312,
+          "gene": "COL11A2",
+          "score": -0.34684,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 11506,
+          "gene": "PADI4",
+          "score": 0.090213,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5363,
+          "gene": "FBXL2",
+          "score": 0.090778,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1782,
+          "gene": "C17orf58",
+          "score": 0.17802,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9995,
+          "gene": "NCAPH2",
+          "score": -0.13073,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8972,
+          "gene": "MAP3K15",
+          "score": 0.19461,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 270,
+          "gene": "ADAMTS15",
+          "score": 0.1399,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18205,
+          "gene": "ZFC3H1",
+          "score": 0.17893,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1317,
+          "gene": "AVIL",
+          "score": -0.061272,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8997,
+          "gene": "MAP9",
+          "score": -0.1395,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10534,
+          "gene": "NTAN1",
+          "score": 0.24579,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10032,
+          "gene": "NDE1",
+          "score": -0.16463,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9009,
+          "gene": "MAPK7",
+          "score": -0.048403,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8497,
+          "gene": "LMNB2",
+          "score": 0.16676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8514,
+          "gene": "LNPK",
+          "score": 0.05208,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15684,
+          "gene": "STON2",
+          "score": -0.10289,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10571,
+          "gene": "NUDT14",
+          "score": -0.27943,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4442,
+          "gene": "DPYD",
+          "score": 0.19486,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1886,
+          "gene": "C2CD2",
+          "score": 0.16108,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1897,
+          "gene": "C2orf27A",
+          "score": 0.11556,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18795,
+          "gene": "ZNG1B",
+          "score": -0.089569,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4461,
+          "gene": "DRG2",
+          "score": 0.044216,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13165,
+          "gene": "RAB6C",
+          "score": 0.0051738,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6010,
+          "gene": "GFOD2",
+          "score": -0.27863,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1404,
+          "gene": "BAZ1A",
+          "score": -0.040676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16767,
+          "gene": "TNFRSF17",
+          "score": 0.33457,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11651,
+          "gene": "PCDHA10",
+          "score": -0.12432,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9623,
+          "gene": "MS4A6A",
+          "score": 0.015818,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13213,
+          "gene": "RAET1L",
+          "score": -0.19668,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9119,
+          "gene": "MCOLN2",
+          "score": 0.059327,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15265,
+          "gene": "SP140",
+          "score": 0.0099601,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5031,
+          "gene": "ETV2",
+          "score": 0.047709,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 426,
+          "gene": "AGMAT",
+          "score": -0.017216,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6571,
+          "gene": "GZMB",
+          "score": 0.042465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2482,
+          "gene": "CD109",
+          "score": 0.1115,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5561,
+          "gene": "FKBPL",
+          "score": 0.16742,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6595,
+          "gene": "H2AC17",
+          "score": -0.13082,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10188,
+          "gene": "NFKBID",
+          "score": -0.024433,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17383,
+          "gene": "UBE2K",
+          "score": 0.10422,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4589,
+          "gene": "ECE1",
+          "score": -0.078588,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7661,
+          "gene": "JPH4",
+          "score": 0.0058785,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16367,
+          "gene": "TINAG",
+          "score": -0.020883,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18416,
+          "gene": "ZNF326",
+          "score": 0.16015,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2042,
+          "gene": "CABP4",
+          "score": 0.19779,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2559,
+          "gene": "CD82",
+          "score": -0.30431,
+          "hit": 0,
+          "round": 3
         }
       ]
     }

```
