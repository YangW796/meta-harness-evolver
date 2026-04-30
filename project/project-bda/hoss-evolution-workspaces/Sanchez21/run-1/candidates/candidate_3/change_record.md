# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21/run-1/best/current/harness
Generated at: 2026-04-30T06:54:50.864301

## Files Changed

- model.py: modified (added=3, deleted=3, delta=0)
- outputs/metrics.json: modified (added=2374, deleted=582, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -58,10 +58,10 @@
     
     # Exploitation: select based on historical scores
     if len(history) > 0 and num_exploit > 0:
-        # Sort history by score (ascending) to prioritize lowest (most negative) scores
-        sorted_history = sorted(history, key=lambda x: x['score'], reverse=False)
+        # Sort by absolute score to prioritize both negative and positive extremes
+        sorted_history = sorted(history, key=lambda x: abs(x['score']), reverse=True)
         
-        # Get top performers (lowest 20% or at least 10)
+        # Get top performers (highest absolute scores, 20% or at least 10)
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
-      "rounds": 2,
+      "rounds": 3,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 128,
-      "baseline_total_hits": 8,
+      "baseline_total_queries": 256,
+      "baseline_total_hits": 15,
       "delta_queries": 128,
-      "delta_hits": 7,
-      "total_queries": 256,
-      "total_hits": 15,
+      "delta_hits": 3,
+      "total_queries": 384,
+      "total_hits": 18,
       "top_k": 924,
       "hit_curve": {
         "queries": [
-          128,
-          256
+          256,
+          384
         ],
         "hits": [
-          8,
-          15
+          15,
+          18
         ]
       },
-      "auc": 1472.0,
-      "auc_normalized": 0.006222943722943723,
-      "ncg": 0.23146633240778638,
+      "auc": 2112.0,
+      "auc_normalized": 0.005952380952380952,
+      "ncg": 0.24958945340405878,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 7,
-          "cumulative_hits": 15,
-          "precision_at_batch": 0.0546875,
+          "hits": 3,
+          "cumulative_hits": 18,
+          "precision_at_batch": 0.0234375,
           "selected": [
-            "ATP6V1B1",
-            "MLNR",
-            "ENHO",
-            "STIM1",
-            "PRADC1",
-            "CNNM4",
-            "SPATA31A6",
-            "TOB1",
-            "AMPD3",
-            "UAP1L1",
-            "SLC16A10",
-            "PRKAR2B",
-            "ZNF341",
-            "SLC22A31",
-            "RC3H1",
-            "GABPB2",
-            "C7orf57",
-            "CSNK2A3",
-            "DHX58",
-            "PRRC2A",
-            "FAM122B",
-            "CNGA1",
-            "FAM98C",
-            "TUSC3",
-            "TNFAIP3",
-            "DNAJC25",
-            "RAB5A",
-            "TRPT1",
-            "MAN1A1",
-            "GFM1",
-            "PRSS56",
-            "CAPN12",
-            "BRD9",
-            "CACNB2",
-            "GMNC",
-            "CACNG5",
-            "FEV",
-            "MTMR14",
-            "MARS",
-            "CD99L2",
-            "USP45",
-            "CPQ",
-            "CACNA2D1",
-            "CLPP",
-            "SRC",
-            "OR5A1",
-            "OR51B6",
-            "WDR12",
-            "SLC37A4",
-            "FGF7",
-            "DLX3",
-            "CDKL2",
-            "NRN1L",
-            "BTBD16",
-            "LY6K",
-            "PPP1R27",
-            "GLTSCR1L",
-            "CCDC66",
-            "ZNF587",
-            "CYP26A1",
-            "MTUS1",
-            "TMPO",
-            "PNPO",
-            "SLC22A25",
-            "B4GALNT1",
-            "TBC1D10B",
-            "SAP130",
-            "CEP295NL",
-            "PLEKHB1",
-            "DNA2",
-            "CGRRF1",
-            "FAM134C",
-            "NDUFB8",
-            "CTDSP2",
-            "YIPF4",
-            "SETX",
-            "SLCO4C1",
-            "ATP5J2-PTCD1",
-            "EPT1",
-            "ABHD14B",
-            "CRYBA1",
-            "DHX33",
-            "DLGAP4",
-            "ALG14",
-            "PAK4",
-            "DDC",
-            "WNT6",
-            "TNS1",
-            "LMAN2L",
-            "SPRR2B",
-            "PATZ1",
-            "RAB22A",
-            "CHERP",
-            "ASB16",
-            "CLEC4E",
-            "HIST1H2AB",
-            "ZBTB45",
-            "EFCAB11",
-            "KLHL9",
-            "IFI44L",
-            "ATP2A2",
-            "PLCXD3",
-            "NCAPG",
-            "RECQL4",
-            "CLEC4D",
-            "SSH1",
-            "GATM",
-            "GORASP1",
-            "C10orf105",
-            "KCNJ1",
-            "N4BP2",
-            "IL2RA",
-            "PEF1",
-            "GORASP2",
-            "IER3",
-            "RAB34",
-            "RBAK",
-            "INTS2",
-            "CACNA1S",
-            "ST8SIA4",
-            "TRIM52",
-            "CADM1",
-            "CNPY4",
-            "ARAP1",
-            "AOX1",
-            "ZNF462",
-            "TYW3",
-            "TRPM7"
+            "RTEL1",
+            "VAPB",
+            "ZNF280A",
+            "DCPS",
+            "GANAB",
+            "PTPRN",
+            "IPP",
+            "MRPL43",
+            "ARHGEF11",
+            "INTS8",
+            "ADAT2",
+            "CORT",
+            "FAM26E",
+            "UCN3",
+            "NCKAP1",
+            "PTMA",
+            "RPP25L",
+            "OR1N2",
+            "PNLIPRP1",
+            "CCT7",
+            "PCDH7",
+            "MIR432",
+            "FAM96B",
+            "CYP1A1",
+            "UBC",
+            "CCDC77",
+            "CMYA5",
+            "MAN2B1",
+            "NPTX2",
+            "CTC1",
+            "MRPL48",
+            "ATAD2",
+            "PDZD4",
+            "RALB",
+            "CNPY3",
+            "TGFB1",
+            "TEX33",
+            "GPR32",
+            "GPD1",
+            "DPP4",
+            "LOC100506127",
+            "KRTAP4-7",
+            "BRSK1",
+            "BCDIN3D",
+            "SLC39A6",
+            "ATP5O",
+            "OR52N2",
+            "PRKAG1",
+            "TBCC",
+            "SPTAN1",
+            "ZNF208",
+            "FABP3",
+            "KCNJ2",
+            "TMED3",
+            "SRSF3",
+            "PEX5",
+            "BCL11A",
+            "MEGF6",
+            "FAM49A",
+            "ADCY9",
+            "INCENP",
+            "AK2",
+            "ZNF345",
+            "MICU2",
+            "PLK5",
+            "HAS3",
+            "RPL3L",
+            "CYBB",
+            "POLR3G",
+            "PCDHGA8",
+            "CYP2A13",
+            "INPP4B",
+            "C9orf85",
+            "SLC27A2",
+            "BPIFB3",
+            "TDG",
+            "C4A",
+            "F2R",
+            "KLF1",
+            "PASD1",
+            "C17orf67",
+            "SPANXC",
+            "TRIM42",
+            "HMGB3",
+            "NT5DC3",
+            "RPS4Y2",
+            "SLC4A5",
+            "MCF2L2",
+            "GDF15",
+            "WDR60",
+            "GRK5",
+            "CADM4",
+            "MGAM",
+            "TMEM156",
+            "LRRFIP2",
+            "CAV2",
+            "UGT2B7",
+            "OSR2",
+            "ZNF627",
+            "TMEM59",
+            "CBWD2",
+            "MOB3B",
+            "TNFSF13",
+            "NAPRT",
+            "RPGRIP1",
+            "RPP40",
+            "NCS1",
+            "ZNF671",
+            "SPINK6",
+            "CCRL2",
+            "NTS",
+            "LEO1",
+            "DUOXA1",
+            "DUSP26",
+            "DUSP28",
+            "CD300E",
+            "SMURF2",
+            "RIT1",
+            "PGBD3",
+            "SNX10",
+            "CFC1",
+            "MCIDAS",
+            "DYSF",
+            "MFAP3L",
+            "ZDHHC5",
+            "TSTA3",
+            "PPID",
+            "KRI1"
           ],
           "selected_scores": [
-            -0.201361404,
-            -0.747039243,
-            -1.741433183,
-            -0.872834543,
-            -0.400385782,
-            -1.958794925,
-            -1.8808401869999998,
-            -0.04263311400000001,
-            -1.560177346,
-            -1.242589671,
-            -0.299769754,
-            -2.180935028,
-            -0.747779243,
-            -3.097231897,
-            -0.284626373,
-            -0.753812977,
-            -2.4030170280000003,
-            -0.424770145,
-            -0.41948254799999996,
-            -1.7020696880000001,
-            -0.624585328,
-            -0.955465346,
-            -0.007484081,
-            -1.477456704,
-            -0.24478269600000002,
-            -0.144876628,
-            -0.816099185,
-            -1.36667693,
-            -0.538292791,
-            -0.751344198,
-            -0.32846977899999996,
-            -1.342826074,
-            -0.48776693600000004,
-            -0.929824685,
-            -0.657510787,
-            -0.554727847,
-            -0.5020772410000001,
-            -0.676362227,
-            -1.7221653730000002,
-            -0.8015028940000001,
-            -0.744610965,
-            -0.21542853399999998,
-            -0.841312252,
-            -0.754310446,
-            -0.18767251100000001,
-            -1.315155034,
-            -0.573881217,
-            -0.489996344,
-            -0.488998694,
-            -0.634709573,
-            -0.5142020860000001,
-            -0.798956039,
-            -0.603685331,
-            -0.46107903899999997,
-            -1.133163553,
-            -0.7634699640000001,
-            -0.532196444,
-            -1.953629576,
-            -0.668699053,
-            -1.181122722,
-            -2.095547005,
-            -0.380735899,
-            -0.625406357,
-            -0.594484782,
-            -0.646906026,
-            -1.332644192,
-            -1.7633453890000002,
-            -0.48691684399999996,
-            -0.42420400700000005,
-            -0.939162108,
-            -0.522701819,
-            -2.578453197,
-            -0.38708333899999997,
-            -0.972576826,
-            -0.82666332,
-            -0.532716148,
-            -0.516317234,
-            -0.037490411,
-            -0.6679974129999999,
-            -0.6283653889999999,
-            -0.268420642,
-            -0.541433907,
-            -1.46070239,
-            -2.68875708,
-            -1.8027060209999999,
-            -0.929506473,
-            -1.671571265,
-            -0.330736545,
-            -0.289915381,
-            -2.2582741669999997,
-            -0.340146965,
-            -0.39571887299999997,
-            -0.40377916399999997,
-            -0.86033773,
-            -0.7449079909999999,
-            -0.8507868270000001,
-            -1.194509909,
-            -0.620572869,
-            -0.6539120939999999,
-            -0.516216255,
-            -1.462034819,
-            -2.179757934,
-            -1.06309241,
-            -0.37270078,
-            -0.983796462,
-            -0.085117982,
-            -0.666915241,
-            -0.547693926,
-            -0.6930261940000001,
-            -0.92222815,
-            -0.5965225670000001,
-            -0.282283954,
-            -0.46186604200000003,
-            -0.608994797,
-            -0.383512454,
-            -0.5423345470000001,
-            -0.627505291,
-            -0.026746527000000003,
-            -0.258920282,
-            -0.514679575,
-            -1.223795966,
-            -0.447477214,
-            -2.1437942580000002,
-            -0.7953905440000001,
-            -0.330226245,
-            -0.126055812,
-            -1.423577743,
-            -1.254003543
+            -1.4855187669999999,
+            -1.2703910729999999,
+            -0.7558665640000001,
+            -1.195998507,
+            -0.63300024,
+            -0.9694214790000001,
+            -0.29513096,
+            -0.815280817,
+            -0.657764427,
+            -2.515189464,
+            -0.181357057,
+            -0.140774507,
+            -1.0365657959999999,
+            -2.0068613999999996,
+            -0.614692695,
+            -1.038748139,
+            -1.405789679,
+            -0.63151199,
+            -0.519566309,
+            -0.704492129,
+            -0.779044927,
+            -0.047927155,
+            -0.890342008,
+            -0.246907181,
+            -1.242476262,
+            -1.112939553,
+            -0.648189609,
+            -0.9480956159999999,
+            -2.401567439,
+            -0.278952628,
+            -0.373296909,
+            -0.534442847,
+            -1.689643157,
+            -0.827657419,
+            -0.22900884300000002,
+            -0.323883879,
+            -1.320435759,
+            -0.491993019,
+            -2.039463539,
+            -0.6797851090000001,
+            -1.118812634,
+            -3.346861492,
+            -0.236795593,
+            -0.8460896000000001,
+            -0.32367678,
+            -1.1252520990000001,
+            -0.842105975,
+            -1.2557984759999998,
+            -1.462807671,
+            -0.28914351,
+            -1.4629832409999999,
+            -0.6001938529999999,
+            -0.685301266,
+            -1.895656615,
+            -1.1955252440000002,
+            -1.004241742,
+            -0.608515755,
+            -0.441613959,
+            -0.45734107399999996,
+            -0.494880649,
+            -0.411976677,
+            -0.43550246600000003,
+            -0.7923046420000001,
+            -0.48885202,
+            -0.285187163,
+            -0.366737059,
+            -1.973648408,
+            -1.4469121919999999,
+            -0.34459338799999994,
+            -1.08085994,
+            -0.7921534929999999,
+            -0.576914143,
+            -0.9804685870000001,
+            -0.111658109,
+            -2.264809504,
+            -0.066540241,
+            -0.298375674,
+            -0.382332281,
+            -0.291552926,
+            -0.37730578200000003,
+            -1.124229479,
+            -0.608521103,
+            -1.022118105,
+            -1.0863716190000001,
+            -0.61964227,
+            -0.48291109299999996,
+            -2.063871355,
+            -0.420416412,
+            -1.127234176,
+            -0.40373960299999995,
+            -0.342649714,
+            -0.66884535,
+            -0.32805284,
+            -1.398034435,
+            -1.549298755,
+            -0.404721396,
+            -0.353900724,
+            -0.612890566,
+            -0.315584109,
+            -0.226062235,
+            -1.26286739,
+            -1.154290228,
+            -0.593435607,
+            -0.43343086700000005,
+            -1.242310251,
+            -1.092353034,
+            -0.167400781,
+            -1.530213681,
+            -0.235857347,
+            -2.039709218,
+            -0.349507898,
+            -1.901654728,
+            -1.175281715,
+            -0.354934275,
+            -0.212464882,
+            -0.416952297,
+            -1.7582445430000002,
+            -0.79174172,
+            -0.128372143,
+            -0.774897576,
+            -1.932787094,
+            -0.118253991,
+            -1.499861251,
+            -1.064490566,
+            -1.040591794,
+            -0.156054917,
+            -0.384717194,
+            -1.111219665
           ],
           "selected_hits": [
             0,
@@ -308,12 +308,40 @@
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
@@ -323,6 +351,31 @@
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
             1,
             0,
             0,
@@ -366,59 +419,6 @@
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
-            1,
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
             0,
             0,
             0,
@@ -1334,896 +1334,1792 @@
           "gene": "ATP6V1B1",
           "score": -0.201361404,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9448,
           "gene": "MLNR",
           "score": -0.747039243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4751,
           "gene": "ENHO",
           "score": -1.741433183,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15267,
           "gene": "STIM1",
           "score": -0.872834543,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12210,
           "gene": "PRADC1",
           "score": -0.400385782,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3178,
           "gene": "CNNM4",
           "score": -1.958794925,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14957,
           "gene": "SPATA31A6",
           "score": -1.8808401869999998,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16441,
           "gene": "TOB1",
           "score": -0.04263311400000001,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 630,
           "gene": "AMPD3",
           "score": -1.560177346,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16961,
           "gene": "UAP1L1",
           "score": -1.242589671,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14272,
           "gene": "SLC16A10",
           "score": -0.299769754,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12291,
           "gene": "PRKAR2B",
           "score": -2.180935028,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18046,
           "gene": "ZNF341",
           "score": -0.747779243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14327,
           "gene": "SLC22A31",
           "score": -3.097231897,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13005,
           "gene": "RC3H1",
           "score": -0.284626373,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5816,
           "gene": "GABPB2",
           "score": -0.753812977,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1903,
           "gene": "C7orf57",
           "score": -2.4030170280000003,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3542,
           "gene": "CSNK2A3",
           "score": -0.424770145,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4112,
           "gene": "DHX58",
           "score": -0.41948254799999996,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12407,
           "gene": "PRRC2A",
           "score": -1.7020696880000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5064,
           "gene": "FAM122B",
           "score": -0.624585328,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3159,
           "gene": "CNGA1",
           "score": -0.955465346,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5303,
           "gene": "FAM98C",
           "score": -0.007484081,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16907,
           "gene": "TUSC3",
           "score": -1.477456704,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16366,
           "gene": "TNFAIP3",
           "score": -0.24478269600000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4248,
           "gene": "DNAJC25",
           "score": -0.144876628,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12772,
           "gene": "RAB5A",
           "score": -0.816099185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16718,
           "gene": "TRPT1",
           "score": -1.36667693,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8980,
           "gene": "MAN1A1",
           "score": -0.538292791,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6001,
           "gene": "GFM1",
           "score": -0.751344198,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12443,
           "gene": "PRSS56",
           "score": -0.32846977899999996,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2094,
           "gene": "CAPN12",
           "score": -1.342826074,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1614,
           "gene": "BRD9",
           "score": -0.48776693600000004,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2017,
           "gene": "CACNB2",
           "score": -0.929824685,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6158,
           "gene": "GMNC",
           "score": -0.657510787,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2024,
           "gene": "CACNG5",
           "score": -0.554727847,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5472,
           "gene": "FEV",
           "score": -0.5020772410000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9781,
           "gene": "MTMR14",
           "score": -0.676362227,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9091,
           "gene": "MARS",
           "score": -1.7221653730000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2540,
           "gene": "CD99L2",
           "score": -0.8015028940000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17229,
           "gene": "USP45",
           "score": -0.744610965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3402,
           "gene": "CPQ",
           "score": -0.21542853399999998,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2012,
           "gene": "CACNA2D1",
           "score": -0.841312252,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3105,
           "gene": "CLPP",
           "score": -0.754310446,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15098,
           "gene": "SRC",
           "score": -0.18767251100000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10935,
           "gene": "OR5A1",
           "score": -1.315155034,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10899,
           "gene": "OR51B6",
           "score": -0.573881217,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17447,
           "gene": "WDR12",
           "score": -0.489996344,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14483,
           "gene": "SLC37A4",
           "score": -0.488998694,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5508,
           "gene": "FGF7",
           "score": -0.634709573,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4170,
           "gene": "DLX3",
           "score": -0.5142020860000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2644,
           "gene": "CDKL2",
           "score": -0.798956039,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10549,
           "gene": "NRN1L",
           "score": -0.603685331,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1652,
           "gene": "BTBD16",
           "score": -0.46107903899999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8855,
           "gene": "LY6K",
           "score": -1.133163553,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12150,
           "gene": "PPP1R27",
           "score": -0.7634699640000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6138,
           "gene": "GLTSCR1L",
           "score": -0.532196444,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2320,
           "gene": "CCDC66",
           "score": -1.953629576,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18210,
           "gene": "ZNF587",
           "score": -0.668699053,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3741,
           "gene": "CYP26A1",
           "score": -1.181122722,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9809,
           "gene": "MTUS1",
           "score": -2.095547005,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16330,
           "gene": "TMPO",
           "score": -0.380735899,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11935,
           "gene": "PNPO",
           "score": -0.625406357,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14325,
           "gene": "SLC22A25",
           "score": -0.594484782,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1362,
           "gene": "B4GALNT1",
           "score": -0.646906026,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15613,
           "gene": "TBC1D10B",
           "score": -1.332644192,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13695,
           "gene": "SAP130",
           "score": -1.7633453890000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2758,
           "gene": "CEP295NL",
           "score": -0.48691684399999996,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11820,
           "gene": "PLEKHB1",
           "score": -0.42420400700000005,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4197,
           "gene": "DNA2",
           "score": -0.939162108,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2843,
           "gene": "CGRRF1",
           "score": -0.522701819,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5085,
           "gene": "FAM134C",
           "score": -2.578453197,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10153,
           "gene": "NDUFB8",
           "score": -0.38708333899999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3596,
           "gene": "CTDSP2",
           "score": -0.972576826,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17656,
           "gene": "YIPF4",
           "score": -0.82666332,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14021,
           "gene": "SETX",
           "score": -0.532716148,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14623,
           "gene": "SLCO4C1",
           "score": -0.516317234,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1252,
           "gene": "ATP5J2-PTCD1",
           "score": -0.037490411,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4837,
           "gene": "EPT1",
           "score": -0.6679974129999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 82,
           "gene": "ABHD14B",
           "score": -0.6283653889999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3491,
           "gene": "CRYBA1",
           "score": -0.268420642,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4104,
           "gene": "DHX33",
           "score": -0.541433907,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4160,
           "gene": "DLGAP4",
           "score": -1.46070239,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 561,
           "gene": "ALG14",
           "score": -2.68875708,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11144,
           "gene": "PAK4",
           "score": -1.8027060209999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3914,
           "gene": "DDC",
           "score": -0.929506473,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17561,
           "gene": "WNT6",
           "score": -1.671571265,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16436,
           "gene": "TNS1",
           "score": -0.330736545,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8548,
           "gene": "LMAN2L",
           "score": -0.289915381,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15059,
           "gene": "SPRR2B",
           "score": -2.2582741669999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11224,
           "gene": "PATZ1",
           "score": -0.340146965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12731,
           "gene": "RAB22A",
           "score": -0.39571887299999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2874,
           "gene": "CHERP",
           "score": -0.40377916399999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1102,
           "gene": "ASB16",
           "score": -0.86033773,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3066,
           "gene": "CLEC4E",
           "score": -0.7449079909999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6798,
           "gene": "HIST1H2AB",
           "score": -0.8507868270000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17731,
           "gene": "ZBTB45",
           "score": -1.194509909,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4553,
           "gene": "EFCAB11",
           "score": -0.620572869,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8074,
           "gene": "KLHL9",
           "score": -0.6539120939999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7211,
           "gene": "IFI44L",
           "score": -0.516216255,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1229,
           "gene": "ATP2A2",
           "score": -1.462034819,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11801,
           "gene": "PLCXD3",
           "score": -2.179757934,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10066,
           "gene": "NCAPG",
           "score": -1.06309241,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13042,
           "gene": "RECQL4",
           "score": -0.37270078,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3065,
           "gene": "CLEC4D",
           "score": -0.983796462,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15164,
           "gene": "SSH1",
           "score": -0.085117982,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5917,
           "gene": "GATM",
           "score": -0.666915241,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6245,
           "gene": "GORASP1",
           "score": -0.547693926,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1695,
           "gene": "C10orf105",
           "score": -0.6930261940000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7758,
           "gene": "KCNJ1",
           "score": -0.92222815,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9964,
           "gene": "N4BP2",
           "score": -0.5965225670000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7378,
           "gene": "IL2RA",
           "score": -0.282283954,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11469,
           "gene": "PEF1",
           "score": -0.46186604200000003,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6246,
           "gene": "GORASP2",
           "score": -0.608994797,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7198,
           "gene": "IER3",
           "score": -0.383512454,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12747,
           "gene": "RAB34",
           "score": -0.5423345470000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12924,
           "gene": "RBAK",
           "score": -0.627505291,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7475,
           "gene": "INTS2",
           "score": -0.026746527000000003,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2011,
           "gene": "CACNA1S",
           "score": -0.258920282,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15219,
           "gene": "ST8SIA4",
           "score": -0.514679575,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16641,
           "gene": "TRIM52",
           "score": -1.223795966,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2032,
           "gene": "CADM1",
           "score": -0.447477214,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3194,
           "gene": "CNPY4",
           "score": -2.1437942580000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 899,
           "gene": "ARAP1",
           "score": -0.7953905440000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 784,
           "gene": "AOX1",
           "score": -0.330226245,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18114,
           "gene": "ZNF462",
           "score": -0.126055812,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16953,
           "gene": "TYW3",
           "score": -1.423577743,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16715,
           "gene": "TRPM7",
           "score": -1.254003543,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 13581,
+          "gene": "RTEL1",
+          "score": -1.4855187669999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17277,
+          "gene": "VAPB",
+          "score": -1.2703910729999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18007,
+          "gene": "ZNF280A",
+          "score": -0.7558665640000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3889,
+          "gene": "DCPS",
+          "score": -1.195998507,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5884,
+          "gene": "GANAB",
+          "score": -0.63300024,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12623,
+          "gene": "PTPRN",
+          "score": -0.9694214790000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7497,
+          "gene": "IPP",
+          "score": -0.29513096,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9635,
+          "gene": "MRPL43",
+          "score": -0.815280817,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 963,
+          "gene": "ARHGEF11",
+          "score": -0.657764427,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7481,
+          "gene": "INTS8",
+          "score": -2.515189464,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 291,
+          "gene": "ADAT2",
+          "score": -0.181357057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3338,
+          "gene": "CORT",
+          "score": -0.140774507,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5221,
+          "gene": "FAM26E",
+          "score": -1.0365657959999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17069,
+          "gene": "UCN3",
+          "score": -2.0068613999999996,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10080,
+          "gene": "NCKAP1",
+          "score": -0.614692695,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12585,
+          "gene": "PTMA",
+          "score": -1.038748139,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13467,
+          "gene": "RPP25L",
+          "score": -1.405789679,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10843,
+          "gene": "OR1N2",
+          "score": -0.63151199,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11912,
+          "gene": "PNLIPRP1",
+          "score": -0.519566309,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2447,
+          "gene": "CCT7",
+          "score": -0.704492129,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11266,
+          "gene": "PCDH7",
+          "score": -0.779044927,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9408,
+          "gene": "MIR432",
+          "score": -0.047927155,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 5300,
+          "gene": "FAM96B",
+          "score": -0.890342008,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3735,
+          "gene": "CYP1A1",
+          "score": -0.246907181,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16980,
+          "gene": "UBC",
+          "score": -1.242476262,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2331,
+          "gene": "CCDC77",
+          "score": -1.112939553,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3151,
+          "gene": "CMYA5",
+          "score": -0.648189609,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8986,
+          "gene": "MAN2B1",
+          "score": -0.9480956159999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10490,
+          "gene": "NPTX2",
+          "score": -2.401567439,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3590,
+          "gene": "CTC1",
+          "score": -0.278952628,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9640,
+          "gene": "MRPL48",
+          "score": -0.373296909,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1160,
+          "gene": "ATAD2",
+          "score": -0.534442847,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11455,
+          "gene": "PDZD4",
+          "score": -1.689643157,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12833,
+          "gene": "RALB",
+          "score": -0.827657419,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3193,
+          "gene": "CNPY3",
+          "score": -0.22900884300000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15861,
+          "gene": "TGFB1",
+          "score": -0.323883879,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15823,
+          "gene": "TEX33",
+          "score": -1.320435759,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6347,
+          "gene": "GPR32",
+          "score": -0.491993019,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6281,
+          "gene": "GPD1",
+          "score": -2.039463539,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4336,
+          "gene": "DPP4",
+          "score": -0.6797851090000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8594,
+          "gene": "LOC100506127",
+          "score": -1.118812634,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8253,
+          "gene": "KRTAP4-7",
+          "score": -3.346861492,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 1634,
+          "gene": "BRSK1",
+          "score": -0.236795593,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1442,
+          "gene": "BCDIN3D",
+          "score": -0.8460896000000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14505,
+          "gene": "SLC39A6",
+          "score": -0.32367678,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1255,
+          "gene": "ATP5O",
+          "score": -1.1252520990000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10927,
+          "gene": "OR52N2",
+          "score": -0.842105975,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12285,
+          "gene": "PRKAG1",
+          "score": -1.2557984759999998,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15651,
+          "gene": "TBCC",
+          "score": -1.462807671,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15079,
+          "gene": "SPTAN1",
+          "score": -0.28914351,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17960,
+          "gene": "ZNF208",
+          "score": -1.4629832409999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5017,
+          "gene": "FABP3",
+          "score": -0.6001938529999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7766,
+          "gene": "KCNJ2",
+          "score": -0.685301266,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16063,
+          "gene": "TMED3",
+          "score": -1.895656615,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15144,
+          "gene": "SRSF3",
+          "score": -1.1955252440000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11500,
+          "gene": "PEX5",
+          "score": -1.004241742,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1448,
+          "gene": "BCL11A",
+          "score": -0.608515755,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9252,
+          "gene": "MEGF6",
+          "score": -0.441613959,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5241,
+          "gene": "FAM49A",
+          "score": -0.45734107399999996,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 307,
+          "gene": "ADCY9",
+          "score": -0.494880649,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7429,
+          "gene": "INCENP",
+          "score": -0.411976677,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 482,
+          "gene": "AK2",
+          "score": -0.43550246600000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18048,
+          "gene": "ZNF345",
+          "score": -0.7923046420000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9375,
+          "gene": "MICU2",
+          "score": -0.48885202,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11858,
+          "gene": "PLK5",
+          "score": -0.285187163,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6626,
+          "gene": "HAS3",
+          "score": -0.366737059,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13450,
+          "gene": "RPL3L",
+          "score": -1.973648408,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3719,
+          "gene": "CYBB",
+          "score": -1.4469121919999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12001,
+          "gene": "POLR3G",
+          "score": -0.34459338799999994,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11310,
+          "gene": "PCDHGA8",
+          "score": -1.08085994,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3747,
+          "gene": "CYP2A13",
+          "score": -0.7921534929999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7450,
+          "gene": "INPP4B",
+          "score": -0.576914143,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1968,
+          "gene": "C9orf85",
+          "score": -0.9804685870000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14402,
+          "gene": "SLC27A2",
+          "score": -0.111658109,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1593,
+          "gene": "BPIFB3",
+          "score": -2.264809504,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15752,
+          "gene": "TDG",
+          "score": -0.066540241,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 1859,
+          "gene": "C4A",
+          "score": -0.298375674,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4999,
+          "gene": "F2R",
+          "score": -0.382332281,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8011,
+          "gene": "KLF1",
+          "score": -0.291552926,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11216,
+          "gene": "PASD1",
+          "score": -0.37730578200000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1745,
+          "gene": "C17orf67",
+          "score": -1.124229479,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14929,
+          "gene": "SPANXC",
+          "score": -0.608521103,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16629,
+          "gene": "TRIM42",
+          "score": -1.022118105,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6905,
+          "gene": "HMGB3",
+          "score": -1.0863716190000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10587,
+          "gene": "NT5DC3",
+          "score": -0.61964227,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13503,
+          "gene": "RPS4Y2",
+          "score": -0.48291109299999996,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14540,
+          "gene": "SLC4A5",
+          "score": -2.063871355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9162,
+          "gene": "MCF2L2",
+          "score": -0.420416412,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5972,
+          "gene": "GDF15",
+          "score": -1.127234176,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17482,
+          "gene": "WDR60",
+          "score": -0.40373960299999995,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6447,
+          "gene": "GRK5",
+          "score": -0.342649714,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2035,
+          "gene": "CADM4",
+          "score": -0.66884535,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9342,
+          "gene": "MGAM",
+          "score": -0.32805284,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16132,
+          "gene": "TMEM156",
+          "score": -1.398034435,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8780,
+          "gene": "LRRFIP2",
+          "score": -1.549298755,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2172,
+          "gene": "CAV2",
+          "score": -0.404721396,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17102,
+          "gene": "UGT2B7",
+          "score": -0.353900724,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11022,
+          "gene": "OSR2",
+          "score": -0.612890566,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18241,
+          "gene": "ZNF627",
+          "score": -0.315584109,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16281,
+          "gene": "TMEM59",
+          "score": -0.226062235,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2190,
+          "gene": "CBWD2",
+          "score": -1.26286739,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9502,
+          "gene": "MOB3B",
+          "score": -1.154290228,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16398,
+          "gene": "TNFSF13",
+          "score": -0.593435607,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10025,
+          "gene": "NAPRT",
+          "score": -0.43343086700000005,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13405,
+          "gene": "RPGRIP1",
+          "score": -1.242310251,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13470,
+          "gene": "RPP40",
+          "score": -1.092353034,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10101,
+          "gene": "NCS1",
+          "score": -0.167400781,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18267,
+          "gene": "ZNF671",
+          "score": -1.530213681,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15022,
+          "gene": "SPINK6",
+          "score": -0.235857347,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2435,
+          "gene": "CCRL2",
+          "score": -2.039709218,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10607,
+          "gene": "NTS",
+          "score": -0.349507898,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8431,
+          "gene": "LEO1",
+          "score": -1.901654728,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4414,
+          "gene": "DUOXA1",
+          "score": -1.175281715,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4435,
+          "gene": "DUSP26",
+          "score": -0.354934275,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4437,
+          "gene": "DUSP28",
+          "score": -0.212464882,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2488,
+          "gene": "CD300E",
+          "score": -0.416952297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14751,
+          "gene": "SMURF2",
+          "score": -1.7582445430000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13234,
+          "gene": "RIT1",
+          "score": -0.79174172,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11535,
+          "gene": "PGBD3",
+          "score": -0.128372143,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14811,
+          "gene": "SNX10",
+          "score": -0.774897576,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2816,
+          "gene": "CFC1",
+          "score": -1.932787094,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9166,
+          "gene": "MCIDAS",
+          "score": -0.118253991,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4473,
+          "gene": "DYSF",
+          "score": -1.499861251,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9316,
+          "gene": "MFAP3L",
+          "score": -1.064490566,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17807,
+          "gene": "ZDHHC5",
+          "score": -1.040591794,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16800,
+          "gene": "TSTA3",
+          "score": -0.156054917,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12097,
+          "gene": "PPID",
+          "score": -0.384717194,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8133,
+          "gene": "KRI1",
+          "score": -1.111219665,
+          "hit": 0,
+          "round": 2
         }
       ],
       "queried_history": [
@@ -3128,896 +4024,1792 @@
           "gene": "ATP6V1B1",
           "score": -0.201361404,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9448,
           "gene": "MLNR",
           "score": -0.747039243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4751,
           "gene": "ENHO",
           "score": -1.741433183,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15267,
           "gene": "STIM1",
           "score": -0.872834543,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12210,
           "gene": "PRADC1",
           "score": -0.400385782,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3178,
           "gene": "CNNM4",
           "score": -1.958794925,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14957,
           "gene": "SPATA31A6",
           "score": -1.8808401869999998,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16441,
           "gene": "TOB1",
           "score": -0.04263311400000001,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 630,
           "gene": "AMPD3",
           "score": -1.560177346,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16961,
           "gene": "UAP1L1",
           "score": -1.242589671,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14272,
           "gene": "SLC16A10",
           "score": -0.299769754,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12291,
           "gene": "PRKAR2B",
           "score": -2.180935028,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18046,
           "gene": "ZNF341",
           "score": -0.747779243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14327,
           "gene": "SLC22A31",
           "score": -3.097231897,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13005,
           "gene": "RC3H1",
           "score": -0.284626373,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5816,
           "gene": "GABPB2",
           "score": -0.753812977,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1903,
           "gene": "C7orf57",
           "score": -2.4030170280000003,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3542,
           "gene": "CSNK2A3",
           "score": -0.424770145,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4112,
           "gene": "DHX58",
           "score": -0.41948254799999996,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12407,
           "gene": "PRRC2A",
           "score": -1.7020696880000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5064,
           "gene": "FAM122B",
           "score": -0.624585328,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3159,
           "gene": "CNGA1",
           "score": -0.955465346,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5303,
           "gene": "FAM98C",
           "score": -0.007484081,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16907,
           "gene": "TUSC3",
           "score": -1.477456704,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16366,
           "gene": "TNFAIP3",
           "score": -0.24478269600000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4248,
           "gene": "DNAJC25",
           "score": -0.144876628,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12772,
           "gene": "RAB5A",
           "score": -0.816099185,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16718,
           "gene": "TRPT1",
           "score": -1.36667693,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8980,
           "gene": "MAN1A1",
           "score": -0.538292791,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6001,
           "gene": "GFM1",
           "score": -0.751344198,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12443,
           "gene": "PRSS56",
           "score": -0.32846977899999996,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2094,
           "gene": "CAPN12",
           "score": -1.342826074,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1614,
           "gene": "BRD9",
           "score": -0.48776693600000004,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2017,
           "gene": "CACNB2",
           "score": -0.929824685,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6158,
           "gene": "GMNC",
           "score": -0.657510787,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2024,
           "gene": "CACNG5",
           "score": -0.554727847,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5472,
           "gene": "FEV",
           "score": -0.5020772410000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9781,
           "gene": "MTMR14",
           "score": -0.676362227,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9091,
           "gene": "MARS",
           "score": -1.7221653730000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2540,
           "gene": "CD99L2",
           "score": -0.8015028940000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17229,
           "gene": "USP45",
           "score": -0.744610965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3402,
           "gene": "CPQ",
           "score": -0.21542853399999998,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2012,
           "gene": "CACNA2D1",
           "score": -0.841312252,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3105,
           "gene": "CLPP",
           "score": -0.754310446,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15098,
           "gene": "SRC",
           "score": -0.18767251100000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10935,
           "gene": "OR5A1",
           "score": -1.315155034,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10899,
           "gene": "OR51B6",
           "score": -0.573881217,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17447,
           "gene": "WDR12",
           "score": -0.489996344,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14483,
           "gene": "SLC37A4",
           "score": -0.488998694,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5508,
           "gene": "FGF7",
           "score": -0.634709573,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4170,
           "gene": "DLX3",
           "score": -0.5142020860000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2644,
           "gene": "CDKL2",
           "score": -0.798956039,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10549,
           "gene": "NRN1L",
           "score": -0.603685331,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1652,
           "gene": "BTBD16",
           "score": -0.46107903899999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8855,
           "gene": "LY6K",
           "score": -1.133163553,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12150,
           "gene": "PPP1R27",
           "score": -0.7634699640000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6138,
           "gene": "GLTSCR1L",
           "score": -0.532196444,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2320,
           "gene": "CCDC66",
           "score": -1.953629576,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18210,
           "gene": "ZNF587",
           "score": -0.668699053,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3741,
           "gene": "CYP26A1",
           "score": -1.181122722,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9809,
           "gene": "MTUS1",
           "score": -2.095547005,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16330,
           "gene": "TMPO",
           "score": -0.380735899,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11935,
           "gene": "PNPO",
           "score": -0.625406357,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14325,
           "gene": "SLC22A25",
           "score": -0.594484782,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1362,
           "gene": "B4GALNT1",
           "score": -0.646906026,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15613,
           "gene": "TBC1D10B",
           "score": -1.332644192,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13695,
           "gene": "SAP130",
           "score": -1.7633453890000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2758,
           "gene": "CEP295NL",
           "score": -0.48691684399999996,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11820,
           "gene": "PLEKHB1",
           "score": -0.42420400700000005,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4197,
           "gene": "DNA2",
           "score": -0.939162108,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2843,
           "gene": "CGRRF1",
           "score": -0.522701819,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5085,
           "gene": "FAM134C",
           "score": -2.578453197,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10153,
           "gene": "NDUFB8",
           "score": -0.38708333899999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3596,
           "gene": "CTDSP2",
           "score": -0.972576826,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17656,
           "gene": "YIPF4",
           "score": -0.82666332,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14021,
           "gene": "SETX",
           "score": -0.532716148,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14623,
           "gene": "SLCO4C1",
           "score": -0.516317234,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1252,
           "gene": "ATP5J2-PTCD1",
           "score": -0.037490411,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4837,
           "gene": "EPT1",
           "score": -0.6679974129999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 82,
           "gene": "ABHD14B",
           "score": -0.6283653889999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3491,
           "gene": "CRYBA1",
           "score": -0.268420642,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4104,
           "gene": "DHX33",
           "score": -0.541433907,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4160,
           "gene": "DLGAP4",
           "score": -1.46070239,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 561,
           "gene": "ALG14",
           "score": -2.68875708,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11144,
           "gene": "PAK4",
           "score": -1.8027060209999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3914,
           "gene": "DDC",
           "score": -0.929506473,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17561,
           "gene": "WNT6",
           "score": -1.671571265,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16436,
           "gene": "TNS1",
           "score": -0.330736545,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8548,
           "gene": "LMAN2L",
           "score": -0.289915381,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15059,
           "gene": "SPRR2B",
           "score": -2.2582741669999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11224,
           "gene": "PATZ1",
           "score": -0.340146965,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12731,
           "gene": "RAB22A",
           "score": -0.39571887299999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2874,
           "gene": "CHERP",
           "score": -0.40377916399999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1102,
           "gene": "ASB16",
           "score": -0.86033773,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3066,
           "gene": "CLEC4E",
           "score": -0.7449079909999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6798,
           "gene": "HIST1H2AB",
           "score": -0.8507868270000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17731,
           "gene": "ZBTB45",
           "score": -1.194509909,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 4553,
           "gene": "EFCAB11",
           "score": -0.620572869,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8074,
           "gene": "KLHL9",
           "score": -0.6539120939999999,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7211,
           "gene": "IFI44L",
           "score": -0.516216255,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1229,
           "gene": "ATP2A2",
           "score": -1.462034819,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11801,
           "gene": "PLCXD3",
           "score": -2.179757934,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10066,
           "gene": "NCAPG",
           "score": -1.06309241,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13042,
           "gene": "RECQL4",
           "score": -0.37270078,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3065,
           "gene": "CLEC4D",
           "score": -0.983796462,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15164,
           "gene": "SSH1",
           "score": -0.085117982,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5917,
           "gene": "GATM",
           "score": -0.666915241,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6245,
           "gene": "GORASP1",
           "score": -0.547693926,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1695,
           "gene": "C10orf105",
           "score": -0.6930261940000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7758,
           "gene": "KCNJ1",
           "score": -0.92222815,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9964,
           "gene": "N4BP2",
           "score": -0.5965225670000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7378,
           "gene": "IL2RA",
           "score": -0.282283954,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11469,
           "gene": "PEF1",
           "score": -0.46186604200000003,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6246,
           "gene": "GORASP2",
           "score": -0.608994797,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7198,
           "gene": "IER3",
           "score": -0.383512454,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12747,
           "gene": "RAB34",
           "score": -0.5423345470000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12924,
           "gene": "RBAK",
           "score": -0.627505291,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7475,
           "gene": "INTS2",
           "score": -0.026746527000000003,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2011,
           "gene": "CACNA1S",
           "score": -0.258920282,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15219,
           "gene": "ST8SIA4",
           "score": -0.514679575,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16641,
           "gene": "TRIM52",
           "score": -1.223795966,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2032,
           "gene": "CADM1",
           "score": -0.447477214,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3194,
           "gene": "CNPY4",
           "score": -2.1437942580000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 899,
           "gene": "ARAP1",
           "score": -0.7953905440000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 784,
           "gene": "AOX1",
           "score": -0.330226245,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18114,
           "gene": "ZNF462",
           "score": -0.126055812,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16953,
           "gene": "TYW3",
           "score": -1.423577743,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16715,
           "gene": "TRPM7",
           "score": -1.254003543,
           "hit": 0,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 13581,
+          "gene": "RTEL1",
+          "score": -1.4855187669999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17277,
+          "gene": "VAPB",
+          "score": -1.2703910729999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18007,
+          "gene": "ZNF280A",
+          "score": -0.7558665640000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3889,
+          "gene": "DCPS",
+          "score": -1.195998507,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5884,
+          "gene": "GANAB",
+          "score": -0.63300024,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12623,
+          "gene": "PTPRN",
+          "score": -0.9694214790000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7497,
+          "gene": "IPP",
+          "score": -0.29513096,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9635,
+          "gene": "MRPL43",
+          "score": -0.815280817,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 963,
+          "gene": "ARHGEF11",
+          "score": -0.657764427,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7481,
+          "gene": "INTS8",
+          "score": -2.515189464,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 291,
+          "gene": "ADAT2",
+          "score": -0.181357057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3338,
+          "gene": "CORT",
+          "score": -0.140774507,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5221,
+          "gene": "FAM26E",
+          "score": -1.0365657959999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17069,
+          "gene": "UCN3",
+          "score": -2.0068613999999996,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10080,
+          "gene": "NCKAP1",
+          "score": -0.614692695,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12585,
+          "gene": "PTMA",
+          "score": -1.038748139,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13467,
+          "gene": "RPP25L",
+          "score": -1.405789679,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10843,
+          "gene": "OR1N2",
+          "score": -0.63151199,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11912,
+          "gene": "PNLIPRP1",
+          "score": -0.519566309,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2447,
+          "gene": "CCT7",
+          "score": -0.704492129,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11266,
+          "gene": "PCDH7",
+          "score": -0.779044927,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9408,
+          "gene": "MIR432",
+          "score": -0.047927155,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 5300,
+          "gene": "FAM96B",
+          "score": -0.890342008,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3735,
+          "gene": "CYP1A1",
+          "score": -0.246907181,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16980,
+          "gene": "UBC",
+          "score": -1.242476262,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2331,
+          "gene": "CCDC77",
+          "score": -1.112939553,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3151,
+          "gene": "CMYA5",
+          "score": -0.648189609,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8986,
+          "gene": "MAN2B1",
+          "score": -0.9480956159999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10490,
+          "gene": "NPTX2",
+          "score": -2.401567439,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3590,
+          "gene": "CTC1",
+          "score": -0.278952628,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9640,
+          "gene": "MRPL48",
+          "score": -0.373296909,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1160,
+          "gene": "ATAD2",
+          "score": -0.534442847,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11455,
+          "gene": "PDZD4",
+          "score": -1.689643157,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12833,
+          "gene": "RALB",
+          "score": -0.827657419,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3193,
+          "gene": "CNPY3",
+          "score": -0.22900884300000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15861,
+          "gene": "TGFB1",
+          "score": -0.323883879,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15823,
+          "gene": "TEX33",
+          "score": -1.320435759,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6347,
+          "gene": "GPR32",
+          "score": -0.491993019,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6281,
+          "gene": "GPD1",
+          "score": -2.039463539,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4336,
+          "gene": "DPP4",
+          "score": -0.6797851090000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8594,
+          "gene": "LOC100506127",
+          "score": -1.118812634,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8253,
+          "gene": "KRTAP4-7",
+          "score": -3.346861492,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 1634,
+          "gene": "BRSK1",
+          "score": -0.236795593,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1442,
+          "gene": "BCDIN3D",
+          "score": -0.8460896000000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14505,
+          "gene": "SLC39A6",
+          "score": -0.32367678,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1255,
+          "gene": "ATP5O",
+          "score": -1.1252520990000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10927,
+          "gene": "OR52N2",
+          "score": -0.842105975,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12285,
+          "gene": "PRKAG1",
+          "score": -1.2557984759999998,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15651,
+          "gene": "TBCC",
+          "score": -1.462807671,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15079,
+          "gene": "SPTAN1",
+          "score": -0.28914351,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17960,
+          "gene": "ZNF208",
+          "score": -1.4629832409999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5017,
+          "gene": "FABP3",
+          "score": -0.6001938529999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7766,
+          "gene": "KCNJ2",
+          "score": -0.685301266,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16063,
+          "gene": "TMED3",
+          "score": -1.895656615,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15144,
+          "gene": "SRSF3",
+          "score": -1.1955252440000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11500,
+          "gene": "PEX5",
+          "score": -1.004241742,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1448,
+          "gene": "BCL11A",
+          "score": -0.608515755,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9252,
+          "gene": "MEGF6",
+          "score": -0.441613959,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5241,
+          "gene": "FAM49A",
+          "score": -0.45734107399999996,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 307,
+          "gene": "ADCY9",
+          "score": -0.494880649,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7429,
+          "gene": "INCENP",
+          "score": -0.411976677,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 482,
+          "gene": "AK2",
+          "score": -0.43550246600000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18048,
+          "gene": "ZNF345",
+          "score": -0.7923046420000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9375,
+          "gene": "MICU2",
+          "score": -0.48885202,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11858,
+          "gene": "PLK5",
+          "score": -0.285187163,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6626,
+          "gene": "HAS3",
+          "score": -0.366737059,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13450,
+          "gene": "RPL3L",
+          "score": -1.973648408,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3719,
+          "gene": "CYBB",
+          "score": -1.4469121919999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12001,
+          "gene": "POLR3G",
+          "score": -0.34459338799999994,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11310,
+          "gene": "PCDHGA8",
+          "score": -1.08085994,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3747,
+          "gene": "CYP2A13",
+          "score": -0.7921534929999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7450,
+          "gene": "INPP4B",
+          "score": -0.576914143,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1968,
+          "gene": "C9orf85",
+          "score": -0.9804685870000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14402,
+          "gene": "SLC27A2",
+          "score": -0.111658109,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1593,
+          "gene": "BPIFB3",
+          "score": -2.264809504,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15752,
+          "gene": "TDG",
+          "score": -0.066540241,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 1859,
+          "gene": "C4A",
+          "score": -0.298375674,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4999,
+          "gene": "F2R",
+          "score": -0.382332281,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8011,
+          "gene": "KLF1",
+          "score": -0.291552926,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11216,
+          "gene": "PASD1",
+          "score": -0.37730578200000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1745,
+          "gene": "C17orf67",
+          "score": -1.124229479,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14929,
+          "gene": "SPANXC",
+          "score": -0.608521103,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16629,
+          "gene": "TRIM42",
+          "score": -1.022118105,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6905,
+          "gene": "HMGB3",
+          "score": -1.0863716190000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10587,
+          "gene": "NT5DC3",
+          "score": -0.61964227,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13503,
+          "gene": "RPS4Y2",
+          "score": -0.48291109299999996,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14540,
+          "gene": "SLC4A5",
+          "score": -2.063871355,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9162,
+          "gene": "MCF2L2",
+          "score": -0.420416412,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5972,
+          "gene": "GDF15",
+          "score": -1.127234176,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17482,
+          "gene": "WDR60",
+          "score": -0.40373960299999995,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6447,
+          "gene": "GRK5",
+          "score": -0.342649714,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2035,
+          "gene": "CADM4",
+          "score": -0.66884535,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9342,
+          "gene": "MGAM",
+          "score": -0.32805284,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16132,
+          "gene": "TMEM156",
+          "score": -1.398034435,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8780,
+          "gene": "LRRFIP2",
+          "score": -1.549298755,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2172,
+          "gene": "CAV2",
+          "score": -0.404721396,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17102,
+          "gene": "UGT2B7",
+          "score": -0.353900724,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11022,
+          "gene": "OSR2",
+          "score": -0.612890566,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18241,
+          "gene": "ZNF627",
+          "score": -0.315584109,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16281,
+          "gene": "TMEM59",
+          "score": -0.226062235,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2190,
+          "gene": "CBWD2",
+          "score": -1.26286739,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9502,
+          "gene": "MOB3B",
+          "score": -1.154290228,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16398,
+          "gene": "TNFSF13",
+          "score": -0.593435607,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10025,
+          "gene": "NAPRT",
+          "score": -0.43343086700000005,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13405,
+          "gene": "RPGRIP1",
+          "score": -1.242310251,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13470,
+          "gene": "RPP40",
+          "score": -1.092353034,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10101,
+          "gene": "NCS1",
+          "score": -0.167400781,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18267,
+          "gene": "ZNF671",
+          "score": -1.530213681,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15022,
+          "gene": "SPINK6",
+          "score": -0.235857347,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2435,
+          "gene": "CCRL2",
+          "score": -2.039709218,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10607,
+          "gene": "NTS",
+          "score": -0.349507898,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8431,
+          "gene": "LEO1",
+          "score": -1.901654728,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4414,
+          "gene": "DUOXA1",
+          "score": -1.175281715,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4435,
+          "gene": "DUSP26",
+          "score": -0.354934275,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4437,
+          "gene": "DUSP28",
+          "score": -0.212464882,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2488,
+          "gene": "CD300E",
+          "score": -0.416952297,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14751,
+          "gene": "SMURF2",
+          "score": -1.7582445430000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13234,
+          "gene": "RIT1",
+          "score": -0.79174172,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11535,
+          "gene": "PGBD3",
+          "score": -0.128372143,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14811,
+          "gene": "SNX10",
+          "score": -0.774897576,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2816,
+          "gene": "CFC1",
+          "score": -1.932787094,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9166,
+          "gene": "MCIDAS",
+          "score": -0.118253991,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4473,
+          "gene": "DYSF",
+          "score": -1.499861251,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9316,
+          "gene": "MFAP3L",
+          "score": -1.064490566,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17807,
+          "gene": "ZDHHC5",
+          "score": -1.040591794,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16800,
+          "gene": "TSTA3",
+          "score": -0.156054917,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12097,
+          "gene": "PPID",
+          "score": -0.384717194,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8133,
+          "gene": "KRI1",
+          "score": -1.111219665,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
