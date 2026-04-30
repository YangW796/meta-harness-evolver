# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Carnevale22_Adenosine/run-1/best/current/harness
Generated at: 2026-04-30T06:50:08.129086

## Files Changed

- model.py: modified (added=4, deleted=3, delta=1)
- outputs/metrics.json: modified (added=2134, deleted=342, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -58,10 +58,11 @@
     
     # Exploitation: select based on scores
     if len(history) > 0 and num_exploit > 0:
-        # Sort history by score (descending)
-        sorted_history = sorted(history, key=lambda x: x['score'], reverse=True)
+        # For this task, NEGATIVE scores are better (boost T cell proliferation)
+        # Sort history by score (ascending to prioritize negative scores)
+        sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
         
-        # Get top performers
+        # Get top performers (most negative scores)
         top_performers = [h['candidate_index'] for h in sorted_history[:min(50, len(sorted_history))]]
         
         # Find candidates similar to top performers (if gene search available)

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
+      "baseline_total_hits": 2,
       "delta_queries": 128,
-      "delta_hits": 2,
-      "total_queries": 128,
-      "total_hits": 2,
+      "delta_hits": 5,
+      "total_queries": 256,
+      "total_hits": 7,
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
-          2
+          2,
+          7
         ]
       },
-      "auc": 128.0,
-      "auc_normalized": 0.0010604453870625664,
-      "ncg": 0.20757310219173042,
+      "auc": 576.0,
+      "auc_normalized": 0.0023860021208907743,
+      "ncg": 0.23323368332888017,
       "round_details": [
         {
-          "round": 0,
+          "round": 1,
           "selected_count": 128,
-          "hits": 2,
-          "cumulative_hits": 2,
-          "precision_at_batch": 0.015625,
+          "hits": 5,
+          "cumulative_hits": 7,
+          "precision_at_batch": 0.0390625,
           "selected": [
-            "CT45A7",
-            "APBB1IP",
-            "MAPK8IP2",
-            "KLK2",
-            "IL16",
-            "E2F6",
-            "COLGALT1",
-            "WDR44",
-            "CFAP43",
-            "RPL41",
-            "ARMH4",
-            "ARHGEF7",
-            "CKS1B",
-            "IDH3A",
-            "IZUMO1R",
-            "TMEM185B",
-            "APOL5",
-            "ZNF280D",
-            "GTF2H1",
-            "WDR24",
-            "RNMT",
-            "IFNL3",
-            "SLC25A12",
-            "MCM9",
-            "ACTL9",
-            "FAM217B",
-            "RPRM",
-            "OR3A2",
-            "MCIDAS",
-            "EZR",
-            "HSDL2",
-            "OR10Z1",
-            "COL8A1",
-            "CIMAP2",
-            "POU4F2",
-            "CLN8",
-            "PDE11A",
-            "OR5D18",
-            "LRRC17",
-            "BCAP29",
-            "SMC1A",
-            "USP1",
-            "DEFB132",
-            "POLRMT",
-            "CDC25C",
-            "ZBP1",
-            "MRPS7",
-            "PELI1",
-            "GPN2",
-            "CCDC138",
-            "BHLHE22",
-            "INTS8",
-            "MPND",
-            "CDH11",
-            "JADE2",
-            "COIL",
-            "POU6F2",
-            "MCM3",
-            "SLC37A3",
-            "PHF1",
-            "FASTKD1",
-            "PLA1A",
-            "PCDH12",
-            "HLA-DPA1",
-            "LRTOMT",
-            "CCDC43",
-            "FNDC1",
-            "UNC119",
-            "KLK13",
-            "FBRSL1",
-            "SNED1",
-            "POTEG",
-            "LYZL6",
-            "ZGRF1",
-            "IFITM1",
-            "NUTM2F",
-            "C1S",
-            "IQSEC3",
-            "ARPC4-TTLL3",
-            "NOD1",
-            "RAB3D",
-            "LTB",
-            "CARD9",
-            "HMX3",
-            "ZNF584",
-            "NME6",
-            "HOXB1",
-            "TIMM50",
-            "PTGR1",
-            "SMAD5",
-            "EGLN1",
-            "LRRC3",
-            "E4F1",
-            "KRIT1",
-            "ZNF284",
-            "UTS2R",
-            "LPAR5",
-            "S1PR2",
-            "QRICH1",
-            "PERP",
-            "IFI35",
-            "DXO",
-            "TNFSF8",
-            "TGFBR3L",
-            "CHST1",
-            "BMP1",
-            "CSNK2A3",
-            "ETV5",
-            "FAM53B",
-            "RRP1B",
-            "CALCOCO2",
-            "PRKCE",
-            "PPP4R4",
-            "SPOCK3",
-            "UBTD2",
-            "LAS1L",
-            "ZFP82",
-            "ADRA2B",
-            "CXXC1",
-            "VBP1",
-            "LXN",
-            "OR51G2",
-            "CTC1",
-            "MTCH2",
-            "SERINC2",
-            "FAM185A",
-            "SLC6A4",
-            "ABO"
+            "ATP6V1E1",
+            "MON1A",
+            "EIF5A",
+            "SP140L",
+            "PLEKHF2",
+            "CLPSL2",
+            "SLC6A8",
+            "TMC3",
+            "AMY1B",
+            "TRARG1",
+            "SELENOP",
+            "PMEPA1",
+            "YIPF4",
+            "SERF1A",
+            "PTPRC",
+            "GABRA4",
+            "C2orf68",
+            "CRLS1",
+            "DENND4B",
+            "POM121L2",
+            "EXOC4",
+            "CLK2",
+            "FAM9B",
+            "TPRA1",
+            "TIMP3",
+            "DLX1",
+            "PRR20A",
+            "TMPRSS11B",
+            "MAP3K5",
+            "GET3",
+            "POU2F1",
+            "CALHM1",
+            "BRCA2",
+            "C9orf78",
+            "GMPR",
+            "CA14",
+            "FFAR1",
+            "MXRA5",
+            "MC5R",
+            "CD5",
+            "TTC4",
+            "COQ9",
+            "C9orf50",
+            "CLDN25",
+            "SMIM8",
+            "ODAPH",
+            "NonTarget.CTRL95",
+            "UCK2",
+            "SH3GL1",
+            "FGFR1OP2",
+            "DHRS2",
+            "CDK11B",
+            "NTRK2",
+            "BTBD1",
+            "MAB21L1",
+            "PLA2G6",
+            "GLUL",
+            "CCDC187",
+            "ZFP1",
+            "CUTC",
+            "MYH1",
+            "TIAM2",
+            "PGPEP1",
+            "SERAC1",
+            "B4GALT6",
+            "STAMBPL1",
+            "RNF167",
+            "CENPN",
+            "PDRG1",
+            "DIABLO",
+            "CFAP299",
+            "EXTL2",
+            "NEURL2",
+            "CSGALNACT2",
+            "UTP3",
+            "S100A13",
+            "SLC10A7",
+            "ATP5PO",
+            "ENDOD1",
+            "ABHD14B",
+            "CR1L",
+            "DENND1B",
+            "DHDH",
+            "ZNF350",
+            "SLC35G5",
+            "TPP2",
+            "ANGEL1",
+            "SPEM1",
+            "ZDHHC4",
+            "STBD1",
+            "DLK2",
+            "ZER1",
+            "FYCO1",
+            "WNT2",
+            "ADAMTS9",
+            "VWF",
+            "MFAP1",
+            "TXNDC17",
+            "SNF8",
+            "NLRP1",
+            "CDH10",
+            "RGL1",
+            "ZNF808",
+            "SPAM1",
+            "ZNF469",
+            "USP18",
+            "ZNF814",
+            "DPP3",
+            "FARP1",
+            "TRPM4",
+            "PRCP",
+            "CAND1",
+            "IGFBP2",
+            "CLMN",
+            "PSMC4",
+            "SNX27",
+            "CCL17",
+            "CDK2AP1",
+            "ARL16",
+            "CD47",
+            "CA4",
+            "CAPZA2",
+            "PDCD7",
+            "FBXL18",
+            "ECHDC3",
+            "TUBB2B",
+            "SIVA1",
+            "WFDC8"
           ],
           "selected_scores": [
-            -0.12966,
-            0.10238,
-            0.030073,
-            -0.1668,
-            -0.18023,
-            -0.04133,
-            -0.094579,
-            -0.19475,
-            -0.035481,
-            -0.16498,
-            -0.47401,
-            -0.0014975,
-            0.077615,
-            0.30811,
-            0.027915,
-            0.32316,
-            0.15146,
-            0.19312,
-            0.066402,
-            0.25827,
-            0.17691,
-            0.15437,
-            -0.0409,
-            0.13342,
-            0.09746,
-            0.11815,
-            -0.09576,
-            0.1804,
-            -0.064846,
-            0.051338,
-            -0.038049,
-            0.10104,
-            -0.029402,
-            -0.031647,
-            0.24683,
-            0.022065,
-            0.2464,
-            -0.036079,
-            0.063089,
-            -0.18674,
-            0.058556,
-            -0.057823,
-            -0.11005,
-            0.11097,
-            -0.037071,
-            -0.04,
-            0.078211,
-            0.028462,
-            0.13921,
-            0.065409,
-            -0.09801,
-            -0.20387,
-            -0.038419,
-            0.085857,
-            0.27221,
-            -0.18843,
-            -0.14212,
-            0.15926,
-            0.14003,
-            0.046076,
-            -0.15487,
-            0.041628,
-            0.30732,
-            -0.34454,
-            0.14498,
-            0.20342,
-            0.32899,
-            0.16335,
-            0.19205,
-            0.17804,
-            -0.20528,
-            0.21909,
-            0.022274,
-            -0.09377,
-            -0.2055,
-            0.056891,
-            0.18327,
-            0.046515,
-            0.027792,
-            -0.18365,
-            0.2332,
-            -0.13657,
-            -0.22407,
-            -0.09499,
-            -0.13782,
-            -0.083038,
-            -0.12558,
-            -0.27507,
-            0.15051,
-            -0.18691,
-            0.19385,
-            -0.0070939,
-            0.0095273,
-            -0.18255,
-            -0.13206,
-            -0.32043,
-            0.16689,
-            -0.15072,
-            -0.090926,
-            -0.04397,
-            0.030184,
-            0.20724,
-            -0.015146,
-            -0.33596,
-            0.24443,
-            0.072848,
-            -0.041738,
-            0.059629,
-            0.049745,
-            0.21357,
-            0.19982,
-            0.088743,
-            0.072569,
-            -0.056925,
-            0.051937,
-            -0.15746,
-            -0.10838,
-            0.061005,
-            0.074451,
-            -0.013253,
-            0.12194,
-            -0.068408,
-            -0.085898,
-            0.026809,
-            0.083967,
-            -0.010977,
-            0.0127,
-            -0.037216
+            0.045874,
+            -0.24772,
+            0.22815,
+            0.078495,
+            -0.023711,
+            0.14989,
+            -0.22267,
+            0.044808,
+            0.052605,
+            0.30501,
+            0.0134015,
+            -0.122093,
+            -0.21191,
+            0.25029,
+            -0.28242,
+            -0.080544,
+            -0.020633,
+            0.15191,
+            0.16249,
+            0.2843,
+            -0.0041473,
+            -0.35613,
+            -0.10442,
+            -0.16902,
+            0.033329,
+            0.01813,
+            0.060526,
+            -0.24971,
+            -0.082904,
+            -0.14026,
+            -0.43957,
+            -0.22231,
+            0.073084,
+            -0.13503,
+            -0.045694,
+            -0.14264,
+            -0.01248,
+            0.031039,
+            -0.28603,
+            0.080001,
+            -0.035282,
+            -0.17211,
+            0.36936,
+            -0.16321,
+            0.004964,
+            0.080498,
+            0.049269,
+            -0.039443,
+            -0.072301,
+            0.017969,
+            0.14619,
+            0.037942,
+            0.14333,
+            -0.43089,
+            0.07773,
+            -0.027941,
+            0.088831,
+            0.023173,
+            -0.014842,
+            -0.18485,
+            0.17845,
+            0.27459,
+            0.0388275,
+            -0.035284,
+            0.078371,
+            0.047768,
+            0.19611,
+            0.15354,
+            -0.014472,
+            0.073076,
+            -0.00070511,
+            0.045831,
+            -0.22225,
+            -0.046169,
+            -0.046037,
+            -0.21237,
+            0.19453,
+            0.082329,
+            0.20888,
+            0.023426,
+            -0.18867,
+            0.023313,
+            0.09446,
+            -0.039011,
+            0.16566,
+            0.24338,
+            -0.13474,
+            0.29424,
+            -0.043506,
+            -0.068879,
+            0.10306,
+            0.016376,
+            -0.14937,
+            0.12185,
+            -0.27175,
+            -0.1986,
+            -0.15274,
+            0.11567,
+            -0.082349,
+            -0.56947,
+            -0.095898,
+            0.065055,
+            -0.021356,
+            0.063423,
+            -0.051998,
+            0.11306,
+            0.086018,
+            -0.1326,
+            -0.19461,
+            0.031861,
+            0.23864,
+            -0.0682,
+            -0.21138,
+            -0.15263,
+            -0.20681,
+            0.05235,
+            -0.19129,
+            -0.2877,
+            0.21682,
+            0.02847,
+            -0.026209,
+            -0.14898,
+            0.14103,
+            -0.023129,
+            0.12136,
+            0.032747,
+            0.23603,
+            0.039682
           ],
           "selected_hits": [
             0,
@@ -311,6 +311,17 @@
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
             1,
             0,
             0,
@@ -320,50 +331,6 @@
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
             1,
             0,
             0,
@@ -376,31 +343,64 @@
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
           "score": -0.037216,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 1271,
+          "gene": "ATP6V1E1",
+          "score": 0.045874,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9447,
+          "gene": "MON1A",
+          "score": -0.24772,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4751,
+          "gene": "EIF5A",
+          "score": 0.22815,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15266,
+          "gene": "SP140L",
+          "score": 0.078495,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12209,
+          "gene": "PLEKHF2",
+          "score": -0.023711,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3178,
+          "gene": "CLPSL2",
+          "score": 0.14989,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14957,
+          "gene": "SLC6A8",
+          "score": -0.22267,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16440,
+          "gene": "TMC3",
+          "score": 0.044808,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 630,
+          "gene": "AMY1B",
+          "score": 0.052605,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16960,
+          "gene": "TRARG1",
+          "score": 0.30501,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14271,
+          "gene": "SELENOP",
+          "score": 0.0134015,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12290,
+          "gene": "PMEPA1",
+          "score": -0.122093,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18045,
+          "gene": "YIPF4",
+          "score": -0.21191,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14326,
+          "gene": "SERF1A",
+          "score": 0.25029,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13004,
+          "gene": "PTPRC",
+          "score": -0.28242,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5816,
+          "gene": "GABRA4",
+          "score": -0.080544,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1903,
+          "gene": "C2orf68",
+          "score": -0.020633,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3542,
+          "gene": "CRLS1",
+          "score": 0.15191,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4112,
+          "gene": "DENND4B",
+          "score": 0.16249,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12406,
+          "gene": "POM121L2",
+          "score": 0.2843,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5064,
+          "gene": "EXOC4",
+          "score": -0.0041473,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3159,
+          "gene": "CLK2",
+          "score": -0.35613,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 5303,
+          "gene": "FAM9B",
+          "score": -0.10442,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16906,
+          "gene": "TPRA1",
+          "score": -0.16902,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16365,
+          "gene": "TIMP3",
+          "score": 0.033329,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4248,
+          "gene": "DLX1",
+          "score": 0.01813,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12771,
+          "gene": "PRR20A",
+          "score": 0.060526,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16716,
+          "gene": "TMPRSS11B",
+          "score": -0.24971,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8979,
+          "gene": "MAP3K5",
+          "score": -0.082904,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6001,
+          "gene": "GET3",
+          "score": -0.14026,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12442,
+          "gene": "POU2F1",
+          "score": -0.43957,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2094,
+          "gene": "CALHM1",
+          "score": -0.22231,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1614,
+          "gene": "BRCA2",
+          "score": 0.073084,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2017,
+          "gene": "C9orf78",
+          "score": -0.13503,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6158,
+          "gene": "GMPR",
+          "score": -0.045694,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2024,
+          "gene": "CA14",
+          "score": -0.14264,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5472,
+          "gene": "FFAR1",
+          "score": -0.01248,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9780,
+          "gene": "MXRA5",
+          "score": 0.031039,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9090,
+          "gene": "MC5R",
+          "score": -0.28603,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2540,
+          "gene": "CD5",
+          "score": 0.080001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17228,
+          "gene": "TTC4",
+          "score": -0.035282,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3402,
+          "gene": "COQ9",
+          "score": -0.17211,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2012,
+          "gene": "C9orf50",
+          "score": 0.36936,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3105,
+          "gene": "CLDN25",
+          "score": -0.16321,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15097,
+          "gene": "SMIM8",
+          "score": 0.004964,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10934,
+          "gene": "ODAPH",
+          "score": 0.080498,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10898,
+          "gene": "NonTarget.CTRL95",
+          "score": 0.049269,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17446,
+          "gene": "UCK2",
+          "score": -0.039443,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14482,
+          "gene": "SH3GL1",
+          "score": -0.072301,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5508,
+          "gene": "FGFR1OP2",
+          "score": 0.017969,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4170,
+          "gene": "DHRS2",
+          "score": 0.14619,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2644,
+          "gene": "CDK11B",
+          "score": 0.037942,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10548,
+          "gene": "NTRK2",
+          "score": 0.14333,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1652,
+          "gene": "BTBD1",
+          "score": -0.43089,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 8854,
+          "gene": "MAB21L1",
+          "score": 0.07773,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12149,
+          "gene": "PLA2G6",
+          "score": -0.027941,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6138,
+          "gene": "GLUL",
+          "score": 0.088831,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2320,
+          "gene": "CCDC187",
+          "score": 0.023173,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18209,
+          "gene": "ZFP1",
+          "score": -0.014842,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3741,
+          "gene": "CUTC",
+          "score": -0.18485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9808,
+          "gene": "MYH1",
+          "score": 0.17845,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16329,
+          "gene": "TIAM2",
+          "score": 0.27459,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11934,
+          "gene": "PGPEP1",
+          "score": 0.0388275,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14324,
+          "gene": "SERAC1",
+          "score": -0.035284,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1362,
+          "gene": "B4GALT6",
+          "score": 0.078371,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15612,
+          "gene": "STAMBPL1",
+          "score": 0.047768,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13694,
+          "gene": "RNF167",
+          "score": 0.19611,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2758,
+          "gene": "CENPN",
+          "score": 0.15354,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11819,
+          "gene": "PDRG1",
+          "score": -0.014472,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4197,
+          "gene": "DIABLO",
+          "score": 0.073076,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2843,
+          "gene": "CFAP299",
+          "score": -0.00070511,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5085,
+          "gene": "EXTL2",
+          "score": 0.045831,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10152,
+          "gene": "NEURL2",
+          "score": -0.22225,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3595,
+          "gene": "CSGALNACT2",
+          "score": -0.046169,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17655,
+          "gene": "UTP3",
+          "score": -0.046037,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14020,
+          "gene": "S100A13",
+          "score": -0.21237,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14622,
+          "gene": "SLC10A7",
+          "score": 0.19453,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1252,
+          "gene": "ATP5PO",
+          "score": 0.082329,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4837,
+          "gene": "ENDOD1",
+          "score": 0.20888,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 82,
+          "gene": "ABHD14B",
+          "score": 0.023426,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3491,
+          "gene": "CR1L",
+          "score": -0.18867,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4104,
+          "gene": "DENND1B",
+          "score": 0.023313,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4160,
+          "gene": "DHDH",
+          "score": 0.09446,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18432,
+          "gene": "ZNF350",
+          "score": -0.039011,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14849,
+          "gene": "SLC35G5",
+          "score": 0.16566,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16901,
+          "gene": "TPP2",
+          "score": 0.24338,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 647,
+          "gene": "ANGEL1",
+          "score": -0.13474,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15371,
+          "gene": "SPEM1",
+          "score": 0.29424,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18188,
+          "gene": "ZDHHC4",
+          "score": -0.043506,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15634,
+          "gene": "STBD1",
+          "score": -0.068879,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4243,
+          "gene": "DLK2",
+          "score": 0.10306,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18196,
+          "gene": "ZER1",
+          "score": 0.016376,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5781,
+          "gene": "FYCO1",
+          "score": -0.14937,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17944,
+          "gene": "WNT2",
+          "score": 0.12185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 283,
+          "gene": "ADAMTS9",
+          "score": -0.27175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17820,
+          "gene": "VWF",
+          "score": -0.1986,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9251,
+          "gene": "MFAP1",
+          "score": -0.15274,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17316,
+          "gene": "TXNDC17",
+          "score": 0.11567,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15148,
+          "gene": "SNF8",
+          "score": -0.082349,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10287,
+          "gene": "NLRP1",
+          "score": -0.56947,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2613,
+          "gene": "CDH10",
+          "score": -0.095898,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13501,
+          "gene": "RGL1",
+          "score": 0.065055,
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
+          "candidate_index": 15295,
+          "gene": "SPAM1",
+          "score": 0.063423,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18497,
+          "gene": "ZNF469",
+          "score": -0.051998,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17602,
+          "gene": "USP18",
+          "score": 0.11306,
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
+          "candidate_index": 4424,
+          "gene": "DPP3",
+          "score": -0.1326,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5321,
+          "gene": "FARP1",
+          "score": -0.19461,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17105,
+          "gene": "TRPM4",
+          "score": 0.031861,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12626,
+          "gene": "PRCP",
+          "score": 0.23864,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2131,
+          "gene": "CAND1",
+          "score": -0.0682,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7259,
+          "gene": "IGFBP2",
+          "score": -0.21138,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3164,
+          "gene": "CLMN",
+          "score": -0.15263,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12893,
+          "gene": "PSMC4",
+          "score": -0.20681,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15198,
+          "gene": "SNX27",
+          "score": 0.05235,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2399,
+          "gene": "CCL17",
+          "score": -0.19129,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2655,
+          "gene": "CDK2AP1",
+          "score": -0.2877,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1001,
+          "gene": "ARL16",
+          "score": 0.21682,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2538,
+          "gene": "CD47",
+          "score": 0.02847,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2027,
+          "gene": "CA4",
+          "score": -0.026209,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2156,
+          "gene": "CAPZA2",
+          "score": -0.14898,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11758,
+          "gene": "PDCD7",
+          "score": 0.14103,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5361,
+          "gene": "FBXL18",
+          "score": -0.023129,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4595,
+          "gene": "ECHDC3",
+          "score": 0.12136,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17270,
+          "gene": "TUBB2B",
+          "score": 0.032747,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14586,
+          "gene": "SIVA1",
+          "score": 0.23603,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17919,
+          "gene": "WFDC8",
+          "score": 0.039682,
+          "hit": 0,
+          "round": 1
         }
       ],
       "queried_history": [
@@ -2226,6 +3122,902 @@
           "score": -0.037216,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 1271,
+          "gene": "ATP6V1E1",
+          "score": 0.045874,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9447,
+          "gene": "MON1A",
+          "score": -0.24772,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4751,
+          "gene": "EIF5A",
+          "score": 0.22815,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15266,
+          "gene": "SP140L",
+          "score": 0.078495,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12209,
+          "gene": "PLEKHF2",
+          "score": -0.023711,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3178,
+          "gene": "CLPSL2",
+          "score": 0.14989,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14957,
+          "gene": "SLC6A8",
+          "score": -0.22267,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16440,
+          "gene": "TMC3",
+          "score": 0.044808,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 630,
+          "gene": "AMY1B",
+          "score": 0.052605,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16960,
+          "gene": "TRARG1",
+          "score": 0.30501,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14271,
+          "gene": "SELENOP",
+          "score": 0.0134015,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12290,
+          "gene": "PMEPA1",
+          "score": -0.122093,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18045,
+          "gene": "YIPF4",
+          "score": -0.21191,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14326,
+          "gene": "SERF1A",
+          "score": 0.25029,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13004,
+          "gene": "PTPRC",
+          "score": -0.28242,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5816,
+          "gene": "GABRA4",
+          "score": -0.080544,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1903,
+          "gene": "C2orf68",
+          "score": -0.020633,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3542,
+          "gene": "CRLS1",
+          "score": 0.15191,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4112,
+          "gene": "DENND4B",
+          "score": 0.16249,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12406,
+          "gene": "POM121L2",
+          "score": 0.2843,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5064,
+          "gene": "EXOC4",
+          "score": -0.0041473,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3159,
+          "gene": "CLK2",
+          "score": -0.35613,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 5303,
+          "gene": "FAM9B",
+          "score": -0.10442,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16906,
+          "gene": "TPRA1",
+          "score": -0.16902,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16365,
+          "gene": "TIMP3",
+          "score": 0.033329,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4248,
+          "gene": "DLX1",
+          "score": 0.01813,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12771,
+          "gene": "PRR20A",
+          "score": 0.060526,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16716,
+          "gene": "TMPRSS11B",
+          "score": -0.24971,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8979,
+          "gene": "MAP3K5",
+          "score": -0.082904,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6001,
+          "gene": "GET3",
+          "score": -0.14026,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12442,
+          "gene": "POU2F1",
+          "score": -0.43957,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2094,
+          "gene": "CALHM1",
+          "score": -0.22231,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1614,
+          "gene": "BRCA2",
+          "score": 0.073084,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2017,
+          "gene": "C9orf78",
+          "score": -0.13503,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6158,
+          "gene": "GMPR",
+          "score": -0.045694,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2024,
+          "gene": "CA14",
+          "score": -0.14264,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5472,
+          "gene": "FFAR1",
+          "score": -0.01248,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9780,
+          "gene": "MXRA5",
+          "score": 0.031039,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9090,
+          "gene": "MC5R",
+          "score": -0.28603,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2540,
+          "gene": "CD5",
+          "score": 0.080001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17228,
+          "gene": "TTC4",
+          "score": -0.035282,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3402,
+          "gene": "COQ9",
+          "score": -0.17211,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2012,
+          "gene": "C9orf50",
+          "score": 0.36936,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3105,
+          "gene": "CLDN25",
+          "score": -0.16321,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15097,
+          "gene": "SMIM8",
+          "score": 0.004964,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10934,
+          "gene": "ODAPH",
+          "score": 0.080498,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10898,
+          "gene": "NonTarget.CTRL95",
+          "score": 0.049269,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17446,
+          "gene": "UCK2",
+          "score": -0.039443,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14482,
+          "gene": "SH3GL1",
+          "score": -0.072301,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5508,
+          "gene": "FGFR1OP2",
+          "score": 0.017969,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4170,
+          "gene": "DHRS2",
+          "score": 0.14619,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2644,
+          "gene": "CDK11B",
+          "score": 0.037942,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10548,
+          "gene": "NTRK2",
+          "score": 0.14333,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1652,
+          "gene": "BTBD1",
+          "score": -0.43089,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 8854,
+          "gene": "MAB21L1",
+          "score": 0.07773,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12149,
+          "gene": "PLA2G6",
+          "score": -0.027941,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6138,
+          "gene": "GLUL",
+          "score": 0.088831,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2320,
+          "gene": "CCDC187",
+          "score": 0.023173,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18209,
+          "gene": "ZFP1",
+          "score": -0.014842,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3741,
+          "gene": "CUTC",
+          "score": -0.18485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9808,
+          "gene": "MYH1",
+          "score": 0.17845,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16329,
+          "gene": "TIAM2",
+          "score": 0.27459,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11934,
+          "gene": "PGPEP1",
+          "score": 0.0388275,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14324,
+          "gene": "SERAC1",
+          "score": -0.035284,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1362,
+          "gene": "B4GALT6",
+          "score": 0.078371,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15612,
+          "gene": "STAMBPL1",
+          "score": 0.047768,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13694,
+          "gene": "RNF167",
+          "score": 0.19611,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2758,
+          "gene": "CENPN",
+          "score": 0.15354,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11819,
+          "gene": "PDRG1",
+          "score": -0.014472,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4197,
+          "gene": "DIABLO",
+          "score": 0.073076,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2843,
+          "gene": "CFAP299",
+          "score": -0.00070511,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5085,
+          "gene": "EXTL2",
+          "score": 0.045831,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10152,
+          "gene": "NEURL2",
+          "score": -0.22225,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3595,
+          "gene": "CSGALNACT2",
+          "score": -0.046169,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17655,
+          "gene": "UTP3",
+          "score": -0.046037,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14020,
+          "gene": "S100A13",
+          "score": -0.21237,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14622,
+          "gene": "SLC10A7",
+          "score": 0.19453,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1252,
+          "gene": "ATP5PO",
+          "score": 0.082329,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4837,
+          "gene": "ENDOD1",
+          "score": 0.20888,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 82,
+          "gene": "ABHD14B",
+          "score": 0.023426,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3491,
+          "gene": "CR1L",
+          "score": -0.18867,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4104,
+          "gene": "DENND1B",
+          "score": 0.023313,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4160,
+          "gene": "DHDH",
+          "score": 0.09446,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18432,
+          "gene": "ZNF350",
+          "score": -0.039011,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14849,
+          "gene": "SLC35G5",
+          "score": 0.16566,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16901,
+          "gene": "TPP2",
+          "score": 0.24338,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 647,
+          "gene": "ANGEL1",
+          "score": -0.13474,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15371,
+          "gene": "SPEM1",
+          "score": 0.29424,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18188,
+          "gene": "ZDHHC4",
+          "score": -0.043506,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15634,
+          "gene": "STBD1",
+          "score": -0.068879,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4243,
+          "gene": "DLK2",
+          "score": 0.10306,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18196,
+          "gene": "ZER1",
+          "score": 0.016376,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5781,
+          "gene": "FYCO1",
+          "score": -0.14937,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17944,
+          "gene": "WNT2",
+          "score": 0.12185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 283,
+          "gene": "ADAMTS9",
+          "score": -0.27175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17820,
+          "gene": "VWF",
+          "score": -0.1986,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9251,
+          "gene": "MFAP1",
+          "score": -0.15274,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17316,
+          "gene": "TXNDC17",
+          "score": 0.11567,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15148,
+          "gene": "SNF8",
+          "score": -0.082349,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10287,
+          "gene": "NLRP1",
+          "score": -0.56947,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2613,
+          "gene": "CDH10",
+          "score": -0.095898,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13501,
+          "gene": "RGL1",
+          "score": 0.065055,
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
+          "candidate_index": 15295,
+          "gene": "SPAM1",
+          "score": 0.063423,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18497,
+          "gene": "ZNF469",
+          "score": -0.051998,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17602,
+          "gene": "USP18",
+          "score": 0.11306,
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
+          "candidate_index": 4424,
+          "gene": "DPP3",
+          "score": -0.1326,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5321,
+          "gene": "FARP1",
+          "score": -0.19461,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17105,
+          "gene": "TRPM4",
+          "score": 0.031861,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12626,
+          "gene": "PRCP",
+          "score": 0.23864,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2131,
+          "gene": "CAND1",
+          "score": -0.0682,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7259,
+          "gene": "IGFBP2",
+          "score": -0.21138,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3164,
+          "gene": "CLMN",
+          "score": -0.15263,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12893,
+          "gene": "PSMC4",
+          "score": -0.20681,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15198,
+          "gene": "SNX27",
+          "score": 0.05235,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2399,
+          "gene": "CCL17",
+          "score": -0.19129,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2655,
+          "gene": "CDK2AP1",
+          "score": -0.2877,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1001,
+          "gene": "ARL16",
+          "score": 0.21682,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2538,
+          "gene": "CD47",
+          "score": 0.02847,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2027,
+          "gene": "CA4",
+          "score": -0.026209,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2156,
+          "gene": "CAPZA2",
+          "score": -0.14898,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11758,
+          "gene": "PDCD7",
+          "score": 0.14103,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5361,
+          "gene": "FBXL18",
+          "score": -0.023129,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4595,
+          "gene": "ECHDC3",
+          "score": 0.12136,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17270,
+          "gene": "TUBB2B",
+          "score": 0.032747,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14586,
+          "gene": "SIVA1",
+          "score": 0.23603,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17919,
+          "gene": "WFDC8",
+          "score": 0.039682,
+          "hit": 0,
+          "round": 1
         }
       ]
     }

```
