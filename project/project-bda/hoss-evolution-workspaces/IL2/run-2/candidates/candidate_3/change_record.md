# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IL2/run-2/best/current/harness
Generated at: 2026-04-30T07:05:41.307908

## Files Changed

- model.py: modified (added=4, deleted=4, delta=0)
- outputs/metrics.json: modified (added=2422, deleted=630, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -85,13 +85,13 @@
         # Sample from Beta posterior
         sampled_prob = np.random.beta(1 + hits, 1 + trials - hits)
         
-        # Boost probability for genes with high scores (even if not hits)
-        # This helps prioritize genes that showed promising scores
+        # Boost probability for genes with extreme scores (both positive and negative)
+        # Hits can be extreme in either direction, so we want to pursue both
         avg_score = stats['sum_score'] / trials
         if avg_score > 0.1:  # Boost genes with positive average scores
             sampled_prob *= (1.0 + avg_score)
-        elif avg_score < -0.1:  # Penalize genes with negative average scores
-            sampled_prob *= (1.0 + avg_score)  # This reduces the probability
+        elif avg_score < -0.2:  # Boost genes with strongly negative scores (potential hits)
+            sampled_prob *= (1.0 + abs(avg_score))
         
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
-      "rounds": 2,
+      "rounds": 3,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 128,
-      "baseline_total_hits": 2,
+      "baseline_total_queries": 256,
+      "baseline_total_hits": 10,
       "delta_queries": 128,
-      "delta_hits": 8,
-      "total_queries": 256,
-      "total_hits": 10,
+      "delta_hits": 3,
+      "total_queries": 384,
+      "total_hits": 13,
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
-          10
+          10,
+          13
         ]
       },
