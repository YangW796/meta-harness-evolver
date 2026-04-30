# Change Record — candidate_3

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21/run-2/best/current/harness
Generated at: 2026-04-30T07:21:55.047401

## Files Changed

- model.py: modified (added=14, deleted=5, delta=9)
- outputs/metrics.json: modified (added=2385, deleted=593, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -66,8 +66,7 @@
         weights = np.array(abs_deviations) + 1e-6
         weights = weights / weights.sum()  # Normalize
         
-        # Sample from history with replacement (we'll map to available candidates)
-        # We use the indices of history entries to get the gene names
+        # Sample candidate indices from history with replacement, weighted by score extremity
         exploit_indices = np.random.choice(len(history), size=min(exploit_count * 3, len(history)), replace=True, p=weights)
         
         # Convert to actual selected indices from available pool
@@ -76,9 +75,19 @@
         for idx in exploit_indices:
             if len(exploit_set) >= exploit_count:
                 break
-            # Add random available candidate (simulating exploration around high-score regions)
-            if available:
-                exploit_set.add(rng.choice(available))
+            # Add the historically high-value candidate if still available
+            hist_idx = history[idx]['candidate_index']
+            if hist_idx in available:
+                exploit_set.add(hist_idx)
+        
+        # If we don't have enough from direct hits, supplement with candidates that have similar extreme scores
+        if len(exploit_set) < exploit_count:
+            # Sort available candidates by how extreme their scores would be
+            # We don't know actual scores, so we'll prioritize based on the distribution we've seen
+            # Use the weighted sampling to bias toward regions of the search space with extreme scores
+            remaining_needed = exploit_count - len(exploit_set)
+            supplemental = rng.sample(available, min(remaining_needed, len(available)))
+            exploit_set.update(supplemental)
         
         selected.extend(list(exploit_set))
         available = [i for i in available if i not in selected]

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
+      "delta_hits": 4,
+      "total_queries": 384,
+      "total_hits": 19,
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
+          19
         ]
       },
