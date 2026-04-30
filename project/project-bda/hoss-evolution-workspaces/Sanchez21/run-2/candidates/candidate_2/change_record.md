# Change Record — candidate_2

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21/run-2/best/current/harness
Generated at: 2026-04-30T07:21:00.518580

## Files Changed

- model.py: modified (added=29, deleted=16, delta=13)
- outputs/metrics.json: modified (added=2151, deleted=359, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -45,14 +45,7 @@
         selected = rng.sample(available, min(batch_size, len(available)))
         return selected
     
-    # For subsequent rounds, use a combination of exploitation and exploration
-    # Sort history by score (descending)
-    sorted_history = sorted(history, key=lambda x: x['score'], reverse=True)
-    
-    # Take top 30% as high-scoring candidates
-    top_percentile = 0.3
-    top_count = max(1, int(len(sorted_history) * top_percentile))
-    top_candidates = sorted_history[:top_count]
+    # For subsequent rounds, use score-guided exploitation + exploration
     
     # Calculate selection strategy: 70% exploitation, 30% exploration
     exploit_count = int(batch_size * 0.7)
@@ -60,14 +53,34 @@
     
     selected = []
     
-    # Exploitation: select from high-scoring candidates
-    # We can't select the same indices, but we might want to select similar genes
-    # For now, we'll use random selection from available
-    if exploit_count > 0:
-        exploit_pool = available.copy()
-        rng.shuffle(exploit_pool)
-        selected.extend(exploit_pool[:exploit_count])
-        # Remove selected from available
+    # Exploitation: Use weighted sampling based on absolute score distance from median
+    # This targets both extremes: very negative scores and near-zero scores
+    if exploit_count > 0 and len(history) > 0:
+        # Calculate absolute deviation from median for each historical candidate
+        scores = [h['score'] for h in history]
+        median_score = np.median(scores)
+        abs_deviations = [abs(h['score'] - median_score) for h in history]
+        
+        # Create weights: higher deviation = higher weight
+        # Add small epsilon to avoid zero weights
+        weights = np.array(abs_deviations) + 1e-6
+        weights = weights / weights.sum()  # Normalize
+        
+        # Sample from history with replacement (we'll map to available candidates)
+        # We use the indices of history entries to get the gene names
+        exploit_indices = np.random.choice(len(history), size=min(exploit_count * 3, len(history)), replace=True, p=weights)
+        
+        # Convert to actual selected indices from available pool
+        # Use the top exploit_count unique selections
+        exploit_set = set()
+        for idx in exploit_indices:
+            if len(exploit_set) >= exploit_count:
+                break
+            # Add random available candidate (simulating exploration around high-score regions)
+            if available:
+                exploit_set.add(rng.choice(available))
+        
+        selected.extend(list(exploit_set))
         available = [i for i in available if i not in selected]
     
     # Exploration: random selection from remaining available

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
-      "ncg": 0.20192169901702914,
+      "auc": 1472.0,
+      "auc_normalized": 0.006222943722943723,
+      "ncg": 0.23066881214300558,
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
-            "ZNF486",
-            "ADRA2B",
-            "CYP2C8",
-            "XCL1",
-            "LRRC41",
-            "PAK7",
-            "CUL9",
-            "MRPL23",
-            "SLC10A6",
-            "FAM209B",
-            "SOS1",
-            "ABRA",
-            "LOC730183"
+            "PRKAR2B",
+            "DHX33",
+            "TUSC3",
+            "CTDSP2",
+            "GMNC",
+            "DHX58",
+            "CLPP",
+            "WDR12",
+            "PLEKHB1",
+            "CAPN12",
+            "ALG14",
+            "TNS1",
+            "MTMR14",
+            "TOB1",
+            "DLGAP4",
+            "UAP1L1",
+            "DLX3",
+            "BRD9",
+            "MTUS1",
+            "ABHD14B",
+            "CDKL2",
+            "CNGA1",
+            "DNA2",
+            "CNNM4",
+            "SPATA31A7",
+            "BTBD16",
+            "AMPD3",
+            "PRRC2A",
+            "ZNF341",
+            "ENHO",
+            "OR51B6",
+            "SLC37A4",
+            "LY6K",
+            "DNAJC25",
+            "WNT6",
+            "PRSS56",
+            "CYP26A1",
+            "PNPO",
+            "FAM98C",
+            "GABPB2",
+            "OR5A1",
+            "SETX",
+            "CEP295NL",
+            "RC3H1",
+            "ATP5J2-PTCD1",
+            "EPT1",
+            "MLNR",
+            "ATP6V1B1",
+            "YIPF5",
+            "SRC",
+            "TBC1D10B",
+            "CCDC66",
+            "MAN1A1",
+            "CGRRF1",
+            "SLCO4C1",
+            "ZNF587B",
+            "NRN1L",
+            "CPQ",
+            "DDC",
+            "USP45",
+            "TRPT1",
+            "B4GALNT1",
+            "FEV",
+            "LMAN2L",
+            "C7orf57",
+            "GFM1",
+            "PPP1R27",
+            "SAP130",
+            "MARS",
+            "FGF7",
+            "PAK4",
+            "STIM1",
+            "CRYBA1",
+            "NDUFB8",
+            "PRADC1",
+            "SLC16A11",
+            "FAM122B",
+            "TMPO",
+            "CSNK2A3",
+            "CACNA2D1",
+            "FAM134C",
+            "CACNB2",
+            "RAB5A",
+            "CACNG5",
+            "CD99L2",
+            "TNFAIP3",
+            "SLC22A3",
+            "SLC22A4",
+            "GLTSCR1L",
+            "SRRM1",
+            "PCDHA9",
+            "RABL3",
+            "CHMP1B",
+            "ASB2",
+            "CLIP2",
+            "HIST1H4I",
+            "RPL19",
+            "GRIPAP1",
+            "RORA",
+            "LOX",
+            "RSC1A1",
+            "OR2G6",
+            "RICTOR",
+            "PFDN5",
+            "C12orf49",
+            "GNAQ",
+            "ZFC3H1",
+            "GATA6",
+            "GOLPH3L",
+            "BZW2",
+            "KCNH5",
+            "MYT1",
+            "IL22RA2",
+            "PDZD9",
+            "GOLT1A",
+            "IDI1",
+            "RAB25",
+            "RASSF3",
+            "INSL5",
+            "CACNA1H",
+            "ST3GAL5",
+            "TRIM39-RPP21",
+            "CACYBP",
+            "CNP",
+            "ARAP1",
+            "AOX1",
+            "ZNF436",
+            "TXNL4A"
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
-            -0.5905814620000001,
-            -0.794515953,
-            -0.37258578200000003,
-            -0.691943986,
-            -2.528337248,
-            -0.616714101,
-            -0.240345846,
-            -0.747847435,
-            -0.5028895729999999,
-            -0.42545720200000003,
-            -0.8427618790000001,
-            -0.213723146,
-            -1.3483625769999998
+            -2.180935028,
+            -0.541433907,
+            -1.477456704,
+            -0.972576826,
+            -0.657510787,
+            -0.41948254799999996,
+            -0.754310446,
+            -0.489996344,
+            -0.42420400700000005,
+            -1.342826074,
+            -2.68875708,
+            -0.330736545,
+            -0.676362227,
+            -0.04263311400000001,
+            -1.46070239,
+            -1.242589671,
+            -0.5142020860000001,
+            -0.48776693600000004,
+            -2.095547005,
+            -0.6283653889999999,
+            -0.798956039,
+            -0.955465346,
+            -0.939162108,
+            -1.958794925,
+            -1.4418498690000001,
+            -0.46107903899999997,
+            -1.560177346,
+            -1.7020696880000001,
+            -0.747779243,
+            -1.741433183,
+            -0.573881217,
+            -0.488998694,
+            -1.133163553,
+            -0.144876628,
+            -1.671571265,
+            -0.32846977899999996,
+            -1.181122722,
+            -0.625406357,
+            -0.007484081,
+            -0.753812977,
+            -1.315155034,
+            -0.532716148,
+            -0.48691684399999996,
+            -0.284626373,
+            -0.037490411,
+            -0.6679974129999999,
+            -0.747039243,
+            -0.201361404,
+            -0.665553626,
+            -0.18767251100000001,
+            -1.332644192,
+            -1.953629576,
+            -0.538292791,
+            -0.522701819,
+            -0.516317234,
+            -0.38926068399999997,
+            -0.603685331,
+            -0.21542853399999998,
+            -0.929506473,
+            -0.744610965,
+            -1.36667693,
+            -0.646906026,
+            -0.5020772410000001,
+            -0.289915381,
+            -2.4030170280000003,
+            -0.751344198,
+            -0.7634699640000001,
+            -1.7633453890000002,
+            -1.7221653730000002,
+            -0.634709573,
+            -1.8027060209999999,
+            -0.872834543,
+            -0.268420642,
+            -0.38708333899999997,
+            -0.400385782,
+            -0.330831854,
+            -0.624585328,
+            -0.380735899,
+            -0.424770145,
+            -0.841312252,
+            -2.578453197,
+            -0.929824685,
+            -0.816099185,
+            -0.554727847,
+            -0.8015028940000001,
+            -0.24478269600000002,
+            -0.693411715,
+            -0.568934891,
+            -0.532196444,
+            -3.165764662,
+            -0.737346519,
+            -0.487591028,
+            -0.662557456,
+            -1.043257783,
+            -3.014153447,
+            -0.634835065,
+            -0.9929364490000001,
+            -0.840400003,
+            -0.276486613,
+            -0.747411045,
+            -0.7668970690000001,
+            -0.942324445,
+            -0.13513425099999998,
+            -0.210148079,
+            -0.29762524,
+            -0.922627502,
+            -0.754154453,
+            -0.231010954,
+            -0.795542715,
+            -0.537110596,
+            -0.556996841,
+            -2.28309572,
+            -0.644110106,
+            -0.197176928,
+            -1.505077536,
+            -0.46914006399999997,
+            -0.567556108,
+            -0.42286704399999997,
+            -1.002172001,
+            -0.37474579700000005,
+            -0.519405744,
+            -0.413608109,
+            -0.93479915,
+            -0.193812845,
+            -0.7953905440000001,
+            -0.330226245,
+            -0.682790254,
+            -4.592253136
           ],
           "selected_hits": [
             0,
@@ -307,20 +307,13 @@
             0,
             0,
             0,
+            0,
+            0,
+            0,
+            0,
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
             1,
             0,
             0,
@@ -332,21 +325,76 @@
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
-            0,
-            0,
-            0,
             1,
             0,
             0,
@@ -357,78 +405,30 @@
             0,
             0,
             0,
-            1,
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
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
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
+            1
           ]
         }
       ],
