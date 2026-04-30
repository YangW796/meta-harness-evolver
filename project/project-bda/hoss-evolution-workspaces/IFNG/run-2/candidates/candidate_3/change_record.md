# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IFNG/run-2/best/current/harness
Generated at: 2026-04-30T07:12:02.825695

## Files Changed

- model.py: modified (added=2, deleted=2, delta=0)
- outputs/metrics.json: modified (added=2391, deleted=599, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -102,8 +102,8 @@
                     
                     # If we found diverse genes, include some in the selection
                     if diverse_available:
-                        # Take up to 40% of batch from diverse exploration
-                        num_diverse = min(len(diverse_available), batch_size * 2 // 5)
+                        # Take up to 60% of batch from diverse exploration
+                        num_diverse = min(len(diverse_available), batch_size * 3 // 5)
                         selected = diverse_available[:num_diverse]
                         remaining_batch = batch_size - len(selected)
                         

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,299 +9,313 @@
   "metrics": {
     "test": {
       "pool_size": 18418,
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
+      "delta_hits": 6,
+      "total_queries": 384,
+      "total_hits": 16,
       "top_k": 920,
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
+          16
         ]
       },
-      "auc": 768.0,
-      "auc_normalized": 0.003260869565217391,
-      "ncg": 0.14926231786886981,
+      "auc": 1664.0,
+      "auc_normalized": 0.004710144927536232,
+      "ncg": 0.18082586691885927,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 8,
-          "cumulative_hits": 10,
-          "precision_at_batch": 0.0625,
+          "hits": 6,
+          "cumulative_hits": 16,
+          "precision_at_batch": 0.046875,
           "selected": [
-            "GRB10",
-            "CHSY3",
-            "CDV3",
-            "TSEN54",
-            "MPZL3",
-            "STAT5A",
-            "LAMP1",
-            "TMCC1",
-            "GRPR",
-            "EPPIN",
-            "HM13",
-            "HOXA10",
-            "CACNA1B",
-            "HSPA1A",
-            "CELF3",
-            "PRDX4",
-            "HPD",
-            "GART",
-            "NDUFA4",
-            "PIMREG",
-            "FAM221B",
-            "ACTA2",
-            "NME6",
-            "MARCHF4",
-            "RAB11A",
-            "MMP1",
-            "LYRM4",
-            "CHRAC1",
-            "KCTD8",
-            "CEP97",
-            "ARSI",
-            "KCNQ5",
-            "OR9I1",
-            "ALYREF",
-            "ATP4A",
-            "EIF5A2",
-            "CACNA1A",
-            "GABRR3",
-            "EPB41L1",
-            "SEZ6",
-            "C3orf79",
-            "MRPL32",
-            "CMTM7",
-            "CRLF2",
-            "EDNRA",
-            "FAR2",
-            "PIEZO2",
-            "SLBP",
-            "B3GALNT2",
-            "GOLGA8O",
-            "AMOTL1",
-            "SERPINE3",
-            "RXFP4",
-            "ASIC3",
-            "CD207",
-            "GJB1",
-            "MAP3K21",
-            "FOXR2",
-            "PPA1",
-            "OXA1L",
-            "PCDHGB3",
-            "RIOX2",
-            "GABRG1",
-            "BBS12",
-            "KDM4C",
-            "RBM34",
-            "MRPL39",
-            "CRIP3",
-            "ZP3",
-            "FCMR",
-            "SP100",
-            "SAPCD2",
-            "ZPLD1",
-            "TOB2",
-            "OR10A4",
-            "MMP26",
-            "DAZAP1",
-            "BCKDHA",
-            "MS4A4E",
-            "COMMD5",
-            "TOGARAM2",
-            "PCDHB13",
-            "SLC35F5",
-            "CASP3",
-            "SNRPD3",
-            "RNASE10",
-            "CMPK2",
-            "CEACAM18",
-            "MTERF4",
-            "ZNF451",
-            "IQCN",
-            "FAM98B",
-            "DYRK1A",
-            "MSANTD3-TMEFF1",
-            "LUZP1",
-            "EXTL2",
-            "SPTB",
-            "POT1",
-            "KRTAP19-5",
-            "PTGFRN",
-            "EPM2A",
-            "ARHGEF38",
-            "ATMIN",
-            "CDH13",
-            "RPS26",
-            "NEK11",
-            "CARD18",
-            "PRDM10",
-            "FHIP2A",
-            "SRSF12",
-            "DSTN",
-            "SPON2",
-            "APOLD1",
-            "OLFM3",
-            "MARF1",
-            "RASGRP4",
-            "ERCC4",
-            "SDHC",
-            "OR2T4",
-            "ATP8A1",
-            "SLAIN2",
-            "COL7A1",
-            "PRR27",
-            "ERCC6L",
-            "CLEC14A",
-            "RSAD1",
-            "CCDC88A",
-            "LACTBL1"
+            "C9orf43",
+            "FLRT3",
+            "LCE5A",
+            "PRAMEF9",
+            "OR8I2",
+            "DAPP1",
+            "OXNAD1",
+            "OR2A1",
+            "DEAF1",
+            "TRAPPC10",
+            "POLDIP2",
+            "PLXNB1",
+            "OR10J3",
+            "HOXD8",
+            "OCLM",
+            "RPS27A",
+            "USP1",
+            "CPNE9",
+            "FDX1",
+            "SHANK2",
+            "KCNAB1",
+            "EPC2",
+            "COL10A1",
+            "SPCS3",
+            "SMPD2",
+            "TUT1",
+            "CETN2",
+            "SEMA3B",
+            "CCM2L",
+            "TMEM63B",
+            "AKR1C1",
+            "MYL12B",
+            "DCST2",
+            "GPALPP1",
+            "HIPK2",
+            "IFITM2",
+            "PGBD1",
+            "HSD17B7",
+            "OR10T2",
+            "CILP",
+            "SNAI3",
+            "OR4F4",
+            "KRT17",
+            "NDUFB7",
+            "CASQ2",
+            "LRRN4",
+            "FAM229B",
+            "ZNF652",
+            "FOXB1",
+            "KIF2A",
+            "HOMER2",
+            "AGPAT2",
+            "KCNG2",
+            "TRABD",
+            "CRYGB",
+            "GALR2",
+            "WDR55",
+            "IFI27L2",
+            "BRIP1",
+            "RLBP1",
+            "FAIM2",
+            "SLC5A3",
+            "NMNAT3",
+            "CSF2RB",
+            "PTCRA",
+            "RECQL5",
+            "STUB1",
+            "ZFY",
+            "ELAPOR1",
+            "CCDC177",
+            "MYCBPAP",
+            "TTC19",
+            "HLA-C",
+            "HS3ST4",
+            "ZFTA",
+            "FAM120AOS",
+            "HPDL",
+            "EDARADD",
+            "CTNNA3",
+            "TAS2R16",
+            "TMT1A",
+            "OR52N5",
+            "WDR25",
+            "L3MBTL1",
+            "PAPLN",
+            "PTPN6",
+            "SRSF4",
+            "KDM4A",
+            "FDCSP",
+            "PPP1R37",
+            "GPATCH2",
+            "TBPL1",
+            "SLC34A2",
+            "GIMAP8",
+            "DEFB115",
+            "STK19",
+            "CLCA4",
+            "TIAM1",
+            "DEPDC1B",
+            "FLT1",
+            "RPUSD1",
+            "POU2F3",
+            "WSCD2",
+            "OR8K3",
+            "DES",
+            "EBF2",
+            "ZSWIM4",
+            "CORO1B",
+            "PRDM12",
+            "OOEP",
+            "TMEM219",
+            "SLC25A24",
+            "SLC9A3",
+            "UBASH3A",
+            "RCL1",
+            "HADHA",
+            "WNK3",
+            "GTPBP2",
+            "CT83",
+            "CCL3L3",
+            "NUDT19",
+            "LOC339862",
+            "UHMK1",
+            "ANKRD24",
+            "RTRAF",
+            "BTN3A2",
+            "ERGIC2",
+            "KLF7"
           ],
           "selected_scores": [
-            -0.248375,
-            -0.412895,
-            -0.0747755,
-            -0.1799,
-            0.091062,
-            0.070219,
-            -0.250764,
-            -0.24566,
-            -0.34612,
-            0.1894457,
-            -0.1634025,
-            0.138547,
-            -0.018338,
-            -0.18896,
-            -0.209461,
-            -0.05254,
-            -0.0576055,
-            0.680965,
-            -0.0954025,
-            -0.067748,
-            0.15022,
-            0.0549595,
-            -0.143155,
-            -0.006445,
-            -0.36555,
-            -0.10929505,
-            -0.0324625,
-            0.0712425,
-            -0.149912,
-            0.151961,
-            -0.108513,
-            0.0243845,
-            -0.39658,
-            0.29792,
-            0.13117,
-            0.0379539,
-            -0.0910175,
-            0.01787,
-            0.11663,
-            0.30831,
-            0.029185,
-            -0.011175,
-            0.44058,
-            -0.05671,
-            0.313375,
-            -0.0430835,
-            0.113345,
-            0.31116,
-            -0.069145,
-            -0.21548,
-            -0.045733,
-            -0.20525,
-            -0.011635,
-            -0.08891,
-            0.082544,
-            -0.01148,
-            0.096635,
-            -0.077375,
-            0.037033,
-            -0.11009675,
-            0.0901975,
-            0.016995,
-            -0.1049975,
-            -0.09705,
-            -0.10772,
-            -0.088945,
-            0.096265,
-            0.156865,
-            0.179865,
-            -0.1574545,
-            0.35942,
-            -0.016528,
-            0.26673,
-            0.3595075,
-            -0.35446,
-            -0.447885,
-            0.058625,
-            0.0544845,
-            0.197935,
-            -0.170365,
-            0.0094185,
-            0.05577,
-            -0.009455,
-            -0.27373,
-            -0.0978905,
-            0.1520625,
-            0.338575,
-            -0.0762515,
-            -0.1273965,
-            -0.06424,
-            0.032715,
-            0.036453,
-            -0.53973,
-            -0.062495,
-            0.165695,
-            0.1882635,
-            0.1158745,
-            0.05799565,
-            -0.24164,
-            0.02096,
-            0.21128,
-            -0.1083765,
-            0.1215055,
-            -0.1230715,
-            -0.042948,
-            0.104762,
-            0.1253575,
-            0.054417,
-            -0.060856,
-            0.34673,
-            -0.121887,
-            -0.1191485,
-            0.1369725,
-            -0.001175,
-            -0.178513,
-            0.01226,
-            0.1543335,
-            0.5242,
-            -0.1580005,
-            -0.244146,
-            0.067428,
-            -0.268605,
-            0.210485,
-            0.07,
-            -0.20048,
-            0.400445,
-            0.162785,
-            0.080435
+            -0.121209,
+            -0.342325,
+            -0.106373,
+            0.22872,
+            -0.0619,
+            -0.153128,
+            0.1366305,
+            0.0972775,
+            0.3774842,
+            0.13969,
+            0.26151,
+            0.0057805,
+            0.21113,
+            0.173175,
+            -0.021735,
+            0.586065,
+            0.23304,
+            0.03956,
+            -0.059622,
+            0.245764,
+            0.0267669,
+            0.255006,
+            0.09023,
+            -0.73383,
+            -0.1506315,
+            0.34309,
+            0.017013,
+            0.038255,
+            -0.107333,
+            0.022489,
+            0.0594665,
+            -0.01441,
+            -0.017094,
+            0.248535,
+            0.0237305,
+            0.17169,
+            0.07664085,
+            0.0491875,
+            -0.018596,
+            -0.00866,
+            0.180015,
+            -0.060785,
+            -0.101185,
+            -0.29093,
+            0.06984,
+            -0.5025,
+            0.0503065,
+            0.1074805,
+            0.033265,
+            -0.097671,
+            -0.05724825,
+            0.220305,
+            -0.059309,
+            -0.02693,
+            -0.0725975,
+            -0.352975,
+            0.0017455,
+            -0.064292,
+            0.06074125,
+            0.1716665,
+            -0.169465,
+            0.0183725,
+            -0.18652,
+            0.1318105,
+            -0.188151,
+            -0.05877,
+            0.071698,
+            -0.1789355,
+            0.0777455,
+            0.231777,
+            0.380385,
+            0.0648395,
+            -0.159725,
+            0.10231,
+            0.295155,
+            -0.008135,
+            0.16511,
+            -0.189085,
+            -0.1643525,
+            0.16296,
+            0.16839,
+            0.1934785,
+            0.2083875,
+            -0.065173,
+            0.26057,
+            0.247855,
+            -0.121985,
+            -0.0238664,
+            0.029475,
+            0.009535,
+            0.2751515,
+            0.1815968,
+            -0.232403,
+            -0.12592,
+            -0.292765,
+            -0.223335,
+            -0.132371,
+            0.16909,
+            0.04660265,
+            -0.187085,
+            0.1830785,
+            0.0138355,
+            -0.028234,
+            -0.128625,
+            -0.49181,
+            -0.106032,
+            -0.2097455,
+            -0.28897,
+            -0.007624,
+            0.28676,
+            0.17395675,
+            0.421035,
+            -0.15355,
+            0.347969,
+            0.887835,
+            -0.1265685,
+            -0.134325,
+            -0.17266345,
+            -0.0519932,
+            0.29666,
+            -0.15354745,
+            0.072995,
+            0.0180035,
+            -0.05942,
+            -0.1060871,
+            0.1734735,
+            -0.01648,
+            -0.0773255
           ],
           "selected_hits": [
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
             1,
             0,
             0,
@@ -310,14 +324,6 @@
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
             0,
             0,
@@ -333,6 +339,13 @@
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
             1,
             0,
             0,
@@ -343,6 +356,55 @@
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
@@ -350,49 +412,9 @@
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
             1,
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
             1,
             0,
             0,
@@ -405,28 +427,6 @@
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
-            1,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            1,
             0,
             0
           ]
@@ -1334,896 +1334,1792 @@
           "gene": "GRB10",
           "score": -0.248375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2982,
           "gene": "CHSY3",
           "score": -0.412895,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2681,
           "gene": "CDV3",
           "score": -0.0747755,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16710,
           "gene": "TSEN54",
           "score": -0.1799,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9420,
           "gene": "MPZL3",
           "score": 0.091062,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15222,
           "gene": "STAT5A",
           "score": 0.070219,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8172,
           "gene": "LAMP1",
           "score": -0.250764,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16035,
           "gene": "TMCC1",
           "score": -0.24566,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6383,
           "gene": "GRPR",
           "score": -0.34612,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4863,
           "gene": "EPPIN",
           "score": 0.1894457,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6793,
           "gene": "HM13",
           "score": -0.1634025,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6870,
           "gene": "HOXA10",
           "score": 0.138547,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2035,
           "gene": "CACNA1B",
           "score": -0.018338,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6983,
           "gene": "HSPA1A",
           "score": -0.18896,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2715,
           "gene": "CELF3",
           "score": -0.209461,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12273,
           "gene": "PRDX4",
           "score": -0.05254,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6909,
           "gene": "HPD",
           "score": -0.0576055,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5825,
           "gene": "GART",
           "score": 0.680965,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9984,
           "gene": "NDUFA4",
           "score": -0.0954025,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11718,
           "gene": "PIMREG",
           "score": -0.067748,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5171,
           "gene": "FAM221B",
           "score": 0.15022,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 198,
           "gene": "ACTA2",
           "score": 0.0549595,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10235,
           "gene": "NME6",
           "score": -0.143155,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8949,
           "gene": "MARCHF4",
           "score": -0.006445,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12715,
           "gene": "RAB11A",
           "score": -0.36555,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9318,
           "gene": "MMP1",
           "score": -0.10929505,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8751,
           "gene": "LYRM4",
           "score": -0.0324625,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2940,
           "gene": "CHRAC1",
           "score": 0.0712425,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7733,
           "gene": "KCTD8",
           "score": -0.149912,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2787,
           "gene": "CEP97",
           "score": 0.151961,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1064,
           "gene": "ARSI",
           "score": -0.108513,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7703,
           "gene": "KCNQ5",
           "score": 0.0243845,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11022,
           "gene": "OR9I1",
           "score": -0.39658,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 594,
           "gene": "ALYREF",
           "score": 0.29792,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1223,
           "gene": "ATP4A",
           "score": 0.13117,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4691,
           "gene": "EIF5A2",
           "score": 0.0379539,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2034,
           "gene": "CACNA1A",
           "score": -0.0910175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5760,
           "gene": "GABRR3",
           "score": 0.01787,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4825,
           "gene": "EPB41L1",
           "score": 0.11663,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14006,
           "gene": "SEZ6",
           "score": 0.30831,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1911,
           "gene": "C3orf79",
           "score": 0.029185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9475,
           "gene": "MRPL32",
           "score": -0.011175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3190,
           "gene": "CMTM7",
           "score": 0.44058,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3510,
           "gene": "CRLF2",
           "score": -0.05671,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4565,
           "gene": "EDNRA",
           "score": 0.313375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5251,
           "gene": "FAR2",
           "score": -0.0430835,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11671,
           "gene": "PIEZO2",
           "score": 0.113345,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14220,
           "gene": "SLBP",
           "score": 0.31116,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1327,
           "gene": "B3GALNT2",
           "score": -0.069145,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6158,
           "gene": "GOLGA8O",
           "score": -0.21548,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 617,
           "gene": "AMOTL1",
           "score": -0.045733,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13974,
           "gene": "SERPINE3",
           "score": -0.20525,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13614,
           "gene": "RXFP4",
           "score": -0.011635,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1117,
           "gene": "ASIC3",
           "score": -0.08891,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2484,
           "gene": "CD207",
           "score": 0.082544,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6000,
           "gene": "GJB1",
           "score": -0.01148,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8896,
           "gene": "MAP3K21",
           "score": 0.096635,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5611,
           "gene": "FOXR2",
           "score": -0.077375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12088,
           "gene": "PPA1",
           "score": 0.037033,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11100,
           "gene": "OXA1L",
           "score": -0.11009675,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11351,
           "gene": "PCDHGB3",
           "score": 0.0901975,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13216,
           "gene": "RIOX2",
           "score": 0.016995,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5753,
           "gene": "GABRG1",
           "score": -0.1049975,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1406,
           "gene": "BBS12",
           "score": -0.09705,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7747,
           "gene": "KDM4C",
           "score": -0.10772,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12956,
           "gene": "RBM34",
           "score": -0.088945,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9482,
           "gene": "MRPL39",
           "score": 0.096265,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3499,
           "gene": "CRIP3",
           "score": 0.156865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18367,
           "gene": "ZP3",
           "score": 0.179865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5368,
           "gene": "FCMR",
           "score": -0.1574545,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14863,
           "gene": "SP100",
           "score": 0.35942,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13690,
           "gene": "SAPCD2",
           "score": -0.016528,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18371,
           "gene": "ZPLD1",
           "score": 0.26673,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16408,
           "gene": "TOB2",
           "score": 0.3595075,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10662,
           "gene": "OR10A4",
           "score": -0.35446,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9333,
           "gene": "MMP26",
           "score": -0.447885,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3867,
           "gene": "DAZAP1",
           "score": 0.058625,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1427,
           "gene": "BCKDHA",
           "score": 0.0544845,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9545,
           "gene": "MS4A4E",
           "score": 0.197935,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3337,
           "gene": "COMMD5",
           "score": -0.170365,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16411,
           "gene": "TOGARAM2",
           "score": 0.0094185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11325,
           "gene": "PCDHB13",
           "score": 0.05577,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14448,
           "gene": "SLC35F5",
           "score": -0.009455,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2174,
           "gene": "CASP3",
           "score": -0.27373,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14768,
           "gene": "SNRPD3",
           "score": -0.0978905,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13246,
           "gene": "RNASE10",
           "score": 0.1520625,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3182,
           "gene": "CMPK2",
           "score": 0.338575,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2690,
           "gene": "CEACAM18",
           "score": -0.0762515,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9609,
           "gene": "MTERF4",
           "score": -0.1273965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18052,
           "gene": "ZNF451",
           "score": -0.06424,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7410,
           "gene": "IQCN",
           "score": 0.032715,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5231,
           "gene": "FAM98B",
           "score": 0.036453,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4498,
           "gene": "DYRK1A",
           "score": -0.53973,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9552,
           "gene": "MSANTD3-TMEFF1",
           "score": -0.062495,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8713,
           "gene": "LUZP1",
           "score": 0.165695,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5020,
           "gene": "EXTL2",
           "score": 0.1882635,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15061,
           "gene": "SPTB",
           "score": 0.1158745,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12057,
           "gene": "POT1",
           "score": 0.05799565,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8077,
           "gene": "KRTAP19-5",
           "score": -0.24164,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12578,
           "gene": "PTGFRN",
           "score": 0.02096,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4856,
           "gene": "EPM2A",
           "score": 0.21128,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 964,
           "gene": "ARHGEF38",
           "score": -0.1083765,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1186,
           "gene": "ATMIN",
           "score": 0.1215055,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2599,
           "gene": "CDH13",
           "score": -0.1230715,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13475,
           "gene": "RPS26",
           "score": -0.042948,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10046,
           "gene": "NEK11",
           "score": 0.104762,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2150,
           "gene": "CARD18",
           "score": 0.1253575,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12256,
           "gene": "PRDM10",
           "score": 0.054417,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5456,
           "gene": "FHIP2A",
           "score": -0.060856,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15121,
           "gene": "SRSF12",
           "score": 0.34673,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4422,
           "gene": "DSTN",
           "score": -0.121887,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15024,
           "gene": "SPON2",
           "score": -0.1191485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 865,
           "gene": "APOLD1",
           "score": 0.1369725,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10624,
           "gene": "OLFM3",
           "score": -0.001175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8958,
           "gene": "MARF1",
           "score": -0.178513,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12899,
           "gene": "RASGRP4",
           "score": 0.01226,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4888,
           "gene": "ERCC4",
           "score": 0.1543335,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13825,
           "gene": "SDHC",
           "score": 0.5242,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10798,
           "gene": "OR2T4",
           "score": -0.1580005,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1271,
           "gene": "ATP8A1",
           "score": -0.244146,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14214,
           "gene": "SLAIN2",
           "score": 0.067428,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3319,
           "gene": "COL7A1",
           "score": -0.268605,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12406,
           "gene": "PRR27",
           "score": 0.210485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4891,
           "gene": "ERCC6L",
           "score": 0.07,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3090,
           "gene": "CLEC14A",
           "score": -0.20048,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13530,
           "gene": "RSAD1",
           "score": 0.400445,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2357,
           "gene": "CCDC88A",
           "score": 0.162785,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8155,
           "gene": "LACTBL1",
           "score": 0.080435,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 1996,
+          "gene": "C9orf43",
+          "score": -0.121209,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5511,
+          "gene": "FLRT3",
+          "score": -0.342325,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8228,
+          "gene": "LCE5A",
+          "score": -0.106373,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12246,
+          "gene": "PRAMEF9",
+          "score": 0.22872,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11009,
+          "gene": "OR8I2",
+          "score": -0.0619,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3860,
+          "gene": "DAPP1",
+          "score": -0.153128,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11106,
+          "gene": "OXNAD1",
+          "score": 0.1366305,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10745,
+          "gene": "OR2A1",
+          "score": 0.0972775,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4001,
+          "gene": "DEAF1",
+          "score": 0.3774842,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16526,
+          "gene": "TRAPPC10",
+          "score": 0.13969,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11993,
+          "gene": "POLDIP2",
+          "score": 0.26151,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11916,
+          "gene": "PLXNB1",
+          "score": 0.0057805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10681,
+          "gene": "OR10J3",
+          "score": 0.21113,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6904,
+          "gene": "HOXD8",
+          "score": 0.173175,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10588,
+          "gene": "OCLM",
+          "score": -0.021735,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13477,
+          "gene": "RPS27A",
+          "score": 0.586065,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 17152,
+          "gene": "USP1",
+          "score": 0.23304,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3439,
+          "gene": "CPNE9",
+          "score": 0.03956,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5383,
+          "gene": "FDX1",
+          "score": -0.059622,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14104,
+          "gene": "SHANK2",
+          "score": 0.245764,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7626,
+          "gene": "KCNAB1",
+          "score": 0.0267669,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4833,
+          "gene": "EPC2",
+          "score": 0.255006,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3280,
+          "gene": "COL10A1",
+          "score": 0.09023,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14950,
+          "gene": "SPCS3",
+          "score": -0.73383,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 14709,
+          "gene": "SMPD2",
+          "score": -0.1506315,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16872,
+          "gene": "TUT1",
+          "score": 0.34309,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2804,
+          "gene": "CETN2",
+          "score": 0.017013,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13890,
+          "gene": "SEMA3B",
+          "score": 0.038255,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2402,
+          "gene": "CCM2L",
+          "score": -0.107333,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16256,
+          "gene": "TMEM63B",
+          "score": 0.022489,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 509,
+          "gene": "AKR1C1",
+          "score": 0.0594665,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9753,
+          "gene": "MYL12B",
+          "score": -0.01441,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3924,
+          "gene": "DCST2",
+          "score": -0.017094,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6185,
+          "gene": "GPALPP1",
+          "score": 0.248535,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6759,
+          "gene": "HIPK2",
+          "score": 0.0237305,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7108,
+          "gene": "IFITM2",
+          "score": 0.17169,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11562,
+          "gene": "PGBD1",
+          "score": 0.07664085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6960,
+          "gene": "HSD17B7",
+          "score": 0.0491875,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10689,
+          "gene": "OR10T2",
+          "score": -0.018596,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3005,
+          "gene": "CILP",
+          "score": -0.00866,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14731,
+          "gene": "SNAI3",
+          "score": 0.180015,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10837,
+          "gene": "OR4F4",
+          "score": -0.060785,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7998,
+          "gene": "KRT17",
+          "score": -0.101185,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10008,
+          "gene": "NDUFB7",
+          "score": -0.29093,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2183,
+          "gene": "CASQ2",
+          "score": 0.06984,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8659,
+          "gene": "LRRN4",
+          "score": -0.5025,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 5179,
+          "gene": "FAM229B",
+          "score": 0.0503065,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18193,
+          "gene": "ZNF652",
+          "score": 0.1074805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5566,
+          "gene": "FOXB1",
+          "score": 0.033265,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7826,
+          "gene": "KIF2A",
+          "score": -0.097671,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6860,
+          "gene": "HOMER2",
+          "score": -0.05724825,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 431,
+          "gene": "AGPAT2",
+          "score": 0.220305,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7645,
+          "gene": "KCNG2",
+          "score": -0.059309,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16504,
+          "gene": "TRABD",
+          "score": -0.02693,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3543,
+          "gene": "CRYGB",
+          "score": -0.0725975,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5802,
+          "gene": "GALR2",
+          "score": -0.352975,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17443,
+          "gene": "WDR55",
+          "score": 0.0017455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7094,
+          "gene": "IFI27L2",
+          "score": -0.064292,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1614,
+          "gene": "BRIP1",
+          "score": 0.06074125,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13230,
+          "gene": "RLBP1",
+          "score": 0.1716665,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5071,
+          "gene": "FAIM2",
+          "score": -0.169465,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14535,
+          "gene": "SLC5A3",
+          "score": 0.0183725,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10241,
+          "gene": "NMNAT3",
+          "score": -0.18652,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3563,
+          "gene": "CSF2RB",
+          "score": 0.1318105,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12560,
+          "gene": "PTCRA",
+          "score": -0.188151,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13031,
+          "gene": "RECQL5",
+          "score": -0.05877,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15301,
+          "gene": "STUB1",
+          "score": 0.071698,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17802,
+          "gene": "ZFY",
+          "score": -0.1789355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4699,
+          "gene": "ELAPOR1",
+          "score": 0.0777455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2294,
+          "gene": "CCDC177",
+          "score": 0.231777,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9725,
+          "gene": "MYCBPAP",
+          "score": 0.380385,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16784,
+          "gene": "TTC19",
+          "score": 0.0648395,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6772,
+          "gene": "HLA-C",
+          "score": -0.159725,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6939,
+          "gene": "HS3ST4",
+          "score": 0.10231,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17799,
+          "gene": "ZFTA",
+          "score": 0.295155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5089,
+          "gene": "FAM120AOS",
+          "score": -0.008135,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6910,
+          "gene": "HPDL",
+          "score": 0.16511,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4552,
+          "gene": "EDARADD",
+          "score": -0.189085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3649,
+          "gene": "CTNNA3",
+          "score": -0.1643525,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15558,
+          "gene": "TAS2R16",
+          "score": 0.16296,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16318,
+          "gene": "TMT1A",
+          "score": 0.16839,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10900,
+          "gene": "OR52N5",
+          "score": 0.1934785,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17420,
+          "gene": "WDR25",
+          "score": 0.2083875,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8147,
+          "gene": "L3MBTL1",
+          "score": -0.065173,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11208,
+          "gene": "PAPLN",
+          "score": 0.26057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12617,
+          "gene": "PTPN6",
+          "score": 0.247855,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15124,
+          "gene": "SRSF4",
+          "score": -0.121985,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7745,
+          "gene": "KDM4A",
+          "score": -0.0238664,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5380,
+          "gene": "FDCSP",
+          "score": 0.029475,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12171,
+          "gene": "PPP1R37",
+          "score": 0.009535,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6191,
+          "gene": "GPATCH2",
+          "score": 0.2751515,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15640,
+          "gene": "TBPL1",
+          "score": 0.1815968,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14423,
+          "gene": "SLC34A2",
+          "score": -0.232403,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5981,
+          "gene": "GIMAP8",
+          "score": -0.12592,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4024,
+          "gene": "DEFB115",
+          "score": -0.292765,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15250,
+          "gene": "STK19",
+          "score": -0.223335,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3048,
+          "gene": "CLCA4",
+          "score": -0.132371,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15917,
+          "gene": "TIAM1",
+          "score": 0.16909,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4068,
+          "gene": "DEPDC1B",
+          "score": 0.04660265,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5512,
+          "gene": "FLT1",
+          "score": -0.187085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13504,
+          "gene": "RPUSD1",
+          "score": 0.1830785,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12074,
+          "gene": "POU2F3",
+          "score": 0.0138355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17528,
+          "gene": "WSCD2",
+          "score": -0.028234,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11013,
+          "gene": "OR8K3",
+          "score": -0.128625,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4078,
+          "gene": "DES",
+          "score": -0.49181,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 4523,
+          "gene": "EBF2",
+          "score": -0.106032,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18400,
+          "gene": "ZSWIM4",
+          "score": -0.2097455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3376,
+          "gene": "CORO1B",
+          "score": -0.28897,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12258,
+          "gene": "PRDM12",
+          "score": -0.007624,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10640,
+          "gene": "OOEP",
+          "score": 0.28676,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16175,
+          "gene": "TMEM219",
+          "score": 0.17395675,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14337,
+          "gene": "SLC25A24",
+          "score": 0.421035,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 14583,
+          "gene": "SLC9A3",
+          "score": -0.15355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16941,
+          "gene": "UBASH3A",
+          "score": 0.347969,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13005,
+          "gene": "RCL1",
+          "score": 0.887835,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 6589,
+          "gene": "HADHA",
+          "score": -0.1265685,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17500,
+          "gene": "WNK3",
+          "score": -0.134325,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6454,
+          "gene": "GTPBP2",
+          "score": -0.17266345,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3622,
+          "gene": "CT83",
+          "score": -0.0519932,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2396,
+          "gene": "CCL3L3",
+          "score": 0.29666,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10498,
+          "gene": "NUDT19",
+          "score": -0.15354745,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8487,
+          "gene": "LOC339862",
+          "score": 0.072995,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17069,
+          "gene": "UHMK1",
+          "score": 0.0180035,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 692,
+          "gene": "ANKRD24",
+          "score": -0.05942,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13586,
+          "gene": "RTRAF",
+          "score": -0.1060871,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1663,
+          "gene": "BTN3A2",
+          "score": 0.1734735,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4899,
+          "gene": "ERGIC2",
+          "score": -0.01648,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7879,
+          "gene": "KLF7",
+          "score": -0.0773255,
+          "hit": 0,
+          "round": 2
         }
       ],
       "queried_history": [
@@ -3128,896 +4024,1792 @@
           "gene": "GRB10",
           "score": -0.248375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2982,
           "gene": "CHSY3",
           "score": -0.412895,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2681,
           "gene": "CDV3",
           "score": -0.0747755,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16710,
           "gene": "TSEN54",
           "score": -0.1799,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9420,
           "gene": "MPZL3",
           "score": 0.091062,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15222,
           "gene": "STAT5A",
           "score": 0.070219,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8172,
           "gene": "LAMP1",
           "score": -0.250764,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16035,
           "gene": "TMCC1",
           "score": -0.24566,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6383,
           "gene": "GRPR",
           "score": -0.34612,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4863,
           "gene": "EPPIN",
           "score": 0.1894457,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6793,
           "gene": "HM13",
           "score": -0.1634025,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6870,
           "gene": "HOXA10",
           "score": 0.138547,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2035,
           "gene": "CACNA1B",
           "score": -0.018338,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6983,
           "gene": "HSPA1A",
           "score": -0.18896,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2715,
           "gene": "CELF3",
           "score": -0.209461,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12273,
           "gene": "PRDX4",
           "score": -0.05254,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6909,
           "gene": "HPD",
           "score": -0.0576055,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5825,
           "gene": "GART",
           "score": 0.680965,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9984,
           "gene": "NDUFA4",
           "score": -0.0954025,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11718,
           "gene": "PIMREG",
           "score": -0.067748,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5171,
           "gene": "FAM221B",
           "score": 0.15022,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 198,
           "gene": "ACTA2",
           "score": 0.0549595,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10235,
           "gene": "NME6",
           "score": -0.143155,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8949,
           "gene": "MARCHF4",
           "score": -0.006445,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12715,
           "gene": "RAB11A",
           "score": -0.36555,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9318,
           "gene": "MMP1",
           "score": -0.10929505,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8751,
           "gene": "LYRM4",
           "score": -0.0324625,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2940,
           "gene": "CHRAC1",
           "score": 0.0712425,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7733,
           "gene": "KCTD8",
           "score": -0.149912,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2787,
           "gene": "CEP97",
           "score": 0.151961,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1064,
           "gene": "ARSI",
           "score": -0.108513,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7703,
           "gene": "KCNQ5",
           "score": 0.0243845,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11022,
           "gene": "OR9I1",
           "score": -0.39658,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 594,
           "gene": "ALYREF",
           "score": 0.29792,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1223,
           "gene": "ATP4A",
           "score": 0.13117,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4691,
           "gene": "EIF5A2",
           "score": 0.0379539,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2034,
           "gene": "CACNA1A",
           "score": -0.0910175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5760,
           "gene": "GABRR3",
           "score": 0.01787,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4825,
           "gene": "EPB41L1",
           "score": 0.11663,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14006,
           "gene": "SEZ6",
           "score": 0.30831,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1911,
           "gene": "C3orf79",
           "score": 0.029185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9475,
           "gene": "MRPL32",
           "score": -0.011175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3190,
           "gene": "CMTM7",
           "score": 0.44058,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3510,
           "gene": "CRLF2",
           "score": -0.05671,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4565,
           "gene": "EDNRA",
           "score": 0.313375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5251,
           "gene": "FAR2",
           "score": -0.0430835,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11671,
           "gene": "PIEZO2",
           "score": 0.113345,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14220,
           "gene": "SLBP",
           "score": 0.31116,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1327,
           "gene": "B3GALNT2",
           "score": -0.069145,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6158,
           "gene": "GOLGA8O",
           "score": -0.21548,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 617,
           "gene": "AMOTL1",
           "score": -0.045733,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13974,
           "gene": "SERPINE3",
           "score": -0.20525,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13614,
           "gene": "RXFP4",
           "score": -0.011635,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1117,
           "gene": "ASIC3",
           "score": -0.08891,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2484,
           "gene": "CD207",
           "score": 0.082544,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6000,
           "gene": "GJB1",
           "score": -0.01148,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8896,
           "gene": "MAP3K21",
           "score": 0.096635,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5611,
           "gene": "FOXR2",
           "score": -0.077375,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12088,
           "gene": "PPA1",
           "score": 0.037033,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11100,
           "gene": "OXA1L",
           "score": -0.11009675,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11351,
           "gene": "PCDHGB3",
           "score": 0.0901975,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13216,
           "gene": "RIOX2",
           "score": 0.016995,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5753,
           "gene": "GABRG1",
           "score": -0.1049975,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1406,
           "gene": "BBS12",
           "score": -0.09705,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7747,
           "gene": "KDM4C",
           "score": -0.10772,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12956,
           "gene": "RBM34",
           "score": -0.088945,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9482,
           "gene": "MRPL39",
           "score": 0.096265,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3499,
           "gene": "CRIP3",
           "score": 0.156865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18367,
           "gene": "ZP3",
           "score": 0.179865,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5368,
           "gene": "FCMR",
           "score": -0.1574545,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14863,
           "gene": "SP100",
           "score": 0.35942,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13690,
           "gene": "SAPCD2",
           "score": -0.016528,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18371,
           "gene": "ZPLD1",
           "score": 0.26673,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16408,
           "gene": "TOB2",
           "score": 0.3595075,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10662,
           "gene": "OR10A4",
           "score": -0.35446,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9333,
           "gene": "MMP26",
           "score": -0.447885,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3867,
           "gene": "DAZAP1",
           "score": 0.058625,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1427,
           "gene": "BCKDHA",
           "score": 0.0544845,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9545,
           "gene": "MS4A4E",
           "score": 0.197935,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3337,
           "gene": "COMMD5",
           "score": -0.170365,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16411,
           "gene": "TOGARAM2",
           "score": 0.0094185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11325,
           "gene": "PCDHB13",
           "score": 0.05577,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14448,
           "gene": "SLC35F5",
           "score": -0.009455,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2174,
           "gene": "CASP3",
           "score": -0.27373,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14768,
           "gene": "SNRPD3",
           "score": -0.0978905,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13246,
           "gene": "RNASE10",
           "score": 0.1520625,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3182,
           "gene": "CMPK2",
           "score": 0.338575,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2690,
           "gene": "CEACAM18",
           "score": -0.0762515,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9609,
           "gene": "MTERF4",
           "score": -0.1273965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18052,
           "gene": "ZNF451",
           "score": -0.06424,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7410,
           "gene": "IQCN",
           "score": 0.032715,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5231,
           "gene": "FAM98B",
           "score": 0.036453,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4498,
           "gene": "DYRK1A",
           "score": -0.53973,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9552,
           "gene": "MSANTD3-TMEFF1",
           "score": -0.062495,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8713,
           "gene": "LUZP1",
           "score": 0.165695,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5020,
           "gene": "EXTL2",
           "score": 0.1882635,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15061,
           "gene": "SPTB",
           "score": 0.1158745,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12057,
           "gene": "POT1",
           "score": 0.05799565,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8077,
           "gene": "KRTAP19-5",
           "score": -0.24164,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12578,
           "gene": "PTGFRN",
           "score": 0.02096,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4856,
           "gene": "EPM2A",
           "score": 0.21128,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 964,
           "gene": "ARHGEF38",
           "score": -0.1083765,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1186,
           "gene": "ATMIN",
           "score": 0.1215055,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2599,
           "gene": "CDH13",
           "score": -0.1230715,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13475,
           "gene": "RPS26",
           "score": -0.042948,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10046,
           "gene": "NEK11",
           "score": 0.104762,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2150,
           "gene": "CARD18",
           "score": 0.1253575,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12256,
           "gene": "PRDM10",
           "score": 0.054417,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5456,
           "gene": "FHIP2A",
           "score": -0.060856,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15121,
           "gene": "SRSF12",
           "score": 0.34673,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4422,
           "gene": "DSTN",
           "score": -0.121887,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15024,
           "gene": "SPON2",
           "score": -0.1191485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 865,
           "gene": "APOLD1",
           "score": 0.1369725,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10624,
           "gene": "OLFM3",
           "score": -0.001175,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8958,
           "gene": "MARF1",
           "score": -0.178513,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12899,
           "gene": "RASGRP4",
           "score": 0.01226,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4888,
           "gene": "ERCC4",
           "score": 0.1543335,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13825,
           "gene": "SDHC",
           "score": 0.5242,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10798,
           "gene": "OR2T4",
           "score": -0.1580005,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1271,
           "gene": "ATP8A1",
           "score": -0.244146,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14214,
           "gene": "SLAIN2",
           "score": 0.067428,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3319,
           "gene": "COL7A1",
           "score": -0.268605,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12406,
           "gene": "PRR27",
           "score": 0.210485,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4891,
           "gene": "ERCC6L",
           "score": 0.07,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3090,
           "gene": "CLEC14A",
           "score": -0.20048,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13530,
           "gene": "RSAD1",
           "score": 0.400445,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2357,
           "gene": "CCDC88A",
           "score": 0.162785,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8155,
           "gene": "LACTBL1",
           "score": 0.080435,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 1996,
+          "gene": "C9orf43",
+          "score": -0.121209,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5511,
+          "gene": "FLRT3",
+          "score": -0.342325,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8228,
+          "gene": "LCE5A",
+          "score": -0.106373,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12246,
+          "gene": "PRAMEF9",
+          "score": 0.22872,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11009,
+          "gene": "OR8I2",
+          "score": -0.0619,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3860,
+          "gene": "DAPP1",
+          "score": -0.153128,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11106,
+          "gene": "OXNAD1",
+          "score": 0.1366305,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10745,
+          "gene": "OR2A1",
+          "score": 0.0972775,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4001,
+          "gene": "DEAF1",
+          "score": 0.3774842,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16526,
+          "gene": "TRAPPC10",
+          "score": 0.13969,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11993,
+          "gene": "POLDIP2",
+          "score": 0.26151,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11916,
+          "gene": "PLXNB1",
+          "score": 0.0057805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10681,
+          "gene": "OR10J3",
+          "score": 0.21113,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6904,
+          "gene": "HOXD8",
+          "score": 0.173175,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10588,
+          "gene": "OCLM",
+          "score": -0.021735,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13477,
+          "gene": "RPS27A",
+          "score": 0.586065,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 17152,
+          "gene": "USP1",
+          "score": 0.23304,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3439,
+          "gene": "CPNE9",
+          "score": 0.03956,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5383,
+          "gene": "FDX1",
+          "score": -0.059622,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14104,
+          "gene": "SHANK2",
+          "score": 0.245764,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7626,
+          "gene": "KCNAB1",
+          "score": 0.0267669,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4833,
+          "gene": "EPC2",
+          "score": 0.255006,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3280,
+          "gene": "COL10A1",
+          "score": 0.09023,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14950,
+          "gene": "SPCS3",
+          "score": -0.73383,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 14709,
+          "gene": "SMPD2",
+          "score": -0.1506315,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16872,
+          "gene": "TUT1",
+          "score": 0.34309,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2804,
+          "gene": "CETN2",
+          "score": 0.017013,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13890,
+          "gene": "SEMA3B",
+          "score": 0.038255,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2402,
+          "gene": "CCM2L",
+          "score": -0.107333,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16256,
+          "gene": "TMEM63B",
+          "score": 0.022489,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 509,
+          "gene": "AKR1C1",
+          "score": 0.0594665,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9753,
+          "gene": "MYL12B",
+          "score": -0.01441,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3924,
+          "gene": "DCST2",
+          "score": -0.017094,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6185,
+          "gene": "GPALPP1",
+          "score": 0.248535,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6759,
+          "gene": "HIPK2",
+          "score": 0.0237305,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7108,
+          "gene": "IFITM2",
+          "score": 0.17169,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11562,
+          "gene": "PGBD1",
+          "score": 0.07664085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6960,
+          "gene": "HSD17B7",
+          "score": 0.0491875,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10689,
+          "gene": "OR10T2",
+          "score": -0.018596,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3005,
+          "gene": "CILP",
+          "score": -0.00866,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14731,
+          "gene": "SNAI3",
+          "score": 0.180015,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10837,
+          "gene": "OR4F4",
+          "score": -0.060785,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7998,
+          "gene": "KRT17",
+          "score": -0.101185,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10008,
+          "gene": "NDUFB7",
+          "score": -0.29093,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2183,
+          "gene": "CASQ2",
+          "score": 0.06984,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8659,
+          "gene": "LRRN4",
+          "score": -0.5025,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 5179,
+          "gene": "FAM229B",
+          "score": 0.0503065,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18193,
+          "gene": "ZNF652",
+          "score": 0.1074805,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5566,
+          "gene": "FOXB1",
+          "score": 0.033265,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7826,
+          "gene": "KIF2A",
+          "score": -0.097671,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6860,
+          "gene": "HOMER2",
+          "score": -0.05724825,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 431,
+          "gene": "AGPAT2",
+          "score": 0.220305,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7645,
+          "gene": "KCNG2",
+          "score": -0.059309,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16504,
+          "gene": "TRABD",
+          "score": -0.02693,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3543,
+          "gene": "CRYGB",
+          "score": -0.0725975,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5802,
+          "gene": "GALR2",
+          "score": -0.352975,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17443,
+          "gene": "WDR55",
+          "score": 0.0017455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7094,
+          "gene": "IFI27L2",
+          "score": -0.064292,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1614,
+          "gene": "BRIP1",
+          "score": 0.06074125,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13230,
+          "gene": "RLBP1",
+          "score": 0.1716665,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5071,
+          "gene": "FAIM2",
+          "score": -0.169465,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14535,
+          "gene": "SLC5A3",
+          "score": 0.0183725,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10241,
+          "gene": "NMNAT3",
+          "score": -0.18652,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3563,
+          "gene": "CSF2RB",
+          "score": 0.1318105,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12560,
+          "gene": "PTCRA",
+          "score": -0.188151,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13031,
+          "gene": "RECQL5",
+          "score": -0.05877,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15301,
+          "gene": "STUB1",
+          "score": 0.071698,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17802,
+          "gene": "ZFY",
+          "score": -0.1789355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4699,
+          "gene": "ELAPOR1",
+          "score": 0.0777455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2294,
+          "gene": "CCDC177",
+          "score": 0.231777,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9725,
+          "gene": "MYCBPAP",
+          "score": 0.380385,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16784,
+          "gene": "TTC19",
+          "score": 0.0648395,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6772,
+          "gene": "HLA-C",
+          "score": -0.159725,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6939,
+          "gene": "HS3ST4",
+          "score": 0.10231,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17799,
+          "gene": "ZFTA",
+          "score": 0.295155,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5089,
+          "gene": "FAM120AOS",
+          "score": -0.008135,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6910,
+          "gene": "HPDL",
+          "score": 0.16511,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4552,
+          "gene": "EDARADD",
+          "score": -0.189085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3649,
+          "gene": "CTNNA3",
+          "score": -0.1643525,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15558,
+          "gene": "TAS2R16",
+          "score": 0.16296,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16318,
+          "gene": "TMT1A",
+          "score": 0.16839,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10900,
+          "gene": "OR52N5",
+          "score": 0.1934785,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17420,
+          "gene": "WDR25",
+          "score": 0.2083875,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8147,
+          "gene": "L3MBTL1",
+          "score": -0.065173,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11208,
+          "gene": "PAPLN",
+          "score": 0.26057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12617,
+          "gene": "PTPN6",
+          "score": 0.247855,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15124,
+          "gene": "SRSF4",
+          "score": -0.121985,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7745,
+          "gene": "KDM4A",
+          "score": -0.0238664,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5380,
+          "gene": "FDCSP",
+          "score": 0.029475,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12171,
+          "gene": "PPP1R37",
+          "score": 0.009535,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6191,
+          "gene": "GPATCH2",
+          "score": 0.2751515,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15640,
+          "gene": "TBPL1",
+          "score": 0.1815968,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14423,
+          "gene": "SLC34A2",
+          "score": -0.232403,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5981,
+          "gene": "GIMAP8",
+          "score": -0.12592,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4024,
+          "gene": "DEFB115",
+          "score": -0.292765,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15250,
+          "gene": "STK19",
+          "score": -0.223335,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3048,
+          "gene": "CLCA4",
+          "score": -0.132371,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15917,
+          "gene": "TIAM1",
+          "score": 0.16909,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4068,
+          "gene": "DEPDC1B",
+          "score": 0.04660265,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5512,
+          "gene": "FLT1",
+          "score": -0.187085,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13504,
+          "gene": "RPUSD1",
+          "score": 0.1830785,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12074,
+          "gene": "POU2F3",
+          "score": 0.0138355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17528,
+          "gene": "WSCD2",
+          "score": -0.028234,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11013,
+          "gene": "OR8K3",
+          "score": -0.128625,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4078,
+          "gene": "DES",
+          "score": -0.49181,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 4523,
+          "gene": "EBF2",
+          "score": -0.106032,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18400,
+          "gene": "ZSWIM4",
+          "score": -0.2097455,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3376,
+          "gene": "CORO1B",
+          "score": -0.28897,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12258,
+          "gene": "PRDM12",
+          "score": -0.007624,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10640,
+          "gene": "OOEP",
+          "score": 0.28676,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16175,
+          "gene": "TMEM219",
+          "score": 0.17395675,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14337,
+          "gene": "SLC25A24",
+          "score": 0.421035,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 14583,
+          "gene": "SLC9A3",
+          "score": -0.15355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16941,
+          "gene": "UBASH3A",
+          "score": 0.347969,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13005,
+          "gene": "RCL1",
+          "score": 0.887835,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 6589,
+          "gene": "HADHA",
+          "score": -0.1265685,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17500,
+          "gene": "WNK3",
+          "score": -0.134325,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6454,
+          "gene": "GTPBP2",
+          "score": -0.17266345,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3622,
+          "gene": "CT83",
+          "score": -0.0519932,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2396,
+          "gene": "CCL3L3",
+          "score": 0.29666,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10498,
+          "gene": "NUDT19",
+          "score": -0.15354745,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8487,
+          "gene": "LOC339862",
+          "score": 0.072995,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17069,
+          "gene": "UHMK1",
+          "score": 0.0180035,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 692,
+          "gene": "ANKRD24",
+          "score": -0.05942,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13586,
+          "gene": "RTRAF",
+          "score": -0.1060871,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1663,
+          "gene": "BTN3A2",
+          "score": 0.1734735,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4899,
+          "gene": "ERGIC2",
+          "score": -0.01648,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7879,
+          "gene": "KLF7",
+          "score": -0.0773255,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
