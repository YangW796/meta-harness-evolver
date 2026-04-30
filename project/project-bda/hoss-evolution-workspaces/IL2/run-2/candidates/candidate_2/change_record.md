# Change Record — candidate_2

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IL2/run-2/best/current/harness
Generated at: 2026-04-30T07:04:42.762028

## Files Changed

- model.py: modified (added=17, deleted=4, delta=13)
- outputs/metrics.json: modified (added=2161, deleted=369, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -30,6 +30,7 @@
     Strategy:
     - Thompson Sampling with Beta-Bernoulli model for hit probability
     - Uses gene search to expand candidate pool for similar genes
+    - Incorporates continuous score information for better prioritization
     - Naturally balances exploration vs exploitation through posterior sampling
     """
     rng = random.Random(seed)
@@ -48,8 +49,8 @@
         return selected
     
     # Build gene performance statistics
-    # Track hits and trials per gene
-    gene_stats = {}  # gene_name -> {'hits': int, 'trials': int}
+    # Track hits, trials, and score statistics per gene
+    gene_stats = {}  # gene_name -> {'hits': int, 'trials': int, 'sum_score': float, 'max_score': float}
     
     for h in history:
         idx = h['candidate_index']
@@ -64,9 +65,12 @@
             continue
         
         if gene not in gene_stats:
-            gene_stats[gene] = {'hits': 0, 'trials': 0}
+            gene_stats[gene] = {'hits': 0, 'trials': 0, 'sum_score': 0.0, 'max_score': -float('inf')}
         
         gene_stats[gene]['trials'] += 1
+        score = h.get('score', 0.0)
+        gene_stats[gene]['sum_score'] += score
+        gene_stats[gene]['max_score'] = max(gene_stats[gene]['max_score'], score)
         if h.get('hit', 0) == 1:
             gene_stats[gene]['hits'] += 1
     
@@ -80,7 +84,16 @@
         trials = stats['trials']
         # Sample from Beta posterior
         sampled_prob = np.random.beta(1 + hits, 1 + trials - hits)
-        gene_sampled_probs[gene] = sampled_prob
+        
+        # Boost probability for genes with high scores (even if not hits)
+        # This helps prioritize genes that showed promising scores
+        avg_score = stats['sum_score'] / trials
+        if avg_score > 0.1:  # Boost genes with positive average scores
+            sampled_prob *= (1.0 + avg_score)
+        elif avg_score < -0.1:  # Penalize genes with negative average scores
+            sampled_prob *= (1.0 + avg_score)  # This reduces the probability
+        
+        gene_sampled_probs[gene] = min(sampled_prob, 1.0)  # Cap at 1.0
     
     # Create candidate pool with Thompson Sampling scores
     candidate_pool = []

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
+      "delta_hits": 8,
+      "total_queries": 256,
+      "total_hits": 10,
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
+          10
         ]
       },
-      "auc": 128.0,
-      "auc_normalized": 0.0015290519877675841,
-      "ncg": 0.10946446196271965,
+      "auc": 768.0,
+      "auc_normalized": 0.0045871559633027525,
+      "ncg": 0.15166213156940128,
       "round_details": [
         {
-          "round": 0,
+          "round": 1,
           "selected_count": 128,
-          "hits": 2,
-          "cumulative_hits": 2,
-          "precision_at_batch": 0.015625,
+          "hits": 8,
+          "cumulative_hits": 10,
+          "precision_at_batch": 0.0625,
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
+            "HOXC4",
+            "NOTUM",
+            "NANS",
+            "KLRC1",
+            "ZNF430",
+            "RMND5A",
+            "DUSP28",
+            "EXO5",
+            "POLR1A",
+            "C17orf53",
+            "IFITM3",
+            "MARCH8",
+            "PREX1",
+            "TMEM191B",
+            "ELK1",
+            "S100A2",
+            "OR10J1",
+            "GCNT1",
+            "CHDH",
+            "RAB25",
+            "ZNF341",
+            "UBL4A",
+            "DRD1",
+            "PTMS",
+            "OTOP1",
+            "FAM133B",
+            "INS",
+            "GLB1L",
+            "DENND5A",
+            "LINGO4",
+            "DDX3Y",
+            "PPP1R17",
+            "C21orf140",
+            "DPRX",
+            "KDM6B",
+            "HESX1",
+            "OR2A5",
+            "RHOQ",
+            "ANAPC16",
+            "DHRS12",
+            "SIN3B",
+            "HNRNPCL1",
+            "CCL8",
+            "IFI27",
+            "GABARAPL1",
+            "LOC101927572",
+            "NSA2",
+            "TRIM71",
+            "PRPF4B",
+            "PTPRB",
+            "OR2Y1",
+            "PFKFB4",
+            "OR2T4",
+            "EPS8L2",
+            "ZNF491",
+            "CDRT4",
+            "USP17L18",
+            "CDC40",
+            "TRIM4",
+            "SEC23B",
+            "TCTEX1D4",
+            "OR52H1",
+            "ARL14EP",
+            "PRIM1",
+            "TK2",
+            "ANKH",
+            "ADAMTS19",
+            "YAF2",
+            "FGFR3",
+            "NEK9",
+            "COLEC10",
+            "FADS3",
+            "C1orf53",
+            "OGN",
+            "CSNK1E",
+            "OR2M7",
+            "CHST10",
+            "CDC42EP2",
+            "SRSF11",
+            "C20orf24",
+            "AWAT1",
+            "TJP1",
+            "CHMP6",
+            "GCM1",
+            "BPIFB2",
+            "TMED7",
+            "PROKR1",
+            "PRMT8",
+            "C9orf62"
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
+            -0.12667,
+            0.10129,
+            -0.23371,
+            -0.16521,
+            -0.18517,
+            0.461,
+            -0.033971,
+            0.017809,
+            0.46875,
+            0.12673,
+            0.0028595,
+            -0.13199,
+            -0.095804,
+            -0.12651,
+            -0.13432,
+            -0.09511,
+            0.012205,
+            -0.071154,
+            -0.061039,
+            0.055788,
+            0.0011696,
+            0.042462,
+            -0.03893,
+            -0.034787,
+            0.013069,
+            -0.20275,
+            -0.079412,
+            -0.043243,
+            -0.20781,
+            0.17735,
+            -0.14918,
+            -0.11426,
+            0.053805,
+            -0.024793,
+            -0.095585,
+            0.027254,
+            0.14379,
+            0.021322,
+            -0.15207,
+            0.024013,
+            -0.41614,
+            -0.1827,
+            -0.016116,
+            0.083302,
+            -0.23303,
+            -0.039871,
+            0.11643,
+            0.11847,
+            0.51551,
+            0.078528,
+            0.13271,
+            0.033601,
+            0.056779,
+            -0.01759,
+            -0.17236,
+            -0.040732,
+            -0.19344,
+            -0.0058287,
+            -0.020529,
+            0.075106,
+            0.11718,
+            -0.023666,
+            0.085855,
+            0.10731,
+            -0.037066,
+            0.072463,
+            0.1544,
+            0.0023117,
+            0.036341,
+            -0.057703,
+            -0.27127,
+            0.053787,
+            0.13969,
+            0.26433,
+            0.17414,
+            -0.14509,
+            0.20932,
+            0.19288,
+            0.049908,
+            -0.027283,
+            -0.17269,
+            0.3089,
+            0.85209,
+            -0.0060783,
+            -0.09537,
+            -0.27279,
+            -0.075679,
+            -0.044211,
+            0.061272
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
@@ -367,62 +327,102 @@
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
+            1,
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
+            1,
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
+          "candidate_index": 2539,
+          "gene": "HOXC4",
+          "score": -0.12667,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17227,
+          "gene": "NOTUM",
+          "score": 0.10129,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3401,
+          "gene": "NANS",
+          "score": -0.23371,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2011,
+          "gene": "KLRC1",
+          "score": -0.16521,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3104,
+          "gene": "ZNF430",
+          "score": -0.18517,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15096,
+          "gene": "RMND5A",
+          "score": 0.461,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 10933,
+          "gene": "DUSP28",
+          "score": -0.033971,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10897,
+          "gene": "EXO5",
+          "score": 0.017809,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17445,
+          "gene": "POLR1A",
+          "score": 0.46875,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 14481,
+          "gene": "C17orf53",
+          "score": 0.12673,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5507,
+          "gene": "IFITM3",
+          "score": 0.0028595,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4169,
+          "gene": "MARCH8",
+          "score": -0.13199,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2643,
+          "gene": "PREX1",
+          "score": -0.095804,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10547,
+          "gene": "TMEM191B",
+          "score": -0.12651,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1651,
+          "gene": "ELK1",
+          "score": -0.13432,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8853,
+          "gene": "S100A2",
+          "score": -0.09511,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12148,
+          "gene": "OR10J1",
+          "score": 0.012205,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6137,
+          "gene": "GCNT1",
+          "score": -0.071154,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2319,
+          "gene": "CHDH",
+          "score": -0.061039,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18209,
+          "gene": "RAB25",
+          "score": 0.055788,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3740,
+          "gene": "ZNF341",
+          "score": 0.0011696,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9807,
+          "gene": "UBL4A",
+          "score": 0.042462,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16328,
+          "gene": "DRD1",
+          "score": -0.03893,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11933,
+          "gene": "PTMS",
+          "score": -0.034787,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14324,
+          "gene": "OTOP1",
+          "score": 0.013069,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1361,
+          "gene": "FAM133B",
+          "score": -0.20275,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15611,
+          "gene": "INS",
+          "score": -0.079412,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13693,
+          "gene": "GLB1L",
+          "score": -0.043243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2757,
+          "gene": "DENND5A",
+          "score": -0.20781,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11818,
+          "gene": "LINGO4",
+          "score": 0.17735,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4196,
+          "gene": "DDX3Y",
+          "score": -0.14918,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2842,
+          "gene": "PPP1R17",
+          "score": -0.11426,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5084,
+          "gene": "C21orf140",
+          "score": 0.053805,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10151,
+          "gene": "DPRX",
+          "score": -0.024793,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3595,
+          "gene": "KDM6B",
+          "score": -0.095585,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17655,
+          "gene": "HESX1",
+          "score": 0.027254,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14019,
+          "gene": "OR2A5",
+          "score": 0.14379,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14621,
+          "gene": "RHOQ",
+          "score": 0.021322,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1251,
+          "gene": "ANAPC16",
+          "score": -0.15207,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4836,
+          "gene": "DHRS12",
+          "score": 0.024013,
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
+          "candidate_index": 3490,
+          "gene": "HNRNPCL1",
+          "score": -0.1827,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4103,
+          "gene": "CCL8",
+          "score": -0.016116,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4159,
+          "gene": "IFI27",
+          "score": 0.083302,
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
+          "candidate_index": 11142,
+          "gene": "LOC101927572",
+          "score": -0.039871,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3913,
+          "gene": "NSA2",
+          "score": 0.11643,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17559,
+          "gene": "TRIM71",
+          "score": 0.11847,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16434,
+          "gene": "PRPF4B",
+          "score": 0.51551,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 8547,
+          "gene": "PTPRB",
+          "score": 0.078528,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15057,
+          "gene": "OR2Y1",
+          "score": 0.13271,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11222,
+          "gene": "PFKFB4",
+          "score": 0.033601,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12729,
+          "gene": "OR2T4",
+          "score": 0.056779,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2873,
+          "gene": "EPS8L2",
+          "score": -0.01759,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1101,
+          "gene": "ZNF491",
+          "score": -0.17236,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3065,
+          "gene": "CDRT4",
+          "score": -0.040732,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6797,
+          "gene": "USP17L18",
+          "score": -0.19344,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13356,
+          "gene": "CDC40",
+          "score": -0.0058287,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6399,
+          "gene": "TRIM4",
+          "score": -0.020529,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13317,
+          "gene": "SEC23B",
+          "score": 0.075106,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8591,
+          "gene": "TCTEX1D4",
+          "score": 0.11718,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13489,
+          "gene": "OR52H1",
+          "score": -0.023666,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10804,
+          "gene": "ARL14EP",
+          "score": 0.085855,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13134,
+          "gene": "PRIM1",
+          "score": 0.10731,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11452,
+          "gene": "TK2",
+          "score": -0.037066,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1708,
+          "gene": "ANKH",
+          "score": 0.072463,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6130,
+          "gene": "ADAMTS19",
+          "score": 0.1544,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17734,
+          "gene": "YAF2",
+          "score": 0.0023117,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5869,
+          "gene": "FGFR3",
+          "score": 0.036341,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6194,
+          "gene": "NEK9",
+          "score": -0.057703,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1684,
+          "gene": "COLEC10",
+          "score": -0.27127,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7705,
+          "gene": "FADS3",
+          "score": 0.053787,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9902,
+          "gene": "C1orf53",
+          "score": 0.13969,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7325,
+          "gene": "OGN",
+          "score": 0.26433,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11400,
+          "gene": "CSNK1E",
+          "score": 0.17414,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6195,
+          "gene": "OR2M7",
+          "score": -0.14509,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7143,
+          "gene": "CHST10",
+          "score": 0.20932,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12669,
+          "gene": "CDC42EP2",
+          "score": 0.19288,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12845,
+          "gene": "SRSF11",
+          "score": 0.049908,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7421,
+          "gene": "C20orf24",
+          "score": -0.027283,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1999,
+          "gene": "AWAT1",
+          "score": -0.17269,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15126,
+          "gene": "TJP1",
+          "score": 0.3089,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16542,
+          "gene": "CHMP6",
+          "score": 0.85209,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2017,
+          "gene": "GCM1",
+          "score": -0.0060783,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3166,
+          "gene": "BPIFB2",
+          "score": -0.09537,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 895,
+          "gene": "TMED7",
+          "score": -0.27279,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 780,
+          "gene": "PROKR1",
+          "score": -0.075679,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18006,
+          "gene": "PRMT8",
+          "score": -0.044211,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16853,
+          "gene": "C9orf62",
+          "score": 0.061272,
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
+          "candidate_index": 2539,
+          "gene": "HOXC4",
+          "score": -0.12667,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17227,
+          "gene": "NOTUM",
+          "score": 0.10129,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3401,
+          "gene": "NANS",
+          "score": -0.23371,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2011,
+          "gene": "KLRC1",
+          "score": -0.16521,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3104,
+          "gene": "ZNF430",
+          "score": -0.18517,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15096,
+          "gene": "RMND5A",
+          "score": 0.461,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 10933,
+          "gene": "DUSP28",
+          "score": -0.033971,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10897,
+          "gene": "EXO5",
+          "score": 0.017809,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17445,
+          "gene": "POLR1A",
+          "score": 0.46875,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 14481,
+          "gene": "C17orf53",
+          "score": 0.12673,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5507,
+          "gene": "IFITM3",
+          "score": 0.0028595,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4169,
+          "gene": "MARCH8",
+          "score": -0.13199,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2643,
+          "gene": "PREX1",
+          "score": -0.095804,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10547,
+          "gene": "TMEM191B",
+          "score": -0.12651,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1651,
+          "gene": "ELK1",
+          "score": -0.13432,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8853,
+          "gene": "S100A2",
+          "score": -0.09511,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12148,
+          "gene": "OR10J1",
+          "score": 0.012205,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6137,
+          "gene": "GCNT1",
+          "score": -0.071154,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2319,
+          "gene": "CHDH",
+          "score": -0.061039,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18209,
+          "gene": "RAB25",
+          "score": 0.055788,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3740,
+          "gene": "ZNF341",
+          "score": 0.0011696,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9807,
+          "gene": "UBL4A",
+          "score": 0.042462,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16328,
+          "gene": "DRD1",
+          "score": -0.03893,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11933,
+          "gene": "PTMS",
+          "score": -0.034787,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14324,
+          "gene": "OTOP1",
+          "score": 0.013069,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1361,
+          "gene": "FAM133B",
+          "score": -0.20275,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15611,
+          "gene": "INS",
+          "score": -0.079412,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13693,
+          "gene": "GLB1L",
+          "score": -0.043243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2757,
+          "gene": "DENND5A",
+          "score": -0.20781,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11818,
+          "gene": "LINGO4",
+          "score": 0.17735,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4196,
+          "gene": "DDX3Y",
+          "score": -0.14918,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2842,
+          "gene": "PPP1R17",
+          "score": -0.11426,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5084,
+          "gene": "C21orf140",
+          "score": 0.053805,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10151,
+          "gene": "DPRX",
+          "score": -0.024793,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3595,
+          "gene": "KDM6B",
+          "score": -0.095585,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17655,
+          "gene": "HESX1",
+          "score": 0.027254,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14019,
+          "gene": "OR2A5",
+          "score": 0.14379,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14621,
+          "gene": "RHOQ",
+          "score": 0.021322,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1251,
+          "gene": "ANAPC16",
+          "score": -0.15207,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4836,
+          "gene": "DHRS12",
+          "score": 0.024013,
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
+          "candidate_index": 3490,
+          "gene": "HNRNPCL1",
+          "score": -0.1827,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4103,
+          "gene": "CCL8",
+          "score": -0.016116,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4159,
+          "gene": "IFI27",
+          "score": 0.083302,
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
+          "candidate_index": 11142,
+          "gene": "LOC101927572",
+          "score": -0.039871,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3913,
+          "gene": "NSA2",
+          "score": 0.11643,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17559,
+          "gene": "TRIM71",
+          "score": 0.11847,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16434,
+          "gene": "PRPF4B",
+          "score": 0.51551,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 8547,
+          "gene": "PTPRB",
+          "score": 0.078528,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15057,
+          "gene": "OR2Y1",
+          "score": 0.13271,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11222,
+          "gene": "PFKFB4",
+          "score": 0.033601,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12729,
+          "gene": "OR2T4",
+          "score": 0.056779,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2873,
+          "gene": "EPS8L2",
+          "score": -0.01759,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1101,
+          "gene": "ZNF491",
+          "score": -0.17236,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3065,
+          "gene": "CDRT4",
+          "score": -0.040732,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6797,
+          "gene": "USP17L18",
+          "score": -0.19344,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13356,
+          "gene": "CDC40",
+          "score": -0.0058287,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6399,
+          "gene": "TRIM4",
+          "score": -0.020529,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13317,
+          "gene": "SEC23B",
+          "score": 0.075106,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8591,
+          "gene": "TCTEX1D4",
+          "score": 0.11718,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13489,
+          "gene": "OR52H1",
+          "score": -0.023666,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10804,
+          "gene": "ARL14EP",
+          "score": 0.085855,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13134,
+          "gene": "PRIM1",
+          "score": 0.10731,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11452,
+          "gene": "TK2",
+          "score": -0.037066,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1708,
+          "gene": "ANKH",
+          "score": 0.072463,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6130,
+          "gene": "ADAMTS19",
+          "score": 0.1544,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17734,
+          "gene": "YAF2",
+          "score": 0.0023117,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5869,
+          "gene": "FGFR3",
+          "score": 0.036341,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6194,
+          "gene": "NEK9",
+          "score": -0.057703,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1684,
+          "gene": "COLEC10",
+          "score": -0.27127,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7705,
+          "gene": "FADS3",
+          "score": 0.053787,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9902,
+          "gene": "C1orf53",
+          "score": 0.13969,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7325,
+          "gene": "OGN",
+          "score": 0.26433,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11400,
+          "gene": "CSNK1E",
+          "score": 0.17414,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6195,
+          "gene": "OR2M7",
+          "score": -0.14509,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7143,
+          "gene": "CHST10",
+          "score": 0.20932,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12669,
+          "gene": "CDC42EP2",
+          "score": 0.19288,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12845,
+          "gene": "SRSF11",
+          "score": 0.049908,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7421,
+          "gene": "C20orf24",
+          "score": -0.027283,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1999,
+          "gene": "AWAT1",
+          "score": -0.17269,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15126,
+          "gene": "TJP1",
+          "score": 0.3089,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16542,
+          "gene": "CHMP6",
+          "score": 0.85209,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2017,
+          "gene": "GCM1",
+          "score": -0.0060783,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3166,
+          "gene": "BPIFB2",
+          "score": -0.09537,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 895,
+          "gene": "TMED7",
+          "score": -0.27279,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 780,
+          "gene": "PROKR1",
+          "score": -0.075679,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18006,
+          "gene": "PRMT8",
+          "score": -0.044211,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16853,
+          "gene": "C9orf62",
+          "score": 0.061272,
+          "hit": 0,
+          "round": 1
         }
       ]
     }

```
