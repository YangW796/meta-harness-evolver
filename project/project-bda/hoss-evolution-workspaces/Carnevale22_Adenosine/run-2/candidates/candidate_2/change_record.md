# Change Record — candidate_2

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Carnevale22_Adenosine/run-2/best/current/harness
Generated at: 2026-04-30T07:14:50.208246

## Files Changed

- model.py: modified (added=3, deleted=2, delta=1)
- outputs/metrics.json: modified (added=2147, deleted=355, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -71,8 +71,9 @@
     
     for idx in available_indices:
         if idx in mean_scores:
-            # Exploitation term: mean score
-            exploitation = mean_scores[idx]
+            # Exploitation term: absolute mean score (prioritize extreme effects)
+            # Since hits are defined by large deviations in either direction
+            exploitation = abs(mean_scores[idx])
             # Exploration term: uncertainty bonus
             exploration = np.sqrt(2 * np.log(total_pulls) / counts[idx])
             ucb = exploitation + exploration

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18861,
-      "rounds": 1,
+      "rounds": 2,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 0,
-      "baseline_total_hits": 0,
+      "baseline_total_queries": 128,
+      "baseline_total_hits": 5,
       "delta_queries": 128,
-      "delta_hits": 5,
-      "total_queries": 128,
-      "total_hits": 5,
+      "delta_hits": 10,
+      "total_queries": 256,
+      "total_hits": 15,
       "top_k": 943,
       "hit_curve": {
         "queries": [
-          0,
-          128
+          128,
+          256
         ],
         "hits": [
-          0,
-          5
+          5,
+          15
         ]
       },
-      "auc": 320.0,
-      "auc_normalized": 0.002651113467656416,
-      "ncg": 0.22370739228746422,
+      "auc": 1280.0,
+      "auc_normalized": 0.005302226935312832,
+      "ncg": 0.2674238651142878,
       "round_details": [
         {
-          "round": 0,
+          "round": 1,
           "selected_count": 128,
-          "hits": 5,
-          "cumulative_hits": 5,
-          "precision_at_batch": 0.0390625,
+          "hits": 10,
+          "cumulative_hits": 15,
+          "precision_at_batch": 0.078125,
           "selected": [
-            "NonTarget.CTRL183",
-            "CCZ1B",
-            "RRP15",
-            "DERL2",
-            "LCN9",
-            "C11orf16",
-            "SLF2",
-            "MEX3C",
-            "APEX1",
-            "CLU",
-            "CSPG5",
-            "EQTN",
-            "PLA2R1",
-            "URI1",
-            "PROK2",
-            "BICRA",
-            "BCAS4",
-            "FBXO4",
-            "RIGI",
-            "SCN2B",
-            "NRBP2",
-            "PSTPIP1",
-            "DNAAF11",
-            "RFX6",
-            "CCDC12",
-            "ATP6V0D1",
-            "PTPRCAP",
-            "RPS6KA6",
-            "IL12RB2",
-            "GAGE12I",
-            "C5orf15",
-            "ADD3",
-            "ENO4",
-            "TTLL11",
-            "CDHR3",
-            "MTCL1",
-            "ZMYND12",
-            "DDR1",
-            "DHX57",
-            "SYNE4",
-            "ABCB1",
-            "EIF4E1B",
-            "PIGS",
-            "PPIL6",
-            "CD160",
-            "H2BC21",
-            "MAP3K1",
-            "NDUFS6",
-            "TMEM176B",
-            "MRPS7",
-            "TARP",
-            "PPIB",
-            "TMEM184A",
-            "RNASE6",
-            "LRRC14B",
-            "FGFBP1",
-            "SDR39U1",
-            "GOLGA8R",
-            "NonTarget.CTRL241",
-            "NELFE",
-            "PPARA",
-            "TLCD3B",
-            "MACROD2",
-            "FOXRED2",
-            "MAMDC4",
-            "NBL1",
-            "LIPM",
-            "MGAT4D",
-            "HACL1",
-            "PRELID3A",
-            "PTPRS",
-            "MYO5B",
-            "TNFSF4",
-            "HCLS1",
-            "MOGS",
-            "COL20A1",
-            "OPN1MW2",
-            "CDC34",
-            "C7orf77",
-            "NEUROD6",
-            "CDK14",
-            "COQ10B",
-            "SLC16A5",
-            "TERB1",
-            "NUP58",
-            "HEATR5A",
-            "THRSP",
-            "ARID2",
-            "SPON2",
-            "CDH13",
-            "TPBGL",
-            "TGFBI",
-            "MED16",
-            "IRAK2",
-            "TBC1D5",
-            "ADRB1",
-            "VWC2",
-            "IGSF10",
-            "IL11",
-            "TRIM49C",
-            "ZNF37A",
-            "HMGCR",
-            "TVP23B",
-            "ABCC4",
-            "CCNL2",
-            "PTGDR2",
-            "RPL7L1",
-            "GLRX5",
-            "TSPAN31",
-            "ADGRF1",
-            "SKIC8",
-            "PPIL1",
-            "MYO1H",
-            "SEMA6D",
-            "RIMBP3B",
-            "DCAF12",
-            "SPATA31C2",
-            "ST6GALNAC5",
-            "KDM5B",
-            "OR56A3",
-            "FAM210B",
-            "MSTO1",
-            "DDX49",
-            "SORCS3",
-            "GAL3ST1",
-            "CD5",
-            "PPP1R18",
-            "CAPN5"
+            "ZZZ3",
+            "ZZEF1",
+            "ZYX",
+            "ZYG11B",
+            "ZYG11A",
+            "ZXDC",
+            "ZXDB",
+            "ZXDA",
+            "ZWINT",
+            "ZWILCH",
+            "ZW10",
+            "ZUP1",
+            "ZSWIM9",
+            "ZSWIM8",
+            "ZSWIM7",
+            "ZSWIM6",
+            "ZSWIM5",
+            "ZSWIM4",
+            "ZSWIM3",
+            "ZSWIM2",
+            "ZSWIM1",
+            "ZSCAN9",
+            "ZSCAN5B",
+            "ZSCAN5A",
+            "ZSCAN4",
+            "ZSCAN32",
+            "ZSCAN31",
+            "ZSCAN30",
+            "ZSCAN29",
+            "ZSCAN26",
+            "ZSCAN25",
+            "ZSCAN23",
+            "ZSCAN22",
+            "ZSCAN21",
+            "ZSCAN20",
+            "ZSCAN2",
+            "ZSCAN18",
+            "ZSCAN16",
+            "ZSCAN12",
+            "ZSCAN10",
+            "ZSCAN1",
+            "ZRSR2",
+            "ZRANB3",
+            "ZRANB2",
+            "ZRANB1",
+            "ZPR1",
+            "ZPLD1",
+            "ZPBP2",
+            "ZPBP",
+            "ZP4",
+            "ZP3",
+            "ZP2",
+            "ZP1",
+            "ZNRF4",
+            "ZNRF3",
+            "ZNRF2",
+            "ZNRF1",
+            "ZNRD2",
+            "ZNHIT6",
+            "ZNHIT3",
+            "ZNHIT2",
+            "ZNHIT1",
+            "ZNG1F",
+            "ZNG1E",
+            "ZNG1C",
+            "ZNG1B",
+            "ZNG1A",
+            "ZNFX1",
+            "ZNF99",
+            "ZNF98",
+            "ZNF93",
+            "ZNF92",
+            "ZNF91",
+            "ZNF90",
+            "ZNF891",
+            "ZNF883",
+            "ZNF880",
+            "ZNF879",
+            "ZNF878",
+            "ZNF875",
+            "ZNF865",
+            "ZNF862",
+            "ZNF860",
+            "ZNF853",
+            "ZNF852",
+            "ZNF850",
+            "ZNF85",
+            "ZNF846",
+            "ZNF845",
+            "ZNF844",
+            "ZNF843",
+            "ZNF841",
+            "ZNF84",
+            "ZNF839",
+            "ZNF837",
+            "ZNF836",
+            "ZNF835",
+            "ZNF831",
+            "ZNF830",
+            "ZNF83",
+            "ZNF829",
+            "ZNF827",
+            "ZNF823",
+            "ZNF821",
+            "ZNF816-ZNF321P",
+            "ZNF816",
+            "ZNF814",
+            "ZNF813",
+            "ZNF812",
+            "ZNF81",
+            "ZNF808",
+            "ZNF806",
+            "ZNF805",
+            "ZNF804B",
+            "ZNF804A",
+            "ZNF800",
+            "ZNF80",
+            "ZNF8",
+            "ZNF799",
+            "ZNF793",
+            "ZNF792",
+            "ZNF791",
+            "ZNF790",
+            "ZNF79",
+            "ZNF789",
+            "ZNF787",
+            "ZNF786",
+            "ZNF785"
           ],
           "selected_scores": [
-            -0.013679,
-            -0.077916,
-            0.14121,
-            -0.17611,
-            0.17513,
-            -0.030504,
-            0.063605,
-            -0.071707,
-            -0.126416,
-            -0.015579,
-            0.11243,
-            0.00054836,
-            -0.17919,
-            0.015715,
-            -0.10179,
-            0.16015,
-            0.22939,
-            -0.56094,
-            0.051934,
-            0.33024,
-            0.073147,
-            0.0942,
-            0.096602,
-            0.13655,
-            -0.14117,
-            -0.9752,
-            0.091003,
-            0.030792,
-            0.23173,
-            0.04828,
-            0.021269,
-            -0.22285,
-            0.11626,
-            -0.04865,
-            -0.069768,
-            0.0146,
-            0.25557,
-            -0.14871,
-            0.071437,
-            0.09327,
-            0.34192,
-            -0.0537,
-            -0.04923,
-            -0.22363,
-            -0.054722,
-            -0.23789,
-            0.034984,
-            -0.16117,
-            0.087379,
-            0.078211,
-            -0.035043,
-            0.16509,
-            -0.044388,
-            0.088345,
-            -0.15484,
-            -0.27016,
-            0.11719,
-            0.048333,
-            0.13635,
-            -0.24708,
-            -0.049037,
-            -0.22864,
-            -0.029052,
-            0.044742,
-            0.01794,
-            0.12739,
-            -0.21006,
-            -0.093951,
-            0.1124,
-            0.080141,
-            -0.0097004,
-            -0.013569,
-            -0.19644,
-            -0.31934,
-            -0.22716,
-            0.075814,
-            -0.30922,
-            -0.26361,
-            -0.2155,
-            0.25833,
-            -0.033587,
-            -0.028383,
-            -0.013077,
-            -0.17629,
-            -0.18384,
-            0.16255,
-            0.083109,
-            0.055388,
-            -0.011189,
-            0.52117,
-            0.11907,
-            0.046072,
-            0.14753,
-            0.14208,
-            0.20667,
-            -0.24,
-            0.031964,
-            -0.11365,
-            -0.10291,
-            -0.056043,
-            0.19132,
-            -0.30428,
-            -0.038374,
-            0.30528,
-            -0.13455,
-            -0.17351,
-            0.09012,
-            0.038956,
-            0.078824,
-            0.074631,
-            0.044791,
-            0.16078,
-            0.14864,
-            0.018581,
-            -0.34541,
-            -0.016793,
-            -0.10327,
-            0.1771,
-            0.036445,
-            -0.038736,
-            0.10696,
-            -0.32416,
-            0.051002,
-            0.12779,
-            -0.089594,
-            0.080001,
-            -0.23215,
-            -0.2056985
+            0.0042296,
+            -0.025285,
+            -0.12133,
+            -0.17865,
+            -0.092959,
+            -0.34067,
+            0.23355,
+            0.046151,
+            0.2271,
+            -0.25147,
+            0.10344,
+            -0.18422,
+            -0.11507,
+            -0.30802,
+            0.0039042,
+            -0.10342,
+            0.12314,
+            -0.16708,
+            0.039048,
+            -0.052248,
+            0.29132,
+            -0.29343,
+            0.27484,
+            -0.18237,
+            0.11831,
+            0.051154,
+            -0.13807,
+            0.12307,
+            -0.19019,
+            0.25286,
+            0.048302,
+            0.22488,
+            -0.022625,
+            0.11542,
+            0.1752,
+            -0.066826,
+            -0.20931,
+            0.1603,
+            0.06866,
+            0.012773,
+            -0.29437,
+            -0.087505,
+            0.01562,
+            0.11397,
+            0.021138,
+            0.11386,
+            -0.36895,
+            0.1462,
+            -0.047664,
+            0.19443,
+            -0.11782,
+            0.20235,
+            -0.044293,
+            0.29151,
+            0.041693,
+            -0.089597,
+            0.12582,
+            0.26195,
+            -0.20291,
+            0.0056953,
+            -1.3601,
+            0.036511,
+            -0.038808,
+            0.14976,
+            0.37958,
+            -0.089569,
+            0.56598,
+            0.24159,
+            -0.27492,
+            -0.22855,
+            -0.15849,
+            -0.14714,
+            0.11351,
+            -0.040383,
+            0.21264,
+            0.14573,
+            0.19681,
+            -0.046847,
+            -0.064465,
+            0.25437,
+            -0.16523,
+            -0.20088,
+            0.12794,
+            -0.053904,
+            0.33108,
+            -0.01923,
+            -0.12341,
+            0.099597,
+            -0.013274,
+            0.26723,
+            0.0179,
+            4.0967e-06,
+            -0.042649,
+            0.13634,
+            -0.082197,
+            -0.044699,
+            0.22762,
+            0.30395,
+            -0.043654,
+            0.0444415,
+            -0.27861,
+            0.0040781,
+            0.3592,
+            0.34549,
+            0.011543,
+            -0.012604,
+            0.086018,
+            0.017173,
+            -0.050495,
+            -0.26963,
+            -0.021356,
+            0.33901,
+            0.052151,
+            -0.1854,
+            0.43123,
+            -0.0068465,
+            -0.058066,
+            0.10159,
+            -0.19427,
+            -0.0069571,
+            0.19458,
+            0.06026,
+            0.26988,
+            -0.013901,
+            -0.083043,
+            0.15997,
+            -0.074249,
+            0.57649
           ],
           "selected_hits": [
             0,
@@ -306,18 +306,6 @@
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
             1,
             0,
             0,
@@ -326,6 +314,39 @@
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
@@ -340,81 +361,12 @@
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
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
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
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
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
@@ -428,7 +380,55 @@
             0,
             0,
             0,
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
+            1,
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
+            1
           ]
         }
       ],
@@ -1328,6 +1328,902 @@
           "score": -0.2056985,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 18860,
+          "gene": "ZZZ3",
+          "score": 0.0042296,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18859,
+          "gene": "ZZEF1",
+          "score": -0.025285,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18858,
+          "gene": "ZYX",
+          "score": -0.12133,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18857,
+          "gene": "ZYG11B",
+          "score": -0.17865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18856,
+          "gene": "ZYG11A",
+          "score": -0.092959,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18855,
+          "gene": "ZXDC",
+          "score": -0.34067,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18854,
+          "gene": "ZXDB",
+          "score": 0.23355,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18853,
+          "gene": "ZXDA",
+          "score": 0.046151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18852,
+          "gene": "ZWINT",
+          "score": 0.2271,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18851,
+          "gene": "ZWILCH",
+          "score": -0.25147,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18850,
+          "gene": "ZW10",
+          "score": 0.10344,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18849,
+          "gene": "ZUP1",
+          "score": -0.18422,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18848,
+          "gene": "ZSWIM9",
+          "score": -0.11507,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18847,
+          "gene": "ZSWIM8",
+          "score": -0.30802,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18846,
+          "gene": "ZSWIM7",
+          "score": 0.0039042,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18845,
+          "gene": "ZSWIM6",
+          "score": -0.10342,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18844,
+          "gene": "ZSWIM5",
+          "score": 0.12314,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18843,
+          "gene": "ZSWIM4",
+          "score": -0.16708,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18842,
+          "gene": "ZSWIM3",
+          "score": 0.039048,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18841,
+          "gene": "ZSWIM2",
+          "score": -0.052248,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18840,
+          "gene": "ZSWIM1",
+          "score": 0.29132,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18839,
+          "gene": "ZSCAN9",
+          "score": -0.29343,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18838,
+          "gene": "ZSCAN5B",
+          "score": 0.27484,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18837,
+          "gene": "ZSCAN5A",
+          "score": -0.18237,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18836,
+          "gene": "ZSCAN4",
+          "score": 0.11831,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18835,
+          "gene": "ZSCAN32",
+          "score": 0.051154,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18834,
+          "gene": "ZSCAN31",
+          "score": -0.13807,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18833,
+          "gene": "ZSCAN30",
+          "score": 0.12307,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18832,
+          "gene": "ZSCAN29",
+          "score": -0.19019,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18831,
+          "gene": "ZSCAN26",
+          "score": 0.25286,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18830,
+          "gene": "ZSCAN25",
+          "score": 0.048302,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18829,
+          "gene": "ZSCAN23",
+          "score": 0.22488,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18828,
+          "gene": "ZSCAN22",
+          "score": -0.022625,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18827,
+          "gene": "ZSCAN21",
+          "score": 0.11542,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18826,
+          "gene": "ZSCAN20",
+          "score": 0.1752,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18825,
+          "gene": "ZSCAN2",
+          "score": -0.066826,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18824,
+          "gene": "ZSCAN18",
+          "score": -0.20931,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18823,
+          "gene": "ZSCAN16",
+          "score": 0.1603,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18822,
+          "gene": "ZSCAN12",
+          "score": 0.06866,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18821,
+          "gene": "ZSCAN10",
+          "score": 0.012773,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18820,
+          "gene": "ZSCAN1",
+          "score": -0.29437,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18819,
+          "gene": "ZRSR2",
+          "score": -0.087505,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18818,
+          "gene": "ZRANB3",
+          "score": 0.01562,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18817,
+          "gene": "ZRANB2",
+          "score": 0.11397,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18816,
+          "gene": "ZRANB1",
+          "score": 0.021138,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18815,
+          "gene": "ZPR1",
+          "score": 0.11386,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18814,
+          "gene": "ZPLD1",
+          "score": -0.36895,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18813,
+          "gene": "ZPBP2",
+          "score": 0.1462,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18812,
+          "gene": "ZPBP",
+          "score": -0.047664,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18811,
+          "gene": "ZP4",
+          "score": 0.19443,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18810,
+          "gene": "ZP3",
+          "score": -0.11782,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18809,
+          "gene": "ZP2",
+          "score": 0.20235,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18808,
+          "gene": "ZP1",
+          "score": -0.044293,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18807,
+          "gene": "ZNRF4",
+          "score": 0.29151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18806,
+          "gene": "ZNRF3",
+          "score": 0.041693,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18805,
+          "gene": "ZNRF2",
+          "score": -0.089597,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18804,
+          "gene": "ZNRF1",
+          "score": 0.12582,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18803,
+          "gene": "ZNRD2",
+          "score": 0.26195,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18802,
+          "gene": "ZNHIT6",
+          "score": -0.20291,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18801,
+          "gene": "ZNHIT3",
+          "score": 0.0056953,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18800,
+          "gene": "ZNHIT2",
+          "score": -1.3601,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18799,
+          "gene": "ZNHIT1",
+          "score": 0.036511,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18798,
+          "gene": "ZNG1F",
+          "score": -0.038808,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18797,
+          "gene": "ZNG1E",
+          "score": 0.14976,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18796,
+          "gene": "ZNG1C",
+          "score": 0.37958,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18795,
+          "gene": "ZNG1B",
+          "score": -0.089569,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18794,
+          "gene": "ZNG1A",
+          "score": 0.56598,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18793,
+          "gene": "ZNFX1",
+          "score": 0.24159,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18792,
+          "gene": "ZNF99",
+          "score": -0.27492,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18791,
+          "gene": "ZNF98",
+          "score": -0.22855,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18790,
+          "gene": "ZNF93",
+          "score": -0.15849,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18789,
+          "gene": "ZNF92",
+          "score": -0.14714,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18788,
+          "gene": "ZNF91",
+          "score": 0.11351,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18787,
+          "gene": "ZNF90",
+          "score": -0.040383,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18786,
+          "gene": "ZNF891",
+          "score": 0.21264,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18785,
+          "gene": "ZNF883",
+          "score": 0.14573,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18784,
+          "gene": "ZNF880",
+          "score": 0.19681,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18783,
+          "gene": "ZNF879",
+          "score": -0.046847,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18782,
+          "gene": "ZNF878",
+          "score": -0.064465,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18781,
+          "gene": "ZNF875",
+          "score": 0.25437,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18780,
+          "gene": "ZNF865",
+          "score": -0.16523,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18779,
+          "gene": "ZNF862",
+          "score": -0.20088,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18778,
+          "gene": "ZNF860",
+          "score": 0.12794,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18777,
+          "gene": "ZNF853",
+          "score": -0.053904,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18776,
+          "gene": "ZNF852",
+          "score": 0.33108,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18775,
+          "gene": "ZNF850",
+          "score": -0.01923,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18774,
+          "gene": "ZNF85",
+          "score": -0.12341,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18773,
+          "gene": "ZNF846",
+          "score": 0.099597,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18772,
+          "gene": "ZNF845",
+          "score": -0.013274,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18771,
+          "gene": "ZNF844",
+          "score": 0.26723,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18770,
+          "gene": "ZNF843",
+          "score": 0.0179,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18769,
+          "gene": "ZNF841",
+          "score": 4.0967e-06,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18768,
+          "gene": "ZNF84",
+          "score": -0.042649,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18767,
+          "gene": "ZNF839",
+          "score": 0.13634,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18766,
+          "gene": "ZNF837",
+          "score": -0.082197,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18765,
+          "gene": "ZNF836",
+          "score": -0.044699,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18764,
+          "gene": "ZNF835",
+          "score": 0.22762,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18763,
+          "gene": "ZNF831",
+          "score": 0.30395,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18762,
+          "gene": "ZNF830",
+          "score": -0.043654,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18761,
+          "gene": "ZNF83",
+          "score": 0.0444415,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18760,
+          "gene": "ZNF829",
+          "score": -0.27861,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18759,
+          "gene": "ZNF827",
+          "score": 0.0040781,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18758,
+          "gene": "ZNF823",
+          "score": 0.3592,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18757,
+          "gene": "ZNF821",
+          "score": 0.34549,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18756,
+          "gene": "ZNF816-ZNF321P",
+          "score": 0.011543,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18755,
+          "gene": "ZNF816",
+          "score": -0.012604,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18754,
+          "gene": "ZNF814",
+          "score": 0.086018,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18753,
+          "gene": "ZNF813",
+          "score": 0.017173,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18752,
+          "gene": "ZNF812",
+          "score": -0.050495,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18751,
+          "gene": "ZNF81",
+          "score": -0.26963,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18750,
+          "gene": "ZNF808",
+          "score": -0.021356,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18749,
+          "gene": "ZNF806",
+          "score": 0.33901,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18748,
+          "gene": "ZNF805",
+          "score": 0.052151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18747,
+          "gene": "ZNF804B",
+          "score": -0.1854,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18746,
+          "gene": "ZNF804A",
+          "score": 0.43123,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18745,
+          "gene": "ZNF800",
+          "score": -0.0068465,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18744,
+          "gene": "ZNF80",
+          "score": -0.058066,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18743,
+          "gene": "ZNF8",
+          "score": 0.10159,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18742,
+          "gene": "ZNF799",
+          "score": -0.19427,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18741,
+          "gene": "ZNF793",
+          "score": -0.0069571,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18740,
+          "gene": "ZNF792",
+          "score": 0.19458,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18739,
+          "gene": "ZNF791",
+          "score": 0.06026,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18738,
+          "gene": "ZNF790",
+          "score": 0.26988,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18737,
+          "gene": "ZNF79",
+          "score": -0.013901,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18736,
+          "gene": "ZNF789",
+          "score": -0.083043,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18735,
+          "gene": "ZNF787",
+          "score": 0.15997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18734,
+          "gene": "ZNF786",
+          "score": -0.074249,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18733,
+          "gene": "ZNF785",
+          "score": 0.57649,
+          "hit": 1,
+          "round": 1
         }
       ],
       "queried_history": [
@@ -2226,6 +3122,902 @@
           "score": -0.2056985,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 18860,
+          "gene": "ZZZ3",
+          "score": 0.0042296,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18859,
+          "gene": "ZZEF1",
+          "score": -0.025285,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18858,
+          "gene": "ZYX",
+          "score": -0.12133,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18857,
+          "gene": "ZYG11B",
+          "score": -0.17865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18856,
+          "gene": "ZYG11A",
+          "score": -0.092959,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18855,
+          "gene": "ZXDC",
+          "score": -0.34067,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18854,
+          "gene": "ZXDB",
+          "score": 0.23355,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18853,
+          "gene": "ZXDA",
+          "score": 0.046151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18852,
+          "gene": "ZWINT",
+          "score": 0.2271,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18851,
+          "gene": "ZWILCH",
+          "score": -0.25147,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18850,
+          "gene": "ZW10",
+          "score": 0.10344,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18849,
+          "gene": "ZUP1",
+          "score": -0.18422,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18848,
+          "gene": "ZSWIM9",
+          "score": -0.11507,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18847,
+          "gene": "ZSWIM8",
+          "score": -0.30802,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18846,
+          "gene": "ZSWIM7",
+          "score": 0.0039042,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18845,
+          "gene": "ZSWIM6",
+          "score": -0.10342,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18844,
+          "gene": "ZSWIM5",
+          "score": 0.12314,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18843,
+          "gene": "ZSWIM4",
+          "score": -0.16708,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18842,
+          "gene": "ZSWIM3",
+          "score": 0.039048,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18841,
+          "gene": "ZSWIM2",
+          "score": -0.052248,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18840,
+          "gene": "ZSWIM1",
+          "score": 0.29132,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18839,
+          "gene": "ZSCAN9",
+          "score": -0.29343,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18838,
+          "gene": "ZSCAN5B",
+          "score": 0.27484,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18837,
+          "gene": "ZSCAN5A",
+          "score": -0.18237,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18836,
+          "gene": "ZSCAN4",
+          "score": 0.11831,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18835,
+          "gene": "ZSCAN32",
+          "score": 0.051154,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18834,
+          "gene": "ZSCAN31",
+          "score": -0.13807,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18833,
+          "gene": "ZSCAN30",
+          "score": 0.12307,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18832,
+          "gene": "ZSCAN29",
+          "score": -0.19019,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18831,
+          "gene": "ZSCAN26",
+          "score": 0.25286,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18830,
+          "gene": "ZSCAN25",
+          "score": 0.048302,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18829,
+          "gene": "ZSCAN23",
+          "score": 0.22488,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18828,
+          "gene": "ZSCAN22",
+          "score": -0.022625,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18827,
+          "gene": "ZSCAN21",
+          "score": 0.11542,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18826,
+          "gene": "ZSCAN20",
+          "score": 0.1752,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18825,
+          "gene": "ZSCAN2",
+          "score": -0.066826,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18824,
+          "gene": "ZSCAN18",
+          "score": -0.20931,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18823,
+          "gene": "ZSCAN16",
+          "score": 0.1603,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18822,
+          "gene": "ZSCAN12",
+          "score": 0.06866,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18821,
+          "gene": "ZSCAN10",
+          "score": 0.012773,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18820,
+          "gene": "ZSCAN1",
+          "score": -0.29437,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18819,
+          "gene": "ZRSR2",
+          "score": -0.087505,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18818,
+          "gene": "ZRANB3",
+          "score": 0.01562,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18817,
+          "gene": "ZRANB2",
+          "score": 0.11397,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18816,
+          "gene": "ZRANB1",
+          "score": 0.021138,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18815,
+          "gene": "ZPR1",
+          "score": 0.11386,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18814,
+          "gene": "ZPLD1",
+          "score": -0.36895,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18813,
+          "gene": "ZPBP2",
+          "score": 0.1462,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18812,
+          "gene": "ZPBP",
+          "score": -0.047664,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18811,
+          "gene": "ZP4",
+          "score": 0.19443,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18810,
+          "gene": "ZP3",
+          "score": -0.11782,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18809,
+          "gene": "ZP2",
+          "score": 0.20235,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18808,
+          "gene": "ZP1",
+          "score": -0.044293,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18807,
+          "gene": "ZNRF4",
+          "score": 0.29151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18806,
+          "gene": "ZNRF3",
+          "score": 0.041693,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18805,
+          "gene": "ZNRF2",
+          "score": -0.089597,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18804,
+          "gene": "ZNRF1",
+          "score": 0.12582,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18803,
+          "gene": "ZNRD2",
+          "score": 0.26195,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18802,
+          "gene": "ZNHIT6",
+          "score": -0.20291,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18801,
+          "gene": "ZNHIT3",
+          "score": 0.0056953,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18800,
+          "gene": "ZNHIT2",
+          "score": -1.3601,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18799,
+          "gene": "ZNHIT1",
+          "score": 0.036511,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18798,
+          "gene": "ZNG1F",
+          "score": -0.038808,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18797,
+          "gene": "ZNG1E",
+          "score": 0.14976,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18796,
+          "gene": "ZNG1C",
+          "score": 0.37958,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18795,
+          "gene": "ZNG1B",
+          "score": -0.089569,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18794,
+          "gene": "ZNG1A",
+          "score": 0.56598,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18793,
+          "gene": "ZNFX1",
+          "score": 0.24159,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18792,
+          "gene": "ZNF99",
+          "score": -0.27492,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18791,
+          "gene": "ZNF98",
+          "score": -0.22855,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18790,
+          "gene": "ZNF93",
+          "score": -0.15849,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18789,
+          "gene": "ZNF92",
+          "score": -0.14714,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18788,
+          "gene": "ZNF91",
+          "score": 0.11351,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18787,
+          "gene": "ZNF90",
+          "score": -0.040383,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18786,
+          "gene": "ZNF891",
+          "score": 0.21264,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18785,
+          "gene": "ZNF883",
+          "score": 0.14573,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18784,
+          "gene": "ZNF880",
+          "score": 0.19681,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18783,
+          "gene": "ZNF879",
+          "score": -0.046847,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18782,
+          "gene": "ZNF878",
+          "score": -0.064465,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18781,
+          "gene": "ZNF875",
+          "score": 0.25437,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18780,
+          "gene": "ZNF865",
+          "score": -0.16523,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18779,
+          "gene": "ZNF862",
+          "score": -0.20088,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18778,
+          "gene": "ZNF860",
+          "score": 0.12794,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18777,
+          "gene": "ZNF853",
+          "score": -0.053904,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18776,
+          "gene": "ZNF852",
+          "score": 0.33108,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18775,
+          "gene": "ZNF850",
+          "score": -0.01923,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18774,
+          "gene": "ZNF85",
+          "score": -0.12341,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18773,
+          "gene": "ZNF846",
+          "score": 0.099597,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18772,
+          "gene": "ZNF845",
+          "score": -0.013274,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18771,
+          "gene": "ZNF844",
+          "score": 0.26723,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18770,
+          "gene": "ZNF843",
+          "score": 0.0179,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18769,
+          "gene": "ZNF841",
+          "score": 4.0967e-06,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18768,
+          "gene": "ZNF84",
+          "score": -0.042649,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18767,
+          "gene": "ZNF839",
+          "score": 0.13634,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18766,
+          "gene": "ZNF837",
+          "score": -0.082197,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18765,
+          "gene": "ZNF836",
+          "score": -0.044699,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18764,
+          "gene": "ZNF835",
+          "score": 0.22762,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18763,
+          "gene": "ZNF831",
+          "score": 0.30395,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18762,
+          "gene": "ZNF830",
+          "score": -0.043654,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18761,
+          "gene": "ZNF83",
+          "score": 0.0444415,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18760,
+          "gene": "ZNF829",
+          "score": -0.27861,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18759,
+          "gene": "ZNF827",
+          "score": 0.0040781,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18758,
+          "gene": "ZNF823",
+          "score": 0.3592,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18757,
+          "gene": "ZNF821",
+          "score": 0.34549,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18756,
+          "gene": "ZNF816-ZNF321P",
+          "score": 0.011543,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18755,
+          "gene": "ZNF816",
+          "score": -0.012604,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18754,
+          "gene": "ZNF814",
+          "score": 0.086018,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18753,
+          "gene": "ZNF813",
+          "score": 0.017173,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18752,
+          "gene": "ZNF812",
+          "score": -0.050495,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18751,
+          "gene": "ZNF81",
+          "score": -0.26963,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18750,
+          "gene": "ZNF808",
+          "score": -0.021356,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18749,
+          "gene": "ZNF806",
+          "score": 0.33901,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18748,
+          "gene": "ZNF805",
+          "score": 0.052151,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18747,
+          "gene": "ZNF804B",
+          "score": -0.1854,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18746,
+          "gene": "ZNF804A",
+          "score": 0.43123,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 18745,
+          "gene": "ZNF800",
+          "score": -0.0068465,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18744,
+          "gene": "ZNF80",
+          "score": -0.058066,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18743,
+          "gene": "ZNF8",
+          "score": 0.10159,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18742,
+          "gene": "ZNF799",
+          "score": -0.19427,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18741,
+          "gene": "ZNF793",
+          "score": -0.0069571,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18740,
+          "gene": "ZNF792",
+          "score": 0.19458,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18739,
+          "gene": "ZNF791",
+          "score": 0.06026,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18738,
+          "gene": "ZNF790",
+          "score": 0.26988,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18737,
+          "gene": "ZNF79",
+          "score": -0.013901,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18736,
+          "gene": "ZNF789",
+          "score": -0.083043,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18735,
+          "gene": "ZNF787",
+          "score": 0.15997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18734,
+          "gene": "ZNF786",
+          "score": -0.074249,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18733,
+          "gene": "ZNF785",
+          "score": 0.57649,
+          "hit": 1,
+          "round": 1
         }
       ]
     }

```