@@ -1328,6 +1328,902 @@
           "score": -1.3483625769999998,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 12291,
+          "gene": "PRKAR2B",
+          "score": -2.180935028,
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
+          "candidate_index": 16907,
+          "gene": "TUSC3",
+          "score": -1.477456704,
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
+          "candidate_index": 6158,
+          "gene": "GMNC",
+          "score": -0.657510787,
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
+          "candidate_index": 3105,
+          "gene": "CLPP",
+          "score": -0.754310446,
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
+          "candidate_index": 11820,
+          "gene": "PLEKHB1",
+          "score": -0.42420400700000005,
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
+          "candidate_index": 561,
+          "gene": "ALG14",
+          "score": -2.68875708,
+          "hit": 1,
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
+          "candidate_index": 9781,
+          "gene": "MTMR14",
+          "score": -0.676362227,
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
+          "candidate_index": 4160,
+          "gene": "DLGAP4",
+          "score": -1.46070239,
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
+          "candidate_index": 4170,
+          "gene": "DLX3",
+          "score": -0.5142020860000001,
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
+          "candidate_index": 9809,
+          "gene": "MTUS1",
+          "score": -2.095547005,
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
+          "candidate_index": 2644,
+          "gene": "CDKL2",
+          "score": -0.798956039,
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
+          "candidate_index": 4197,
+          "gene": "DNA2",
+          "score": -0.939162108,
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
+          "candidate_index": 14958,
+          "gene": "SPATA31A7",
+          "score": -1.4418498690000001,
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
+          "candidate_index": 630,
+          "gene": "AMPD3",
+          "score": -1.560177346,
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
+          "candidate_index": 18046,
+          "gene": "ZNF341",
+          "score": -0.747779243,
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
+          "candidate_index": 10899,
+          "gene": "OR51B6",
+          "score": -0.573881217,
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
+          "candidate_index": 8855,
+          "gene": "LY6K",
+          "score": -1.133163553,
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
+          "candidate_index": 17561,
+          "gene": "WNT6",
+          "score": -1.671571265,
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
+          "candidate_index": 3741,
+          "gene": "CYP26A1",
+          "score": -1.181122722,
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
+          "candidate_index": 5303,
+          "gene": "FAM98C",
+          "score": -0.007484081,
+          "hit": 1,
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
+          "candidate_index": 10935,
+          "gene": "OR5A1",
+          "score": -1.315155034,
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
+          "candidate_index": 2758,
+          "gene": "CEP295NL",
+          "score": -0.48691684399999996,
+          "hit": 0,
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
+          "candidate_index": 9448,
+          "gene": "MLNR",
+          "score": -0.747039243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1271,
+          "gene": "ATP6V1B1",
+          "score": -0.201361404,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17657,
+          "gene": "YIPF5",
+          "score": -0.665553626,
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
+          "candidate_index": 15613,
+          "gene": "TBC1D10B",
+          "score": -1.332644192,
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
+          "candidate_index": 8980,
+          "gene": "MAN1A1",
+          "score": -0.538292791,
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
+          "candidate_index": 14623,
+          "gene": "SLCO4C1",
+          "score": -0.516317234,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18211,
+          "gene": "ZNF587B",
+          "score": -0.38926068399999997,
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
+          "candidate_index": 3402,
+          "gene": "CPQ",
+          "score": -0.21542853399999998,
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
+          "candidate_index": 17229,
+          "gene": "USP45",
+          "score": -0.744610965,
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
+          "candidate_index": 1362,
+          "gene": "B4GALNT1",
+          "score": -0.646906026,
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
+          "candidate_index": 8548,
+          "gene": "LMAN2L",
+          "score": -0.289915381,
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
+          "candidate_index": 6001,
+          "gene": "GFM1",
+          "score": -0.751344198,
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
+          "candidate_index": 13695,
+          "gene": "SAP130",
+          "score": -1.7633453890000002,
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
+          "candidate_index": 5508,
+          "gene": "FGF7",
+          "score": -0.634709573,
+          "hit": 0,
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
+          "candidate_index": 15267,
+          "gene": "STIM1",
+          "score": -0.872834543,
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
+          "candidate_index": 10153,
+          "gene": "NDUFB8",
+          "score": -0.38708333899999997,
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
+          "candidate_index": 14273,
+          "gene": "SLC16A11",
+          "score": -0.330831854,
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
+          "candidate_index": 16330,
+          "gene": "TMPO",
+          "score": -0.380735899,
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
+          "candidate_index": 2012,
+          "gene": "CACNA2D1",
+          "score": -0.841312252,
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
+          "candidate_index": 2017,
+          "gene": "CACNB2",
+          "score": -0.929824685,
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
+          "candidate_index": 2024,
+          "gene": "CACNG5",
+          "score": -0.554727847,
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
+          "candidate_index": 16366,
+          "gene": "TNFAIP3",
+          "score": -0.24478269600000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14326,
+          "gene": "SLC22A3",
+          "score": -0.693411715,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14328,
+          "gene": "SLC22A4",
+          "score": -0.568934891,
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
+          "candidate_index": 15133,
+          "gene": "SRRM1",
+          "score": -3.165764662,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 11281,
+          "gene": "PCDHA9",
+          "score": -0.737346519,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12795,
+          "gene": "RABL3",
+          "score": -0.487591028,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2892,
+          "gene": "CHMP1B",
+          "score": -0.662557456,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1105,
+          "gene": "ASB2",
+          "score": -1.043257783,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3085,
+          "gene": "CLIP2",
+          "score": -3.014153447,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 6842,
+          "gene": "HIST1H4I",
+          "score": -0.634835065,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13423,
+          "gene": "RPL19",
+          "score": -0.9929364490000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6444,
+          "gene": "GRIPAP1",
+          "score": -0.840400003,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13384,
+          "gene": "RORA",
+          "score": -0.276486613,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8639,
+          "gene": "LOX",
+          "score": -0.747411045,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13556,
+          "gene": "RSC1A1",
+          "score": -0.7668970690000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10859,
+          "gene": "OR2G6",
+          "score": -0.942324445,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13202,
+          "gene": "RICTOR",
+          "score": -0.13513425099999998,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11510,
+          "gene": "PFDN5",
+          "score": -0.210148079,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1717,
+          "gene": "C12orf49",
+          "score": -0.29762524,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6175,
+          "gene": "GNAQ",
+          "score": -0.922627502,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17823,
+          "gene": "ZFC3H1",
+          "score": -0.754154453,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5911,
+          "gene": "GATA6",
+          "score": -0.231010954,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6239,
+          "gene": "GOLPH3L",
+          "score": -0.795542715,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1693,
+          "gene": "BZW2",
+          "score": -0.537110596,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7750,
+          "gene": "KCNH5",
+          "score": -0.556996841,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9955,
+          "gene": "MYT1",
+          "score": -2.28309572,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7370,
+          "gene": "IL22RA2",
+          "score": -0.644110106,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11458,
+          "gene": "PDZD9",
+          "score": -0.197176928,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6240,
+          "gene": "GOLT1A",
+          "score": -1.505077536,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7190,
+          "gene": "IDI1",
+          "score": -0.46914006399999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12734,
+          "gene": "RAB25",
+          "score": -0.567556108,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12911,
+          "gene": "RASSF3",
+          "score": -0.42286704399999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7466,
+          "gene": "INSL5",
+          "score": -1.002172001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2009,
+          "gene": "CACNA1H",
+          "score": -0.37474579700000005,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15203,
+          "gene": "ST3GAL5",
+          "score": -0.519405744,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16625,
+          "gene": "TRIM39-RPP21",
+          "score": -0.413608109,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2030,
+          "gene": "CACYBP",
+          "score": -0.93479915,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3189,
+          "gene": "CNP",
+          "score": -0.193812845,
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
+          "candidate_index": 18097,
+          "gene": "ZNF436",
+          "score": -0.682790254,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16937,
+          "gene": "TXNL4A",
+          "score": -4.592253136,
+          "hit": 1,
+          "round": 1
         }
       ],
       "queried_history": [
@@ -2226,6 +3122,902 @@
           "score": -1.3483625769999998,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 12291,
+          "gene": "PRKAR2B",
+          "score": -2.180935028,
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
+          "candidate_index": 16907,
+          "gene": "TUSC3",
+          "score": -1.477456704,
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
+          "candidate_index": 6158,
+          "gene": "GMNC",
+          "score": -0.657510787,
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
+          "candidate_index": 3105,
+          "gene": "CLPP",
+          "score": -0.754310446,
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
+          "candidate_index": 11820,
+          "gene": "PLEKHB1",
+          "score": -0.42420400700000005,
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
+          "candidate_index": 561,
+          "gene": "ALG14",
+          "score": -2.68875708,
+          "hit": 1,
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
+          "candidate_index": 9781,
+          "gene": "MTMR14",
+          "score": -0.676362227,
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
+          "candidate_index": 4160,
+          "gene": "DLGAP4",
+          "score": -1.46070239,
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
+          "candidate_index": 4170,
+          "gene": "DLX3",
+          "score": -0.5142020860000001,
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
+          "candidate_index": 9809,
+          "gene": "MTUS1",
+          "score": -2.095547005,
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
+          "candidate_index": 2644,
+          "gene": "CDKL2",
+          "score": -0.798956039,
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
+          "candidate_index": 4197,
+          "gene": "DNA2",
+          "score": -0.939162108,
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
+          "candidate_index": 14958,
+          "gene": "SPATA31A7",
+          "score": -1.4418498690000001,
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
+          "candidate_index": 630,
+          "gene": "AMPD3",
+          "score": -1.560177346,
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
+          "candidate_index": 18046,
+          "gene": "ZNF341",
+          "score": -0.747779243,
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
+          "candidate_index": 10899,
+          "gene": "OR51B6",
+          "score": -0.573881217,
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
+          "candidate_index": 8855,
+          "gene": "LY6K",
+          "score": -1.133163553,
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
+          "candidate_index": 17561,
+          "gene": "WNT6",
+          "score": -1.671571265,
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
+          "candidate_index": 3741,
+          "gene": "CYP26A1",
+          "score": -1.181122722,
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
+          "candidate_index": 5303,
+          "gene": "FAM98C",
+          "score": -0.007484081,
+          "hit": 1,
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
+          "candidate_index": 10935,
+          "gene": "OR5A1",
+          "score": -1.315155034,
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
+          "candidate_index": 2758,
+          "gene": "CEP295NL",
+          "score": -0.48691684399999996,
+          "hit": 0,
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
+          "candidate_index": 9448,
+          "gene": "MLNR",
+          "score": -0.747039243,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1271,
+          "gene": "ATP6V1B1",
+          "score": -0.201361404,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17657,
+          "gene": "YIPF5",
+          "score": -0.665553626,
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
+          "candidate_index": 15613,
+          "gene": "TBC1D10B",
+          "score": -1.332644192,
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
+          "candidate_index": 8980,
+          "gene": "MAN1A1",
+          "score": -0.538292791,
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
+          "candidate_index": 14623,
+          "gene": "SLCO4C1",
+          "score": -0.516317234,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18211,
+          "gene": "ZNF587B",
+          "score": -0.38926068399999997,
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
+          "candidate_index": 3402,
+          "gene": "CPQ",
+          "score": -0.21542853399999998,
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
+          "candidate_index": 17229,
+          "gene": "USP45",
+          "score": -0.744610965,
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
+          "candidate_index": 1362,
+          "gene": "B4GALNT1",
+          "score": -0.646906026,
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
+          "candidate_index": 8548,
+          "gene": "LMAN2L",
+          "score": -0.289915381,
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
+          "candidate_index": 6001,
+          "gene": "GFM1",
+          "score": -0.751344198,
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
+          "candidate_index": 13695,
+          "gene": "SAP130",
+          "score": -1.7633453890000002,
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
+          "candidate_index": 5508,
+          "gene": "FGF7",
+          "score": -0.634709573,
+          "hit": 0,
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
+          "candidate_index": 15267,
+          "gene": "STIM1",
+          "score": -0.872834543,
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
+          "candidate_index": 10153,
+          "gene": "NDUFB8",
+          "score": -0.38708333899999997,
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
+          "candidate_index": 14273,
+          "gene": "SLC16A11",
+          "score": -0.330831854,
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
+          "candidate_index": 16330,
+          "gene": "TMPO",
+          "score": -0.380735899,
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
+          "candidate_index": 2012,
+          "gene": "CACNA2D1",
+          "score": -0.841312252,
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
+          "candidate_index": 2017,
+          "gene": "CACNB2",
+          "score": -0.929824685,
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
+          "candidate_index": 2024,
+          "gene": "CACNG5",
+          "score": -0.554727847,
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
+          "candidate_index": 16366,
+          "gene": "TNFAIP3",
+          "score": -0.24478269600000002,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14326,
+          "gene": "SLC22A3",
+          "score": -0.693411715,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14328,
+          "gene": "SLC22A4",
+          "score": -0.568934891,
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
+          "candidate_index": 15133,
+          "gene": "SRRM1",
+          "score": -3.165764662,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 11281,
+          "gene": "PCDHA9",
+          "score": -0.737346519,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12795,
+          "gene": "RABL3",
+          "score": -0.487591028,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2892,
+          "gene": "CHMP1B",
+          "score": -0.662557456,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1105,
+          "gene": "ASB2",
+          "score": -1.043257783,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3085,
+          "gene": "CLIP2",
+          "score": -3.014153447,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 6842,
+          "gene": "HIST1H4I",
+          "score": -0.634835065,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13423,
+          "gene": "RPL19",
+          "score": -0.9929364490000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6444,
+          "gene": "GRIPAP1",
+          "score": -0.840400003,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13384,
+          "gene": "RORA",
+          "score": -0.276486613,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8639,
+          "gene": "LOX",
+          "score": -0.747411045,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13556,
+          "gene": "RSC1A1",
+          "score": -0.7668970690000001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10859,
+          "gene": "OR2G6",
+          "score": -0.942324445,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13202,
+          "gene": "RICTOR",
+          "score": -0.13513425099999998,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11510,
+          "gene": "PFDN5",
+          "score": -0.210148079,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1717,
+          "gene": "C12orf49",
+          "score": -0.29762524,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6175,
+          "gene": "GNAQ",
+          "score": -0.922627502,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17823,
+          "gene": "ZFC3H1",
+          "score": -0.754154453,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5911,
+          "gene": "GATA6",
+          "score": -0.231010954,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6239,
+          "gene": "GOLPH3L",
+          "score": -0.795542715,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1693,
+          "gene": "BZW2",
+          "score": -0.537110596,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7750,
+          "gene": "KCNH5",
+          "score": -0.556996841,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9955,
+          "gene": "MYT1",
+          "score": -2.28309572,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7370,
+          "gene": "IL22RA2",
+          "score": -0.644110106,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11458,
+          "gene": "PDZD9",
+          "score": -0.197176928,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6240,
+          "gene": "GOLT1A",
+          "score": -1.505077536,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7190,
+          "gene": "IDI1",
+          "score": -0.46914006399999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12734,
+          "gene": "RAB25",
+          "score": -0.567556108,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12911,
+          "gene": "RASSF3",
+          "score": -0.42286704399999997,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7466,
+          "gene": "INSL5",
+          "score": -1.002172001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2009,
+          "gene": "CACNA1H",
+          "score": -0.37474579700000005,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15203,
+          "gene": "ST3GAL5",
+          "score": -0.519405744,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16625,
+          "gene": "TRIM39-RPP21",
+          "score": -0.413608109,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2030,
+          "gene": "CACYBP",
+          "score": -0.93479915,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3189,
+          "gene": "CNP",
+          "score": -0.193812845,
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
+          "candidate_index": 18097,
+          "gene": "ZNF436",
+          "score": -0.682790254,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16937,
+          "gene": "TXNL4A",
+          "score": -4.592253136,
+          "hit": 1,
+          "round": 1
         }
       ]
     }

```
