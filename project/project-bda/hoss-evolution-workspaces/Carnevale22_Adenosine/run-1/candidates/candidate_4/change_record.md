# Change Record — candidate_4

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Carnevale22_Adenosine/run-1/best/current/harness
Generated at: 2026-04-30T06:50:52.483542

## Files Changed

- model.py: modified (added=13, deleted=6, delta=7)
- outputs/metrics.json: modified (added=2381, deleted=589, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -56,14 +56,21 @@
     # Exploration: random sampling
     explore_indices = rng.sample(available, min(num_explore, len(available)))
     
-    # Exploitation: select based on scores
+    # Exploitation: select based on hits first, then scores
     if len(history) > 0 and num_exploit > 0:
-        # For this task, NEGATIVE scores are better (boost T cell proliferation)
-        # Sort history by score (ascending to prioritize negative scores)
-        sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
+        # Check if we have hits in history
+        hits = [h for h in history if h.get('hit', 0) == 1]
         
-        # Get top performers (most negative scores)
-        top_performers = [h['candidate_index'] for h in sorted_history[:min(50, len(sorted_history))]]
+        if len(hits) > 0:
+            # Prioritize hit genes (they're confirmed to boost T cell proliferation)
+            # Sort hits by score (ascending to prioritize most negative)
+            sorted_hits = sorted(hits, key=lambda x: x['score'], reverse=False)
+            top_performers = [h['candidate_index'] for h in sorted_hits[:min(50, len(sorted_hits))]]
+        else:
+            # Fall back to best scores if no hits yet
+            # For this task, NEGATIVE scores are better (boost T cell proliferation)
+            sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
+            top_performers = [h['candidate_index'] for h in sorted_history[:min(50, len(sorted_history))]]
         
         # Find candidates similar to top performers (if gene search available)
         exploit_candidates = set()

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
-      "baseline_total_hits": 2,
+      "baseline_total_queries": 256,
+      "baseline_total_hits": 7,
       "delta_queries": 128,
-      "delta_hits": 5,
-      "total_queries": 256,
-      "total_hits": 7,
+      "delta_hits": 8,
+      "total_queries": 384,
+      "total_hits": 15,
       "top_k": 943,
       "hit_curve": {
         "queries": [
-          128,
-          256
+          256,
+          384
         ],
         "hits": [
-          2,
-          7
+          7,
+          15
         ]
       },
-      "auc": 576.0,
-      "auc_normalized": 0.0023860021208907743,
-      "ncg": 0.23323368332888017,
+      "auc": 1408.0,
+      "auc_normalized": 0.003888299752562743,
+      "ncg": 0.25772253765769115,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 5,
-          "cumulative_hits": 7,
-          "precision_at_batch": 0.0390625,
+          "hits": 8,
+          "cumulative_hits": 15,
+          "precision_at_batch": 0.0625,
           "selected": [
-            "ATP6V1E1",
-            "MON1A",
-            "EIF5A",
-            "SP140L",
-            "PLEKHF2",
-            "CLPSL2",
-            "SLC6A8",
-            "TMC3",
-            "AMY1B",
-            "TRARG1",
-            "SELENOP",
-            "PMEPA1",
-            "YIPF4",
-            "SERF1A",
-            "PTPRC",
-            "GABRA4",
-            "C2orf68",
-            "CRLS1",
-            "DENND4B",
-            "POM121L2",
-            "EXOC4",
-            "CLK2",
-            "FAM9B",
-            "TPRA1",
-            "TIMP3",
-            "DLX1",
-            "PRR20A",
-            "TMPRSS11B",
-            "MAP3K5",
-            "GET3",
-            "POU2F1",
-            "CALHM1",
-            "BRCA2",
-            "C9orf78",
-            "GMPR",
-            "CA14",
-            "FFAR1",
-            "MXRA5",
-            "MC5R",
-            "CD5",
-            "TTC4",
-            "COQ9",
-            "C9orf50",
-            "CLDN25",
-            "SMIM8",
-            "ODAPH",
-            "NonTarget.CTRL95",
-            "UCK2",
-            "SH3GL1",
-            "FGFR1OP2",
-            "DHRS2",
-            "CDK11B",
-            "NTRK2",
-            "BTBD1",
-            "MAB21L1",
-            "PLA2G6",
-            "GLUL",
-            "CCDC187",
-            "ZFP1",
-            "CUTC",
-            "MYH1",
-            "TIAM2",
-            "PGPEP1",
-            "SERAC1",
-            "B4GALT6",
-            "STAMBPL1",
-            "RNF167",
-            "CENPN",
-            "PDRG1",
-            "DIABLO",
-            "CFAP299",
-            "EXTL2",
-            "NEURL2",
-            "CSGALNACT2",
-            "UTP3",
-            "S100A13",
-            "SLC10A7",
-            "ATP5PO",
-            "ENDOD1",
-            "ABHD14B",
-            "CR1L",
-            "DENND1B",
-            "DHDH",
-            "ZNF350",
-            "SLC35G5",
-            "TPP2",
-            "ANGEL1",
-            "SPEM1",
-            "ZDHHC4",
-            "STBD1",
-            "DLK2",
-            "ZER1",
-            "FYCO1",
-            "WNT2",
-            "ADAMTS9",
-            "VWF",
-            "MFAP1",
-            "TXNDC17",
-            "SNF8",
-            "NLRP1",
-            "CDH10",
-            "RGL1",
-            "ZNF808",
-            "SPAM1",
-            "ZNF469",
-            "USP18",
-            "ZNF814",
-            "DPP3",
-            "FARP1",
-            "TRPM4",
-            "PRCP",
-            "CAND1",
-            "IGFBP2",
-            "CLMN",
-            "PSMC4",
-            "SNX27",
-            "CCL17",
-            "CDK2AP1",
-            "ARL16",
-            "CD47",
-            "CA4",
-            "CAPZA2",
-            "PDCD7",
-            "FBXL18",
-            "ECHDC3",
-            "TUBB2B",
-            "SIVA1",
-            "WFDC8"
+            "RHOT2",
+            "TUBAL3",
+            "XKRY2",
+            "DAB2IP",
+            "GAPT",
+            "PRAMEF2",
+            "IQCF3",
+            "MSANTD3-TMEFF1",
+            "ARHGEF2",
+            "IPO13",
+            "ADARB1",
+            "COL4A4",
+            "FAM209A",
+            "TRIML2",
+            "NDUFB1",
+            "PPP3CB",
+            "RERGL",
+            "NonTarget.CTRL38",
+            "PGA3",
+            "CCNJL",
+            "OR5AN1",
+            "MMP16",
+            "FAM98B",
+            "CUL3",
+            "TREML4",
+            "CCDC28B",
+            "CLIC2",
+            "MAP3K3",
+            "NRG4",
+            "CSF2",
+            "MSH3",
+            "ATAT1",
+            "OXCT2",
+            "PRSS33",
+            "CLTRN",
+            "SYT1",
+            "SYCP2",
+            "GPR25",
+            "GPC2",
+            "DNAJC2",
+            "LOC729159",
+            "LAD1",
+            "BRMS1L",
+            "BCL11A",
+            "SH3TC1",
+            "ATP6AP1",
+            "OCA2",
+            "PLXDC1",
+            "STH",
+            "SMDT1",
+            "WNT8A",
+            "ESYT3",
+            "KCNJ3",
+            "TBRG1",
+            "SNAP29",
+            "PABPC3",
+            "BCL2L11",
+            "METTL6",
+            "FAM227B",
+            "ADCY9",
+            "INO80E",
+            "AK7",
+            "ZNF428",
+            "YIF1B",
+            "PMEL",
+            "TLCD3B",
+            "ANAPC4",
+            "TBC1D15",
+            "SDHA",
+            "SLC25A19",
+            "HERC3",
+            "ZSCAN20",
+            "LRRC7",
+            "YTHDF3",
+            "EP400",
+            "STC2",
+            "MUC13",
+            "FZD1",
+            "AP1S2",
+            "GUK1",
+            "ANKFY1",
+            "ZNF586",
+            "USH1G",
+            "HSPA12B",
+            "ZW10",
+            "KDR",
+            "CRACR2A",
+            "SUSD6",
+            "BCL7B",
+            "ODAD2",
+            "COPG1",
+            "BORCS5",
+            "ABCC12",
+            "ANKRD20A2",
+            "BCO2",
+            "BCOR",
+            "LMOD2",
+            "ZNF805",
+            "HOXC13",
+            "DNAH14",
+            "BEND3",
+            "UBA3",
+            "ATP2A3",
+            "LAMTOR1",
+            "ZNF654",
+            "FRMD6",
+            "ZNF669",
+            "CDK12",
+            "FMN2",
+            "DZIP1L",
+            "PRDM2",
+            "ZC3H13",
+            "SLC22A10",
+            "XPOT",
+            "ZMAT5",
+            "CEP43",
+            "DEFB112",
+            "ADNP",
+            "SLC6A6",
+            "CYP26C1",
+            "CAB39L",
+            "TMEM141",
+            "MYO1E",
+            "TUBB8",
+            "SPDL1",
+            "SYT9",
+            "ENSA",
+            "PPP4R2"
           ],
           "selected_scores": [
-            0.045874,
-            -0.24772,
-            0.22815,
-            0.078495,
-            -0.023711,
-            0.14989,
-            -0.22267,
-            0.044808,
-            0.052605,
-            0.30501,
-            0.0134015,
-            -0.122093,
-            -0.21191,
-            0.25029,
-            -0.28242,
-            -0.080544,
-            -0.020633,
-            0.15191,
-            0.16249,
-            0.2843,
-            -0.0041473,
-            -0.35613,
-            -0.10442,
-            -0.16902,
-            0.033329,
-            0.01813,
-            0.060526,
-            -0.24971,
-            -0.082904,
-            -0.14026,
-            -0.43957,
-            -0.22231,
-            0.073084,
-            -0.13503,
-            -0.045694,
-            -0.14264,
-            -0.01248,
-            0.031039,
-            -0.28603,
-            0.080001,
-            -0.035282,
-            -0.17211,
-            0.36936,
-            -0.16321,
-            0.004964,
-            0.080498,
-            0.049269,
-            -0.039443,
-            -0.072301,
-            0.017969,
-            0.14619,
-            0.037942,
-            0.14333,
-            -0.43089,
-            0.07773,
-            -0.027941,
-            0.088831,
-            0.023173,
-            -0.014842,
-            -0.18485,
-            0.17845,
-            0.27459,
-            0.0388275,
-            -0.035284,
-            0.078371,
-            0.047768,
-            0.19611,
-            0.15354,
-            -0.014472,
-            0.073076,
-            -0.00070511,
-            0.045831,
-            -0.22225,
-            -0.046169,
-            -0.046037,
-            -0.21237,
-            0.19453,
-            0.082329,
-            0.20888,
-            0.023426,
-            -0.18867,
-            0.023313,
-            0.09446,
-            -0.039011,
-            0.16566,
-            0.24338,
-            -0.13474,
-            0.29424,
-            -0.043506,
-            -0.068879,
-            0.10306,
-            0.016376,
-            -0.14937,
-            0.12185,
-            -0.27175,
-            -0.1986,
-            -0.15274,
-            0.11567,
-            -0.082349,
-            -0.56947,
-            -0.095898,
-            0.065055,
-            -0.021356,
-            0.063423,
-            -0.051998,
-            0.11306,
-            0.086018,
-            -0.1326,
-            -0.19461,
-            0.031861,
-            0.23864,
-            -0.0682,
-            -0.21138,
-            -0.15263,
-            -0.20681,
-            0.05235,
-            -0.19129,
-            -0.2877,
-            0.21682,
-            0.02847,
-            -0.026209,
-            -0.14898,
-            0.14103,
-            -0.023129,
-            0.12136,
-            0.032747,
-            0.23603,
-            0.039682
+            0.15184,
+            0.080271,
+            -0.2123,
+            0.044769,
+            -0.011911,
+            0.20294,
+            -0.044255,
+            -0.09824,
+            -0.034241,
+            -0.089332,
+            0.0072941,
+            0.079952,
+            -0.048248,
+            -0.011292,
+            -0.010165,
+            -0.011778,
+            0.14828,
+            -0.069151,
+            0.17943,
+            0.14958,
+            0.35942,
+            0.052122,
+            0.16907,
+            0.14949,
+            -0.4477,
+            0.37577,
+            0.18831,
+            0.066618,
+            0.041164,
+            -0.050149,
+            -0.20566,
+            0.31263,
+            0.33819,
+            -0.22276,
+            -0.13725,
+            -0.15675,
+            0.02306,
+            0.018811,
+            0.29964,
+            0.40151,
+            -0.24846,
+            0.33505,
+            -0.018266,
+            0.21109,
+            -0.3089,
+            0.30095,
+            -0.049326,
+            -0.2769,
+            -0.02723,
+            0.16957,
+            0.057329,
+            -0.30907,
+            -0.016158,
+            -0.21505,
+            -0.23827,
+            -0.21966,
+            0.33719,
+            -0.2162,
+            -0.18169,
+            0.15946,
+            -0.12583,
+            -0.053844,
+            0.043155,
+            -0.14187,
+            0.0077955,
+            -0.22864,
+            0.13634,
+            -0.044763,
+            0.19929,
+            0.008568,
+            -0.01863,
+            0.1752,
+            -0.064914,
+            -0.062509,
+            -0.071699,
+            -0.059057,
+            0.14463,
+            -0.1079,
+            -0.37582,
+            0.53392,
+            0.1186,
+            0.050891,
+            -0.035439,
+            -0.1018,
+            0.10344,
+            0.085495,
+            0.028925,
+            0.068816,
+            0.095651,
+            0.29212,
+            0.16188,
+            -0.090122,
+            0.068198,
+            0.19531,
+            0.27607,
+            -0.2411,
+            -0.0378,
+            0.052151,
+            -0.13105,
+            0.10655,
+            -0.1477,
+            0.075581,
+            -0.21116,
+            0.14123,
+            -0.065974,
+            0.074162,
+            0.001308,
+            -0.014396,
+            -0.17091,
+            -0.052318,
+            0.09734,
+            0.054432,
+            0.094775,
+            -0.084016,
+            0.11764,
+            0.063922,
+            -0.019297,
+            -0.085647,
+            0.065536,
+            0.27422,
+            0.33077,
+            0.22945,
+            -0.026485667,
+            -0.28545,
+            0.12938,
+            -0.10176,
+            -0.18372,
+            -0.061497
           ],
           "selected_hits": [
             0,
@@ -321,28 +321,11 @@
             0,
             0,
             0,
-            0,
             1,
             0,
             0,
             0,
-            0,
-            0,
-            0,
-            0,
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
             1,
             0,
             0,
@@ -350,10 +333,6 @@
             0,
             0,
             0,
-            0,
-            0,
-            0,
-            0,
             1,
             0,
             0,
@@ -361,46 +340,67 @@
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
             0,
             0,
             0,
@@ -1334,896 +1334,1792 @@
           "gene": "ATP6V1E1",
           "score": 0.045874,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9447,
           "gene": "MON1A",
           "score": -0.24772,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4751,
           "gene": "EIF5A",
           "score": 0.22815,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15266,
           "gene": "SP140L",
           "score": 0.078495,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12209,
           "gene": "PLEKHF2",
           "score": -0.023711,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3178,
           "gene": "CLPSL2",
           "score": 0.14989,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14957,
           "gene": "SLC6A8",
           "score": -0.22267,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16440,
           "gene": "TMC3",
           "score": 0.044808,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 630,
           "gene": "AMY1B",
           "score": 0.052605,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16960,
           "gene": "TRARG1",
           "score": 0.30501,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14271,
           "gene": "SELENOP",
           "score": 0.0134015,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12290,
           "gene": "PMEPA1",
           "score": -0.122093,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18045,
           "gene": "YIPF4",
           "score": -0.21191,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14326,
           "gene": "SERF1A",
           "score": 0.25029,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13004,
           "gene": "PTPRC",
           "score": -0.28242,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5816,
           "gene": "GABRA4",
           "score": -0.080544,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1903,
           "gene": "C2orf68",
           "score": -0.020633,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3542,
           "gene": "CRLS1",
           "score": 0.15191,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4112,
           "gene": "DENND4B",
           "score": 0.16249,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12406,
           "gene": "POM121L2",
           "score": 0.2843,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5064,
           "gene": "EXOC4",
           "score": -0.0041473,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3159,
           "gene": "CLK2",
           "score": -0.35613,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5303,
           "gene": "FAM9B",
           "score": -0.10442,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16906,
           "gene": "TPRA1",
           "score": -0.16902,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16365,
           "gene": "TIMP3",
           "score": 0.033329,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4248,
           "gene": "DLX1",
           "score": 0.01813,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12771,
           "gene": "PRR20A",
           "score": 0.060526,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16716,
           "gene": "TMPRSS11B",
           "score": -0.24971,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8979,
           "gene": "MAP3K5",
           "score": -0.082904,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6001,
           "gene": "GET3",
           "score": -0.14026,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12442,
           "gene": "POU2F1",
           "score": -0.43957,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2094,
           "gene": "CALHM1",
           "score": -0.22231,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1614,
           "gene": "BRCA2",
           "score": 0.073084,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2017,
           "gene": "C9orf78",
           "score": -0.13503,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6158,
           "gene": "GMPR",
           "score": -0.045694,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2024,
           "gene": "CA14",
           "score": -0.14264,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5472,
           "gene": "FFAR1",
           "score": -0.01248,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9780,
           "gene": "MXRA5",
           "score": 0.031039,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9090,
           "gene": "MC5R",
           "score": -0.28603,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2540,
           "gene": "CD5",
           "score": 0.080001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17228,
           "gene": "TTC4",
           "score": -0.035282,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3402,
           "gene": "COQ9",
           "score": -0.17211,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2012,
           "gene": "C9orf50",
           "score": 0.36936,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3105,
           "gene": "CLDN25",
           "score": -0.16321,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15097,
           "gene": "SMIM8",
           "score": 0.004964,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10934,
           "gene": "ODAPH",
           "score": 0.080498,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10898,
           "gene": "NonTarget.CTRL95",
           "score": 0.049269,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17446,
           "gene": "UCK2",
           "score": -0.039443,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14482,
           "gene": "SH3GL1",
           "score": -0.072301,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5508,
           "gene": "FGFR1OP2",
           "score": 0.017969,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4170,
           "gene": "DHRS2",
           "score": 0.14619,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2644,
           "gene": "CDK11B",
           "score": 0.037942,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10548,
           "gene": "NTRK2",
           "score": 0.14333,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1652,
           "gene": "BTBD1",
           "score": -0.43089,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8854,
           "gene": "MAB21L1",
           "score": 0.07773,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12149,
           "gene": "PLA2G6",
           "score": -0.027941,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6138,
           "gene": "GLUL",
           "score": 0.088831,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2320,
           "gene": "CCDC187",
           "score": 0.023173,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18209,
           "gene": "ZFP1",
           "score": -0.014842,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3741,
           "gene": "CUTC",
           "score": -0.18485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9808,
           "gene": "MYH1",
           "score": 0.17845,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16329,
           "gene": "TIAM2",
           "score": 0.27459,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11934,
           "gene": "PGPEP1",
           "score": 0.0388275,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14324,
           "gene": "SERAC1",
           "score": -0.035284,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1362,
           "gene": "B4GALT6",
           "score": 0.078371,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15612,
           "gene": "STAMBPL1",
           "score": 0.047768,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13694,
           "gene": "RNF167",
           "score": 0.19611,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2758,
           "gene": "CENPN",
           "score": 0.15354,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11819,
           "gene": "PDRG1",
           "score": -0.014472,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4197,
           "gene": "DIABLO",
           "score": 0.073076,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2843,
           "gene": "CFAP299",
           "score": -0.00070511,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5085,
           "gene": "EXTL2",
           "score": 0.045831,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10152,
           "gene": "NEURL2",
           "score": -0.22225,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3595,
           "gene": "CSGALNACT2",
           "score": -0.046169,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17655,
           "gene": "UTP3",
           "score": -0.046037,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14020,
           "gene": "S100A13",
           "score": -0.21237,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14622,
           "gene": "SLC10A7",
           "score": 0.19453,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1252,
           "gene": "ATP5PO",
           "score": 0.082329,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4837,
           "gene": "ENDOD1",
           "score": 0.20888,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 82,
           "gene": "ABHD14B",
           "score": 0.023426,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3491,
           "gene": "CR1L",
           "score": -0.18867,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4104,
           "gene": "DENND1B",
           "score": 0.023313,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4160,
           "gene": "DHDH",
           "score": 0.09446,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18432,
           "gene": "ZNF350",
           "score": -0.039011,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14849,
           "gene": "SLC35G5",
           "score": 0.16566,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16901,
           "gene": "TPP2",
           "score": 0.24338,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 647,
           "gene": "ANGEL1",
           "score": -0.13474,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15371,
           "gene": "SPEM1",
           "score": 0.29424,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18188,
           "gene": "ZDHHC4",
           "score": -0.043506,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15634,
           "gene": "STBD1",
           "score": -0.068879,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4243,
           "gene": "DLK2",
           "score": 0.10306,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18196,
           "gene": "ZER1",
           "score": 0.016376,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5781,
           "gene": "FYCO1",
           "score": -0.14937,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17944,
           "gene": "WNT2",
           "score": 0.12185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 283,
           "gene": "ADAMTS9",
           "score": -0.27175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17820,
           "gene": "VWF",
           "score": -0.1986,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9251,
           "gene": "MFAP1",
           "score": -0.15274,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17316,
           "gene": "TXNDC17",
           "score": 0.11567,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15148,
           "gene": "SNF8",
           "score": -0.082349,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10287,
           "gene": "NLRP1",
           "score": -0.56947,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2613,
           "gene": "CDH10",
           "score": -0.095898,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13501,
           "gene": "RGL1",
           "score": 0.065055,
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
           "candidate_index": 15295,
           "gene": "SPAM1",
           "score": 0.063423,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18497,
           "gene": "ZNF469",
           "score": -0.051998,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17602,
           "gene": "USP18",
           "score": 0.11306,
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
           "candidate_index": 4424,
           "gene": "DPP3",
           "score": -0.1326,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5321,
           "gene": "FARP1",
           "score": -0.19461,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17105,
           "gene": "TRPM4",
           "score": 0.031861,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12626,
           "gene": "PRCP",
           "score": 0.23864,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2131,
           "gene": "CAND1",
           "score": -0.0682,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7259,
           "gene": "IGFBP2",
           "score": -0.21138,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3164,
           "gene": "CLMN",
           "score": -0.15263,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12893,
           "gene": "PSMC4",
           "score": -0.20681,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15198,
           "gene": "SNX27",
           "score": 0.05235,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2399,
           "gene": "CCL17",
           "score": -0.19129,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2655,
           "gene": "CDK2AP1",
           "score": -0.2877,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1001,
           "gene": "ARL16",
           "score": 0.21682,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2538,
           "gene": "CD47",
           "score": 0.02847,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2027,
           "gene": "CA4",
           "score": -0.026209,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2156,
           "gene": "CAPZA2",
           "score": -0.14898,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11758,
           "gene": "PDCD7",
           "score": 0.14103,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5361,
           "gene": "FBXL18",
           "score": -0.023129,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4595,
           "gene": "ECHDC3",
           "score": 0.12136,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17270,
           "gene": "TUBB2B",
           "score": 0.032747,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14586,
           "gene": "SIVA1",
           "score": 0.23603,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17919,
           "gene": "WFDC8",
           "score": 0.039682,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 13569,
+          "gene": "RHOT2",
+          "score": 0.15184,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17267,
+          "gene": "TUBAL3",
+          "score": 0.080271,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18001,
+          "gene": "XKRY2",
+          "score": -0.2123,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3888,
+          "gene": "DAB2IP",
+          "score": 0.044769,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5887,
+          "gene": "GAPT",
+          "score": -0.011911,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12611,
+          "gene": "PRAMEF2",
+          "score": 0.20294,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7493,
+          "gene": "IQCF3",
+          "score": -0.044255,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9628,
+          "gene": "MSANTD3-TMEFF1",
+          "score": -0.09824,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 962,
+          "gene": "ARHGEF2",
+          "score": -0.034241,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7477,
+          "gene": "IPO13",
+          "score": -0.089332,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 292,
+          "gene": "ADARB1",
+          "score": 0.0072941,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3337,
+          "gene": "COL4A4",
+          "score": 0.079952,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5221,
+          "gene": "FAM209A",
+          "score": -0.048248,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17058,
+          "gene": "TRIML2",
+          "score": -0.011292,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10071,
+          "gene": "NDUFB1",
+          "score": -0.010165,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12573,
+          "gene": "PPP3CB",
+          "score": -0.011778,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13454,
+          "gene": "RERGL",
+          "score": 0.14828,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10835,
+          "gene": "NonTarget.CTRL38",
+          "score": -0.069151,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11901,
+          "gene": "PGA3",
+          "score": 0.17943,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2446,
+          "gene": "CCNJL",
+          "score": 0.14958,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11256,
+          "gene": "OR5AN1",
+          "score": 0.35942,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 9401,
+          "gene": "MMP16",
+          "score": 0.052122,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5300,
+          "gene": "FAM98B",
+          "score": 0.16907,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3734,
+          "gene": "CUL3",
+          "score": 0.14949,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16969,
+          "gene": "TREML4",
+          "score": -0.4477,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 2329,
+          "gene": "CCDC28B",
+          "score": 0.37577,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 3150,
+          "gene": "CLIC2",
+          "score": 0.18831,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8977,
+          "gene": "MAP3K3",
+          "score": 0.066618,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10482,
+          "gene": "NRG4",
+          "score": 0.041164,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3589,
+          "gene": "CSF2",
+          "score": -0.050149,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9633,
+          "gene": "MSH3",
+          "score": -0.20566,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1159,
+          "gene": "ATAT1",
+          "score": 0.31263,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11445,
+          "gene": "OXCT2",
+          "score": 0.33819,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 12821,
+          "gene": "PRSS33",
+          "score": -0.22276,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3193,
+          "gene": "CLTRN",
+          "score": -0.13725,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15853,
+          "gene": "SYT1",
+          "score": -0.15675,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15815,
+          "gene": "SYCP2",
+          "score": 0.02306,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6347,
+          "gene": "GPR25",
+          "score": 0.018811,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6281,
+          "gene": "GPC2",
+          "score": 0.29964,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4335,
+          "gene": "DNAJC2",
+          "score": 0.40151,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 8587,
+          "gene": "LOC729159",
+          "score": -0.24846,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8246,
+          "gene": "LAD1",
+          "score": 0.33505,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1632,
+          "gene": "BRMS1L",
+          "score": -0.018266,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1440,
+          "gene": "BCL11A",
+          "score": 0.21109,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14493,
+          "gene": "SH3TC1",
+          "score": -0.3089,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1253,
+          "gene": "ATP6AP1",
+          "score": 0.30095,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10919,
+          "gene": "OCA2",
+          "score": -0.049326,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12274,
+          "gene": "PLXDC1",
+          "score": -0.2769,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15643,
+          "gene": "STH",
+          "score": -0.02723,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15068,
+          "gene": "SMDT1",
+          "score": 0.16957,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17954,
+          "gene": "WNT8A",
+          "score": 0.057329,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5016,
+          "gene": "ESYT3",
+          "score": -0.30907,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7761,
+          "gene": "KCNJ3",
+          "score": -0.016158,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16055,
+          "gene": "TBRG1",
+          "score": -0.21505,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15133,
+          "gene": "SNAP29",
+          "score": -0.23827,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11489,
+          "gene": "PABPC3",
+          "score": -0.21966,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1446,
+          "gene": "BCL2L11",
+          "score": 0.33719,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 9244,
+          "gene": "METTL6",
+          "score": -0.2162,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5241,
+          "gene": "FAM227B",
+          "score": -0.18169,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 308,
+          "gene": "ADCY9",
+          "score": 0.15946,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7426,
+          "gene": "INO80E",
+          "score": -0.12583,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 483,
+          "gene": "AK7",
+          "score": -0.053844,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18470,
+          "gene": "ZNF428",
+          "score": 0.043155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18041,
+          "gene": "YIF1B",
+          "score": -0.14187,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12289,
+          "gene": "PMEL",
+          "score": 0.0077955,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16386,
+          "gene": "TLCD3B",
+          "score": -0.22864,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 643,
+          "gene": "ANAPC4",
+          "score": 0.13634,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16004,
+          "gene": "TBC1D15",
+          "score": -0.044763,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14212,
+          "gene": "SDHA",
+          "score": 0.19929,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14726,
+          "gene": "SLC25A19",
+          "score": 0.008568,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6788,
+          "gene": "HERC3",
+          "score": -0.01863,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18826,
+          "gene": "ZSCAN20",
+          "score": 0.1752,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8714,
+          "gene": "LRRC7",
+          "score": -0.064914,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18066,
+          "gene": "YTHDF3",
+          "score": -0.062509,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4882,
+          "gene": "EP400",
+          "score": -0.071699,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15636,
+          "gene": "STC2",
+          "score": -0.059057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9749,
+          "gene": "MUC13",
+          "score": 0.14463,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5784,
+          "gene": "FZD1",
+          "score": -0.1079,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 792,
+          "gene": "AP1S2",
+          "score": -0.37582,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 6556,
+          "gene": "GUK1",
+          "score": 0.53392,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 669,
+          "gene": "ANKFY1",
+          "score": 0.1186,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18588,
+          "gene": "ZNF586",
+          "score": 0.050891,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17567,
+          "gene": "USH1G",
+          "score": -0.035439,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7070,
+          "gene": "HSPA12B",
+          "score": -0.1018,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18850,
+          "gene": "ZW10",
+          "score": 0.10344,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7847,
+          "gene": "KDR",
+          "score": 0.085495,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3497,
+          "gene": "CRACR2A",
+          "score": 0.028925,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15790,
+          "gene": "SUSD6",
+          "score": 0.068816,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1457,
+          "gene": "BCL7B",
+          "score": 0.095651,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10930,
+          "gene": "ODAD2",
+          "score": 0.29212,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3379,
+          "gene": "COPG1",
+          "score": 0.16188,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1589,
+          "gene": "BORCS5",
+          "score": -0.090122,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 54,
+          "gene": "ABCC12",
+          "score": 0.068198,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 694,
+          "gene": "ANKRD20A2",
+          "score": 0.19531,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1464,
+          "gene": "BCO2",
+          "score": 0.27607,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1465,
+          "gene": "BCOR",
+          "score": -0.2411,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8507,
+          "gene": "LMOD2",
+          "score": -0.0378,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18748,
+          "gene": "ZNF805",
+          "score": 0.052151,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6980,
+          "gene": "HOXC13",
+          "score": -0.13105,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4293,
+          "gene": "DNAH14",
+          "score": 0.10655,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1478,
+          "gene": "BEND3",
+          "score": -0.1477,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17348,
+          "gene": "UBA3",
+          "score": 0.075581,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1225,
+          "gene": "ATP2A3",
+          "score": -0.21116,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8266,
+          "gene": "LAMTOR1",
+          "score": 0.14123,
+          "hit": 0,
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
+          "candidate_index": 5707,
+          "gene": "FRMD6",
+          "score": 0.074162,
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
+          "candidate_index": 2645,
+          "gene": "CDK12",
+          "score": -0.014396,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5590,
+          "gene": "FMN2",
+          "score": -0.17091,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4565,
+          "gene": "DZIP1L",
+          "score": -0.052318,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12635,
+          "gene": "PRDM2",
+          "score": 0.09734,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18140,
+          "gene": "ZC3H13",
+          "score": 0.054432,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14685,
+          "gene": "SLC22A10",
+          "score": 0.094775,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18012,
+          "gene": "XPOT",
+          "score": -0.084016,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18274,
+          "gene": "ZMAT5",
+          "score": 0.11764,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2790,
+          "gene": "CEP43",
+          "score": 0.063922,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4073,
+          "gene": "DEFB112",
+          "score": -0.019297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 362,
+          "gene": "ADNP",
+          "score": -0.085647,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14955,
+          "gene": "SLC6A6",
+          "score": 0.065536,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3824,
+          "gene": "CYP26C1",
+          "score": 0.27422,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2036,
+          "gene": "CAB39L",
+          "score": 0.33077,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16509,
+          "gene": "TMEM141",
+          "score": 0.22945,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9850,
+          "gene": "MYO1E",
+          "score": -0.026485667,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17275,
+          "gene": "TUBB8",
+          "score": -0.28545,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15356,
+          "gene": "SPDL1",
+          "score": 0.12938,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15869,
+          "gene": "SYT9",
+          "score": -0.10176,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4862,
+          "gene": "ENSA",
+          "score": -0.18372,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12579,
+          "gene": "PPP4R2",
+          "score": -0.061497,
+          "hit": 0,
+          "round": 2
         }
       ],
       "queried_history": [
@@ -3128,896 +4024,1792 @@
           "gene": "ATP6V1E1",
           "score": 0.045874,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9447,
           "gene": "MON1A",
           "score": -0.24772,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4751,
           "gene": "EIF5A",
           "score": 0.22815,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15266,
           "gene": "SP140L",
           "score": 0.078495,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12209,
           "gene": "PLEKHF2",
           "score": -0.023711,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3178,
           "gene": "CLPSL2",
           "score": 0.14989,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14957,
           "gene": "SLC6A8",
           "score": -0.22267,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16440,
           "gene": "TMC3",
           "score": 0.044808,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 630,
           "gene": "AMY1B",
           "score": 0.052605,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16960,
           "gene": "TRARG1",
           "score": 0.30501,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14271,
           "gene": "SELENOP",
           "score": 0.0134015,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12290,
           "gene": "PMEPA1",
           "score": -0.122093,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18045,
           "gene": "YIPF4",
           "score": -0.21191,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14326,
           "gene": "SERF1A",
           "score": 0.25029,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13004,
           "gene": "PTPRC",
           "score": -0.28242,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5816,
           "gene": "GABRA4",
           "score": -0.080544,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1903,
           "gene": "C2orf68",
           "score": -0.020633,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3542,
           "gene": "CRLS1",
           "score": 0.15191,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4112,
           "gene": "DENND4B",
           "score": 0.16249,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12406,
           "gene": "POM121L2",
           "score": 0.2843,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5064,
           "gene": "EXOC4",
           "score": -0.0041473,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3159,
           "gene": "CLK2",
           "score": -0.35613,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5303,
           "gene": "FAM9B",
           "score": -0.10442,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16906,
           "gene": "TPRA1",
           "score": -0.16902,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16365,
           "gene": "TIMP3",
           "score": 0.033329,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4248,
           "gene": "DLX1",
           "score": 0.01813,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12771,
           "gene": "PRR20A",
           "score": 0.060526,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16716,
           "gene": "TMPRSS11B",
           "score": -0.24971,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8979,
           "gene": "MAP3K5",
           "score": -0.082904,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6001,
           "gene": "GET3",
           "score": -0.14026,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12442,
           "gene": "POU2F1",
           "score": -0.43957,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2094,
           "gene": "CALHM1",
           "score": -0.22231,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1614,
           "gene": "BRCA2",
           "score": 0.073084,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2017,
           "gene": "C9orf78",
           "score": -0.13503,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6158,
           "gene": "GMPR",
           "score": -0.045694,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2024,
           "gene": "CA14",
           "score": -0.14264,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5472,
           "gene": "FFAR1",
           "score": -0.01248,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9780,
           "gene": "MXRA5",
           "score": 0.031039,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9090,
           "gene": "MC5R",
           "score": -0.28603,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2540,
           "gene": "CD5",
           "score": 0.080001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17228,
           "gene": "TTC4",
           "score": -0.035282,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3402,
           "gene": "COQ9",
           "score": -0.17211,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2012,
           "gene": "C9orf50",
           "score": 0.36936,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3105,
           "gene": "CLDN25",
           "score": -0.16321,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15097,
           "gene": "SMIM8",
           "score": 0.004964,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10934,
           "gene": "ODAPH",
           "score": 0.080498,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10898,
           "gene": "NonTarget.CTRL95",
           "score": 0.049269,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17446,
           "gene": "UCK2",
           "score": -0.039443,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14482,
           "gene": "SH3GL1",
           "score": -0.072301,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5508,
           "gene": "FGFR1OP2",
           "score": 0.017969,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4170,
           "gene": "DHRS2",
           "score": 0.14619,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2644,
           "gene": "CDK11B",
           "score": 0.037942,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10548,
           "gene": "NTRK2",
           "score": 0.14333,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1652,
           "gene": "BTBD1",
           "score": -0.43089,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8854,
           "gene": "MAB21L1",
           "score": 0.07773,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12149,
           "gene": "PLA2G6",
           "score": -0.027941,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6138,
           "gene": "GLUL",
           "score": 0.088831,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2320,
           "gene": "CCDC187",
           "score": 0.023173,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18209,
           "gene": "ZFP1",
           "score": -0.014842,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3741,
           "gene": "CUTC",
           "score": -0.18485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9808,
           "gene": "MYH1",
           "score": 0.17845,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16329,
           "gene": "TIAM2",
           "score": 0.27459,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11934,
           "gene": "PGPEP1",
           "score": 0.0388275,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14324,
           "gene": "SERAC1",
           "score": -0.035284,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1362,
           "gene": "B4GALT6",
           "score": 0.078371,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15612,
           "gene": "STAMBPL1",
           "score": 0.047768,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13694,
           "gene": "RNF167",
           "score": 0.19611,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2758,
           "gene": "CENPN",
           "score": 0.15354,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11819,
           "gene": "PDRG1",
           "score": -0.014472,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4197,
           "gene": "DIABLO",
           "score": 0.073076,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2843,
           "gene": "CFAP299",
           "score": -0.00070511,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5085,
           "gene": "EXTL2",
           "score": 0.045831,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10152,
           "gene": "NEURL2",
           "score": -0.22225,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3595,
           "gene": "CSGALNACT2",
           "score": -0.046169,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17655,
           "gene": "UTP3",
           "score": -0.046037,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14020,
           "gene": "S100A13",
           "score": -0.21237,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14622,
           "gene": "SLC10A7",
           "score": 0.19453,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1252,
           "gene": "ATP5PO",
           "score": 0.082329,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4837,
           "gene": "ENDOD1",
           "score": 0.20888,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 82,
           "gene": "ABHD14B",
           "score": 0.023426,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3491,
           "gene": "CR1L",
           "score": -0.18867,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4104,
           "gene": "DENND1B",
           "score": 0.023313,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4160,
           "gene": "DHDH",
           "score": 0.09446,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18432,
           "gene": "ZNF350",
           "score": -0.039011,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14849,
           "gene": "SLC35G5",
           "score": 0.16566,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16901,
           "gene": "TPP2",
           "score": 0.24338,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 647,
           "gene": "ANGEL1",
           "score": -0.13474,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15371,
           "gene": "SPEM1",
           "score": 0.29424,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18188,
           "gene": "ZDHHC4",
           "score": -0.043506,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15634,
           "gene": "STBD1",
           "score": -0.068879,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4243,
           "gene": "DLK2",
           "score": 0.10306,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18196,
           "gene": "ZER1",
           "score": 0.016376,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5781,
           "gene": "FYCO1",
           "score": -0.14937,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17944,
           "gene": "WNT2",
           "score": 0.12185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 283,
           "gene": "ADAMTS9",
           "score": -0.27175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17820,
           "gene": "VWF",
           "score": -0.1986,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9251,
           "gene": "MFAP1",
           "score": -0.15274,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17316,
           "gene": "TXNDC17",
           "score": 0.11567,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15148,
           "gene": "SNF8",
           "score": -0.082349,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10287,
           "gene": "NLRP1",
           "score": -0.56947,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2613,
           "gene": "CDH10",
           "score": -0.095898,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13501,
           "gene": "RGL1",
           "score": 0.065055,
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
           "candidate_index": 15295,
           "gene": "SPAM1",
           "score": 0.063423,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18497,
           "gene": "ZNF469",
           "score": -0.051998,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17602,
           "gene": "USP18",
           "score": 0.11306,
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
           "candidate_index": 4424,
           "gene": "DPP3",
           "score": -0.1326,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5321,
           "gene": "FARP1",
           "score": -0.19461,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17105,
           "gene": "TRPM4",
           "score": 0.031861,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12626,
           "gene": "PRCP",
           "score": 0.23864,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2131,
           "gene": "CAND1",
           "score": -0.0682,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7259,
           "gene": "IGFBP2",
           "score": -0.21138,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3164,
           "gene": "CLMN",
           "score": -0.15263,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12893,
           "gene": "PSMC4",
           "score": -0.20681,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15198,
           "gene": "SNX27",
           "score": 0.05235,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2399,
           "gene": "CCL17",
           "score": -0.19129,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2655,
           "gene": "CDK2AP1",
           "score": -0.2877,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1001,
           "gene": "ARL16",
           "score": 0.21682,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2538,
           "gene": "CD47",
           "score": 0.02847,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2027,
           "gene": "CA4",
           "score": -0.026209,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2156,
           "gene": "CAPZA2",
           "score": -0.14898,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11758,
           "gene": "PDCD7",
           "score": 0.14103,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5361,
           "gene": "FBXL18",
           "score": -0.023129,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4595,
           "gene": "ECHDC3",
           "score": 0.12136,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17270,
           "gene": "TUBB2B",
           "score": 0.032747,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14586,
           "gene": "SIVA1",
           "score": 0.23603,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17919,
           "gene": "WFDC8",
           "score": 0.039682,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 13569,
+          "gene": "RHOT2",
+          "score": 0.15184,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17267,
+          "gene": "TUBAL3",
+          "score": 0.080271,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18001,
+          "gene": "XKRY2",
+          "score": -0.2123,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3888,
+          "gene": "DAB2IP",
+          "score": 0.044769,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5887,
+          "gene": "GAPT",
+          "score": -0.011911,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12611,
+          "gene": "PRAMEF2",
+          "score": 0.20294,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7493,
+          "gene": "IQCF3",
+          "score": -0.044255,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9628,
+          "gene": "MSANTD3-TMEFF1",
+          "score": -0.09824,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 962,
+          "gene": "ARHGEF2",
+          "score": -0.034241,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7477,
+          "gene": "IPO13",
+          "score": -0.089332,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 292,
+          "gene": "ADARB1",
+          "score": 0.0072941,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3337,
+          "gene": "COL4A4",
+          "score": 0.079952,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5221,
+          "gene": "FAM209A",
+          "score": -0.048248,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17058,
+          "gene": "TRIML2",
+          "score": -0.011292,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10071,
+          "gene": "NDUFB1",
+          "score": -0.010165,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12573,
+          "gene": "PPP3CB",
+          "score": -0.011778,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13454,
+          "gene": "RERGL",
+          "score": 0.14828,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10835,
+          "gene": "NonTarget.CTRL38",
+          "score": -0.069151,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11901,
+          "gene": "PGA3",
+          "score": 0.17943,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2446,
+          "gene": "CCNJL",
+          "score": 0.14958,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11256,
+          "gene": "OR5AN1",
+          "score": 0.35942,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 9401,
+          "gene": "MMP16",
+          "score": 0.052122,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5300,
+          "gene": "FAM98B",
+          "score": 0.16907,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3734,
+          "gene": "CUL3",
+          "score": 0.14949,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16969,
+          "gene": "TREML4",
+          "score": -0.4477,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 2329,
+          "gene": "CCDC28B",
+          "score": 0.37577,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 3150,
+          "gene": "CLIC2",
+          "score": 0.18831,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8977,
+          "gene": "MAP3K3",
+          "score": 0.066618,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10482,
+          "gene": "NRG4",
+          "score": 0.041164,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3589,
+          "gene": "CSF2",
+          "score": -0.050149,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9633,
+          "gene": "MSH3",
+          "score": -0.20566,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1159,
+          "gene": "ATAT1",
+          "score": 0.31263,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11445,
+          "gene": "OXCT2",
+          "score": 0.33819,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 12821,
+          "gene": "PRSS33",
+          "score": -0.22276,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3193,
+          "gene": "CLTRN",
+          "score": -0.13725,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15853,
+          "gene": "SYT1",
+          "score": -0.15675,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15815,
+          "gene": "SYCP2",
+          "score": 0.02306,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6347,
+          "gene": "GPR25",
+          "score": 0.018811,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6281,
+          "gene": "GPC2",
+          "score": 0.29964,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4335,
+          "gene": "DNAJC2",
+          "score": 0.40151,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 8587,
+          "gene": "LOC729159",
+          "score": -0.24846,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8246,
+          "gene": "LAD1",
+          "score": 0.33505,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1632,
+          "gene": "BRMS1L",
+          "score": -0.018266,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1440,
+          "gene": "BCL11A",
+          "score": 0.21109,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14493,
+          "gene": "SH3TC1",
+          "score": -0.3089,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1253,
+          "gene": "ATP6AP1",
+          "score": 0.30095,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10919,
+          "gene": "OCA2",
+          "score": -0.049326,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12274,
+          "gene": "PLXDC1",
+          "score": -0.2769,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15643,
+          "gene": "STH",
+          "score": -0.02723,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15068,
+          "gene": "SMDT1",
+          "score": 0.16957,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17954,
+          "gene": "WNT8A",
+          "score": 0.057329,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5016,
+          "gene": "ESYT3",
+          "score": -0.30907,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7761,
+          "gene": "KCNJ3",
+          "score": -0.016158,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16055,
+          "gene": "TBRG1",
+          "score": -0.21505,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15133,
+          "gene": "SNAP29",
+          "score": -0.23827,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11489,
+          "gene": "PABPC3",
+          "score": -0.21966,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1446,
+          "gene": "BCL2L11",
+          "score": 0.33719,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 9244,
+          "gene": "METTL6",
+          "score": -0.2162,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5241,
+          "gene": "FAM227B",
+          "score": -0.18169,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 308,
+          "gene": "ADCY9",
+          "score": 0.15946,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7426,
+          "gene": "INO80E",
+          "score": -0.12583,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 483,
+          "gene": "AK7",
+          "score": -0.053844,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18470,
+          "gene": "ZNF428",
+          "score": 0.043155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18041,
+          "gene": "YIF1B",
+          "score": -0.14187,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12289,
+          "gene": "PMEL",
+          "score": 0.0077955,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16386,
+          "gene": "TLCD3B",
+          "score": -0.22864,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 643,
+          "gene": "ANAPC4",
+          "score": 0.13634,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16004,
+          "gene": "TBC1D15",
+          "score": -0.044763,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14212,
+          "gene": "SDHA",
+          "score": 0.19929,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14726,
+          "gene": "SLC25A19",
+          "score": 0.008568,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6788,
+          "gene": "HERC3",
+          "score": -0.01863,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18826,
+          "gene": "ZSCAN20",
+          "score": 0.1752,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8714,
+          "gene": "LRRC7",
+          "score": -0.064914,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18066,
+          "gene": "YTHDF3",
+          "score": -0.062509,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4882,
+          "gene": "EP400",
+          "score": -0.071699,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15636,
+          "gene": "STC2",
+          "score": -0.059057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9749,
+          "gene": "MUC13",
+          "score": 0.14463,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5784,
+          "gene": "FZD1",
+          "score": -0.1079,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 792,
+          "gene": "AP1S2",
+          "score": -0.37582,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 6556,
+          "gene": "GUK1",
+          "score": 0.53392,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 669,
+          "gene": "ANKFY1",
+          "score": 0.1186,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18588,
+          "gene": "ZNF586",
+          "score": 0.050891,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17567,
+          "gene": "USH1G",
+          "score": -0.035439,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7070,
+          "gene": "HSPA12B",
+          "score": -0.1018,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18850,
+          "gene": "ZW10",
+          "score": 0.10344,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7847,
+          "gene": "KDR",
+          "score": 0.085495,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3497,
+          "gene": "CRACR2A",
+          "score": 0.028925,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15790,
+          "gene": "SUSD6",
+          "score": 0.068816,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1457,
+          "gene": "BCL7B",
+          "score": 0.095651,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10930,
+          "gene": "ODAD2",
+          "score": 0.29212,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3379,
+          "gene": "COPG1",
+          "score": 0.16188,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1589,
+          "gene": "BORCS5",
+          "score": -0.090122,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 54,
+          "gene": "ABCC12",
+          "score": 0.068198,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 694,
+          "gene": "ANKRD20A2",
+          "score": 0.19531,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1464,
+          "gene": "BCO2",
+          "score": 0.27607,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1465,
+          "gene": "BCOR",
+          "score": -0.2411,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8507,
+          "gene": "LMOD2",
+          "score": -0.0378,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18748,
+          "gene": "ZNF805",
+          "score": 0.052151,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6980,
+          "gene": "HOXC13",
+          "score": -0.13105,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4293,
+          "gene": "DNAH14",
+          "score": 0.10655,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1478,
+          "gene": "BEND3",
+          "score": -0.1477,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17348,
+          "gene": "UBA3",
+          "score": 0.075581,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1225,
+          "gene": "ATP2A3",
+          "score": -0.21116,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8266,
+          "gene": "LAMTOR1",
+          "score": 0.14123,
+          "hit": 0,
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
+          "candidate_index": 5707,
+          "gene": "FRMD6",
+          "score": 0.074162,
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
+          "candidate_index": 2645,
+          "gene": "CDK12",
+          "score": -0.014396,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5590,
+          "gene": "FMN2",
+          "score": -0.17091,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4565,
+          "gene": "DZIP1L",
+          "score": -0.052318,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12635,
+          "gene": "PRDM2",
+          "score": 0.09734,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18140,
+          "gene": "ZC3H13",
+          "score": 0.054432,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14685,
+          "gene": "SLC22A10",
+          "score": 0.094775,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18012,
+          "gene": "XPOT",
+          "score": -0.084016,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18274,
+          "gene": "ZMAT5",
+          "score": 0.11764,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2790,
+          "gene": "CEP43",
+          "score": 0.063922,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4073,
+          "gene": "DEFB112",
+          "score": -0.019297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 362,
+          "gene": "ADNP",
+          "score": -0.085647,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14955,
+          "gene": "SLC6A6",
+          "score": 0.065536,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3824,
+          "gene": "CYP26C1",
+          "score": 0.27422,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2036,
+          "gene": "CAB39L",
+          "score": 0.33077,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16509,
+          "gene": "TMEM141",
+          "score": 0.22945,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9850,
+          "gene": "MYO1E",
+          "score": -0.026485667,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17275,
+          "gene": "TUBB8",
+          "score": -0.28545,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15356,
+          "gene": "SPDL1",
+          "score": 0.12938,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15869,
+          "gene": "SYT9",
+          "score": -0.10176,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4862,
+          "gene": "ENSA",
+          "score": -0.18372,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12579,
+          "gene": "PPP4R2",
+          "score": -0.061497,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
