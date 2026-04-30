# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21_down/run-1/best/current/harness
Generated at: 2026-04-30T07:00:18.859669

## Files Changed

- model.py: modified (added=6, deleted=4, delta=2)
- outputs/metrics.json: modified (added=2367, deleted=575, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -211,12 +211,14 @@
         cluster_id = candidate_to_cluster[idx]
         cluster_post = cluster_posterior[cluster_id]
         
-        # Update from cluster prior with single observation
-        lambda_n = cluster_post['lambda_n'] + 1
-        mu_n = (cluster_post['lambda_n'] * cluster_post['mu_n'] + score) / lambda_n
+        # Conservative update: treat cluster prior as having stronger weight
+        # This prevents overfitting to a single observation when cluster has limited data
+        effective_prior_weight = max(cluster_post['lambda_n'], 2.0)  # At least 2 pseudo-observations
+        lambda_n = effective_prior_weight + 1
+        mu_n = (effective_prior_weight * cluster_post['mu_n'] + score) / lambda_n
         alpha_n = cluster_post['alpha_n'] + 0.5
         beta_n = cluster_post['beta_n'] + 0.5 * (score - cluster_post['mu_n']) ** 2 * \
-                 cluster_post['lambda_n'] / lambda_n
+                 effective_prior_weight / lambda_n
         
         candidate_posterior[idx] = {
             'mu_n': mu_n,

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18469,
-      "rounds": 2,
+      "rounds": 3,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 128,
-      "baseline_total_hits": 5,
+      "baseline_total_queries": 256,
+      "baseline_total_hits": 10,
       "delta_queries": 128,
-      "delta_hits": 5,
-      "total_queries": 256,
-      "total_hits": 10,
+      "delta_hits": 6,
+      "total_queries": 384,
+      "total_hits": 16,
       "top_k": 924,
       "hit_curve": {
         "queries": [
-          128,
-          256
+          256,
+          384
         ],
         "hits": [
-          5,
-          10
+          10,
+          16
         ]
       },
-      "auc": 960.0,
-      "auc_normalized": 0.004058441558441558,
-      "ncg": 0.2031925200173379,
+      "auc": 1664.0,
+      "auc_normalized": 0.00468975468975469,
+      "ncg": 0.22354381263581585,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 5,
-          "cumulative_hits": 10,
-          "precision_at_batch": 0.0390625,
+          "hits": 6,
+          "cumulative_hits": 16,
+          "precision_at_batch": 0.046875,
           "selected": [
-            "DDI2",
-            "LONRF2",
-            "ZNF559-ZNF177",
-            "TSSC4",
-            "LDLRAD4",
-            "CDK15",
-            "DPPA2",
-            "CDC5L",
-            "KDM3B",
-            "P2RX4",
-            "HTR3C",
-            "BRE",
-            "BRWD1",
-            "TNFSF8",
-            "ARL6IP4",
-            "AAGAB",
-            "TCL1A",
-            "ZKSCAN7",
-            "AMOTL2",
-            "GRID2IP",
-            "ERP27",
-            "ZNF83",
-            "IL36RN",
-            "CHD6",
-            "CCDC122",
-            "MTA2",
-            "FOXE1",
-            "RND2",
-            "TRIM58",
-            "ETFDH",
-            "ENOPH1",
-            "PKM",
-            "CAPZA2",
-            "ACTR1B",
-            "CLASP2",
-            "GTF2A1",
-            "IL31",
-            "NAPB",
-            "SPINT1",
-            "BBS10",
-            "VDR",
-            "TCEB3CL2",
-            "B4GALNT3",
-            "TAC4",
-            "CLPX",
-            "TEX40",
-            "IMPA2",
-            "LRRTM1",
-            "UBL7",
-            "TP73",
-            "RTN1",
-            "SPATS2",
-            "ZWILCH",
-            "RS1",
-            "SLC30A6",
-            "TAS2R20",
-            "C4orf29",
-            "GMFB",
-            "SDHC",
-            "RABAC1",
-            "FSTL1",
-            "CRCP",
-            "AIF1L",
-            "HNRNPR",
-            "PUM2",
-            "VASP",
-            "TMEM238",
-            "XAB2",
-            "HS6ST1",
-            "MUC3A",
-            "SPATA31A6",
-            "UTP20",
-            "SSR1",
-            "FOXA2",
-            "ANGPTL4",
-            "COL24A1",
-            "NUDT15",
-            "GDF6",
-            "ME2",
-            "ZBTB8B",
-            "RAET1G",
-            "SYCE1",
-            "FAM160B1",
-            "RNF167",
-            "AXIN1",
-            "CD164L2",
-            "TP63",
-            "CINP",
-            "CDK2AP1",
-            "NCAM2",
-            "DIS3L2",
-            "PGBD1",
-            "ING2",
-            "PFN2",
-            "MYO19",
-            "MAGEB17",
-            "FAM114A1",
-            "SPCS3",
-            "DCAF8L2",
-            "IL36A",
-            "PARD3",
-            "MAP3K7",
-            "CDK16",
-            "BMPR2",
-            "PLXNA1",
-            "NAV1",
-            "RPP40",
-            "CRHBP",
-            "ZNF568",
-            "POMGNT1",
-            "TNR",
-            "PTPRK",
-            "LMBRD1",
-            "LGALS2",
-            "CNTNAP3",
-            "SGSH",
-            "COX7A2L",
-            "RAD54L2",
-            "PARP9",
-            "BTN3A1",
-            "AMACR",
-            "PPP1R17",
-            "TMEM8C",
-            "NPW",
-            "SYT2",
-            "JAK1",
-            "SLC25A17",
-            "GDPD1"
+            "LYPD3",
+            "LOC100287477",
+            "RQCD1",
+            "SYNJ2",
+            "SPTAN1",
+            "DOCK8",
+            "COX20",
+            "EPM2A",
+            "SLC26A1",
+            "CHRNB3",
+            "GPR62",
+            "DMP1",
+            "MARCHF6",
+            "CTNNA3",
+            "MTX1",
+            "YIF1A",
+            "FMO1",
+            "USP47",
+            "OPN1LW",
+            "ZNF620",
+            "ARHGAP26",
+            "BFSP2",
+            "SNCAIP",
+            "RPS6KC1",
+            "NCR3",
+            "ZNF658",
+            "SREK1",
+            "PLEKHJ1",
+            "ALG5",
+            "CNN1",
+            "MEP1A",
+            "NUAK2",
+            "VASH2",
+            "IFNA4",
+            "KAT2A",
+            "POLQ",
+            "CASP7",
+            "TYW5",
+            "BCL2L14",
+            "TRMT112",
+            "ZNF217",
+            "UMPS",
+            "RTKN2",
+            "GIPC1",
+            "LLPH",
+            "ZCCHC18",
+            "WDR26",
+            "OR2Y1",
+            "DTNA",
+            "FOXG1",
+            "TMEM40",
+            "NEFH",
+            "WWP1",
+            "DTNBP1",
+            "MBTPS2",
+            "TRIML2",
+            "IL4I1",
+            "EMC1",
+            "MLLT11",
+            "KAT7",
+            "QSOX2",
+            "ZCWPW1",
+            "TICRR",
+            "PRKAR1A",
+            "CRYBB1",
+            "POU2AF1",
+            "MAP1LC3A",
+            "ADGRB2",
+            "ARHGEF17",
+            "DCD",
+            "ADAMTS2",
+            "ING5",
+            "CLRN2",
+            "SOCS4",
+            "PRSS12",
+            "AANAT",
+            "ARHGAP29",
+            "ASPSCR1",
+            "PDE6H",
+            "LY6D",
+            "DAB2IP",
+            "VRK3",
+            "ACTB",
+            "ARMCX2",
+            "PANK3",
+            "DKK4",
+            "ZC3H13",
+            "KLHL15",
+            "CCNB2",
+            "MMP28",
+            "FBLN2",
+            "SERPIND1",
+            "AP2B1",
+            "ZNF154",
+            "FGF14",
+            "DBT",
+            "ADCY7",
+            "EIF5A",
+            "CEP41",
+            "HOMEZ",
+            "KIAA1161",
+            "KIAA1549",
+            "ZNF468",
+            "ACOT8",
+            "FBXO15",
+            "CCNA2",
+            "RAB3GAP2",
+            "AHCYL1",
+            "CSH1",
+            "TCF21",
+            "TMPRSS11B",
+            "TP53I13",
+            "ARL14EPL",
+            "SUMO1",
+            "CNST",
+            "FJX1",
+            "PCDH9",
+            "NAMPT",
+            "COQ2",
+            "NKIRAS2",
+            "SOHLH2",
+            "LENG1",
+            "ERH",
+            "SLIT1",
+            "SMAP2",
+            "GLRA3",
+            "GYS1",
+            "GCLC"
           ],
           "selected_scores": [
-            -0.306600558,
-            -0.942059951,
-            -0.512561534,
-            -0.434762436,
-            -0.515691564,
-            -0.543954085,
-            -0.231849981,
-            -1.30631225,
-            -2.123302384,
-            -0.895888332,
-            -0.893999647,
-            -0.719399047,
-            -1.369489525,
-            -1.580145467,
-            -0.383464419,
-            -0.669472472,
-            -0.313284927,
-            -0.801952387,
-            -0.597616552,
-            -0.112350676,
-            -0.60564137,
-            -0.323889734,
-            -0.539854908,
-            -0.269144461,
-            -0.477657619,
-            -1.753059275,
-            -0.126096573,
-            -0.456952444,
-            -1.107643035,
-            -1.005968912,
-            -1.039459342,
-            -0.566469921,
-            -0.547647084,
-            -2.676961105,
-            -0.720196739,
-            -0.560837764,
-            -0.48859985,
-            -0.504563953,
-            -0.876782278,
-            -0.555709322,
-            -0.684824516,
-            -0.381023993,
-            -0.347115866,
-            -0.828933135,
-            -0.140477532,
-            -0.422164937,
-            -0.461318003,
-            -2.592523477,
-            -0.764022397,
-            -0.566748018,
-            -0.69771725,
-            -0.378330042,
-            -0.934061114,
-            -0.235661351,
-            -1.244838015,
-            -0.307960534,
-            -0.415325668,
-            -0.854138764,
-            -0.656352894,
-            -1.180092247,
-            -0.963236266,
-            -1.080601987,
-            -0.762862387,
-            -0.682290269,
-            -0.755236631,
-            -1.133624527,
-            -0.695619006,
-            -1.307671029,
-            -0.943631679,
-            -1.01937299,
-            -0.906503046,
-            -2.077461957,
-            -1.577564116,
-            -0.295863731,
-            -0.804895793,
-            -1.335594247,
-            -1.575994641,
-            -1.153146511,
-            -0.7198085,
-            -1.738619696,
-            -0.557222438,
-            -1.083570349,
-            -0.513260184,
-            -1.127926173,
-            -1.109688797,
-            -0.329972028,
-            -0.350176452,
-            -0.934284081,
-            -0.44125141,
-            -2.197398787,
-            -0.27799242,
-            -0.935941336,
-            -3.745862679,
-            -2.022894031,
-            -0.359967096,
-            -0.401092105,
-            -0.582838656,
-            -0.313799055,
-            -0.828336324,
-            -0.565361589,
-            -1.438277915,
-            -0.441209211,
-            -0.453217512,
-            -0.046077773,
-            -0.680411001,
-            -0.740697779,
-            -1.098501412,
-            -1.013220548,
-            -0.239185293,
-            -1.252663599,
-            -0.745389295,
-            -1.573596014,
-            -1.485285374,
-            -0.774989349,
-            -1.119232109,
-            -0.996524308,
-            -1.898013587,
-            -0.8352701,
-            -0.376506713,
-            -0.713514398,
-            -2.001973503,
-            -0.708628462,
-            -0.289417769,
-            -0.138030494,
-            -0.823101552,
-            -1.801116994,
-            -0.567387603,
-            -0.384405013
+            -1.35862469,
+            -0.714511497,
+            -0.412618154,
+            -0.946737582,
+            -0.110600586,
+            -0.331870644,
+            -0.231494198,
+            -1.13272984,
+            -0.340620639,
+            -2.974043214,
+            -1.52512221,
+            -0.542018268,
+            -0.353619146,
+            -0.711096746,
+            -0.673788849,
+            -0.475032682,
+            -4.34614456,
+            -0.218625057,
+            -1.070313023,
+            -0.715613633,
+            -0.375240063,
+            -0.961354228,
+            -0.130516403,
+            -0.628991819,
+            -1.33108691,
+            -0.184765673,
+            -1.153381909,
+            -1.051687891,
+            -0.535264912,
+            -1.284906283,
+            -0.646113304,
+            -0.716196527,
+            -0.473840215,
+            -0.366091012,
+            -0.189584307,
+            -1.839250336,
+            -1.10957167,
+            -0.31017817,
+            -0.494356377,
+            -0.82337045,
+            -2.62607704,
+            -0.771155229,
+            -0.651918167,
+            -1.722157093,
+            -0.481776426,
+            -0.984339194,
+            -1.416994653,
+            -0.90365762,
+            -0.881416777,
+            -0.505383294,
+            -1.262485406,
+            -0.738043137,
+            -0.164219297,
+            -0.677369341,
+            -2.831200619,
+            -0.937099889,
+            -0.305075396,
+            -0.129501889,
+            -0.600085993,
+            -0.301507101,
+            -0.620933935,
+            -0.762857292,
+            -1.141863426,
+            -1.529192383,
+            -0.903576324,
+            -0.767488353,
+            -2.515142622,
+            -0.682196751,
+            -1.996654631,
+            -0.507601331,
+            -0.903810552,
+            -0.176333875,
+            -0.191239295,
+            -0.180146011,
+            -0.331270376,
+            -1.317191481,
+            -0.982532766,
+            -0.493709476,
+            -1.195308373,
+            -0.778574612,
+            -1.011509084,
+            -0.694219654,
+            -0.093546774,
+            -0.217900514,
+            -0.76677056,
+            -0.379994765,
+            -0.77871719,
+            -1.562471917,
+            -1.725644291,
+            -0.608958085,
+            -0.352870141,
+            -0.249057418,
+            -0.439214772,
+            -0.163350964,
+            -0.667065541,
+            -0.528454256,
+            -1.046469874,
+            -0.563953435,
+            -0.516591895,
+            -0.956648528,
+            -0.790960097,
+            -0.537273716,
+            -0.696135309,
+            -0.645103279,
+            -0.515742054,
+            -0.271994632,
+            -0.355411507,
+            -0.091852957,
+            -0.582788947,
+            -0.630659951,
+            -0.902259812,
+            -0.527069086,
+            -0.841783023,
+            -0.505812475,
+            -1.221261734,
+            -1.668473818,
+            -1.045287462,
+            -0.501845016,
+            -1.062150642,
+            -0.106123369,
+            -0.483619272,
+            -0.619251179,
+            -0.595676674,
+            -0.892832717,
+            -2.863345223,
+            -0.4349469,
+            -0.33920348,
+            -0.288138675
           ],
           "selected_hits": [
             0,
@@ -309,6 +309,7 @@
             0,
             0,
             0,
+            0,
             1,
             0,
             0,
@@ -316,24 +317,6 @@
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
@@ -348,6 +331,16 @@
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
             1,
             0,
             0,
@@ -362,37 +355,18 @@
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
             1,
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
             1,
             0,
             0,
@@ -426,6 +400,32 @@
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
+            1,
             0,
             0,
             0
@@ -1334,896 +1334,1792 @@
           "gene": "DDI2",
           "score": -0.306600558,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8636,
           "gene": "LONRF2",
           "score": -0.942059951,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18180,
           "gene": "ZNF559-ZNF177",
           "score": -0.512561534,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16793,
           "gene": "TSSC4",
           "score": -0.434762436,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8412,
           "gene": "LDLRAD4",
           "score": -0.515691564,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2621,
           "gene": "CDK15",
           "score": -0.543954085,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4342,
           "gene": "DPPA2",
           "score": -0.231849981,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2572,
           "gene": "CDC5L",
           "score": -1.30631225,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7843,
           "gene": "KDM3B",
           "score": -2.123302384,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11075,
           "gene": "P2RX4",
           "score": -0.895888332,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7131,
           "gene": "HTR3C",
           "score": -0.893999647,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1616,
           "gene": "BRE",
           "score": -0.719399047,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1636,
           "gene": "BRWD1",
           "score": -1.369489525,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16404,
           "gene": "TNFSF8",
           "score": -1.580145467,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1022,
           "gene": "ARL6IP4",
           "score": -0.383464419,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14,
           "gene": "AAGAB",
           "score": -0.669472472,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15730,
           "gene": "TCL1A",
           "score": -0.313284927,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17885,
           "gene": "ZKSCAN7",
           "score": -0.801952387,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 627,
           "gene": "AMOTL2",
           "score": -0.597616552,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6428,
           "gene": "GRID2IP",
           "score": -0.112350676,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4885,
           "gene": "ERP27",
           "score": -0.60564137,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18377,
           "gene": "ZNF83",
           "score": -0.323889734,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7390,
           "gene": "IL36RN",
           "score": -0.539854908,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2867,
           "gene": "CHD6",
           "score": -0.269144461,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2232,
           "gene": "CCDC122",
           "score": -0.477657619,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9744,
           "gene": "MTA2",
           "score": -1.753059275,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5650,
           "gene": "FOXE1",
           "score": -0.126096573,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13272,
           "gene": "RND2",
           "score": -0.456952444,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16645,
           "gene": "TRIM58",
           "score": -1.107643035,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4919,
           "gene": "ETFDH",
           "score": -1.005968912,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4758,
           "gene": "ENOPH1",
           "score": -1.039459342,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11737,
           "gene": "PKM",
           "score": -0.566469921,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2113,
           "gene": "CAPZA2",
           "score": -0.547647084,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 215,
           "gene": "ACTR1B",
           "score": -2.676961105,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3001,
           "gene": "CLASP2",
           "score": -0.720196739,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6510,
           "gene": "GTF2A1",
           "score": -0.560837764,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7382,
           "gene": "IL31",
           "score": -0.48859985,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10022,
           "gene": "NAPB",
           "score": -0.504563953,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15026,
           "gene": "SPINT1",
           "score": -0.876782278,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1421,
           "gene": "BBS10",
           "score": -0.555709322,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17307,
           "gene": "VDR",
           "score": -0.684824516,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15709,
           "gene": "TCEB3CL2",
           "score": -0.381023993,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1364,
           "gene": "B4GALNT3",
           "score": -0.347115866,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15510,
           "gene": "TAC4",
           "score": -0.828933135,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3111,
           "gene": "CLPX",
           "score": -0.140477532,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15828,
           "gene": "TEX40",
           "score": -0.422164937,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7418,
           "gene": "IMPA2",
           "score": -0.461318003,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8791,
           "gene": "LRRTM1",
           "score": -2.592523477,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17031,
           "gene": "UBL7",
           "score": -0.764022397,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16495,
           "gene": "TP73",
           "score": -0.566748018,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13587,
           "gene": "RTN1",
           "score": -0.69771725,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14974,
           "gene": "SPATS2",
           "score": -0.378330042,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18459,
           "gene": "ZWILCH",
           "score": -0.934061114,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13551,
           "gene": "RS1",
           "score": -0.235661351,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14435,
           "gene": "SLC30A6",
           "score": -1.244838015,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15584,
           "gene": "TAS2R20",
           "score": -0.307960534,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1864,
           "gene": "C4orf29",
           "score": -0.415325668,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6154,
           "gene": "GMFB",
           "score": -0.854138764,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13844,
           "gene": "SDHC",
           "score": -0.656352894,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12783,
           "gene": "RABAC1",
           "score": -1.180092247,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5735,
           "gene": "FSTL1",
           "score": -0.963236266,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3436,
           "gene": "CRCP",
           "score": -1.080601987,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 466,
           "gene": "AIF1L",
           "score": -0.762862387,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6953,
           "gene": "HNRNPR",
           "score": -0.682290269,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12644,
           "gene": "PUM2",
           "score": -0.755236631,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17283,
           "gene": "VASP",
           "score": -1.133624527,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16219,
           "gene": "TMEM238",
           "score": -0.695619006,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17587,
           "gene": "XAB2",
           "score": -1.307671029,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7052,
           "gene": "HS6ST1",
           "score": -0.943631679,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9825,
           "gene": "MUC3A",
           "score": -1.01937299,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14957,
           "gene": "SPATA31A6",
           "score": -0.906503046,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17253,
           "gene": "UTP20",
           "score": -2.077461957,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15171,
           "gene": "SSR1",
           "score": -1.577564116,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5635,
           "gene": "FOXA2",
           "score": -0.295863731,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 660,
           "gene": "ANGPTL4",
           "score": -0.804895793,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3254,
           "gene": "COL24A1",
           "score": -1.335594247,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10629,
           "gene": "NUDT15",
           "score": -1.575994641,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5976,
           "gene": "GDF6",
           "score": -1.153146511,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9205,
           "gene": "ME2",
           "score": -0.7198085,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17742,
           "gene": "ZBTB8B",
           "score": -1.738619696,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12824,
           "gene": "RAET1G",
           "score": -0.557222438,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15430,
           "gene": "SYCE1",
           "score": -1.083570349,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5108,
           "gene": "FAM160B1",
           "score": -0.513260184,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13310,
           "gene": "RNF167",
           "score": -1.127926173,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1333,
           "gene": "AXIN1",
           "score": -1.109688797,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2460,
           "gene": "CD164L2",
           "score": -0.329972028,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16494,
           "gene": "TP63",
           "score": -0.350176452,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2973,
           "gene": "CINP",
           "score": -0.934284081,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2628,
           "gene": "CDK2AP1",
           "score": -0.44125141,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10062,
           "gene": "NCAM2",
           "score": -2.197398787,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4136,
           "gene": "DIS3L2",
           "score": -0.27799242,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11533,
           "gene": "PGBD1",
           "score": -0.935941336,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7432,
           "gene": "ING2",
           "score": -3.745862679,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11520,
           "gene": "PFN2",
           "score": -2.022894031,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9918,
           "gene": "MYO19",
           "score": -0.359967096,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8941,
           "gene": "MAGEB17",
           "score": -0.401092105,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5053,
           "gene": "FAM114A1",
           "score": -0.582838656,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14980,
           "gene": "SPCS3",
           "score": -0.313799055,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3865,
           "gene": "DCAF8L2",
           "score": -0.828336324,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7387,
           "gene": "IL36A",
           "score": -0.565361589,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11187,
           "gene": "PARD3",
           "score": -1.438277915,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9028,
           "gene": "MAP3K7",
           "score": -0.441209211,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2622,
           "gene": "CDK16",
           "score": -0.453217512,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1563,
           "gene": "BMPR2",
           "score": -0.046077773,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11878,
           "gene": "PLXNA1",
           "score": -0.680411001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10044,
           "gene": "NAV1",
           "score": -0.740697779,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13470,
           "gene": "RPP40",
           "score": -1.098501412,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3455,
           "gene": "CRHBP",
           "score": -1.013220548,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18189,
           "gene": "ZNF568",
           "score": -0.239185293,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12011,
           "gene": "POMGNT1",
           "score": -1.252663599,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16431,
           "gene": "TNR",
           "score": -0.745389295,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12621,
           "gene": "PTPRK",
           "score": -1.573596014,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8551,
           "gene": "LMBRD1",
           "score": -1.485285374,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8446,
           "gene": "LGALS2",
           "score": -0.774989349,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3212,
           "gene": "CNTNAP3",
           "score": -1.119232109,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14080,
           "gene": "SGSH",
           "score": -0.996524308,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3360,
           "gene": "COX7A2L",
           "score": -1.898013587,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12818,
           "gene": "RAD54L2",
           "score": -0.8352701,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11210,
           "gene": "PARP9",
           "score": -0.376506713,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1675,
           "gene": "BTN3A1",
           "score": -0.713514398,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 602,
           "gene": "AMACR",
           "score": -2.001973503,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12142,
           "gene": "PPP1R17",
           "score": -0.708628462,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16312,
           "gene": "TMEM8C",
           "score": -0.289417769,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10493,
           "gene": "NPW",
           "score": -0.138030494,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15483,
           "gene": "SYT2",
           "score": -0.823101552,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7647,
           "gene": "JAK1",
           "score": -1.801116994,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14350,
           "gene": "SLC25A17",
           "score": -0.567387603,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5982,
           "gene": "GDPD1",
           "score": -0.384405013,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 8869,
+          "gene": "LYPD3",
+          "score": -1.35862469,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8590,
+          "gene": "LOC100287477",
+          "score": -0.714511497,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13526,
+          "gene": "RQCD1",
+          "score": -0.412618154,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15461,
+          "gene": "SYNJ2",
+          "score": -0.946737582,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15079,
+          "gene": "SPTAN1",
+          "score": -0.110600586,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4300,
+          "gene": "DOCK8",
+          "score": -0.331870644,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3348,
+          "gene": "COX20",
+          "score": -0.231494198,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4819,
+          "gene": "EPM2A",
+          "score": -1.13272984,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14390,
+          "gene": "SLC26A1",
+          "score": -0.340620639,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2932,
+          "gene": "CHRNB3",
+          "score": -2.974043214,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 6360,
+          "gene": "GPR62",
+          "score": -1.52512221,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4181,
+          "gene": "DMP1",
+          "score": -0.542018268,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9080,
+          "gene": "MARCHF6",
+          "score": -0.353619146,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3607,
+          "gene": "CTNNA3",
+          "score": -0.711096746,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9811,
+          "gene": "MTX1",
+          "score": -0.673788849,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17651,
+          "gene": "YIF1A",
+          "score": -0.475032682,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5599,
+          "gene": "FMO1",
+          "score": -4.34614456,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 17231,
+          "gene": "USP47",
+          "score": -0.218625057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10787,
+          "gene": "OPN1LW",
+          "score": -1.070313023,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18234,
+          "gene": "ZNF620",
+          "score": -0.715613633,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 939,
+          "gene": "ARHGAP26",
+          "score": -0.375240063,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1503,
+          "gene": "BFSP2",
+          "score": -0.961354228,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14772,
+          "gene": "SNCAIP",
+          "score": -0.130516403,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13514,
+          "gene": "RPS6KC1",
+          "score": -0.628991819,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10099,
+          "gene": "NCR3",
+          "score": -1.33108691,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18257,
+          "gene": "ZNF658",
+          "score": -0.184765673,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15106,
+          "gene": "SREK1",
+          "score": -1.153381909,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11836,
+          "gene": "PLEKHJ1",
+          "score": -1.051687891,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 565,
+          "gene": "ALG5",
+          "score": -0.535264912,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3172,
+          "gene": "CNN1",
+          "score": -1.284906283,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9266,
+          "gene": "MEP1A",
+          "score": -0.646113304,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10611,
+          "gene": "NUAK2",
+          "score": -0.716196527,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17281,
+          "gene": "VASH2",
+          "score": -0.473840215,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7232,
+          "gene": "IFNA4",
+          "score": -0.366091012,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7692,
+          "gene": "KAT2A",
+          "score": -0.189584307,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11974,
+          "gene": "POLQ",
+          "score": -1.839250336,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2152,
+          "gene": "CASP7",
+          "score": -1.10957167,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16954,
+          "gene": "TYW5",
+          "score": -0.31017817,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1457,
+          "gene": "BCL2L14",
+          "score": -0.494356377,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16683,
+          "gene": "TRMT112",
+          "score": -0.82337045,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17966,
+          "gene": "ZNF217",
+          "score": -2.62607704,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 17121,
+          "gene": "UMPS",
+          "score": -0.771155229,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13585,
+          "gene": "RTKN2",
+          "score": -0.651918167,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6059,
+          "gene": "GIPC1",
+          "score": -1.722157093,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8544,
+          "gene": "LLPH",
+          "score": -0.481776426,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17775,
+          "gene": "ZCCHC18",
+          "score": -0.984339194,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17455,
+          "gene": "WDR26",
+          "score": -1.416994653,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10872,
+          "gene": "OR2Y1",
+          "score": -0.90365762,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4401,
+          "gene": "DTNA",
+          "score": -0.881416777,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5654,
+          "gene": "FOXG1",
+          "score": -0.505383294,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16259,
+          "gene": "TMEM40",
+          "score": -1.262485406,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10182,
+          "gene": "NEFH",
+          "score": -0.738043137,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17584,
+          "gene": "WWP1",
+          "score": -0.164219297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4403,
+          "gene": "DTNBP1",
+          "score": -0.677369341,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9146,
+          "gene": "MBTPS2",
+          "score": -2.831200619,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 16667,
+          "gene": "TRIML2",
+          "score": -0.937099889,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7394,
+          "gene": "IL4I1",
+          "score": -0.305075396,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4710,
+          "gene": "EMC1",
+          "score": -0.129501889,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9443,
+          "gene": "MLLT11",
+          "score": -0.600085993,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7697,
+          "gene": "KAT7",
+          "score": -0.301507101,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12703,
+          "gene": "QSOX2",
+          "score": -0.620933935,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17786,
+          "gene": "ZCWPW1",
+          "score": -0.762857292,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15943,
+          "gene": "TICRR",
+          "score": -1.141863426,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12288,
+          "gene": "PRKAR1A",
+          "score": -1.529192383,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3494,
+          "gene": "CRYBB1",
+          "score": -0.903576324,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12043,
+          "gene": "POU2AF1",
+          "score": -0.767488353,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9001,
+          "gene": "MAP1LC3A",
+          "score": -2.515142622,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 318,
+          "gene": "ADGRB2",
+          "score": -0.682196751,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 967,
+          "gene": "ARHGEF17",
+          "score": -1.996654631,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3870,
+          "gene": "DCD",
+          "score": -0.507601331,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 271,
+          "gene": "ADAMTS2",
+          "score": -0.903810552,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7435,
+          "gene": "ING5",
+          "score": -0.176333875,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3113,
+          "gene": "CLRN2",
+          "score": -0.191239295,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14846,
+          "gene": "SOCS4",
+          "score": -0.180146011,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12421,
+          "gene": "PRSS12",
+          "score": -0.331270376,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18,
+          "gene": "AANAT",
+          "score": -1.317191481,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 942,
+          "gene": "ARHGAP29",
+          "score": -0.982532766,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1147,
+          "gene": "ASPSCR1",
+          "score": -0.493709476,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11402,
+          "gene": "PDE6H",
+          "score": -1.195308373,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8847,
+          "gene": "LY6D",
+          "score": -0.778574612,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3803,
+          "gene": "DAB2IP",
+          "score": -1.011509084,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17381,
+          "gene": "VRK3",
+          "score": -0.694219654,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 198,
+          "gene": "ACTB",
+          "score": -0.093546774,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1040,
+          "gene": "ARMCX2",
+          "score": -0.217900514,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11162,
+          "gene": "PANK3",
+          "score": -0.76677056,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4145,
+          "gene": "DKK4",
+          "score": -0.379994765,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17754,
+          "gene": "ZC3H13",
+          "score": -0.77871719,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8044,
+          "gene": "KLHL15",
+          "score": -1.562471917,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2398,
+          "gene": "CCNB2",
+          "score": -1.725644291,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9481,
+          "gene": "MMP28",
+          "score": -0.608958085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5348,
+          "gene": "FBLN2",
+          "score": -0.352870141,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13987,
+          "gene": "SERPIND1",
+          "score": -0.249057418,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 796,
+          "gene": "AP2B1",
+          "score": -0.439214772,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17933,
+          "gene": "ZNF154",
+          "score": -0.163350964,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5494,
+          "gene": "FGF14",
+          "score": -0.667065541,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3845,
+          "gene": "DBT",
+          "score": -0.528454256,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 305,
+          "gene": "ADCY7",
+          "score": -1.046469874,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4662,
+          "gene": "EIF5A",
+          "score": -0.563953435,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2760,
+          "gene": "CEP41",
+          "score": -0.516591895,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6961,
+          "gene": "HOMEZ",
+          "score": -0.956648528,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7906,
+          "gene": "KIAA1161",
+          "score": -0.790960097,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7924,
+          "gene": "KIAA1549",
+          "score": -0.537273716,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18116,
+          "gene": "ZNF468",
+          "score": -0.696135309,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 161,
+          "gene": "ACOT8",
+          "score": -0.645103279,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5378,
+          "gene": "FBXO15",
+          "score": -0.515742054,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2395,
+          "gene": "CCNA2",
+          "score": -0.271994632,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12759,
+          "gene": "RAB3GAP2",
+          "score": -0.355411507,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 451,
+          "gene": "AHCYL1",
+          "score": -0.091852957,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3523,
+          "gene": "CSH1",
+          "score": -0.582788947,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15716,
+          "gene": "TCF21",
+          "score": -0.630659951,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16333,
+          "gene": "TMPRSS11B",
+          "score": -0.902259812,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16484,
+          "gene": "TP53I13",
+          "score": -0.527069086,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1006,
+          "gene": "ARL14EPL",
+          "score": -0.841783023,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15382,
+          "gene": "SUMO1",
+          "score": -0.505812475,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3198,
+          "gene": "CNST",
+          "score": -1.221261734,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5553,
+          "gene": "FJX1",
+          "score": -1.668473818,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11268,
+          "gene": "PCDH9",
+          "score": -1.045287462,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10008,
+          "gene": "NAMPT",
+          "score": -0.501845016,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3322,
+          "gene": "COQ2",
+          "score": -1.062150642,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10317,
+          "gene": "NKIRAS2",
+          "score": -0.106123369,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14856,
+          "gene": "SOHLH2",
+          "score": -0.483619272,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8428,
+          "gene": "LENG1",
+          "score": -0.619251179,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4866,
+          "gene": "ERH",
+          "score": -0.595676674,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14634,
+          "gene": "SLIT1",
+          "score": -0.892832717,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14666,
+          "gene": "SMAP2",
+          "score": -2.863345223,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 6122,
+          "gene": "GLRA3",
+          "score": -0.4349469,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6569,
+          "gene": "GYS1",
+          "score": -0.33920348,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5950,
+          "gene": "GCLC",
+          "score": -0.288138675,
+          "hit": 0,
+          "round": 2
         }
       ],
       "queried_history": [
@@ -3128,896 +4024,1792 @@
           "gene": "DDI2",
           "score": -0.306600558,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8636,
           "gene": "LONRF2",
           "score": -0.942059951,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18180,
           "gene": "ZNF559-ZNF177",
           "score": -0.512561534,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16793,
           "gene": "TSSC4",
           "score": -0.434762436,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8412,
           "gene": "LDLRAD4",
           "score": -0.515691564,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2621,
           "gene": "CDK15",
           "score": -0.543954085,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4342,
           "gene": "DPPA2",
           "score": -0.231849981,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2572,
           "gene": "CDC5L",
           "score": -1.30631225,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7843,
           "gene": "KDM3B",
           "score": -2.123302384,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11075,
           "gene": "P2RX4",
           "score": -0.895888332,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7131,
           "gene": "HTR3C",
           "score": -0.893999647,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1616,
           "gene": "BRE",
           "score": -0.719399047,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1636,
           "gene": "BRWD1",
           "score": -1.369489525,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16404,
           "gene": "TNFSF8",
           "score": -1.580145467,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1022,
           "gene": "ARL6IP4",
           "score": -0.383464419,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14,
           "gene": "AAGAB",
           "score": -0.669472472,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15730,
           "gene": "TCL1A",
           "score": -0.313284927,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17885,
           "gene": "ZKSCAN7",
           "score": -0.801952387,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 627,
           "gene": "AMOTL2",
           "score": -0.597616552,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6428,
           "gene": "GRID2IP",
           "score": -0.112350676,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4885,
           "gene": "ERP27",
           "score": -0.60564137,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18377,
           "gene": "ZNF83",
           "score": -0.323889734,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7390,
           "gene": "IL36RN",
           "score": -0.539854908,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2867,
           "gene": "CHD6",
           "score": -0.269144461,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2232,
           "gene": "CCDC122",
           "score": -0.477657619,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9744,
           "gene": "MTA2",
           "score": -1.753059275,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5650,
           "gene": "FOXE1",
           "score": -0.126096573,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13272,
           "gene": "RND2",
           "score": -0.456952444,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16645,
           "gene": "TRIM58",
           "score": -1.107643035,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4919,
           "gene": "ETFDH",
           "score": -1.005968912,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4758,
           "gene": "ENOPH1",
           "score": -1.039459342,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11737,
           "gene": "PKM",
           "score": -0.566469921,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2113,
           "gene": "CAPZA2",
           "score": -0.547647084,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 215,
           "gene": "ACTR1B",
           "score": -2.676961105,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3001,
           "gene": "CLASP2",
           "score": -0.720196739,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6510,
           "gene": "GTF2A1",
           "score": -0.560837764,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7382,
           "gene": "IL31",
           "score": -0.48859985,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10022,
           "gene": "NAPB",
           "score": -0.504563953,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15026,
           "gene": "SPINT1",
           "score": -0.876782278,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1421,
           "gene": "BBS10",
           "score": -0.555709322,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17307,
           "gene": "VDR",
           "score": -0.684824516,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15709,
           "gene": "TCEB3CL2",
           "score": -0.381023993,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1364,
           "gene": "B4GALNT3",
           "score": -0.347115866,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15510,
           "gene": "TAC4",
           "score": -0.828933135,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3111,
           "gene": "CLPX",
           "score": -0.140477532,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15828,
           "gene": "TEX40",
           "score": -0.422164937,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7418,
           "gene": "IMPA2",
           "score": -0.461318003,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8791,
           "gene": "LRRTM1",
           "score": -2.592523477,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17031,
           "gene": "UBL7",
           "score": -0.764022397,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16495,
           "gene": "TP73",
           "score": -0.566748018,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13587,
           "gene": "RTN1",
           "score": -0.69771725,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14974,
           "gene": "SPATS2",
           "score": -0.378330042,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18459,
           "gene": "ZWILCH",
           "score": -0.934061114,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13551,
           "gene": "RS1",
           "score": -0.235661351,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14435,
           "gene": "SLC30A6",
           "score": -1.244838015,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15584,
           "gene": "TAS2R20",
           "score": -0.307960534,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1864,
           "gene": "C4orf29",
           "score": -0.415325668,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6154,
           "gene": "GMFB",
           "score": -0.854138764,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13844,
           "gene": "SDHC",
           "score": -0.656352894,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12783,
           "gene": "RABAC1",
           "score": -1.180092247,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5735,
           "gene": "FSTL1",
           "score": -0.963236266,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3436,
           "gene": "CRCP",
           "score": -1.080601987,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 466,
           "gene": "AIF1L",
           "score": -0.762862387,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6953,
           "gene": "HNRNPR",
           "score": -0.682290269,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12644,
           "gene": "PUM2",
           "score": -0.755236631,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17283,
           "gene": "VASP",
           "score": -1.133624527,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16219,
           "gene": "TMEM238",
           "score": -0.695619006,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17587,
           "gene": "XAB2",
           "score": -1.307671029,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7052,
           "gene": "HS6ST1",
           "score": -0.943631679,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9825,
           "gene": "MUC3A",
           "score": -1.01937299,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14957,
           "gene": "SPATA31A6",
           "score": -0.906503046,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17253,
           "gene": "UTP20",
           "score": -2.077461957,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15171,
           "gene": "SSR1",
           "score": -1.577564116,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5635,
           "gene": "FOXA2",
           "score": -0.295863731,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 660,
           "gene": "ANGPTL4",
           "score": -0.804895793,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3254,
           "gene": "COL24A1",
           "score": -1.335594247,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10629,
           "gene": "NUDT15",
           "score": -1.575994641,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5976,
           "gene": "GDF6",
           "score": -1.153146511,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9205,
           "gene": "ME2",
           "score": -0.7198085,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17742,
           "gene": "ZBTB8B",
           "score": -1.738619696,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12824,
           "gene": "RAET1G",
           "score": -0.557222438,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15430,
           "gene": "SYCE1",
           "score": -1.083570349,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5108,
           "gene": "FAM160B1",
           "score": -0.513260184,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13310,
           "gene": "RNF167",
           "score": -1.127926173,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1333,
           "gene": "AXIN1",
           "score": -1.109688797,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2460,
           "gene": "CD164L2",
           "score": -0.329972028,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16494,
           "gene": "TP63",
           "score": -0.350176452,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2973,
           "gene": "CINP",
           "score": -0.934284081,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2628,
           "gene": "CDK2AP1",
           "score": -0.44125141,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10062,
           "gene": "NCAM2",
           "score": -2.197398787,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4136,
           "gene": "DIS3L2",
           "score": -0.27799242,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11533,
           "gene": "PGBD1",
           "score": -0.935941336,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7432,
           "gene": "ING2",
           "score": -3.745862679,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11520,
           "gene": "PFN2",
           "score": -2.022894031,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9918,
           "gene": "MYO19",
           "score": -0.359967096,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8941,
           "gene": "MAGEB17",
           "score": -0.401092105,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5053,
           "gene": "FAM114A1",
           "score": -0.582838656,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14980,
           "gene": "SPCS3",
           "score": -0.313799055,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3865,
           "gene": "DCAF8L2",
           "score": -0.828336324,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7387,
           "gene": "IL36A",
           "score": -0.565361589,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11187,
           "gene": "PARD3",
           "score": -1.438277915,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9028,
           "gene": "MAP3K7",
           "score": -0.441209211,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2622,
           "gene": "CDK16",
           "score": -0.453217512,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1563,
           "gene": "BMPR2",
           "score": -0.046077773,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11878,
           "gene": "PLXNA1",
           "score": -0.680411001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10044,
           "gene": "NAV1",
           "score": -0.740697779,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13470,
           "gene": "RPP40",
           "score": -1.098501412,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3455,
           "gene": "CRHBP",
           "score": -1.013220548,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18189,
           "gene": "ZNF568",
           "score": -0.239185293,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12011,
           "gene": "POMGNT1",
           "score": -1.252663599,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16431,
           "gene": "TNR",
           "score": -0.745389295,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12621,
           "gene": "PTPRK",
           "score": -1.573596014,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8551,
           "gene": "LMBRD1",
           "score": -1.485285374,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8446,
           "gene": "LGALS2",
           "score": -0.774989349,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3212,
           "gene": "CNTNAP3",
           "score": -1.119232109,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14080,
           "gene": "SGSH",
           "score": -0.996524308,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3360,
           "gene": "COX7A2L",
           "score": -1.898013587,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12818,
           "gene": "RAD54L2",
           "score": -0.8352701,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11210,
           "gene": "PARP9",
           "score": -0.376506713,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1675,
           "gene": "BTN3A1",
           "score": -0.713514398,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 602,
           "gene": "AMACR",
           "score": -2.001973503,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12142,
           "gene": "PPP1R17",
           "score": -0.708628462,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16312,
           "gene": "TMEM8C",
           "score": -0.289417769,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10493,
           "gene": "NPW",
           "score": -0.138030494,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15483,
           "gene": "SYT2",
           "score": -0.823101552,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7647,
           "gene": "JAK1",
           "score": -1.801116994,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14350,
           "gene": "SLC25A17",
           "score": -0.567387603,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5982,
           "gene": "GDPD1",
           "score": -0.384405013,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 8869,
+          "gene": "LYPD3",
+          "score": -1.35862469,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8590,
+          "gene": "LOC100287477",
+          "score": -0.714511497,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13526,
+          "gene": "RQCD1",
+          "score": -0.412618154,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15461,
+          "gene": "SYNJ2",
+          "score": -0.946737582,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15079,
+          "gene": "SPTAN1",
+          "score": -0.110600586,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4300,
+          "gene": "DOCK8",
+          "score": -0.331870644,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3348,
+          "gene": "COX20",
+          "score": -0.231494198,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4819,
+          "gene": "EPM2A",
+          "score": -1.13272984,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14390,
+          "gene": "SLC26A1",
+          "score": -0.340620639,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2932,
+          "gene": "CHRNB3",
+          "score": -2.974043214,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 6360,
+          "gene": "GPR62",
+          "score": -1.52512221,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4181,
+          "gene": "DMP1",
+          "score": -0.542018268,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9080,
+          "gene": "MARCHF6",
+          "score": -0.353619146,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3607,
+          "gene": "CTNNA3",
+          "score": -0.711096746,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9811,
+          "gene": "MTX1",
+          "score": -0.673788849,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17651,
+          "gene": "YIF1A",
+          "score": -0.475032682,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5599,
+          "gene": "FMO1",
+          "score": -4.34614456,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 17231,
+          "gene": "USP47",
+          "score": -0.218625057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10787,
+          "gene": "OPN1LW",
+          "score": -1.070313023,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18234,
+          "gene": "ZNF620",
+          "score": -0.715613633,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 939,
+          "gene": "ARHGAP26",
+          "score": -0.375240063,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1503,
+          "gene": "BFSP2",
+          "score": -0.961354228,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14772,
+          "gene": "SNCAIP",
+          "score": -0.130516403,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13514,
+          "gene": "RPS6KC1",
+          "score": -0.628991819,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10099,
+          "gene": "NCR3",
+          "score": -1.33108691,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18257,
+          "gene": "ZNF658",
+          "score": -0.184765673,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15106,
+          "gene": "SREK1",
+          "score": -1.153381909,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11836,
+          "gene": "PLEKHJ1",
+          "score": -1.051687891,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 565,
+          "gene": "ALG5",
+          "score": -0.535264912,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3172,
+          "gene": "CNN1",
+          "score": -1.284906283,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9266,
+          "gene": "MEP1A",
+          "score": -0.646113304,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10611,
+          "gene": "NUAK2",
+          "score": -0.716196527,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17281,
+          "gene": "VASH2",
+          "score": -0.473840215,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7232,
+          "gene": "IFNA4",
+          "score": -0.366091012,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7692,
+          "gene": "KAT2A",
+          "score": -0.189584307,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11974,
+          "gene": "POLQ",
+          "score": -1.839250336,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2152,
+          "gene": "CASP7",
+          "score": -1.10957167,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16954,
+          "gene": "TYW5",
+          "score": -0.31017817,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1457,
+          "gene": "BCL2L14",
+          "score": -0.494356377,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16683,
+          "gene": "TRMT112",
+          "score": -0.82337045,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17966,
+          "gene": "ZNF217",
+          "score": -2.62607704,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 17121,
+          "gene": "UMPS",
+          "score": -0.771155229,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13585,
+          "gene": "RTKN2",
+          "score": -0.651918167,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6059,
+          "gene": "GIPC1",
+          "score": -1.722157093,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8544,
+          "gene": "LLPH",
+          "score": -0.481776426,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17775,
+          "gene": "ZCCHC18",
+          "score": -0.984339194,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17455,
+          "gene": "WDR26",
+          "score": -1.416994653,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10872,
+          "gene": "OR2Y1",
+          "score": -0.90365762,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4401,
+          "gene": "DTNA",
+          "score": -0.881416777,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5654,
+          "gene": "FOXG1",
+          "score": -0.505383294,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16259,
+          "gene": "TMEM40",
+          "score": -1.262485406,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10182,
+          "gene": "NEFH",
+          "score": -0.738043137,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17584,
+          "gene": "WWP1",
+          "score": -0.164219297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4403,
+          "gene": "DTNBP1",
+          "score": -0.677369341,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9146,
+          "gene": "MBTPS2",
+          "score": -2.831200619,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 16667,
+          "gene": "TRIML2",
+          "score": -0.937099889,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7394,
+          "gene": "IL4I1",
+          "score": -0.305075396,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4710,
+          "gene": "EMC1",
+          "score": -0.129501889,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9443,
+          "gene": "MLLT11",
+          "score": -0.600085993,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7697,
+          "gene": "KAT7",
+          "score": -0.301507101,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12703,
+          "gene": "QSOX2",
+          "score": -0.620933935,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17786,
+          "gene": "ZCWPW1",
+          "score": -0.762857292,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15943,
+          "gene": "TICRR",
+          "score": -1.141863426,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12288,
+          "gene": "PRKAR1A",
+          "score": -1.529192383,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3494,
+          "gene": "CRYBB1",
+          "score": -0.903576324,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12043,
+          "gene": "POU2AF1",
+          "score": -0.767488353,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9001,
+          "gene": "MAP1LC3A",
+          "score": -2.515142622,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 318,
+          "gene": "ADGRB2",
+          "score": -0.682196751,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 967,
+          "gene": "ARHGEF17",
+          "score": -1.996654631,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3870,
+          "gene": "DCD",
+          "score": -0.507601331,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 271,
+          "gene": "ADAMTS2",
+          "score": -0.903810552,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7435,
+          "gene": "ING5",
+          "score": -0.176333875,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3113,
+          "gene": "CLRN2",
+          "score": -0.191239295,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14846,
+          "gene": "SOCS4",
+          "score": -0.180146011,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12421,
+          "gene": "PRSS12",
+          "score": -0.331270376,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18,
+          "gene": "AANAT",
+          "score": -1.317191481,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 942,
+          "gene": "ARHGAP29",
+          "score": -0.982532766,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1147,
+          "gene": "ASPSCR1",
+          "score": -0.493709476,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11402,
+          "gene": "PDE6H",
+          "score": -1.195308373,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8847,
+          "gene": "LY6D",
+          "score": -0.778574612,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3803,
+          "gene": "DAB2IP",
+          "score": -1.011509084,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17381,
+          "gene": "VRK3",
+          "score": -0.694219654,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 198,
+          "gene": "ACTB",
+          "score": -0.093546774,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1040,
+          "gene": "ARMCX2",
+          "score": -0.217900514,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11162,
+          "gene": "PANK3",
+          "score": -0.76677056,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4145,
+          "gene": "DKK4",
+          "score": -0.379994765,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17754,
+          "gene": "ZC3H13",
+          "score": -0.77871719,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8044,
+          "gene": "KLHL15",
+          "score": -1.562471917,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2398,
+          "gene": "CCNB2",
+          "score": -1.725644291,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9481,
+          "gene": "MMP28",
+          "score": -0.608958085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5348,
+          "gene": "FBLN2",
+          "score": -0.352870141,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13987,
+          "gene": "SERPIND1",
+          "score": -0.249057418,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 796,
+          "gene": "AP2B1",
+          "score": -0.439214772,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17933,
+          "gene": "ZNF154",
+          "score": -0.163350964,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5494,
+          "gene": "FGF14",
+          "score": -0.667065541,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3845,
+          "gene": "DBT",
+          "score": -0.528454256,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 305,
+          "gene": "ADCY7",
+          "score": -1.046469874,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4662,
+          "gene": "EIF5A",
+          "score": -0.563953435,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2760,
+          "gene": "CEP41",
+          "score": -0.516591895,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6961,
+          "gene": "HOMEZ",
+          "score": -0.956648528,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7906,
+          "gene": "KIAA1161",
+          "score": -0.790960097,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7924,
+          "gene": "KIAA1549",
+          "score": -0.537273716,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18116,
+          "gene": "ZNF468",
+          "score": -0.696135309,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 161,
+          "gene": "ACOT8",
+          "score": -0.645103279,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5378,
+          "gene": "FBXO15",
+          "score": -0.515742054,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2395,
+          "gene": "CCNA2",
+          "score": -0.271994632,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12759,
+          "gene": "RAB3GAP2",
+          "score": -0.355411507,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 451,
+          "gene": "AHCYL1",
+          "score": -0.091852957,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3523,
+          "gene": "CSH1",
+          "score": -0.582788947,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15716,
+          "gene": "TCF21",
+          "score": -0.630659951,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16333,
+          "gene": "TMPRSS11B",
+          "score": -0.902259812,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16484,
+          "gene": "TP53I13",
+          "score": -0.527069086,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1006,
+          "gene": "ARL14EPL",
+          "score": -0.841783023,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15382,
+          "gene": "SUMO1",
+          "score": -0.505812475,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3198,
+          "gene": "CNST",
+          "score": -1.221261734,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5553,
+          "gene": "FJX1",
+          "score": -1.668473818,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11268,
+          "gene": "PCDH9",
+          "score": -1.045287462,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10008,
+          "gene": "NAMPT",
+          "score": -0.501845016,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3322,
+          "gene": "COQ2",
+          "score": -1.062150642,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10317,
+          "gene": "NKIRAS2",
+          "score": -0.106123369,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14856,
+          "gene": "SOHLH2",
+          "score": -0.483619272,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8428,
+          "gene": "LENG1",
+          "score": -0.619251179,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4866,
+          "gene": "ERH",
+          "score": -0.595676674,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14634,
+          "gene": "SLIT1",
+          "score": -0.892832717,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14666,
+          "gene": "SMAP2",
+          "score": -2.863345223,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 6122,
+          "gene": "GLRA3",
+          "score": -0.4349469,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6569,
+          "gene": "GYS1",
+          "score": -0.33920348,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5950,
+          "gene": "GCLC",
+          "score": -0.288138675,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
