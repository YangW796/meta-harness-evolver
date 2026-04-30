# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IL2/run-1/best/current/harness
Generated at: 2026-04-30T06:42:15.385850

## Files Changed

- model.py: modified (added=4, deleted=1, delta=3)
- outputs/metrics.json: modified (added=2422, deleted=630, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -107,7 +107,10 @@
                 similar_indices = bda_tools.gene_search(gene, k=10, diverse=False)
                 # Filter to available indices only (not yet selected)
                 similar_available = [i for i in similar_indices if i in available_indices and i not in exploit_pool and i not in selected]
-                exploit_pool.extend(similar_available)
+                # Only keep top 50% of similar genes to maintain quality
+                # Use the first half (higher-ranked by gene search)
+                keep_count = max(1, len(similar_available) // 2)
+                exploit_pool.extend(similar_available[:keep_count])
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
-      "rounds": 2,
+      "rounds": 3,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 128,
-      "baseline_total_hits": 2,
+      "baseline_total_queries": 256,
+      "baseline_total_hits": 8,
       "delta_queries": 128,
-      "delta_hits": 6,
-      "total_queries": 256,
-      "total_hits": 8,
+      "delta_hits": 2,
+      "total_queries": 384,
+      "total_hits": 10,
       "top_k": 654,
       "hit_curve": {
         "queries": [
-          128,
-          256
+          256,
+          384
         ],
         "hits": [
-          2,
-          8
+          8,
+          10
         ]
       },
-      "auc": 640.0,
-      "auc_normalized": 0.00382262996941896,
-      "ncg": 0.14829332160283393,
+      "auc": 1152.0,
+      "auc_normalized": 0.0045871559633027525,
+      "ncg": 0.1647511167553707,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 6,
-          "cumulative_hits": 8,
-          "precision_at_batch": 0.046875,
+          "hits": 2,
+          "cumulative_hits": 10,
+          "precision_at_batch": 0.015625,
           "selected": [
-            "C18orf65",
-            "NUFIP2",
-            "MRPL45",
-            "MXRA7",
-            "TMEM41B",
-            "WDR54",
-            "TSPAN19",
-            "STAT5B",
-            "SLC15A1",
-            "HIST3H2BB",
-            "DLL1",
-            "HIGD1B",
-            "ETV1",
-            "SPTSSB",
-            "PODNL1",
-            "SERINC4",
-            "FUOM",
-            "C15orf39",
-            "ARSK",
-            "BCAN",
-            "ZNF623",
-            "DCAF8L1",
-            "CRELD1",
-            "TMSB4X",
-            "DTNA",
-            "UBR4",
-            "CTPS1",
-            "SUGCT",
-            "NLGN1",
-            "FRMPD4",
-            "NIM1K",
-            "HNRNPD",
-            "HK3",
-            "GOLGA2",
-            "LOC729159",
-            "FCER2",
-            "PKDCC",
-            "ZMYM3",
-            "CARMIL3",
-            "IARS2",
-            "C10orf82",
-            "HLA-DMA",
-            "ARSF",
-            "PCDHGA2",
-            "MRPL39",
-            "PPM1B",
-            "ZBTB7A",
-            "VTI1B",
-            "FAM124A",
-            "TMEM86B",
-            "PABPC5",
-            "IFNL2",
-            "HOXB7",
-            "APP",
-            "CERS5",
-            "TSC2",
-            "PCDHB16",
-            "CHD2",
-            "SLC35G1",
-            "SLC19A3",
-            "TRIM49",
-            "SART3",
-            "RNF217",
-            "EFCAB1",
-            "MRPL20",
-            "CUL4A",
-            "TBCD",
-            "C9",
-            "IZUMO3",
-            "C10orf111",
-            "SLC5A1",
-            "C1orf115",
-            "CCDC175",
-            "UQCR10",
-            "CLDN16",
-            "CDK16",
-            "ASCL2",
-            "PTRH2",
-            "CFAP47",
-            "SIN3B",
-            "GIF",
-            "SDS",
-            "LGR4",
-            "GABARAPL1",
-            "CCDC142",
-            "SLC5A10",
-            "KLHL38",
-            "POU3F3",
-            "NSL1",
-            "NHLRC4",
-            "EBF2",
-            "XYLT1",
-            "CCL23",
-            "SP3",
-            "OR2AK2",
-            "ACE2",
-            "GABRD",
-            "RALGAPA2",
-            "KARS",
-            "DNAJC24",
-            "USMG5",
-            "PRSS42",
-            "DSCC1",
-            "HARS2",
-            "METTL18",
-            "IL37",
-            "C1orf131",
-            "OR5H14",
-            "GPR171",
-            "ZFP36",
-            "RBM11",
-            "AIP",
-            "BICC1",
-            "NET1",
-            "EXOSC10",
-            "SLC25A53",
-            "NRBP1",
-            "KLF15",
-            "KRT72",
-            "MYOM2",
-            "FBXO44",
-            "RASGRP4",
-            "NR1H4",
-            "HIPK3",
-            "FBRSL1",
-            "SSX5",
-            "NISCH",
-            "AGAP9"
+            "C1orf158",
+            "DTX3",
+            "PYCR1",
+            "ANKRD1",
+            "ANXA7",
+            "IFT57",
+            "AGXT",
+            "FCRL5",
+            "PDCD1",
+            "CAVIN1",
+            "RPF2",
+            "FAM76A",
+            "SERPINB11",
+            "KLHL31",
+            "GHDC",
+            "SHOX",
+            "LRRC63",
+            "ZWILCH",
+            "MTRNR2L1",
+            "FBXL19",
+            "RASSF9",
+            "SAMD4A",
+            "PICK1",
+            "NEMP1",
+            "VSIG10L2",
+            "MSI1",
+            "SCN11A",
+            "EGFL7",
+            "ISPD",
+            "FLOT1",
+            "FAS",
+            "ARL13A",
+            "ADAM18",
+            "BOLA1",
+            "ZNF773",
+            "COA6",
+            "GRK6",
+            "HACD3",
+            "GPBP1",
+            "ELF4",
+            "MACF1",
+            "NDUFA13",
+            "TSKS",
+            "GBA",
+            "CHORDC1",
+            "SMIM19",
+            "WDR64",
+            "EPHX2",
+            "IFITM2",
+            "VSTM2A",
+            "TTC39B",
+            "HLA-DPB1",
+            "CXCR2",
+            "STUB1",
+            "SAFB",
+            "TCP10L2",
+            "SUV39H1",
+            "MED6",
+            "ATP6V1D",
+            "WDR88",
+            "CEACAM3",
+            "TSPO",
+            "KCNN4",
+            "PLCG2",
+            "ADH6",
+            "LBP",
+            "GRINA",
+            "WDR3",
+            "PDE8B",
+            "PRKACA",
+            "PRKN",
+            "PANX3",
+            "RGPD4",
+            "G2E3",
+            "ORC1",
+            "CLEC7A",
+            "SCARF2",
+            "SULT1B1",
+            "LARS2",
+            "OR5I1",
+            "PYHIN1",
+            "ZNF761",
+            "SPAG6",
+            "ZNF703",
+            "SLC24A5",
+            "SH2D4A",
+            "NOMO1",
+            "OR14A16",
+            "ZNF330",
+            "SSTR4",
+            "OR13J1",
+            "TRIM34",
+            "TMEM225B",
+            "RHBDL1",
+            "LIMD2",
+            "SNAI1",
+            "CA5A",
+            "STARD4",
+            "TRIM31",
+            "PRAMEF14",
+            "RPA2",
+            "LHB",
+            "OR10G4",
+            "BCL11A",
+            "SNAP23",
+            "CSPG4",
+            "B3GNT6",
+            "TGIF2-C20orf24",
+            "SYT17",
+            "TUBGCP3",
+            "CLVS2",
+            "BRWD3",
+            "OR52L1",
+            "B4GALT6",
+            "KRT71",
+            "PSIP1",
+            "LRG1",
+            "ENTPD5",
+            "NPB",
+            "CACNA1D",
+            "DACT1",
+            "CADM2",
+            "NRN1",
+            "OR2AE1",
+            "YLPM1",
+            "MFSD2A",
+            "DFFA",
+            "BID"
           ],
           "selected_scores": [
-            -0.15548,
-            -0.13605,
-            -0.036223,
-            0.10713,
-            0.085085,
-            -0.10631,
-            0.10151,
-            0.66825,
-            -0.33204,
-            0.11889,
-            0.042788,
-            -0.058602,
-            0.091516,
-            0.038805,
-            0.014045,
-            -0.12633,
-            0.015142,
-            -0.13525,
-            -0.098201,
-            0.15259,
-            -0.0068339,
-            -0.011761,
-            -0.13571,
-            0.13174,
-            0.17313,
-            -0.13676,
-            0.75435,
-            0.1954,
-            0.053172,
-            -0.055871,
-            0.18883,
-            -0.24775,
-            -0.1471,
-            -0.11265,
-            0.015227,
-            -0.07774,
-            -0.059766,
-            -0.1353,
-            -0.009723,
-            -0.053533,
-            0.17092,
-            -0.10256,
-            -0.23222,
-            -0.03869,
-            0.33297,
-            0.19186,
-            -0.0031567,
-            -0.036043,
-            0.042661,
-            -0.16725,
-            -0.12012,
-            -0.15254,
-            0.086387,
-            -0.11897,
-            -0.0074335,
-            0.37433,
-            -0.21398,
-            -0.042776,
-            0.10571,
-            -0.081111,
-            0.16044,
-            0.26696,
-            -0.033267,
-            -0.023499,
-            -0.19691,
-            -0.012886,
-            0.19745,
-            -0.07877,
-            -0.10881,
-            -0.029118,
-            -0.1587,
-            -0.11322,
-            0.10326,
-            0.076353,
-            -0.078631,
-            0.13724,
-            -0.0808,
-            -0.20475,
-            0.039072,
-            -0.41614,
-            0.074703,
-            -0.092917,
-            -0.05853,
-            -0.23303,
-            -0.11455,
-            -0.080302,
-            -0.0014004,
-            0.18901,
-            0.16991,
-            0.004058,
-            -0.13201,
-            0.27896,
-            -0.11632,
-            -0.17675,
-            -0.16243,
-            -0.090405,
-            0.064745,
-            -0.12151,
-            0.11366,
-            0.092131,
-            -0.023547,
-            0.057466,
-            0.015806,
-            0.15363,
-            -0.11573,
-            -0.13746,
-            0.12026,
-            -0.037378,
-            -0.041124,
-            -0.017196,
-            0.1164,
-            -0.021423,
-            0.024422,
-            -0.091153,
-            0.075299,
-            -0.043129,
-            0.36928,
-            0.21171,
-            0.033732,
-            0.048418,
-            0.16553,
-            0.039352,
-            0.089194,
-            0.04917,
-            -0.20488,
-            -0.2542,
-            0.095073,
-            -0.13724
+            0.097043,
+            0.038861,
+            0.06193,
+            -0.0057194,
+            -0.026024,
+            0.19312,
+            0.26047,
+            0.053097,
+            -0.23117,
+            -0.07357,
+            0.44494,
+            -0.30972,
+            -0.023671,
+            -0.083264,
+            0.010694,
+            0.05685,
+            0.11154,
+            0.15664,
+            -0.034782,
+            0.035626,
+            -0.12464,
+            -0.091046,
+            0.010582,
+            0.068917,
+            0.038939,
+            0.0062171,
+            -0.22155,
+            0.032839,
+            0.032868,
+            -0.0061212,
+            -0.16284,
+            -0.12537,
+            -0.028411,
+            -0.00089316,
+            0.045895,
+            -0.18267,
+            0.08963,
+            0.1045,
+            -0.090071,
+            -0.18139,
+            -0.11163,
+            0.014495,
+            -0.090791,
+            -0.23715,
+            -0.0047188,
+            0.091257,
+            -0.046877,
+            0.22395,
+            0.11283,
+            0.065186,
+            -0.047559,
+            -0.08977,
+            0.067021,
+            -0.067023,
+            0.19949,
+            0.19728,
+            -0.018781,
+            -0.164,
+            -0.031837,
+            -0.08229,
+            0.097253,
+            -0.094768,
+            -0.236,
+            0.042606,
+            0.10784,
+            0.1237,
+            -0.14135,
+            0.33659,
+            0.049945,
+            -0.0045085,
+            0.093661,
+            0.10517,
+            0.08214,
+            -0.20105,
+            -0.11196,
+            -0.16276,
+            -0.046342,
+            -0.19371,
+            0.09608,
+            -0.11676,
+            -0.04228,
+            -0.079377,
+            -0.19942,
+            -0.1523,
+            0.062797,
+            -0.0058831,
+            -0.0093454,
+            -0.12285,
+            0.12166,
+            0.097402,
+            -0.064619,
+            0.062544,
+            0.033022,
+            -0.030375,
+            -0.026979,
+            -0.061154,
+            0.12589,
+            0.053657,
+            0.054297,
+            -0.099496,
+            0.20762,
+            0.086577,
+            -0.23147,
+            -0.077921,
+            0.18266,
+            -0.022444,
+            0.047247,
+            0.14962,
+            0.040779,
+            0.41857,
+            0.0028453,
+            -0.2053,
+            0.054894,
+            -0.11599,
+            0.12077,
+            0.021862,
+            -0.094189,
+            -0.050377,
+            -0.020113,
+            0.071356,
+            0.10007,
+            -0.081387,
+            0.05283,
+            -0.038128,
+            -0.029124,
+            -0.012017,
+            0.24165,
+            0.14308
           ],
           "selected_hits": [
             0,
@@ -308,7 +308,108 @@
             0,
             0,
             0,
+            0,
+            0,
+            0,
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
@@ -317,107 +418,6 @@
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
-            1,
             0,
             0,
             0,
@@ -1334,896 +1334,1792 @@
           "gene": "C18orf65",
           "score": -0.15548,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9446,
           "gene": "NUFIP2",
           "score": -0.13605,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4750,
           "gene": "MRPL45",
           "score": -0.036223,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15265,
           "gene": "MXRA7",
           "score": 0.10713,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12208,
           "gene": "TMEM41B",
           "score": 0.085085,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3177,
           "gene": "WDR54",
           "score": -0.10631,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14956,
           "gene": "TSPAN19",
           "score": 0.10151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16439,
           "gene": "STAT5B",
           "score": 0.66825,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 629,
           "gene": "SLC15A1",
           "score": -0.33204,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16959,
           "gene": "HIST3H2BB",
           "score": 0.11889,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14271,
           "gene": "DLL1",
           "score": 0.042788,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12289,
           "gene": "HIGD1B",
           "score": -0.058602,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18044,
           "gene": "ETV1",
           "score": 0.091516,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14326,
           "gene": "SPTSSB",
           "score": 0.038805,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13003,
           "gene": "PODNL1",
           "score": 0.014045,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5815,
           "gene": "SERINC4",
           "score": -0.12633,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1902,
           "gene": "FUOM",
           "score": 0.015142,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3541,
           "gene": "C15orf39",
           "score": -0.13525,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4111,
           "gene": "ARSK",
           "score": -0.098201,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12405,
           "gene": "BCAN",
           "score": 0.15259,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5063,
           "gene": "ZNF623",
           "score": -0.0068339,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3158,
           "gene": "DCAF8L1",
           "score": -0.011761,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5302,
           "gene": "CRELD1",
           "score": -0.13571,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16905,
           "gene": "TMSB4X",
           "score": 0.13174,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16364,
           "gene": "DTNA",
           "score": 0.17313,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4247,
           "gene": "UBR4",
           "score": -0.13676,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12770,
           "gene": "CTPS1",
           "score": 0.75435,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16716,
           "gene": "SUGCT",
           "score": 0.1954,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8978,
           "gene": "NLGN1",
           "score": 0.053172,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6000,
           "gene": "FRMPD4",
           "score": -0.055871,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12441,
           "gene": "NIM1K",
           "score": 0.18883,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2093,
           "gene": "HNRNPD",
           "score": -0.24775,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1613,
           "gene": "HK3",
           "score": -0.1471,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2016,
           "gene": "GOLGA2",
           "score": -0.11265,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6157,
           "gene": "LOC729159",
           "score": 0.015227,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2023,
           "gene": "FCER2",
           "score": -0.07774,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5471,
           "gene": "PKDCC",
           "score": -0.059766,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9779,
           "gene": "ZMYM3",
           "score": -0.1353,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9089,
           "gene": "CARMIL3",
           "score": -0.009723,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2546,
           "gene": "IARS2",
           "score": -0.053533,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17265,
           "gene": "C10orf82",
           "score": 0.17092,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3410,
           "gene": "HLA-DMA",
           "score": -0.10256,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2015,
           "gene": "ARSF",
           "score": -0.23222,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3111,
           "gene": "PCDHGA2",
           "score": -0.03869,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15128,
           "gene": "MRPL39",
           "score": 0.33297,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10956,
           "gene": "PPM1B",
           "score": 0.19186,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10920,
           "gene": "ZBTB7A",
           "score": -0.0031567,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17483,
           "gene": "VTI1B",
           "score": -0.036043,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14512,
           "gene": "FAM124A",
           "score": 0.042661,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5523,
           "gene": "TMEM86B",
           "score": -0.16725,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4180,
           "gene": "PABPC5",
           "score": -0.12012,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2650,
           "gene": "IFNL2",
           "score": -0.15254,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10570,
           "gene": "HOXB7",
           "score": 0.086387,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1654,
           "gene": "APP",
           "score": -0.11897,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8872,
           "gene": "CERS5",
           "score": -0.0074335,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12171,
           "gene": "TSC2",
           "score": 0.37433,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6155,
           "gene": "PCDHB16",
           "score": -0.21398,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2326,
           "gene": "CHD2",
           "score": -0.042776,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18248,
           "gene": "SLC35G1",
           "score": 0.10571,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3750,
           "gene": "SLC19A3",
           "score": -0.081111,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9830,
           "gene": "TRIM49",
           "score": 0.16044,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16362,
           "gene": "SART3",
           "score": 0.26696,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11957,
           "gene": "RNF217",
           "score": -0.033267,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14355,
           "gene": "EFCAB1",
           "score": -0.023499,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1363,
           "gene": "MRPL20",
           "score": -0.19691,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15644,
           "gene": "CUL4A",
           "score": -0.012886,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13722,
           "gene": "TBCD",
           "score": 0.19745,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2764,
           "gene": "C9",
           "score": -0.07877,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11841,
           "gene": "IZUMO3",
           "score": -0.10881,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4207,
           "gene": "C10orf111",
           "score": -0.029118,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2850,
           "gene": "SLC5A1",
           "score": -0.1587,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5099,
           "gene": "C1orf115",
           "score": -0.11322,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10174,
           "gene": "CCDC175",
           "score": 0.10326,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3605,
           "gene": "UQCR10",
           "score": 0.076353,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17694,
           "gene": "CLDN16",
           "score": -0.078631,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14049,
           "gene": "CDK16",
           "score": 0.13724,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14652,
           "gene": "ASCL2",
           "score": -0.0808,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1252,
           "gene": "PTRH2",
           "score": -0.20475,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4849,
           "gene": "CFAP47",
           "score": 0.039072,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 82,
           "gene": "SIN3B",
           "score": -0.41614,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3499,
           "gene": "GIF",
           "score": 0.074703,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4114,
           "gene": "SDS",
           "score": -0.092917,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4170,
           "gene": "LGR4",
           "score": -0.05853,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 560,
           "gene": "GABARAPL1",
           "score": -0.23303,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11167,
           "gene": "CCDC142",
           "score": -0.11455,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3923,
           "gene": "SLC5A10",
           "score": -0.080302,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17599,
           "gene": "KLHL38",
           "score": -0.0014004,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16469,
           "gene": "POU3F3",
           "score": 0.18901,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8566,
           "gene": "NSL1",
           "score": 0.16991,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15089,
           "gene": "NHLRC4",
           "score": 0.004058,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11245,
           "gene": "EBF2",
           "score": -0.13201,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12756,
           "gene": "XYLT1",
           "score": 0.27896,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2880,
           "gene": "CCL23",
           "score": -0.11632,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1102,
           "gene": "SP3",
           "score": -0.17675,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3073,
           "gene": "OR2AK2",
           "score": -0.16243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6816,
           "gene": "ACE2",
           "score": -0.090405,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13385,
           "gene": "GABRD",
           "score": 0.064745,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6418,
           "gene": "RALGAPA2",
           "score": -0.12151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13346,
           "gene": "KARS",
           "score": 0.11366,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8611,
           "gene": "DNAJC24",
           "score": 0.092131,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13518,
           "gene": "USMG5",
           "score": -0.023547,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10827,
           "gene": "PRSS42",
           "score": 0.057466,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13164,
           "gene": "DSCC1",
           "score": 0.015806,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11475,
           "gene": "HARS2",
           "score": 0.15363,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1711,
           "gene": "METTL18",
           "score": -0.11573,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6148,
           "gene": "IL37",
           "score": -0.13746,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17772,
           "gene": "C1orf131",
           "score": 0.12026,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5886,
           "gene": "OR5H14",
           "score": -0.037378,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6213,
           "gene": "GPR171",
           "score": -0.041124,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1687,
           "gene": "ZFP36",
           "score": -0.017196,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7724,
           "gene": "RBM11",
           "score": 0.1164,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9925,
           "gene": "AIP",
           "score": -0.021423,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7344,
           "gene": "BICC1",
           "score": 0.024422,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11423,
           "gene": "NET1",
           "score": -0.091153,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6214,
           "gene": "EXOSC10",
           "score": 0.075299,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7162,
           "gene": "SLC25A53",
           "score": -0.043129,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12696,
           "gene": "NRBP1",
           "score": 0.36928,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12873,
           "gene": "KLF15",
           "score": 0.21171,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7440,
           "gene": "KRT72",
           "score": 0.033732,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2003,
           "gene": "MYOM2",
           "score": 0.048418,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15159,
           "gene": "FBXO44",
           "score": 0.16553,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16578,
           "gene": "RASGRP4",
           "score": 0.039352,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2022,
           "gene": "NR1H4",
           "score": 0.089194,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3175,
           "gene": "HIPK3",
           "score": 0.04917,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 896,
           "gene": "FBRSL1",
           "score": -0.20488,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 781,
           "gene": "SSX5",
           "score": -0.2542,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18045,
           "gene": "NISCH",
           "score": 0.095073,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16889,
           "gene": "AGAP9",
           "score": -0.13724,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 13581,
+          "gene": "C1orf158",
+          "score": 0.097043,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17275,
+          "gene": "DTX3",
+          "score": 0.038861,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18005,
+          "gene": "PYCR1",
+          "score": 0.06193,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3887,
+          "gene": "ANKRD1",
+          "score": -0.0057194,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5881,
+          "gene": "ANXA7",
+          "score": -0.026024,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12620,
+          "gene": "IFT57",
+          "score": 0.19312,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7495,
+          "gene": "AGXT",
+          "score": 0.26047,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9633,
+          "gene": "FCRL5",
+          "score": 0.053097,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 962,
+          "gene": "PDCD1",
+          "score": -0.23117,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7479,
+          "gene": "CAVIN1",
+          "score": -0.07357,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18889,
+          "gene": "RPF2",
+          "score": 0.44494,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 290,
+          "gene": "FAM76A",
+          "score": -0.30972,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3336,
+          "gene": "SERPINB11",
+          "score": -0.023671,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5218,
+          "gene": "KLHL31",
+          "score": -0.083264,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17067,
+          "gene": "GHDC",
+          "score": 0.010694,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10076,
+          "gene": "SHOX",
+          "score": 0.05685,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12582,
+          "gene": "LRRC63",
+          "score": 0.11154,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13466,
+          "gene": "ZWILCH",
+          "score": 0.15664,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10840,
+          "gene": "MTRNR2L1",
+          "score": -0.034782,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11909,
+          "gene": "FBXL19",
+          "score": 0.035626,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2446,
+          "gene": "RASSF9",
+          "score": -0.12464,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11263,
+          "gene": "SAMD4A",
+          "score": -0.091046,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9405,
+          "gene": "PICK1",
+          "score": 0.010582,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5297,
+          "gene": "NEMP1",
+          "score": 0.068917,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3733,
+          "gene": "VSIG10L2",
+          "score": 0.038939,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16978,
+          "gene": "MSI1",
+          "score": 0.0062171,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2330,
+          "gene": "SCN11A",
+          "score": -0.22155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3149,
+          "gene": "EGFL7",
+          "score": 0.032839,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8983,
+          "gene": "ISPD",
+          "score": 0.032868,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10486,
+          "gene": "FLOT1",
+          "score": -0.0061212,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3588,
+          "gene": "FAS",
+          "score": -0.16284,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9638,
+          "gene": "ARL13A",
+          "score": -0.12537,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1159,
+          "gene": "ADAM18",
+          "score": -0.028411,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11453,
+          "gene": "BOLA1",
+          "score": -0.00089316,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12830,
+          "gene": "ZNF773",
+          "score": 0.045895,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3192,
+          "gene": "COA6",
+          "score": -0.18267,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15860,
+          "gene": "GRK6",
+          "score": 0.08963,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15822,
+          "gene": "HACD3",
+          "score": 0.1045,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6345,
+          "gene": "GPBP1",
+          "score": -0.090071,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6293,
+          "gene": "ELF4",
+          "score": -0.18139,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4345,
+          "gene": "MACF1",
+          "score": -0.11163,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8608,
+          "gene": "NDUFA13",
+          "score": 0.014495,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8267,
+          "gene": "TSKS",
+          "score": -0.090791,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1635,
+          "gene": "GBA",
+          "score": -0.23715,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1443,
+          "gene": "CHORDC1",
+          "score": -0.0047188,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14537,
+          "gene": "SMIM19",
+          "score": 0.091257,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1256,
+          "gene": "WDR64",
+          "score": -0.046877,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10948,
+          "gene": "EPHX2",
+          "score": 0.22395,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12310,
+          "gene": "IFITM2",
+          "score": 0.11283,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15682,
+          "gene": "VSTM2A",
+          "score": 0.065186,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15111,
+          "gene": "TTC39B",
+          "score": -0.047559,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17995,
+          "gene": "HLA-DPB1",
+          "score": -0.08977,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5025,
+          "gene": "CXCR2",
+          "score": 0.067021,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7781,
+          "gene": "STUB1",
+          "score": -0.067023,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16096,
+          "gene": "SAFB",
+          "score": 0.19949,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15178,
+          "gene": "TCP10L2",
+          "score": 0.19728,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11524,
+          "gene": "SUV39H1",
+          "score": -0.018781,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1449,
+          "gene": "MED6",
+          "score": -0.164,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9267,
+          "gene": "ATP6V1D",
+          "score": -0.031837,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5251,
+          "gene": "WDR88",
+          "score": -0.08229,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 307,
+          "gene": "CEACAM3",
+          "score": 0.097253,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7443,
+          "gene": "TSPO",
+          "score": -0.094768,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 482,
+          "gene": "KCNN4",
+          "score": -0.236,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18510,
+          "gene": "PLCG2",
+          "score": 0.042606,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18085,
+          "gene": "ADH6",
+          "score": 0.10784,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9390,
+          "gene": "LBP",
+          "score": 0.1237,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11882,
+          "gene": "GRINA",
+          "score": -0.14135,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18757,
+          "gene": "WDR3",
+          "score": 0.33659,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6640,
+          "gene": "PDE8B",
+          "score": 0.049945,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13480,
+          "gene": "PRKACA",
+          "score": -0.0045085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3726,
+          "gene": "PRKN",
+          "score": 0.093661,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12025,
+          "gene": "PANX3",
+          "score": 0.10517,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11332,
+          "gene": "RGPD4",
+          "score": 0.08214,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3756,
+          "gene": "G2E3",
+          "score": -0.20105,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7464,
+          "gene": "ORC1",
+          "score": -0.11196,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1970,
+          "gene": "CLEC7A",
+          "score": -0.16276,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14434,
+          "gene": "SCARF2",
+          "score": -0.046342,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1594,
+          "gene": "SULT1B1",
+          "score": -0.19371,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15783,
+          "gene": "LARS2",
+          "score": 0.09608,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4091,
+          "gene": "OR5I1",
+          "score": -0.11676,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4764,
+          "gene": "PYHIN1",
+          "score": -0.04228,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5987,
+          "gene": "ZNF761",
+          "score": -0.079377,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 177,
+          "gene": "SPAG6",
+          "score": -0.19942,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9790,
+          "gene": "ZNF703",
+          "score": -0.1523,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2101,
+          "gene": "SLC24A5",
+          "score": 0.062797,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9069,
+          "gene": "SH2D4A",
+          "score": -0.0058831,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2480,
+          "gene": "NOMO1",
+          "score": -0.0093454,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 222,
+          "gene": "OR14A16",
+          "score": -0.12285,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14500,
+          "gene": "ZNF330",
+          "score": 0.12166,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9134,
+          "gene": "SSTR4",
+          "score": 0.097402,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5953,
+          "gene": "OR13J1",
+          "score": -0.064619,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17433,
+          "gene": "TRIM34",
+          "score": 0.062544,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6429,
+          "gene": "TMEM225B",
+          "score": 0.033022,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2024,
+          "gene": "RHBDL1",
+          "score": -0.030375,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9313,
+          "gene": "LIMD2",
+          "score": -0.026979,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16086,
+          "gene": "SNAI1",
+          "score": -0.061154,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8752,
+          "gene": "CA5A",
+          "score": 0.12589,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2160,
+          "gene": "STARD4",
+          "score": 0.053657,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17053,
+          "gene": "TRIM31",
+          "score": 0.054297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10990,
+          "gene": "PRAMEF14",
+          "score": -0.099496,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18190,
+          "gene": "RPA2",
+          "score": 0.20762,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16235,
+          "gene": "LHB",
+          "score": 0.086577,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2179,
+          "gene": "OR10G4",
+          "score": -0.23147,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9471,
+          "gene": "BCL11A",
+          "score": -0.077921,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16349,
+          "gene": "SNAP23",
+          "score": 0.18266,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9995,
+          "gene": "CSPG4",
+          "score": -0.022444,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13368,
+          "gene": "B3GNT6",
+          "score": 0.047247,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13432,
+          "gene": "TGIF2-C20orf24",
+          "score": 0.14962,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10069,
+          "gene": "SYT17",
+          "score": 0.040779,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18215,
+          "gene": "TUBGCP3",
+          "score": 0.41857,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 14982,
+          "gene": "CLVS2",
+          "score": 0.0028453,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2424,
+          "gene": "BRWD3",
+          "score": -0.2053,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10575,
+          "gene": "OR52L1",
+          "score": 0.054894,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8404,
+          "gene": "B4GALT6",
+          "score": -0.11599,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4399,
+          "gene": "KRT71",
+          "score": 0.12077,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4420,
+          "gene": "PSIP1",
+          "score": 0.021862,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4422,
+          "gene": "LRG1",
+          "score": -0.094189,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2477,
+          "gene": "ENTPD5",
+          "score": -0.050377,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14711,
+          "gene": "NPB",
+          "score": -0.020113,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13196,
+          "gene": "CACNA1D",
+          "score": 0.071356,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11501,
+          "gene": "DACT1",
+          "score": 0.10007,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14772,
+          "gene": "CADM2",
+          "score": -0.081387,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2805,
+          "gene": "NRN1",
+          "score": 0.05283,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9138,
+          "gene": "OR2AE1",
+          "score": -0.038128,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4458,
+          "gene": "YLPM1",
+          "score": -0.029124,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9287,
+          "gene": "MFSD2A",
+          "score": -0.012017,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17758,
+          "gene": "DFFA",
+          "score": 0.24165,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16752,
+          "gene": "BID",
+          "score": 0.14308,
+          "hit": 0,
+          "round": 2
         }
       ],
       "queried_history": [
@@ -3128,896 +4024,1792 @@
           "gene": "C18orf65",
           "score": -0.15548,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9446,
           "gene": "NUFIP2",
           "score": -0.13605,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4750,
           "gene": "MRPL45",
           "score": -0.036223,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15265,
           "gene": "MXRA7",
           "score": 0.10713,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12208,
           "gene": "TMEM41B",
           "score": 0.085085,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3177,
           "gene": "WDR54",
           "score": -0.10631,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14956,
           "gene": "TSPAN19",
           "score": 0.10151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16439,
           "gene": "STAT5B",
           "score": 0.66825,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 629,
           "gene": "SLC15A1",
           "score": -0.33204,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16959,
           "gene": "HIST3H2BB",
           "score": 0.11889,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14271,
           "gene": "DLL1",
           "score": 0.042788,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12289,
           "gene": "HIGD1B",
           "score": -0.058602,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18044,
           "gene": "ETV1",
           "score": 0.091516,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14326,
           "gene": "SPTSSB",
           "score": 0.038805,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13003,
           "gene": "PODNL1",
           "score": 0.014045,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5815,
           "gene": "SERINC4",
           "score": -0.12633,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1902,
           "gene": "FUOM",
           "score": 0.015142,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3541,
           "gene": "C15orf39",
           "score": -0.13525,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4111,
           "gene": "ARSK",
           "score": -0.098201,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12405,
           "gene": "BCAN",
           "score": 0.15259,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5063,
           "gene": "ZNF623",
           "score": -0.0068339,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3158,
           "gene": "DCAF8L1",
           "score": -0.011761,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5302,
           "gene": "CRELD1",
           "score": -0.13571,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16905,
           "gene": "TMSB4X",
           "score": 0.13174,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16364,
           "gene": "DTNA",
           "score": 0.17313,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4247,
           "gene": "UBR4",
           "score": -0.13676,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12770,
           "gene": "CTPS1",
           "score": 0.75435,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16716,
           "gene": "SUGCT",
           "score": 0.1954,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8978,
           "gene": "NLGN1",
           "score": 0.053172,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6000,
           "gene": "FRMPD4",
           "score": -0.055871,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12441,
           "gene": "NIM1K",
           "score": 0.18883,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2093,
           "gene": "HNRNPD",
           "score": -0.24775,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1613,
           "gene": "HK3",
           "score": -0.1471,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2016,
           "gene": "GOLGA2",
           "score": -0.11265,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6157,
           "gene": "LOC729159",
           "score": 0.015227,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2023,
           "gene": "FCER2",
           "score": -0.07774,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5471,
           "gene": "PKDCC",
           "score": -0.059766,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9779,
           "gene": "ZMYM3",
           "score": -0.1353,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9089,
           "gene": "CARMIL3",
           "score": -0.009723,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2546,
           "gene": "IARS2",
           "score": -0.053533,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17265,
           "gene": "C10orf82",
           "score": 0.17092,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3410,
           "gene": "HLA-DMA",
           "score": -0.10256,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2015,
           "gene": "ARSF",
           "score": -0.23222,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3111,
           "gene": "PCDHGA2",
           "score": -0.03869,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15128,
           "gene": "MRPL39",
           "score": 0.33297,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10956,
           "gene": "PPM1B",
           "score": 0.19186,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10920,
           "gene": "ZBTB7A",
           "score": -0.0031567,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17483,
           "gene": "VTI1B",
           "score": -0.036043,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14512,
           "gene": "FAM124A",
           "score": 0.042661,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5523,
           "gene": "TMEM86B",
           "score": -0.16725,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4180,
           "gene": "PABPC5",
           "score": -0.12012,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2650,
           "gene": "IFNL2",
           "score": -0.15254,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10570,
           "gene": "HOXB7",
           "score": 0.086387,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1654,
           "gene": "APP",
           "score": -0.11897,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8872,
           "gene": "CERS5",
           "score": -0.0074335,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12171,
           "gene": "TSC2",
           "score": 0.37433,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6155,
           "gene": "PCDHB16",
           "score": -0.21398,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2326,
           "gene": "CHD2",
           "score": -0.042776,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18248,
           "gene": "SLC35G1",
           "score": 0.10571,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3750,
           "gene": "SLC19A3",
           "score": -0.081111,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9830,
           "gene": "TRIM49",
           "score": 0.16044,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16362,
           "gene": "SART3",
           "score": 0.26696,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11957,
           "gene": "RNF217",
           "score": -0.033267,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14355,
           "gene": "EFCAB1",
           "score": -0.023499,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1363,
           "gene": "MRPL20",
           "score": -0.19691,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15644,
           "gene": "CUL4A",
           "score": -0.012886,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13722,
           "gene": "TBCD",
           "score": 0.19745,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2764,
           "gene": "C9",
           "score": -0.07877,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11841,
           "gene": "IZUMO3",
           "score": -0.10881,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4207,
           "gene": "C10orf111",
           "score": -0.029118,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2850,
           "gene": "SLC5A1",
           "score": -0.1587,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5099,
           "gene": "C1orf115",
           "score": -0.11322,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10174,
           "gene": "CCDC175",
           "score": 0.10326,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3605,
           "gene": "UQCR10",
           "score": 0.076353,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17694,
           "gene": "CLDN16",
           "score": -0.078631,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14049,
           "gene": "CDK16",
           "score": 0.13724,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14652,
           "gene": "ASCL2",
           "score": -0.0808,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1252,
           "gene": "PTRH2",
           "score": -0.20475,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4849,
           "gene": "CFAP47",
           "score": 0.039072,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 82,
           "gene": "SIN3B",
           "score": -0.41614,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3499,
           "gene": "GIF",
           "score": 0.074703,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4114,
           "gene": "SDS",
           "score": -0.092917,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4170,
           "gene": "LGR4",
           "score": -0.05853,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 560,
           "gene": "GABARAPL1",
           "score": -0.23303,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11167,
           "gene": "CCDC142",
           "score": -0.11455,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3923,
           "gene": "SLC5A10",
           "score": -0.080302,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17599,
           "gene": "KLHL38",
           "score": -0.0014004,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16469,
           "gene": "POU3F3",
           "score": 0.18901,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8566,
           "gene": "NSL1",
           "score": 0.16991,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15089,
           "gene": "NHLRC4",
           "score": 0.004058,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11245,
           "gene": "EBF2",
           "score": -0.13201,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12756,
           "gene": "XYLT1",
           "score": 0.27896,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2880,
           "gene": "CCL23",
           "score": -0.11632,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1102,
           "gene": "SP3",
           "score": -0.17675,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3073,
           "gene": "OR2AK2",
           "score": -0.16243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6816,
           "gene": "ACE2",
           "score": -0.090405,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13385,
           "gene": "GABRD",
           "score": 0.064745,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6418,
           "gene": "RALGAPA2",
           "score": -0.12151,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13346,
           "gene": "KARS",
           "score": 0.11366,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8611,
           "gene": "DNAJC24",
           "score": 0.092131,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13518,
           "gene": "USMG5",
           "score": -0.023547,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10827,
           "gene": "PRSS42",
           "score": 0.057466,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13164,
           "gene": "DSCC1",
           "score": 0.015806,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11475,
           "gene": "HARS2",
           "score": 0.15363,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1711,
           "gene": "METTL18",
           "score": -0.11573,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6148,
           "gene": "IL37",
           "score": -0.13746,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17772,
           "gene": "C1orf131",
           "score": 0.12026,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5886,
           "gene": "OR5H14",
           "score": -0.037378,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6213,
           "gene": "GPR171",
           "score": -0.041124,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1687,
           "gene": "ZFP36",
           "score": -0.017196,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7724,
           "gene": "RBM11",
           "score": 0.1164,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9925,
           "gene": "AIP",
           "score": -0.021423,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7344,
           "gene": "BICC1",
           "score": 0.024422,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11423,
           "gene": "NET1",
           "score": -0.091153,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6214,
           "gene": "EXOSC10",
           "score": 0.075299,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7162,
           "gene": "SLC25A53",
           "score": -0.043129,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12696,
           "gene": "NRBP1",
           "score": 0.36928,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12873,
           "gene": "KLF15",
           "score": 0.21171,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7440,
           "gene": "KRT72",
           "score": 0.033732,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2003,
           "gene": "MYOM2",
           "score": 0.048418,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15159,
           "gene": "FBXO44",
           "score": 0.16553,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16578,
           "gene": "RASGRP4",
           "score": 0.039352,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2022,
           "gene": "NR1H4",
           "score": 0.089194,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3175,
           "gene": "HIPK3",
           "score": 0.04917,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 896,
           "gene": "FBRSL1",
           "score": -0.20488,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 781,
           "gene": "SSX5",
           "score": -0.2542,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18045,
           "gene": "NISCH",
           "score": 0.095073,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16889,
           "gene": "AGAP9",
           "score": -0.13724,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 13581,
+          "gene": "C1orf158",
+          "score": 0.097043,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17275,
+          "gene": "DTX3",
+          "score": 0.038861,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18005,
+          "gene": "PYCR1",
+          "score": 0.06193,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3887,
+          "gene": "ANKRD1",
+          "score": -0.0057194,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5881,
+          "gene": "ANXA7",
+          "score": -0.026024,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12620,
+          "gene": "IFT57",
+          "score": 0.19312,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7495,
+          "gene": "AGXT",
+          "score": 0.26047,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9633,
+          "gene": "FCRL5",
+          "score": 0.053097,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 962,
+          "gene": "PDCD1",
+          "score": -0.23117,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7479,
+          "gene": "CAVIN1",
+          "score": -0.07357,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18889,
+          "gene": "RPF2",
+          "score": 0.44494,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 290,
+          "gene": "FAM76A",
+          "score": -0.30972,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3336,
+          "gene": "SERPINB11",
+          "score": -0.023671,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5218,
+          "gene": "KLHL31",
+          "score": -0.083264,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17067,
+          "gene": "GHDC",
+          "score": 0.010694,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10076,
+          "gene": "SHOX",
+          "score": 0.05685,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12582,
+          "gene": "LRRC63",
+          "score": 0.11154,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13466,
+          "gene": "ZWILCH",
+          "score": 0.15664,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10840,
+          "gene": "MTRNR2L1",
+          "score": -0.034782,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11909,
+          "gene": "FBXL19",
+          "score": 0.035626,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2446,
+          "gene": "RASSF9",
+          "score": -0.12464,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11263,
+          "gene": "SAMD4A",
+          "score": -0.091046,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9405,
+          "gene": "PICK1",
+          "score": 0.010582,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5297,
+          "gene": "NEMP1",
+          "score": 0.068917,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3733,
+          "gene": "VSIG10L2",
+          "score": 0.038939,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16978,
+          "gene": "MSI1",
+          "score": 0.0062171,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2330,
+          "gene": "SCN11A",
+          "score": -0.22155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3149,
+          "gene": "EGFL7",
+          "score": 0.032839,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8983,
+          "gene": "ISPD",
+          "score": 0.032868,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10486,
+          "gene": "FLOT1",
+          "score": -0.0061212,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3588,
+          "gene": "FAS",
+          "score": -0.16284,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9638,
+          "gene": "ARL13A",
+          "score": -0.12537,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1159,
+          "gene": "ADAM18",
+          "score": -0.028411,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11453,
+          "gene": "BOLA1",
+          "score": -0.00089316,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12830,
+          "gene": "ZNF773",
+          "score": 0.045895,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3192,
+          "gene": "COA6",
+          "score": -0.18267,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15860,
+          "gene": "GRK6",
+          "score": 0.08963,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15822,
+          "gene": "HACD3",
+          "score": 0.1045,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6345,
+          "gene": "GPBP1",
+          "score": -0.090071,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6293,
+          "gene": "ELF4",
+          "score": -0.18139,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4345,
+          "gene": "MACF1",
+          "score": -0.11163,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8608,
+          "gene": "NDUFA13",
+          "score": 0.014495,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8267,
+          "gene": "TSKS",
+          "score": -0.090791,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1635,
+          "gene": "GBA",
+          "score": -0.23715,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1443,
+          "gene": "CHORDC1",
+          "score": -0.0047188,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14537,
+          "gene": "SMIM19",
+          "score": 0.091257,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1256,
+          "gene": "WDR64",
+          "score": -0.046877,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10948,
+          "gene": "EPHX2",
+          "score": 0.22395,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12310,
+          "gene": "IFITM2",
+          "score": 0.11283,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15682,
+          "gene": "VSTM2A",
+          "score": 0.065186,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15111,
+          "gene": "TTC39B",
+          "score": -0.047559,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17995,
+          "gene": "HLA-DPB1",
+          "score": -0.08977,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5025,
+          "gene": "CXCR2",
+          "score": 0.067021,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7781,
+          "gene": "STUB1",
+          "score": -0.067023,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16096,
+          "gene": "SAFB",
+          "score": 0.19949,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15178,
+          "gene": "TCP10L2",
+          "score": 0.19728,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11524,
+          "gene": "SUV39H1",
+          "score": -0.018781,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1449,
+          "gene": "MED6",
+          "score": -0.164,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9267,
+          "gene": "ATP6V1D",
+          "score": -0.031837,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5251,
+          "gene": "WDR88",
+          "score": -0.08229,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 307,
+          "gene": "CEACAM3",
+          "score": 0.097253,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7443,
+          "gene": "TSPO",
+          "score": -0.094768,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 482,
+          "gene": "KCNN4",
+          "score": -0.236,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18510,
+          "gene": "PLCG2",
+          "score": 0.042606,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18085,
+          "gene": "ADH6",
+          "score": 0.10784,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9390,
+          "gene": "LBP",
+          "score": 0.1237,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11882,
+          "gene": "GRINA",
+          "score": -0.14135,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18757,
+          "gene": "WDR3",
+          "score": 0.33659,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6640,
+          "gene": "PDE8B",
+          "score": 0.049945,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13480,
+          "gene": "PRKACA",
+          "score": -0.0045085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3726,
+          "gene": "PRKN",
+          "score": 0.093661,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12025,
+          "gene": "PANX3",
+          "score": 0.10517,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11332,
+          "gene": "RGPD4",
+          "score": 0.08214,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3756,
+          "gene": "G2E3",
+          "score": -0.20105,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7464,
+          "gene": "ORC1",
+          "score": -0.11196,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1970,
+          "gene": "CLEC7A",
+          "score": -0.16276,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14434,
+          "gene": "SCARF2",
+          "score": -0.046342,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1594,
+          "gene": "SULT1B1",
+          "score": -0.19371,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15783,
+          "gene": "LARS2",
+          "score": 0.09608,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4091,
+          "gene": "OR5I1",
+          "score": -0.11676,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4764,
+          "gene": "PYHIN1",
+          "score": -0.04228,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5987,
+          "gene": "ZNF761",
+          "score": -0.079377,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 177,
+          "gene": "SPAG6",
+          "score": -0.19942,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9790,
+          "gene": "ZNF703",
+          "score": -0.1523,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2101,
+          "gene": "SLC24A5",
+          "score": 0.062797,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9069,
+          "gene": "SH2D4A",
+          "score": -0.0058831,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2480,
+          "gene": "NOMO1",
+          "score": -0.0093454,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 222,
+          "gene": "OR14A16",
+          "score": -0.12285,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14500,
+          "gene": "ZNF330",
+          "score": 0.12166,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9134,
+          "gene": "SSTR4",
+          "score": 0.097402,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5953,
+          "gene": "OR13J1",
+          "score": -0.064619,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17433,
+          "gene": "TRIM34",
+          "score": 0.062544,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6429,
+          "gene": "TMEM225B",
+          "score": 0.033022,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2024,
+          "gene": "RHBDL1",
+          "score": -0.030375,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9313,
+          "gene": "LIMD2",
+          "score": -0.026979,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16086,
+          "gene": "SNAI1",
+          "score": -0.061154,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8752,
+          "gene": "CA5A",
+          "score": 0.12589,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2160,
+          "gene": "STARD4",
+          "score": 0.053657,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17053,
+          "gene": "TRIM31",
+          "score": 0.054297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10990,
+          "gene": "PRAMEF14",
+          "score": -0.099496,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18190,
+          "gene": "RPA2",
+          "score": 0.20762,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16235,
+          "gene": "LHB",
+          "score": 0.086577,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2179,
+          "gene": "OR10G4",
+          "score": -0.23147,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9471,
+          "gene": "BCL11A",
+          "score": -0.077921,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16349,
+          "gene": "SNAP23",
+          "score": 0.18266,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9995,
+          "gene": "CSPG4",
+          "score": -0.022444,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13368,
+          "gene": "B3GNT6",
+          "score": 0.047247,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13432,
+          "gene": "TGIF2-C20orf24",
+          "score": 0.14962,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10069,
+          "gene": "SYT17",
+          "score": 0.040779,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18215,
+          "gene": "TUBGCP3",
+          "score": 0.41857,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 14982,
+          "gene": "CLVS2",
+          "score": 0.0028453,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2424,
+          "gene": "BRWD3",
+          "score": -0.2053,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10575,
+          "gene": "OR52L1",
+          "score": 0.054894,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8404,
+          "gene": "B4GALT6",
+          "score": -0.11599,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4399,
+          "gene": "KRT71",
+          "score": 0.12077,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4420,
+          "gene": "PSIP1",
+          "score": 0.021862,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4422,
+          "gene": "LRG1",
+          "score": -0.094189,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2477,
+          "gene": "ENTPD5",
+          "score": -0.050377,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14711,
+          "gene": "NPB",
+          "score": -0.020113,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13196,
+          "gene": "CACNA1D",
+          "score": 0.071356,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11501,
+          "gene": "DACT1",
+          "score": 0.10007,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14772,
+          "gene": "CADM2",
+          "score": -0.081387,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2805,
+          "gene": "NRN1",
+          "score": 0.05283,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9138,
+          "gene": "OR2AE1",
+          "score": -0.038128,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4458,
+          "gene": "YLPM1",
+          "score": -0.029124,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9287,
+          "gene": "MFSD2A",
+          "score": -0.012017,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17758,
+          "gene": "DFFA",
+          "score": 0.24165,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16752,
+          "gene": "BID",
+          "score": 0.14308,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
