# Change Record — candidate_2

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IL2/run-1/best/current/harness
Generated at: 2026-04-30T06:41:38.791150

## Files Changed

- model.py: modified (added=17, deleted=7, delta=10)
- outputs/metrics.json: modified (added=2156, deleted=364, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -52,8 +52,9 @@
         idx = h['candidate_index']
         score = h.get('score', 0.0)
         hit = h.get('hit', 0)
-        # Combine score and hit with preference for hits
-        candidate_scores[idx] = score + (hit * 2.0)
+        # Heavily prioritize hits - they are the target metric
+        # Use a large weight for hits (10x max expected score) plus the actual score
+        candidate_scores[idx] = score + (hit * 10.0)
     
     # Sort candidates by score
     sorted_history = sorted(history, key=lambda h: candidate_scores.get(h['candidate_index'], 0), reverse=True)
@@ -79,8 +80,12 @@
         gene_search_available = False
     
     if gene_search_available:
-        # For top performers, find similar genes
-        for h in sorted_history[:max(1, len(sorted_history) // 10)]:
+        # Prioritize finding similar genes to HIT genes first
+        hit_genes = [h for h in sorted_history if h.get('hit', 0) == 1]
+        genes_to_search = hit_genes + sorted_history[:max(1, len(sorted_history) // 10)]
+        genes_seen = set()
+        
+        for h in genes_to_search:
             idx = h['candidate_index']
             candidate = candidates[idx]
             
@@ -92,11 +97,16 @@
             else:
                 continue
             
+            # Avoid searching for the same gene multiple times
+            if gene in genes_seen:
+                continue
+            genes_seen.add(gene)
+            
             # Search for similar genes
             try:
-                similar_indices = bda_tools.gene_search(gene, k=5, diverse=False)
-                # Filter to available indices only
-                similar_available = [i for i in similar_indices if i in available_indices and i not in selected]
+                similar_indices = bda_tools.gene_search(gene, k=10, diverse=False)
+                # Filter to available indices only (not yet selected)
+                similar_available = [i for i in similar_indices if i in available_indices and i not in exploit_pool and i not in selected]
                 exploit_pool.extend(similar_available)
             except:
                 pass

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18939,
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
+      "delta_hits": 6,
+      "total_queries": 256,
+      "total_hits": 8,
       "top_k": 654,
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
+          8
         ]
       },
-      "auc": 128.0,
-      "auc_normalized": 0.0015290519877675841,
-      "ncg": 0.10946446196271965,
+      "auc": 640.0,
+      "auc_normalized": 0.00382262996941896,
+      "ncg": 0.14829332160283393,
       "round_details": [
         {
-          "round": 0,
+          "round": 1,
           "selected_count": 128,
-          "hits": 2,
-          "cumulative_hits": 2,
-          "precision_at_batch": 0.015625,
+          "hits": 6,
+          "cumulative_hits": 8,
+          "precision_at_batch": 0.046875,
           "selected": [
-            "ILKAP",
-            "SLC7A3",
-            "C21orf59",
-            "EPM2A",
-            "CMBL",
-            "BCAP29",
-            "POLE2",
-            "ALYREF",
-            "SSBP3",
-            "USP35",
-            "ATP1A2",
-            "TIMM10B",
-            "PLA2G16",
-            "CENPBD1",
-            "CFHR4",
-            "DCTN5",
-            "KIAA0754",
-            "CELF3",
-            "SH3BP5",
-            "LMBR1L",
-            "ATP5G3",
-            "MOV10L1",
-            "HLA-DQA1",
-            "GPALPP1",
-            "CREBBP",
-            "TMEM53",
-            "APTX",
-            "IGSF22",
-            "NRG2",
-            "KRTAP22-2",
-            "SPO11",
-            "PQLC2L",
-            "SIMC1",
-            "CNTNAP3B",
-            "LRRC20",
-            "EPS8L3",
-            "LHX5",
-            "OR8H3",
-            "CEP68",
-            "CATSPER1",
-            "EIF4EBP3",
-            "ECM2",
-            "LOC284898",
-            "OR5M3",
-            "CEP78",
-            "NFKBIA",
-            "OVCA2",
-            "KREMEN2",
-            "MEMO1",
-            "RWDD2B",
-            "ZNF490",
-            "SH3BP2",
-            "YWHAZ",
-            "MRTO4",
-            "POU4F3",
-            "C6orf132",
-            "TMEM229B",
-            "ATP8A2",
-            "CTAGE6",
-            "LCN8",
-            "SRGAP2C",
-            "ACKR2",
-            "WNT3A",
-            "NOL12",
-            "FOXS1",
-            "DRD4",
-            "CNPPD1",
-            "MMP21",
-            "TXNDC8",
-            "MAGI2",
-            "SYNE1",
-            "SFTPA2",
-            "ZNF566",
-            "KRTAP19-5",
-            "NAGS",
-            "C20orf144",
-            "NIFK",
-            "TMEM268",
-            "GFM2",
-            "TNFSF11",
-            "LRIG2",
-            "RPLP0",
-            "SFRP4",
-            "HBEGF",
-            "THTPA",
-            "LRPPRC",
-            "ZNF740",
-            "WNT5A",
-            "NASP",
-            "GYS1",
-            "ZFYVE27",
-            "APC2",
-            "OR2J3",
-            "PARD3",
-            "MYLK",
-            "DPP7",
-            "CLEC16A",
-            "FA2H",
-            "PPFIA1",
-            "DEFB116",
-            "HLA-DQB1",
-            "FAM43B",
-            "SOX30",
-            "FOXO6",
-            "SLC25A34",
-            "ACIN1",
-            "DMKN",
-            "FYB",
-            "OR2F2",
-            "IFNA14",
-            "SPINK8",
-            "SLAMF8",
-            "TMEM260",
-            "NAGPA",
-            "VPS33A",
-            "RAB1B",
-            "LCE5A",
-            "BFAR",
-            "MFSD8",
-            "TIMM17B",
-            "TMBIM4",
-            "DCXR",
-            "SLC25A40",
-            "IER2",
-            "TRAK1",
-            "SUMO1",
-            "NAMPT",
-            "PTTG2"
+            "C18orf65",
+            "NUFIP2",
+            "MRPL45",
+            "MXRA7",
+            "TMEM41B",
+            "WDR54",
+            "TSPAN19",
+            "STAT5B",
+            "SLC15A1",
+            "HIST3H2BB",
+            "DLL1",
+            "HIGD1B",
+            "ETV1",
+            "SPTSSB",
+            "PODNL1",
+            "SERINC4",
+            "FUOM",
+            "C15orf39",
+            "ARSK",
+            "BCAN",
+            "ZNF623",
+            "DCAF8L1",
+            "CRELD1",
+            "TMSB4X",
+            "DTNA",
+            "UBR4",
+            "CTPS1",
+            "SUGCT",
+            "NLGN1",
+            "FRMPD4",
+            "NIM1K",
+            "HNRNPD",
+            "HK3",
+            "GOLGA2",
+            "LOC729159",
+            "FCER2",
+            "PKDCC",
+            "ZMYM3",
+            "CARMIL3",
+            "IARS2",
+            "C10orf82",
+            "HLA-DMA",
+            "ARSF",
+            "PCDHGA2",
+            "MRPL39",
+            "PPM1B",
+            "ZBTB7A",
+            "VTI1B",
+            "FAM124A",
+            "TMEM86B",
+            "PABPC5",
+            "IFNL2",
+            "HOXB7",
+            "APP",
+            "CERS5",
+            "TSC2",
+            "PCDHB16",
+            "CHD2",
+            "SLC35G1",
+            "SLC19A3",
+            "TRIM49",
+            "SART3",
+            "RNF217",
+            "EFCAB1",
+            "MRPL20",
+            "CUL4A",
+            "TBCD",
+            "C9",
+            "IZUMO3",
+            "C10orf111",
+            "SLC5A1",
+            "C1orf115",
+            "CCDC175",
+            "UQCR10",
+            "CLDN16",
+            "CDK16",
+            "ASCL2",
+            "PTRH2",
+            "CFAP47",
+            "SIN3B",
+            "GIF",
+            "SDS",
+            "LGR4",
+            "GABARAPL1",
+            "CCDC142",
+            "SLC5A10",
+            "KLHL38",
+            "POU3F3",
+            "NSL1",
+            "NHLRC4",
+            "EBF2",
+            "XYLT1",
+            "CCL23",
+            "SP3",
+            "OR2AK2",
+            "ACE2",
+            "GABRD",
+            "RALGAPA2",
+            "KARS",
+            "DNAJC24",
+            "USMG5",
+            "PRSS42",
+            "DSCC1",
+            "HARS2",
+            "METTL18",
+            "IL37",
+            "C1orf131",
+            "OR5H14",
+            "GPR171",
+            "ZFP36",
+            "RBM11",
+            "AIP",
+            "BICC1",
+            "NET1",
+            "EXOSC10",
+            "SLC25A53",
+            "NRBP1",
+            "KLF15",
+            "KRT72",
+            "MYOM2",
+            "FBXO44",
+            "RASGRP4",
+            "NR1H4",
+            "HIPK3",
+            "FBRSL1",
+            "SSX5",
+            "NISCH",
+            "AGAP9"
           ],
           "selected_scores": [
-            0.01106,
-            -0.10663,
-            0.046914,
-            -0.054053,
-            0.052273,
-            0.051055,
-            0.093466,
-            0.19903,
-            -0.23246,
-            0.03355,
-            -0.2031,
-            -0.28268,
-            -0.21437,
-            0.059897,
-            -0.096415,
-            0.50045,
-            -0.17078,
-            0.076988,
-            0.17998,
-            0.072043,
-            -0.071837,
-            -0.056153,
-            0.062367,
-            0.15528,
-            -0.25859,
-            -0.098286,
-            0.052481,
-            -0.097452,
-            0.12534,
-            -0.024004,
-            0.12787,
-            -0.04925,
-            -0.064746,
-            -0.03737,
-            0.082693,
-            0.050768,
-            0.17887,
-            0.034619,
-            -0.13196,
-            -0.18712,
-            0.14182,
-            0.13478,
-            0.0091898,
-            -0.057844,
-            0.12283,
-            0.14574,
-            0.21121,
-            -0.08067,
-            0.73471,
-            0.093253,
-            -0.15993,
-            -0.11788,
-            -0.052884,
-            -0.057524,
-            -0.033234,
-            -0.017814,
-            -0.11726,
-            0.15144,
-            -0.04022,
-            -0.084012,
-            0.01427,
-            -0.093882,
-            0.19544,
-            -0.062201,
-            -0.087002,
-            0.017744,
-            -0.12037,
-            -0.046955,
-            -0.018096,
-            0.10336,
-            -0.12223,
-            0.064198,
-            0.12948,
-            0.073363,
-            -0.049917,
-            0.16321,
-            0.26479,
-            0.0085949,
-            -0.0091051,
-            -0.25904,
-            -0.024438,
-            0.25585,
-            0.057375,
-            0.14176,
-            -0.051704,
-            0.17284,
-            0.058713,
-            0.03889,
-            0.2853,
-            0.054807,
-            0.14991,
-            -0.0010187,
-            -0.055757,
-            0.061334,
-            0.046966,
-            0.14819,
-            0.23957,
-            0.032426,
-            0.011903,
-            0.056855,
-            0.083377,
-            0.070334,
-            -0.034098,
-            0.15798,
-            -0.043333,
-            -0.1498,
-            -0.089161,
-            -0.11311,
-            -0.035877,
-            0.055208,
-            -0.043273,
-            -0.19809,
-            0.015501,
-            -0.069095,
-            0.084537,
-            0.34005,
-            0.014338,
-            0.15287,
-            -0.15928,
-            0.010223,
-            0.092215,
-            0.281,
-            0.068711,
-            -0.081251,
-            0.017949,
-            0.027002,
-            -0.11147,
-            -0.0016693
+            -0.15548,
+            -0.13605,
+            -0.036223,
+            0.10713,
+            0.085085,
+            -0.10631,
+            0.10151,
+            0.66825,
+            -0.33204,
+            0.11889,
+            0.042788,
+            -0.058602,
+            0.091516,
+            0.038805,
+            0.014045,
+            -0.12633,
+            0.015142,
+            -0.13525,
+            -0.098201,
+            0.15259,
+            -0.0068339,
+            -0.011761,
+            -0.13571,
+            0.13174,
+            0.17313,
+            -0.13676,
+            0.75435,
+            0.1954,
+            0.053172,
+            -0.055871,
+            0.18883,
+            -0.24775,
+            -0.1471,
+            -0.11265,
+            0.015227,
+            -0.07774,
+            -0.059766,
+            -0.1353,
+            -0.009723,
+            -0.053533,
+            0.17092,
+            -0.10256,
+            -0.23222,
+            -0.03869,
+            0.33297,
+            0.19186,
+            -0.0031567,
+            -0.036043,
+            0.042661,
+            -0.16725,
+            -0.12012,
+            -0.15254,
+            0.086387,
+            -0.11897,
+            -0.0074335,
+            0.37433,
+            -0.21398,
+            -0.042776,
+            0.10571,
+            -0.081111,
+            0.16044,
+            0.26696,
+            -0.033267,
+            -0.023499,
+            -0.19691,
+            -0.012886,
+            0.19745,
+            -0.07877,
+            -0.10881,
+            -0.029118,
+            -0.1587,
+            -0.11322,
+            0.10326,
+            0.076353,
+            -0.078631,
+            0.13724,
+            -0.0808,
+            -0.20475,
+            0.039072,
+            -0.41614,
+            0.074703,
+            -0.092917,
+            -0.05853,
+            -0.23303,
+            -0.11455,
+            -0.080302,
+            -0.0014004,
+            0.18901,
+            0.16991,
+            0.004058,
+            -0.13201,
+            0.27896,
+            -0.11632,
+            -0.17675,
+            -0.16243,
+            -0.090405,
+            0.064745,
+            -0.12151,
+            0.11366,
+            0.092131,
+            -0.023547,
+            0.057466,
+            0.015806,
+            0.15363,
+            -0.11573,
+            -0.13746,
+            0.12026,
+            -0.037378,
+            -0.041124,
+            -0.017196,
+            0.1164,
+            -0.021423,
+            0.024422,
+            -0.091153,
+            0.075299,
+            -0.043129,
+            0.36928,
+            0.21171,
+            0.033732,
+            0.048418,
+            0.16553,
+            0.039352,
+            0.089194,
+            0.04917,
+            -0.20488,
+            -0.2542,
+            0.095073,
+            -0.13724
           ],
           "selected_hits": [
             0,
@@ -308,47 +308,7 @@
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
             1,
             0,
             0,
@@ -367,57 +327,97 @@
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
+            1,
             0,
             0,
             0,
@@ -1328,6 +1328,902 @@
           "score": -0.0016693,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 1270,
+          "gene": "C18orf65",
+          "score": -0.15548,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9446,
+          "gene": "NUFIP2",
+          "score": -0.13605,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4750,
+          "gene": "MRPL45",
+          "score": -0.036223,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15265,
+          "gene": "MXRA7",
+          "score": 0.10713,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12208,
+          "gene": "TMEM41B",
+          "score": 0.085085,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3177,
+          "gene": "WDR54",
+          "score": -0.10631,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14956,
+          "gene": "TSPAN19",
+          "score": 0.10151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16439,
+          "gene": "STAT5B",
+          "score": 0.66825,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 629,
+          "gene": "SLC15A1",
+          "score": -0.33204,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 16959,
+          "gene": "HIST3H2BB",
+          "score": 0.11889,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14271,
+          "gene": "DLL1",
+          "score": 0.042788,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12289,
+          "gene": "HIGD1B",
+          "score": -0.058602,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18044,
+          "gene": "ETV1",
+          "score": 0.091516,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14326,
+          "gene": "SPTSSB",
+          "score": 0.038805,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13003,
+          "gene": "PODNL1",
+          "score": 0.014045,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5815,
+          "gene": "SERINC4",
+          "score": -0.12633,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1902,
+          "gene": "FUOM",
+          "score": 0.015142,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3541,
+          "gene": "C15orf39",
+          "score": -0.13525,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4111,
+          "gene": "ARSK",
+          "score": -0.098201,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12405,
+          "gene": "BCAN",
+          "score": 0.15259,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5063,
+          "gene": "ZNF623",
+          "score": -0.0068339,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3158,
+          "gene": "DCAF8L1",
+          "score": -0.011761,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5302,
+          "gene": "CRELD1",
+          "score": -0.13571,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16905,
+          "gene": "TMSB4X",
+          "score": 0.13174,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16364,
+          "gene": "DTNA",
+          "score": 0.17313,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4247,
+          "gene": "UBR4",
+          "score": -0.13676,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12770,
+          "gene": "CTPS1",
+          "score": 0.75435,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 16716,
+          "gene": "SUGCT",
+          "score": 0.1954,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8978,
+          "gene": "NLGN1",
+          "score": 0.053172,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6000,
+          "gene": "FRMPD4",
+          "score": -0.055871,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12441,
+          "gene": "NIM1K",
+          "score": 0.18883,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2093,
+          "gene": "HNRNPD",
+          "score": -0.24775,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1613,
+          "gene": "HK3",
+          "score": -0.1471,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2016,
+          "gene": "GOLGA2",
+          "score": -0.11265,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6157,
+          "gene": "LOC729159",
+          "score": 0.015227,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2023,
+          "gene": "FCER2",
+          "score": -0.07774,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5471,
+          "gene": "PKDCC",
+          "score": -0.059766,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9779,
+          "gene": "ZMYM3",
+          "score": -0.1353,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9089,
+          "gene": "CARMIL3",
+          "score": -0.009723,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2546,
+          "gene": "IARS2",
+          "score": -0.053533,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17265,
+          "gene": "C10orf82",
+          "score": 0.17092,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3410,
+          "gene": "HLA-DMA",
+          "score": -0.10256,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2015,
+          "gene": "ARSF",
+          "score": -0.23222,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3111,
+          "gene": "PCDHGA2",
+          "score": -0.03869,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15128,
+          "gene": "MRPL39",
+          "score": 0.33297,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10956,
+          "gene": "PPM1B",
+          "score": 0.19186,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10920,
+          "gene": "ZBTB7A",
+          "score": -0.0031567,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17483,
+          "gene": "VTI1B",
+          "score": -0.036043,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14512,
+          "gene": "FAM124A",
+          "score": 0.042661,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5523,
+          "gene": "TMEM86B",
+          "score": -0.16725,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4180,
+          "gene": "PABPC5",
+          "score": -0.12012,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2650,
+          "gene": "IFNL2",
+          "score": -0.15254,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10570,
+          "gene": "HOXB7",
+          "score": 0.086387,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1654,
+          "gene": "APP",
+          "score": -0.11897,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8872,
+          "gene": "CERS5",
+          "score": -0.0074335,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12171,
+          "gene": "TSC2",
+          "score": 0.37433,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 6155,
+          "gene": "PCDHB16",
+          "score": -0.21398,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2326,
+          "gene": "CHD2",
+          "score": -0.042776,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18248,
+          "gene": "SLC35G1",
+          "score": 0.10571,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3750,
+          "gene": "SLC19A3",
+          "score": -0.081111,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9830,
+          "gene": "TRIM49",
+          "score": 0.16044,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16362,
+          "gene": "SART3",
+          "score": 0.26696,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11957,
+          "gene": "RNF217",
+          "score": -0.033267,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14355,
+          "gene": "EFCAB1",
+          "score": -0.023499,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1363,
+          "gene": "MRPL20",
+          "score": -0.19691,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15644,
+          "gene": "CUL4A",
+          "score": -0.012886,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13722,
+          "gene": "TBCD",
+          "score": 0.19745,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2764,
+          "gene": "C9",
+          "score": -0.07877,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11841,
+          "gene": "IZUMO3",
+          "score": -0.10881,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4207,
+          "gene": "C10orf111",
+          "score": -0.029118,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2850,
+          "gene": "SLC5A1",
+          "score": -0.1587,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5099,
+          "gene": "C1orf115",
+          "score": -0.11322,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10174,
+          "gene": "CCDC175",
+          "score": 0.10326,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3605,
+          "gene": "UQCR10",
+          "score": 0.076353,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17694,
+          "gene": "CLDN16",
+          "score": -0.078631,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14049,
+          "gene": "CDK16",
+          "score": 0.13724,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14652,
+          "gene": "ASCL2",
+          "score": -0.0808,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1252,
+          "gene": "PTRH2",
+          "score": -0.20475,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4849,
+          "gene": "CFAP47",
+          "score": 0.039072,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 82,
+          "gene": "SIN3B",
+          "score": -0.41614,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3499,
+          "gene": "GIF",
+          "score": 0.074703,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4114,
+          "gene": "SDS",
+          "score": -0.092917,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4170,
+          "gene": "LGR4",
+          "score": -0.05853,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 560,
+          "gene": "GABARAPL1",
+          "score": -0.23303,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11167,
+          "gene": "CCDC142",
+          "score": -0.11455,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3923,
+          "gene": "SLC5A10",
+          "score": -0.080302,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17599,
+          "gene": "KLHL38",
+          "score": -0.0014004,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16469,
+          "gene": "POU3F3",
+          "score": 0.18901,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8566,
+          "gene": "NSL1",
+          "score": 0.16991,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15089,
+          "gene": "NHLRC4",
+          "score": 0.004058,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11245,
+          "gene": "EBF2",
+          "score": -0.13201,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12756,
+          "gene": "XYLT1",
+          "score": 0.27896,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2880,
+          "gene": "CCL23",
+          "score": -0.11632,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1102,
+          "gene": "SP3",
+          "score": -0.17675,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3073,
+          "gene": "OR2AK2",
+          "score": -0.16243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6816,
+          "gene": "ACE2",
+          "score": -0.090405,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13385,
+          "gene": "GABRD",
+          "score": 0.064745,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6418,
+          "gene": "RALGAPA2",
+          "score": -0.12151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13346,
+          "gene": "KARS",
+          "score": 0.11366,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8611,
+          "gene": "DNAJC24",
+          "score": 0.092131,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13518,
+          "gene": "USMG5",
+          "score": -0.023547,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10827,
+          "gene": "PRSS42",
+          "score": 0.057466,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13164,
+          "gene": "DSCC1",
+          "score": 0.015806,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11475,
+          "gene": "HARS2",
+          "score": 0.15363,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1711,
+          "gene": "METTL18",
+          "score": -0.11573,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6148,
+          "gene": "IL37",
+          "score": -0.13746,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17772,
+          "gene": "C1orf131",
+          "score": 0.12026,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5886,
+          "gene": "OR5H14",
+          "score": -0.037378,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6213,
+          "gene": "GPR171",
+          "score": -0.041124,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1687,
+          "gene": "ZFP36",
+          "score": -0.017196,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7724,
+          "gene": "RBM11",
+          "score": 0.1164,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9925,
+          "gene": "AIP",
+          "score": -0.021423,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7344,
+          "gene": "BICC1",
+          "score": 0.024422,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11423,
+          "gene": "NET1",
+          "score": -0.091153,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6214,
+          "gene": "EXOSC10",
+          "score": 0.075299,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7162,
+          "gene": "SLC25A53",
+          "score": -0.043129,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12696,
+          "gene": "NRBP1",
+          "score": 0.36928,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 12873,
+          "gene": "KLF15",
+          "score": 0.21171,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7440,
+          "gene": "KRT72",
+          "score": 0.033732,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2003,
+          "gene": "MYOM2",
+          "score": 0.048418,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15159,
+          "gene": "FBXO44",
+          "score": 0.16553,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16578,
+          "gene": "RASGRP4",
+          "score": 0.039352,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2022,
+          "gene": "NR1H4",
+          "score": 0.089194,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3175,
+          "gene": "HIPK3",
+          "score": 0.04917,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 896,
+          "gene": "FBRSL1",
+          "score": -0.20488,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 781,
+          "gene": "SSX5",
+          "score": -0.2542,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18045,
+          "gene": "NISCH",
+          "score": 0.095073,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16889,
+          "gene": "AGAP9",
+          "score": -0.13724,
+          "hit": 0,
+          "round": 1
         }
       ],
       "queried_history": [
@@ -2226,6 +3122,902 @@
           "score": -0.0016693,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 1270,
+          "gene": "C18orf65",
+          "score": -0.15548,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9446,
+          "gene": "NUFIP2",
+          "score": -0.13605,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4750,
+          "gene": "MRPL45",
+          "score": -0.036223,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15265,
+          "gene": "MXRA7",
+          "score": 0.10713,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12208,
+          "gene": "TMEM41B",
+          "score": 0.085085,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3177,
+          "gene": "WDR54",
+          "score": -0.10631,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14956,
+          "gene": "TSPAN19",
+          "score": 0.10151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16439,
+          "gene": "STAT5B",
+          "score": 0.66825,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 629,
+          "gene": "SLC15A1",
+          "score": -0.33204,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 16959,
+          "gene": "HIST3H2BB",
+          "score": 0.11889,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14271,
+          "gene": "DLL1",
+          "score": 0.042788,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12289,
+          "gene": "HIGD1B",
+          "score": -0.058602,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18044,
+          "gene": "ETV1",
+          "score": 0.091516,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14326,
+          "gene": "SPTSSB",
+          "score": 0.038805,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13003,
+          "gene": "PODNL1",
+          "score": 0.014045,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5815,
+          "gene": "SERINC4",
+          "score": -0.12633,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1902,
+          "gene": "FUOM",
+          "score": 0.015142,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3541,
+          "gene": "C15orf39",
+          "score": -0.13525,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4111,
+          "gene": "ARSK",
+          "score": -0.098201,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12405,
+          "gene": "BCAN",
+          "score": 0.15259,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5063,
+          "gene": "ZNF623",
+          "score": -0.0068339,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3158,
+          "gene": "DCAF8L1",
+          "score": -0.011761,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5302,
+          "gene": "CRELD1",
+          "score": -0.13571,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16905,
+          "gene": "TMSB4X",
+          "score": 0.13174,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16364,
+          "gene": "DTNA",
+          "score": 0.17313,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4247,
+          "gene": "UBR4",
+          "score": -0.13676,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12770,
+          "gene": "CTPS1",
+          "score": 0.75435,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 16716,
+          "gene": "SUGCT",
+          "score": 0.1954,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8978,
+          "gene": "NLGN1",
+          "score": 0.053172,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6000,
+          "gene": "FRMPD4",
+          "score": -0.055871,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12441,
+          "gene": "NIM1K",
+          "score": 0.18883,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2093,
+          "gene": "HNRNPD",
+          "score": -0.24775,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1613,
+          "gene": "HK3",
+          "score": -0.1471,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2016,
+          "gene": "GOLGA2",
+          "score": -0.11265,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6157,
+          "gene": "LOC729159",
+          "score": 0.015227,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2023,
+          "gene": "FCER2",
+          "score": -0.07774,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5471,
+          "gene": "PKDCC",
+          "score": -0.059766,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9779,
+          "gene": "ZMYM3",
+          "score": -0.1353,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9089,
+          "gene": "CARMIL3",
+          "score": -0.009723,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2546,
+          "gene": "IARS2",
+          "score": -0.053533,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17265,
+          "gene": "C10orf82",
+          "score": 0.17092,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3410,
+          "gene": "HLA-DMA",
+          "score": -0.10256,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2015,
+          "gene": "ARSF",
+          "score": -0.23222,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3111,
+          "gene": "PCDHGA2",
+          "score": -0.03869,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15128,
+          "gene": "MRPL39",
+          "score": 0.33297,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10956,
+          "gene": "PPM1B",
+          "score": 0.19186,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10920,
+          "gene": "ZBTB7A",
+          "score": -0.0031567,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17483,
+          "gene": "VTI1B",
+          "score": -0.036043,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14512,
+          "gene": "FAM124A",
+          "score": 0.042661,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5523,
+          "gene": "TMEM86B",
+          "score": -0.16725,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4180,
+          "gene": "PABPC5",
+          "score": -0.12012,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2650,
+          "gene": "IFNL2",
+          "score": -0.15254,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10570,
+          "gene": "HOXB7",
+          "score": 0.086387,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1654,
+          "gene": "APP",
+          "score": -0.11897,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8872,
+          "gene": "CERS5",
+          "score": -0.0074335,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12171,
+          "gene": "TSC2",
+          "score": 0.37433,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 6155,
+          "gene": "PCDHB16",
+          "score": -0.21398,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2326,
+          "gene": "CHD2",
+          "score": -0.042776,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18248,
+          "gene": "SLC35G1",
+          "score": 0.10571,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3750,
+          "gene": "SLC19A3",
+          "score": -0.081111,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9830,
+          "gene": "TRIM49",
+          "score": 0.16044,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16362,
+          "gene": "SART3",
+          "score": 0.26696,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11957,
+          "gene": "RNF217",
+          "score": -0.033267,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14355,
+          "gene": "EFCAB1",
+          "score": -0.023499,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1363,
+          "gene": "MRPL20",
+          "score": -0.19691,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15644,
+          "gene": "CUL4A",
+          "score": -0.012886,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13722,
+          "gene": "TBCD",
+          "score": 0.19745,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2764,
+          "gene": "C9",
+          "score": -0.07877,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11841,
+          "gene": "IZUMO3",
+          "score": -0.10881,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4207,
+          "gene": "C10orf111",
+          "score": -0.029118,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2850,
+          "gene": "SLC5A1",
+          "score": -0.1587,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5099,
+          "gene": "C1orf115",
+          "score": -0.11322,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10174,
+          "gene": "CCDC175",
+          "score": 0.10326,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3605,
+          "gene": "UQCR10",
+          "score": 0.076353,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17694,
+          "gene": "CLDN16",
+          "score": -0.078631,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14049,
+          "gene": "CDK16",
+          "score": 0.13724,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14652,
+          "gene": "ASCL2",
+          "score": -0.0808,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1252,
+          "gene": "PTRH2",
+          "score": -0.20475,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4849,
+          "gene": "CFAP47",
+          "score": 0.039072,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 82,
+          "gene": "SIN3B",
+          "score": -0.41614,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3499,
+          "gene": "GIF",
+          "score": 0.074703,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4114,
+          "gene": "SDS",
+          "score": -0.092917,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4170,
+          "gene": "LGR4",
+          "score": -0.05853,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 560,
+          "gene": "GABARAPL1",
+          "score": -0.23303,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11167,
+          "gene": "CCDC142",
+          "score": -0.11455,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3923,
+          "gene": "SLC5A10",
+          "score": -0.080302,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17599,
+          "gene": "KLHL38",
+          "score": -0.0014004,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16469,
+          "gene": "POU3F3",
+          "score": 0.18901,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8566,
+          "gene": "NSL1",
+          "score": 0.16991,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15089,
+          "gene": "NHLRC4",
+          "score": 0.004058,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11245,
+          "gene": "EBF2",
+          "score": -0.13201,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12756,
+          "gene": "XYLT1",
+          "score": 0.27896,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2880,
+          "gene": "CCL23",
+          "score": -0.11632,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1102,
+          "gene": "SP3",
+          "score": -0.17675,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3073,
+          "gene": "OR2AK2",
+          "score": -0.16243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6816,
+          "gene": "ACE2",
+          "score": -0.090405,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13385,
+          "gene": "GABRD",
+          "score": 0.064745,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6418,
+          "gene": "RALGAPA2",
+          "score": -0.12151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13346,
+          "gene": "KARS",
+          "score": 0.11366,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8611,
+          "gene": "DNAJC24",
+          "score": 0.092131,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13518,
+          "gene": "USMG5",
+          "score": -0.023547,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10827,
+          "gene": "PRSS42",
+          "score": 0.057466,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13164,
+          "gene": "DSCC1",
+          "score": 0.015806,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11475,
+          "gene": "HARS2",
+          "score": 0.15363,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1711,
+          "gene": "METTL18",
+          "score": -0.11573,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6148,
+          "gene": "IL37",
+          "score": -0.13746,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17772,
+          "gene": "C1orf131",
+          "score": 0.12026,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5886,
+          "gene": "OR5H14",
+          "score": -0.037378,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6213,
+          "gene": "GPR171",
+          "score": -0.041124,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1687,
+          "gene": "ZFP36",
+          "score": -0.017196,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7724,
+          "gene": "RBM11",
+          "score": 0.1164,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9925,
+          "gene": "AIP",
+          "score": -0.021423,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7344,
+          "gene": "BICC1",
+          "score": 0.024422,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11423,
+          "gene": "NET1",
+          "score": -0.091153,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6214,
+          "gene": "EXOSC10",
+          "score": 0.075299,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7162,
+          "gene": "SLC25A53",
+          "score": -0.043129,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12696,
+          "gene": "NRBP1",
+          "score": 0.36928,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 12873,
+          "gene": "KLF15",
+          "score": 0.21171,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7440,
+          "gene": "KRT72",
+          "score": 0.033732,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2003,
+          "gene": "MYOM2",
+          "score": 0.048418,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15159,
+          "gene": "FBXO44",
+          "score": 0.16553,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16578,
+          "gene": "RASGRP4",
+          "score": 0.039352,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2022,
+          "gene": "NR1H4",
+          "score": 0.089194,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3175,
+          "gene": "HIPK3",
+          "score": 0.04917,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 896,
+          "gene": "FBRSL1",
+          "score": -0.20488,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 781,
+          "gene": "SSX5",
+          "score": -0.2542,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18045,
+          "gene": "NISCH",
+          "score": 0.095073,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16889,
+          "gene": "AGAP9",
+          "score": -0.13724,
+          "hit": 0,
+          "round": 1
         }
       ]
     }

```
