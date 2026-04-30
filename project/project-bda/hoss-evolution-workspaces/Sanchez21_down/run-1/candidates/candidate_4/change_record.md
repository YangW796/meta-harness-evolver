# Change Record — candidate_4

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21_down/run-1/best/current/harness
Generated at: 2026-04-30T07:01:22.352672

## Files Changed

- model.py: modified (added=22, deleted=5, delta=17)
- outputs/metrics.json: modified (added=2410, deleted=618, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -227,7 +227,16 @@
             'beta_n': beta_n
         }
     
-    # Thompson Sampling: sample from posterior predictive (Student-t)
+    # Enhanced Thompson Sampling with explicit exploration bonus
+    # Estimate total rounds from history to calibrate exploration
+    observed_rounds = len(set(h.get('round', 0) for h in history))
+    total_rounds_estimate = max(5, observed_rounds + 1)  # At least 5 rounds expected
+    
+    # Exploration coefficient: higher early on, decays with rounds
+    # Starts at 2.0 for round 1, decays to 0.5 by final round
+    exploration_coeff = 2.0 * (1.0 - 0.75 * (observed_rounds / total_rounds_estimate))
+    exploration_coeff = max(0.5, exploration_coeff)  # Minimum exploration
+    
     sampled_scores = {}
     
     for idx in available:
@@ -243,11 +252,19 @@
         # Sample precision from Gamma
         tau = np.random.gamma(post['alpha_n'], 1.0 / post['beta_n'])
         
+        # Compute standard deviation (uncertainty)
+        std_dev = 1.0 / np.sqrt(post['lambda_n'] * tau)
+        
         # Sample mean from Gaussian given precision
-        mean_sample = np.random.normal(post['mu_n'], 1.0 / np.sqrt(post['lambda_n'] * tau))
-        
-        # Store sampled score (we want more negative = better for this task)
-        sampled_scores[idx] = mean_sample
+        mean_sample = np.random.normal(post['mu_n'], std_dev)
+        
+        # Add exploration bonus: favor high-uncertainty candidates
+        # For this task (more negative = better), subtract exploration term
+        exploration_bonus = exploration_coeff * std_dev
+        exploration_sample = mean_sample - exploration_bonus
+        
+        # Store sampled score with exploration bonus
+        sampled_scores[idx] = exploration_sample
     
     # Select top candidates by sampled score (prioritize more negative values)
     sorted_by_sample = sorted(available, key=lambda x: sampled_scores[x])

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18469,
-      "rounds": 3,
+      "rounds": 4,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 256,
-      "baseline_total_hits": 10,
+      "baseline_total_queries": 384,
+      "baseline_total_hits": 16,
       "delta_queries": 128,
-      "delta_hits": 6,
-      "total_queries": 384,
-      "total_hits": 16,
+      "delta_hits": 3,
+      "total_queries": 512,
+      "total_hits": 19,
       "top_k": 924,
       "hit_curve": {
         "queries": [
-          256,
-          384
+          384,
+          512
         ],
         "hits": [
-          10,
-          16
+          16,
+          19
         ]
       },
