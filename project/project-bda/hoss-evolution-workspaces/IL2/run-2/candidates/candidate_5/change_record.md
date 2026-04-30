# Change Record — candidate_5

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IL2/run-2/best/current/harness
Generated at: 2026-04-30T07:09:50.436005

## Files Changed

- model.py: modified (added=130, deleted=91, delta=39)
- outputs/metrics.json: modified (added=2392, deleted=600, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -28,10 +28,11 @@
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
 
     Strategy:
-    - Thompson Sampling with Beta-Bernoulli model for hit probability
-    - Uses gene search to expand candidate pool for similar genes
-    - Incorporates continuous score information for better prioritization
-    - Naturally balances exploration vs exploitation through posterior sampling
+    - Evolutionary Strategy (ES) approach for gene selection
+    - Maintains a population of promising genes based on fitness (score magnitude)
+    - Uses mutation (gene search for similar genes) to explore neighborhood
+    - Uses selection pressure to focus on high-fitness regions
+    - Balances exploration (new genes) vs exploitation (known good gene families)
     """
     rng = random.Random(seed)
     np.random.seed(seed)
@@ -48,9 +49,9 @@
         selected = rng.sample(available_indices, min(batch_size, len(available_indices)))
         return selected
     
-    # Build gene performance statistics
-    # Track hits, trials, and score statistics per gene
-    gene_stats = {}  # gene_name -> {'hits': int, 'trials': int, 'sum_score': float, 'max_score': float}
+    # Build gene fitness scores based on extreme values (both positive and negative)
+    # Fitness = absolute score magnitude (we care about extreme effects in either direction)
+    gene_fitness = {}  # gene_name -> {'fitness': float, 'count': int, 'indices': list[int]}
     
     for h in history:
         idx = h['candidate_index']
@@ -64,106 +65,144 @@
         else:
             continue
         
-        if gene not in gene_stats:
-            gene_stats[gene] = {'hits': 0, 'trials': 0, 'sum_score': 0.0, 'max_score': -float('inf')}
-        
-        gene_stats[gene]['trials'] += 1
         score = h.get('score', 0.0)
-        gene_stats[gene]['sum_score'] += score
-        gene_stats[gene]['max_score'] = max(gene_stats[gene]['max_score'], score)
-        if h.get('hit', 0) == 1:
-            gene_stats[gene]['hits'] += 1
-    
-    # Thompson Sampling: Sample hit probabilities from Beta posterior
-    # Prior: Beta(1, 1) which is uniform [0, 1]
-    # Posterior: Beta(1 + hits, 1 + trials - hits)
-    gene_sampled_probs = {}
-    
-    for gene, stats in gene_stats.items():
-        hits = stats['hits']
-        trials = stats['trials']
-        # Sample from Beta posterior
-        sampled_prob = np.random.beta(1 + hits, 1 + trials - hits)
-        
-        # Boost probability for genes with extreme scores (both positive and negative)
-        # Hits can be extreme in either direction, so we want to pursue both
-        avg_score = stats['sum_score'] / trials
-        max_score = stats['max_score']
-        
-        # Boost based on average score (consistent behavior)
-        if avg_score > 0.1:  # Boost genes with positive average scores
-            sampled_prob *= (1.0 + avg_score)
-        elif avg_score < -0.2:  # Boost genes with strongly negative scores (potential hits)
-            sampled_prob *= (1.0 + abs(avg_score))
-        
-        # Additionally boost genes that have shown extreme values (high max_score)
-        # This helps find hits even when the average is moderate
-        if max_score > 0.3:  # Gene has shown strongly positive behavior at least once
-            sampled_prob *= (1.0 + 0.3 * max_score)
-        elif max_score < -0.3:  # Gene has shown strongly negative behavior at least once
-            sampled_prob *= (1.0 + 0.3 * abs(max_score))
-        
-        gene_sampled_probs[gene] = min(sampled_prob, 1.0)  # Cap at 1.0
-    
-    # Create candidate pool with Thompson Sampling scores
-    candidate_pool = []
-    
-    # Add candidates corresponding to tested genes with sampled probabilities
-    for h in history:
-        idx = h['candidate_index']
-        if idx not in available_indices:
-            continue
-        
-        candidate = candidates[idx]
-        if 'gene' in candidate:
-            gene = candidate['gene']
-        elif 'gene_a' in candidate:
-            gene = candidate['gene_a']
-        else:
-            continue
-        
-        if gene in gene_sampled_probs:
-            candidate_pool.append((idx, gene_sampled_probs[gene]))
-    
-    # Try to use gene search to expand pool with similar genes
+        # Use absolute score as fitness (extreme values in either direction are interesting)
+        fitness = abs(score)
+        
+        if gene not in gene_fitness:
+            gene_fitness[gene] = {'fitness': 0.0, 'count': 0, 'indices': []}
+        
+        # Accumulate fitness (could use max, sum, or weighted average)
+        # Using max to prioritize genes that have shown extreme behavior
+        gene_fitness[gene]['fitness'] = max(gene_fitness[gene]['fitness'], fitness)
+        gene_fitness[gene]['count'] += 1
+        gene_fitness[gene]['indices'].append(idx)
+    
+    # Sort genes by fitness (descending)
+    sorted_genes = sorted(gene_fitness.items(), key=lambda x: x[1]['fitness'], reverse=True)
+    
+    # Evolutionary Strategy: Select parents and generate offspring
+    selected = []
+    
+    # Phase 1: Exploitation - Select top-performing genes (elite selection)
+    # Take top 20% of genes as "parents"
+    num_parents = max(5, len(sorted_genes) // 5)
+    parents = sorted_genes[:num_parents]
+    
+    for gene, data in parents:
+        # Add the actual tested indices that are still available
+        for idx in data['indices']:
+            if idx in available_indices and idx not in selected:
+                selected.append(idx)
+                if len(selected) >= batch_size // 2:  # Reserve half for exploration
+                    break
+        if len(selected) >= batch_size // 2:
+            break
+    
+    # Phase 2: Mutation - Use gene search to find similar genes to top performers
     try:
         import bda_tools
         
-        # Sort genes by sampled probability (descending)
-        sorted_genes = sorted(gene_sampled_probs.items(), key=lambda x: x[1], reverse=True)
-        
-        # Search similar genes for top performers
         genes_seen = set()
-        for gene, prob in sorted_genes[:max(10, len(sorted_genes) // 5)]:
+        for gene, data in parents[:max(3, len(parents) // 2)]:  # Top 50% of parents
             if gene in genes_seen:
                 continue
             genes_seen.add(gene)
             
             try:
-                # Search for similar genes
-                similar_indices = bda_tools.gene_search(gene, k=10, diverse=False)
-                
-                # Assign Thompson Sampling score to similar genes
-                # Use the sampled probability of the query gene
+                # Search for similar genes (mutation with small perturbation)
+                similar_indices = bda_tools.gene_search(gene, k=15, diverse=False)
+                
+                # Add similar genes that haven't been selected
                 for sim_idx in similar_indices:
-                    if sim_idx in available_indices and sim_idx not in [c[0] for c in candidate_pool]:
-                        candidate_pool.append((sim_idx, prob))
+                    if sim_idx in available_indices and sim_idx not in selected:
+                        selected.append(sim_idx)
+                        if len(selected) >= batch_size * 3 // 4:  # Reserve 75% total
+                            break
+                    if len(selected) >= batch_size * 3 // 4:
+                        break
             except:
                 pass
+            
+            if len(selected) >= batch_size * 3 // 4:
+                break
     except ImportError:
         pass
     
-    # Sort candidate pool by Thompson Sampling score
-    candidate_pool.sort(key=lambda x: x[1], reverse=True)
-    
-    # Select top candidates from pool
-    selected = []
-    if candidate_pool:
-        # Take top candidates based on Thompson Sampling scores
-        num_from_pool = min(batch_size, len(candidate_pool))
-        selected = [idx for idx, _ in candidate_pool[:num_from_pool]]
-    
-    # If we need more candidates, add random exploration
+    # Phase 3: Exploration - Add diverse genes to maintain population diversity
+    try:
+        import bda_tools
+        
+        # For top 2-3 parents, also search for DIVERSE genes (exploration)
+        genes_seen_diverse = set()
+        for gene, data in parents[:min(3, len(parents))]:
+            if gene in genes_seen_diverse:
+                continue
+            genes_seen_diverse.add(gene)
+            
+            try:
+                # Search for diverse genes (explore different regions)
+                diverse_indices = bda_tools.gene_search(gene, k=10, diverse=True)
+                
+                for div_idx in diverse_indices:
+                    if div_idx in available_indices and div_idx not in selected:
+                        selected.append(div_idx)
+                        if len(selected) >= batch_size - 10:  # Leave room for random
+                            break
+                    if len(selected) >= batch_size - 10:
+                        break
+            except:
+                pass
+            
+            if len(selected) >= batch_size - 10:
+                break
+    except ImportError:
+        pass
+    
+    # Phase 4: Fill remaining slots with random genes from high-fitness families
+    if len(selected) < batch_size:
+        # Create a probability distribution based on gene fitness
+        remaining_available = [idx for idx in available_indices if idx not in selected]
+        
+        if remaining_available:
+            # Score remaining candidates by their gene family fitness
+            candidate_scores = []
+            for idx in remaining_available:
+                candidate = candidates[idx]
+                if 'gene' in candidate:
+                    gene = candidate['gene']
+                elif 'gene_a' in candidate:
+                    gene = candidate['gene_a']
+                else:
+                    gene = None
+                
+                if gene and gene in gene_fitness:
+                    score = gene_fitness[gene]['fitness']
+                else:
+                    # Give unknown genes a small chance
+                    score = 0.01
+                
+                candidate_scores.append((idx, score))
+            
+            # Sample with probability proportional to fitness
+            num_needed = batch_size - len(selected)
+            if candidate_scores:
+                indices, scores = zip(*candidate_scores)
+                scores = np.array(scores)
+                # Add small epsilon to avoid division by zero
+                scores = scores + 0.01
+                probs = scores / scores.sum()
+                
+                # Sample without replacement
+                sampled_indices = np.random.choice(
+                    list(indices), 
+                    size=min(num_needed, len(indices)), 
+                    replace=False, 
+                    p=probs
+                )
+                selected.extend(sampled_indices.tolist())
+    
+    # Final fallback: if we still need more, add pure random
     if len(selected) < batch_size:
         remaining_available = [idx for idx in available_indices if idx not in selected]
         if remaining_available:

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18939,
-      "rounds": 4,
+      "rounds": 5,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 384,
-      "baseline_total_hits": 13,
+      "baseline_total_queries": 512,
+      "baseline_total_hits": 19,
       "delta_queries": 128,
       "delta_hits": 6,
-      "total_queries": 512,
-      "total_hits": 19,
+      "total_queries": 640,
+      "total_hits": 25,
       "top_k": 654,
       "hit_curve": {
         "queries": [
-          384,
-          512
+          512,
+          640
         ],
         "hits": [
-          13,
-          19
+          19,
+          25
         ]
       },
-      "auc": 2048.0,
-      "auc_normalized": 0.0061162079510703364,
-      "ncg": 0.19439150821138396,
+      "auc": 2816.0,
+      "auc_normalized": 0.00672782874617737,
+      "ncg": 0.2091275961781894,
       "round_details": [
         {
-          "round": 3,
+          "round": 4,
           "selected_count": 128,
           "hits": 6,
-          "cumulative_hits": 19,
+          "cumulative_hits": 25,
           "precision_at_batch": 0.046875,
           "selected": [
-            "ZNF682",
-            "SUGP1",
-            "ADGRB1",
-            "NSMCE1",
-            "PRR21",
-            "ZNF410",
-            "TSPOAP1",
-            "ZXDB",
-            "PCM1",
-            "AKR1C1",
-            "AWAT2",
-            "C17orf67",
-            "CLOCK",
-            "TSPAN17",
-            "KLC3",
-            "CCL24",
-            "ZG16",
-            "PLA2G2C",
-            "PGAM5",
-            "PAPD7",
-            "CBLN2",
-            "LYZL1",
-            "KRTAP10-1",
-            "HLA-A",
-            "HBD",
-            "GNMT",
-            "HEATR9",
-            "AFTPH",
-            "DIO2",
-            "HSDL1",
-            "NPC2",
-            "SDR39U1",
-            "SPINT3",
-            "OR52A5",
-            "MTRNR2L5",
-            "UBE2M",
-            "CD1D",
-            "C2CD6",
-            "IFT27",
-            "CDC23",
-            "PDLIM2",
-            "NPY2R",
-            "LUC7L",
-            "PCNT",
-            "ABCC3",
-            "HIST1H2AI",
-            "ABCB8",
-            "C3orf36",
-            "CHRM1",
-            "DTL",
-            "LRP4",
-            "CCDC7",
-            "PDZRN4",
-            "BANP",
-            "CR2",
-            "EGF",
-            "REST",
-            "DZANK1",
-            "KBTBD11",
-            "MEGF11",
-            "NUCB1",
-            "NUP214",
-            "VWA1",
-            "C4orf33",
-            "QDPR",
-            "LOC100130705",
-            "IARS",
-            "PPM1L",
-            "SLC39A9",
-            "CREBRF",
-            "CHIT1",
-            "FAM133A",
-            "RNF130",
-            "RNF146",
-            "TOMM22",
-            "DMP1",
-            "NLRP3",
-            "ASB14",
-            "FLVCR2",
-            "FOXA2",
-            "PPM1M",
-            "MRGPRE",
-            "TAOK2",
-            "CD40LG",
-            "CCDC102A",
-            "RABL6",
-            "UNC93B1",
-            "NIPSNAP1",
-            "PEX6",
-            "BEGAIN",
-            "ARHGEF6",
-            "C11orf16",
-            "ADGRL4",
-            "MT1M",
-            "BARX1",
-            "TMEM134",
-            "BTD",
-            "SELENBP1",
-            "SPRY4",
-            "OR2AK2",
-            "ARHGAP17",
-            "RNASE7",
-            "SIGLEC14",
-            "AQP12A",
-            "ACTN1",
-            "POLG2",
-            "MRPS15",
-            "ZFP57",
-            "NDUFB10",
-            "GPR89A",
-            "ZNF324B",
-            "ZIM3",
-            "PAM16",
-            "ZNF513",
-            "CHRNA4",
-            "BSPH1",
-            "LIPC",
-            "FAM183A",
-            "EPO",
-            "HEPHL1",
-            "BCAP31",
-            "BIRC2",
-            "NUP210L",
-            "POMP",
-            "CLTC",
-            "PTPRC",
-            "OR7C1",
-            "PCYT2"
+            "HCFC1R1",
+            "ZNF708",
+            "COPS7B",
+            "MSANTD4",
+            "OR13J1",
+            "BIRC5",
+            "ASPA",
+            "PMEPA1",
+            "TBX2",
+            "MAZ",
+            "LMNTD1",
+            "BRPF3",
+            "RPL13A",
+            "TBP",
+            "DVL1",
+            "ETV4",
+            "CYP4Z1",
+            "FCER1A",
+            "PRCD",
+            "TMEM52",
+            "AXIN2",
+            "AP2M1",
+            "AHSG",
+            "ZNF514",
+            "FRS2",
+            "RPL3",
+            "NBPF26",
+            "HERC4",
+            "FXYD4",
+            "WDR87",
+            "MOB1A",
+            "WNK3",
+            "RNF11",
+            "PPP1R21",
+            "CUL2",
+            "TMEM82",
+            "GJA3",
+            "FER1L6",
+            "ZNFX1",
+            "EIF3I",
+            "PRR9",
+            "BEND6",
+            "EBLN1",
+            "ZCCHC18",
+            "SSBP1",
+            "NAPA",
+            "PAGE5",
+            "SKAP2",
+            "RHBDL1",
+            "CLDN20",
+            "DAD1",
+            "FTMT",
+            "SIRT1",
+            "FOXD4L6",
+            "USP14",
+            "GOLT1B",
+            "BICDL1",
+            "ICAM2",
+            "SPATA21",
+            "CDKN2A",
+            "SAMD8",
+            "HES6",
+            "ZFC3H1",
+            "OVCH1",
+            "RNF220",
+            "IL3",
+            "USP7",
+            "EXO1",
+            "VAMP1",
+            "C12orf80",
+            "CHPF",
+            "TRIP13",
+            "PSMA7",
+            "JARID2",
+            "ACTR2",
+            "NARR",
+            "WNT8A",
+            "IL12A",
+            "STX3",
+            "C15orf57",
+            "FAM159A",
+            "SLC46A3",
+            "ACTA1",
+            "CNOT8",
+            "TMEM234",
+            "SPERT",
+            "RGPD6",
+            "CDK11B",
+            "PIGF",
+            "GPR34",
+            "ZBTB49",
+            "USH1G",
+            "RPS18",
+            "NOMO2",
+            "CCSER2",
+            "SH3RF2",
+            "IL12RB2",
+            "SOST",
+            "C1QTNF9B",
+            "ACSM4",
+            "C6orf10",
+            "ZNF852",
+            "BARHL1",
+            "PDIA3",
+            "AOC1",
+            "NKX2-1",
+            "GCAT",
+            "DDA1",
+            "PTPRF",
+            "CRMP1",
+            "CCDC15",
+            "ATP8B4",
+            "DOCK3",
+            "PI15",
+            "GTF3C2",
+            "PXDN",
+            "SLC26A11",
+            "SOX11",
+            "FUBP3",
+            "ATP10B",
+            "GMNN",
+            "GLIS2",
+            "PVALB",
+            "PPP1R13L",
+            "ZNF292",
+            "AGGF1",
+            "ZNF431",
+            "BANF2"
           ],
           "selected_scores": [
-            -0.066292,
-            -0.10537,
-            -0.016333,
-            0.10446,
-            -0.045793,
-            -0.10611,
-            -0.023655,
-            -0.22122,
-            -0.14485,
-            -0.024633,
-            -0.20968,
-            -0.0018348,
-            -0.0871,
-            0.32379,
-            0.022576,
-            -0.0052071,
-            -0.19057,
-            0.15158,
-            0.17435,
-            0.16202,
-            0.039316,
-            -0.026279,
-            -0.13763,
-            0.03841,
-            -0.11022,
-            0.021289,
-            -0.11612,
-            -0.23038,
-            0.21103,
-            -0.08225,
-            0.071884,
-            -0.049585,
-            -0.092487,
-            -0.010455,
-            -0.060609,
-            -0.25676,
-            -0.1676,
-            0.029571,
-            0.049569,
-            0.75313,
-            0.16687,
-            0.020643,
-            0.02102,
-            0.27061,
-            0.10402,
-            -0.093945,
-            -0.05807,
-            -0.17073,
-            -0.038634,
-            0.062116,
-            0.041176,
-            0.035182,
-            0.030132,
-            -0.14328,
-            0.29724,
-            0.16804,
-            0.06455,
-            -0.15082,
-            0.037302,
-            0.077542,
-            -0.14142,
-            0.16475,
-            0.093404,
-            -0.24117,
-            0.089388,
-            -0.2275,
-            0.21769,
-            0.097688,
-            -0.019225,
-            0.067736,
-            -0.10366,
-            -0.13119,
-            -0.14976,
-            -0.33644,
-            -0.050375,
-            -0.16108,
-            0.20612,
-            -0.029937,
-            0.11643,
-            -0.06962,
-            0.066489,
-            0.069416,
-            0.08395,
-            -0.022008,
-            -0.1765,
-            -0.071797,
-            0.1316,
-            0.17017,
-            -0.24127,
-            0.37792,
-            -0.23752,
-            -0.072414,
-            -0.035615,
-            -0.057575,
-            0.082774,
-            -0.089285,
-            -0.1237,
-            -0.10742,
-            -0.196,
-            -0.16243,
-            0.10559,
-            -0.1516,
-            -0.036235,
-            -0.14952,
-            0.055767,
-            0.2274,
-            0.14946,
-            -0.035847,
-            0.27002,
-            -0.089878,
-            0.051283,
-            0.049688,
-            0.19394,
-            0.050747,
-            -0.039819,
-            -0.027673,
-            0.0011676,
-            0.085677,
-            -0.017593,
-            0.083083,
-            0.0062327,
-            0.027505,
-            -0.10562,
-            0.47385,
-            0.25547,
-            -0.86005,
-            0.084699,
-            -0.32403
+            0.14374,
+            -0.061487,
+            0.19767,
+            0.090499,
+            -0.064619,
+            0.29587,
+            -0.21605,
+            -0.079207,
+            0.042468,
+            -0.029087,
+            -0.055232,
+            -0.035772,
+            0.68174,
+            0.081131,
+            0.22398,
+            -0.17676,
+            -0.10156,
+            0.045692,
+            0.010934,
+            0.0088776,
+            -0.26523,
+            0.15837,
+            -0.083725,
+            0.05209,
+            -0.081124,
+            0.42418,
+            -0.057371,
+            0.059392,
+            0.034557,
+            0.025666,
+            -0.01396,
+            0.04998,
+            -0.13504,
+            0.14537,
+            0.085472,
+            -0.080469,
+            -0.18926,
+            0.11182,
+            0.12573,
+            0.44982,
+            -0.20238,
+            0.051703,
+            -0.2278,
+            0.059908,
+            0.32334,
+            -0.030536,
+            -0.12672,
+            -0.098957,
+            -0.030375,
+            0.087545,
+            -0.41773,
+            -0.12925,
+            -0.016595,
+            0.040517,
+            0.03691,
+            -0.15175,
+            0.079299,
+            0.2347,
+            0.0077313,
+            0.081554,
+            0.22405,
+            0.20548,
+            -0.0034201,
+            -0.019738,
+            -0.10547,
+            -0.081305,
+            0.13261,
+            0.012177,
+            0.049521,
+            0.013292,
+            0.010451,
+            0.17361,
+            -0.0031551,
+            -0.079904,
+            -0.062077,
+            0.013846,
+            0.20219,
+            -0.037198,
+            -0.011611,
+            0.044398,
+            -0.045287,
+            0.072478,
+            0.14594,
+            -0.21178,
+            -0.097457,
+            -0.070814,
+            0.083009,
+            -0.03803,
+            0.095559,
+            -0.058217,
+            0.02022,
+            0.06636,
+            0.45801,
+            -0.14486,
+            0.051897,
+            0.052436,
+            -0.034375,
+            0.14584,
+            -0.0093955,
+            0.09115,
+            0.0043576,
+            -0.033076,
+            -0.026312,
+            0.096204,
+            -0.13228,
+            -0.0021911,
+            -0.086123,
+            -0.35533,
+            -0.013963,
+            0.16603,
+            -0.016091,
+            -0.017006,
+            -0.013813,
+            -0.028295,
+            -0.30493,
+            0.19555,
+            -0.095656,
+            0.062703,
+            -0.11714,
+            -0.07034,
+            0.16855,
+            0.017302,
+            0.12967,
+            -0.11964,
+            -0.15018,
+            0.034109,
+            -0.13139,
+            -0.18523
           ],
           "selected_hits": [
             0,
@@ -313,33 +313,6 @@
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
             1,
             0,
             0,
@@ -353,27 +326,6 @@
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
             1,
             0,
             0,
@@ -388,8 +340,6 @@
             0,
             0,
             0,
-            0,
-            0,
             1,
             0,
             0,
@@ -401,34 +351,84 @@
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
             1,
             0,
-            1
+            0,
+            0,
+            0,
+            0,
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
+            0
           ]
         }
       ],
@@ -3126,896 +3126,1792 @@
           "gene": "ZNF682",
           "score": -0.066292,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13983,
           "gene": "SUGP1",
           "score": -0.10537,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16326,
           "gene": "ADGRB1",
           "score": -0.016333,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8628,
           "gene": "NSMCE1",
           "score": 0.10446,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2745,
           "gene": "PRR21",
           "score": -0.045793,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10157,
           "gene": "ZNF410",
           "score": -0.10611,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11342,
           "gene": "TSPOAP1",
           "score": -0.023655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 717,
           "gene": "ZXDB",
           "score": -0.22122,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2425,
           "gene": "PCM1",
           "score": -0.14485,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16202,
           "gene": "AKR1C1",
           "score": -0.024633,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 367,
           "gene": "AWAT2",
           "score": -0.20968,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3858,
           "gene": "C17orf67",
           "score": -0.0018348,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9512,
           "gene": "CLOCK",
           "score": -0.0871,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3954,
           "gene": "TSPAN17",
           "score": 0.32379,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10417,
           "gene": "KLC3",
           "score": 0.022576,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1191,
           "gene": "CCL24",
           "score": -0.0052071,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2233,
           "gene": "ZG16",
           "score": -0.19057,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4535,
           "gene": "PLA2G2C",
           "score": 0.15158,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9097,
           "gene": "PGAM5",
           "score": 0.17435,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5172,
           "gene": "PAPD7",
           "score": 0.16202,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7071,
           "gene": "CBLN2",
           "score": 0.039316,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14340,
           "gene": "LYZL1",
           "score": -0.026279,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2514,
           "gene": "KRTAP10-1",
           "score": -0.13763,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13665,
           "gene": "HLA-A",
           "score": 0.03841,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4795,
           "gene": "HBD",
           "score": -0.11022,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1911,
           "gene": "GNMT",
           "score": 0.021289,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1072,
           "gene": "HEATR9",
           "score": -0.11612,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5777,
           "gene": "AFTPH",
           "score": -0.23038,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10736,
           "gene": "DIO2",
           "score": 0.21103,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8434,
           "gene": "HSDL1",
           "score": -0.08225,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11939,
           "gene": "NPC2",
           "score": 0.071884,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10715,
           "gene": "SDR39U1",
           "score": -0.049585,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3144,
           "gene": "SPINT3",
           "score": -0.092487,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13774,
           "gene": "OR52A5",
           "score": -0.010455,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3011,
           "gene": "MTRNR2L5",
           "score": -0.060609,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 705,
           "gene": "UBE2M",
           "score": -0.25676,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10999,
           "gene": "CD1D",
           "score": -0.1676,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10615,
           "gene": "C2CD6",
           "score": 0.029571,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12951,
           "gene": "IFT27",
           "score": 0.049569,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17752,
           "gene": "CDC23",
           "score": 0.75313,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17959,
           "gene": "PDLIM2",
           "score": 0.16687,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8513,
           "gene": "NPY2R",
           "score": 0.020643,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2000,
           "gene": "LUC7L",
           "score": 0.02102,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16484,
           "gene": "PCNT",
           "score": 0.27061,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12514,
           "gene": "ABCC3",
           "score": 0.10402,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7026,
           "gene": "HIST1H2AI",
           "score": -0.093945,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11761,
           "gene": "ABCB8",
           "score": -0.05807,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5235,
           "gene": "C3orf36",
           "score": -0.17073,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 562,
           "gene": "CHRM1",
           "score": -0.038634,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8361,
           "gene": "DTL",
           "score": 0.062116,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16727,
           "gene": "LRP4",
           "score": 0.041176,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14193,
           "gene": "CCDC7",
           "score": 0.035182,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9844,
           "gene": "PDZRN4",
           "score": 0.030132,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7034,
           "gene": "BANP",
           "score": -0.14328,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13879,
           "gene": "CR2",
           "score": 0.29724,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12898,
           "gene": "EGF",
           "score": 0.16804,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12726,
           "gene": "REST",
           "score": 0.06455,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4816,
           "gene": "DZANK1",
           "score": -0.15082,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15247,
           "gene": "KBTBD11",
           "score": 0.037302,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18545,
           "gene": "MEGF11",
           "score": 0.077542,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2897,
           "gene": "NUCB1",
           "score": -0.14142,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18736,
           "gene": "NUP214",
           "score": 0.16475,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12874,
           "gene": "VWA1",
           "score": 0.093404,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2070,
           "gene": "C4orf33",
           "score": -0.24117,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17232,
           "gene": "QDPR",
           "score": 0.089388,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 965,
           "gene": "LOC100130705",
           "score": -0.2275,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18175,
           "gene": "IARS",
           "score": 0.21769,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17412,
           "gene": "PPM1L",
           "score": 0.097688,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9667,
           "gene": "SLC39A9",
           "score": -0.019225,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10657,
           "gene": "CREBRF",
           "score": 0.067736,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10080,
           "gene": "CHIT1",
           "score": -0.10366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5643,
           "gene": "FAM133A",
           "score": -0.13119,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6133,
           "gene": "RNF130",
           "score": -0.14976,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 334,
           "gene": "RNF146",
           "score": -0.33644,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9365,
           "gene": "TOMM22",
           "score": -0.050375,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1663,
           "gene": "DMP1",
           "score": -0.16108,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13435,
           "gene": "NLRP3",
           "score": 0.20612,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3449,
           "gene": "ASB14",
           "score": -0.029937,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 97,
           "gene": "FLVCR2",
           "score": 0.11643,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12128,
           "gene": "FOXA2",
           "score": -0.06962,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9327,
           "gene": "PPM1M",
           "score": 0.066489,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15230,
           "gene": "MRGPRE",
           "score": 0.069416,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14698,
           "gene": "TAOK2",
           "score": 0.08395,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6721,
           "gene": "CD40LG",
           "score": -0.022008,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11027,
           "gene": "CCDC102A",
           "score": -0.1765,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9067,
           "gene": "RABL6",
           "score": -0.071797,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8118,
           "gene": "UNC93B1",
           "score": 0.1316,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17347,
           "gene": "NIPSNAP1",
           "score": 0.17017,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7546,
           "gene": "PEX6",
           "score": -0.24127,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16520,
           "gene": "BEGAIN",
           "score": 0.37792,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 920,
           "gene": "ARHGEF6",
           "score": -0.23752,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4988,
           "gene": "C11orf16",
           "score": -0.072414,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 753,
           "gene": "ADGRL4",
           "score": -0.035615,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8798,
           "gene": "MT1M",
           "score": -0.057575,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16045,
           "gene": "BARX1",
           "score": 0.082774,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3193,
           "gene": "TMEM134",
           "score": -0.089285,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5864,
           "gene": "BTD",
           "score": -0.1237,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7184,
           "gene": "SELENBP1",
           "score": -0.10742,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2112,
           "gene": "SPRY4",
           "score": -0.196,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3073,
           "gene": "OR2AK2",
           "score": -0.16243,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2167,
           "gene": "ARHGAP17",
           "score": 0.10559,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4443,
           "gene": "RNASE7",
           "score": -0.1516,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13133,
           "gene": "SIGLEC14",
           "score": -0.036235,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5495,
           "gene": "AQP12A",
           "score": -0.14952,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2773,
           "gene": "ACTN1",
           "score": 0.055767,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14954,
           "gene": "POLG2",
           "score": 0.2274,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13023,
           "gene": "MRPS15",
           "score": 0.14946,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9294,
           "gene": "ZFP57",
           "score": -0.035847,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12799,
           "gene": "NDUFB10",
           "score": 0.27002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13470,
           "gene": "GPR89A",
           "score": -0.089878,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12632,
           "gene": "ZNF324B",
           "score": 0.051283,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5467,
           "gene": "ZIM3",
           "score": 0.049688,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17579,
           "gene": "PAM16",
           "score": 0.19394,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1001,
           "gene": "ZNF513",
           "score": 0.050747,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2422,
           "gene": "CHRNA4",
           "score": -0.039819,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10751,
           "gene": "BSPH1",
           "score": -0.027673,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13891,
           "gene": "LIPC",
           "score": 0.0011676,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7844,
           "gene": "FAM183A",
           "score": 0.085677,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10759,
           "gene": "EPO",
           "score": -0.017593,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12200,
           "gene": "HEPHL1",
           "score": 0.083083,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14657,
           "gene": "BCAP31",
           "score": 0.0062327,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7233,
           "gene": "BIRC2",
           "score": 0.027505,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13118,
           "gene": "NUP210L",
           "score": -0.10562,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17403,
           "gene": "POMP",
           "score": 0.47385,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18021,
           "gene": "CLTC",
           "score": 0.25547,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 35,
           "gene": "PTPRC",
           "score": -0.86005,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13817,
           "gene": "OR7C1",
           "score": 0.084699,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1112,
           "gene": "PCYT2",
           "score": -0.32403,
           "hit": 1,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 14863,
+          "gene": "HCFC1R1",
+          "score": 0.14374,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12040,
+          "gene": "ZNF708",
+          "score": -0.061487,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4739,
+          "gene": "COPS7B",
+          "score": 0.19767,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14378,
+          "gene": "MSANTD4",
+          "score": 0.090499,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5953,
+          "gene": "OR13J1",
+          "score": -0.064619,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17757,
+          "gene": "BIRC5",
+          "score": 0.29587,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 808,
+          "gene": "ASPA",
+          "score": -0.21605,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8359,
+          "gene": "PMEPA1",
+          "score": -0.079207,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17289,
+          "gene": "TBX2",
+          "score": 0.042468,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8629,
+          "gene": "MAZ",
+          "score": -0.029087,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9642,
+          "gene": "LMNTD1",
+          "score": -0.055232,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1608,
+          "gene": "BRPF3",
+          "score": -0.035772,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8089,
+          "gene": "RPL13A",
+          "score": 0.68174,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 14144,
+          "gene": "TBP",
+          "score": 0.081131,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16429,
+          "gene": "DVL1",
+          "score": 0.22398,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6153,
+          "gene": "ETV4",
+          "score": -0.17676,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1971,
+          "gene": "CYP4Z1",
+          "score": -0.10156,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15212,
+          "gene": "FCER1A",
+          "score": 0.045692,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7498,
+          "gene": "PRCD",
+          "score": 0.010934,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11904,
+          "gene": "TMEM52",
+          "score": 0.0088776,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 678,
+          "gene": "AXIN2",
+          "score": -0.26523,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5704,
+          "gene": "AP2M1",
+          "score": 0.15837,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 900,
+          "gene": "AHSG",
+          "score": -0.083725,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7065,
+          "gene": "ZNF514",
+          "score": 0.05209,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4991,
+          "gene": "FRS2",
+          "score": -0.081124,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18762,
+          "gene": "RPL3",
+          "score": 0.42418,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 7504,
+          "gene": "NBPF26",
+          "score": -0.057371,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5847,
+          "gene": "HERC4",
+          "score": 0.059392,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4212,
+          "gene": "FXYD4",
+          "score": 0.034557,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9377,
+          "gene": "WDR87",
+          "score": 0.025666,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1096,
+          "gene": "MOB1A",
+          "score": -0.01396,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5514,
+          "gene": "WNK3",
+          "score": 0.04998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4474,
+          "gene": "RNF11",
+          "score": -0.13504,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18256,
+          "gene": "PPP1R21",
+          "score": 0.14537,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11676,
+          "gene": "CUL2",
+          "score": 0.085472,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16344,
+          "gene": "TMEM82",
+          "score": -0.080469,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1710,
+          "gene": "GJA3",
+          "score": -0.18926,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2835,
+          "gene": "FER1L6",
+          "score": 0.11182,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12757,
+          "gene": "ZNFX1",
+          "score": 0.12573,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18546,
+          "gene": "EIF3I",
+          "score": 0.44982,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 438,
+          "gene": "PRR9",
+          "score": -0.20238,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17194,
+          "gene": "BEND6",
+          "score": 0.051703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1099,
+          "gene": "EBLN1",
+          "score": -0.2278,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14332,
+          "gene": "ZCCHC18",
+          "score": 0.059908,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1224,
+          "gene": "SSBP1",
+          "score": 0.32334,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4867,
+          "gene": "NAPA",
+          "score": -0.030536,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3234,
+          "gene": "PAGE5",
+          "score": -0.12672,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3718,
+          "gene": "SKAP2",
+          "score": -0.098957,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2024,
+          "gene": "RHBDL1",
+          "score": -0.030375,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9884,
+          "gene": "CLDN20",
+          "score": 0.087545,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 118,
+          "gene": "DAD1",
+          "score": -0.41773,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 14992,
+          "gene": "FTMT",
+          "score": -0.12925,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2641,
+          "gene": "SIRT1",
+          "score": -0.016595,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2035,
+          "gene": "FOXD4L6",
+          "score": 0.040517,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8150,
+          "gene": "USP14",
+          "score": 0.03691,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4172,
+          "gene": "GOLT1B",
+          "score": -0.15175,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15842,
+          "gene": "BICDL1",
+          "score": 0.079299,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 111,
+          "gene": "ICAM2",
+          "score": 0.2347,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2823,
+          "gene": "SPATA21",
+          "score": 0.0077313,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13248,
+          "gene": "CDKN2A",
+          "score": 0.081554,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2810,
+          "gene": "SAMD8",
+          "score": 0.22405,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16500,
+          "gene": "HES6",
+          "score": 0.20548,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9755,
+          "gene": "ZFC3H1",
+          "score": -0.0034201,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8059,
+          "gene": "OVCH1",
+          "score": -0.019738,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 358,
+          "gene": "RNF220",
+          "score": -0.10547,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9382,
+          "gene": "IL3",
+          "score": -0.081305,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17932,
+          "gene": "USP7",
+          "score": 0.13261,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6570,
+          "gene": "EXO1",
+          "score": 0.012177,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7733,
+          "gene": "VAMP1",
+          "score": 0.049521,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15712,
+          "gene": "C12orf80",
+          "score": 0.013292,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13546,
+          "gene": "CHPF",
+          "score": 0.010451,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9233,
+          "gene": "TRIP13",
+          "score": 0.17361,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4431,
+          "gene": "PSMA7",
+          "score": -0.0031551,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12746,
+          "gene": "JARID2",
+          "score": -0.079904,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10976,
+          "gene": "ACTR2",
+          "score": -0.062077,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8501,
+          "gene": "NARR",
+          "score": 0.013846,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10936,
+          "gene": "WNT8A",
+          "score": 0.20219,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5915,
+          "gene": "IL12A",
+          "score": -0.037198,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12364,
+          "gene": "STX3",
+          "score": -0.011611,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1725,
+          "gene": "C15orf57",
+          "score": 0.044398,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6971,
+          "gene": "FAM159A",
+          "score": -0.045287,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10853,
+          "gene": "SLC46A3",
+          "score": 0.072478,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15375,
+          "gene": "ACTA1",
+          "score": 0.14594,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8850,
+          "gene": "CNOT8",
+          "score": -0.21178,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11837,
+          "gene": "TMEM234",
+          "score": -0.097457,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10577,
+          "gene": "SPERT",
+          "score": -0.070814,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6316,
+          "gene": "RGPD6",
+          "score": 0.083009,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2612,
+          "gene": "CDK11B",
+          "score": -0.03803,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17128,
+          "gene": "PIGF",
+          "score": 0.095559,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4355,
+          "gene": "GPR34",
+          "score": -0.058217,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4044,
+          "gene": "ZBTB49",
+          "score": 0.02022,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3389,
+          "gene": "USH1G",
+          "score": 0.06636,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12425,
+          "gene": "RPS18",
+          "score": 0.45801,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 964,
+          "gene": "NOMO2",
+          "score": -0.14486,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1735,
+          "gene": "CCSER2",
+          "score": 0.051897,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13313,
+          "gene": "SH3RF2",
+          "score": 0.052436,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13753,
+          "gene": "IL12RB2",
+          "score": -0.034375,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9788,
+          "gene": "SOST",
+          "score": 0.14584,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12499,
+          "gene": "C1QTNF9B",
+          "score": -0.0093955,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5904,
+          "gene": "ACSM4",
+          "score": 0.09115,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1492,
+          "gene": "C6orf10",
+          "score": 0.0043576,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13561,
+          "gene": "ZNF852",
+          "score": -0.033076,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13723,
+          "gene": "BARHL1",
+          "score": -0.026312,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2340,
+          "gene": "PDIA3",
+          "score": 0.096204,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8509,
+          "gene": "AOC1",
+          "score": -0.13228,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6062,
+          "gene": "NKX2-1",
+          "score": -0.0021911,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9230,
+          "gene": "GCAT",
+          "score": -0.086123,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 143,
+          "gene": "DDA1",
+          "score": -0.35533,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 7953,
+          "gene": "PTPRF",
+          "score": -0.013963,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8159,
+          "gene": "CRMP1",
+          "score": 0.16603,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14933,
+          "gene": "CCDC15",
+          "score": -0.016091,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4566,
+          "gene": "ATP8B4",
+          "score": -0.017006,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3943,
+          "gene": "DOCK3",
+          "score": -0.013813,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1581,
+          "gene": "PI15",
+          "score": -0.028295,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 247,
+          "gene": "GTF3C2",
+          "score": -0.30493,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12605,
+          "gene": "PXDN",
+          "score": 0.19555,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6392,
+          "gene": "SLC26A11",
+          "score": -0.095656,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17859,
+          "gene": "SOX11",
+          "score": 0.062703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11288,
+          "gene": "FUBP3",
+          "score": -0.11714,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6682,
+          "gene": "ATP10B",
+          "score": -0.07034,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14861,
+          "gene": "GMNN",
+          "score": 0.16855,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16066,
+          "gene": "GLIS2",
+          "score": 0.017302,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2398,
+          "gene": "PVALB",
+          "score": 0.12967,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16060,
+          "gene": "PPP1R13L",
+          "score": -0.11964,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3341,
+          "gene": "ZNF292",
+          "score": -0.15018,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18541,
+          "gene": "AGGF1",
+          "score": 0.034109,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2735,
+          "gene": "ZNF431",
+          "score": -0.13139,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2141,
+          "gene": "BANF2",
+          "score": -0.18523,
+          "hit": 0,
+          "round": 4
         }
       ],
       "queried_history": [
@@ -6712,896 +7608,1792 @@
           "gene": "ZNF682",
           "score": -0.066292,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13983,
           "gene": "SUGP1",
           "score": -0.10537,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16326,
           "gene": "ADGRB1",
           "score": -0.016333,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8628,
           "gene": "NSMCE1",
           "score": 0.10446,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2745,
           "gene": "PRR21",
           "score": -0.045793,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10157,
           "gene": "ZNF410",
           "score": -0.10611,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11342,
           "gene": "TSPOAP1",
           "score": -0.023655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 717,
           "gene": "ZXDB",
           "score": -0.22122,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2425,
           "gene": "PCM1",
           "score": -0.14485,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16202,
           "gene": "AKR1C1",
           "score": -0.024633,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 367,
           "gene": "AWAT2",
           "score": -0.20968,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3858,
           "gene": "C17orf67",
           "score": -0.0018348,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9512,
           "gene": "CLOCK",
           "score": -0.0871,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3954,
           "gene": "TSPAN17",
           "score": 0.32379,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10417,
           "gene": "KLC3",
           "score": 0.022576,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1191,
           "gene": "CCL24",
           "score": -0.0052071,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2233,
           "gene": "ZG16",
           "score": -0.19057,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4535,
           "gene": "PLA2G2C",
           "score": 0.15158,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9097,
           "gene": "PGAM5",
           "score": 0.17435,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5172,
           "gene": "PAPD7",
           "score": 0.16202,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7071,
           "gene": "CBLN2",
           "score": 0.039316,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14340,
           "gene": "LYZL1",
           "score": -0.026279,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2514,
           "gene": "KRTAP10-1",
           "score": -0.13763,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13665,
           "gene": "HLA-A",
           "score": 0.03841,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4795,
           "gene": "HBD",
           "score": -0.11022,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1911,
           "gene": "GNMT",
           "score": 0.021289,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1072,
           "gene": "HEATR9",
           "score": -0.11612,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5777,
           "gene": "AFTPH",
           "score": -0.23038,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10736,
           "gene": "DIO2",
           "score": 0.21103,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8434,
           "gene": "HSDL1",
           "score": -0.08225,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11939,
           "gene": "NPC2",
           "score": 0.071884,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10715,
           "gene": "SDR39U1",
           "score": -0.049585,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3144,
           "gene": "SPINT3",
           "score": -0.092487,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13774,
           "gene": "OR52A5",
           "score": -0.010455,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3011,
           "gene": "MTRNR2L5",
           "score": -0.060609,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 705,
           "gene": "UBE2M",
           "score": -0.25676,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10999,
           "gene": "CD1D",
           "score": -0.1676,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10615,
           "gene": "C2CD6",
           "score": 0.029571,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12951,
           "gene": "IFT27",
           "score": 0.049569,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17752,
           "gene": "CDC23",
           "score": 0.75313,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17959,
           "gene": "PDLIM2",
           "score": 0.16687,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8513,
           "gene": "NPY2R",
           "score": 0.020643,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2000,
           "gene": "LUC7L",
           "score": 0.02102,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16484,
           "gene": "PCNT",
           "score": 0.27061,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12514,
           "gene": "ABCC3",
           "score": 0.10402,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7026,
           "gene": "HIST1H2AI",
           "score": -0.093945,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11761,
           "gene": "ABCB8",
           "score": -0.05807,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5235,
           "gene": "C3orf36",
           "score": -0.17073,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 562,
           "gene": "CHRM1",
           "score": -0.038634,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8361,
           "gene": "DTL",
           "score": 0.062116,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16727,
           "gene": "LRP4",
           "score": 0.041176,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14193,
           "gene": "CCDC7",
           "score": 0.035182,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9844,
           "gene": "PDZRN4",
           "score": 0.030132,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7034,
           "gene": "BANP",
           "score": -0.14328,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13879,
           "gene": "CR2",
           "score": 0.29724,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12898,
           "gene": "EGF",
           "score": 0.16804,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12726,
           "gene": "REST",
           "score": 0.06455,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4816,
           "gene": "DZANK1",
           "score": -0.15082,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15247,
           "gene": "KBTBD11",
           "score": 0.037302,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18545,
           "gene": "MEGF11",
           "score": 0.077542,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2897,
           "gene": "NUCB1",
           "score": -0.14142,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18736,
           "gene": "NUP214",
           "score": 0.16475,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12874,
           "gene": "VWA1",
           "score": 0.093404,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2070,
           "gene": "C4orf33",
           "score": -0.24117,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17232,
           "gene": "QDPR",
           "score": 0.089388,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 965,
           "gene": "LOC100130705",
           "score": -0.2275,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18175,
           "gene": "IARS",
           "score": 0.21769,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17412,
           "gene": "PPM1L",
           "score": 0.097688,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9667,
           "gene": "SLC39A9",
           "score": -0.019225,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10657,
           "gene": "CREBRF",
           "score": 0.067736,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10080,
           "gene": "CHIT1",
           "score": -0.10366,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5643,
           "gene": "FAM133A",
           "score": -0.13119,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6133,
           "gene": "RNF130",
           "score": -0.14976,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 334,
           "gene": "RNF146",
           "score": -0.33644,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9365,
           "gene": "TOMM22",
           "score": -0.050375,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1663,
           "gene": "DMP1",
           "score": -0.16108,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13435,
           "gene": "NLRP3",
           "score": 0.20612,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3449,
           "gene": "ASB14",
           "score": -0.029937,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 97,
           "gene": "FLVCR2",
           "score": 0.11643,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12128,
           "gene": "FOXA2",
           "score": -0.06962,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9327,
           "gene": "PPM1M",
           "score": 0.066489,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15230,
           "gene": "MRGPRE",
           "score": 0.069416,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14698,
           "gene": "TAOK2",
           "score": 0.08395,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6721,
           "gene": "CD40LG",
           "score": -0.022008,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11027,
           "gene": "CCDC102A",
           "score": -0.1765,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9067,
           "gene": "RABL6",
           "score": -0.071797,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8118,
           "gene": "UNC93B1",
           "score": 0.1316,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17347,
           "gene": "NIPSNAP1",
           "score": 0.17017,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7546,
           "gene": "PEX6",
           "score": -0.24127,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16520,
           "gene": "BEGAIN",
           "score": 0.37792,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 920,
           "gene": "ARHGEF6",
           "score": -0.23752,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4988,
           "gene": "C11orf16",
           "score": -0.072414,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 753,
           "gene": "ADGRL4",
           "score": -0.035615,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8798,
           "gene": "MT1M",
           "score": -0.057575,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16045,
           "gene": "BARX1",
           "score": 0.082774,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3193,
           "gene": "TMEM134",
           "score": -0.089285,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5864,
           "gene": "BTD",
           "score": -0.1237,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7184,
           "gene": "SELENBP1",
           "score": -0.10742,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2112,
           "gene": "SPRY4",
           "score": -0.196,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3073,
           "gene": "OR2AK2",
           "score": -0.16243,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2167,
           "gene": "ARHGAP17",
           "score": 0.10559,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4443,
           "gene": "RNASE7",
           "score": -0.1516,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13133,
           "gene": "SIGLEC14",
           "score": -0.036235,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5495,
           "gene": "AQP12A",
           "score": -0.14952,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2773,
           "gene": "ACTN1",
           "score": 0.055767,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14954,
           "gene": "POLG2",
           "score": 0.2274,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13023,
           "gene": "MRPS15",
           "score": 0.14946,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9294,
           "gene": "ZFP57",
           "score": -0.035847,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12799,
           "gene": "NDUFB10",
           "score": 0.27002,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13470,
           "gene": "GPR89A",
           "score": -0.089878,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12632,
           "gene": "ZNF324B",
           "score": 0.051283,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5467,
           "gene": "ZIM3",
           "score": 0.049688,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17579,
           "gene": "PAM16",
           "score": 0.19394,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1001,
           "gene": "ZNF513",
           "score": 0.050747,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2422,
           "gene": "CHRNA4",
           "score": -0.039819,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10751,
           "gene": "BSPH1",
           "score": -0.027673,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13891,
           "gene": "LIPC",
           "score": 0.0011676,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7844,
           "gene": "FAM183A",
           "score": 0.085677,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10759,
           "gene": "EPO",
           "score": -0.017593,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12200,
           "gene": "HEPHL1",
           "score": 0.083083,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14657,
           "gene": "BCAP31",
           "score": 0.0062327,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7233,
           "gene": "BIRC2",
           "score": 0.027505,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13118,
           "gene": "NUP210L",
           "score": -0.10562,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17403,
           "gene": "POMP",
           "score": 0.47385,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18021,
           "gene": "CLTC",
           "score": 0.25547,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 35,
           "gene": "PTPRC",
           "score": -0.86005,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13817,
           "gene": "OR7C1",
           "score": 0.084699,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1112,
           "gene": "PCYT2",
           "score": -0.32403,
           "hit": 1,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 14863,
+          "gene": "HCFC1R1",
+          "score": 0.14374,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12040,
+          "gene": "ZNF708",
+          "score": -0.061487,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4739,
+          "gene": "COPS7B",
+          "score": 0.19767,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14378,
+          "gene": "MSANTD4",
+          "score": 0.090499,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5953,
+          "gene": "OR13J1",
+          "score": -0.064619,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17757,
+          "gene": "BIRC5",
+          "score": 0.29587,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 808,
+          "gene": "ASPA",
+          "score": -0.21605,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8359,
+          "gene": "PMEPA1",
+          "score": -0.079207,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17289,
+          "gene": "TBX2",
+          "score": 0.042468,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8629,
+          "gene": "MAZ",
+          "score": -0.029087,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9642,
+          "gene": "LMNTD1",
+          "score": -0.055232,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1608,
+          "gene": "BRPF3",
+          "score": -0.035772,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8089,
+          "gene": "RPL13A",
+          "score": 0.68174,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 14144,
+          "gene": "TBP",
+          "score": 0.081131,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16429,
+          "gene": "DVL1",
+          "score": 0.22398,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6153,
+          "gene": "ETV4",
+          "score": -0.17676,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1971,
+          "gene": "CYP4Z1",
+          "score": -0.10156,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15212,
+          "gene": "FCER1A",
+          "score": 0.045692,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7498,
+          "gene": "PRCD",
+          "score": 0.010934,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11904,
+          "gene": "TMEM52",
+          "score": 0.0088776,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 678,
+          "gene": "AXIN2",
+          "score": -0.26523,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5704,
+          "gene": "AP2M1",
+          "score": 0.15837,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 900,
+          "gene": "AHSG",
+          "score": -0.083725,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7065,
+          "gene": "ZNF514",
+          "score": 0.05209,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4991,
+          "gene": "FRS2",
+          "score": -0.081124,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18762,
+          "gene": "RPL3",
+          "score": 0.42418,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 7504,
+          "gene": "NBPF26",
+          "score": -0.057371,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5847,
+          "gene": "HERC4",
+          "score": 0.059392,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4212,
+          "gene": "FXYD4",
+          "score": 0.034557,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9377,
+          "gene": "WDR87",
+          "score": 0.025666,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1096,
+          "gene": "MOB1A",
+          "score": -0.01396,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5514,
+          "gene": "WNK3",
+          "score": 0.04998,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4474,
+          "gene": "RNF11",
+          "score": -0.13504,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18256,
+          "gene": "PPP1R21",
+          "score": 0.14537,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11676,
+          "gene": "CUL2",
+          "score": 0.085472,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16344,
+          "gene": "TMEM82",
+          "score": -0.080469,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1710,
+          "gene": "GJA3",
+          "score": -0.18926,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2835,
+          "gene": "FER1L6",
+          "score": 0.11182,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12757,
+          "gene": "ZNFX1",
+          "score": 0.12573,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18546,
+          "gene": "EIF3I",
+          "score": 0.44982,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 438,
+          "gene": "PRR9",
+          "score": -0.20238,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17194,
+          "gene": "BEND6",
+          "score": 0.051703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1099,
+          "gene": "EBLN1",
+          "score": -0.2278,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14332,
+          "gene": "ZCCHC18",
+          "score": 0.059908,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1224,
+          "gene": "SSBP1",
+          "score": 0.32334,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4867,
+          "gene": "NAPA",
+          "score": -0.030536,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3234,
+          "gene": "PAGE5",
+          "score": -0.12672,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3718,
+          "gene": "SKAP2",
+          "score": -0.098957,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2024,
+          "gene": "RHBDL1",
+          "score": -0.030375,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9884,
+          "gene": "CLDN20",
+          "score": 0.087545,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 118,
+          "gene": "DAD1",
+          "score": -0.41773,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 14992,
+          "gene": "FTMT",
+          "score": -0.12925,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2641,
+          "gene": "SIRT1",
+          "score": -0.016595,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2035,
+          "gene": "FOXD4L6",
+          "score": 0.040517,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8150,
+          "gene": "USP14",
+          "score": 0.03691,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4172,
+          "gene": "GOLT1B",
+          "score": -0.15175,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15842,
+          "gene": "BICDL1",
+          "score": 0.079299,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 111,
+          "gene": "ICAM2",
+          "score": 0.2347,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2823,
+          "gene": "SPATA21",
+          "score": 0.0077313,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13248,
+          "gene": "CDKN2A",
+          "score": 0.081554,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2810,
+          "gene": "SAMD8",
+          "score": 0.22405,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16500,
+          "gene": "HES6",
+          "score": 0.20548,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9755,
+          "gene": "ZFC3H1",
+          "score": -0.0034201,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8059,
+          "gene": "OVCH1",
+          "score": -0.019738,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 358,
+          "gene": "RNF220",
+          "score": -0.10547,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9382,
+          "gene": "IL3",
+          "score": -0.081305,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17932,
+          "gene": "USP7",
+          "score": 0.13261,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6570,
+          "gene": "EXO1",
+          "score": 0.012177,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7733,
+          "gene": "VAMP1",
+          "score": 0.049521,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15712,
+          "gene": "C12orf80",
+          "score": 0.013292,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13546,
+          "gene": "CHPF",
+          "score": 0.010451,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9233,
+          "gene": "TRIP13",
+          "score": 0.17361,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4431,
+          "gene": "PSMA7",
+          "score": -0.0031551,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12746,
+          "gene": "JARID2",
+          "score": -0.079904,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10976,
+          "gene": "ACTR2",
+          "score": -0.062077,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8501,
+          "gene": "NARR",
+          "score": 0.013846,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10936,
+          "gene": "WNT8A",
+          "score": 0.20219,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5915,
+          "gene": "IL12A",
+          "score": -0.037198,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12364,
+          "gene": "STX3",
+          "score": -0.011611,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1725,
+          "gene": "C15orf57",
+          "score": 0.044398,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6971,
+          "gene": "FAM159A",
+          "score": -0.045287,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10853,
+          "gene": "SLC46A3",
+          "score": 0.072478,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15375,
+          "gene": "ACTA1",
+          "score": 0.14594,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8850,
+          "gene": "CNOT8",
+          "score": -0.21178,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11837,
+          "gene": "TMEM234",
+          "score": -0.097457,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10577,
+          "gene": "SPERT",
+          "score": -0.070814,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6316,
+          "gene": "RGPD6",
+          "score": 0.083009,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2612,
+          "gene": "CDK11B",
+          "score": -0.03803,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17128,
+          "gene": "PIGF",
+          "score": 0.095559,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4355,
+          "gene": "GPR34",
+          "score": -0.058217,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4044,
+          "gene": "ZBTB49",
+          "score": 0.02022,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3389,
+          "gene": "USH1G",
+          "score": 0.06636,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12425,
+          "gene": "RPS18",
+          "score": 0.45801,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 964,
+          "gene": "NOMO2",
+          "score": -0.14486,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1735,
+          "gene": "CCSER2",
+          "score": 0.051897,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13313,
+          "gene": "SH3RF2",
+          "score": 0.052436,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13753,
+          "gene": "IL12RB2",
+          "score": -0.034375,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9788,
+          "gene": "SOST",
+          "score": 0.14584,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12499,
+          "gene": "C1QTNF9B",
+          "score": -0.0093955,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5904,
+          "gene": "ACSM4",
+          "score": 0.09115,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1492,
+          "gene": "C6orf10",
+          "score": 0.0043576,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13561,
+          "gene": "ZNF852",
+          "score": -0.033076,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13723,
+          "gene": "BARHL1",
+          "score": -0.026312,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2340,
+          "gene": "PDIA3",
+          "score": 0.096204,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8509,
+          "gene": "AOC1",
+          "score": -0.13228,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6062,
+          "gene": "NKX2-1",
+          "score": -0.0021911,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9230,
+          "gene": "GCAT",
+          "score": -0.086123,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 143,
+          "gene": "DDA1",
+          "score": -0.35533,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 7953,
+          "gene": "PTPRF",
+          "score": -0.013963,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8159,
+          "gene": "CRMP1",
+          "score": 0.16603,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14933,
+          "gene": "CCDC15",
+          "score": -0.016091,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4566,
+          "gene": "ATP8B4",
+          "score": -0.017006,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3943,
+          "gene": "DOCK3",
+          "score": -0.013813,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1581,
+          "gene": "PI15",
+          "score": -0.028295,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 247,
+          "gene": "GTF3C2",
+          "score": -0.30493,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12605,
+          "gene": "PXDN",
+          "score": 0.19555,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6392,
+          "gene": "SLC26A11",
+          "score": -0.095656,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17859,
+          "gene": "SOX11",
+          "score": 0.062703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11288,
+          "gene": "FUBP3",
+          "score": -0.11714,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6682,
+          "gene": "ATP10B",
+          "score": -0.07034,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 14861,
+          "gene": "GMNN",
+          "score": 0.16855,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16066,
+          "gene": "GLIS2",
+          "score": 0.017302,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2398,
+          "gene": "PVALB",
+          "score": 0.12967,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16060,
+          "gene": "PPP1R13L",
+          "score": -0.11964,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3341,
+          "gene": "ZNF292",
+          "score": -0.15018,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 18541,
+          "gene": "AGGF1",
+          "score": 0.034109,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2735,
+          "gene": "ZNF431",
+          "score": -0.13139,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2141,
+          "gene": "BANF2",
+          "score": -0.18523,
+          "hit": 0,
+          "round": 4
         }
       ]
     }

```
