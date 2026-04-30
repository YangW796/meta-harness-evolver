# Change Record — candidate_5

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IL2/run-1/best/current/harness
Generated at: 2026-04-30T06:43:57.245032

## Files Changed

- model.py: modified (added=81, deleted=77, delta=4)
- outputs/metrics.json: modified (added=2427, deleted=635, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -28,11 +28,12 @@
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
 
     Strategy:
-    - If no history (round 1): random exploration
-    - If history exists: 70% exploitation (top scorers + similar genes), 30% exploration
-    - Uses gene search if available to find similar genes to high performers
+    - Thompson Sampling with Beta-Bernoulli model for hit probability
+    - Uses gene search to expand candidate pool for similar genes
+    - Naturally balances exploration vs exploitation through posterior sampling
     """
     rng = random.Random(seed)
+    np.random.seed(seed)
     
     # Get already selected indices
     already_selected = {h['candidate_index'] for h in history}
@@ -46,102 +47,105 @@
         selected = rng.sample(available_indices, min(batch_size, len(available_indices)))
         return selected
     
-    # Calculate scores for each candidate in history
-    candidate_scores = {}
+    # Build gene performance statistics
+    # Track hits and trials per gene
+    gene_stats = {}  # gene_name -> {'hits': int, 'trials': int}
+    
     for h in history:
         idx = h['candidate_index']
-        score = h.get('score', 0.0)
-        hit = h.get('hit', 0)
-        # Heavily prioritize hits - they are the target metric
-        # Use a large weight for hits (10x max expected score) plus the actual score
-        candidate_scores[idx] = score + (hit * 10.0)
+        candidate = candidates[idx]
+        
+        # Get gene name
+        if 'gene' in candidate:
+            gene = candidate['gene']
+        elif 'gene_a' in candidate:
+            gene = candidate['gene_a']
+        else:
+            continue
+        
+        if gene not in gene_stats:
+            gene_stats[gene] = {'hits': 0, 'trials': 0}
+        
+        gene_stats[gene]['trials'] += 1
+        if h.get('hit', 0) == 1:
+            gene_stats[gene]['hits'] += 1
     
-    # Sort candidates by score
-    sorted_history = sorted(history, key=lambda h: candidate_scores.get(h['candidate_index'], 0), reverse=True)
+    # Thompson Sampling: Sample hit probabilities from Beta posterior
+    # Prior: Beta(1, 1) which is uniform [0, 1]
+    # Posterior: Beta(1 + hits, 1 + trials - hits)
+    gene_sampled_probs = {}
     
-    # Strategy: 70% exploitation, 30% exploration
-    num_exploit = int(batch_size * 0.7)
-    num_explore = batch_size - num_exploit
+    for gene, stats in gene_stats.items():
+        hits = stats['hits']
+        trials = stats['trials']
+        # Sample from Beta posterior
+        sampled_prob = np.random.beta(1 + hits, 1 + trials - hits)
+        gene_sampled_probs[gene] = sampled_prob
     
-    selected = []
+    # Create candidate pool with Thompson Sampling scores
+    candidate_pool = []
     
-    # Exploitation: select top performers and their similar genes
-    exploit_pool = []
+    # Add candidates corresponding to tested genes with sampled probabilities
+    for h in history:
+        idx = h['candidate_index']
+        if idx not in available_indices:
+            continue
+        
+        candidate = candidates[idx]
+        if 'gene' in candidate:
+            gene = candidate['gene']
+        elif 'gene_a' in candidate:
+            gene = candidate['gene_a']
+        else:
+            continue
+        
+        if gene in gene_sampled_probs:
+            candidate_pool.append((idx, gene_sampled_probs[gene]))
     
-    # Add top 20% of historical candidates to exploitation pool
-    top_performers = [h['candidate_index'] for h in sorted_history[:max(1, len(sorted_history) // 5)]]
-    exploit_pool.extend(top_performers)
-    
-    # Try to use gene search to find similar genes
+    # Try to use gene search to expand pool with similar genes
     try:
         import bda_tools
-        gene_search_available = True
-    except ImportError:
-        gene_search_available = False
-    
-    if gene_search_available:
-        # Prioritize finding similar genes to HIT genes first
-        hit_genes = [h for h in sorted_history if h.get('hit', 0) == 1]
-        genes_to_search = hit_genes + sorted_history[:max(1, len(sorted_history) // 10)]
+        
+        # Sort genes by sampled probability (descending)
+        sorted_genes = sorted(gene_sampled_probs.items(), key=lambda x: x[1], reverse=True)
+        
+        # Search similar genes for top performers
         genes_seen = set()
-        
-        for h in genes_to_search:
-            idx = h['candidate_index']
-            candidate = candidates[idx]
-            
-            # Get gene name
-            if 'gene' in candidate:
-                gene = candidate['gene']
-            elif 'gene_a' in candidate:
-                gene = candidate['gene_a']
-            else:
-                continue
-            
-            # Avoid searching for the same gene multiple times
+        for gene, prob in sorted_genes[:max(10, len(sorted_genes) // 5)]:
             if gene in genes_seen:
                 continue
             genes_seen.add(gene)
             
-            # Search for similar genes
             try:
+                # Search for similar genes
                 similar_indices = bda_tools.gene_search(gene, k=10, diverse=False)
-                # Filter to available indices only (not yet selected)
-                similar_available = [i for i in similar_indices if i in available_indices and i not in exploit_pool and i not in selected]
-                # Only keep top 50% of similar genes to maintain quality
-                # Use the first half (higher-ranked by gene search)
-                keep_count = max(1, len(similar_available) // 2)
-                exploit_pool.extend(similar_available[:keep_count])
+                
+                # Assign Thompson Sampling score to similar genes
+                # Use the sampled probability of the query gene
+                for sim_idx in similar_indices:
+                    if sim_idx in available_indices and sim_idx not in [c[0] for c in candidate_pool]:
+                        candidate_pool.append((sim_idx, prob))
             except:
                 pass
+    except ImportError:
+        pass
     
-    # Remove duplicates and already selected
-    exploit_pool = [idx for idx in exploit_pool if idx in available_indices and idx not in selected]
+    # Sort candidate pool by Thompson Sampling score
+    candidate_pool.sort(key=lambda x: x[1], reverse=True)
     
-    # Sample from exploitation pool
-    if exploit_pool:
-        num_to_sample = min(num_exploit, len(exploit_pool))
-        selected.extend(rng.sample(exploit_pool, num_to_sample))
+    # Select top candidates from pool
+    selected = []
+    if candidate_pool:
+        # Take top candidates based on Thompson Sampling scores
+        num_from_pool = min(batch_size, len(candidate_pool))
+        selected = [idx for idx, _ in candidate_pool[:num_from_pool]]
     
-    # If we need more exploitation candidates, add more top performers
-    if len(selected) < num_exploit:
-        remaining_needed = num_exploit - len(selected)
-        top_available = [h['candidate_index'] for h in sorted_history 
-                        if h['candidate_index'] in available_indices and h['candidate_index'] not in selected]
-        if top_available:
-            num_to_add = min(remaining_needed, len(top_available))
-            selected.extend(rng.sample(top_available, num_to_add))
-    
-    # Exploration: random sampling from remaining available indices
-    remaining_available = [idx for idx in available_indices if idx not in selected]
-    if remaining_available and num_explore > 0:
-        num_to_explore = min(num_explore, len(remaining_available))
-        selected.extend(rng.sample(remaining_available, num_to_explore))
-    
-    # If we still don't have enough, fill with any available
+    # If we need more candidates, add random exploration
     if len(selected) < batch_size:
-        still_available = [idx for idx in available_indices if idx not in selected]
-        if still_available:
+        remaining_available = [idx for idx in available_indices if idx not in selected]
+        if remaining_available:
             num_needed = batch_size - len(selected)
-            selected.extend(rng.sample(still_available, min(num_needed, len(still_available))))
+            num_to_add = min(num_needed, len(remaining_available))
+            selected.extend(rng.sample(remaining_available, num_to_add))
     
     return selected[:batch_size]
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
-      "baseline_total_hits": 8,
+      "baseline_total_queries": 384,
+      "baseline_total_hits": 10,
       "delta_queries": 128,
-      "delta_hits": 2,
-      "total_queries": 384,
-      "total_hits": 10,
+      "delta_hits": 6,
+      "total_queries": 512,
+      "total_hits": 16,
       "top_k": 654,
       "hit_curve": {
         "queries": [
-          256,
-          384
+          384,
+          512
         ],
         "hits": [
-          8,
-          10
+          10,
+          16
         ]
       },
-      "auc": 1152.0,
-      "auc_normalized": 0.0045871559633027525,
-      "ncg": 0.1647511167553707,
+      "auc": 1664.0,
+      "auc_normalized": 0.004969418960244648,
+      "ncg": 0.18646904838310088,
       "round_details": [
         {
-          "round": 2,
+          "round": 3,
           "selected_count": 128,
-          "hits": 2,
-          "cumulative_hits": 10,
-          "precision_at_batch": 0.015625,
+          "hits": 6,
+          "cumulative_hits": 16,
+          "precision_at_batch": 0.046875,
           "selected": [
-            "C1orf158",
-            "DTX3",
-            "PYCR1",
-            "ANKRD1",
-            "ANXA7",
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
-            "BOLA1",
-            "ZNF773",
-            "COA6",
-            "GRK6",
-            "HACD3",
-            "GPBP1",
-            "ELF4",
-            "MACF1",
-            "NDUFA13",
-            "TSKS",
-            "GBA",
-            "CHORDC1",
-            "SMIM19",
-            "WDR64",
-            "EPHX2",
-            "IFITM2",
-            "VSTM2A",
-            "TTC39B",
-            "HLA-DPB1",
-            "CXCR2",
-            "STUB1",
-            "SAFB",
-            "TCP10L2",
-            "SUV39H1",
-            "MED6",
-            "ATP6V1D",
-            "WDR88",
-            "CEACAM3",
-            "TSPO",
-            "KCNN4",
-            "PLCG2",
-            "ADH6",
-            "LBP",
-            "GRINA",
-            "WDR3",
-            "PDE8B",
-            "PRKACA",
-            "PRKN",
-            "PANX3",
-            "RGPD4",
-            "G2E3",
-            "ORC1",
-            "CLEC7A",
-            "SCARF2",
-            "SULT1B1",
-            "LARS2",
-            "OR5I1",
-            "PYHIN1",
-            "ZNF761",
-            "SPAG6",
-            "ZNF703",
-            "SLC24A5",
-            "SH2D4A",
-            "NOMO1",
-            "OR14A16",
-            "ZNF330",
-            "SSTR4",
-            "OR13J1",
-            "TRIM34",
-            "TMEM225B",
-            "RHBDL1",
-            "LIMD2",
-            "SNAI1",
-            "CA5A",
-            "STARD4",
-            "TRIM31",
-            "PRAMEF14",
-            "RPA2",
-            "LHB",
-            "OR10G4",
-            "BCL11A",
-            "SNAP23",
-            "CSPG4",
-            "B3GNT6",
-            "TGIF2-C20orf24",
-            "SYT17",
-            "TUBGCP3",
-            "CLVS2",
-            "BRWD3",
-            "OR52L1",
-            "B4GALT6",
-            "KRT71",
-            "PSIP1",
-            "LRG1",
-            "ENTPD5",
-            "NPB",
-            "CACNA1D",
-            "DACT1",
-            "CADM2",
-            "NRN1",
-            "OR2AE1",
-            "YLPM1",
-            "MFSD2A",
-            "DFFA",
-            "BID"
+            "ZNF682",
+            "SUGP1",
+            "MFSD3",
+            "NSMCE1",
+            "PRR21",
+            "KCND2",
+            "TSPOAP1",
+            "ZXDB",
+            "PCM1",
+            "SOCS4",
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
+            "TNFRSF11B",
+            "KRTAP10-1",
+            "HLA-A",
+            "HBD",
+            "GNMT",
+            "HEATR9",
+            "AFTPH",
+            "DIO2",
+            "HSDL1",
+            "OR4D2",
+            "SDR39U1",
+            "SPINT3",
+            "OR52A5",
+            "MTRNR2L5",
+            "UBE2M",
+            "CD1D",
+            "C2CD6",
+            "IFT27",
+            "TRIM37",
+            "CCL28",
+            "NPY2R",
+            "AWAT1",
+            "PCNT",
+            "ABCC3",
+            "HIST1H2AI",
+            "ABCB8",
+            "C3orf36",
+            "CHRM1",
+            "DTL",
+            "PSME3",
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
+            "CTDSPL2",
+            "VWA1",
+            "C4orf33",
+            "NCAPD2",
+            "LOC100130705",
+            "COPS4",
+            "CSF2",
+            "SLC39A9",
+            "CREBRF",
+            "CHIT1",
+            "FAM133A",
+            "CEP120",
+            "RNF146",
+            "TOMM22",
+            "DMP1",
+            "NLRP3",
+            "ASB14",
+            "FLVCR2",
+            "FOXA2",
+            "PPM1M",
+            "MRGPRE",
+            "OCIAD1",
+            "CD40LG",
+            "CCDC102A",
+            "TNNI3",
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
+            "ATF6",
+            "ARHGAP17",
+            "RNASE7",
+            "SIGLEC14",
+            "AQP12A",
+            "ACTN1",
+            "XIAP",
+            "MRPS15",
+            "ZFP57",
+            "NDUFB10",
+            "ZFYVE16",
+            "ZNF324B",
+            "ZIM3",
+            "PSMB9",
+            "ZNF513",
+            "CALU",
+            "BSPH1",
+            "LIPC",
+            "FAM183A",
+            "EPO",
+            "HEPHL1",
+            "BCAP31",
+            "BIRC2",
+            "NUP210L",
+            "SLC39A2",
+            "KNDC1",
+            "PTPRC",
+            "OR7C1",
+            "PCYT2"
           ],
           "selected_scores": [
-            0.097043,
-            0.038861,
-            0.06193,
-            -0.0057194,
-            -0.026024,
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
-            -0.00089316,
-            0.045895,
-            -0.18267,
-            0.08963,
-            0.1045,
-            -0.090071,
-            -0.18139,
-            -0.11163,
-            0.014495,
-            -0.090791,
-            -0.23715,
-            -0.0047188,
-            0.091257,
-            -0.046877,
-            0.22395,
-            0.11283,
-            0.065186,
-            -0.047559,
-            -0.08977,
-            0.067021,
-            -0.067023,
-            0.19949,
-            0.19728,
-            -0.018781,
-            -0.164,
-            -0.031837,
-            -0.08229,
-            0.097253,
-            -0.094768,
-            -0.236,
-            0.042606,
-            0.10784,
-            0.1237,
-            -0.14135,
-            0.33659,
-            0.049945,
-            -0.0045085,
-            0.093661,
-            0.10517,
-            0.08214,
-            -0.20105,
-            -0.11196,
-            -0.16276,
-            -0.046342,
-            -0.19371,
-            0.09608,
-            -0.11676,
-            -0.04228,
-            -0.079377,
-            -0.19942,
-            -0.1523,
-            0.062797,
-            -0.0058831,
-            -0.0093454,
-            -0.12285,
-            0.12166,
-            0.097402,
-            -0.064619,
-            0.062544,
-            0.033022,
-            -0.030375,
-            -0.026979,
-            -0.061154,
-            0.12589,
-            0.053657,
-            0.054297,
-            -0.099496,
-            0.20762,
-            0.086577,
-            -0.23147,
-            -0.077921,
-            0.18266,
-            -0.022444,
-            0.047247,
-            0.14962,
-            0.040779,
-            0.41857,
-            0.0028453,
-            -0.2053,
-            0.054894,
-            -0.11599,
-            0.12077,
-            0.021862,
-            -0.094189,
-            -0.050377,
-            -0.020113,
-            0.071356,
-            0.10007,
-            -0.081387,
-            0.05283,
-            -0.038128,
-            -0.029124,
-            -0.012017,
-            0.24165,
-            0.14308
+            -0.066292,
+            -0.10537,
+            0.080117,
+            0.10446,
+            -0.045793,
+            -0.039075,
+            -0.023655,
+            -0.22122,
+            -0.14485,
+            0.073544,
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
+            -0.044209,
+            -0.13763,
+            0.03841,
+            -0.11022,
+            0.021289,
+            -0.11612,
+            -0.23038,
+            0.21103,
+            -0.08225,
+            0.22436,
+            -0.049585,
+            -0.092487,
+            -0.010455,
+            -0.060609,
+            -0.25676,
+            -0.1676,
+            0.029571,
+            0.049569,
+            0.07034,
+            0.11867,
+            0.020643,
+            -0.17269,
+            0.27061,
+            0.10402,
+            -0.093945,
+            -0.05807,
+            -0.17073,
+            -0.038634,
+            0.062116,
+            -0.0026347,
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
+            0.42383,
+            0.093404,
+            -0.24117,
+            0.43568,
+            -0.2275,
+            -0.0042149,
+            0.0052531,
+            -0.019225,
+            0.067736,
+            -0.10366,
+            -0.13119,
+            -0.083101,
+            -0.33644,
+            -0.050375,
+            -0.16108,
+            0.20612,
+            -0.029937,
+            0.11643,
+            -0.06962,
+            0.066489,
+            0.069416,
+            -0.025822,
+            -0.022008,
+            -0.1765,
+            0.028936,
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
+            -0.080113,
+            0.10559,
+            -0.1516,
+            -0.036235,
+            -0.14952,
+            0.055767,
+            -0.062923,
+            0.14946,
+            -0.035847,
+            0.27002,
+            -0.0051672,
+            0.051283,
+            0.049688,
+            0.025062,
+            0.050747,
+            -0.14609,
+            -0.027673,
+            0.0011676,
+            0.085677,
+            -0.017593,
+            0.083083,
+            0.0062327,
+            0.027505,
+            -0.10562,
+            0.12401,
+            0.11623,
+            -0.86005,
+            0.084699,
+            -0.32403
           ],
           "selected_hits": [
             0,
@@ -311,105 +311,60 @@
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
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
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
@@ -419,16 +374,61 @@
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
-            0
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
           "candidate_index": 5881,
           "gene": "ANXA7",
           "score": -0.026024,
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
           "candidate_index": 11453,
           "gene": "BOLA1",
           "score": -0.00089316,
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
           "candidate_index": 6293,
           "gene": "ELF4",
           "score": -0.18139,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4345,
           "gene": "MACF1",
           "score": -0.11163,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8608,
           "gene": "NDUFA13",
           "score": 0.014495,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8267,
           "gene": "TSKS",
           "score": -0.090791,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1635,
           "gene": "GBA",
           "score": -0.23715,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1443,
           "gene": "CHORDC1",
           "score": -0.0047188,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14537,
           "gene": "SMIM19",
           "score": 0.091257,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1256,
           "gene": "WDR64",
           "score": -0.046877,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10948,
           "gene": "EPHX2",
           "score": 0.22395,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12310,
           "gene": "IFITM2",
           "score": 0.11283,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15682,
           "gene": "VSTM2A",
           "score": 0.065186,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15111,
           "gene": "TTC39B",
           "score": -0.047559,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17995,
           "gene": "HLA-DPB1",
           "score": -0.08977,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5025,
           "gene": "CXCR2",
           "score": 0.067021,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7781,
           "gene": "STUB1",
           "score": -0.067023,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16096,
           "gene": "SAFB",
           "score": 0.19949,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15178,
           "gene": "TCP10L2",
           "score": 0.19728,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11524,
           "gene": "SUV39H1",
           "score": -0.018781,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1449,
           "gene": "MED6",
           "score": -0.164,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9267,
           "gene": "ATP6V1D",
           "score": -0.031837,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5251,
           "gene": "WDR88",
           "score": -0.08229,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 307,
           "gene": "CEACAM3",
           "score": 0.097253,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7443,
           "gene": "TSPO",
           "score": -0.094768,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 482,
           "gene": "KCNN4",
           "score": -0.236,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18510,
           "gene": "PLCG2",
           "score": 0.042606,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18085,
           "gene": "ADH6",
           "score": 0.10784,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9390,
           "gene": "LBP",
           "score": 0.1237,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11882,
           "gene": "GRINA",
           "score": -0.14135,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18757,
           "gene": "WDR3",
           "score": 0.33659,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6640,
           "gene": "PDE8B",
           "score": 0.049945,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13480,
           "gene": "PRKACA",
           "score": -0.0045085,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3726,
           "gene": "PRKN",
           "score": 0.093661,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12025,
           "gene": "PANX3",
           "score": 0.10517,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11332,
           "gene": "RGPD4",
           "score": 0.08214,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3756,
           "gene": "G2E3",
           "score": -0.20105,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7464,
           "gene": "ORC1",
           "score": -0.11196,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1970,
           "gene": "CLEC7A",
           "score": -0.16276,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14434,
           "gene": "SCARF2",
           "score": -0.046342,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1594,
           "gene": "SULT1B1",
           "score": -0.19371,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15783,
           "gene": "LARS2",
           "score": 0.09608,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4091,
           "gene": "OR5I1",
           "score": -0.11676,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4764,
           "gene": "PYHIN1",
           "score": -0.04228,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5987,
           "gene": "ZNF761",
           "score": -0.079377,
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
           "candidate_index": 9790,
           "gene": "ZNF703",
           "score": -0.1523,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2101,
           "gene": "SLC24A5",
           "score": 0.062797,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9069,
           "gene": "SH2D4A",
           "score": -0.0058831,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2480,
           "gene": "NOMO1",
           "score": -0.0093454,
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
           "candidate_index": 14500,
           "gene": "ZNF330",
           "score": 0.12166,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9134,
           "gene": "SSTR4",
           "score": 0.097402,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5953,
           "gene": "OR13J1",
           "score": -0.064619,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17433,
           "gene": "TRIM34",
           "score": 0.062544,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6429,
           "gene": "TMEM225B",
           "score": 0.033022,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2024,
           "gene": "RHBDL1",
           "score": -0.030375,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9313,
           "gene": "LIMD2",
           "score": -0.026979,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16086,
           "gene": "SNAI1",
           "score": -0.061154,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8752,
           "gene": "CA5A",
           "score": 0.12589,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2160,
           "gene": "STARD4",
           "score": 0.053657,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17053,
           "gene": "TRIM31",
           "score": 0.054297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10990,
           "gene": "PRAMEF14",
           "score": -0.099496,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18190,
           "gene": "RPA2",
           "score": 0.20762,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16235,
           "gene": "LHB",
           "score": 0.086577,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2179,
           "gene": "OR10G4",
           "score": -0.23147,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9471,
           "gene": "BCL11A",
           "score": -0.077921,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16349,
           "gene": "SNAP23",
           "score": 0.18266,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9995,
           "gene": "CSPG4",
           "score": -0.022444,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13368,
           "gene": "B3GNT6",
           "score": 0.047247,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13432,
           "gene": "TGIF2-C20orf24",
           "score": 0.14962,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10069,
           "gene": "SYT17",
           "score": 0.040779,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18215,
           "gene": "TUBGCP3",
           "score": 0.41857,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14982,
           "gene": "CLVS2",
           "score": 0.0028453,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2424,
           "gene": "BRWD3",
           "score": -0.2053,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10575,
           "gene": "OR52L1",
           "score": 0.054894,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8404,
           "gene": "B4GALT6",
           "score": -0.11599,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4399,
           "gene": "KRT71",
           "score": 0.12077,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4420,
           "gene": "PSIP1",
           "score": 0.021862,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4422,
           "gene": "LRG1",
           "score": -0.094189,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2477,
           "gene": "ENTPD5",
           "score": -0.050377,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14711,
           "gene": "NPB",
           "score": -0.020113,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13196,
           "gene": "CACNA1D",
           "score": 0.071356,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11501,
           "gene": "DACT1",
           "score": 0.10007,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14772,
           "gene": "CADM2",
           "score": -0.081387,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2805,
           "gene": "NRN1",
           "score": 0.05283,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9138,
           "gene": "OR2AE1",
           "score": -0.038128,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4458,
           "gene": "YLPM1",
           "score": -0.029124,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9287,
           "gene": "MFSD2A",
           "score": -0.012017,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17758,
           "gene": "DFFA",
           "score": 0.24165,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16752,
           "gene": "BID",
           "score": 0.14308,
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
+          "candidate_index": 16325,
+          "gene": "MFSD3",
+          "score": 0.080117,
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
+          "candidate_index": 10156,
+          "gene": "KCND2",
+          "score": -0.039075,
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
+          "candidate_index": 16201,
+          "gene": "SOCS4",
+          "score": 0.073544,
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
+          "candidate_index": 14339,
+          "gene": "TNFRSF11B",
+          "score": -0.044209,
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
+          "candidate_index": 11938,
+          "gene": "OR4D2",
+          "score": 0.22436,
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
+          "candidate_index": 17750,
+          "gene": "TRIM37",
+          "score": 0.07034,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17958,
+          "gene": "CCL28",
+          "score": 0.11867,
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
+          "candidate_index": 1999,
+          "gene": "AWAT1",
+          "score": -0.17269,
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
+          "candidate_index": 16726,
+          "gene": "PSME3",
+          "score": -0.0026347,
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
+          "candidate_index": 18735,
+          "gene": "CTDSPL2",
+          "score": 0.42383,
+          "hit": 1,
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
+          "candidate_index": 17231,
+          "gene": "NCAPD2",
+          "score": 0.43568,
+          "hit": 1,
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
+          "candidate_index": 18174,
+          "gene": "COPS4",
+          "score": -0.0042149,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17411,
+          "gene": "CSF2",
+          "score": 0.0052531,
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
+          "candidate_index": 6132,
+          "gene": "CEP120",
+          "score": -0.083101,
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
+          "candidate_index": 14697,
+          "gene": "OCIAD1",
+          "score": -0.025822,
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
+          "candidate_index": 9066,
+          "gene": "TNNI3",
+          "score": 0.028936,
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
+          "candidate_index": 3072,
+          "gene": "ATF6",
+          "score": -0.080113,
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
+          "candidate_index": 14953,
+          "gene": "XIAP",
+          "score": -0.062923,
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
+          "candidate_index": 13469,
+          "gene": "ZFYVE16",
+          "score": -0.0051672,
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
+          "candidate_index": 17578,
+          "gene": "PSMB9",
+          "score": 0.025062,
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
+          "candidate_index": 2421,
+          "gene": "CALU",
+          "score": -0.14609,
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
+          "candidate_index": 17402,
+          "gene": "SLC39A2",
+          "score": 0.12401,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18020,
+          "gene": "KNDC1",
+          "score": 0.11623,
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
           "candidate_index": 5881,
           "gene": "ANXA7",
           "score": -0.026024,
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
           "candidate_index": 11453,
           "gene": "BOLA1",
           "score": -0.00089316,
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
           "candidate_index": 6293,
           "gene": "ELF4",
           "score": -0.18139,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4345,
           "gene": "MACF1",
           "score": -0.11163,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8608,
           "gene": "NDUFA13",
           "score": 0.014495,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8267,
           "gene": "TSKS",
           "score": -0.090791,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1635,
           "gene": "GBA",
           "score": -0.23715,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1443,
           "gene": "CHORDC1",
           "score": -0.0047188,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14537,
           "gene": "SMIM19",
           "score": 0.091257,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1256,
           "gene": "WDR64",
           "score": -0.046877,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10948,
           "gene": "EPHX2",
           "score": 0.22395,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12310,
           "gene": "IFITM2",
           "score": 0.11283,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15682,
           "gene": "VSTM2A",
           "score": 0.065186,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15111,
           "gene": "TTC39B",
           "score": -0.047559,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17995,
           "gene": "HLA-DPB1",
           "score": -0.08977,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5025,
           "gene": "CXCR2",
           "score": 0.067021,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7781,
           "gene": "STUB1",
           "score": -0.067023,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16096,
           "gene": "SAFB",
           "score": 0.19949,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15178,
           "gene": "TCP10L2",
           "score": 0.19728,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11524,
           "gene": "SUV39H1",
           "score": -0.018781,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1449,
           "gene": "MED6",
           "score": -0.164,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9267,
           "gene": "ATP6V1D",
           "score": -0.031837,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5251,
           "gene": "WDR88",
           "score": -0.08229,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 307,
           "gene": "CEACAM3",
           "score": 0.097253,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7443,
           "gene": "TSPO",
           "score": -0.094768,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 482,
           "gene": "KCNN4",
           "score": -0.236,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18510,
           "gene": "PLCG2",
           "score": 0.042606,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18085,
           "gene": "ADH6",
           "score": 0.10784,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9390,
           "gene": "LBP",
           "score": 0.1237,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11882,
           "gene": "GRINA",
           "score": -0.14135,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18757,
           "gene": "WDR3",
           "score": 0.33659,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6640,
           "gene": "PDE8B",
           "score": 0.049945,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13480,
           "gene": "PRKACA",
           "score": -0.0045085,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3726,
           "gene": "PRKN",
           "score": 0.093661,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12025,
           "gene": "PANX3",
           "score": 0.10517,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11332,
           "gene": "RGPD4",
           "score": 0.08214,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3756,
           "gene": "G2E3",
           "score": -0.20105,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7464,
           "gene": "ORC1",
           "score": -0.11196,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1970,
           "gene": "CLEC7A",
           "score": -0.16276,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14434,
           "gene": "SCARF2",
           "score": -0.046342,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1594,
           "gene": "SULT1B1",
           "score": -0.19371,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15783,
           "gene": "LARS2",
           "score": 0.09608,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4091,
           "gene": "OR5I1",
           "score": -0.11676,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4764,
           "gene": "PYHIN1",
           "score": -0.04228,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5987,
           "gene": "ZNF761",
           "score": -0.079377,
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
           "candidate_index": 9790,
           "gene": "ZNF703",
           "score": -0.1523,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2101,
           "gene": "SLC24A5",
           "score": 0.062797,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9069,
           "gene": "SH2D4A",
           "score": -0.0058831,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2480,
           "gene": "NOMO1",
           "score": -0.0093454,
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
           "candidate_index": 14500,
           "gene": "ZNF330",
           "score": 0.12166,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9134,
           "gene": "SSTR4",
           "score": 0.097402,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5953,
           "gene": "OR13J1",
           "score": -0.064619,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17433,
           "gene": "TRIM34",
           "score": 0.062544,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6429,
           "gene": "TMEM225B",
           "score": 0.033022,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2024,
           "gene": "RHBDL1",
           "score": -0.030375,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9313,
           "gene": "LIMD2",
           "score": -0.026979,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16086,
           "gene": "SNAI1",
           "score": -0.061154,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8752,
           "gene": "CA5A",
           "score": 0.12589,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2160,
           "gene": "STARD4",
           "score": 0.053657,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17053,
           "gene": "TRIM31",
           "score": 0.054297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10990,
           "gene": "PRAMEF14",
           "score": -0.099496,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18190,
           "gene": "RPA2",
           "score": 0.20762,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16235,
           "gene": "LHB",
           "score": 0.086577,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2179,
           "gene": "OR10G4",
           "score": -0.23147,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9471,
           "gene": "BCL11A",
           "score": -0.077921,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16349,
           "gene": "SNAP23",
           "score": 0.18266,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9995,
           "gene": "CSPG4",
           "score": -0.022444,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13368,
           "gene": "B3GNT6",
           "score": 0.047247,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13432,
           "gene": "TGIF2-C20orf24",
           "score": 0.14962,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10069,
           "gene": "SYT17",
           "score": 0.040779,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18215,
           "gene": "TUBGCP3",
           "score": 0.41857,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14982,
           "gene": "CLVS2",
           "score": 0.0028453,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2424,
           "gene": "BRWD3",
           "score": -0.2053,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10575,
           "gene": "OR52L1",
           "score": 0.054894,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8404,
           "gene": "B4GALT6",
           "score": -0.11599,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4399,
           "gene": "KRT71",
           "score": 0.12077,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4420,
           "gene": "PSIP1",
           "score": 0.021862,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4422,
           "gene": "LRG1",
           "score": -0.094189,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2477,
           "gene": "ENTPD5",
           "score": -0.050377,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14711,
           "gene": "NPB",
           "score": -0.020113,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13196,
           "gene": "CACNA1D",
           "score": 0.071356,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11501,
           "gene": "DACT1",
           "score": 0.10007,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14772,
           "gene": "CADM2",
           "score": -0.081387,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2805,
           "gene": "NRN1",
           "score": 0.05283,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9138,
           "gene": "OR2AE1",
           "score": -0.038128,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4458,
           "gene": "YLPM1",
           "score": -0.029124,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9287,
           "gene": "MFSD2A",
           "score": -0.012017,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17758,
           "gene": "DFFA",
           "score": 0.24165,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16752,
           "gene": "BID",
           "score": 0.14308,
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
+          "candidate_index": 16325,
+          "gene": "MFSD3",
+          "score": 0.080117,
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
+          "candidate_index": 10156,
+          "gene": "KCND2",
+          "score": -0.039075,
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
+          "candidate_index": 16201,
+          "gene": "SOCS4",
+          "score": 0.073544,
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
+          "candidate_index": 14339,
+          "gene": "TNFRSF11B",
+          "score": -0.044209,
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
+          "candidate_index": 11938,
+          "gene": "OR4D2",
+          "score": 0.22436,
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
+          "candidate_index": 17750,
+          "gene": "TRIM37",
+          "score": 0.07034,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17958,
+          "gene": "CCL28",
+          "score": 0.11867,
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
+          "candidate_index": 1999,
+          "gene": "AWAT1",
+          "score": -0.17269,
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
+          "candidate_index": 16726,
+          "gene": "PSME3",
+          "score": -0.0026347,
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
+          "candidate_index": 18735,
+          "gene": "CTDSPL2",
+          "score": 0.42383,
+          "hit": 1,
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
+          "candidate_index": 17231,
+          "gene": "NCAPD2",
+          "score": 0.43568,
+          "hit": 1,
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
+          "candidate_index": 18174,
+          "gene": "COPS4",
+          "score": -0.0042149,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17411,
+          "gene": "CSF2",
+          "score": 0.0052531,
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
+          "candidate_index": 6132,
+          "gene": "CEP120",
+          "score": -0.083101,
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
+          "candidate_index": 14697,
+          "gene": "OCIAD1",
+          "score": -0.025822,
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
+          "candidate_index": 9066,
+          "gene": "TNNI3",
+          "score": 0.028936,
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
+          "candidate_index": 3072,
+          "gene": "ATF6",
+          "score": -0.080113,
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
+          "candidate_index": 14953,
+          "gene": "XIAP",
+          "score": -0.062923,
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
+          "candidate_index": 13469,
+          "gene": "ZFYVE16",
+          "score": -0.0051672,
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
+          "candidate_index": 17578,
+          "gene": "PSMB9",
+          "score": 0.025062,
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
+          "candidate_index": 2421,
+          "gene": "CALU",
+          "score": -0.14609,
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
+          "candidate_index": 17402,
+          "gene": "SLC39A2",
+          "score": 0.12401,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18020,
+          "gene": "KNDC1",
+          "score": 0.11623,
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