-      "auc": 1472.0,
-      "auc_normalized": 0.006222943722943723,
-      "ncg": 0.23066881214300558,
+      "auc": 2176.0,
+      "auc_normalized": 0.006132756132756133,
+      "ncg": 0.25412715881821035,
       "round_details": [
         {
-          "round": 1,
+          "round": 2,
           "selected_count": 128,
-          "hits": 7,
-          "cumulative_hits": 15,
-          "precision_at_batch": 0.0546875,
+          "hits": 4,
+          "cumulative_hits": 19,
+          "precision_at_batch": 0.03125,
           "selected": [
-            "PRKAR2B",
-            "DHX33",
-            "TUSC3",
-            "CTDSP2",
-            "GMNC",
-            "DHX58",
-            "CLPP",
-            "WDR12",
-            "PLEKHB1",
-            "CAPN12",
-            "ALG14",
-            "TNS1",
-            "MTMR14",
-            "TOB1",
-            "DLGAP4",
-            "UAP1L1",
-            "DLX3",
-            "BRD9",
-            "MTUS1",
-            "ABHD14B",
-            "CDKL2",
-            "CNGA1",
-            "DNA2",
-            "CNNM4",
-            "SPATA31A7",
-            "BTBD16",
-            "AMPD3",
-            "PRRC2A",
-            "ZNF341",
-            "ENHO",
-            "OR51B6",
-            "SLC37A4",
-            "LY6K",
-            "DNAJC25",
-            "WNT6",
-            "PRSS56",
-            "CYP26A1",
-            "PNPO",
-            "FAM98C",
-            "GABPB2",
-            "OR5A1",
-            "SETX",
-            "CEP295NL",
-            "RC3H1",
-            "ATP5J2-PTCD1",
-            "EPT1",
-            "MLNR",
-            "ATP6V1B1",
-            "YIPF5",
-            "SRC",
-            "TBC1D10B",
-            "CCDC66",
-            "MAN1A1",
-            "CGRRF1",
-            "SLCO4C1",
-            "ZNF587B",
-            "NRN1L",
-            "CPQ",
-            "DDC",
-            "USP45",
-            "TRPT1",
-            "B4GALNT1",
-            "FEV",
-            "LMAN2L",
-            "C7orf57",
-            "GFM1",
-            "PPP1R27",
-            "SAP130",
-            "MARS",
-            "FGF7",
-            "PAK4",
-            "STIM1",
-            "CRYBA1",
-            "NDUFB8",
-            "PRADC1",
-            "SLC16A11",
-            "FAM122B",
-            "TMPO",
-            "CSNK2A3",
-            "CACNA2D1",
-            "FAM134C",
-            "CACNB2",
-            "RAB5A",
-            "CACNG5",
-            "CD99L2",
-            "TNFAIP3",
-            "SLC22A3",
-            "SLC22A4",
-            "GLTSCR1L",
-            "SRRM1",
-            "PCDHA9",
-            "RABL3",
-            "CHMP1B",
-            "ASB2",
-            "CLIP2",
-            "HIST1H4I",
-            "RPL19",
-            "GRIPAP1",
-            "RORA",
-            "LOX",
-            "RSC1A1",
-            "OR2G6",
-            "RICTOR",
-            "PFDN5",
-            "C12orf49",
-            "GNAQ",
-            "ZFC3H1",
-            "GATA6",
-            "GOLPH3L",
-            "BZW2",
-            "KCNH5",
-            "MYT1",
-            "IL22RA2",
-            "PDZD9",
-            "GOLT1A",
-            "IDI1",
-            "RAB25",
-            "RASSF3",
-            "INSL5",
-            "CACNA1H",
-            "ST3GAL5",
-            "TRIM39-RPP21",
-            "CACYBP",
-            "CNP",
-            "ARAP1",
-            "AOX1",
-            "ZNF436",
-            "TXNL4A"
+            "PCDH19",
+            "CTBS",
+            "RALA",
+            "MEGF11",
+            "ZNF208",
+            "MTHFR",
+            "PCDHGA7",
+            "CAPN3",
+            "BPIFB2",
+            "KRTAP4-5",
+            "SLC27A4",
+            "CMTR2",
+            "PLK4",
+            "UBC",
+            "KCNJ16",
+            "ZNF280A",
+            "OR1M1",
+            "BRS3",
+            "FAM25G",
+            "FAM47E",
+            "CNPY3",
+            "ZNF345",
+            "CYBA",
+            "PNLIP",
+            "ATAD2",
+            "GPCPD1",
+            "SLC35F6",
+            "RPL4",
+            "ENO1",
+            "CYP19A1",
+            "RPP30",
+            "MICU1",
+            "CYP27C1",
+            "SLC39A8",
+            "UCN3",
+            "OR52N1",
+            "FAM92B",
+            "ACSBG2",
+            "PDZD3",
+            "MIR218-1",
+            "TMED4",
+            "GPR31",
+            "ACTRT1",
+            "POLR3F",
+            "ATP5L2",
+            "SPTB",
+            "PEX3",
+            "DPP3",
+            "NPTN",
+            "GAMT",
+            "INCA1",
+            "CORO7-PAM16",
+            "RTFDC1",
+            "MAN2A2",
+            "INPP4A",
+            "CCDC77",
+            "ADAT2",
+            "TBCCD1",
+            "PTK7",
+            "SRSF5",
+            "DCP2",
+            "ADCY9",
+            "GCC1",
+            "INTS7",
+            "IPO9",
+            "PTPRM",
+            "GDF3",
+            "MAPK3",
+            "NCK1",
+            "VAPB",
+            "TDGF1",
+            "CCT7",
+            "LOC100288336",
+            "FABP12",
+            "MB",
+            "BCCIP",
+            "MRPL43",
+            "BCL10",
+            "MRPL48",
+            "CD226",
+            "C9orf85",
+            "ARHGEF11",
+            "TEX35",
+            "AK2",
+            "HAS3",
+            "DHFR",
+            "TGFB1I1",
+            "VTA1",
+            "PRKACG",
+            "GRM3",
+            "CADM4",
+            "MGAT3",
+            "TMEM161A",
+            "LRRIQ4",
+            "CAV3",
+            "UGT3A2",
+            "OSTM1",
+            "ZNF630",
+            "TMEM62",
+            "CBWD3",
+            "MOCOS",
+            "TNFSF18",
+            "NARS",
+            "RPIA",
+            "RPRML",
+            "NDE1",
+            "ZNF675",
+            "SPINT2",
+            "CCRN4L",
+            "NUAK1",
+            "LEP",
+            "DUPD1",
+            "DUSP28",
+            "DUSP4",
+            "CD300LD",
+            "SNAI1",
+            "RLBP1",
+            "PGD",
+            "SNX16",
+            "CFD",
+            "MCM3",
+            "DYX1C1",
+            "MFGE8",
+            "ZDHHC7",
+            "TSTD2",
+            "PPIG",
+            "KRIT1",
+            "ASXL1"
           ],
           "selected_scores": [
-            -2.180935028,
-            -0.541433907,
-            -1.477456704,
-            -0.972576826,
-            -0.657510787,
-            -0.41948254799999996,
-            -0.754310446,
-            -0.489996344,
-            -0.42420400700000005,
-            -1.342826074,
-            -2.68875708,
-            -0.330736545,
-            -0.676362227,
-            -0.04263311400000001,
-            -1.46070239,
-            -1.242589671,
-            -0.5142020860000001,
-            -0.48776693600000004,
-            -2.095547005,
-            -0.6283653889999999,
-            -0.798956039,
-            -0.955465346,
-            -0.939162108,
-            -1.958794925,
-            -1.4418498690000001,
-            -0.46107903899999997,
-            -1.560177346,
-            -1.7020696880000001,
-            -0.747779243,
-            -1.741433183,
-            -0.573881217,
-            -0.488998694,
-            -1.133163553,
-            -0.144876628,
-            -1.671571265,
-            -0.32846977899999996,
-            -1.181122722,
-            -0.625406357,
-            -0.007484081,
-            -0.753812977,
-            -1.315155034,
-            -0.532716148,
-            -0.48691684399999996,
-            -0.284626373,
-            -0.037490411,
-            -0.6679974129999999,
-            -0.747039243,
-            -0.201361404,
-            -0.665553626,
-            -0.18767251100000001,
-            -1.332644192,
-            -1.953629576,
-            -0.538292791,
-            -0.522701819,
-            -0.516317234,
-            -0.38926068399999997,
-            -0.603685331,
-            -0.21542853399999998,
-            -0.929506473,
-            -0.744610965,
-            -1.36667693,
-            -0.646906026,
-            -0.5020772410000001,
-            -0.289915381,
-            -2.4030170280000003,
-            -0.751344198,
-            -0.7634699640000001,
-            -1.7633453890000002,
-            -1.7221653730000002,
-            -0.634709573,
-            -1.8027060209999999,
-            -0.872834543,
-            -0.268420642,
-            -0.38708333899999997,
-            -0.400385782,
-            -0.330831854,
-            -0.624585328,
-            -0.380735899,
-            -0.424770145,
-            -0.841312252,
-            -2.578453197,
-            -0.929824685,
-            -0.816099185,
-            -0.554727847,
-            -0.8015028940000001,
-            -0.24478269600000002,
-            -0.693411715,
-            -0.568934891,
-            -0.532196444,
-            -3.165764662,
-            -0.737346519,
-            -0.487591028,
-            -0.662557456,
-            -1.043257783,
-            -3.014153447,
-            -0.634835065,
-            -0.9929364490000001,
-            -0.840400003,
-            -0.276486613,
-            -0.747411045,
-            -0.7668970690000001,
-            -0.942324445,
-            -0.13513425099999998,
-            -0.210148079,
-            -0.29762524,
-            -0.922627502,
-            -0.754154453,
-            -0.231010954,
-            -0.795542715,
-            -0.537110596,
-            -0.556996841,
-            -2.28309572,
-            -0.644110106,
-            -0.197176928,
-            -1.505077536,
-            -0.46914006399999997,
-            -0.567556108,
-            -0.42286704399999997,
-            -1.002172001,
-            -0.37474579700000005,
-            -0.519405744,
-            -0.413608109,
-            -0.93479915,
-            -0.193812845,
-            -0.7953905440000001,
-            -0.330226245,
-            -0.682790254,
-            -4.592253136
+            -0.17986812300000002,
+            -0.93184741,
+            -0.110080666,
+            -1.2621971570000001,
+            -1.4629832409999999,
+            -0.53056721,
+            -1.0357653359999999,
+            -1.516184917,
+            -2.4363128119999997,
+            -0.33412183100000004,
+            -0.909587081,
+            -0.867622597,
+            -0.649978527,
+            -1.242476262,
+            -1.535717328,
+            -0.7558665640000001,
+            -0.795292752,
+            -0.87202951,
+            -2.256070067,
+            -1.432234274,
+            -0.22900884300000002,
+            -0.7923046420000001,
+            -1.995410484,
+            -0.199076256,
+            -0.534442847,
+            -1.721282059,
+            -1.467071482,
+            -1.258452004,
+            -0.10322920699999999,
+            -0.9652608109999999,
+            -0.7923896229999999,
+            -0.709519401,
+            -0.307623705,
+            -0.134866984,
+            -2.0068613999999996,
+            -0.531539028,
+            -1.174618668,
+            -0.48418083700000003,
+            -0.655837214,
+            -0.527375421,
+            -0.557226137,
+            -0.692123335,
+            -0.982993062,
+            -1.553605335,
+            -0.9284767629999999,
+            -3.8845286530000003,
+            -0.5142025179999999,
+            -0.8456294670000001,
+            -0.605387434,
+            -0.084168268,
+            -1.809067376,
+            -0.47678603700000005,
+            -1.560368985,
+            -0.7152809309999999,
+            -0.718339979,
+            -1.112939553,
+            -0.181357057,
+            -0.476479091,
+            -0.381601255,
+            -0.642006444,
+            -1.34009841,
+            -0.494880649,
+            -1.429033762,
+            -1.232835635,
+            -0.26407106399999997,
+            -0.41914722200000004,
+            -0.49975885200000003,
+            -1.175905668,
+            -1.076478817,
+            -1.2703910729999999,
+            -0.674693352,
+            -0.704492129,
+            -1.12702237,
+            -0.672295058,
+            -0.727664667,
+            -1.442685503,
+            -0.815280817,
+            -0.553760464,
+            -0.373296909,
+            -0.191011193,
+            -0.9804685870000001,
+            -0.657764427,
+            -1.061614066,
+            -0.43550246600000003,
+            -0.366737059,
+            -0.757486294,
+            -0.040351722,
+            -1.3761129980000002,
+            -1.236471839,
+            -0.352056585,
+            -0.66884535,
+            -0.671983824,
+            -2.472286256,
+            -0.26448087600000003,
+            -1.242797965,
+            -1.61152489,
+            -0.430547529,
+            -0.665419244,
+            -0.978275274,
+            -0.71276899,
+            -0.63995502,
+            -0.330687015,
+            -1.347113393,
+            -0.196614078,
+            -0.7978009709999999,
+            -1.70578438,
+            -0.47199178,
+            -0.0279334,
+            -1.149630254,
+            -0.472024826,
+            -1.021180824,
+            -1.021444857,
+            -0.212464882,
+            -2.4841461369999998,
+            -0.854753243,
+            -1.0884399340000002,
+            -1.160592356,
+            -2.3963191669999997,
+            -0.251794205,
+            -0.799418519,
+            -0.6152584329999999,
+            -1.117229415,
+            -0.667099899,
+            -1.3195440059999999,
+            -2.175362109,
+            -0.39313499,
+            -0.105699421,
+            -1.6404002359999998
           ],
           "selected_hits": [
             0,
@@ -311,9 +311,45 @@
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
             1,
             0,
             0,
+            0,
             1,
             0,
             0,
@@ -339,12 +375,39 @@
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
+            0,
             1,
             0,
             0,
@@ -365,70 +428,7 @@
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
-            1,
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
-            1
+            0
           ]
         }
       ],