-      "auc": 1664.0,
-      "auc_normalized": 0.00468975468975469,
-      "ncg": 0.22354381263581585,
+      "auc": 2240.0,
+      "auc_normalized": 0.004734848484848485,
+      "ncg": 0.24199090775013854,
       "round_details": [
         {
-          "round": 2,
+          "round": 3,
           "selected_count": 128,
-          "hits": 6,
-          "cumulative_hits": 16,
-          "precision_at_batch": 0.046875,
+          "hits": 3,
+          "cumulative_hits": 19,
+          "precision_at_batch": 0.0234375,
           "selected": [
-            "LYPD3",
-            "LOC100287477",
-            "RQCD1",
-            "SYNJ2",
-            "SPTAN1",
-            "DOCK8",
-            "COX20",
-            "EPM2A",
-            "SLC26A1",
-            "CHRNB3",
-            "GPR62",
-            "DMP1",
-            "MARCHF6",
-            "CTNNA3",
-            "MTX1",
-            "YIF1A",
-            "FMO1",
-            "USP47",
-            "OPN1LW",
-            "ZNF620",
-            "ARHGAP26",
-            "BFSP2",
-            "SNCAIP",
-            "RPS6KC1",
-            "NCR3",
-            "ZNF658",
-            "SREK1",
-            "PLEKHJ1",
-            "ALG5",
-            "CNN1",
-            "MEP1A",
-            "NUAK2",
-            "VASH2",
-            "IFNA4",
-            "KAT2A",
-            "POLQ",
-            "CASP7",
-            "TYW5",
-            "BCL2L14",
-            "TRMT112",
-            "ZNF217",
-            "UMPS",
-            "RTKN2",
-            "GIPC1",
-            "LLPH",
-            "ZCCHC18",
-            "WDR26",
-            "OR2Y1",
-            "DTNA",
-            "FOXG1",
-            "TMEM40",
-            "NEFH",
-            "WWP1",
-            "DTNBP1",
-            "MBTPS2",
-            "TRIML2",
-            "IL4I1",
-            "EMC1",
-            "MLLT11",
-            "KAT7",
-            "QSOX2",
-            "ZCWPW1",
-            "TICRR",
-            "PRKAR1A",
-            "CRYBB1",
-            "POU2AF1",
-            "MAP1LC3A",
-            "ADGRB2",
-            "ARHGEF17",
-            "DCD",
-            "ADAMTS2",
-            "ING5",
-            "CLRN2",
-            "SOCS4",
-            "PRSS12",
-            "AANAT",
-            "ARHGAP29",
-            "ASPSCR1",
-            "PDE6H",
-            "LY6D",
-            "DAB2IP",
-            "VRK3",
-            "ACTB",
-            "ARMCX2",
-            "PANK3",
-            "DKK4",
-            "ZC3H13",
-            "KLHL15",
-            "CCNB2",
-            "MMP28",
-            "FBLN2",
-            "SERPIND1",
-            "AP2B1",
-            "ZNF154",
-            "FGF14",
-            "DBT",
-            "ADCY7",
-            "EIF5A",
-            "CEP41",
-            "HOMEZ",
-            "KIAA1161",
-            "KIAA1549",
-            "ZNF468",
-            "ACOT8",
-            "FBXO15",
-            "CCNA2",
-            "RAB3GAP2",
-            "AHCYL1",
-            "CSH1",
-            "TCF21",
-            "TMPRSS11B",
-            "TP53I13",
-            "ARL14EPL",
-            "SUMO1",
-            "CNST",
-            "FJX1",
-            "PCDH9",
-            "NAMPT",
-            "COQ2",
-            "NKIRAS2",
-            "SOHLH2",
-            "LENG1",
-            "ERH",
-            "SLIT1",
-            "SMAP2",
-            "GLRA3",
-            "GYS1",
-            "GCLC"
+            "ECD",
+            "SYT3",
+            "RRM1",
+            "BAZ1B",
+            "BLOC1S6",
+            "PLCXD2",
+            "CRISP3",
+            "MAPK9",
+            "PITPNB",
+            "CASR",
+            "PCSK2",
+            "LMO7",
+            "ATP6V1B2",
+            "IRAK3",
+            "FSCN1",
+            "METAP1",
+            "TIPARP",
+            "EXOC3L4",
+            "GPR180",
+            "ARHGEF19",
+            "CD48",
+            "NCL",
+            "TFDP3",
+            "ST6GALNAC6",
+            "ZNF92",
+            "PPP1R26",
+            "HERC4",
+            "MCM6",
+            "SPECC1L",
+            "ZNF639",
+            "ENDOU",
+            "APEX1",
+            "SIDT1",
+            "TAPBP",
+            "BSDC1",
+            "SERAC1",
+            "SPC24",
+            "MAP2K3",
+            "MORN5",
+            "FAM3A",
+            "LYN",
+            "PRSS54",
+            "S100A6",
+            "DNAJA1",
+            "PTGS1",
+            "TBXA2R",
+            "MSTN",
+            "ZNF613",
+            "ANKRD17",
+            "INCA1",
+            "RBM41",
+            "FTL",
+            "CFAP45",
+            "SLC7A3",
+            "ARPC5L",
+            "SLC22A13",
+            "MXRA7",
+            "NME4",
+            "ZFYVE19",
+            "UTP11L",
+            "ZNF860",
+            "DNM2",
+            "ELMO2",
+            "CSTL1",
+            "SPERT",
+            "ASB10",
+            "TEKT5",
+            "TBX2",
+            "EXOG",
+            "PHLDB3",
+            "JAG1",
+            "LCE1B",
+            "GPR155",
+            "TMEM182",
+            "TMX4",
+            "HOMER3",
+            "SEMA6A",
+            "LACRT",
+            "NECAB1",
+            "TNNT2",
+            "HTR1D",
+            "TRMT10B",
+            "KIAA1598",
+            "ASCL1",
+            "PCDHGA1",
+            "TTLL4",
+            "NCOA7",
+            "HSH2D",
+            "LRCH3",
+            "CSNK1G3",
+            "MYCT1",
+            "HBG2",
+            "OR6Y1",
+            "PPP1R16B",
+            "WDR89",
+            "GPR82",
+            "COL4A1",
+            "SFI1",
+            "DTD2",
+            "LRRC14B",
+            "LCK",
+            "EIF2AK4",
+            "PRPF6",
+            "RAD51B",
+            "BCL2L11",
+            "TRIM67",
+            "SLC6A16",
+            "CLNK",
+            "HAS1",
+            "SEC24D",
+            "FOXO3",
+            "TFDP2",
+            "TMEM41B",
+            "SLC24A5",
+            "GZMH",
+            "MKL1",
+            "SYNCRIP",
+            "QSOX1",
+            "HEATR1",
+            "BTBD11",
+            "ZNF16",
+            "ZSCAN30",
+            "ZNF35",
+            "BOD1L1",
+            "LPPR3",
+            "SFTA2",
+            "PROSER1",
+            "SCNN1D"
           ],
           "selected_scores": [
-            -1.35862469,
-            -0.714511497,
-            -0.412618154,
-            -0.946737582,
-            -0.110600586,
-            -0.331870644,
-            -0.231494198,
-            -1.13272984,
-            -0.340620639,
-            -2.974043214,
-            -1.52512221,
-            -0.542018268,
-            -0.353619146,
-            -0.711096746,
-            -0.673788849,
-            -0.475032682,
-            -4.34614456,
-            -0.218625057,
-            -1.070313023,
-            -0.715613633,
-            -0.375240063,
-            -0.961354228,
-            -0.130516403,
-            -0.628991819,
-            -1.33108691,
-            -0.184765673,
-            -1.153381909,
-            -1.051687891,
-            -0.535264912,
-            -1.284906283,
-            -0.646113304,
-            -0.716196527,
-            -0.473840215,
-            -0.366091012,
-            -0.189584307,
-            -1.839250336,
-            -1.10957167,
-            -0.31017817,
-            -0.494356377,
-            -0.82337045,
-            -2.62607704,
-            -0.771155229,
-            -0.651918167,
-            -1.722157093,
-            -0.481776426,
-            -0.984339194,
-            -1.416994653,
-            -0.90365762,
-            -0.881416777,
-            -0.505383294,
-            -1.262485406,
-            -0.738043137,
-            -0.164219297,
-            -0.677369341,
-            -2.831200619,
-            -0.937099889,
-            -0.305075396,
-            -0.129501889,
-            -0.600085993,
-            -0.301507101,
-            -0.620933935,
-            -0.762857292,
-            -1.141863426,
-            -1.529192383,
-            -0.903576324,
-            -0.767488353,
-            -2.515142622,
-            -0.682196751,
-            -1.996654631,
-            -0.507601331,
-            -0.903810552,
-            -0.176333875,
-            -0.191239295,
-            -0.180146011,
-            -0.331270376,
-            -1.317191481,
-            -0.982532766,
-            -0.493709476,
-            -1.195308373,
-            -0.778574612,
-            -1.011509084,
-            -0.694219654,
-            -0.093546774,
-            -0.217900514,
-            -0.76677056,
-            -0.379994765,
-            -0.77871719,
-            -1.562471917,
-            -1.725644291,
-            -0.608958085,
-            -0.352870141,
-            -0.249057418,
-            -0.439214772,
-            -0.163350964,
-            -0.667065541,
-            -0.528454256,
-            -1.046469874,
-            -0.563953435,
-            -0.516591895,
-            -0.956648528,
-            -0.790960097,
-            -0.537273716,
-            -0.696135309,
-            -0.645103279,
-            -0.515742054,
-            -0.271994632,
-            -0.355411507,
-            -0.091852957,
-            -0.582788947,
-            -0.630659951,
-            -0.902259812,
-            -0.527069086,
-            -0.841783023,
-            -0.505812475,
-            -1.221261734,
-            -1.668473818,
-            -1.045287462,
-            -0.501845016,
-            -1.062150642,
-            -0.106123369,
-            -0.483619272,
-            -0.619251179,
-            -0.595676674,
-            -0.892832717,
-            -2.863345223,
-            -0.4349469,
-            -0.33920348,
-            -0.288138675
+            -0.771727807,
+            -0.657671024,
+            -1.589108919,
+            -1.358205594,
+            -0.709688832,
+            -0.82898389,
+            -0.68294363,
+            -0.107817483,
+            -0.613558182,
+            -0.603843115,
+            -1.428592082,
+            -1.038774629,
+            -0.64175475,
+            -0.55630682,
+            -1.737922516,
+            -3.467403866,
+            -0.723071233,
+            -0.279485651,
+            -0.205966576,
+            -0.42081153,
+            -1.462076556,
+            -1.334924453,
+            -1.668787689,
+            -0.341726043,
+            -1.976399656,
+            -0.317375955,
+            -0.617694233,
+            -0.621614572,
+            -0.199774547,
+            -0.68097358,
+            -0.543100757,
+            -0.803498906,
+            -0.392442658,
+            -1.087895224,
+            -1.056781378,
+            -0.730893618,
+            -0.28586155,
+            -0.138621146,
+            -1.288641038,
+            -0.800316735,
+            -0.363114043,
+            -0.990354612,
+            -1.689889747,
+            -0.006179969,
+            -0.458220964,
+            -1.19988353,
+            -0.771792541,
+            -0.559903684,
+            -0.492526171,
+            -0.547074506,
+            -1.192523699,
+            -0.939115266,
+            -0.685511331,
+            -1.68097089,
+            -1.813787653,
+            -2.606926552,
+            -0.555642515,
+            -1.391680682,
+            -0.378750065,
+            -0.186709721,
+            -0.157582105,
+            -2.099300133,
+            -0.722450379,
+            -1.588077652,
+            -0.858794701,
+            -1.354822467,
+            -0.196528938,
+            -0.307810077,
+            -0.55416703,
+            -0.780692943,
+            -0.525434014,
+            -0.35401784,
+            -0.646506215,
+            -0.469387502,
+            -0.225968331,
+            -0.661488558,
+            -0.602172178,
+            -0.687435288,
+            -0.603126514,
+            -0.871145657,
+            -0.939109947,
+            -1.130523021,
+            -0.40591144,
+            -0.442493635,
+            -1.106021124,
+            -0.727006676,
+            -1.930474871,
+            -0.801102116,
+            -1.218507103,
+            -1.660520671,
+            -0.518249823,
+            -0.751676373,
+            -1.348577222,
+            -1.546194645,
+            -0.644404655,
+            -1.35659231,
+            -0.542830084,
+            -0.499479583,
+            -1.08526838,
+            -0.343087942,
+            -0.52052891,
+            -0.204981202,
+            -0.609118337,
+            -0.789476994,
+            -1.676432541,
+            -0.917894817,
+            -1.931530047,
+            -1.408963114,
+            -0.605557261,
+            -0.437243173,
+            -1.015406624,
+            -0.267557884,
+            -0.416568026,
+            -1.016902515,
+            -0.524681967,
+            -0.991542854,
+            -0.771070943,
+            -0.049414434,
+            -1.76546051,
+            -1.259541465,
+            -0.934229552,
+            -0.164749845,
+            -0.336678778,
+            -0.083415498,
+            -0.468513215,
+            -0.626802614,
+            -0.380465795,
+            -0.473168344
           ],
           "selected_hits": [
             0,
@@ -310,6 +310,12 @@
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
@@ -317,30 +323,45 @@
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
@@ -355,77 +376,56 @@
             0,
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
-            0,
-            0,
-            0,
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
             0
@@ -2230,896 +2230,1792 @@
           "gene": "LYPD3",
           "score": -1.35862469,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8590,
           "gene": "LOC100287477",
           "score": -0.714511497,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13526,
           "gene": "RQCD1",
           "score": -0.412618154,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15461,
           "gene": "SYNJ2",
           "score": -0.946737582,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15079,
           "gene": "SPTAN1",
           "score": -0.110600586,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4300,
           "gene": "DOCK8",
           "score": -0.331870644,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3348,
           "gene": "COX20",
           "score": -0.231494198,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4819,
           "gene": "EPM2A",
           "score": -1.13272984,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14390,
           "gene": "SLC26A1",
           "score": -0.340620639,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2932,
           "gene": "CHRNB3",
           "score": -2.974043214,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6360,
           "gene": "GPR62",
           "score": -1.52512221,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4181,
           "gene": "DMP1",
           "score": -0.542018268,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9080,
           "gene": "MARCHF6",
           "score": -0.353619146,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3607,
           "gene": "CTNNA3",
           "score": -0.711096746,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9811,
           "gene": "MTX1",
           "score": -0.673788849,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17651,
           "gene": "YIF1A",
           "score": -0.475032682,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5599,
           "gene": "FMO1",
           "score": -4.34614456,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17231,
           "gene": "USP47",
           "score": -0.218625057,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10787,
           "gene": "OPN1LW",
           "score": -1.070313023,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18234,
           "gene": "ZNF620",
           "score": -0.715613633,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 939,
           "gene": "ARHGAP26",
           "score": -0.375240063,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1503,
           "gene": "BFSP2",
           "score": -0.961354228,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14772,
           "gene": "SNCAIP",
           "score": -0.130516403,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13514,
           "gene": "RPS6KC1",
           "score": -0.628991819,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10099,
           "gene": "NCR3",
           "score": -1.33108691,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18257,
           "gene": "ZNF658",
           "score": -0.184765673,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15106,
           "gene": "SREK1",
           "score": -1.153381909,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11836,
           "gene": "PLEKHJ1",
           "score": -1.051687891,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 565,
           "gene": "ALG5",
           "score": -0.535264912,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3172,
           "gene": "CNN1",
           "score": -1.284906283,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9266,
           "gene": "MEP1A",
           "score": -0.646113304,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10611,
           "gene": "NUAK2",
           "score": -0.716196527,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17281,
           "gene": "VASH2",
           "score": -0.473840215,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7232,
           "gene": "IFNA4",
           "score": -0.366091012,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7692,
           "gene": "KAT2A",
           "score": -0.189584307,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11974,
           "gene": "POLQ",
           "score": -1.839250336,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2152,
           "gene": "CASP7",
           "score": -1.10957167,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16954,
           "gene": "TYW5",
           "score": -0.31017817,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1457,
           "gene": "BCL2L14",
           "score": -0.494356377,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16683,
           "gene": "TRMT112",
           "score": -0.82337045,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17966,
           "gene": "ZNF217",
           "score": -2.62607704,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17121,
           "gene": "UMPS",
           "score": -0.771155229,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13585,
           "gene": "RTKN2",
           "score": -0.651918167,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6059,
           "gene": "GIPC1",
           "score": -1.722157093,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8544,
           "gene": "LLPH",
           "score": -0.481776426,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17775,
           "gene": "ZCCHC18",
           "score": -0.984339194,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17455,
           "gene": "WDR26",
           "score": -1.416994653,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10872,
           "gene": "OR2Y1",
           "score": -0.90365762,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4401,
           "gene": "DTNA",
           "score": -0.881416777,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5654,
           "gene": "FOXG1",
           "score": -0.505383294,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16259,
           "gene": "TMEM40",
           "score": -1.262485406,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10182,
           "gene": "NEFH",
           "score": -0.738043137,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17584,
           "gene": "WWP1",
           "score": -0.164219297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4403,
           "gene": "DTNBP1",
           "score": -0.677369341,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9146,
           "gene": "MBTPS2",
           "score": -2.831200619,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16667,
           "gene": "TRIML2",
           "score": -0.937099889,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7394,
           "gene": "IL4I1",
           "score": -0.305075396,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4710,
           "gene": "EMC1",
           "score": -0.129501889,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9443,
           "gene": "MLLT11",
           "score": -0.600085993,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7697,
           "gene": "KAT7",
           "score": -0.301507101,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12703,
           "gene": "QSOX2",
           "score": -0.620933935,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17786,
           "gene": "ZCWPW1",
           "score": -0.762857292,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15943,
           "gene": "TICRR",
           "score": -1.141863426,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12288,
           "gene": "PRKAR1A",
           "score": -1.529192383,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3494,
           "gene": "CRYBB1",
           "score": -0.903576324,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12043,
           "gene": "POU2AF1",
           "score": -0.767488353,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9001,
           "gene": "MAP1LC3A",
           "score": -2.515142622,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 318,
           "gene": "ADGRB2",
           "score": -0.682196751,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 967,
           "gene": "ARHGEF17",
           "score": -1.996654631,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3870,
           "gene": "DCD",
           "score": -0.507601331,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 271,
           "gene": "ADAMTS2",
           "score": -0.903810552,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7435,
           "gene": "ING5",
           "score": -0.176333875,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3113,
           "gene": "CLRN2",
           "score": -0.191239295,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14846,
           "gene": "SOCS4",
           "score": -0.180146011,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12421,
           "gene": "PRSS12",
           "score": -0.331270376,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18,
           "gene": "AANAT",
           "score": -1.317191481,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 942,
           "gene": "ARHGAP29",
           "score": -0.982532766,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1147,
           "gene": "ASPSCR1",
           "score": -0.493709476,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11402,
           "gene": "PDE6H",
           "score": -1.195308373,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8847,
           "gene": "LY6D",
           "score": -0.778574612,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3803,
           "gene": "DAB2IP",
           "score": -1.011509084,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17381,
           "gene": "VRK3",
           "score": -0.694219654,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 198,
           "gene": "ACTB",
           "score": -0.093546774,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1040,
           "gene": "ARMCX2",
           "score": -0.217900514,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11162,
           "gene": "PANK3",
           "score": -0.76677056,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4145,
           "gene": "DKK4",
           "score": -0.379994765,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17754,
           "gene": "ZC3H13",
           "score": -0.77871719,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8044,
           "gene": "KLHL15",
           "score": -1.562471917,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2398,
           "gene": "CCNB2",
           "score": -1.725644291,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9481,
           "gene": "MMP28",
           "score": -0.608958085,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5348,
           "gene": "FBLN2",
           "score": -0.352870141,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13987,
           "gene": "SERPIND1",
           "score": -0.249057418,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 796,
           "gene": "AP2B1",
           "score": -0.439214772,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17933,
           "gene": "ZNF154",
           "score": -0.163350964,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5494,
           "gene": "FGF14",
           "score": -0.667065541,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3845,
           "gene": "DBT",
           "score": -0.528454256,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 305,
           "gene": "ADCY7",
           "score": -1.046469874,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4662,
           "gene": "EIF5A",
           "score": -0.563953435,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2760,
           "gene": "CEP41",
           "score": -0.516591895,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6961,
           "gene": "HOMEZ",
           "score": -0.956648528,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7906,
           "gene": "KIAA1161",
           "score": -0.790960097,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7924,
           "gene": "KIAA1549",
           "score": -0.537273716,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18116,
           "gene": "ZNF468",
           "score": -0.696135309,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 161,
           "gene": "ACOT8",
           "score": -0.645103279,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5378,
           "gene": "FBXO15",
           "score": -0.515742054,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2395,
           "gene": "CCNA2",
           "score": -0.271994632,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12759,
           "gene": "RAB3GAP2",
           "score": -0.355411507,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 451,
           "gene": "AHCYL1",
           "score": -0.091852957,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3523,
           "gene": "CSH1",
           "score": -0.582788947,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15716,
           "gene": "TCF21",
           "score": -0.630659951,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16333,
           "gene": "TMPRSS11B",
           "score": -0.902259812,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16484,
           "gene": "TP53I13",
           "score": -0.527069086,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1006,
           "gene": "ARL14EPL",
           "score": -0.841783023,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15382,
           "gene": "SUMO1",
           "score": -0.505812475,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3198,
           "gene": "CNST",
           "score": -1.221261734,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5553,
           "gene": "FJX1",
           "score": -1.668473818,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11268,
           "gene": "PCDH9",
           "score": -1.045287462,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10008,
           "gene": "NAMPT",
           "score": -0.501845016,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3322,
           "gene": "COQ2",
           "score": -1.062150642,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10317,
           "gene": "NKIRAS2",
           "score": -0.106123369,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14856,
           "gene": "SOHLH2",
           "score": -0.483619272,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8428,
           "gene": "LENG1",
           "score": -0.619251179,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4866,
           "gene": "ERH",
           "score": -0.595676674,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14634,
           "gene": "SLIT1",
           "score": -0.892832717,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14666,
           "gene": "SMAP2",
           "score": -2.863345223,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6122,
           "gene": "GLRA3",
           "score": -0.4349469,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6569,
           "gene": "GYS1",
           "score": -0.33920348,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5950,
           "gene": "GCLC",
           "score": -0.288138675,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 4504,
+          "gene": "ECD",
+          "score": -0.771727807,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15484,
+          "gene": "SYT3",
+          "score": -0.657671024,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13537,
+          "gene": "RRM1",
+          "score": -1.589108919,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1414,
+          "gene": "BAZ1B",
+          "score": -1.358205594,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1542,
+          "gene": "BLOC1S6",
+          "score": -0.709688832,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11800,
+          "gene": "PLCXD2",
+          "score": -0.82898389,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3466,
+          "gene": "CRISP3",
+          "score": -0.68294363,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9061,
+          "gene": "MAPK9",
+          "score": -0.107817483,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11707,
+          "gene": "PITPNB",
+          "score": -0.613558182,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2158,
+          "gene": "CASR",
+          "score": -0.603843115,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11353,
+          "gene": "PCSK2",
+          "score": -1.428592082,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8565,
+          "gene": "LMO7",
+          "score": -1.038774629,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1272,
+          "gene": "ATP6V1B2",
+          "score": -0.64175475,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7524,
+          "gene": "IRAK3",
+          "score": -0.55630682,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5724,
+          "gene": "FSCN1",
+          "score": -1.737922516,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9277,
+          "gene": "METAP1",
+          "score": -3.467403866,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 15979,
+          "gene": "TIPARP",
+          "score": -0.723071233,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4960,
+          "gene": "EXOC3L4",
+          "score": -0.279485651,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6335,
+          "gene": "GPR180",
+          "score": -0.205966576,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 969,
+          "gene": "ARHGEF19",
+          "score": -0.42081153,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2510,
+          "gene": "CD48",
+          "score": -1.462076556,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10085,
+          "gene": "NCL",
+          "score": -1.334924453,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15844,
+          "gene": "TFDP3",
+          "score": -1.668787689,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15213,
+          "gene": "ST6GALNAC6",
+          "score": -0.341726043,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18403,
+          "gene": "ZNF92",
+          "score": -1.976399656,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12149,
+          "gene": "PPP1R26",
+          "score": -0.317375955,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6725,
+          "gene": "HERC4",
+          "score": -0.617694233,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9174,
+          "gene": "MCM6",
+          "score": -0.621614572,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14991,
+          "gene": "SPECC1L",
+          "score": -0.199774547,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18246,
+          "gene": "ZNF639",
+          "score": -0.68097358,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4747,
+          "gene": "ENDOU",
+          "score": -0.543100757,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 828,
+          "gene": "APEX1",
+          "score": -0.803498906,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14167,
+          "gene": "SIDT1",
+          "score": -0.392442658,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15565,
+          "gene": "TAPBP",
+          "score": -1.087895224,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1639,
+          "gene": "BSDC1",
+          "score": -1.056781378,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13949,
+          "gene": "SERAC1",
+          "score": -0.730893618,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14976,
+          "gene": "SPC24",
+          "score": -0.28586155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9010,
+          "gene": "MAP2K3",
+          "score": -0.138621146,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9529,
+          "gene": "MORN5",
+          "score": -1.288641038,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5225,
+          "gene": "FAM3A",
+          "score": -0.800316735,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8865,
+          "gene": "LYN",
+          "score": -0.363114043,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12441,
+          "gene": "PRSS54",
+          "score": -0.990354612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13645,
+          "gene": "S100A6",
+          "score": -1.689889747,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4217,
+          "gene": "DNAJA1",
+          "score": -0.006179969,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12574,
+          "gene": "PTGS1",
+          "score": -0.458220964,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15683,
+          "gene": "TBXA2R",
+          "score": -1.19988353,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9728,
+          "gene": "MSTN",
+          "score": -0.771792541,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18228,
+          "gene": "ZNF613",
+          "score": -0.559903684,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 693,
+          "gene": "ANKRD17",
+          "score": -0.492526171,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7428,
+          "gene": "INCA1",
+          "score": -0.547074506,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12966,
+          "gene": "RBM41",
+          "score": -1.192523699,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5742,
+          "gene": "FTL",
+          "score": -0.939115266,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2801,
+          "gene": "CFAP45",
+          "score": -0.685511331,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14587,
+          "gene": "SLC7A3",
+          "score": -1.68097089,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1058,
+          "gene": "ARPC5L",
+          "score": -1.813787653,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14314,
+          "gene": "SLC22A13",
+          "score": -2.606926552,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 9853,
+          "gene": "MXRA7",
+          "score": -0.555642515,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10367,
+          "gene": "NME4",
+          "score": -1.391680682,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17857,
+          "gene": "ZFYVE19",
+          "score": -0.378750065,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17248,
+          "gene": "UTP11L",
+          "score": -0.186709721,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18393,
+          "gene": "ZNF860",
+          "score": -0.157582105,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4277,
+          "gene": "DNM2",
+          "score": -2.099300133,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 4688,
+          "gene": "ELMO2",
+          "score": -0.722450379,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3571,
+          "gene": "CSTL1",
+          "score": -1.588077652,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14997,
+          "gene": "SPERT",
+          "score": -0.858794701,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1096,
+          "gene": "ASB10",
+          "score": -1.354822467,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15785,
+          "gene": "TEKT5",
+          "score": -0.196528938,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15675,
+          "gene": "TBX2",
+          "score": -0.307810077,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4967,
+          "gene": "EXOG",
+          "score": -0.55416703,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11603,
+          "gene": "PHLDB3",
+          "score": -0.780692943,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7644,
+          "gene": "JAG1",
+          "score": -0.525434014,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8363,
+          "gene": "LCE1B",
+          "score": -0.35401784,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6321,
+          "gene": "GPR155",
+          "score": -0.646506215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16162,
+          "gene": "TMEM182",
+          "score": -0.469387502,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16361,
+          "gene": "TMX4",
+          "score": -0.225968331,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6960,
+          "gene": "HOMER3",
+          "score": -0.661488558,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13916,
+          "gene": "SEMA6A",
+          "score": -0.602172178,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8298,
+          "gene": "LACRT",
+          "score": -0.687435288,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10171,
+          "gene": "NECAB1",
+          "score": -0.603126514,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16424,
+          "gene": "TNNT2",
+          "score": -0.871145657,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7123,
+          "gene": "HTR1D",
+          "score": -0.939109947,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16680,
+          "gene": "TRMT10B",
+          "score": -1.130523021,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7928,
+          "gene": "KIAA1598",
+          "score": -0.40591144,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1116,
+          "gene": "ASCL1",
+          "score": -0.442493635,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11300,
+          "gene": "PCDHGA1",
+          "score": -1.106021124,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16858,
+          "gene": "TTLL4",
+          "score": -0.727006676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10094,
+          "gene": "NCOA7",
+          "score": -1.930474871,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7087,
+          "gene": "HSH2D",
+          "score": -0.801102116,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8673,
+          "gene": "LRCH3",
+          "score": -1.218507103,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3539,
+          "gene": "CSNK1G3",
+          "score": -1.660520671,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9872,
+          "gene": "MYCT1",
+          "score": -0.518249823,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6645,
+          "gene": "HBG2",
+          "score": -0.751676373,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10968,
+          "gene": "OR6Y1",
+          "score": -1.348577222,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12141,
+          "gene": "PPP1R16B",
+          "score": -1.546194645,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17504,
+          "gene": "WDR89",
+          "score": -0.644404655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6367,
+          "gene": "GPR82",
+          "score": -1.35659231,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3261,
+          "gene": "COL4A1",
+          "score": -0.542830084,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14035,
+          "gene": "SFI1",
+          "score": -0.499479583,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4398,
+          "gene": "DTD2",
+          "score": -1.08526838,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8711,
+          "gene": "LRRC14B",
+          "score": -0.343087942,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8380,
+          "gene": "LCK",
+          "score": -0.52052891,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4621,
+          "gene": "EIF2AK4",
+          "score": -0.204981202,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12364,
+          "gene": "PRPF6",
+          "score": -0.609118337,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12812,
+          "gene": "RAD51B",
+          "score": -0.789476994,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1454,
+          "gene": "BCL2L11",
+          "score": -1.676432541,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16655,
+          "gene": "TRIM67",
+          "score": -0.917894817,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14568,
+          "gene": "SLC6A16",
+          "score": -1.931530047,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3100,
+          "gene": "CLNK",
+          "score": -1.408963114,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6624,
+          "gene": "HAS1",
+          "score": -0.605557261,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13875,
+          "gene": "SEC24D",
+          "score": -0.437243173,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5672,
+          "gene": "FOXO3",
+          "score": -1.015406624,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15843,
+          "gene": "TFDP2",
+          "score": -0.267557884,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16261,
+          "gene": "TMEM41B",
+          "score": -0.416568026,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14341,
+          "gene": "SLC24A5",
+          "score": -1.016902515,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6574,
+          "gene": "GZMH",
+          "score": -0.524681967,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9422,
+          "gene": "MKL1",
+          "score": -0.991542854,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15448,
+          "gene": "SYNCRIP",
+          "score": -0.771070943,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12702,
+          "gene": "QSOX1",
+          "score": -0.049414434,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6691,
+          "gene": "HEATR1",
+          "score": -1.76546051,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1651,
+          "gene": "BTBD11",
+          "score": -1.259541465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17936,
+          "gene": "ZNF16",
+          "score": -0.934229552,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18442,
+          "gene": "ZSCAN30",
+          "score": -0.164749845,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18051,
+          "gene": "ZNF35",
+          "score": -0.336678778,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1575,
+          "gene": "BOD1L1",
+          "score": -0.083415498,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8665,
+          "gene": "LPPR3",
+          "score": -0.468513215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14049,
+          "gene": "SFTA2",
+          "score": -0.626802614,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12347,
+          "gene": "PROSER1",
+          "score": -0.380465795,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13801,
+          "gene": "SCNN1D",
+          "score": -0.473168344,
+          "hit": 0,
+          "round": 3
         }
       ],
       "queried_history": [
@@ -4920,896 +5816,1792 @@
           "gene": "LYPD3",
           "score": -1.35862469,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8590,
           "gene": "LOC100287477",
           "score": -0.714511497,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13526,
           "gene": "RQCD1",
           "score": -0.412618154,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15461,
           "gene": "SYNJ2",
           "score": -0.946737582,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15079,
           "gene": "SPTAN1",
           "score": -0.110600586,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4300,
           "gene": "DOCK8",
           "score": -0.331870644,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3348,
           "gene": "COX20",
           "score": -0.231494198,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4819,
           "gene": "EPM2A",
           "score": -1.13272984,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14390,
           "gene": "SLC26A1",
           "score": -0.340620639,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2932,
           "gene": "CHRNB3",
           "score": -2.974043214,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6360,
           "gene": "GPR62",
           "score": -1.52512221,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4181,
           "gene": "DMP1",
           "score": -0.542018268,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9080,
           "gene": "MARCHF6",
           "score": -0.353619146,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3607,
           "gene": "CTNNA3",
           "score": -0.711096746,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9811,
           "gene": "MTX1",
           "score": -0.673788849,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17651,
           "gene": "YIF1A",
           "score": -0.475032682,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5599,
           "gene": "FMO1",
           "score": -4.34614456,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17231,
           "gene": "USP47",
           "score": -0.218625057,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10787,
           "gene": "OPN1LW",
           "score": -1.070313023,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18234,
           "gene": "ZNF620",
           "score": -0.715613633,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 939,
           "gene": "ARHGAP26",
           "score": -0.375240063,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1503,
           "gene": "BFSP2",
           "score": -0.961354228,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14772,
           "gene": "SNCAIP",
           "score": -0.130516403,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13514,
           "gene": "RPS6KC1",
           "score": -0.628991819,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10099,
           "gene": "NCR3",
           "score": -1.33108691,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18257,
           "gene": "ZNF658",
           "score": -0.184765673,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15106,
           "gene": "SREK1",
           "score": -1.153381909,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11836,
           "gene": "PLEKHJ1",
           "score": -1.051687891,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 565,
           "gene": "ALG5",
           "score": -0.535264912,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3172,
           "gene": "CNN1",
           "score": -1.284906283,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9266,
           "gene": "MEP1A",
           "score": -0.646113304,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10611,
           "gene": "NUAK2",
           "score": -0.716196527,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17281,
           "gene": "VASH2",
           "score": -0.473840215,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7232,
           "gene": "IFNA4",
           "score": -0.366091012,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7692,
           "gene": "KAT2A",
           "score": -0.189584307,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11974,
           "gene": "POLQ",
           "score": -1.839250336,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2152,
           "gene": "CASP7",
           "score": -1.10957167,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16954,
           "gene": "TYW5",
           "score": -0.31017817,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1457,
           "gene": "BCL2L14",
           "score": -0.494356377,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16683,
           "gene": "TRMT112",
           "score": -0.82337045,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17966,
           "gene": "ZNF217",
           "score": -2.62607704,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17121,
           "gene": "UMPS",
           "score": -0.771155229,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13585,
           "gene": "RTKN2",
           "score": -0.651918167,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6059,
           "gene": "GIPC1",
           "score": -1.722157093,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8544,
           "gene": "LLPH",
           "score": -0.481776426,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17775,
           "gene": "ZCCHC18",
           "score": -0.984339194,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17455,
           "gene": "WDR26",
           "score": -1.416994653,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10872,
           "gene": "OR2Y1",
           "score": -0.90365762,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4401,
           "gene": "DTNA",
           "score": -0.881416777,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5654,
           "gene": "FOXG1",
           "score": -0.505383294,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16259,
           "gene": "TMEM40",
           "score": -1.262485406,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10182,
           "gene": "NEFH",
           "score": -0.738043137,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17584,
           "gene": "WWP1",
           "score": -0.164219297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4403,
           "gene": "DTNBP1",
           "score": -0.677369341,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9146,
           "gene": "MBTPS2",
           "score": -2.831200619,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16667,
           "gene": "TRIML2",
           "score": -0.937099889,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7394,
           "gene": "IL4I1",
           "score": -0.305075396,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4710,
           "gene": "EMC1",
           "score": -0.129501889,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9443,
           "gene": "MLLT11",
           "score": -0.600085993,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7697,
           "gene": "KAT7",
           "score": -0.301507101,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12703,
           "gene": "QSOX2",
           "score": -0.620933935,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17786,
           "gene": "ZCWPW1",
           "score": -0.762857292,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15943,
           "gene": "TICRR",
           "score": -1.141863426,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12288,
           "gene": "PRKAR1A",
           "score": -1.529192383,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3494,
           "gene": "CRYBB1",
           "score": -0.903576324,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12043,
           "gene": "POU2AF1",
           "score": -0.767488353,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9001,
           "gene": "MAP1LC3A",
           "score": -2.515142622,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 318,
           "gene": "ADGRB2",
           "score": -0.682196751,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 967,
           "gene": "ARHGEF17",
           "score": -1.996654631,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3870,
           "gene": "DCD",
           "score": -0.507601331,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 271,
           "gene": "ADAMTS2",
           "score": -0.903810552,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7435,
           "gene": "ING5",
           "score": -0.176333875,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3113,
           "gene": "CLRN2",
           "score": -0.191239295,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14846,
           "gene": "SOCS4",
           "score": -0.180146011,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12421,
           "gene": "PRSS12",
           "score": -0.331270376,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18,
           "gene": "AANAT",
           "score": -1.317191481,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 942,
           "gene": "ARHGAP29",
           "score": -0.982532766,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1147,
           "gene": "ASPSCR1",
           "score": -0.493709476,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11402,
           "gene": "PDE6H",
           "score": -1.195308373,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8847,
           "gene": "LY6D",
           "score": -0.778574612,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3803,
           "gene": "DAB2IP",
           "score": -1.011509084,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17381,
           "gene": "VRK3",
           "score": -0.694219654,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 198,
           "gene": "ACTB",
           "score": -0.093546774,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1040,
           "gene": "ARMCX2",
           "score": -0.217900514,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11162,
           "gene": "PANK3",
           "score": -0.76677056,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4145,
           "gene": "DKK4",
           "score": -0.379994765,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17754,
           "gene": "ZC3H13",
           "score": -0.77871719,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8044,
           "gene": "KLHL15",
           "score": -1.562471917,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2398,
           "gene": "CCNB2",
           "score": -1.725644291,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9481,
           "gene": "MMP28",
           "score": -0.608958085,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5348,
           "gene": "FBLN2",
           "score": -0.352870141,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13987,
           "gene": "SERPIND1",
           "score": -0.249057418,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 796,
           "gene": "AP2B1",
           "score": -0.439214772,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17933,
           "gene": "ZNF154",
           "score": -0.163350964,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5494,
           "gene": "FGF14",
           "score": -0.667065541,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3845,
           "gene": "DBT",
           "score": -0.528454256,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 305,
           "gene": "ADCY7",
           "score": -1.046469874,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4662,
           "gene": "EIF5A",
           "score": -0.563953435,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2760,
           "gene": "CEP41",
           "score": -0.516591895,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6961,
           "gene": "HOMEZ",
           "score": -0.956648528,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7906,
           "gene": "KIAA1161",
           "score": -0.790960097,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7924,
           "gene": "KIAA1549",
           "score": -0.537273716,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18116,
           "gene": "ZNF468",
           "score": -0.696135309,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 161,
           "gene": "ACOT8",
           "score": -0.645103279,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5378,
           "gene": "FBXO15",
           "score": -0.515742054,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2395,
           "gene": "CCNA2",
           "score": -0.271994632,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12759,
           "gene": "RAB3GAP2",
           "score": -0.355411507,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 451,
           "gene": "AHCYL1",
           "score": -0.091852957,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3523,
           "gene": "CSH1",
           "score": -0.582788947,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15716,
           "gene": "TCF21",
           "score": -0.630659951,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16333,
           "gene": "TMPRSS11B",
           "score": -0.902259812,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16484,
           "gene": "TP53I13",
           "score": -0.527069086,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1006,
           "gene": "ARL14EPL",
           "score": -0.841783023,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15382,
           "gene": "SUMO1",
           "score": -0.505812475,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3198,
           "gene": "CNST",
           "score": -1.221261734,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5553,
           "gene": "FJX1",
           "score": -1.668473818,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11268,
           "gene": "PCDH9",
           "score": -1.045287462,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10008,
           "gene": "NAMPT",
           "score": -0.501845016,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3322,
           "gene": "COQ2",
           "score": -1.062150642,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10317,
           "gene": "NKIRAS2",
           "score": -0.106123369,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14856,
           "gene": "SOHLH2",
           "score": -0.483619272,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8428,
           "gene": "LENG1",
           "score": -0.619251179,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4866,
           "gene": "ERH",
           "score": -0.595676674,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14634,
           "gene": "SLIT1",
           "score": -0.892832717,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14666,
           "gene": "SMAP2",
           "score": -2.863345223,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6122,
           "gene": "GLRA3",
           "score": -0.4349469,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6569,
           "gene": "GYS1",
           "score": -0.33920348,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5950,
           "gene": "GCLC",
           "score": -0.288138675,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 4504,
+          "gene": "ECD",
+          "score": -0.771727807,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15484,
+          "gene": "SYT3",
+          "score": -0.657671024,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13537,
+          "gene": "RRM1",
+          "score": -1.589108919,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1414,
+          "gene": "BAZ1B",
+          "score": -1.358205594,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1542,
+          "gene": "BLOC1S6",
+          "score": -0.709688832,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11800,
+          "gene": "PLCXD2",
+          "score": -0.82898389,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3466,
+          "gene": "CRISP3",
+          "score": -0.68294363,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9061,
+          "gene": "MAPK9",
+          "score": -0.107817483,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11707,
+          "gene": "PITPNB",
+          "score": -0.613558182,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2158,
+          "gene": "CASR",
+          "score": -0.603843115,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11353,
+          "gene": "PCSK2",
+          "score": -1.428592082,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8565,
+          "gene": "LMO7",
+          "score": -1.038774629,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1272,
+          "gene": "ATP6V1B2",
+          "score": -0.64175475,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7524,
+          "gene": "IRAK3",
+          "score": -0.55630682,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5724,
+          "gene": "FSCN1",
+          "score": -1.737922516,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9277,
+          "gene": "METAP1",
+          "score": -3.467403866,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 15979,
+          "gene": "TIPARP",
+          "score": -0.723071233,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4960,
+          "gene": "EXOC3L4",
+          "score": -0.279485651,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6335,
+          "gene": "GPR180",
+          "score": -0.205966576,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 969,
+          "gene": "ARHGEF19",
+          "score": -0.42081153,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2510,
+          "gene": "CD48",
+          "score": -1.462076556,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10085,
+          "gene": "NCL",
+          "score": -1.334924453,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15844,
+          "gene": "TFDP3",
+          "score": -1.668787689,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15213,
+          "gene": "ST6GALNAC6",
+          "score": -0.341726043,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18403,
+          "gene": "ZNF92",
+          "score": -1.976399656,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12149,
+          "gene": "PPP1R26",
+          "score": -0.317375955,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6725,
+          "gene": "HERC4",
+          "score": -0.617694233,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9174,
+          "gene": "MCM6",
+          "score": -0.621614572,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14991,
+          "gene": "SPECC1L",
+          "score": -0.199774547,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18246,
+          "gene": "ZNF639",
+          "score": -0.68097358,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4747,
+          "gene": "ENDOU",
+          "score": -0.543100757,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 828,
+          "gene": "APEX1",
+          "score": -0.803498906,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14167,
+          "gene": "SIDT1",
+          "score": -0.392442658,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15565,
+          "gene": "TAPBP",
+          "score": -1.087895224,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1639,
+          "gene": "BSDC1",
+          "score": -1.056781378,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13949,
+          "gene": "SERAC1",
+          "score": -0.730893618,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14976,
+          "gene": "SPC24",
+          "score": -0.28586155,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9010,
+          "gene": "MAP2K3",
+          "score": -0.138621146,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9529,
+          "gene": "MORN5",
+          "score": -1.288641038,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5225,
+          "gene": "FAM3A",
+          "score": -0.800316735,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8865,
+          "gene": "LYN",
+          "score": -0.363114043,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12441,
+          "gene": "PRSS54",
+          "score": -0.990354612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13645,
+          "gene": "S100A6",
+          "score": -1.689889747,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4217,
+          "gene": "DNAJA1",
+          "score": -0.006179969,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12574,
+          "gene": "PTGS1",
+          "score": -0.458220964,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15683,
+          "gene": "TBXA2R",
+          "score": -1.19988353,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9728,
+          "gene": "MSTN",
+          "score": -0.771792541,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18228,
+          "gene": "ZNF613",
+          "score": -0.559903684,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 693,
+          "gene": "ANKRD17",
+          "score": -0.492526171,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7428,
+          "gene": "INCA1",
+          "score": -0.547074506,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12966,
+          "gene": "RBM41",
+          "score": -1.192523699,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5742,
+          "gene": "FTL",
+          "score": -0.939115266,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2801,
+          "gene": "CFAP45",
+          "score": -0.685511331,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14587,
+          "gene": "SLC7A3",
+          "score": -1.68097089,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1058,
+          "gene": "ARPC5L",
+          "score": -1.813787653,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14314,
+          "gene": "SLC22A13",
+          "score": -2.606926552,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 9853,
+          "gene": "MXRA7",
+          "score": -0.555642515,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10367,
+          "gene": "NME4",
+          "score": -1.391680682,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17857,
+          "gene": "ZFYVE19",
+          "score": -0.378750065,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17248,
+          "gene": "UTP11L",
+          "score": -0.186709721,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18393,
+          "gene": "ZNF860",
+          "score": -0.157582105,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4277,
+          "gene": "DNM2",
+          "score": -2.099300133,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 4688,
+          "gene": "ELMO2",
+          "score": -0.722450379,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3571,
+          "gene": "CSTL1",
+          "score": -1.588077652,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14997,
+          "gene": "SPERT",
+          "score": -0.858794701,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1096,
+          "gene": "ASB10",
+          "score": -1.354822467,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15785,
+          "gene": "TEKT5",
+          "score": -0.196528938,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15675,
+          "gene": "TBX2",
+          "score": -0.307810077,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4967,
+          "gene": "EXOG",
+          "score": -0.55416703,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11603,
+          "gene": "PHLDB3",
+          "score": -0.780692943,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7644,
+          "gene": "JAG1",
+          "score": -0.525434014,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8363,
+          "gene": "LCE1B",
+          "score": -0.35401784,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6321,
+          "gene": "GPR155",
+          "score": -0.646506215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16162,
+          "gene": "TMEM182",
+          "score": -0.469387502,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16361,
+          "gene": "TMX4",
+          "score": -0.225968331,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6960,
+          "gene": "HOMER3",
+          "score": -0.661488558,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13916,
+          "gene": "SEMA6A",
+          "score": -0.602172178,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8298,
+          "gene": "LACRT",
+          "score": -0.687435288,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10171,
+          "gene": "NECAB1",
+          "score": -0.603126514,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16424,
+          "gene": "TNNT2",
+          "score": -0.871145657,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7123,
+          "gene": "HTR1D",
+          "score": -0.939109947,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16680,
+          "gene": "TRMT10B",
+          "score": -1.130523021,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7928,
+          "gene": "KIAA1598",
+          "score": -0.40591144,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1116,
+          "gene": "ASCL1",
+          "score": -0.442493635,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11300,
+          "gene": "PCDHGA1",
+          "score": -1.106021124,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16858,
+          "gene": "TTLL4",
+          "score": -0.727006676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10094,
+          "gene": "NCOA7",
+          "score": -1.930474871,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7087,
+          "gene": "HSH2D",
+          "score": -0.801102116,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8673,
+          "gene": "LRCH3",
+          "score": -1.218507103,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3539,
+          "gene": "CSNK1G3",
+          "score": -1.660520671,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9872,
+          "gene": "MYCT1",
+          "score": -0.518249823,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6645,
+          "gene": "HBG2",
+          "score": -0.751676373,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10968,
+          "gene": "OR6Y1",
+          "score": -1.348577222,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12141,
+          "gene": "PPP1R16B",
+          "score": -1.546194645,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17504,
+          "gene": "WDR89",
+          "score": -0.644404655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6367,
+          "gene": "GPR82",
+          "score": -1.35659231,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3261,
+          "gene": "COL4A1",
+          "score": -0.542830084,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14035,
+          "gene": "SFI1",
+          "score": -0.499479583,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4398,
+          "gene": "DTD2",
+          "score": -1.08526838,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8711,
+          "gene": "LRRC14B",
+          "score": -0.343087942,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8380,
+          "gene": "LCK",
+          "score": -0.52052891,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4621,
+          "gene": "EIF2AK4",
+          "score": -0.204981202,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12364,
+          "gene": "PRPF6",
+          "score": -0.609118337,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12812,
+          "gene": "RAD51B",
+          "score": -0.789476994,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1454,
+          "gene": "BCL2L11",
+          "score": -1.676432541,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16655,
+          "gene": "TRIM67",
+          "score": -0.917894817,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14568,
+          "gene": "SLC6A16",
+          "score": -1.931530047,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3100,
+          "gene": "CLNK",
+          "score": -1.408963114,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6624,
+          "gene": "HAS1",
+          "score": -0.605557261,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13875,
+          "gene": "SEC24D",
+          "score": -0.437243173,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5672,
+          "gene": "FOXO3",
+          "score": -1.015406624,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15843,
+          "gene": "TFDP2",
+          "score": -0.267557884,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16261,
+          "gene": "TMEM41B",
+          "score": -0.416568026,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14341,
+          "gene": "SLC24A5",
+          "score": -1.016902515,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6574,
+          "gene": "GZMH",
+          "score": -0.524681967,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9422,
+          "gene": "MKL1",
+          "score": -0.991542854,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15448,
+          "gene": "SYNCRIP",
+          "score": -0.771070943,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12702,
+          "gene": "QSOX1",
+          "score": -0.049414434,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6691,
+          "gene": "HEATR1",
+          "score": -1.76546051,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1651,
+          "gene": "BTBD11",
+          "score": -1.259541465,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17936,
+          "gene": "ZNF16",
+          "score": -0.934229552,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18442,
+          "gene": "ZSCAN30",
+          "score": -0.164749845,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18051,
+          "gene": "ZNF35",
+          "score": -0.336678778,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1575,
+          "gene": "BOD1L1",
+          "score": -0.083415498,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8665,
+          "gene": "LPPR3",
+          "score": -0.468513215,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14049,
+          "gene": "SFTA2",
+          "score": -0.626802614,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12347,
+          "gene": "PROSER1",
+          "score": -0.380465795,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13801,
+          "gene": "SCNN1D",
+          "score": -0.473168344,
+          "hit": 0,
+          "round": 3
         }
       ]
     }

```