-      "auc": 768.0,
-      "auc_normalized": 0.0045871559633027525,
-      "ncg": 0.15166213156940128,
+      "auc": 1472.0,
+      "auc_normalized": 0.005861365953109072,
+      "ncg": 0.1697223832957915,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 8,
-          "cumulative_hits": 10,
-          "precision_at_batch": 0.0625,
+          "hits": 3,
+          "cumulative_hits": 13,
+          "precision_at_batch": 0.0234375,
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
-            "HOXC4",
-            "NOTUM",
-            "NANS",
-            "KLRC1",
-            "ZNF430",
-            "RMND5A",
-            "DUSP28",
-            "EXO5",
-            "POLR1A",
-            "C17orf53",
-            "IFITM3",
-            "MARCH8",
-            "PREX1",
-            "TMEM191B",
-            "ELK1",
-            "S100A2",
-            "OR10J1",
-            "GCNT1",
-            "CHDH",
-            "RAB25",
-            "ZNF341",
-            "UBL4A",
-            "DRD1",
-            "PTMS",
-            "OTOP1",
-            "FAM133B",
-            "INS",
-            "GLB1L",
-            "DENND5A",
-            "LINGO4",
-            "DDX3Y",
-            "PPP1R17",
-            "C21orf140",
-            "DPRX",
-            "KDM6B",
-            "HESX1",
-            "OR2A5",
-            "RHOQ",
-            "ANAPC16",
-            "DHRS12",
-            "SIN3B",
-            "HNRNPCL1",
-            "CCL8",
-            "IFI27",
-            "GABARAPL1",
-            "LOC101927572",
-            "NSA2",
-            "TRIM71",
-            "PRPF4B",
-            "PTPRB",
-            "OR2Y1",
-            "PFKFB4",
-            "OR2T4",
-            "EPS8L2",
-            "ZNF491",
-            "CDRT4",
-            "USP17L18",
-            "CDC40",
-            "TRIM4",
-            "SEC23B",
-            "TCTEX1D4",
-            "OR52H1",
-            "ARL14EP",
-            "PRIM1",
-            "TK2",
-            "ANKH",
-            "ADAMTS19",
-            "YAF2",
-            "FGFR3",
-            "NEK9",
-            "COLEC10",
-            "FADS3",
-            "C1orf53",
-            "OGN",
-            "CSNK1E",
-            "OR2M7",
-            "CHST10",
-            "CDC42EP2",
-            "SRSF11",
-            "C20orf24",
-            "AWAT1",
-            "TJP1",
-            "CHMP6",
-            "GCM1",
-            "BPIFB2",
-            "TMED7",
-            "PROKR1",
-            "PRMT8",
-            "C9orf62"
+            "C1orf158",
+            "DTX3",
+            "PYCR1",
+            "ANKRD1",
+            "FAM209B",
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
+            "MAPKAPK2",
+            "ZNF773",
+            "COA6",
+            "GRK6",
+            "HACD3",
+            "GPBP1",
+            "SIGLEC6",
+            "PGRMC1",
+            "ST13",
+            "FFAR1",
+            "ARHGEF7",
+            "ADIPOR2",
+            "ZNF653",
+            "TMEM139",
+            "ACBD4",
+            "CD300C",
+            "ICMT",
+            "DNER",
+            "CCL28",
+            "GPC1",
+            "OR52N2",
+            "SSBP2",
+            "RAD21",
+            "LRRC4",
+            "OAZ1",
+            "TMEM92",
+            "SLC45A4",
+            "CAPZA1",
+            "NDUFA4L2",
+            "HIST1H4C",
+            "USP19",
+            "SLC30A3",
+            "MLST8",
+            "MASP2",
+            "MAP9",
+            "TOPORS",
+            "GALNT16",
+            "FOXD4L3",
+            "ABCB7",
+            "DEFB114",
+            "C14orf2",
+            "FAM187A",
+            "PITPNA",
+            "NXPE1",
+            "EVI2A",
+            "PROK1",
+            "PDLIM7",
+            "DRAXIN",
+            "PAPOLB",
+            "SPAG6",
+            "LRBA",
+            "MS4A7",
+            "CRABP1",
+            "MRPL24",
+            "OR14A16",
+            "PELI3",
+            "P2RX2",
+            "THOC2",
+            "SLC51A",
+            "IGDCC3",
+            "CLEC19A",
+            "SMARCD1",
+            "ABCC1",
+            "XBP1",
+            "NEK4",
+            "WFDC3",
+            "GNA15",
+            "SLC35B4",
+            "SOCS4",
+            "OR2T27",
+            "TTC7B",
+            "R3HDML",
+            "WNT11",
+            "ETV6",
+            "EML6",
+            "TOX",
+            "BATF",
+            "ZBP1",
+            "OR4C46",
+            "PCID2",
+            "HIST1H4L",
+            "WSCD2",
+            "IGFL4",
+            "MYL6B",
+            "DLL3",
+            "ZC3H7A",
+            "FAAH",
+            "HARS2",
+            "SLC5A6",
+            "ZCCHC6",
+            "ATP6V1C1",
+            "C12orf42",
+            "COX11",
+            "PRPF19",
+            "ACOT11"
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
-            -0.12667,
-            0.10129,
-            -0.23371,
-            -0.16521,
-            -0.18517,
-            0.461,
-            -0.033971,
-            0.017809,
-            0.46875,
-            0.12673,
-            0.0028595,
-            -0.13199,
-            -0.095804,
-            -0.12651,
-            -0.13432,
-            -0.09511,
-            0.012205,
-            -0.071154,
-            -0.061039,
-            0.055788,
-            0.0011696,
-            0.042462,
-            -0.03893,
-            -0.034787,
-            0.013069,
-            -0.20275,
-            -0.079412,
-            -0.043243,
-            -0.20781,
-            0.17735,
-            -0.14918,
-            -0.11426,
-            0.053805,
-            -0.024793,
-            -0.095585,
-            0.027254,
-            0.14379,
-            0.021322,
-            -0.15207,
-            0.024013,
-            -0.41614,
-            -0.1827,
-            -0.016116,
-            0.083302,
-            -0.23303,
-            -0.039871,
-            0.11643,
-            0.11847,
-            0.51551,
-            0.078528,
-            0.13271,
-            0.033601,
-            0.056779,
-            -0.01759,
-            -0.17236,
-            -0.040732,
-            -0.19344,
-            -0.0058287,
-            -0.020529,
-            0.075106,
-            0.11718,
-            -0.023666,
-            0.085855,
-            0.10731,
-            -0.037066,
-            0.072463,
-            0.1544,
-            0.0023117,
-            0.036341,
-            -0.057703,
-            -0.27127,
-            0.053787,
-            0.13969,
-            0.26433,
-            0.17414,
-            -0.14509,
-            0.20932,
-            0.19288,
-            0.049908,
-            -0.027283,
-            -0.17269,
-            0.3089,
-            0.85209,
-            -0.0060783,
-            -0.09537,
-            -0.27279,
-            -0.075679,
-            -0.044211,
-            0.061272
+            0.097043,
+            0.038861,
+            0.06193,
+            -0.0057194,
+            -0.082289,
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
+            0.19245,
+            0.045895,
+            -0.18267,
+            0.08963,
+            0.1045,
+            -0.090071,
+            -0.045845,
+            0.079825,
+            -0.04562,
+            0.069572,
+            -0.1306,
+            0.080924,
+            0.1237,
+            -0.12916,
+            0.082714,
+            -0.039319,
+            0.14553,
+            0.080505,
+            0.11867,
+            0.11686,
+            -0.11302,
+            0.0092768,
+            0.080238,
+            0.0091324,
+            -0.2093,
+            -0.13056,
+            -0.050475,
+            -0.17333,
+            -0.15782,
+            -0.21326,
+            -0.046145,
+            -0.063142,
+            -0.15324,
+            -0.008059,
+            0.12728,
+            -0.060971,
+            -0.14829,
+            -0.15181,
+            0.10038,
+            -0.090918,
+            -0.11477,
+            -0.031775,
+            -0.17168,
+            -0.061962,
+            -0.058831,
+            0.25729,
+            -0.134,
+            -0.17434,
+            0.080265,
+            -0.19942,
+            -0.14092,
+            -0.010499,
+            0.096255,
+            -0.17216,
+            -0.12285,
+            -0.03983,
+            -0.081321,
+            0.24104,
+            0.10035,
+            -0.15193,
+            -0.11868,
+            0.082628,
+            0.071233,
+            -0.17879,
+            -0.11655,
+            -0.056472,
+            -0.055715,
+            0.0041306,
+            0.073544,
+            -0.096019,
+            0.14533,
+            0.11373,
+            -0.066327,
+            0.041669,
+            0.0025375,
+            0.029981,
+            0.42521,
+            0.0070346,
+            -0.15106,
+            0.13588,
+            0.14993,
+            0.095297,
+            -0.18012,
+            -0.090291,
+            -0.10726,
+            -0.042454,
+            0.018843,
+            0.15363,
+            -0.02445,
+            -0.02287,
+            -0.052995,
+            -0.1366,
+            -0.0027798,
+            0.38417,
+            0.11124
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
@@ -326,108 +427,7 @@
             0,
             0,
             0,
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
-            1,
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
-            1,
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
-            1,
-            0,
-            0,
-            0,
-            0,
-            0,
             0
           ]
         }
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
           "candidate_index": 2539,
           "gene": "HOXC4",
           "score": -0.12667,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17227,
           "gene": "NOTUM",
           "score": 0.10129,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3401,
           "gene": "NANS",
           "score": -0.23371,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2011,
           "gene": "KLRC1",
           "score": -0.16521,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3104,
           "gene": "ZNF430",
           "score": -0.18517,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15096,
           "gene": "RMND5A",
           "score": 0.461,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10933,
           "gene": "DUSP28",
           "score": -0.033971,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10897,
           "gene": "EXO5",
           "score": 0.017809,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17445,
           "gene": "POLR1A",
           "score": 0.46875,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14481,
           "gene": "C17orf53",
           "score": 0.12673,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5507,
           "gene": "IFITM3",
           "score": 0.0028595,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4169,
           "gene": "MARCH8",
           "score": -0.13199,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2643,
           "gene": "PREX1",
           "score": -0.095804,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10547,
           "gene": "TMEM191B",
           "score": -0.12651,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1651,
           "gene": "ELK1",
           "score": -0.13432,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8853,
           "gene": "S100A2",
           "score": -0.09511,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12148,
           "gene": "OR10J1",
           "score": 0.012205,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6137,
           "gene": "GCNT1",
           "score": -0.071154,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2319,
           "gene": "CHDH",
           "score": -0.061039,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18209,
           "gene": "RAB25",
           "score": 0.055788,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3740,
           "gene": "ZNF341",
           "score": 0.0011696,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9807,
           "gene": "UBL4A",
           "score": 0.042462,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16328,
           "gene": "DRD1",
           "score": -0.03893,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11933,
           "gene": "PTMS",
           "score": -0.034787,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14324,
           "gene": "OTOP1",
           "score": 0.013069,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1361,
           "gene": "FAM133B",
           "score": -0.20275,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15611,
           "gene": "INS",
           "score": -0.079412,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13693,
           "gene": "GLB1L",
           "score": -0.043243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2757,
           "gene": "DENND5A",
           "score": -0.20781,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11818,
           "gene": "LINGO4",
           "score": 0.17735,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4196,
           "gene": "DDX3Y",
           "score": -0.14918,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2842,
           "gene": "PPP1R17",
           "score": -0.11426,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5084,
           "gene": "C21orf140",
           "score": 0.053805,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10151,
           "gene": "DPRX",
           "score": -0.024793,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3595,
           "gene": "KDM6B",
           "score": -0.095585,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17655,
           "gene": "HESX1",
           "score": 0.027254,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14019,
           "gene": "OR2A5",
           "score": 0.14379,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14621,
           "gene": "RHOQ",
           "score": 0.021322,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1251,
           "gene": "ANAPC16",
           "score": -0.15207,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4836,
           "gene": "DHRS12",
           "score": 0.024013,
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
           "candidate_index": 3490,
           "gene": "HNRNPCL1",
           "score": -0.1827,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4103,
           "gene": "CCL8",
           "score": -0.016116,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4159,
           "gene": "IFI27",
           "score": 0.083302,
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
           "candidate_index": 11142,
           "gene": "LOC101927572",
           "score": -0.039871,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3913,
           "gene": "NSA2",
           "score": 0.11643,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17559,
           "gene": "TRIM71",
           "score": 0.11847,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16434,
           "gene": "PRPF4B",
           "score": 0.51551,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8547,
           "gene": "PTPRB",
           "score": 0.078528,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15057,
           "gene": "OR2Y1",
           "score": 0.13271,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11222,
           "gene": "PFKFB4",
           "score": 0.033601,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12729,
           "gene": "OR2T4",
           "score": 0.056779,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2873,
           "gene": "EPS8L2",
           "score": -0.01759,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1101,
           "gene": "ZNF491",
           "score": -0.17236,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3065,
           "gene": "CDRT4",
           "score": -0.040732,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6797,
           "gene": "USP17L18",
           "score": -0.19344,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13356,
           "gene": "CDC40",
           "score": -0.0058287,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6399,
           "gene": "TRIM4",
           "score": -0.020529,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13317,
           "gene": "SEC23B",
           "score": 0.075106,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8591,
           "gene": "TCTEX1D4",
           "score": 0.11718,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13489,
           "gene": "OR52H1",
           "score": -0.023666,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10804,
           "gene": "ARL14EP",
           "score": 0.085855,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13134,
           "gene": "PRIM1",
           "score": 0.10731,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11452,
           "gene": "TK2",
           "score": -0.037066,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1708,
           "gene": "ANKH",
           "score": 0.072463,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6130,
           "gene": "ADAMTS19",
           "score": 0.1544,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17734,
           "gene": "YAF2",
           "score": 0.0023117,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5869,
           "gene": "FGFR3",
           "score": 0.036341,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6194,
           "gene": "NEK9",
           "score": -0.057703,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1684,
           "gene": "COLEC10",
           "score": -0.27127,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7705,
           "gene": "FADS3",
           "score": 0.053787,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9902,
           "gene": "C1orf53",
           "score": 0.13969,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7325,
           "gene": "OGN",
           "score": 0.26433,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11400,
           "gene": "CSNK1E",
           "score": 0.17414,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6195,
           "gene": "OR2M7",
           "score": -0.14509,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7143,
           "gene": "CHST10",
           "score": 0.20932,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12669,
           "gene": "CDC42EP2",
           "score": 0.19288,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12845,
           "gene": "SRSF11",
           "score": 0.049908,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7421,
           "gene": "C20orf24",
           "score": -0.027283,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1999,
           "gene": "AWAT1",
           "score": -0.17269,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15126,
           "gene": "TJP1",
           "score": 0.3089,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16542,
           "gene": "CHMP6",
           "score": 0.85209,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2017,
           "gene": "GCM1",
           "score": -0.0060783,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3166,
           "gene": "BPIFB2",
           "score": -0.09537,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 895,
           "gene": "TMED7",
           "score": -0.27279,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 780,
           "gene": "PROKR1",
           "score": -0.075679,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18006,
           "gene": "PRMT8",
           "score": -0.044211,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16853,
           "gene": "C9orf62",
           "score": 0.061272,
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
+          "candidate_index": 5882,
+          "gene": "FAM209B",
+          "score": -0.082289,
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
+          "candidate_index": 11454,
+          "gene": "MAPKAPK2",
+          "score": 0.19245,
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
+          "candidate_index": 6279,
+          "gene": "SIGLEC6",
+          "score": -0.045845,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4334,
+          "gene": "PGRMC1",
+          "score": 0.079825,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8592,
+          "gene": "ST13",
+          "score": -0.04562,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8250,
+          "gene": "FFAR1",
+          "score": 0.069572,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1632,
+          "gene": "ARHGEF7",
+          "score": -0.1306,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1440,
+          "gene": "ADIPOR2",
+          "score": 0.080924,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14505,
+          "gene": "ZNF653",
+          "score": 0.1237,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1253,
+          "gene": "TMEM139",
+          "score": -0.12916,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10924,
+          "gene": "ACBD4",
+          "score": 0.082714,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12282,
+          "gene": "CD300C",
+          "score": -0.039319,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15650,
+          "gene": "ICMT",
+          "score": 0.14553,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15079,
+          "gene": "DNER",
+          "score": 0.080505,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17958,
+          "gene": "CCL28",
+          "score": 0.11867,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5014,
+          "gene": "GPC1",
+          "score": 0.11686,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7764,
+          "gene": "OR52N2",
+          "score": -0.11302,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16062,
+          "gene": "SSBP2",
+          "score": 0.0092768,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15145,
+          "gene": "RAD21",
+          "score": 0.080238,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11498,
+          "gene": "LRRC4",
+          "score": 0.0091324,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1446,
+          "gene": "OAZ1",
+          "score": -0.2093,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9249,
+          "gene": "TMEM92",
+          "score": -0.13056,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5238,
+          "gene": "SLC45A4",
+          "score": -0.050475,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 306,
+          "gene": "CAPZA1",
+          "score": -0.17333,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7428,
+          "gene": "NDUFA4L2",
+          "score": -0.15782,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 481,
+          "gene": "HIST1H4C",
+          "score": -0.21326,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18472,
+          "gene": "USP19",
+          "score": -0.046145,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18047,
+          "gene": "SLC30A3",
+          "score": -0.063142,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9372,
+          "gene": "MLST8",
+          "score": -0.15324,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11855,
+          "gene": "MASP2",
+          "score": -0.008059,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18719,
+          "gene": "MAP9",
+          "score": 0.12728,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6625,
+          "gene": "TOPORS",
+          "score": -0.060971,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13449,
+          "gene": "GALNT16",
+          "score": -0.14829,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3717,
+          "gene": "FOXD4L3",
+          "score": -0.15181,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11998,
+          "gene": "ABCB7",
+          "score": 0.10038,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11307,
+          "gene": "DEFB114",
+          "score": -0.090918,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3745,
+          "gene": "C14orf2",
+          "score": -0.11477,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7449,
+          "gene": "FAM187A",
+          "score": -0.031775,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1967,
+          "gene": "PITPNA",
+          "score": -0.17168,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14402,
+          "gene": "NXPE1",
+          "score": -0.061962,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1591,
+          "gene": "EVI2A",
+          "score": -0.058831,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15751,
+          "gene": "PROK1",
+          "score": 0.25729,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4079,
+          "gene": "PDLIM7",
+          "score": -0.134,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4753,
+          "gene": "DRAXIN",
+          "score": -0.17434,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5973,
+          "gene": "PAPOLB",
+          "score": 0.080265,
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
+          "candidate_index": 9768,
+          "gene": "LRBA",
+          "score": -0.14092,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2098,
+          "gene": "MS4A7",
+          "score": -0.010499,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9051,
+          "gene": "CRABP1",
+          "score": 0.096255,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2475,
+          "gene": "MRPL24",
+          "score": -0.17216,
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
+          "candidate_index": 14468,
+          "gene": "PELI3",
+          "score": -0.03983,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9116,
+          "gene": "P2RX2",
+          "score": -0.081321,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5939,
+          "gene": "THOC2",
+          "score": 0.24104,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17396,
+          "gene": "SLC51A",
+          "score": 0.10035,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6414,
+          "gene": "IGDCC3",
+          "score": -0.15193,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2020,
+          "gene": "CLEC19A",
+          "score": -0.11868,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9295,
+          "gene": "SMARCD1",
+          "score": 0.082628,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16052,
+          "gene": "ABCC1",
+          "score": 0.071233,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8733,
+          "gene": "XBP1",
+          "score": -0.17879,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2157,
+          "gene": "NEK4",
+          "score": -0.11655,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17018,
+          "gene": "WFDC3",
+          "score": -0.056472,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10966,
+          "gene": "GNA15",
+          "score": -0.055715,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18152,
+          "gene": "SLC35B4",
+          "score": 0.0041306,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16201,
+          "gene": "SOCS4",
+          "score": 0.073544,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2176,
+          "gene": "OR2T27",
+          "score": -0.096019,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9452,
+          "gene": "TTC7B",
+          "score": 0.14533,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16315,
+          "gene": "R3HDML",
+          "score": 0.11373,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9974,
+          "gene": "WNT11",
+          "score": -0.066327,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13338,
+          "gene": "ETV6",
+          "score": 0.041669,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13402,
+          "gene": "EML6",
+          "score": 0.0025375,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10048,
+          "gene": "TOX",
+          "score": 0.029981,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18177,
+          "gene": "BATF",
+          "score": 0.42521,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 14949,
+          "gene": "ZBP1",
+          "score": 0.0070346,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2420,
+          "gene": "OR4C46",
+          "score": -0.15106,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10552,
+          "gene": "PCID2",
+          "score": 0.13588,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8387,
+          "gene": "HIST1H4L",
+          "score": 0.14993,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4388,
+          "gene": "WSCD2",
+          "score": 0.095297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4409,
+          "gene": "IGFL4",
+          "score": -0.18012,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4411,
+          "gene": "MYL6B",
+          "score": -0.090291,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2472,
+          "gene": "DLL3",
+          "score": -0.10726,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14679,
+          "gene": "ZC3H7A",
+          "score": -0.042454,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13166,
+          "gene": "FAAH",
+          "score": 0.018843,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11475,
+          "gene": "HARS2",
+          "score": 0.15363,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14740,
+          "gene": "SLC5A6",
+          "score": -0.02445,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2800,
+          "gene": "ZCCHC6",
+          "score": -0.02287,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9120,
+          "gene": "ATP6V1C1",
+          "score": -0.052995,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4447,
+          "gene": "C12orf42",
+          "score": -0.1366,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9269,
+          "gene": "COX11",
+          "score": -0.0027798,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17721,
+          "gene": "PRPF19",
+          "score": 0.38417,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 16718,
+          "gene": "ACOT11",
+          "score": 0.11124,
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
           "candidate_index": 2539,
           "gene": "HOXC4",
           "score": -0.12667,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17227,
           "gene": "NOTUM",
           "score": 0.10129,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3401,
           "gene": "NANS",
           "score": -0.23371,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2011,
           "gene": "KLRC1",
           "score": -0.16521,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3104,
           "gene": "ZNF430",
           "score": -0.18517,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15096,
           "gene": "RMND5A",
           "score": 0.461,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10933,
           "gene": "DUSP28",
           "score": -0.033971,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10897,
           "gene": "EXO5",
           "score": 0.017809,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17445,
           "gene": "POLR1A",
           "score": 0.46875,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14481,
           "gene": "C17orf53",
           "score": 0.12673,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5507,
           "gene": "IFITM3",
           "score": 0.0028595,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4169,
           "gene": "MARCH8",
           "score": -0.13199,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2643,
           "gene": "PREX1",
           "score": -0.095804,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10547,
           "gene": "TMEM191B",
           "score": -0.12651,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1651,
           "gene": "ELK1",
           "score": -0.13432,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8853,
           "gene": "S100A2",
           "score": -0.09511,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12148,
           "gene": "OR10J1",
           "score": 0.012205,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6137,
           "gene": "GCNT1",
           "score": -0.071154,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2319,
           "gene": "CHDH",
           "score": -0.061039,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18209,
           "gene": "RAB25",
           "score": 0.055788,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3740,
           "gene": "ZNF341",
           "score": 0.0011696,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9807,
           "gene": "UBL4A",
           "score": 0.042462,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16328,
           "gene": "DRD1",
           "score": -0.03893,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11933,
           "gene": "PTMS",
           "score": -0.034787,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14324,
           "gene": "OTOP1",
           "score": 0.013069,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1361,
           "gene": "FAM133B",
           "score": -0.20275,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15611,
           "gene": "INS",
           "score": -0.079412,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13693,
           "gene": "GLB1L",
           "score": -0.043243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2757,
           "gene": "DENND5A",
           "score": -0.20781,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11818,
           "gene": "LINGO4",
           "score": 0.17735,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4196,
           "gene": "DDX3Y",
           "score": -0.14918,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2842,
           "gene": "PPP1R17",
           "score": -0.11426,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5084,
           "gene": "C21orf140",
           "score": 0.053805,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10151,
           "gene": "DPRX",
           "score": -0.024793,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3595,
           "gene": "KDM6B",
           "score": -0.095585,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17655,
           "gene": "HESX1",
           "score": 0.027254,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14019,
           "gene": "OR2A5",
           "score": 0.14379,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14621,
           "gene": "RHOQ",
           "score": 0.021322,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1251,
           "gene": "ANAPC16",
           "score": -0.15207,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4836,
           "gene": "DHRS12",
           "score": 0.024013,
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
           "candidate_index": 3490,
           "gene": "HNRNPCL1",
           "score": -0.1827,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4103,
           "gene": "CCL8",
           "score": -0.016116,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4159,
           "gene": "IFI27",
           "score": 0.083302,
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
           "candidate_index": 11142,
           "gene": "LOC101927572",
           "score": -0.039871,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3913,
           "gene": "NSA2",
           "score": 0.11643,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17559,
           "gene": "TRIM71",
           "score": 0.11847,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16434,
           "gene": "PRPF4B",
           "score": 0.51551,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8547,
           "gene": "PTPRB",
           "score": 0.078528,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15057,
           "gene": "OR2Y1",
           "score": 0.13271,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11222,
           "gene": "PFKFB4",
           "score": 0.033601,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12729,
           "gene": "OR2T4",
           "score": 0.056779,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2873,
           "gene": "EPS8L2",
           "score": -0.01759,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1101,
           "gene": "ZNF491",
           "score": -0.17236,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3065,
           "gene": "CDRT4",
           "score": -0.040732,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6797,
           "gene": "USP17L18",
           "score": -0.19344,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13356,
           "gene": "CDC40",
           "score": -0.0058287,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6399,
           "gene": "TRIM4",
           "score": -0.020529,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13317,
           "gene": "SEC23B",
           "score": 0.075106,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8591,
           "gene": "TCTEX1D4",
           "score": 0.11718,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13489,
           "gene": "OR52H1",
           "score": -0.023666,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10804,
           "gene": "ARL14EP",
           "score": 0.085855,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13134,
           "gene": "PRIM1",
           "score": 0.10731,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11452,
           "gene": "TK2",
           "score": -0.037066,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1708,
           "gene": "ANKH",
           "score": 0.072463,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6130,
           "gene": "ADAMTS19",
           "score": 0.1544,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17734,
           "gene": "YAF2",
           "score": 0.0023117,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5869,
           "gene": "FGFR3",
           "score": 0.036341,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6194,
           "gene": "NEK9",
           "score": -0.057703,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1684,
           "gene": "COLEC10",
           "score": -0.27127,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7705,
           "gene": "FADS3",
           "score": 0.053787,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9902,
           "gene": "C1orf53",
           "score": 0.13969,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7325,
           "gene": "OGN",
           "score": 0.26433,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11400,
           "gene": "CSNK1E",
           "score": 0.17414,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6195,
           "gene": "OR2M7",
           "score": -0.14509,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7143,
           "gene": "CHST10",
           "score": 0.20932,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12669,
           "gene": "CDC42EP2",
           "score": 0.19288,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12845,
           "gene": "SRSF11",
           "score": 0.049908,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7421,
           "gene": "C20orf24",
           "score": -0.027283,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1999,
           "gene": "AWAT1",
           "score": -0.17269,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15126,
           "gene": "TJP1",
           "score": 0.3089,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16542,
           "gene": "CHMP6",
           "score": 0.85209,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2017,
           "gene": "GCM1",
           "score": -0.0060783,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3166,
           "gene": "BPIFB2",
           "score": -0.09537,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 895,
           "gene": "TMED7",
           "score": -0.27279,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 780,
           "gene": "PROKR1",
           "score": -0.075679,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18006,
           "gene": "PRMT8",
           "score": -0.044211,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16853,
           "gene": "C9orf62",
           "score": 0.061272,
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
+          "candidate_index": 5882,
+          "gene": "FAM209B",
+          "score": -0.082289,
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
+          "candidate_index": 11454,
+          "gene": "MAPKAPK2",
+          "score": 0.19245,
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
+          "candidate_index": 6279,
+          "gene": "SIGLEC6",
+          "score": -0.045845,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4334,
+          "gene": "PGRMC1",
+          "score": 0.079825,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8592,
+          "gene": "ST13",
+          "score": -0.04562,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8250,
+          "gene": "FFAR1",
+          "score": 0.069572,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1632,
+          "gene": "ARHGEF7",
+          "score": -0.1306,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1440,
+          "gene": "ADIPOR2",
+          "score": 0.080924,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14505,
+          "gene": "ZNF653",
+          "score": 0.1237,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1253,
+          "gene": "TMEM139",
+          "score": -0.12916,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10924,
+          "gene": "ACBD4",
+          "score": 0.082714,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12282,
+          "gene": "CD300C",
+          "score": -0.039319,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15650,
+          "gene": "ICMT",
+          "score": 0.14553,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15079,
+          "gene": "DNER",
+          "score": 0.080505,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17958,
+          "gene": "CCL28",
+          "score": 0.11867,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5014,
+          "gene": "GPC1",
+          "score": 0.11686,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7764,
+          "gene": "OR52N2",
+          "score": -0.11302,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16062,
+          "gene": "SSBP2",
+          "score": 0.0092768,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15145,
+          "gene": "RAD21",
+          "score": 0.080238,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11498,
+          "gene": "LRRC4",
+          "score": 0.0091324,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1446,
+          "gene": "OAZ1",
+          "score": -0.2093,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9249,
+          "gene": "TMEM92",
+          "score": -0.13056,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5238,
+          "gene": "SLC45A4",
+          "score": -0.050475,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 306,
+          "gene": "CAPZA1",
+          "score": -0.17333,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7428,
+          "gene": "NDUFA4L2",
+          "score": -0.15782,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 481,
+          "gene": "HIST1H4C",
+          "score": -0.21326,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18472,
+          "gene": "USP19",
+          "score": -0.046145,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18047,
+          "gene": "SLC30A3",
+          "score": -0.063142,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9372,
+          "gene": "MLST8",
+          "score": -0.15324,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11855,
+          "gene": "MASP2",
+          "score": -0.008059,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18719,
+          "gene": "MAP9",
+          "score": 0.12728,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6625,
+          "gene": "TOPORS",
+          "score": -0.060971,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13449,
+          "gene": "GALNT16",
+          "score": -0.14829,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3717,
+          "gene": "FOXD4L3",
+          "score": -0.15181,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11998,
+          "gene": "ABCB7",
+          "score": 0.10038,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11307,
+          "gene": "DEFB114",
+          "score": -0.090918,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3745,
+          "gene": "C14orf2",
+          "score": -0.11477,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7449,
+          "gene": "FAM187A",
+          "score": -0.031775,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1967,
+          "gene": "PITPNA",
+          "score": -0.17168,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14402,
+          "gene": "NXPE1",
+          "score": -0.061962,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1591,
+          "gene": "EVI2A",
+          "score": -0.058831,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15751,
+          "gene": "PROK1",
+          "score": 0.25729,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4079,
+          "gene": "PDLIM7",
+          "score": -0.134,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4753,
+          "gene": "DRAXIN",
+          "score": -0.17434,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5973,
+          "gene": "PAPOLB",
+          "score": 0.080265,
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
+          "candidate_index": 9768,
+          "gene": "LRBA",
+          "score": -0.14092,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2098,
+          "gene": "MS4A7",
+          "score": -0.010499,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9051,
+          "gene": "CRABP1",
+          "score": 0.096255,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2475,
+          "gene": "MRPL24",
+          "score": -0.17216,
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
+          "candidate_index": 14468,
+          "gene": "PELI3",
+          "score": -0.03983,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9116,
+          "gene": "P2RX2",
+          "score": -0.081321,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5939,
+          "gene": "THOC2",
+          "score": 0.24104,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17396,
+          "gene": "SLC51A",
+          "score": 0.10035,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6414,
+          "gene": "IGDCC3",
+          "score": -0.15193,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2020,
+          "gene": "CLEC19A",
+          "score": -0.11868,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9295,
+          "gene": "SMARCD1",
+          "score": 0.082628,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16052,
+          "gene": "ABCC1",
+          "score": 0.071233,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8733,
+          "gene": "XBP1",
+          "score": -0.17879,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2157,
+          "gene": "NEK4",
+          "score": -0.11655,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17018,
+          "gene": "WFDC3",
+          "score": -0.056472,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10966,
+          "gene": "GNA15",
+          "score": -0.055715,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18152,
+          "gene": "SLC35B4",
+          "score": 0.0041306,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16201,
+          "gene": "SOCS4",
+          "score": 0.073544,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2176,
+          "gene": "OR2T27",
+          "score": -0.096019,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9452,
+          "gene": "TTC7B",
+          "score": 0.14533,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16315,
+          "gene": "R3HDML",
+          "score": 0.11373,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9974,
+          "gene": "WNT11",
+          "score": -0.066327,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13338,
+          "gene": "ETV6",
+          "score": 0.041669,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13402,
+          "gene": "EML6",
+          "score": 0.0025375,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10048,
+          "gene": "TOX",
+          "score": 0.029981,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18177,
+          "gene": "BATF",
+          "score": 0.42521,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 14949,
+          "gene": "ZBP1",
+          "score": 0.0070346,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2420,
+          "gene": "OR4C46",
+          "score": -0.15106,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10552,
+          "gene": "PCID2",
+          "score": 0.13588,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8387,
+          "gene": "HIST1H4L",
+          "score": 0.14993,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4388,
+          "gene": "WSCD2",
+          "score": 0.095297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4409,
+          "gene": "IGFL4",
+          "score": -0.18012,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4411,
+          "gene": "MYL6B",
+          "score": -0.090291,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2472,
+          "gene": "DLL3",
+          "score": -0.10726,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14679,
+          "gene": "ZC3H7A",
+          "score": -0.042454,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13166,
+          "gene": "FAAH",
+          "score": 0.018843,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11475,
+          "gene": "HARS2",
+          "score": 0.15363,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14740,
+          "gene": "SLC5A6",
+          "score": -0.02445,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2800,
+          "gene": "ZCCHC6",
+          "score": -0.02287,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9120,
+          "gene": "ATP6V1C1",
+          "score": -0.052995,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4447,
+          "gene": "C12orf42",
+          "score": -0.1366,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9269,
+          "gene": "COX11",
+          "score": -0.0027798,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17721,
+          "gene": "PRPF19",
+          "score": 0.38417,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 16718,
+          "gene": "ACOT11",
+          "score": 0.11124,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