@@ -1334,896 +1334,1792 @@
           "gene": "PRKAR2B",
           "score": -2.180935028,
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
           "candidate_index": 16907,
           "gene": "TUSC3",
           "score": -1.477456704,
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
           "candidate_index": 6158,
           "gene": "GMNC",
           "score": -0.657510787,
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
           "candidate_index": 3105,
           "gene": "CLPP",
           "score": -0.754310446,
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
           "candidate_index": 11820,
           "gene": "PLEKHB1",
           "score": -0.42420400700000005,
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
           "candidate_index": 561,
           "gene": "ALG14",
           "score": -2.68875708,
           "hit": 1,
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
           "candidate_index": 9781,
           "gene": "MTMR14",
           "score": -0.676362227,
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
           "candidate_index": 4160,
           "gene": "DLGAP4",
           "score": -1.46070239,
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
           "candidate_index": 4170,
           "gene": "DLX3",
           "score": -0.5142020860000001,
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
           "candidate_index": 9809,
           "gene": "MTUS1",
           "score": -2.095547005,
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
           "candidate_index": 2644,
           "gene": "CDKL2",
           "score": -0.798956039,
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
           "candidate_index": 4197,
           "gene": "DNA2",
           "score": -0.939162108,
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
           "candidate_index": 14958,
           "gene": "SPATA31A7",
           "score": -1.4418498690000001,
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
           "candidate_index": 630,
           "gene": "AMPD3",
           "score": -1.560177346,
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
           "candidate_index": 18046,
           "gene": "ZNF341",
           "score": -0.747779243,
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
           "candidate_index": 10899,
           "gene": "OR51B6",
           "score": -0.573881217,
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
           "candidate_index": 8855,
           "gene": "LY6K",
           "score": -1.133163553,
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
           "candidate_index": 17561,
           "gene": "WNT6",
           "score": -1.671571265,
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
           "candidate_index": 3741,
           "gene": "CYP26A1",
           "score": -1.181122722,
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
           "candidate_index": 5303,
           "gene": "FAM98C",
           "score": -0.007484081,
           "hit": 1,
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
           "candidate_index": 10935,
           "gene": "OR5A1",
           "score": -1.315155034,
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
           "candidate_index": 2758,
           "gene": "CEP295NL",
           "score": -0.48691684399999996,
           "hit": 0,
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
           "candidate_index": 9448,
           "gene": "MLNR",
           "score": -0.747039243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1271,
           "gene": "ATP6V1B1",
           "score": -0.201361404,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17657,
           "gene": "YIPF5",
           "score": -0.665553626,
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
           "candidate_index": 15613,
           "gene": "TBC1D10B",
           "score": -1.332644192,
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
           "candidate_index": 8980,
           "gene": "MAN1A1",
           "score": -0.538292791,
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
           "candidate_index": 14623,
           "gene": "SLCO4C1",
           "score": -0.516317234,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18211,
           "gene": "ZNF587B",
           "score": -0.38926068399999997,
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
           "candidate_index": 3402,
           "gene": "CPQ",
           "score": -0.21542853399999998,
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
           "candidate_index": 17229,
           "gene": "USP45",
           "score": -0.744610965,
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
           "candidate_index": 1362,
           "gene": "B4GALNT1",
           "score": -0.646906026,
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
           "candidate_index": 8548,
           "gene": "LMAN2L",
           "score": -0.289915381,
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
           "candidate_index": 6001,
           "gene": "GFM1",
           "score": -0.751344198,
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
           "candidate_index": 13695,
           "gene": "SAP130",
           "score": -1.7633453890000002,
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
           "candidate_index": 5508,
           "gene": "FGF7",
           "score": -0.634709573,
           "hit": 0,
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
           "candidate_index": 15267,
           "gene": "STIM1",
           "score": -0.872834543,
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
           "candidate_index": 10153,
           "gene": "NDUFB8",
           "score": -0.38708333899999997,
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
           "candidate_index": 14273,
           "gene": "SLC16A11",
           "score": -0.330831854,
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
           "candidate_index": 16330,
           "gene": "TMPO",
           "score": -0.380735899,
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
           "candidate_index": 2012,
           "gene": "CACNA2D1",
           "score": -0.841312252,
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
           "candidate_index": 2017,
           "gene": "CACNB2",
           "score": -0.929824685,
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
           "candidate_index": 2024,
           "gene": "CACNG5",
           "score": -0.554727847,
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
           "candidate_index": 16366,
           "gene": "TNFAIP3",
           "score": -0.24478269600000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14326,
           "gene": "SLC22A3",
           "score": -0.693411715,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14328,
           "gene": "SLC22A4",
           "score": -0.568934891,
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
           "candidate_index": 15133,
           "gene": "SRRM1",
           "score": -3.165764662,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11281,
           "gene": "PCDHA9",
           "score": -0.737346519,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12795,
           "gene": "RABL3",
           "score": -0.487591028,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2892,
           "gene": "CHMP1B",
           "score": -0.662557456,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1105,
           "gene": "ASB2",
           "score": -1.043257783,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3085,
           "gene": "CLIP2",
           "score": -3.014153447,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6842,
           "gene": "HIST1H4I",
           "score": -0.634835065,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13423,
           "gene": "RPL19",
           "score": -0.9929364490000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6444,
           "gene": "GRIPAP1",
           "score": -0.840400003,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13384,
           "gene": "RORA",
           "score": -0.276486613,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8639,
           "gene": "LOX",
           "score": -0.747411045,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13556,
           "gene": "RSC1A1",
           "score": -0.7668970690000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10859,
           "gene": "OR2G6",
           "score": -0.942324445,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13202,
           "gene": "RICTOR",
           "score": -0.13513425099999998,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11510,
           "gene": "PFDN5",
           "score": -0.210148079,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1717,
           "gene": "C12orf49",
           "score": -0.29762524,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6175,
           "gene": "GNAQ",
           "score": -0.922627502,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17823,
           "gene": "ZFC3H1",
           "score": -0.754154453,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5911,
           "gene": "GATA6",
           "score": -0.231010954,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6239,
           "gene": "GOLPH3L",
           "score": -0.795542715,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1693,
           "gene": "BZW2",
           "score": -0.537110596,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7750,
           "gene": "KCNH5",
           "score": -0.556996841,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9955,
           "gene": "MYT1",
           "score": -2.28309572,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7370,
           "gene": "IL22RA2",
           "score": -0.644110106,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11458,
           "gene": "PDZD9",
           "score": -0.197176928,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6240,
           "gene": "GOLT1A",
           "score": -1.505077536,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7190,
           "gene": "IDI1",
           "score": -0.46914006399999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12734,
           "gene": "RAB25",
           "score": -0.567556108,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12911,
           "gene": "RASSF3",
           "score": -0.42286704399999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7466,
           "gene": "INSL5",
           "score": -1.002172001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2009,
           "gene": "CACNA1H",
           "score": -0.37474579700000005,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15203,
           "gene": "ST3GAL5",
           "score": -0.519405744,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16625,
           "gene": "TRIM39-RPP21",
           "score": -0.413608109,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2030,
           "gene": "CACYBP",
           "score": -0.93479915,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3189,
           "gene": "CNP",
           "score": -0.193812845,
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
           "candidate_index": 18097,
           "gene": "ZNF436",
           "score": -0.682790254,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16937,
           "gene": "TXNL4A",
           "score": -4.592253136,
           "hit": 1,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 11264,
