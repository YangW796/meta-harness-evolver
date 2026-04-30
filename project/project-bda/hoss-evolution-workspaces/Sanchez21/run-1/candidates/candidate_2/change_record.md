# Change Record — candidate_2

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21/run-1/best/current/harness
Generated at: 2026-04-30T06:54:06.152527

## Files Changed

- model.py: modified (added=3, deleted=3, delta=0)
- outputs/metrics.json: modified (added=2136, deleted=344, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -58,10 +58,10 @@
     
     # Exploitation: select based on historical scores
     if len(history) > 0 and num_exploit > 0:
-        # Sort history by score (descending)
-        sorted_history = sorted(history, key=lambda x: x['score'], reverse=True)
+        # Sort history by score (ascending) to prioritize lowest (most negative) scores
+        sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
         
-        # Get top performers (top 20% or at least 10)
+        # Get top performers (lowest 20% or at least 10)
         top_k = max(10, len(sorted_history) // 5)
         top_performers = [h['candidate_index'] for h in sorted_history[:top_k]]
         

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18469,
-      "rounds": 1,
+      "rounds": 2,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 0,
-      "baseline_total_hits": 0,
+      "baseline_total_queries": 128,
+      "baseline_total_hits": 8,
       "delta_queries": 128,
-      "delta_hits": 8,
-      "total_queries": 128,
-      "total_hits": 8,
+      "delta_hits": 7,
+      "total_queries": 256,
+      "total_hits": 15,
       "top_k": 924,
       "hit_curve": {
         "queries": [
-          0,
-          128
+          128,
+          256
         ],
         "hits": [
-          0,
-          8
+          8,
+          15
         ]
       },
-      "auc": 512.0,
-      "auc_normalized": 0.004329004329004329,
-      "ncg": 0.20608211756124528,
+      "auc": 1472.0,
+      "auc_normalized": 0.006222943722943723,
+      "ncg": 0.23146633240778638,
       "round_details": [
         {
-          "round": 0,
+          "round": 1,
           "selected_count": 128,
-          "hits": 8,
-          "cumulative_hits": 8,
-          "precision_at_batch": 0.0625,
+          "hits": 7,
+          "cumulative_hits": 15,
+          "precision_at_batch": 0.0546875,
           "selected": [
-            "CUL1",
-            "APBB1IP",
-            "MAP2K5",
-            "KLF6",
-            "IKBKG",
-            "EFNA1",
-            "COX7A1",
-            "ZHX2",
-            "CHADL",
-            "SDAD1",
-            "ARMCX3",
-            "ARHGEF35",
-            "CLEC5A",
-            "IBSP",
-            "ITPR1",
-            "TRAM2",
-            "APOL3",
-            "ZNF85",
-            "GTF2E2",
-            "ZFYVE16",
-            "SCAND1",
-            "IFITM5",
-            "SMIM4",
-            "MAVS",
-            "ACTN4",
-            "FAM45A",
-            "SDPR",
-            "PALLD",
-            "MAT1A",
-            "FAM150A",
-            "HSBP1",
-            "OTOA",
-            "COX4I1",
-            "CLDN7",
-            "PRTN3",
-            "CNKSR1",
-            "PLA2G4C",
-            "PCDHA10",
-            "LPPR5",
-            "BBS2",
-            "SPRED3",
-            "WRN",
-            "DHRS3",
-            "PRR5L",
-            "CDCA8",
-            "ZNF426",
-            "MRPL13",
-            "PLIN2",
-            "GPR107",
-            "CCDC178",
-            "BFAR",
-            "INSL6",
-            "MMP3",
-            "CDIPT",
-            "ITPRIPL2",
-            "COPRS",
-            "PSAP",
-            "MATK",
-            "SON",
-            "POLA2",
-            "FASLG",
-            "PPP1R12B",
-            "PIGA",
-            "HK1",
-            "LRRC47",
-            "CCDC84",
-            "FN1",
-            "WDR87",
-            "KLF3",
-            "FBP1",
-            "SRSF6",
-            "PRSS41",
-            "LVRN",
-            "ZNF646",
-            "IDUA",
-            "NUDT12",
-            "C2CD2L",
-            "IQCF2",
-            "ARPC1A",
-            "NLGN2",
-            "RGS20",
-            "LRRC8B",
-            "CATSPERB",
-            "HMGN2",
-            "NKAP",
-            "HORMAD2",
-            "TMX1",
-            "RBM39",
-            "SPNS3",
-            "ELK1",
-            "LRFN4",
-            "EFNA4",
-            "KLK15",
-            "ZNF862",
-            "YKT6",
-            "LOC101060179",
-            "SFN",
-            "RFC3",
-            "PLOD1",
-            "IDH2",
-            "EDIL3",
-            "TRNP1",
-            "TMEM189",
-            "CISD1",
-            "BLVRA",
-            "CTCFL",
-            "F8A2",
-            "FAM49B",
-            "SDCCAG8",
-            "CAMSAP3",
-            "PTPN6",
-            "PSMD1",
-            "STX3",
-            "VN1R1",
-            "KRTAP2-4",
-            "ZNF626",
-            "ADRA2C",
-            "CYP4X1",
-            "ZBTB10",
-            "LSM12",
-            "PATE3",
-            "CXCL5",
-            "MS4A13",
-            "SLC24A5",
-            "FAM24B",
-            "SPATA5",
-            "ABRA",
-            "LRMP"
+            "ATP6V1B1",
+            "MLNR",
+            "ENHO",
+            "STIM1",
+            "PRADC1",
+            "CNNM4",
+            "SPATA31A6",
+            "TOB1",
+            "AMPD3",
+            "UAP1L1",
+            "SLC16A10",
+            "PRKAR2B",
+            "ZNF341",
+            "SLC22A31",
+            "RC3H1",
+            "GABPB2",
+            "C7orf57",
+            "CSNK2A3",
+            "DHX58",
+            "PRRC2A",
+            "FAM122B",
+            "CNGA1",
+            "FAM98C",
+            "TUSC3",
+            "TNFAIP3",
+            "DNAJC25",
+            "RAB5A",
+            "TRPT1",
+            "MAN1A1",
+            "GFM1",
+            "PRSS56",
+            "CAPN12",
+            "BRD9",
+            "CACNB2",
+            "GMNC",
+            "CACNG5",
+            "FEV",
+            "MTMR14",
+            "MARS",
+            "CD99L2",
+            "USP45",
+            "CPQ",
+            "CACNA2D1",
+            "CLPP",
+            "SRC",
+            "OR5A1",
+            "OR51B6",
+            "WDR12",
+            "SLC37A4",
+            "FGF7",
+            "DLX3",
+            "CDKL2",
+            "NRN1L",
+            "BTBD16",
+            "LY6K",
+            "PPP1R27",
+            "GLTSCR1L",
+            "CCDC66",
+            "ZNF587",
+            "CYP26A1",
+            "MTUS1",
+            "TMPO",
+            "PNPO",
+            "SLC22A25",
+            "B4GALNT1",
+            "TBC1D10B",
+            "SAP130",
+            "CEP295NL",
+            "PLEKHB1",
+            "DNA2",
+            "CGRRF1",
+            "FAM134C",
+            "NDUFB8",
+            "CTDSP2",
+            "YIPF4",
+            "SETX",
+            "SLCO4C1",
+            "ATP5J2-PTCD1",
+            "EPT1",
+            "ABHD14B",
+            "CRYBA1",
+            "DHX33",
+            "DLGAP4",
+            "ALG14",
+            "PAK4",
+            "DDC",
+            "WNT6",
+            "TNS1",
+            "LMAN2L",
+            "SPRR2B",
+            "PATZ1",
+            "RAB22A",
+            "CHERP",
+            "ASB16",
+            "CLEC4E",
+            "HIST1H2AB",
+            "ZBTB45",
+            "EFCAB11",
+            "KLHL9",
+            "IFI44L",
+            "ATP2A2",
+            "PLCXD3",
+            "NCAPG",
+            "RECQL4",
+            "CLEC4D",
+            "SSH1",
+            "GATM",
+            "GORASP1",
+            "C10orf105",
+            "KCNJ1",
+            "N4BP2",
+            "IL2RA",
+            "PEF1",
+            "GORASP2",
+            "IER3",
+            "RAB34",
+            "RBAK",
+            "INTS2",
+            "CACNA1S",
+            "ST8SIA4",
+            "TRIM52",
+            "CADM1",
+            "CNPY4",
+            "ARAP1",
+            "AOX1",
+            "ZNF462",
+            "TYW3",
+            "TRPM7"
           ],
           "selected_scores": [
-            -0.7084805590000001,
-            -0.847566367,
-            -0.646392168,
-            -1.286605531,
-            -1.011233856,
-            -0.605851751,
-            -3.0936171619999997,
-            -0.6378804539999999,
-            -1.45418052,
-            -0.463321217,
-            -1.390124729,
-            -0.5351421789999999,
-            -0.526246283,
-            -0.41687788600000003,
-            -0.8075541079999999,
-            -0.207407924,
-            -1.178192222,
-            -0.667703014,
-            -1.161694307,
-            -0.151761909,
-            -0.0308524,
-            -1.034508226,
-            -0.8907777590000001,
-            -0.296087312,
-            -2.1890067109999998,
-            -2.316107883,
-            -0.22494741199999999,
-            -0.25187241,
-            -0.58303235,
-            -1.1998195740000002,
-            -0.680339995,
-            -0.083778762,
-            -0.7748776279999999,
-            -3.4000132339999998,
-            -0.389149951,
-            -0.486427984,
-            -0.5954982870000001,
-            -0.76248473,
-            -2.680333955,
-            -0.44684414,
-            -0.957138816,
-            -1.762816357,
-            -0.343573709,
-            -0.536061023,
-            -1.925039131,
-            -0.755163757,
-            -0.10235072699999999,
-            -0.44822563,
-            -0.177922565,
-            -1.165824661,
-            -0.17457183699999998,
-            -1.491389192,
-            -0.333031154,
-            -1.312742639,
-            -1.127677133,
-            -0.156469786,
-            -3.122229945,
-            -1.420538244,
-            -0.426324209,
-            -0.991251599,
-            -0.38996551,
-            -0.641169591,
-            -0.489342847,
-            -0.194383213,
-            -0.46040265,
-            -4.211130287,
-            -0.133489856,
-            -0.7718566029999999,
-            -0.38812869200000005,
-            -0.283086165,
-            -0.733157018,
-            -1.908639,
-            -1.646824745,
-            -0.6040569410000001,
-            -1.37219963,
-            -0.798608137,
-            -0.7842747290000001,
-            -0.5480988139999999,
-            -0.7191423090000001,
-            -2.298319116,
-            -1.9909401919999998,
-            -0.7791987109999999,
-            -0.30452932899999996,
-            -1.537334942,
-            -0.26130868100000004,
-            -0.217601022,
-            -0.23205319,
-            -0.382187661,
-            -1.310862131,
-            -0.780715103,
-            -0.57855135,
-            -0.41219300799999997,
-            -0.662382259,
-            -0.739281469,
-            -1.4617258359999998,
-            -0.481618604,
-            -0.62648364,
-            -0.339161064,
-            -0.725619907,
-            -1.4750069540000001,
-            -0.43605276600000004,
-            -0.44800802,
-            -1.379951568,
-            -0.697778867,
-            -1.0208300670000001,
-            -0.615594321,
-            -0.757835777,
-            -2.014598466,
-            -0.7172328170000001,
-            -0.503657337,
-            -0.742329297,
-            -0.443164457,
-            -0.369267661,
-            -0.485805724,
-            -1.1155609,
-            -0.48027414700000004,
-            -0.514642412,
-            -0.55176932,
-            -1.454030435,
-            -2.058202489,
-            -1.255088674,
-            -0.57877837,
-            -0.6619021660000001,
-            -1.198486086,
-            -1.130251816,
-            -0.547784346,
-            -0.213723146,
-            -1.582579036
+            -0.201361404,
+            -0.747039243,
+            -1.741433183,
+            -0.872834543,
+            -0.400385782,
+            -1.958794925,
+            -1.8808401869999998,
+            -0.04263311400000001,
+            -1.560177346,
+            -1.242589671,
+            -0.299769754,
+            -2.180935028,
+            -0.747779243,
+            -3.097231897,
+            -0.284626373,
+            -0.753812977,
+            -2.4030170280000003,
+            -0.424770145,
+            -0.41948254799999996,
+            -1.7020696880000001,
+            -0.624585328,
+            -0.955465346,
+            -0.007484081,
+            -1.477456704,
+            -0.24478269600000002,
+            -0.144876628,
+            -0.816099185,
+            -1.36667693,
+            -0.538292791,
+            -0.751344198,
+            -0.32846977899999996,
+            -1.342826074,
+            -0.48776693600000004,
+            -0.929824685,
+            -0.657510787,
+            -0.554727847,
+            -0.5020772410000001,
+            -0.676362227,
+            -1.7221653730000002,
+            -0.8015028940000001,
+            -0.744610965,
+            -0.21542853399999998,
+            -0.841312252,
+            -0.754310446,
+            -0.18767251100000001,
+            -1.315155034,
+            -0.573881217,
+            -0.489996344,
+            -0.488998694,
+            -0.634709573,
+            -0.5142020860000001,
+            -0.798956039,
+            -0.603685331,
+            -0.46107903899999997,
+            -1.133163553,
+            -0.7634699640000001,
+            -0.532196444,
+            -1.953629576,
+            -0.668699053,
+            -1.181122722,
+            -2.095547005,
+            -0.380735899,
+            -0.625406357,
+            -0.594484782,
+            -0.646906026,
+            -1.332644192,
+            -1.7633453890000002,
+            -0.48691684399999996,
+            -0.42420400700000005,
+            -0.939162108,
+            -0.522701819,
+            -2.578453197,
+            -0.38708333899999997,
+            -0.972576826,
+            -0.82666332,
+            -0.532716148,
+            -0.516317234,
+            -0.037490411,
+            -0.6679974129999999,
+            -0.6283653889999999,
+            -0.268420642,
+            -0.541433907,
+            -1.46070239,
+            -2.68875708,
+            -1.8027060209999999,
+            -0.929506473,
+            -1.671571265,
+            -0.330736545,
+            -0.289915381,
+            -2.2582741669999997,
+            -0.340146965,
+            -0.39571887299999997,
+            -0.40377916399999997,
+            -0.86033773,
+            -0.7449079909999999,
+            -0.8507868270000001,
+            -1.194509909,
+            -0.620572869,
+            -0.6539120939999999,
+            -0.516216255,
+            -1.462034819,
+            -2.179757934,
+            -1.06309241,
+            -0.37270078,
+            -0.983796462,
+            -0.085117982,
+            -0.666915241,
+            -0.547693926,
+            -0.6930261940000001,
+            -0.92222815,
+            -0.5965225670000001,
+            -0.282283954,
+            -0.46186604200000003,
+            -0.608994797,
+            -0.383512454,
+            -0.5423345470000001,
+            -0.627505291,
+            -0.026746527000000003,
+            -0.258920282,
+            -0.514679575,
+            -1.223795966,
+            -0.447477214,
+            -2.1437942580000002,
+            -0.7953905440000001,
+            -0.330226245,
+            -0.126055812,
+            -1.423577743,
+            -1.254003543
           ],
           "selected_hits": [
             0,
@@ -307,20 +307,13 @@
             0,
             0,
             0,
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
             1,
             0,
             0,
@@ -330,15 +323,67 @@
             0,
             0,
             0,
-            0,
-            0,
             1,
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
+            0,
+            0,
+            0,
+            0,
             1,
             0,
             0,
             0,
             0,
+            0,
             1,
             0,
             0,
@@ -347,6 +392,20 @@
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
             1,
             0,
             0,
@@ -357,68 +416,9 @@
             0,
             0,
             0,
+            0,
+            0,
             1,
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
             0,
             0,
             0,
@@ -1328,6 +1328,902 @@
           "score": -1.582579036,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 1271,
+          "gene": "ATP6V1B1",
+          "score": -0.201361404,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9448,
+          "gene": "MLNR",
+          "score": -0.747039243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4751,
+          "gene": "ENHO",
+          "score": -1.741433183,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15267,
+          "gene": "STIM1",
+          "score": -0.872834543,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12210,
+          "gene": "PRADC1",
+          "score": -0.400385782,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3178,
+          "gene": "CNNM4",
+          "score": -1.958794925,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14957,
+          "gene": "SPATA31A6",
+          "score": -1.8808401869999998,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16441,
+          "gene": "TOB1",
+          "score": -0.04263311400000001,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 630,
+          "gene": "AMPD3",
+          "score": -1.560177346,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16961,
+          "gene": "UAP1L1",
+          "score": -1.242589671,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14272,
+          "gene": "SLC16A10",
+          "score": -0.299769754,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12291,
+          "gene": "PRKAR2B",
+          "score": -2.180935028,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18046,
+          "gene": "ZNF341",
+          "score": -0.747779243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14327,
+          "gene": "SLC22A31",
+          "score": -3.097231897,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 13005,
+          "gene": "RC3H1",
+          "score": -0.284626373,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5816,
+          "gene": "GABPB2",
+          "score": -0.753812977,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1903,
+          "gene": "C7orf57",
+          "score": -2.4030170280000003,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3542,
+          "gene": "CSNK2A3",
+          "score": -0.424770145,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4112,
+          "gene": "DHX58",
+          "score": -0.41948254799999996,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12407,
+          "gene": "PRRC2A",
+          "score": -1.7020696880000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5064,
+          "gene": "FAM122B",
+          "score": -0.624585328,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3159,
+          "gene": "CNGA1",
+          "score": -0.955465346,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5303,
+          "gene": "FAM98C",
+          "score": -0.007484081,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 16907,
+          "gene": "TUSC3",
+          "score": -1.477456704,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16366,
+          "gene": "TNFAIP3",
+          "score": -0.24478269600000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4248,
+          "gene": "DNAJC25",
+          "score": -0.144876628,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12772,
+          "gene": "RAB5A",
+          "score": -0.816099185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16718,
+          "gene": "TRPT1",
+          "score": -1.36667693,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8980,
+          "gene": "MAN1A1",
+          "score": -0.538292791,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6001,
+          "gene": "GFM1",
+          "score": -0.751344198,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12443,
+          "gene": "PRSS56",
+          "score": -0.32846977899999996,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2094,
+          "gene": "CAPN12",
+          "score": -1.342826074,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1614,
+          "gene": "BRD9",
+          "score": -0.48776693600000004,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2017,
+          "gene": "CACNB2",
+          "score": -0.929824685,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6158,
+          "gene": "GMNC",
+          "score": -0.657510787,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2024,
+          "gene": "CACNG5",
+          "score": -0.554727847,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5472,
+          "gene": "FEV",
+          "score": -0.5020772410000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9781,
+          "gene": "MTMR14",
+          "score": -0.676362227,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9091,
+          "gene": "MARS",
+          "score": -1.7221653730000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2540,
+          "gene": "CD99L2",
+          "score": -0.8015028940000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17229,
+          "gene": "USP45",
+          "score": -0.744610965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3402,
+          "gene": "CPQ",
+          "score": -0.21542853399999998,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2012,
+          "gene": "CACNA2D1",
+          "score": -0.841312252,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3105,
+          "gene": "CLPP",
+          "score": -0.754310446,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15098,
+          "gene": "SRC",
+          "score": -0.18767251100000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10935,
+          "gene": "OR5A1",
+          "score": -1.315155034,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10899,
+          "gene": "OR51B6",
+          "score": -0.573881217,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17447,
+          "gene": "WDR12",
+          "score": -0.489996344,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14483,
+          "gene": "SLC37A4",
+          "score": -0.488998694,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5508,
+          "gene": "FGF7",
+          "score": -0.634709573,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4170,
+          "gene": "DLX3",
+          "score": -0.5142020860000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2644,
+          "gene": "CDKL2",
+          "score": -0.798956039,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10549,
+          "gene": "NRN1L",
+          "score": -0.603685331,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1652,
+          "gene": "BTBD16",
+          "score": -0.46107903899999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8855,
+          "gene": "LY6K",
+          "score": -1.133163553,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12150,
+          "gene": "PPP1R27",
+          "score": -0.7634699640000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6138,
+          "gene": "GLTSCR1L",
+          "score": -0.532196444,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2320,
+          "gene": "CCDC66",
+          "score": -1.953629576,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18210,
+          "gene": "ZNF587",
+          "score": -0.668699053,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3741,
+          "gene": "CYP26A1",
+          "score": -1.181122722,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9809,
+          "gene": "MTUS1",
+          "score": -2.095547005,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16330,
+          "gene": "TMPO",
+          "score": -0.380735899,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11935,
+          "gene": "PNPO",
+          "score": -0.625406357,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14325,
+          "gene": "SLC22A25",
+          "score": -0.594484782,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1362,
+          "gene": "B4GALNT1",
+          "score": -0.646906026,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15613,
+          "gene": "TBC1D10B",
+          "score": -1.332644192,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13695,
+          "gene": "SAP130",
+          "score": -1.7633453890000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2758,
+          "gene": "CEP295NL",
+          "score": -0.48691684399999996,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11820,
+          "gene": "PLEKHB1",
+          "score": -0.42420400700000005,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4197,
+          "gene": "DNA2",
+          "score": -0.939162108,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2843,
+          "gene": "CGRRF1",
+          "score": -0.522701819,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5085,
+          "gene": "FAM134C",
+          "score": -2.578453197,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10153,
+          "gene": "NDUFB8",
+          "score": -0.38708333899999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3596,
+          "gene": "CTDSP2",
+          "score": -0.972576826,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17656,
+          "gene": "YIPF4",
+          "score": -0.82666332,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14021,
+          "gene": "SETX",
+          "score": -0.532716148,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14623,
+          "gene": "SLCO4C1",
+          "score": -0.516317234,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1252,
+          "gene": "ATP5J2-PTCD1",
+          "score": -0.037490411,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 4837,
+          "gene": "EPT1",
+          "score": -0.6679974129999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 82,
+          "gene": "ABHD14B",
+          "score": -0.6283653889999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3491,
+          "gene": "CRYBA1",
+          "score": -0.268420642,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4104,
+          "gene": "DHX33",
+          "score": -0.541433907,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4160,
+          "gene": "DLGAP4",
+          "score": -1.46070239,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 561,
+          "gene": "ALG14",
+          "score": -2.68875708,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 11144,
+          "gene": "PAK4",
+          "score": -1.8027060209999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3914,
+          "gene": "DDC",
+          "score": -0.929506473,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17561,
+          "gene": "WNT6",
+          "score": -1.671571265,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16436,
+          "gene": "TNS1",
+          "score": -0.330736545,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8548,
+          "gene": "LMAN2L",
+          "score": -0.289915381,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15059,
+          "gene": "SPRR2B",
+          "score": -2.2582741669999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11224,
+          "gene": "PATZ1",
+          "score": -0.340146965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12731,
+          "gene": "RAB22A",
+          "score": -0.39571887299999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2874,
+          "gene": "CHERP",
+          "score": -0.40377916399999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1102,
+          "gene": "ASB16",
+          "score": -0.86033773,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3066,
+          "gene": "CLEC4E",
+          "score": -0.7449079909999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6798,
+          "gene": "HIST1H2AB",
+          "score": -0.8507868270000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17731,
+          "gene": "ZBTB45",
+          "score": -1.194509909,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4553,
+          "gene": "EFCAB11",
+          "score": -0.620572869,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8074,
+          "gene": "KLHL9",
+          "score": -0.6539120939999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7211,
+          "gene": "IFI44L",
+          "score": -0.516216255,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1229,
+          "gene": "ATP2A2",
+          "score": -1.462034819,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11801,
+          "gene": "PLCXD3",
+          "score": -2.179757934,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10066,
+          "gene": "NCAPG",
+          "score": -1.06309241,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13042,
+          "gene": "RECQL4",
+          "score": -0.37270078,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3065,
+          "gene": "CLEC4D",
+          "score": -0.983796462,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15164,
+          "gene": "SSH1",
+          "score": -0.085117982,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 5917,
+          "gene": "GATM",
+          "score": -0.666915241,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6245,
+          "gene": "GORASP1",
+          "score": -0.547693926,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1695,
+          "gene": "C10orf105",
+          "score": -0.6930261940000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7758,
+          "gene": "KCNJ1",
+          "score": -0.92222815,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9964,
+          "gene": "N4BP2",
+          "score": -0.5965225670000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7378,
+          "gene": "IL2RA",
+          "score": -0.282283954,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11469,
+          "gene": "PEF1",
+          "score": -0.46186604200000003,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6246,
+          "gene": "GORASP2",
+          "score": -0.608994797,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7198,
+          "gene": "IER3",
+          "score": -0.383512454,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12747,
+          "gene": "RAB34",
+          "score": -0.5423345470000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12924,
+          "gene": "RBAK",
+          "score": -0.627505291,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7475,
+          "gene": "INTS2",
+          "score": -0.026746527000000003,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2011,
+          "gene": "CACNA1S",
+          "score": -0.258920282,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15219,
+          "gene": "ST8SIA4",
+          "score": -0.514679575,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16641,
+          "gene": "TRIM52",
+          "score": -1.223795966,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2032,
+          "gene": "CADM1",
+          "score": -0.447477214,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3194,
+          "gene": "CNPY4",
+          "score": -2.1437942580000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 899,
+          "gene": "ARAP1",
+          "score": -0.7953905440000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 784,
+          "gene": "AOX1",
+          "score": -0.330226245,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18114,
+          "gene": "ZNF462",
+          "score": -0.126055812,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16953,
+          "gene": "TYW3",
+          "score": -1.423577743,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16715,
+          "gene": "TRPM7",
+          "score": -1.254003543,
+          "hit": 0,
+          "round": 1
         }
       ],
       "queried_history": [
@@ -2226,6 +3122,902 @@
           "score": -1.582579036,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 1271,
+          "gene": "ATP6V1B1",
+          "score": -0.201361404,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9448,
+          "gene": "MLNR",
+          "score": -0.747039243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4751,
+          "gene": "ENHO",
+          "score": -1.741433183,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15267,
+          "gene": "STIM1",
+          "score": -0.872834543,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12210,
+          "gene": "PRADC1",
+          "score": -0.400385782,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3178,
+          "gene": "CNNM4",
+          "score": -1.958794925,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14957,
+          "gene": "SPATA31A6",
+          "score": -1.8808401869999998,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16441,
+          "gene": "TOB1",
+          "score": -0.04263311400000001,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 630,
+          "gene": "AMPD3",
+          "score": -1.560177346,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16961,
+          "gene": "UAP1L1",
+          "score": -1.242589671,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14272,
+          "gene": "SLC16A10",
+          "score": -0.299769754,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12291,
+          "gene": "PRKAR2B",
+          "score": -2.180935028,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18046,
+          "gene": "ZNF341",
+          "score": -0.747779243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14327,
+          "gene": "SLC22A31",
+          "score": -3.097231897,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 13005,
+          "gene": "RC3H1",
+          "score": -0.284626373,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5816,
+          "gene": "GABPB2",
+          "score": -0.753812977,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1903,
+          "gene": "C7orf57",
+          "score": -2.4030170280000003,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3542,
+          "gene": "CSNK2A3",
+          "score": -0.424770145,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4112,
+          "gene": "DHX58",
+          "score": -0.41948254799999996,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12407,
+          "gene": "PRRC2A",
+          "score": -1.7020696880000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5064,
+          "gene": "FAM122B",
+          "score": -0.624585328,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3159,
+          "gene": "CNGA1",
+          "score": -0.955465346,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5303,
+          "gene": "FAM98C",
+          "score": -0.007484081,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 16907,
+          "gene": "TUSC3",
+          "score": -1.477456704,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16366,
+          "gene": "TNFAIP3",
+          "score": -0.24478269600000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4248,
+          "gene": "DNAJC25",
+          "score": -0.144876628,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12772,
+          "gene": "RAB5A",
+          "score": -0.816099185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16718,
+          "gene": "TRPT1",
+          "score": -1.36667693,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8980,
+          "gene": "MAN1A1",
+          "score": -0.538292791,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6001,
+          "gene": "GFM1",
+          "score": -0.751344198,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12443,
+          "gene": "PRSS56",
+          "score": -0.32846977899999996,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2094,
+          "gene": "CAPN12",
+          "score": -1.342826074,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1614,
+          "gene": "BRD9",
+          "score": -0.48776693600000004,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2017,
+          "gene": "CACNB2",
+          "score": -0.929824685,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6158,
+          "gene": "GMNC",
+          "score": -0.657510787,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2024,
+          "gene": "CACNG5",
+          "score": -0.554727847,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5472,
+          "gene": "FEV",
+          "score": -0.5020772410000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9781,
+          "gene": "MTMR14",
+          "score": -0.676362227,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9091,
+          "gene": "MARS",
+          "score": -1.7221653730000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2540,
+          "gene": "CD99L2",
+          "score": -0.8015028940000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17229,
+          "gene": "USP45",
+          "score": -0.744610965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3402,
+          "gene": "CPQ",
+          "score": -0.21542853399999998,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2012,
+          "gene": "CACNA2D1",
+          "score": -0.841312252,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3105,
+          "gene": "CLPP",
+          "score": -0.754310446,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15098,
+          "gene": "SRC",
+          "score": -0.18767251100000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10935,
+          "gene": "OR5A1",
+          "score": -1.315155034,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10899,
+          "gene": "OR51B6",
+          "score": -0.573881217,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17447,
+          "gene": "WDR12",
+          "score": -0.489996344,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14483,
+          "gene": "SLC37A4",
+          "score": -0.488998694,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5508,
+          "gene": "FGF7",
+          "score": -0.634709573,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4170,
+          "gene": "DLX3",
+          "score": -0.5142020860000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2644,
+          "gene": "CDKL2",
+          "score": -0.798956039,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10549,
+          "gene": "NRN1L",
+          "score": -0.603685331,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1652,
+          "gene": "BTBD16",
+          "score": -0.46107903899999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8855,
+          "gene": "LY6K",
+          "score": -1.133163553,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12150,
+          "gene": "PPP1R27",
+          "score": -0.7634699640000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6138,
+          "gene": "GLTSCR1L",
+          "score": -0.532196444,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2320,
+          "gene": "CCDC66",
+          "score": -1.953629576,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18210,
+          "gene": "ZNF587",
+          "score": -0.668699053,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3741,
+          "gene": "CYP26A1",
+          "score": -1.181122722,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9809,
+          "gene": "MTUS1",
+          "score": -2.095547005,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16330,
+          "gene": "TMPO",
+          "score": -0.380735899,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11935,
+          "gene": "PNPO",
+          "score": -0.625406357,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14325,
+          "gene": "SLC22A25",
+          "score": -0.594484782,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1362,
+          "gene": "B4GALNT1",
+          "score": -0.646906026,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15613,
+          "gene": "TBC1D10B",
+          "score": -1.332644192,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13695,
+          "gene": "SAP130",
+          "score": -1.7633453890000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2758,
+          "gene": "CEP295NL",
+          "score": -0.48691684399999996,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11820,
+          "gene": "PLEKHB1",
+          "score": -0.42420400700000005,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4197,
+          "gene": "DNA2",
+          "score": -0.939162108,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2843,
+          "gene": "CGRRF1",
+          "score": -0.522701819,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5085,
+          "gene": "FAM134C",
+          "score": -2.578453197,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10153,
+          "gene": "NDUFB8",
+          "score": -0.38708333899999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3596,
+          "gene": "CTDSP2",
+          "score": -0.972576826,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17656,
+          "gene": "YIPF4",
+          "score": -0.82666332,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14021,
+          "gene": "SETX",
+          "score": -0.532716148,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14623,
+          "gene": "SLCO4C1",
+          "score": -0.516317234,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1252,
+          "gene": "ATP5J2-PTCD1",
+          "score": -0.037490411,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 4837,
+          "gene": "EPT1",
+          "score": -0.6679974129999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 82,
+          "gene": "ABHD14B",
+          "score": -0.6283653889999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3491,
+          "gene": "CRYBA1",
+          "score": -0.268420642,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4104,
+          "gene": "DHX33",
+          "score": -0.541433907,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4160,
+          "gene": "DLGAP4",
+          "score": -1.46070239,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 561,
+          "gene": "ALG14",
+          "score": -2.68875708,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 11144,
+          "gene": "PAK4",
+          "score": -1.8027060209999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3914,
+          "gene": "DDC",
+          "score": -0.929506473,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17561,
+          "gene": "WNT6",
+          "score": -1.671571265,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16436,
+          "gene": "TNS1",
+          "score": -0.330736545,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8548,
+          "gene": "LMAN2L",
+          "score": -0.289915381,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15059,
+          "gene": "SPRR2B",
+          "score": -2.2582741669999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11224,
+          "gene": "PATZ1",
+          "score": -0.340146965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12731,
+          "gene": "RAB22A",
+          "score": -0.39571887299999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2874,
+          "gene": "CHERP",
+          "score": -0.40377916399999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1102,
+          "gene": "ASB16",
+          "score": -0.86033773,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3066,
+          "gene": "CLEC4E",
+          "score": -0.7449079909999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6798,
+          "gene": "HIST1H2AB",
+          "score": -0.8507868270000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17731,
+          "gene": "ZBTB45",
+          "score": -1.194509909,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4553,
+          "gene": "EFCAB11",
+          "score": -0.620572869,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8074,
+          "gene": "KLHL9",
+          "score": -0.6539120939999999,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7211,
+          "gene": "IFI44L",
+          "score": -0.516216255,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1229,
+          "gene": "ATP2A2",
+          "score": -1.462034819,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11801,
+          "gene": "PLCXD3",
+          "score": -2.179757934,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10066,
+          "gene": "NCAPG",
+          "score": -1.06309241,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13042,
+          "gene": "RECQL4",
+          "score": -0.37270078,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3065,
+          "gene": "CLEC4D",
+          "score": -0.983796462,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15164,
+          "gene": "SSH1",
+          "score": -0.085117982,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 5917,
+          "gene": "GATM",
+          "score": -0.666915241,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6245,
+          "gene": "GORASP1",
+          "score": -0.547693926,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1695,
+          "gene": "C10orf105",
+          "score": -0.6930261940000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7758,
+          "gene": "KCNJ1",
+          "score": -0.92222815,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9964,
+          "gene": "N4BP2",
+          "score": -0.5965225670000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7378,
+          "gene": "IL2RA",
+          "score": -0.282283954,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11469,
+          "gene": "PEF1",
+          "score": -0.46186604200000003,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6246,
+          "gene": "GORASP2",
+          "score": -0.608994797,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7198,
+          "gene": "IER3",
+          "score": -0.383512454,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12747,
+          "gene": "RAB34",
+          "score": -0.5423345470000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12924,
+          "gene": "RBAK",
+          "score": -0.627505291,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7475,
+          "gene": "INTS2",
+          "score": -0.026746527000000003,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2011,
+          "gene": "CACNA1S",
+          "score": -0.258920282,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15219,
+          "gene": "ST8SIA4",
+          "score": -0.514679575,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16641,
+          "gene": "TRIM52",
+          "score": -1.223795966,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2032,
+          "gene": "CADM1",
+          "score": -0.447477214,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3194,
+          "gene": "CNPY4",
+          "score": -2.1437942580000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 899,
+          "gene": "ARAP1",
+          "score": -0.7953905440000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 784,
+          "gene": "AOX1",
+          "score": -0.330226245,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18114,
+          "gene": "ZNF462",
+          "score": -0.126055812,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16953,
+          "gene": "TYW3",
+          "score": -1.423577743,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16715,
+          "gene": "TRPM7",
+          "score": -1.254003543,
+          "hit": 0,
+          "round": 1
         }
       ]
     }

```
