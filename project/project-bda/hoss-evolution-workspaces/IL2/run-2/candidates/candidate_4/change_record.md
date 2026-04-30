# Change Record — candidate_4

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IL2/run-2/best/current/harness
Generated at: 2026-04-30T07:07:24.336659

## Files Changed

- model.py: modified (added=10, deleted=0, delta=10)
- outputs/metrics.json: modified (added=2388, deleted=596, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -88,10 +88,20 @@
         # Boost probability for genes with extreme scores (both positive and negative)
         # Hits can be extreme in either direction, so we want to pursue both
         avg_score = stats['sum_score'] / trials
+        max_score = stats['max_score']
+        
+        # Boost based on average score (consistent behavior)
         if avg_score > 0.1:  # Boost genes with positive average scores
             sampled_prob *= (1.0 + avg_score)
         elif avg_score < -0.2:  # Boost genes with strongly negative scores (potential hits)
             sampled_prob *= (1.0 + abs(avg_score))
+        
+        # Additionally boost genes that have shown extreme values (high max_score)
+        # This helps find hits even when the average is moderate
+        if max_score > 0.3:  # Gene has shown strongly positive behavior at least once
+            sampled_prob *= (1.0 + 0.3 * max_score)
+        elif max_score < -0.3:  # Gene has shown strongly negative behavior at least once
+            sampled_prob *= (1.0 + 0.3 * abs(max_score))
         
         gene_sampled_probs[gene] = min(sampled_prob, 1.0)  # Cap at 1.0
     

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18939,
-      "rounds": 3,
+      "rounds": 4,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 256,
-      "baseline_total_hits": 10,
+      "baseline_total_queries": 384,
+      "baseline_total_hits": 13,
       "delta_queries": 128,
-      "delta_hits": 3,
-      "total_queries": 384,
-      "total_hits": 13,
+      "delta_hits": 6,
+      "total_queries": 512,
+      "total_hits": 19,
       "top_k": 654,
       "hit_curve": {
         "queries": [
-          256,
-          384
+          384,
+          512
         ],
         "hits": [
-          10,
-          13
+          13,
+          19
         ]
       },
-      "auc": 1472.0,
-      "auc_normalized": 0.005861365953109072,
-      "ncg": 0.1697223832957915,
+      "auc": 2048.0,
+      "auc_normalized": 0.0061162079510703364,
+      "ncg": 0.19439150821138396,
       "round_details": [
         {
-          "round": 2,
+          "round": 3,
           "selected_count": 128,
-          "hits": 3,
-          "cumulative_hits": 13,
-          "precision_at_batch": 0.0234375,
+          "hits": 6,
+          "cumulative_hits": 19,
+          "precision_at_batch": 0.046875,
           "selected": [
-            "C1orf158",
-            "DTX3",
-            "PYCR1",
-            "ANKRD1",
-            "FAM209B",
-            "IFT57",
-            "AGXT",
-            "FCRL5",
-            "PDCD1",
-            "CAVIN1",
-            "RPF2",
-            "FAM76A",
-            "SERPINB11",
-            "KLHL31",
-            "GHDC",
-            "SHOX",
-            "LRRC63",
-            "ZWILCH",
-            "MTRNR2L1",
-            "FBXL19",
-            "RASSF9",
-            "SAMD4A",
-            "PICK1",
-            "NEMP1",
-            "VSIG10L2",
-            "MSI1",
-            "SCN11A",
-            "EGFL7",
-            "ISPD",
-            "FLOT1",
-            "FAS",
-            "ARL13A",
-            "ADAM18",
-            "MAPKAPK2",
-            "ZNF773",
-            "COA6",
-            "GRK6",
-            "HACD3",
-            "GPBP1",
-            "SIGLEC6",
-            "PGRMC1",
-            "ST13",
-            "FFAR1",
-            "ARHGEF7",
-            "ADIPOR2",
-            "ZNF653",
-            "TMEM139",
-            "ACBD4",
-            "CD300C",
-            "ICMT",
-            "DNER",
-            "CCL28",
-            "GPC1",
-            "OR52N2",
-            "SSBP2",
-            "RAD21",
-            "LRRC4",
-            "OAZ1",
-            "TMEM92",
-            "SLC45A4",
-            "CAPZA1",
-            "NDUFA4L2",
-            "HIST1H4C",
-            "USP19",
-            "SLC30A3",
-            "MLST8",
-            "MASP2",
-            "MAP9",
-            "TOPORS",
-            "GALNT16",
-            "FOXD4L3",
-            "ABCB7",
-            "DEFB114",
-            "C14orf2",
-            "FAM187A",
-            "PITPNA",
-            "NXPE1",
-            "EVI2A",
-            "PROK1",
-            "PDLIM7",
-            "DRAXIN",
-            "PAPOLB",
-            "SPAG6",
-            "LRBA",
-            "MS4A7",
-            "CRABP1",
-            "MRPL24",
-            "OR14A16",
-            "PELI3",
-            "P2RX2",
-            "THOC2",
-            "SLC51A",
-            "IGDCC3",
-            "CLEC19A",
-            "SMARCD1",
-            "ABCC1",
-            "XBP1",
-            "NEK4",
-            "WFDC3",
-            "GNA15",
-            "SLC35B4",
-            "SOCS4",
-            "OR2T27",
-            "TTC7B",
-            "R3HDML",
-            "WNT11",
-            "ETV6",
-            "EML6",
-            "TOX",
-            "BATF",
-            "ZBP1",
-            "OR4C46",
-            "PCID2",
-            "HIST1H4L",
-            "WSCD2",
-            "IGFL4",
-            "MYL6B",
-            "DLL3",
-            "ZC3H7A",
-            "FAAH",
-            "HARS2",
-            "SLC5A6",
-            "ZCCHC6",
-            "ATP6V1C1",
-            "C12orf42",
-            "COX11",
-            "PRPF19",
-            "ACOT11"
+            "ZNF682",
+            "SUGP1",
+            "ADGRB1",
+            "NSMCE1",
+            "PRR21",
+            "ZNF410",
+            "TSPOAP1",
+            "ZXDB",
+            "PCM1",
+            "AKR1C1",
+            "AWAT2",
+            "C17orf67",
+            "CLOCK",
+            "TSPAN17",
+            "KLC3",
+            "CCL24",
+            "ZG16",
+            "PLA2G2C",
+            "PGAM5",
+            "PAPD7",
+            "CBLN2",
+            "LYZL1",
+            "KRTAP10-1",
+            "HLA-A",
+            "HBD",
+            "GNMT",
+            "HEATR9",
+            "AFTPH",
+            "DIO2",
+            "HSDL1",
+            "NPC2",
+            "SDR39U1",
+            "SPINT3",
+            "OR52A5",
+            "MTRNR2L5",
+            "UBE2M",
+            "CD1D",
+            "C2CD6",
+            "IFT27",
+            "CDC23",
+            "PDLIM2",
+            "NPY2R",
+            "LUC7L",
+            "PCNT",
+            "ABCC3",
+            "HIST1H2AI",
+            "ABCB8",
+            "C3orf36",
+            "CHRM1",
+            "DTL",
+            "LRP4",
+            "CCDC7",
+            "PDZRN4",
+            "BANP",
+            "CR2",
+            "EGF",
+            "REST",
+            "DZANK1",
+            "KBTBD11",
+            "MEGF11",
+            "NUCB1",
+            "NUP214",
+            "VWA1",
+            "C4orf33",
+            "QDPR",
+            "LOC100130705",
+            "IARS",
+            "PPM1L",
+            "SLC39A9",
+            "CREBRF",
+            "CHIT1",
+            "FAM133A",
+            "RNF130",
+            "RNF146",
+            "TOMM22",
+            "DMP1",
+            "NLRP3",
+            "ASB14",
+            "FLVCR2",
+            "FOXA2",
+            "PPM1M",
+            "MRGPRE",
+            "TAOK2",
+            "CD40LG",
+            "CCDC102A",
+            "RABL6",
+            "UNC93B1",
+            "NIPSNAP1",
+            "PEX6",
+            "BEGAIN",
+            "ARHGEF6",
+            "C11orf16",
+            "ADGRL4",
+            "MT1M",
+            "BARX1",
+            "TMEM134",
+            "BTD",
+            "SELENBP1",
+            "SPRY4",
+            "OR2AK2",
+            "ARHGAP17",
+            "RNASE7",
+            "SIGLEC14",
+            "AQP12A",
+            "ACTN1",
+            "POLG2",
+            "MRPS15",
+            "ZFP57",
+            "NDUFB10",
+            "GPR89A",
+            "ZNF324B",
+            "ZIM3",
+            "PAM16",
+            "ZNF513",
+            "CHRNA4",
+            "BSPH1",
+            "LIPC",
+            "FAM183A",
+            "EPO",
+            "HEPHL1",
+            "BCAP31",
+            "BIRC2",
+            "NUP210L",
+            "POMP",
+            "CLTC",
+            "PTPRC",
+            "OR7C1",
+            "PCYT2"
           ],
           "selected_scores": [
-            0.097043,
-            0.038861,
-            0.06193,
-            -0.0057194,
-            -0.082289,
-            0.19312,
-            0.26047,
-            0.053097,
-            -0.23117,
-            -0.07357,
-            0.44494,
-            -0.30972,
-            -0.023671,
-            -0.083264,
-            0.010694,
-            0.05685,
-            0.11154,
-            0.15664,
-            -0.034782,
-            0.035626,
-            -0.12464,
-            -0.091046,
-            0.010582,
-            0.068917,
-            0.038939,
-            0.0062171,
-            -0.22155,
-            0.032839,
-            0.032868,
-            -0.0061212,
-            -0.16284,
-            -0.12537,
-            -0.028411,
-            0.19245,
-            0.045895,
-            -0.18267,
-            0.08963,
-            0.1045,
-            -0.090071,
-            -0.045845,
-            0.079825,
-            -0.04562,
-            0.069572,
-            -0.1306,
-            0.080924,
-            0.1237,
-            -0.12916,
-            0.082714,
-            -0.039319,
-            0.14553,
-            0.080505,
-            0.11867,
-            0.11686,
-            -0.11302,
-            0.0092768,
-            0.080238,
-            0.0091324,
-            -0.2093,
-            -0.13056,
-            -0.050475,
-            -0.17333,
-            -0.15782,
-            -0.21326,
-            -0.046145,
-            -0.063142,
-            -0.15324,
-            -0.008059,
-            0.12728,
-            -0.060971,
-            -0.14829,
-            -0.15181,
-            0.10038,
-            -0.090918,
-            -0.11477,
-            -0.031775,
-            -0.17168,
-            -0.061962,
-            -0.058831,
-            0.25729,
-            -0.134,
-            -0.17434,
-            0.080265,
-            -0.19942,
-            -0.14092,
-            -0.010499,
-            0.096255,
-            -0.17216,
-            -0.12285,
-            -0.03983,
-            -0.081321,
-            0.24104,
-            0.10035,
-            -0.15193,
-            -0.11868,
-            0.082628,
-            0.071233,
-            -0.17879,
-            -0.11655,
-            -0.056472,
-            -0.055715,
-            0.0041306,
-            0.073544,
-            -0.096019,
-            0.14533,
-            0.11373,
-            -0.066327,
-            0.041669,
-            0.0025375,
-            0.029981,
-            0.42521,
-            0.0070346,
-            -0.15106,
-            0.13588,
-            0.14993,
-            0.095297,
-            -0.18012,
-            -0.090291,
-            -0.10726,
-            -0.042454,
-            0.018843,
-            0.15363,
-            -0.02445,
-            -0.02287,
-            -0.052995,
-            -0.1366,
-            -0.0027798,
-            0.38417,
-            0.11124
+            -0.066292,
+            -0.10537,
+            -0.016333,
+            0.10446,
+            -0.045793,
+            -0.10611,
+            -0.023655,
+            -0.22122,
+            -0.14485,
+            -0.024633,
+            -0.20968,
+            -0.0018348,
+            -0.0871,
+            0.32379,
+            0.022576,
+            -0.0052071,
+            -0.19057,
+            0.15158,
+            0.17435,
+            0.16202,
+            0.039316,
+            -0.026279,
+            -0.13763,
+            0.03841,
+            -0.11022,
+            0.021289,
+            -0.11612,
+            -0.23038,
+            0.21103,
+            -0.08225,
+            0.071884,
+            -0.049585,
+            -0.092487,
+            -0.010455,
+            -0.060609,
+            -0.25676,
+            -0.1676,
+            0.029571,
+            0.049569,
+            0.75313,
+            0.16687,
+            0.020643,
+            0.02102,
+            0.27061,
+            0.10402,
+            -0.093945,
+            -0.05807,
+            -0.17073,
+            -0.038634,
+            0.062116,
+            0.041176,
+            0.035182,
+            0.030132,
+            -0.14328,
+            0.29724,
+            0.16804,
+            0.06455,
+            -0.15082,
+            0.037302,
+            0.077542,
+            -0.14142,
+            0.16475,
+            0.093404,
+            -0.24117,
+            0.089388,
+            -0.2275,
+            0.21769,
+            0.097688,
+            -0.019225,
+            0.067736,
+            -0.10366,
+            -0.13119,
+            -0.14976,
+            -0.33644,
+            -0.050375,
+            -0.16108,
+            0.20612,
+            -0.029937,
+            0.11643,
+            -0.06962,
+            0.066489,
+            0.069416,
+            0.08395,
+            -0.022008,
+            -0.1765,
+            -0.071797,
+            0.1316,
+            0.17017,
+            -0.24127,
+            0.37792,
+            -0.23752,
+            -0.072414,
+            -0.035615,
+            -0.057575,
+            0.082774,
+            -0.089285,
+            -0.1237,
+            -0.10742,
+            -0.196,
+            -0.16243,
+            0.10559,
+            -0.1516,
+            -0.036235,
+            -0.14952,
+            0.055767,
+            0.2274,
+            0.14946,
+            -0.035847,
+            0.27002,
+            -0.089878,
+            0.051283,
+            0.049688,
+            0.19394,
+            0.050747,
+            -0.039819,
+            -0.027673,
+            0.0011676,
+            0.085677,
+            -0.017593,
+            0.083083,
+            0.0062327,
+            0.027505,
+            -0.10562,
+            0.47385,
+            0.25547,
+            -0.86005,
+            0.084699,
+            -0.32403
           ],
           "selected_hits": [
             0,
@@ -311,6 +311,35 @@
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
             1,
             0,
             0,
@@ -345,71 +374,6 @@
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
@@ -426,9 +390,45 @@
             0,
             0,
             0,
-            0,
             1,
-            0
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
+            1,
+            0,
+            1
           ]
         }
       ],
@@ -2230,896 +2230,1792 @@
           "gene": "C1orf158",
           "score": 0.097043,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17275,
           "gene": "DTX3",
           "score": 0.038861,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18005,
           "gene": "PYCR1",
           "score": 0.06193,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3887,
           "gene": "ANKRD1",
           "score": -0.0057194,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5882,
           "gene": "FAM209B",
           "score": -0.082289,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12620,
           "gene": "IFT57",
           "score": 0.19312,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7495,
           "gene": "AGXT",
           "score": 0.26047,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9633,
           "gene": "FCRL5",
           "score": 0.053097,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 962,
           "gene": "PDCD1",
           "score": -0.23117,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7479,
           "gene": "CAVIN1",
           "score": -0.07357,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18889,
           "gene": "RPF2",
           "score": 0.44494,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 290,
           "gene": "FAM76A",
           "score": -0.30972,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3336,
           "gene": "SERPINB11",
           "score": -0.023671,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5218,
           "gene": "KLHL31",
           "score": -0.083264,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17067,
           "gene": "GHDC",
           "score": 0.010694,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10076,
           "gene": "SHOX",
           "score": 0.05685,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12582,
           "gene": "LRRC63",
           "score": 0.11154,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13466,
           "gene": "ZWILCH",
           "score": 0.15664,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10840,
           "gene": "MTRNR2L1",
           "score": -0.034782,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11909,
           "gene": "FBXL19",
           "score": 0.035626,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2446,
           "gene": "RASSF9",
           "score": -0.12464,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11263,
           "gene": "SAMD4A",
           "score": -0.091046,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9405,
           "gene": "PICK1",
           "score": 0.010582,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5297,
           "gene": "NEMP1",
           "score": 0.068917,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3733,
           "gene": "VSIG10L2",
           "score": 0.038939,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16978,
           "gene": "MSI1",
           "score": 0.0062171,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2330,
           "gene": "SCN11A",
           "score": -0.22155,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3149,
           "gene": "EGFL7",
           "score": 0.032839,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8983,
           "gene": "ISPD",
           "score": 0.032868,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10486,
           "gene": "FLOT1",
           "score": -0.0061212,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3588,
           "gene": "FAS",
           "score": -0.16284,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9638,
           "gene": "ARL13A",
           "score": -0.12537,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1159,
           "gene": "ADAM18",
           "score": -0.028411,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11454,
           "gene": "MAPKAPK2",
           "score": 0.19245,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12830,
           "gene": "ZNF773",
           "score": 0.045895,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3192,
           "gene": "COA6",
           "score": -0.18267,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15860,
           "gene": "GRK6",
           "score": 0.08963,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15822,
           "gene": "HACD3",
           "score": 0.1045,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6345,
           "gene": "GPBP1",
           "score": -0.090071,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6279,
           "gene": "SIGLEC6",
           "score": -0.045845,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4334,
           "gene": "PGRMC1",
           "score": 0.079825,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8592,
           "gene": "ST13",
           "score": -0.04562,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8250,
           "gene": "FFAR1",
           "score": 0.069572,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1632,
           "gene": "ARHGEF7",
           "score": -0.1306,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1440,
           "gene": "ADIPOR2",
           "score": 0.080924,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14505,
           "gene": "ZNF653",
           "score": 0.1237,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1253,
           "gene": "TMEM139",
           "score": -0.12916,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10924,
           "gene": "ACBD4",
           "score": 0.082714,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12282,
           "gene": "CD300C",
           "score": -0.039319,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15650,
           "gene": "ICMT",
           "score": 0.14553,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15079,
           "gene": "DNER",
           "score": 0.080505,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17958,
           "gene": "CCL28",
           "score": 0.11867,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5014,
           "gene": "GPC1",
           "score": 0.11686,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7764,
           "gene": "OR52N2",
           "score": -0.11302,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16062,
           "gene": "SSBP2",
           "score": 0.0092768,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15145,
           "gene": "RAD21",
           "score": 0.080238,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11498,
           "gene": "LRRC4",
           "score": 0.0091324,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1446,
           "gene": "OAZ1",
           "score": -0.2093,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9249,
           "gene": "TMEM92",
           "score": -0.13056,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5238,
           "gene": "SLC45A4",
           "score": -0.050475,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 306,
           "gene": "CAPZA1",
           "score": -0.17333,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7428,
           "gene": "NDUFA4L2",
           "score": -0.15782,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 481,
           "gene": "HIST1H4C",
           "score": -0.21326,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18472,
           "gene": "USP19",
           "score": -0.046145,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18047,
           "gene": "SLC30A3",
           "score": -0.063142,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9372,
           "gene": "MLST8",
           "score": -0.15324,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11855,
           "gene": "MASP2",
           "score": -0.008059,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18719,
           "gene": "MAP9",
           "score": 0.12728,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6625,
           "gene": "TOPORS",
           "score": -0.060971,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13449,
           "gene": "GALNT16",
           "score": -0.14829,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3717,
           "gene": "FOXD4L3",
           "score": -0.15181,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11998,
           "gene": "ABCB7",
           "score": 0.10038,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11307,
           "gene": "DEFB114",
           "score": -0.090918,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3745,
           "gene": "C14orf2",
           "score": -0.11477,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7449,
           "gene": "FAM187A",
           "score": -0.031775,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1967,
           "gene": "PITPNA",
           "score": -0.17168,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14402,
           "gene": "NXPE1",
           "score": -0.061962,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1591,
           "gene": "EVI2A",
           "score": -0.058831,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15751,
           "gene": "PROK1",
           "score": 0.25729,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4079,
           "gene": "PDLIM7",
           "score": -0.134,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4753,
           "gene": "DRAXIN",
           "score": -0.17434,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5973,
           "gene": "PAPOLB",
           "score": 0.080265,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 177,
           "gene": "SPAG6",
           "score": -0.19942,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9768,
           "gene": "LRBA",
           "score": -0.14092,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2098,
           "gene": "MS4A7",
           "score": -0.010499,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9051,
           "gene": "CRABP1",
           "score": 0.096255,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2475,
           "gene": "MRPL24",
           "score": -0.17216,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 222,
           "gene": "OR14A16",
           "score": -0.12285,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14468,
           "gene": "PELI3",
           "score": -0.03983,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9116,
           "gene": "P2RX2",
           "score": -0.081321,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5939,
           "gene": "THOC2",
           "score": 0.24104,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17396,
           "gene": "SLC51A",
           "score": 0.10035,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6414,
           "gene": "IGDCC3",
           "score": -0.15193,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2020,
           "gene": "CLEC19A",
           "score": -0.11868,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9295,
           "gene": "SMARCD1",
           "score": 0.082628,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16052,
           "gene": "ABCC1",
           "score": 0.071233,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8733,
           "gene": "XBP1",
           "score": -0.17879,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2157,
           "gene": "NEK4",
           "score": -0.11655,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17018,
           "gene": "WFDC3",
           "score": -0.056472,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10966,
           "gene": "GNA15",
           "score": -0.055715,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18152,
           "gene": "SLC35B4",
           "score": 0.0041306,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16201,
           "gene": "SOCS4",
           "score": 0.073544,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2176,
           "gene": "OR2T27",
           "score": -0.096019,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9452,
           "gene": "TTC7B",
           "score": 0.14533,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16315,
           "gene": "R3HDML",
           "score": 0.11373,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9974,
           "gene": "WNT11",
           "score": -0.066327,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13338,
           "gene": "ETV6",
           "score": 0.041669,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13402,
           "gene": "EML6",
           "score": 0.0025375,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10048,
           "gene": "TOX",
           "score": 0.029981,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18177,
           "gene": "BATF",
           "score": 0.42521,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14949,
           "gene": "ZBP1",
           "score": 0.0070346,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2420,
           "gene": "OR4C46",
           "score": -0.15106,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10552,
           "gene": "PCID2",
           "score": 0.13588,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8387,
           "gene": "HIST1H4L",
           "score": 0.14993,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4388,
           "gene": "WSCD2",
           "score": 0.095297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4409,
           "gene": "IGFL4",
           "score": -0.18012,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4411,
           "gene": "MYL6B",
           "score": -0.090291,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2472,
           "gene": "DLL3",
           "score": -0.10726,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14679,
           "gene": "ZC3H7A",
           "score": -0.042454,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13166,
           "gene": "FAAH",
           "score": 0.018843,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11475,
           "gene": "HARS2",
           "score": 0.15363,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14740,
           "gene": "SLC5A6",
           "score": -0.02445,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2800,
           "gene": "ZCCHC6",
           "score": -0.02287,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9120,
           "gene": "ATP6V1C1",
           "score": -0.052995,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4447,
           "gene": "C12orf42",
           "score": -0.1366,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9269,
           "gene": "COX11",
           "score": -0.0027798,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17721,
           "gene": "PRPF19",
           "score": 0.38417,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16718,
           "gene": "ACOT11",
           "score": 0.11124,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 9107,
+          "gene": "ZNF682",
+          "score": -0.066292,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13983,
+          "gene": "SUGP1",
+          "score": -0.10537,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16326,
+          "gene": "ADGRB1",
+          "score": -0.016333,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8628,
+          "gene": "NSMCE1",
+          "score": 0.10446,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2745,
+          "gene": "PRR21",
+          "score": -0.045793,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10157,
+          "gene": "ZNF410",
+          "score": -0.10611,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11342,
+          "gene": "TSPOAP1",
+          "score": -0.023655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 717,
+          "gene": "ZXDB",
+          "score": -0.22122,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2425,
+          "gene": "PCM1",
+          "score": -0.14485,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16202,
+          "gene": "AKR1C1",
+          "score": -0.024633,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 367,
+          "gene": "AWAT2",
+          "score": -0.20968,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3858,
+          "gene": "C17orf67",
+          "score": -0.0018348,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9512,
+          "gene": "CLOCK",
+          "score": -0.0871,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3954,
+          "gene": "TSPAN17",
+          "score": 0.32379,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10417,
+          "gene": "KLC3",
+          "score": 0.022576,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1191,
+          "gene": "CCL24",
+          "score": -0.0052071,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2233,
+          "gene": "ZG16",
+          "score": -0.19057,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4535,
+          "gene": "PLA2G2C",
+          "score": 0.15158,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9097,
+          "gene": "PGAM5",
+          "score": 0.17435,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5172,
+          "gene": "PAPD7",
+          "score": 0.16202,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7071,
+          "gene": "CBLN2",
+          "score": 0.039316,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14340,
+          "gene": "LYZL1",
+          "score": -0.026279,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2514,
+          "gene": "KRTAP10-1",
+          "score": -0.13763,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13665,
+          "gene": "HLA-A",
+          "score": 0.03841,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4795,
+          "gene": "HBD",
+          "score": -0.11022,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1911,
+          "gene": "GNMT",
+          "score": 0.021289,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1072,
+          "gene": "HEATR9",
+          "score": -0.11612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5777,
+          "gene": "AFTPH",
+          "score": -0.23038,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10736,
+          "gene": "DIO2",
+          "score": 0.21103,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8434,
+          "gene": "HSDL1",
+          "score": -0.08225,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11939,
+          "gene": "NPC2",
+          "score": 0.071884,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10715,
+          "gene": "SDR39U1",
+          "score": -0.049585,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3144,
+          "gene": "SPINT3",
+          "score": -0.092487,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13774,
+          "gene": "OR52A5",
+          "score": -0.010455,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3011,
+          "gene": "MTRNR2L5",
+          "score": -0.060609,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 705,
+          "gene": "UBE2M",
+          "score": -0.25676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10999,
+          "gene": "CD1D",
+          "score": -0.1676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10615,
+          "gene": "C2CD6",
+          "score": 0.029571,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12951,
+          "gene": "IFT27",
+          "score": 0.049569,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17752,
+          "gene": "CDC23",
+          "score": 0.75313,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17959,
+          "gene": "PDLIM2",
+          "score": 0.16687,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8513,
+          "gene": "NPY2R",
+          "score": 0.020643,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2000,
+          "gene": "LUC7L",
+          "score": 0.02102,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16484,
+          "gene": "PCNT",
+          "score": 0.27061,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12514,
+          "gene": "ABCC3",
+          "score": 0.10402,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7026,
+          "gene": "HIST1H2AI",
+          "score": -0.093945,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11761,
+          "gene": "ABCB8",
+          "score": -0.05807,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5235,
+          "gene": "C3orf36",
+          "score": -0.17073,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 562,
+          "gene": "CHRM1",
+          "score": -0.038634,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8361,
+          "gene": "DTL",
+          "score": 0.062116,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16727,
+          "gene": "LRP4",
+          "score": 0.041176,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14193,
+          "gene": "CCDC7",
+          "score": 0.035182,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9844,
+          "gene": "PDZRN4",
+          "score": 0.030132,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7034,
+          "gene": "BANP",
+          "score": -0.14328,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13879,
+          "gene": "CR2",
+          "score": 0.29724,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12898,
+          "gene": "EGF",
+          "score": 0.16804,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12726,
+          "gene": "REST",
+          "score": 0.06455,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4816,
+          "gene": "DZANK1",
+          "score": -0.15082,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15247,
+          "gene": "KBTBD11",
+          "score": 0.037302,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18545,
+          "gene": "MEGF11",
+          "score": 0.077542,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2897,
+          "gene": "NUCB1",
+          "score": -0.14142,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18736,
+          "gene": "NUP214",
+          "score": 0.16475,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12874,
+          "gene": "VWA1",
+          "score": 0.093404,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2070,
+          "gene": "C4orf33",
+          "score": -0.24117,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17232,
+          "gene": "QDPR",
+          "score": 0.089388,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 965,
+          "gene": "LOC100130705",
+          "score": -0.2275,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18175,
+          "gene": "IARS",
+          "score": 0.21769,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17412,
+          "gene": "PPM1L",
+          "score": 0.097688,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9667,
+          "gene": "SLC39A9",
+          "score": -0.019225,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10657,
+          "gene": "CREBRF",
+          "score": 0.067736,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10080,
+          "gene": "CHIT1",
+          "score": -0.10366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5643,
+          "gene": "FAM133A",
+          "score": -0.13119,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6133,
+          "gene": "RNF130",
+          "score": -0.14976,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 334,
+          "gene": "RNF146",
+          "score": -0.33644,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 9365,
+          "gene": "TOMM22",
+          "score": -0.050375,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1663,
+          "gene": "DMP1",
+          "score": -0.16108,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13435,
+          "gene": "NLRP3",
+          "score": 0.20612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3449,
+          "gene": "ASB14",
+          "score": -0.029937,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 97,
+          "gene": "FLVCR2",
+          "score": 0.11643,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12128,
+          "gene": "FOXA2",
+          "score": -0.06962,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9327,
+          "gene": "PPM1M",
+          "score": 0.066489,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15230,
+          "gene": "MRGPRE",
+          "score": 0.069416,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14698,
+          "gene": "TAOK2",
+          "score": 0.08395,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6721,
+          "gene": "CD40LG",
+          "score": -0.022008,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11027,
+          "gene": "CCDC102A",
+          "score": -0.1765,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9067,
+          "gene": "RABL6",
+          "score": -0.071797,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8118,
+          "gene": "UNC93B1",
+          "score": 0.1316,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17347,
+          "gene": "NIPSNAP1",
+          "score": 0.17017,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7546,
+          "gene": "PEX6",
+          "score": -0.24127,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16520,
+          "gene": "BEGAIN",
+          "score": 0.37792,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 920,
+          "gene": "ARHGEF6",
+          "score": -0.23752,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4988,
+          "gene": "C11orf16",
+          "score": -0.072414,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 753,
+          "gene": "ADGRL4",
+          "score": -0.035615,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8798,
+          "gene": "MT1M",
+          "score": -0.057575,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16045,
+          "gene": "BARX1",
+          "score": 0.082774,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3193,
+          "gene": "TMEM134",
+          "score": -0.089285,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5864,
+          "gene": "BTD",
+          "score": -0.1237,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7184,
+          "gene": "SELENBP1",
+          "score": -0.10742,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2112,
+          "gene": "SPRY4",
+          "score": -0.196,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3073,
+          "gene": "OR2AK2",
+          "score": -0.16243,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2167,
+          "gene": "ARHGAP17",
+          "score": 0.10559,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4443,
+          "gene": "RNASE7",
+          "score": -0.1516,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13133,
+          "gene": "SIGLEC14",
+          "score": -0.036235,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5495,
+          "gene": "AQP12A",
+          "score": -0.14952,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2773,
+          "gene": "ACTN1",
+          "score": 0.055767,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14954,
+          "gene": "POLG2",
+          "score": 0.2274,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13023,
+          "gene": "MRPS15",
+          "score": 0.14946,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9294,
+          "gene": "ZFP57",
+          "score": -0.035847,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12799,
+          "gene": "NDUFB10",
+          "score": 0.27002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13470,
+          "gene": "GPR89A",
+          "score": -0.089878,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12632,
+          "gene": "ZNF324B",
+          "score": 0.051283,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5467,
+          "gene": "ZIM3",
+          "score": 0.049688,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17579,
+          "gene": "PAM16",
+          "score": 0.19394,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1001,
+          "gene": "ZNF513",
+          "score": 0.050747,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2422,
+          "gene": "CHRNA4",
+          "score": -0.039819,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10751,
+          "gene": "BSPH1",
+          "score": -0.027673,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13891,
+          "gene": "LIPC",
+          "score": 0.0011676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7844,
+          "gene": "FAM183A",
+          "score": 0.085677,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10759,
+          "gene": "EPO",
+          "score": -0.017593,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12200,
+          "gene": "HEPHL1",
+          "score": 0.083083,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14657,
+          "gene": "BCAP31",
+          "score": 0.0062327,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7233,
+          "gene": "BIRC2",
+          "score": 0.027505,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13118,
+          "gene": "NUP210L",
+          "score": -0.10562,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17403,
+          "gene": "POMP",
+          "score": 0.47385,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18021,
+          "gene": "CLTC",
+          "score": 0.25547,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 35,
+          "gene": "PTPRC",
+          "score": -0.86005,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 13817,
+          "gene": "OR7C1",
+          "score": 0.084699,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1112,
+          "gene": "PCYT2",
+          "score": -0.32403,
+          "hit": 1,
+          "round": 3
         }
       ],
       "queried_history": [
@@ -4920,896 +5816,1792 @@
           "gene": "C1orf158",
           "score": 0.097043,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17275,
           "gene": "DTX3",
           "score": 0.038861,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18005,
           "gene": "PYCR1",
           "score": 0.06193,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3887,
           "gene": "ANKRD1",
           "score": -0.0057194,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5882,
           "gene": "FAM209B",
           "score": -0.082289,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12620,
           "gene": "IFT57",
           "score": 0.19312,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7495,
           "gene": "AGXT",
           "score": 0.26047,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9633,
           "gene": "FCRL5",
           "score": 0.053097,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 962,
           "gene": "PDCD1",
           "score": -0.23117,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7479,
           "gene": "CAVIN1",
           "score": -0.07357,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18889,
           "gene": "RPF2",
           "score": 0.44494,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 290,
           "gene": "FAM76A",
           "score": -0.30972,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3336,
           "gene": "SERPINB11",
           "score": -0.023671,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5218,
           "gene": "KLHL31",
           "score": -0.083264,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17067,
           "gene": "GHDC",
           "score": 0.010694,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10076,
           "gene": "SHOX",
           "score": 0.05685,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12582,
           "gene": "LRRC63",
           "score": 0.11154,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13466,
           "gene": "ZWILCH",
           "score": 0.15664,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10840,
           "gene": "MTRNR2L1",
           "score": -0.034782,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11909,
           "gene": "FBXL19",
           "score": 0.035626,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2446,
           "gene": "RASSF9",
           "score": -0.12464,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11263,
           "gene": "SAMD4A",
           "score": -0.091046,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9405,
           "gene": "PICK1",
           "score": 0.010582,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5297,
           "gene": "NEMP1",
           "score": 0.068917,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3733,
           "gene": "VSIG10L2",
           "score": 0.038939,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16978,
           "gene": "MSI1",
           "score": 0.0062171,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2330,
           "gene": "SCN11A",
           "score": -0.22155,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3149,
           "gene": "EGFL7",
           "score": 0.032839,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8983,
           "gene": "ISPD",
           "score": 0.032868,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10486,
           "gene": "FLOT1",
           "score": -0.0061212,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3588,
           "gene": "FAS",
           "score": -0.16284,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9638,
           "gene": "ARL13A",
           "score": -0.12537,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1159,
           "gene": "ADAM18",
           "score": -0.028411,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11454,
           "gene": "MAPKAPK2",
           "score": 0.19245,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12830,
           "gene": "ZNF773",
           "score": 0.045895,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3192,
           "gene": "COA6",
           "score": -0.18267,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15860,
           "gene": "GRK6",
           "score": 0.08963,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15822,
           "gene": "HACD3",
           "score": 0.1045,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6345,
           "gene": "GPBP1",
           "score": -0.090071,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6279,
           "gene": "SIGLEC6",
           "score": -0.045845,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4334,
           "gene": "PGRMC1",
           "score": 0.079825,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8592,
           "gene": "ST13",
           "score": -0.04562,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8250,
           "gene": "FFAR1",
           "score": 0.069572,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1632,
           "gene": "ARHGEF7",
           "score": -0.1306,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1440,
           "gene": "ADIPOR2",
           "score": 0.080924,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14505,
           "gene": "ZNF653",
           "score": 0.1237,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1253,
           "gene": "TMEM139",
           "score": -0.12916,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10924,
           "gene": "ACBD4",
           "score": 0.082714,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12282,
           "gene": "CD300C",
           "score": -0.039319,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15650,
           "gene": "ICMT",
           "score": 0.14553,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15079,
           "gene": "DNER",
           "score": 0.080505,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17958,
           "gene": "CCL28",
           "score": 0.11867,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5014,
           "gene": "GPC1",
           "score": 0.11686,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7764,
           "gene": "OR52N2",
           "score": -0.11302,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16062,
           "gene": "SSBP2",
           "score": 0.0092768,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15145,
           "gene": "RAD21",
           "score": 0.080238,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11498,
           "gene": "LRRC4",
           "score": 0.0091324,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1446,
           "gene": "OAZ1",
           "score": -0.2093,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9249,
           "gene": "TMEM92",
           "score": -0.13056,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5238,
           "gene": "SLC45A4",
           "score": -0.050475,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 306,
           "gene": "CAPZA1",
           "score": -0.17333,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7428,
           "gene": "NDUFA4L2",
           "score": -0.15782,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 481,
           "gene": "HIST1H4C",
           "score": -0.21326,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18472,
           "gene": "USP19",
           "score": -0.046145,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18047,
           "gene": "SLC30A3",
           "score": -0.063142,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9372,
           "gene": "MLST8",
           "score": -0.15324,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11855,
           "gene": "MASP2",
           "score": -0.008059,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18719,
           "gene": "MAP9",
           "score": 0.12728,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6625,
           "gene": "TOPORS",
           "score": -0.060971,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13449,
           "gene": "GALNT16",
           "score": -0.14829,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3717,
           "gene": "FOXD4L3",
           "score": -0.15181,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11998,
           "gene": "ABCB7",
           "score": 0.10038,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11307,
           "gene": "DEFB114",
           "score": -0.090918,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3745,
           "gene": "C14orf2",
           "score": -0.11477,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7449,
           "gene": "FAM187A",
           "score": -0.031775,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1967,
           "gene": "PITPNA",
           "score": -0.17168,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14402,
           "gene": "NXPE1",
           "score": -0.061962,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1591,
           "gene": "EVI2A",
           "score": -0.058831,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15751,
           "gene": "PROK1",
           "score": 0.25729,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4079,
           "gene": "PDLIM7",
           "score": -0.134,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4753,
           "gene": "DRAXIN",
           "score": -0.17434,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5973,
           "gene": "PAPOLB",
           "score": 0.080265,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 177,
           "gene": "SPAG6",
           "score": -0.19942,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9768,
           "gene": "LRBA",
           "score": -0.14092,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2098,
           "gene": "MS4A7",
           "score": -0.010499,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9051,
           "gene": "CRABP1",
           "score": 0.096255,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2475,
           "gene": "MRPL24",
           "score": -0.17216,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 222,
           "gene": "OR14A16",
           "score": -0.12285,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14468,
           "gene": "PELI3",
           "score": -0.03983,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9116,
           "gene": "P2RX2",
           "score": -0.081321,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5939,
           "gene": "THOC2",
           "score": 0.24104,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17396,
           "gene": "SLC51A",
           "score": 0.10035,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6414,
           "gene": "IGDCC3",
           "score": -0.15193,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2020,
           "gene": "CLEC19A",
           "score": -0.11868,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9295,
           "gene": "SMARCD1",
           "score": 0.082628,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16052,
           "gene": "ABCC1",
           "score": 0.071233,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8733,
           "gene": "XBP1",
           "score": -0.17879,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2157,
           "gene": "NEK4",
           "score": -0.11655,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17018,
           "gene": "WFDC3",
           "score": -0.056472,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10966,
           "gene": "GNA15",
           "score": -0.055715,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18152,
           "gene": "SLC35B4",
           "score": 0.0041306,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16201,
           "gene": "SOCS4",
           "score": 0.073544,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2176,
           "gene": "OR2T27",
           "score": -0.096019,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9452,
           "gene": "TTC7B",
           "score": 0.14533,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16315,
           "gene": "R3HDML",
           "score": 0.11373,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9974,
           "gene": "WNT11",
           "score": -0.066327,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13338,
           "gene": "ETV6",
           "score": 0.041669,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13402,
           "gene": "EML6",
           "score": 0.0025375,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10048,
           "gene": "TOX",
           "score": 0.029981,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18177,
           "gene": "BATF",
           "score": 0.42521,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14949,
           "gene": "ZBP1",
           "score": 0.0070346,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2420,
           "gene": "OR4C46",
           "score": -0.15106,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10552,
           "gene": "PCID2",
           "score": 0.13588,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8387,
           "gene": "HIST1H4L",
           "score": 0.14993,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4388,
           "gene": "WSCD2",
           "score": 0.095297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4409,
           "gene": "IGFL4",
           "score": -0.18012,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4411,
           "gene": "MYL6B",
           "score": -0.090291,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2472,
           "gene": "DLL3",
           "score": -0.10726,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14679,
           "gene": "ZC3H7A",
           "score": -0.042454,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13166,
           "gene": "FAAH",
           "score": 0.018843,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11475,
           "gene": "HARS2",
           "score": 0.15363,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14740,
           "gene": "SLC5A6",
           "score": -0.02445,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2800,
           "gene": "ZCCHC6",
           "score": -0.02287,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9120,
           "gene": "ATP6V1C1",
           "score": -0.052995,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4447,
           "gene": "C12orf42",
           "score": -0.1366,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9269,
           "gene": "COX11",
           "score": -0.0027798,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17721,
           "gene": "PRPF19",
           "score": 0.38417,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16718,
           "gene": "ACOT11",
           "score": 0.11124,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 9107,
+          "gene": "ZNF682",
+          "score": -0.066292,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13983,
+          "gene": "SUGP1",
+          "score": -0.10537,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16326,
+          "gene": "ADGRB1",
+          "score": -0.016333,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8628,
+          "gene": "NSMCE1",
+          "score": 0.10446,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2745,
+          "gene": "PRR21",
+          "score": -0.045793,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10157,
+          "gene": "ZNF410",
+          "score": -0.10611,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11342,
+          "gene": "TSPOAP1",
+          "score": -0.023655,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 717,
+          "gene": "ZXDB",
+          "score": -0.22122,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2425,
+          "gene": "PCM1",
+          "score": -0.14485,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16202,
+          "gene": "AKR1C1",
+          "score": -0.024633,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 367,
+          "gene": "AWAT2",
+          "score": -0.20968,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3858,
+          "gene": "C17orf67",
+          "score": -0.0018348,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9512,
+          "gene": "CLOCK",
+          "score": -0.0871,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3954,
+          "gene": "TSPAN17",
+          "score": 0.32379,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10417,
+          "gene": "KLC3",
+          "score": 0.022576,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1191,
+          "gene": "CCL24",
+          "score": -0.0052071,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2233,
+          "gene": "ZG16",
+          "score": -0.19057,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4535,
+          "gene": "PLA2G2C",
+          "score": 0.15158,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9097,
+          "gene": "PGAM5",
+          "score": 0.17435,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5172,
+          "gene": "PAPD7",
+          "score": 0.16202,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7071,
+          "gene": "CBLN2",
+          "score": 0.039316,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14340,
+          "gene": "LYZL1",
+          "score": -0.026279,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2514,
+          "gene": "KRTAP10-1",
+          "score": -0.13763,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13665,
+          "gene": "HLA-A",
+          "score": 0.03841,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4795,
+          "gene": "HBD",
+          "score": -0.11022,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1911,
+          "gene": "GNMT",
+          "score": 0.021289,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1072,
+          "gene": "HEATR9",
+          "score": -0.11612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5777,
+          "gene": "AFTPH",
+          "score": -0.23038,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10736,
+          "gene": "DIO2",
+          "score": 0.21103,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8434,
+          "gene": "HSDL1",
+          "score": -0.08225,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11939,
+          "gene": "NPC2",
+          "score": 0.071884,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10715,
+          "gene": "SDR39U1",
+          "score": -0.049585,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3144,
+          "gene": "SPINT3",
+          "score": -0.092487,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13774,
+          "gene": "OR52A5",
+          "score": -0.010455,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3011,
+          "gene": "MTRNR2L5",
+          "score": -0.060609,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 705,
+          "gene": "UBE2M",
+          "score": -0.25676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10999,
+          "gene": "CD1D",
+          "score": -0.1676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10615,
+          "gene": "C2CD6",
+          "score": 0.029571,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12951,
+          "gene": "IFT27",
+          "score": 0.049569,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17752,
+          "gene": "CDC23",
+          "score": 0.75313,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17959,
+          "gene": "PDLIM2",
+          "score": 0.16687,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8513,
+          "gene": "NPY2R",
+          "score": 0.020643,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2000,
+          "gene": "LUC7L",
+          "score": 0.02102,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16484,
+          "gene": "PCNT",
+          "score": 0.27061,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12514,
+          "gene": "ABCC3",
+          "score": 0.10402,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7026,
+          "gene": "HIST1H2AI",
+          "score": -0.093945,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11761,
+          "gene": "ABCB8",
+          "score": -0.05807,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5235,
+          "gene": "C3orf36",
+          "score": -0.17073,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 562,
+          "gene": "CHRM1",
+          "score": -0.038634,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8361,
+          "gene": "DTL",
+          "score": 0.062116,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16727,
+          "gene": "LRP4",
+          "score": 0.041176,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14193,
+          "gene": "CCDC7",
+          "score": 0.035182,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9844,
+          "gene": "PDZRN4",
+          "score": 0.030132,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7034,
+          "gene": "BANP",
+          "score": -0.14328,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13879,
+          "gene": "CR2",
+          "score": 0.29724,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12898,
+          "gene": "EGF",
+          "score": 0.16804,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12726,
+          "gene": "REST",
+          "score": 0.06455,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4816,
+          "gene": "DZANK1",
+          "score": -0.15082,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15247,
+          "gene": "KBTBD11",
+          "score": 0.037302,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18545,
+          "gene": "MEGF11",
+          "score": 0.077542,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2897,
+          "gene": "NUCB1",
+          "score": -0.14142,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18736,
+          "gene": "NUP214",
+          "score": 0.16475,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12874,
+          "gene": "VWA1",
+          "score": 0.093404,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2070,
+          "gene": "C4orf33",
+          "score": -0.24117,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17232,
+          "gene": "QDPR",
+          "score": 0.089388,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 965,
+          "gene": "LOC100130705",
+          "score": -0.2275,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18175,
+          "gene": "IARS",
+          "score": 0.21769,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17412,
+          "gene": "PPM1L",
+          "score": 0.097688,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9667,
+          "gene": "SLC39A9",
+          "score": -0.019225,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10657,
+          "gene": "CREBRF",
+          "score": 0.067736,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10080,
+          "gene": "CHIT1",
+          "score": -0.10366,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5643,
+          "gene": "FAM133A",
+          "score": -0.13119,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6133,
+          "gene": "RNF130",
+          "score": -0.14976,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 334,
+          "gene": "RNF146",
+          "score": -0.33644,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 9365,
+          "gene": "TOMM22",
+          "score": -0.050375,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1663,
+          "gene": "DMP1",
+          "score": -0.16108,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13435,
+          "gene": "NLRP3",
+          "score": 0.20612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3449,
+          "gene": "ASB14",
+          "score": -0.029937,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 97,
+          "gene": "FLVCR2",
+          "score": 0.11643,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12128,
+          "gene": "FOXA2",
+          "score": -0.06962,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9327,
+          "gene": "PPM1M",
+          "score": 0.066489,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15230,
+          "gene": "MRGPRE",
+          "score": 0.069416,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14698,
+          "gene": "TAOK2",
+          "score": 0.08395,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6721,
+          "gene": "CD40LG",
+          "score": -0.022008,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11027,
+          "gene": "CCDC102A",
+          "score": -0.1765,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9067,
+          "gene": "RABL6",
+          "score": -0.071797,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8118,
+          "gene": "UNC93B1",
+          "score": 0.1316,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17347,
+          "gene": "NIPSNAP1",
+          "score": 0.17017,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7546,
+          "gene": "PEX6",
+          "score": -0.24127,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16520,
+          "gene": "BEGAIN",
+          "score": 0.37792,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 920,
+          "gene": "ARHGEF6",
+          "score": -0.23752,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4988,
+          "gene": "C11orf16",
+          "score": -0.072414,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 753,
+          "gene": "ADGRL4",
+          "score": -0.035615,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8798,
+          "gene": "MT1M",
+          "score": -0.057575,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16045,
+          "gene": "BARX1",
+          "score": 0.082774,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3193,
+          "gene": "TMEM134",
+          "score": -0.089285,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5864,
+          "gene": "BTD",
+          "score": -0.1237,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7184,
+          "gene": "SELENBP1",
+          "score": -0.10742,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2112,
+          "gene": "SPRY4",
+          "score": -0.196,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3073,
+          "gene": "OR2AK2",
+          "score": -0.16243,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2167,
+          "gene": "ARHGAP17",
+          "score": 0.10559,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4443,
+          "gene": "RNASE7",
+          "score": -0.1516,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13133,
+          "gene": "SIGLEC14",
+          "score": -0.036235,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5495,
+          "gene": "AQP12A",
+          "score": -0.14952,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2773,
+          "gene": "ACTN1",
+          "score": 0.055767,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14954,
+          "gene": "POLG2",
+          "score": 0.2274,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13023,
+          "gene": "MRPS15",
+          "score": 0.14946,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9294,
+          "gene": "ZFP57",
+          "score": -0.035847,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12799,
+          "gene": "NDUFB10",
+          "score": 0.27002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13470,
+          "gene": "GPR89A",
+          "score": -0.089878,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12632,
+          "gene": "ZNF324B",
+          "score": 0.051283,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5467,
+          "gene": "ZIM3",
+          "score": 0.049688,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17579,
+          "gene": "PAM16",
+          "score": 0.19394,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1001,
+          "gene": "ZNF513",
+          "score": 0.050747,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2422,
+          "gene": "CHRNA4",
+          "score": -0.039819,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10751,
+          "gene": "BSPH1",
+          "score": -0.027673,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13891,
+          "gene": "LIPC",
+          "score": 0.0011676,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7844,
+          "gene": "FAM183A",
+          "score": 0.085677,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10759,
+          "gene": "EPO",
+          "score": -0.017593,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12200,
+          "gene": "HEPHL1",
+          "score": 0.083083,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14657,
+          "gene": "BCAP31",
+          "score": 0.0062327,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7233,
+          "gene": "BIRC2",
+          "score": 0.027505,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13118,
+          "gene": "NUP210L",
+          "score": -0.10562,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17403,
+          "gene": "POMP",
+          "score": 0.47385,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 18021,
+          "gene": "CLTC",
+          "score": 0.25547,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 35,
+          "gene": "PTPRC",
+          "score": -0.86005,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 13817,
+          "gene": "OR7C1",
+          "score": 0.084699,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1112,
+          "gene": "PCYT2",
+          "score": -0.32403,
+          "hit": 1,
+          "round": 3
         }
       ]
     }

```