+          "gene": "PCDH19",
+          "score": -0.17986812300000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3589,
+          "gene": "CTBS",
+          "score": -0.93184741,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12832,
+          "gene": "RALA",
+          "score": -0.110080666,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9251,
+          "gene": "MEGF11",
+          "score": -1.2621971570000001,
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
+          "candidate_index": 9770,
+          "gene": "MTHFR",
+          "score": -0.53056721,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11309,
+          "gene": "PCDHGA7",
+          "score": -1.0357653359999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2099,
+          "gene": "CAPN3",
+          "score": -1.516184917,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1592,
+          "gene": "BPIFB2",
+          "score": -2.4363128119999997,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8251,
+          "gene": "KRTAP4-5",
+          "score": -0.33412183100000004,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14404,
+          "gene": "SLC27A4",
+          "score": -0.909587081,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3150,
+          "gene": "CMTR2",
+          "score": -0.867622597,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11857,
+          "gene": "PLK4",
+          "score": -0.649978527,
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
+          "candidate_index": 7765,
+          "gene": "KCNJ16",
+          "score": -1.535717328,
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
+          "candidate_index": 10841,
+          "gene": "OR1M1",
+          "score": -0.795292752,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1633,
+          "gene": "BRS3",
+          "score": -0.87202951,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5219,
+          "gene": "FAM25G",
+          "score": -2.256070067,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5239,
+          "gene": "FAM47E",
+          "score": -1.432234274,
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
+          "candidate_index": 18048,
+          "gene": "ZNF345",
+          "score": -0.7923046420000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3718,
+          "gene": "CYBA",
+          "score": -1.995410484,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11911,
+          "gene": "PNLIP",
+          "score": -0.199076256,
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
+          "candidate_index": 6280,
+          "gene": "GPCPD1",
+          "score": -1.721282059,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14470,
+          "gene": "SLC35F6",
+          "score": -1.467071482,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13451,
+          "gene": "RPL4",
+          "score": -1.258452004,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4754,
+          "gene": "ENO1",
+          "score": -0.10322920699999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3734,
+          "gene": "CYP19A1",
+          "score": -0.9652608109999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13468,
+          "gene": "RPP30",
+          "score": -0.7923896229999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9374,
+          "gene": "MICU1",
+          "score": -0.709519401,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3746,
+          "gene": "CYP27C1",
+          "score": -0.307623705,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14507,
+          "gene": "SLC39A8",
+          "score": -0.134866984,
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
+          "candidate_index": 10926,
+          "gene": "OR52N1",
+          "score": -0.531539028,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5298,
+          "gene": "FAM92B",
+          "score": -1.174618668,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 178,
+          "gene": "ACSBG2",
+          "score": -0.48418083700000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11454,
+          "gene": "PDZD3",
+          "score": -0.655837214,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9407,
+          "gene": "MIR218-1",
+          "score": -0.527375421,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16064,
+          "gene": "TMED4",
+          "score": -0.557226137,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6346,
+          "gene": "GPR31",
+          "score": -0.692123335,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 223,
+          "gene": "ACTRT1",
+          "score": -0.982993062,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12000,
+          "gene": "POLR3F",
+          "score": -1.553605335,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1254,
+          "gene": "ATP5L2",
+          "score": -0.9284767629999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15080,
+          "gene": "SPTB",
+          "score": -3.8845286530000003,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 11499,
+          "gene": "PEX3",
+          "score": -0.5142025179999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4335,
+          "gene": "DPP3",
+          "score": -0.8456294670000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10488,
+          "gene": "NPTN",
+          "score": -0.605387434,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5882,
+          "gene": "GAMT",
+          "score": -0.084168268,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 7428,
+          "gene": "INCA1",
+          "score": -1.809067376,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3337,
+          "gene": "CORO7-PAM16",
+          "score": -0.47678603700000005,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13583,
+          "gene": "RTFDC1",
+          "score": -1.560368985,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8985,
+          "gene": "MAN2A2",
+          "score": -0.7152809309999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7449,
+          "gene": "INPP4A",
+          "score": -0.718339979,
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
+          "candidate_index": 291,
+          "gene": "ADAT2",
+          "score": -0.181357057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15652,
+          "gene": "TBCCD1",
+          "score": -0.476479091,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12584,
+          "gene": "PTK7",
+          "score": -0.381601255,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15146,
+          "gene": "SRSF5",
+          "score": -0.642006444,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3888,
+          "gene": "DCP2",
+          "score": -1.34009841,
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
+          "candidate_index": 5940,
+          "gene": "GCC1",
+          "score": -1.429033762,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7480,
+          "gene": "INTS7",
+          "score": -1.232835635,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7496,
+          "gene": "IPO9",
+          "score": -0.26407106399999997,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12622,
+          "gene": "PTPRM",
+          "score": -0.41914722200000004,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5974,
+          "gene": "GDF3",
+          "score": -0.49975885200000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9053,
+          "gene": "MAPK3",
+          "score": -1.175905668,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10078,
+          "gene": "NCK1",
+          "score": -1.076478817,
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
+          "candidate_index": 15753,
+          "gene": "TDGF1",
+          "score": -0.674693352,
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
+          "candidate_index": 8592,
+          "gene": "LOC100288336",
+          "score": -1.12702237,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5015,
+          "gene": "FABP12",
+          "score": -0.672295058,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9118,
+          "gene": "MB",
+          "score": -0.727664667,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1441,
+          "gene": "BCCIP",
+          "score": -1.442685503,
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
+          "candidate_index": 1447,
+          "gene": "BCL10",
+          "score": -0.553760464,
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
+          "candidate_index": 2476,
+          "gene": "CD226",
+          "score": -0.191011193,
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
+          "candidate_index": 963,
+          "gene": "ARHGEF11",
+          "score": -0.657764427,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15824,
+          "gene": "TEX35",
+          "score": -1.061614066,
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
+          "candidate_index": 6626,
+          "gene": "HAS3",
+          "score": -0.366737059,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4080,
+          "gene": "DHFR",
+          "score": -0.757486294,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15862,
+          "gene": "TGFB1I1",
+          "score": -0.040351722,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 17398,
+          "gene": "VTA1",
+          "score": -1.3761129980000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12284,
+          "gene": "PRKACG",
+          "score": -1.236471839,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6452,
+          "gene": "GRM3",
+          "score": -0.352056585,
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
+          "candidate_index": 9346,
+          "gene": "MGAT3",
+          "score": -0.671983824,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16136,
+          "gene": "TMEM161A",
+          "score": -2.472286256,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8783,
+          "gene": "LRRIQ4",
+          "score": -0.26448087600000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2173,
+          "gene": "CAV3",
+          "score": -1.242797965,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17104,
+          "gene": "UGT3A2",
+          "score": -1.61152489,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11026,
+          "gene": "OSTM1",
+          "score": -0.430547529,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18244,
+          "gene": "ZNF630",
+          "score": -0.665419244,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16285,
+          "gene": "TMEM62",
+          "score": -0.978275274,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2191,
+          "gene": "CBWD3",
+          "score": -0.71276899,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9506,
+          "gene": "MOCOS",
+          "score": -0.63995502,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16402,
+          "gene": "TNFSF18",
+          "score": -0.330687015,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10030,
+          "gene": "NARS",
+          "score": -1.347113393,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13409,
+          "gene": "RPIA",
+          "score": -0.196614078,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13475,
+          "gene": "RPRML",
+          "score": -0.7978009709999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10105,
+          "gene": "NDE1",
+          "score": -1.70578438,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18270,
+          "gene": "ZNF675",
+          "score": -0.47199178,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15027,
+          "gene": "SPINT2",
+          "score": -0.0279334,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 2436,
+          "gene": "CCRN4L",
+          "score": -1.149630254,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10610,
+          "gene": "NUAK1",
+          "score": -0.472024826,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8432,
+          "gene": "LEP",
+          "score": -1.021180824,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4416,
+          "gene": "DUPD1",
+          "score": -1.021444857,
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
+          "candidate_index": 4439,
+          "gene": "DUSP4",
+          "score": -2.4841461369999998,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2490,
+          "gene": "CD300LD",
+          "score": -0.854753243,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14757,
+          "gene": "SNAI1",
+          "score": -1.0884399340000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13237,
+          "gene": "RLBP1",
+          "score": -1.160592356,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11539,
+          "gene": "PGD",
+          "score": -2.3963191669999997,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14817,
+          "gene": "SNX16",
+          "score": -0.251794205,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2818,
+          "gene": "CFD",
+          "score": -0.799418519,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9170,
+          "gene": "MCM3",
+          "score": -0.6152584329999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4475,
+          "gene": "DYX1C1",
+          "score": -1.117229415,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9320,
+          "gene": "MFGE8",
+          "score": -0.667099899,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17809,
+          "gene": "ZDHHC7",
+          "score": -1.3195440059999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16802,
+          "gene": "TSTD2",
+          "score": -2.175362109,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12100,
+          "gene": "PPIG",
+          "score": -0.39313499,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8134,
+          "gene": "KRIT1",
+          "score": -0.105699421,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1155,
+          "gene": "ASXL1",
+          "score": -1.6404002359999998,
+          "hit": 0,
+          "round": 2
         }
       ],
       "queried_history": [
@@ -3128,896 +4024,1792 @@
           "gene": "PRKAR2B",
           "score": -2.180935028,
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
           "candidate_index": 16907,
           "gene": "TUSC3",
           "score": -1.477456704,
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
           "candidate_index": 6158,
           "gene": "GMNC",
           "score": -0.657510787,
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
           "candidate_index": 3105,
           "gene": "CLPP",
           "score": -0.754310446,
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
           "candidate_index": 11820,
           "gene": "PLEKHB1",
           "score": -0.42420400700000005,
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
           "candidate_index": 561,
           "gene": "ALG14",
           "score": -2.68875708,
           "hit": 1,
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
           "candidate_index": 9781,
           "gene": "MTMR14",
           "score": -0.676362227,
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
           "candidate_index": 4160,
           "gene": "DLGAP4",
           "score": -1.46070239,
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
           "candidate_index": 4170,
           "gene": "DLX3",
           "score": -0.5142020860000001,
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
           "candidate_index": 9809,
           "gene": "MTUS1",
           "score": -2.095547005,
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
           "candidate_index": 2644,
           "gene": "CDKL2",
           "score": -0.798956039,
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
           "candidate_index": 4197,
           "gene": "DNA2",
           "score": -0.939162108,
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
           "candidate_index": 14958,
           "gene": "SPATA31A7",
           "score": -1.4418498690000001,
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
           "candidate_index": 630,
           "gene": "AMPD3",
           "score": -1.560177346,
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
           "candidate_index": 18046,
           "gene": "ZNF341",
           "score": -0.747779243,
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
           "candidate_index": 10899,
           "gene": "OR51B6",
           "score": -0.573881217,
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
           "candidate_index": 8855,
           "gene": "LY6K",
           "score": -1.133163553,
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
           "candidate_index": 17561,
           "gene": "WNT6",
           "score": -1.671571265,
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
           "candidate_index": 3741,
           "gene": "CYP26A1",
           "score": -1.181122722,
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
           "candidate_index": 5303,
           "gene": "FAM98C",
           "score": -0.007484081,
           "hit": 1,
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
           "candidate_index": 10935,
           "gene": "OR5A1",
           "score": -1.315155034,
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
           "candidate_index": 2758,
           "gene": "CEP295NL",
           "score": -0.48691684399999996,
           "hit": 0,
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
           "candidate_index": 9448,
           "gene": "MLNR",
           "score": -0.747039243,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1271,
           "gene": "ATP6V1B1",
           "score": -0.201361404,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17657,
           "gene": "YIPF5",
           "score": -0.665553626,
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
           "candidate_index": 15613,
           "gene": "TBC1D10B",
           "score": -1.332644192,
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
           "candidate_index": 8980,
           "gene": "MAN1A1",
           "score": -0.538292791,
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
           "candidate_index": 14623,
           "gene": "SLCO4C1",
           "score": -0.516317234,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 18211,
           "gene": "ZNF587B",
           "score": -0.38926068399999997,
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
           "candidate_index": 3402,
           "gene": "CPQ",
           "score": -0.21542853399999998,
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
           "candidate_index": 17229,
           "gene": "USP45",
           "score": -0.744610965,
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
           "candidate_index": 1362,
           "gene": "B4GALNT1",
           "score": -0.646906026,
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
           "candidate_index": 8548,
           "gene": "LMAN2L",
           "score": -0.289915381,
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
           "candidate_index": 6001,
           "gene": "GFM1",
           "score": -0.751344198,
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
           "candidate_index": 13695,
           "gene": "SAP130",
           "score": -1.7633453890000002,
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
           "candidate_index": 5508,
           "gene": "FGF7",
           "score": -0.634709573,
           "hit": 0,
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
           "candidate_index": 15267,
           "gene": "STIM1",
           "score": -0.872834543,
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
           "candidate_index": 10153,
           "gene": "NDUFB8",
           "score": -0.38708333899999997,
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
           "candidate_index": 14273,
           "gene": "SLC16A11",
           "score": -0.330831854,
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
           "candidate_index": 16330,
           "gene": "TMPO",
           "score": -0.380735899,
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
           "candidate_index": 2012,
           "gene": "CACNA2D1",
           "score": -0.841312252,
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
           "candidate_index": 2017,
           "gene": "CACNB2",
           "score": -0.929824685,
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
           "candidate_index": 2024,
           "gene": "CACNG5",
           "score": -0.554727847,
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
           "candidate_index": 16366,
           "gene": "TNFAIP3",
           "score": -0.24478269600000002,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14326,
           "gene": "SLC22A3",
           "score": -0.693411715,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 14328,
           "gene": "SLC22A4",
           "score": -0.568934891,
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
           "candidate_index": 15133,
           "gene": "SRRM1",
           "score": -3.165764662,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11281,
           "gene": "PCDHA9",
           "score": -0.737346519,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12795,
           "gene": "RABL3",
           "score": -0.487591028,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2892,
           "gene": "CHMP1B",
           "score": -0.662557456,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1105,
           "gene": "ASB2",
           "score": -1.043257783,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3085,
           "gene": "CLIP2",
           "score": -3.014153447,
           "hit": 1,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6842,
           "gene": "HIST1H4I",
           "score": -0.634835065,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13423,
           "gene": "RPL19",
           "score": -0.9929364490000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6444,
           "gene": "GRIPAP1",
           "score": -0.840400003,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13384,
           "gene": "RORA",
           "score": -0.276486613,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 8639,
           "gene": "LOX",
           "score": -0.747411045,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13556,
           "gene": "RSC1A1",
           "score": -0.7668970690000001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 10859,
           "gene": "OR2G6",
           "score": -0.942324445,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 13202,
           "gene": "RICTOR",
           "score": -0.13513425099999998,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11510,
           "gene": "PFDN5",
           "score": -0.210148079,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1717,
           "gene": "C12orf49",
           "score": -0.29762524,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6175,
           "gene": "GNAQ",
           "score": -0.922627502,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 17823,
           "gene": "ZFC3H1",
           "score": -0.754154453,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 5911,
           "gene": "GATA6",
           "score": -0.231010954,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6239,
           "gene": "GOLPH3L",
           "score": -0.795542715,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 1693,
           "gene": "BZW2",
           "score": -0.537110596,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7750,
           "gene": "KCNH5",
           "score": -0.556996841,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 9955,
           "gene": "MYT1",
           "score": -2.28309572,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7370,
           "gene": "IL22RA2",
           "score": -0.644110106,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 11458,
           "gene": "PDZD9",
           "score": -0.197176928,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 6240,
           "gene": "GOLT1A",
           "score": -1.505077536,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7190,
           "gene": "IDI1",
           "score": -0.46914006399999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12734,
           "gene": "RAB25",
           "score": -0.567556108,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 12911,
           "gene": "RASSF3",
           "score": -0.42286704399999997,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 7466,
           "gene": "INSL5",
           "score": -1.002172001,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2009,
           "gene": "CACNA1H",
           "score": -0.37474579700000005,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 15203,
           "gene": "ST3GAL5",
           "score": -0.519405744,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16625,
           "gene": "TRIM39-RPP21",
           "score": -0.413608109,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 2030,
           "gene": "CACYBP",
           "score": -0.93479915,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 3189,
           "gene": "CNP",
           "score": -0.193812845,
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
           "candidate_index": 18097,
           "gene": "ZNF436",
           "score": -0.682790254,
           "hit": 0,
-          "round": 1
+          "round": 0
         },
         {
           "candidate_index": 16937,
           "gene": "TXNL4A",
           "score": -4.592253136,
           "hit": 1,
-          "round": 1
+          "round": 0
+        },
+        {
+          "candidate_index": 11264,
+          "gene": "PCDH19",
+          "score": -0.17986812300000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3589,
+          "gene": "CTBS",
+          "score": -0.93184741,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12832,
+          "gene": "RALA",
+          "score": -0.110080666,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9251,
+          "gene": "MEGF11",
+          "score": -1.2621971570000001,
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
+          "candidate_index": 9770,
+          "gene": "MTHFR",
+          "score": -0.53056721,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11309,
+          "gene": "PCDHGA7",
+          "score": -1.0357653359999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2099,
+          "gene": "CAPN3",
+          "score": -1.516184917,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1592,
+          "gene": "BPIFB2",
+          "score": -2.4363128119999997,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8251,
+          "gene": "KRTAP4-5",
+          "score": -0.33412183100000004,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14404,
+          "gene": "SLC27A4",
+          "score": -0.909587081,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3150,
+          "gene": "CMTR2",
+          "score": -0.867622597,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11857,
+          "gene": "PLK4",
+          "score": -0.649978527,
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
+          "candidate_index": 7765,
+          "gene": "KCNJ16",
+          "score": -1.535717328,
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
+          "candidate_index": 10841,
+          "gene": "OR1M1",
+          "score": -0.795292752,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1633,
+          "gene": "BRS3",
+          "score": -0.87202951,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5219,
+          "gene": "FAM25G",
+          "score": -2.256070067,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5239,
+          "gene": "FAM47E",
+          "score": -1.432234274,
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
+          "candidate_index": 18048,
+          "gene": "ZNF345",
+          "score": -0.7923046420000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3718,
+          "gene": "CYBA",
+          "score": -1.995410484,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11911,
+          "gene": "PNLIP",
+          "score": -0.199076256,
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
+          "candidate_index": 6280,
+          "gene": "GPCPD1",
+          "score": -1.721282059,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14470,
+          "gene": "SLC35F6",
+          "score": -1.467071482,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13451,
+          "gene": "RPL4",
+          "score": -1.258452004,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4754,
+          "gene": "ENO1",
+          "score": -0.10322920699999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3734,
+          "gene": "CYP19A1",
+          "score": -0.9652608109999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13468,
+          "gene": "RPP30",
+          "score": -0.7923896229999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9374,
+          "gene": "MICU1",
+          "score": -0.709519401,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3746,
+          "gene": "CYP27C1",
+          "score": -0.307623705,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14507,
+          "gene": "SLC39A8",
+          "score": -0.134866984,
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
+          "candidate_index": 10926,
+          "gene": "OR52N1",
+          "score": -0.531539028,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5298,
+          "gene": "FAM92B",
+          "score": -1.174618668,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 178,
+          "gene": "ACSBG2",
+          "score": -0.48418083700000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11454,
+          "gene": "PDZD3",
+          "score": -0.655837214,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9407,
+          "gene": "MIR218-1",
+          "score": -0.527375421,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16064,
+          "gene": "TMED4",
+          "score": -0.557226137,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6346,
+          "gene": "GPR31",
+          "score": -0.692123335,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 223,
+          "gene": "ACTRT1",
+          "score": -0.982993062,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12000,
+          "gene": "POLR3F",
+          "score": -1.553605335,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1254,
+          "gene": "ATP5L2",
+          "score": -0.9284767629999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15080,
+          "gene": "SPTB",
+          "score": -3.8845286530000003,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 11499,
+          "gene": "PEX3",
+          "score": -0.5142025179999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4335,
+          "gene": "DPP3",
+          "score": -0.8456294670000001,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10488,
+          "gene": "NPTN",
+          "score": -0.605387434,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5882,
+          "gene": "GAMT",
+          "score": -0.084168268,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 7428,
+          "gene": "INCA1",
+          "score": -1.809067376,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3337,
+          "gene": "CORO7-PAM16",
+          "score": -0.47678603700000005,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13583,
+          "gene": "RTFDC1",
+          "score": -1.560368985,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8985,
+          "gene": "MAN2A2",
+          "score": -0.7152809309999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7449,
+          "gene": "INPP4A",
+          "score": -0.718339979,
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
+          "candidate_index": 291,
+          "gene": "ADAT2",
+          "score": -0.181357057,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15652,
+          "gene": "TBCCD1",
+          "score": -0.476479091,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12584,
+          "gene": "PTK7",
+          "score": -0.381601255,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15146,
+          "gene": "SRSF5",
+          "score": -0.642006444,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 3888,
+          "gene": "DCP2",
+          "score": -1.34009841,
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
+          "candidate_index": 5940,
+          "gene": "GCC1",
+          "score": -1.429033762,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7480,
+          "gene": "INTS7",
+          "score": -1.232835635,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 7496,
+          "gene": "IPO9",
+          "score": -0.26407106399999997,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12622,
+          "gene": "PTPRM",
+          "score": -0.41914722200000004,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5974,
+          "gene": "GDF3",
+          "score": -0.49975885200000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9053,
+          "gene": "MAPK3",
+          "score": -1.175905668,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10078,
+          "gene": "NCK1",
+          "score": -1.076478817,
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
+          "candidate_index": 15753,
+          "gene": "TDGF1",
+          "score": -0.674693352,
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
+          "candidate_index": 8592,
+          "gene": "LOC100288336",
+          "score": -1.12702237,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 5015,
+          "gene": "FABP12",
+          "score": -0.672295058,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9118,
+          "gene": "MB",
+          "score": -0.727664667,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1441,
+          "gene": "BCCIP",
+          "score": -1.442685503,
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
+          "candidate_index": 1447,
+          "gene": "BCL10",
+          "score": -0.553760464,
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
+          "candidate_index": 2476,
+          "gene": "CD226",
+          "score": -0.191011193,
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
+          "candidate_index": 963,
+          "gene": "ARHGEF11",
+          "score": -0.657764427,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15824,
+          "gene": "TEX35",
+          "score": -1.061614066,
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
+          "candidate_index": 6626,
+          "gene": "HAS3",
+          "score": -0.366737059,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4080,
+          "gene": "DHFR",
+          "score": -0.757486294,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15862,
+          "gene": "TGFB1I1",
+          "score": -0.040351722,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 17398,
+          "gene": "VTA1",
+          "score": -1.3761129980000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12284,
+          "gene": "PRKACG",
+          "score": -1.236471839,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 6452,
+          "gene": "GRM3",
+          "score": -0.352056585,
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
+          "candidate_index": 9346,
+          "gene": "MGAT3",
+          "score": -0.671983824,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16136,
+          "gene": "TMEM161A",
+          "score": -2.472286256,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8783,
+          "gene": "LRRIQ4",
+          "score": -0.26448087600000003,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2173,
+          "gene": "CAV3",
+          "score": -1.242797965,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17104,
+          "gene": "UGT3A2",
+          "score": -1.61152489,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11026,
+          "gene": "OSTM1",
+          "score": -0.430547529,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18244,
+          "gene": "ZNF630",
+          "score": -0.665419244,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16285,
+          "gene": "TMEM62",
+          "score": -0.978275274,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2191,
+          "gene": "CBWD3",
+          "score": -0.71276899,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9506,
+          "gene": "MOCOS",
+          "score": -0.63995502,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16402,
+          "gene": "TNFSF18",
+          "score": -0.330687015,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10030,
+          "gene": "NARS",
+          "score": -1.347113393,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13409,
+          "gene": "RPIA",
+          "score": -0.196614078,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13475,
+          "gene": "RPRML",
+          "score": -0.7978009709999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10105,
+          "gene": "NDE1",
+          "score": -1.70578438,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 18270,
+          "gene": "ZNF675",
+          "score": -0.47199178,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 15027,
+          "gene": "SPINT2",
+          "score": -0.0279334,
+          "hit": 1,
+          "round": 2
+        },
+        {
+          "candidate_index": 2436,
+          "gene": "CCRN4L",
+          "score": -1.149630254,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 10610,
+          "gene": "NUAK1",
+          "score": -0.472024826,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8432,
+          "gene": "LEP",
+          "score": -1.021180824,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4416,
+          "gene": "DUPD1",
+          "score": -1.021444857,
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
+          "candidate_index": 4439,
+          "gene": "DUSP4",
+          "score": -2.4841461369999998,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2490,
+          "gene": "CD300LD",
+          "score": -0.854753243,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14757,
+          "gene": "SNAI1",
+          "score": -1.0884399340000002,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 13237,
+          "gene": "RLBP1",
+          "score": -1.160592356,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 11539,
+          "gene": "PGD",
+          "score": -2.3963191669999997,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 14817,
+          "gene": "SNX16",
+          "score": -0.251794205,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 2818,
+          "gene": "CFD",
+          "score": -0.799418519,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9170,
+          "gene": "MCM3",
+          "score": -0.6152584329999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 4475,
+          "gene": "DYX1C1",
+          "score": -1.117229415,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 9320,
+          "gene": "MFGE8",
+          "score": -0.667099899,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 17809,
+          "gene": "ZDHHC7",
+          "score": -1.3195440059999999,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 16802,
+          "gene": "TSTD2",
+          "score": -2.175362109,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 12100,
+          "gene": "PPIG",
+          "score": -0.39313499,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 8134,
+          "gene": "KRIT1",
+          "score": -0.105699421,
+          "hit": 0,
+          "round": 2
+        },
+        {
+          "candidate_index": 1155,
+          "gene": "ASXL1",
+          "score": -1.6404002359999998,
+          "hit": 0,
+          "round": 2
         }
       ]
     }

```
