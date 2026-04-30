# Change Record — candidate_1

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Carnevale22_Adenosine/run-2/best/current/harness
Generated at: 2026-04-30T07:14:13.792133

## Files Changed

- model.py: modified (added=65, deleted=1, delta=64)
- outputs/metrics.json: new (added=2233, deleted=0, delta=2233)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -29,4 +29,68 @@
     traditional algorithms, machine learning models, deep learning models, biological models,
     and mathematical models.
     """
-    pass
+    import numpy as np
+    
+    # Set random seed for reproducibility
+    rng = np.random.RandomState(seed)
+    
+    # Get all candidate indices
+    n_candidates = len(candidates)
+    candidate_indices = list(range(n_candidates))
+    
+    # Remove already selected candidates
+    selected_indices = {h['candidate_index'] for h in history}
+    available_indices = [i for i in candidate_indices if i not in selected_indices]
+    
+    # If no history (first round), use random selection with some diversity
+    if not history:
+        # Simple random sampling for the first batch
+        selected = rng.choice(available_indices, size=min(batch_size, len(available_indices)), replace=False)
+        return selected.tolist()
+    
+    # Build statistics from history
+    # Track mean score and count for each candidate
+    scores = {}
+    counts = {}
+    
+    for h in history:
+        idx = h['candidate_index']
+        score = h['score']
+        if idx not in scores:
+            scores[idx] = 0.0
+            counts[idx] = 0
+        scores[idx] += score
+        counts[idx] += 1
+    
+    # Calculate mean scores
+    mean_scores = {idx: scores[idx] / counts[idx] for idx in scores}
+    
+    # UCB algorithm: balance mean reward vs exploration bonus
+    total_pulls = len(history)
+    ucb_scores = []
+    
+    for idx in available_indices:
+        if idx in mean_scores:
+            # Exploitation term: mean score
+            exploitation = mean_scores[idx]
+            # Exploration term: uncertainty bonus
+            exploration = np.sqrt(2 * np.log(total_pulls) / counts[idx])
+            ucb = exploitation + exploration
+        else:
+            # Never-seen candidates get high priority for exploration
+            ucb = float('inf')
+        ucb_scores.append((ucb, idx))
+    
+    # Sort by UCB score (descending) and select top candidates
+    ucb_scores.sort(reverse=True)
+    selected = [idx for _, idx in ucb_scores[:batch_size]]
+    
+    # If we don't have enough high-UCB candidates, fill with random unexplored ones
+    if len(selected) < batch_size:
+        remaining = [idx for idx in available_indices if idx not in selected]
+        needed = batch_size - len(selected)
+        if remaining:
+            additional = rng.choice(remaining, size=min(needed, len(remaining)), replace=False)
+            selected.extend(additional.tolist())
+    
+    return selected

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -0,0 +1,2233 @@
+{
+  "task": "perturb-genes-brief",
+  "data_name": "Carnevale22_Adenosine",
+  "measurement": "the change in T cell proliferation",
+  "task_prompt": {
+    "Task": "identify genes that, upon being knocked out, would boost the efficacy of engineered T cells in the presence of an adenosine agonist that creates an immunosuppresive condition",
+    "Measurement": "the change in T cell proliferation"
+  },
+  "metrics": {
+    "test": {
+      "pool_size": 18861,
+      "rounds": 1,
+      "executed_rounds": 1,
+      "batch_size": 128,
+      "seed": 42,
+      "baseline_total_queries": 0,
+      "baseline_total_hits": 0,
+      "delta_queries": 128,
+      "delta_hits": 5,
+      "total_queries": 128,
+      "total_hits": 5,
+      "top_k": 943,
+      "hit_curve": {
+        "queries": [
+          0,
+          128
+        ],
+        "hits": [
+          0,
+          5
+        ]
+      },
+      "auc": 320.0,
+      "auc_normalized": 0.002651113467656416,
+      "ncg": 0.22370739228746422,
+      "round_details": [
+        {
+          "round": 0,
+          "selected_count": 128,
+          "hits": 5,
+          "cumulative_hits": 5,
+          "precision_at_batch": 0.0390625,
+          "selected": [
+            "NonTarget.CTRL183",
+            "CCZ1B",
+            "RRP15",
+            "DERL2",
+            "LCN9",
+            "C11orf16",
+            "SLF2",
+            "MEX3C",
+            "APEX1",
+            "CLU",
+            "CSPG5",
+            "EQTN",
+            "PLA2R1",
+            "URI1",
+            "PROK2",
+            "BICRA",
+            "BCAS4",
+            "FBXO4",
+            "RIGI",
+            "SCN2B",
+            "NRBP2",
+            "PSTPIP1",
+            "DNAAF11",
+            "RFX6",
+            "CCDC12",
+            "ATP6V0D1",
+            "PTPRCAP",
+            "RPS6KA6",
+            "IL12RB2",
+            "GAGE12I",
+            "C5orf15",
+            "ADD3",
+            "ENO4",
+            "TTLL11",
+            "CDHR3",
+            "MTCL1",
+            "ZMYND12",
+            "DDR1",
+            "DHX57",
+            "SYNE4",
+            "ABCB1",
+            "EIF4E1B",
+            "PIGS",
+            "PPIL6",
+            "CD160",
+            "H2BC21",
+            "MAP3K1",
+            "NDUFS6",
+            "TMEM176B",
+            "MRPS7",
+            "TARP",
+            "PPIB",
+            "TMEM184A",
+            "RNASE6",
+            "LRRC14B",
+            "FGFBP1",
+            "SDR39U1",
+            "GOLGA8R",
+            "NonTarget.CTRL241",
+            "NELFE",
+            "PPARA",
+            "TLCD3B",
+            "MACROD2",
+            "FOXRED2",
+            "MAMDC4",
+            "NBL1",
+            "LIPM",
+            "MGAT4D",
+            "HACL1",
+            "PRELID3A",
+            "PTPRS",
+            "MYO5B",
+            "TNFSF4",
+            "HCLS1",
+            "MOGS",
+            "COL20A1",
+            "OPN1MW2",
+            "CDC34",
+            "C7orf77",
+            "NEUROD6",
+            "CDK14",
+            "COQ10B",
+            "SLC16A5",
+            "TERB1",
+            "NUP58",
+            "HEATR5A",
+            "THRSP",
+            "ARID2",
+            "SPON2",
+            "CDH13",
+            "TPBGL",
+            "TGFBI",
+            "MED16",
+            "IRAK2",
+            "TBC1D5",
+            "ADRB1",
+            "VWC2",
+            "IGSF10",
+            "IL11",
+            "TRIM49C",
+            "ZNF37A",
+            "HMGCR",
+            "TVP23B",
+            "ABCC4",
+            "CCNL2",
+            "PTGDR2",
+            "RPL7L1",
+            "GLRX5",
+            "TSPAN31",
+            "ADGRF1",
+            "SKIC8",
+            "PPIL1",
+            "MYO1H",
+            "SEMA6D",
+            "RIMBP3B",
+            "DCAF12",
+            "SPATA31C2",
+            "ST6GALNAC5",
+            "KDM5B",
+            "OR56A3",
+            "FAM210B",
+            "MSTO1",
+            "DDX49",
+            "SORCS3",
+            "GAL3ST1",
+            "CD5",
+            "PPP1R18",
+            "CAPN5"
+          ],
+          "selected_scores": [
+            -0.013679,
+            -0.077916,
+            0.14121,
+            -0.17611,
+            0.17513,
+            -0.030504,
+            0.063605,
+            -0.071707,
+            -0.126416,
+            -0.015579,
+            0.11243,
+            0.00054836,
+            -0.17919,
+            0.015715,
+            -0.10179,
+            0.16015,
+            0.22939,
+            -0.56094,
+            0.051934,
+            0.33024,
+            0.073147,
+            0.0942,
+            0.096602,
+            0.13655,
+            -0.14117,
+            -0.9752,
+            0.091003,
+            0.030792,
+            0.23173,
+            0.04828,
+            0.021269,
+            -0.22285,
+            0.11626,
+            -0.04865,
+            -0.069768,
+            0.0146,
+            0.25557,
+            -0.14871,
+            0.071437,
+            0.09327,
+            0.34192,
+            -0.0537,
+            -0.04923,
+            -0.22363,
+            -0.054722,
+            -0.23789,
+            0.034984,
+            -0.16117,
+            0.087379,
+            0.078211,
+            -0.035043,
+            0.16509,
+            -0.044388,
+            0.088345,
+            -0.15484,
+            -0.27016,
+            0.11719,
+            0.048333,
+            0.13635,
+            -0.24708,
+            -0.049037,
+            -0.22864,
+            -0.029052,
+            0.044742,
+            0.01794,
+            0.12739,
+            -0.21006,
+            -0.093951,
+            0.1124,
+            0.080141,
+            -0.0097004,
+            -0.013569,
+            -0.19644,
+            -0.31934,
+            -0.22716,
+            0.075814,
+            -0.30922,
+            -0.26361,
+            -0.2155,
+            0.25833,
+            -0.033587,
+            -0.028383,
+            -0.013077,
+            -0.17629,
+            -0.18384,
+            0.16255,
+            0.083109,
+            0.055388,
+            -0.011189,
+            0.52117,
+            0.11907,
+            0.046072,
+            0.14753,
+            0.14208,
+            0.20667,
+            -0.24,
+            0.031964,
+            -0.11365,
+            -0.10291,
+            -0.056043,
+            0.19132,
+            -0.30428,
+            -0.038374,
+            0.30528,
+            -0.13455,
+            -0.17351,
+            0.09012,
+            0.038956,
+            0.078824,
+            0.074631,
+            0.044791,
+            0.16078,
+            0.14864,
+            0.018581,
+            -0.34541,
+            -0.016793,
+            -0.10327,
+            0.1771,
+            0.036445,
+            -0.038736,
+            0.10696,
+            -0.32416,
+            0.051002,
+            0.12779,
+            -0.089594,
+            0.080001,
+            -0.23215,
+            -0.2056985
+          ],
+          "selected_hits": [
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
+            0
+          ]
+        }
+      ],
+      "queried_records": [
+        {
+          "candidate_index": 10746,
+          "gene": "NonTarget.CTRL183",
+          "score": -0.013679,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2480,
+          "gene": "CCZ1B",
+          "score": -0.077916,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13916,
+          "gene": "RRP15",
+          "score": 0.14121,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4128,
+          "gene": "DERL2",
+          "score": -0.17611,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8331,
+          "gene": "LCN9",
+          "score": 0.17513,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1710,
+          "gene": "C11orf16",
+          "score": -0.030504,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15003,
+          "gene": "SLF2",
+          "score": 0.063605,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9249,
+          "gene": "MEX3C",
+          "score": -0.071707,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 828,
+          "gene": "APEX1",
+          "score": -0.126416,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3194,
+          "gene": "CLU",
+          "score": -0.015579,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3616,
+          "gene": "CSPG5",
+          "score": 0.11243,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4936,
+          "gene": "EQTN",
+          "score": 0.00054836,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12151,
+          "gene": "PLA2R1",
+          "score": -0.17919,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17557,
+          "gene": "URI1",
+          "score": 0.015715,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12726,
+          "gene": "PROK2",
+          "score": -0.10179,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1512,
+          "gene": "BICRA",
+          "score": 0.16015,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1430,
+          "gene": "BCAS4",
+          "score": 0.22939,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5394,
+          "gene": "FBXO4",
+          "score": -0.56094,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 13585,
+          "gene": "RIGI",
+          "score": 0.051934,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14168,
+          "gene": "SCN2B",
+          "score": 0.33024,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10474,
+          "gene": "NRBP2",
+          "score": 0.073147,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12927,
+          "gene": "PSTPIP1",
+          "score": 0.0942,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4281,
+          "gene": "DNAAF11",
+          "score": 0.096602,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13495,
+          "gene": "RFX6",
+          "score": 0.13655,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2267,
+          "gene": "CCDC12",
+          "score": -0.14117,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1261,
+          "gene": "ATP6V0D1",
+          "score": -0.9752,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 13005,
+          "gene": "PTPRCAP",
+          "score": 0.091003,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13886,
+          "gene": "RPS6KA6",
+          "score": 0.030792,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7308,
+          "gene": "IL12RB2",
+          "score": 0.23173,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5843,
+          "gene": "GAGE12I",
+          "score": 0.04828,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1944,
+          "gene": "C5orf15",
+          "score": 0.021269,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 313,
+          "gene": "ADD3",
+          "score": -0.22285,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4849,
+          "gene": "ENO4",
+          "score": 0.11626,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17243,
+          "gene": "TTLL11",
+          "score": -0.04865,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2635,
+          "gene": "CDHR3",
+          "score": -0.069768,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9680,
+          "gene": "MTCL1",
+          "score": 0.0146,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18286,
+          "gene": "ZMYND12",
+          "score": 0.25557,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4007,
+          "gene": "DDR1",
+          "score": -0.14871,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4193,
+          "gene": "DHX57",
+          "score": 0.071437,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15833,
+          "gene": "SYNE4",
+          "score": 0.09327,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 42,
+          "gene": "ABCB1",
+          "score": 0.34192,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 4739,
+          "gene": "EIF4E1B",
+          "score": -0.0537,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12037,
+          "gene": "PIGS",
+          "score": -0.04923,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12498,
+          "gene": "PPIL6",
+          "score": -0.22363,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2485,
+          "gene": "CD160",
+          "score": -0.054722,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6619,
+          "gene": "H2BC21",
+          "score": -0.23789,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8966,
+          "gene": "MAP3K1",
+          "score": 0.034984,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10090,
+          "gene": "NDUFS6",
+          "score": -0.16117,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16544,
+          "gene": "TMEM176B",
+          "score": 0.087379,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9606,
+          "gene": "MRPS7",
+          "score": 0.078211,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15955,
+          "gene": "TARP",
+          "score": -0.035043,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12487,
+          "gene": "PPIB",
+          "score": 0.16509,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16555,
+          "gene": "TMEM184A",
+          "score": -0.044388,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13646,
+          "gene": "RNASE6",
+          "score": 0.088345,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8665,
+          "gene": "LRRC14B",
+          "score": -0.15484,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5504,
+          "gene": "FGFBP1",
+          "score": -0.27016,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14222,
+          "gene": "SDR39U1",
+          "score": 0.11719,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6237,
+          "gene": "GOLGA8R",
+          "score": 0.048333,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10811,
+          "gene": "NonTarget.CTRL241",
+          "score": 0.13635,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10134,
+          "gene": "NELFE",
+          "score": -0.24708,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12461,
+          "gene": "PPARA",
+          "score": -0.049037,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16386,
+          "gene": "TLCD3B",
+          "score": -0.22864,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8863,
+          "gene": "MACROD2",
+          "score": -0.029052,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5681,
+          "gene": "FOXRED2",
+          "score": 0.044742,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8928,
+          "gene": "MAMDC4",
+          "score": 0.01794,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9972,
+          "gene": "NBL1",
+          "score": 0.12739,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8471,
+          "gene": "LIPM",
+          "score": -0.21006,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9287,
+          "gene": "MGAT4D",
+          "score": -0.093951,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6670,
+          "gene": "HACL1",
+          "score": 0.1124,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12650,
+          "gene": "PRELID3A",
+          "score": 0.080141,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13017,
+          "gene": "PTPRS",
+          "score": -0.0097004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9857,
+          "gene": "MYO5B",
+          "score": -0.013569,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16787,
+          "gene": "TNFSF4",
+          "score": -0.19644,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6725,
+          "gene": "HCLS1",
+          "score": -0.31934,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9445,
+          "gene": "MOGS",
+          "score": -0.22716,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3323,
+          "gene": "COL20A1",
+          "score": 0.075814,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10984,
+          "gene": "OPN1MW2",
+          "score": -0.30922,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2585,
+          "gene": "CDC34",
+          "score": -0.26361,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1983,
+          "gene": "C7orf77",
+          "score": -0.2155,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10158,
+          "gene": "NEUROD6",
+          "score": 0.25833,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2647,
+          "gene": "CDK14",
+          "score": -0.033587,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3394,
+          "gene": "COQ10B",
+          "score": -0.028383,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14655,
+          "gene": "SLC16A5",
+          "score": -0.013077,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16183,
+          "gene": "TERB1",
+          "score": -0.17629,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10611,
+          "gene": "NUP58",
+          "score": -0.18384,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6758,
+          "gene": "HEATR5A",
+          "score": 0.16255,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16315,
+          "gene": "THRSP",
+          "score": 0.083109,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 980,
+          "gene": "ARID2",
+          "score": 0.055388,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15429,
+          "gene": "SPON2",
+          "score": -0.011189,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2616,
+          "gene": "CDH13",
+          "score": 0.52117,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 16883,
+          "gene": "TPBGL",
+          "score": 0.11907,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16257,
+          "gene": "TGFBI",
+          "score": 0.046072,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9162,
+          "gene": "MED16",
+          "score": 0.14753,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7511,
+          "gene": "IRAK2",
+          "score": 0.14208,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16031,
+          "gene": "TBC1D5",
+          "score": 0.20667,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 379,
+          "gene": "ADRB1",
+          "score": -0.24,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17816,
+          "gene": "VWC2",
+          "score": 0.031964,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7278,
+          "gene": "IGSF10",
+          "score": -0.11365,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7303,
+          "gene": "IL11",
+          "score": -0.10291,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17023,
+          "gene": "TRIM49C",
+          "score": -0.056043,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18441,
+          "gene": "ZNF37A",
+          "score": 0.19132,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6896,
+          "gene": "HMGCR",
+          "score": -0.30428,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17298,
+          "gene": "TVP23B",
+          "score": -0.038374,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 57,
+          "gene": "ABCC4",
+          "score": 0.30528,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2448,
+          "gene": "CCNL2",
+          "score": -0.13455,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12949,
+          "gene": "PTGDR2",
+          "score": -0.17351,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13830,
+          "gene": "RPL7L1",
+          "score": 0.09012,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6128,
+          "gene": "GLRX5",
+          "score": 0.038956,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17163,
+          "gene": "TSPAN31",
+          "score": 0.078824,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 326,
+          "gene": "ADGRF1",
+          "score": 0.074631,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14601,
+          "gene": "SKIC8",
+          "score": 0.044791,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12494,
+          "gene": "PPIL1",
+          "score": 0.16078,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9853,
+          "gene": "MYO1H",
+          "score": 0.14864,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14297,
+          "gene": "SEMA6D",
+          "score": 0.018581,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13591,
+          "gene": "RIMBP3B",
+          "score": -0.34541,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 3931,
+          "gene": "DCAF12",
+          "score": -0.016793,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15330,
+          "gene": "SPATA31C2",
+          "score": -0.10327,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15593,
+          "gene": "ST6GALNAC5",
+          "score": 0.1771,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7840,
+          "gene": "KDM5B",
+          "score": 0.036445,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11247,
+          "gene": "OR56A3",
+          "score": -0.038736,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5227,
+          "gene": "FAM210B",
+          "score": 0.10696,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9656,
+          "gene": "MSTO1",
+          "score": -0.32416,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4037,
+          "gene": "DDX49",
+          "score": 0.051002,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15231,
+          "gene": "SORCS3",
+          "score": 0.12779,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5849,
+          "gene": "GAL3ST1",
+          "score": -0.089594,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2540,
+          "gene": "CD5",
+          "score": 0.080001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12534,
+          "gene": "PPP1R18",
+          "score": -0.23215,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2145,
+          "gene": "CAPN5",
+          "score": -0.2056985,
+          "hit": 0,
+          "round": 0
+        }
+      ],
+      "queried_history": [
+        {
+          "candidate_index": 10746,
+          "gene": "NonTarget.CTRL183",
+          "score": -0.013679,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2480,
+          "gene": "CCZ1B",
+          "score": -0.077916,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13916,
+          "gene": "RRP15",
+          "score": 0.14121,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4128,
+          "gene": "DERL2",
+          "score": -0.17611,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8331,
+          "gene": "LCN9",
+          "score": 0.17513,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1710,
+          "gene": "C11orf16",
+          "score": -0.030504,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15003,
+          "gene": "SLF2",
+          "score": 0.063605,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9249,
+          "gene": "MEX3C",
+          "score": -0.071707,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 828,
+          "gene": "APEX1",
+          "score": -0.126416,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3194,
+          "gene": "CLU",
+          "score": -0.015579,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3616,
+          "gene": "CSPG5",
+          "score": 0.11243,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4936,
+          "gene": "EQTN",
+          "score": 0.00054836,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12151,
+          "gene": "PLA2R1",
+          "score": -0.17919,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17557,
+          "gene": "URI1",
+          "score": 0.015715,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12726,
+          "gene": "PROK2",
+          "score": -0.10179,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1512,
+          "gene": "BICRA",
+          "score": 0.16015,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1430,
+          "gene": "BCAS4",
+          "score": 0.22939,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5394,
+          "gene": "FBXO4",
+          "score": -0.56094,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 13585,
+          "gene": "RIGI",
+          "score": 0.051934,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14168,
+          "gene": "SCN2B",
+          "score": 0.33024,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10474,
+          "gene": "NRBP2",
+          "score": 0.073147,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12927,
+          "gene": "PSTPIP1",
+          "score": 0.0942,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4281,
+          "gene": "DNAAF11",
+          "score": 0.096602,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13495,
+          "gene": "RFX6",
+          "score": 0.13655,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2267,
+          "gene": "CCDC12",
+          "score": -0.14117,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1261,
+          "gene": "ATP6V0D1",
+          "score": -0.9752,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 13005,
+          "gene": "PTPRCAP",
+          "score": 0.091003,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13886,
+          "gene": "RPS6KA6",
+          "score": 0.030792,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7308,
+          "gene": "IL12RB2",
+          "score": 0.23173,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5843,
+          "gene": "GAGE12I",
+          "score": 0.04828,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1944,
+          "gene": "C5orf15",
+          "score": 0.021269,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 313,
+          "gene": "ADD3",
+          "score": -0.22285,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4849,
+          "gene": "ENO4",
+          "score": 0.11626,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17243,
+          "gene": "TTLL11",
+          "score": -0.04865,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2635,
+          "gene": "CDHR3",
+          "score": -0.069768,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9680,
+          "gene": "MTCL1",
+          "score": 0.0146,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18286,
+          "gene": "ZMYND12",
+          "score": 0.25557,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4007,
+          "gene": "DDR1",
+          "score": -0.14871,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4193,
+          "gene": "DHX57",
+          "score": 0.071437,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15833,
+          "gene": "SYNE4",
+          "score": 0.09327,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 42,
+          "gene": "ABCB1",
+          "score": 0.34192,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 4739,
+          "gene": "EIF4E1B",
+          "score": -0.0537,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12037,
+          "gene": "PIGS",
+          "score": -0.04923,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12498,
+          "gene": "PPIL6",
+          "score": -0.22363,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2485,
+          "gene": "CD160",
+          "score": -0.054722,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6619,
+          "gene": "H2BC21",
+          "score": -0.23789,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8966,
+          "gene": "MAP3K1",
+          "score": 0.034984,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10090,
+          "gene": "NDUFS6",
+          "score": -0.16117,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16544,
+          "gene": "TMEM176B",
+          "score": 0.087379,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9606,
+          "gene": "MRPS7",
+          "score": 0.078211,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15955,
+          "gene": "TARP",
+          "score": -0.035043,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12487,
+          "gene": "PPIB",
+          "score": 0.16509,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16555,
+          "gene": "TMEM184A",
+          "score": -0.044388,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13646,
+          "gene": "RNASE6",
+          "score": 0.088345,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8665,
+          "gene": "LRRC14B",
+          "score": -0.15484,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5504,
+          "gene": "FGFBP1",
+          "score": -0.27016,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14222,
+          "gene": "SDR39U1",
+          "score": 0.11719,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6237,
+          "gene": "GOLGA8R",
+          "score": 0.048333,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10811,
+          "gene": "NonTarget.CTRL241",
+          "score": 0.13635,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10134,
+          "gene": "NELFE",
+          "score": -0.24708,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12461,
+          "gene": "PPARA",
+          "score": -0.049037,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16386,
+          "gene": "TLCD3B",
+          "score": -0.22864,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8863,
+          "gene": "MACROD2",
+          "score": -0.029052,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5681,
+          "gene": "FOXRED2",
+          "score": 0.044742,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8928,
+          "gene": "MAMDC4",
+          "score": 0.01794,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9972,
+          "gene": "NBL1",
+          "score": 0.12739,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 8471,
+          "gene": "LIPM",
+          "score": -0.21006,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9287,
+          "gene": "MGAT4D",
+          "score": -0.093951,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6670,
+          "gene": "HACL1",
+          "score": 0.1124,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12650,
+          "gene": "PRELID3A",
+          "score": 0.080141,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13017,
+          "gene": "PTPRS",
+          "score": -0.0097004,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9857,
+          "gene": "MYO5B",
+          "score": -0.013569,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16787,
+          "gene": "TNFSF4",
+          "score": -0.19644,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6725,
+          "gene": "HCLS1",
+          "score": -0.31934,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9445,
+          "gene": "MOGS",
+          "score": -0.22716,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3323,
+          "gene": "COL20A1",
+          "score": 0.075814,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10984,
+          "gene": "OPN1MW2",
+          "score": -0.30922,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2585,
+          "gene": "CDC34",
+          "score": -0.26361,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 1983,
+          "gene": "C7orf77",
+          "score": -0.2155,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10158,
+          "gene": "NEUROD6",
+          "score": 0.25833,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2647,
+          "gene": "CDK14",
+          "score": -0.033587,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 3394,
+          "gene": "COQ10B",
+          "score": -0.028383,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14655,
+          "gene": "SLC16A5",
+          "score": -0.013077,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16183,
+          "gene": "TERB1",
+          "score": -0.17629,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 10611,
+          "gene": "NUP58",
+          "score": -0.18384,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6758,
+          "gene": "HEATR5A",
+          "score": 0.16255,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16315,
+          "gene": "THRSP",
+          "score": 0.083109,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 980,
+          "gene": "ARID2",
+          "score": 0.055388,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15429,
+          "gene": "SPON2",
+          "score": -0.011189,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2616,
+          "gene": "CDH13",
+          "score": 0.52117,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 16883,
+          "gene": "TPBGL",
+          "score": 0.11907,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16257,
+          "gene": "TGFBI",
+          "score": 0.046072,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9162,
+          "gene": "MED16",
+          "score": 0.14753,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7511,
+          "gene": "IRAK2",
+          "score": 0.14208,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 16031,
+          "gene": "TBC1D5",
+          "score": 0.20667,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 379,
+          "gene": "ADRB1",
+          "score": -0.24,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17816,
+          "gene": "VWC2",
+          "score": 0.031964,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7278,
+          "gene": "IGSF10",
+          "score": -0.11365,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7303,
+          "gene": "IL11",
+          "score": -0.10291,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17023,
+          "gene": "TRIM49C",
+          "score": -0.056043,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 18441,
+          "gene": "ZNF37A",
+          "score": 0.19132,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6896,
+          "gene": "HMGCR",
+          "score": -0.30428,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17298,
+          "gene": "TVP23B",
+          "score": -0.038374,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 57,
+          "gene": "ABCC4",
+          "score": 0.30528,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2448,
+          "gene": "CCNL2",
+          "score": -0.13455,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12949,
+          "gene": "PTGDR2",
+          "score": -0.17351,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13830,
+          "gene": "RPL7L1",
+          "score": 0.09012,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 6128,
+          "gene": "GLRX5",
+          "score": 0.038956,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 17163,
+          "gene": "TSPAN31",
+          "score": 0.078824,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 326,
+          "gene": "ADGRF1",
+          "score": 0.074631,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14601,
+          "gene": "SKIC8",
+          "score": 0.044791,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12494,
+          "gene": "PPIL1",
+          "score": 0.16078,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9853,
+          "gene": "MYO1H",
+          "score": 0.14864,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 14297,
+          "gene": "SEMA6D",
+          "score": 0.018581,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 13591,
+          "gene": "RIMBP3B",
+          "score": -0.34541,
+          "hit": 1,
+          "round": 0
+        },
+        {
+          "candidate_index": 3931,
+          "gene": "DCAF12",
+          "score": -0.016793,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15330,
+          "gene": "SPATA31C2",
+          "score": -0.10327,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15593,
+          "gene": "ST6GALNAC5",
+          "score": 0.1771,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 7840,
+          "gene": "KDM5B",
+          "score": 0.036445,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 11247,
+          "gene": "OR56A3",
+          "score": -0.038736,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5227,
+          "gene": "FAM210B",
+          "score": 0.10696,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 9656,
+          "gene": "MSTO1",
+          "score": -0.32416,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 4037,
+          "gene": "DDX49",
+          "score": 0.051002,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 15231,
+          "gene": "SORCS3",
+          "score": 0.12779,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 5849,
+          "gene": "GAL3ST1",
+          "score": -0.089594,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2540,
+          "gene": "CD5",
+          "score": 0.080001,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 12534,
+          "gene": "PPP1R18",
+          "score": -0.23215,
+          "hit": 0,
+          "round": 0
+        },
+        {
+          "candidate_index": 2145,
+          "gene": "CAPN5",
+          "score": -0.2056985,
+          "hit": 0,
+          "round": 0
+        }
+      ]
+    }
+  }
+}
```
