# Change Record — candidate_5

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21_down/run-1/best/current/harness
Generated at: 2026-04-30T07:02:56.326636

## Files Changed

- model.py: modified (added=90, deleted=177, delta=-87)
- outputs/metrics.json: modified (added=2395, deleted=603, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -28,12 +28,12 @@
     Output:
     - list[int] of NEW candidate indices (no repeats; already-selected may be ignored/replaced by runner).
     
-    Strategy: Thompson Sampling with Gene Cluster Priors
-    - Uses Thompson Sampling (Bayesian bandit algorithm) for adaptive exploration-exploitation
-    - Models each candidate with Beta distribution based on hit observations
-    - Uses gene search to create clusters and share information via Bayesian priors
-    - Enhanced fallback: Uses gene name prefix clustering when gene search unavailable
-    - Naturally balances exploration vs exploitation based on uncertainty
+    Strategy: Bayesian Sparse Hit Detection with Laplace Priors
+    - Uses Bayesian Lasso (Laplace prior) to model sparse hit structure
+    - Assumes only a small fraction of genes are true hits (sparsity assumption)
+    - Uses two-component mixture: (1) Laplace prior for hit genes, (2) Gaussian for background
+    - Adaptively estimates sparsity level from observed hit rate
+    - Uses Upper Confidence Bound (UCB) for selection with sparsity-aware uncertainty
     """
     rng = random.Random(seed)
     np.random.seed(seed)
@@ -79,195 +79,108 @@
         
         return selected_indices[:batch_size]
     
-    # Enhanced Thompson Sampling with Continuous Score Modeling
-    # Use Gaussian-Gamma model for continuous scores instead of Beta for binary hits
+    # Bayesian Sparse Hit Detection with Laplace Priors
+    # Uses two-component mixture: Laplace for hits (sparse), Gaussian for background
     
-    # Group candidates into clusters based on gene similarity
-    clusters = defaultdict(list)
-    candidate_to_cluster = {}
+    # Estimate sparsity level from observed hit rate
+    total_observed = len(history)
+    hit_count = sum(1 for h in history if h.get('hit') == 1)
+    empirical_hit_rate = hit_count / max(total_observed, 1)
     
-    # Try to use gene search to create clusters
-    try:
-        import bda_tools
-        
-        # Create clusters for all candidates we have history for
-        for h in history:
-            idx = h['candidate_index']
-            candidate = candidates[idx]
-            gene = candidate.get('gene') or candidate.get('gene_a')
-            
-            if gene and idx not in candidate_to_cluster:
-                # Find similar genes
-                try:
-                    similar = bda_tools.gene_search(gene, k=20, diverse=False)
-                    cluster_id = f"cluster_{gene}"
-                    
-                    for sim_idx in similar:
-                        if sim_idx not in candidate_to_cluster:
-                            candidate_to_cluster[sim_idx] = cluster_id
-                            clusters[cluster_id].append(sim_idx)
-                except:
-                    # If gene search fails, put in singleton cluster
-                    cluster_id = f"singleton_{idx}"
-                    candidate_to_cluster[idx] = cluster_id
-                    clusters[cluster_id] = [idx]
-        
-        # Assign unassigned candidates to singleton clusters
-        for idx in all_indices:
-            if idx not in candidate_to_cluster:
-                cluster_id = f"singleton_{idx}"
-                candidate_to_cluster[idx] = cluster_id
-                clusters[cluster_id] = [idx]
-                
-    except ImportError:
-        # No gene search available - use enhanced fallback: gene family prefix clustering
-        # Group genes by name prefix to capture gene families (e.g., ZNF, ZSCAN, TNF, etc.)
-        gene_to_prefix = {}
-        
-        for idx in all_indices:
-            candidate = candidates[idx]
-            gene = candidate.get('gene') or candidate.get('gene_a')
-            if gene:
-                # Extract prefix: typically first 3-4 letters before numbers
-                # This captures gene families like ZNF, ZSCAN, TNF, IL, etc.
-                prefix = ''.join([c for c in gene if not c.isdigit()])[:4]
-                if len(prefix) >= 2:
-                    gene_to_prefix[idx] = f"family_{prefix}"
-                else:
-                    gene_to_prefix[idx] = f"singleton_{idx}"
-            else:
-                gene_to_prefix[idx] = f"singleton_{idx}"
-        
-        # Create clusters based on prefix
-        for idx, prefix in gene_to_prefix.items():
-            candidate_to_cluster[idx] = prefix
-            clusters[prefix].append(idx)
+    # Sparsity parameter: assume at least 1% hit rate, cap at 20%
+    sparsity_prior = max(0.01, min(empirical_hit_rate, 0.20)) if total_observed > 0 else 0.05
     
-    # Compute cluster statistics using continuous scores
-    cluster_sums = defaultdict(float)
-    cluster_sums_sq = defaultdict(float)
-    cluster_counts = defaultdict(int)
+    # Compute global statistics for background distribution
+    all_scores = [h['score'] for h in history]
+    background_mean = np.mean(all_scores) if all_scores else 0.0
+    background_var = np.var(all_scores) if len(all_scores) > 1 else 1.0
     
-    for h in history:
-        idx = h['candidate_index']
-        cluster_id = candidate_to_cluster[idx]
-        score = h['score']
-        
-        cluster_sums[cluster_id] += score
-        cluster_sums_sq[cluster_id] += score * score
-        cluster_counts[cluster_id] += 1
+    # For hit distribution: use Laplace prior (double exponential)
+    # Laplace is centered at extreme negative values for this task
+    hit_scores = [h['score'] for h in history if h.get('hit') == 1]
+    if len(hit_scores) > 0:
+        hit_mean = np.mean(hit_scores)
+        hit_scale = np.mean(np.abs(np.array(hit_scores) - hit_mean)) if len(hit_scores) > 1 else 1.0
+    else:
+        # Prior for hits: assume they are at least 2 std devs below background
+        hit_mean = background_mean - 2 * np.sqrt(background_var)
+        hit_scale = np.sqrt(background_var)
     
-    # Compute global statistics for empirical Bayes prior
-    all_scores = [h['score'] for h in history]
-    global_mean = np.mean(all_scores) if all_scores else 0.0
-    global_var = np.var(all_scores) if len(all_scores) > 1 else 1.0
-    
-    # Gaussian-Gamma prior parameters (uninformative but centered at global stats)
-    mu_0 = global_mean  # Prior mean
-    lambda_0 = 1.0      # Prior precision scaling
-    alpha_0 = 1.0       # Prior shape for precision
-    beta_0 = global_var if global_var > 0 else 1.0  # Prior rate for precision
-    
-    # For each cluster, compute posterior parameters
-    cluster_posterior = {}
-    
-    for cluster_id in clusters:
-        n = cluster_counts.get(cluster_id, 0)
-        
-        if n == 0:
-            # No observations, use prior
-            cluster_posterior[cluster_id] = {
-                'mu_n': mu_0,
-                'lambda_n': lambda_0,
-                'alpha_n': alpha_0,
-                'beta_n': beta_0
-            }
-        else:
-            # Update posterior with cluster observations
-            sum_x = cluster_sums[cluster_id]
-            sum_x_sq = cluster_sums_sq[cluster_id]
-            mean_x = sum_x / n
-            
-            # Gaussian-Gamma posterior update
-            lambda_n = lambda_0 + n
-            mu_n = (lambda_0 * mu_0 + sum_x) / lambda_n
-            alpha_n = alpha_0 + n / 2.0
-            beta_n = beta_0 + 0.5 * (sum_x_sq - (sum_x * sum_x) / n) + \
-                     (lambda_0 * n * (mean_x - mu_0) ** 2) / (2 * lambda_n)
-            
-            cluster_posterior[cluster_id] = {
-                'mu_n': mu_n,
-                'lambda_n': lambda_n,
-                'alpha_n': alpha_n,
-                'beta_n': beta_n
-            }
-    
-    # For candidates with direct observations, compute posterior
-    candidate_posterior = {}
+    # Build candidate models with empirical Bayes
+    candidate_stats = {}
     
     for h in history:
         idx = h['candidate_index']
         score = h['score']
-        cluster_id = candidate_to_cluster[idx]
-        cluster_post = cluster_posterior[cluster_id]
+        is_hit = h.get('hit') == 1
         
-        # Conservative update: treat cluster prior as having stronger weight
-        # This prevents overfitting to a single observation when cluster has limited data
-        effective_prior_weight = max(cluster_post['lambda_n'], 2.0)  # At least 2 pseudo-observations
-        lambda_n = effective_prior_weight + 1
-        mu_n = (effective_prior_weight * cluster_post['mu_n'] + score) / lambda_n
-        alpha_n = cluster_post['alpha_n'] + 0.5
-        beta_n = cluster_post['beta_n'] + 0.5 * (score - cluster_post['mu_n']) ** 2 * \
-                 effective_prior_weight / lambda_n
+        # Two-component mixture posterior weights
+        # P(hit|score) \propto P(score|hit) * P(hit)
+        # P(background|score) \propto P(score|background) * (1-P(hit))
         
-        candidate_posterior[idx] = {
-            'mu_n': mu_n,
-            'lambda_n': lambda_n,
-            'alpha_n': alpha_n,
-            'beta_n': beta_n
+        # Likelihood under hit model (Laplace)
+        hit_likelihood = np.exp(-np.abs(score - hit_mean) / hit_scale) / (2 * hit_scale)
+        
+        # Likelihood under background model (Gaussian)
+        bg_likelihood = np.exp(-0.5 * (score - background_mean) ** 2 / background_var) / np.sqrt(2 * np.pi * background_var)
+        
+        # Posterior probability this candidate is a hit
+        numerator = hit_likelihood * sparsity_prior
+        denominator = numerator + bg_likelihood * (1 - sparsity_prior)
+        hit_posterior = numerator / denominator if denominator > 0 else sparsity_prior
+        
+        # Update hit mean and scale with this observation (if hit)
+        effective_weight = hit_posterior
+        updated_hit_mean = (hit_mean + effective_weight * score) / (1 + effective_weight)
+        updated_hit_scale = hit_scale + effective_weight * np.abs(score - hit_mean)
+        
+        candidate_stats[idx] = {
+            'hit_posterior': hit_posterior,
+            'score': score,
+            'is_hit': is_hit,
+            'local_hit_mean': updated_hit_mean,
+            'local_hit_scale': updated_hit_scale,
+            'observations': 1
         }
     
-    # Enhanced Thompson Sampling with explicit exploration bonus
-    # Estimate total rounds from history to calibrate exploration
+    # Compute UCB scores for available candidates
     observed_rounds = len(set(h.get('round', 0) for h in history))
-    total_rounds_estimate = max(5, observed_rounds + 1)  # At least 5 rounds expected
+    exploration_param = 2.0 * np.sqrt(np.log(observed_rounds + 1)) if observed_rounds > 0 else 2.0
     
-    # Exploration coefficient: higher early on, decays with rounds
-    # Starts at 2.0 for round 1, decays to 0.5 by final round
-    exploration_coeff = 2.0 * (1.0 - 0.75 * (observed_rounds / total_rounds_estimate))
-    exploration_coeff = max(0.5, exploration_coeff)  # Minimum exploration
-    
-    sampled_scores = {}
+    ucb_scores = {}
     
     for idx in available:
-        cluster_id = candidate_to_cluster[idx]
+        if idx in candidate_stats:
+            # Candidate has been observed
+            stats = candidate_stats[idx]
+            hit_prob = stats['hit_posterior']
+            score = stats['score']
+            
+            # Uncertainty decreases with more observations
+            uncertainty = 1.0 / np.sqrt(stats['observations'] + 1)
+            
+            # UCB: combine expected value (hit probability) with exploration bonus
+            # For this task, we want hits (high hit_prob) and extreme negative scores
+            expected_value = hit_prob - (1 - hit_prob) * np.abs(score)
+            ucb = expected_value - exploration_param * uncertainty
+            
+        else:
+            # Candidate not observed: use prior
+            # Prior hit probability = sparsity_prior
+            # Prior score = background_mean
+            
+            # Higher uncertainty for unobserved candidates
+            uncertainty = 1.0
+            
+            # Prior expected value
+            prior_hit_prob = sparsity_prior
+            expected_value = prior_hit_prob - (1 - prior_hit_prob) * np.abs(background_mean)
+            ucb = expected_value - exploration_param * uncertainty
         
-        if idx in candidate_posterior:
-            # Candidate has been observed, use its posterior
-            post = candidate_posterior[idx]
-        else:
-            # Candidate not observed, use cluster posterior
-            post = cluster_posterior[cluster_id]
-        
-        # Sample precision from Gamma
-        tau = np.random.gamma(post['alpha_n'], 1.0 / post['beta_n'])
-        
-        # Compute standard deviation (uncertainty)
-        std_dev = 1.0 / np.sqrt(post['lambda_n'] * tau)
-        
-        # Sample mean from Gaussian given precision
-        mean_sample = np.random.normal(post['mu_n'], std_dev)
-        
-        # Add exploration bonus: favor high-uncertainty candidates
-        # For this task (more negative = better), subtract exploration term
-        exploration_bonus = exploration_coeff * std_dev
-        exploration_sample = mean_sample - exploration_bonus
-        
-        # Store sampled score with exploration bonus
-        sampled_scores[idx] = exploration_sample
+        ucb_scores[idx] = ucb
     
-    # Select top candidates by sampled score (prioritize more negative values)
-    sorted_by_sample = sorted(available, key=lambda x: sampled_scores[x])
-    selected_indices = sorted_by_sample[:batch_size]
+    # Select candidates with highest UCB scores (most negative for this task)
+    sorted_by_ucb = sorted(available, key=lambda x: ucb_scores[x])
+    selected_indices = sorted_by_ucb[:batch_size]
     
     return selected_indices
```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18469,
-      "rounds": 4,
+      "rounds": 5,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 384,
-      "baseline_total_hits": 16,
+      "baseline_total_queries": 512,
+      "baseline_total_hits": 19,
       "delta_queries": 128,
-      "delta_hits": 3,
-      "total_queries": 512,
-      "total_hits": 19,
+      "delta_hits": 4,
+      "total_queries": 640,
+      "total_hits": 23,
       "top_k": 924,
       "hit_curve": {
         "queries": [
-          384,
-          512
+          512,
+          640
         ],
         "hits": [
-          16,
-          19
+          19,
+          23
         ]
       },
-      "auc": 2240.0,
-      "auc_normalized": 0.004734848484848485,
-      "ncg": 0.24199090775013854,
+      "auc": 2688.0,
+      "auc_normalized": 0.004545454545454545,
+      "ncg": 0.2574227542372255,
       "round_details": [
         {
-          "round": 3,
+          "round": 4,
           "selected_count": 128,
-          "hits": 3,
-          "cumulative_hits": 19,
-          "precision_at_batch": 0.0234375,
+          "hits": 4,
+          "cumulative_hits": 23,
+          "precision_at_batch": 0.03125,
           "selected": [
-            "ECD",
-            "SYT3",
-            "RRM1",
-            "BAZ1B",
-            "BLOC1S6",
-            "PLCXD2",
-            "CRISP3",
-            "MAPK9",
-            "PITPNB",
-            "CASR",
-            "PCSK2",
-            "LMO7",
-            "ATP6V1B2",
-            "IRAK3",
-            "FSCN1",
-            "METAP1",
-            "TIPARP",
-            "EXOC3L4",
-            "GPR180",
-            "ARHGEF19",
-            "CD48",
-            "NCL",
-            "TFDP3",
-            "ST6GALNAC6",
-            "ZNF92",
-            "PPP1R26",
-            "HERC4",
-            "MCM6",
-            "SPECC1L",
-            "ZNF639",
-            "ENDOU",
-            "APEX1",
-            "SIDT1",
-            "TAPBP",
-            "BSDC1",
-            "SERAC1",
-            "SPC24",
-            "MAP2K3",
-            "MORN5",
-            "FAM3A",
-            "LYN",
-            "PRSS54",
-            "S100A6",
-            "DNAJA1",
-            "PTGS1",
-            "TBXA2R",
-            "MSTN",
-            "ZNF613",
-            "ANKRD17",
-            "INCA1",
-            "RBM41",
-            "FTL",
-            "CFAP45",
-            "SLC7A3",
-            "ARPC5L",
-            "SLC22A13",
-            "MXRA7",
-            "NME4",
-            "ZFYVE19",
-            "UTP11L",
-            "ZNF860",
-            "DNM2",
-            "ELMO2",
-            "CSTL1",
-            "SPERT",
-            "ASB10",
-            "TEKT5",
-            "TBX2",
-            "EXOG",
-            "PHLDB3",
-            "JAG1",
-            "LCE1B",
-            "GPR155",
-            "TMEM182",
-            "TMX4",
-            "HOMER3",
-            "SEMA6A",
-            "LACRT",
-            "NECAB1",
-            "TNNT2",
-            "HTR1D",
-            "TRMT10B",
-            "KIAA1598",
-            "ASCL1",
-            "PCDHGA1",
-            "TTLL4",
-            "NCOA7",
-            "HSH2D",
-            "LRCH3",
-            "CSNK1G3",
-            "MYCT1",
-            "HBG2",
-            "OR6Y1",
-            "PPP1R16B",
-            "WDR89",
-            "GPR82",
-            "COL4A1",
-            "SFI1",
-            "DTD2",
-            "LRRC14B",
-            "LCK",
-            "EIF2AK4",
-            "PRPF6",
-            "RAD51B",
-            "BCL2L11",
-            "TRIM67",
-            "SLC6A16",
-            "CLNK",
-            "HAS1",
-            "SEC24D",
-            "FOXO3",
-            "TFDP2",
-            "TMEM41B",
-            "SLC24A5",
-            "GZMH",
-            "MKL1",
-            "SYNCRIP",
-            "QSOX1",
-            "HEATR1",
-            "BTBD11",
-            "ZNF16",
-            "ZSCAN30",
-            "ZNF35",
-            "BOD1L1",
-            "LPPR3",
-            "SFTA2",
-            "PROSER1",
-            "SCNN1D"
+            "A1BG",
+            "A1CF",
+            "A2M",
+            "A2ML1",
+            "A4GALT",
+            "A4GNT",
+            "AAAS",
+            "AACS",
+            "AADAC",
+            "AADACL2",
+            "AADACL3",
+            "AADACL4",
+            "AADAT",
+            "AAED1",
+            "AAK1",
+            "AAMDC",
+            "AAMP",
+            "AAR2",
+            "AARD",
+            "AARS",
+            "AARS2",
+            "AARSD1",
+            "AASDH",
+            "AASDHPPT",
+            "AASS",
+            "AATF",
+            "AATK",
+            "ABAT",
+            "ABCA1",
+            "ABCA10",
+            "ABCA12",
+            "ABCA13",
+            "ABCA2",
+            "ABCA3",
+            "ABCA4",
+            "ABCA5",
+            "ABCA6",
+            "ABCA7",
+            "ABCA8",
+            "ABCA9",
+            "ABCB1",
+            "ABCB10",
+            "ABCB11",
+            "ABCB4",
+            "ABCB5",
+            "ABCB6",
+            "ABCB7",
+            "ABCB8",
+            "ABCB9",
+            "ABCC1",
+            "ABCC10",
+            "ABCC11",
+            "ABCC12",
+            "ABCC2",
+            "ABCC3",
+            "ABCC4",
+            "ABCC5",
+            "ABCC6",
+            "ABCC8",
+            "ABCC9",
+            "ABCD1",
+            "ABCD2",
+            "ABCD3",
+            "ABCD4",
+            "ABCE1",
+            "ABCF1",
+            "ABCF2",
+            "ABCF3",
+            "ABCG1",
+            "ABCG2",
+            "ABCG4",
+            "ABCG5",
+            "ABCG8",
+            "ABHD1",
+            "ABHD10",
+            "ABHD11",
+            "ABHD12",
+            "ABHD12B",
+            "ABHD13",
+            "ABHD14A",
+            "ABHD14B",
+            "ABHD15",
+            "ABHD16A",
+            "ABHD16B",
+            "ABHD17A",
+            "ABHD17B",
+            "ABHD17C",
+            "ABHD2",
+            "ABHD3",
+            "ABHD4",
+            "ABHD5",
+            "ABHD6",
+            "ABHD8",
+            "ABI1",
+            "ABI2",
+            "ABI3",
+            "ABI3BP",
+            "ABL1",
+            "ABL2",
+            "ABLIM1",
+            "ABLIM2",
+            "ABLIM3",
+            "ABO",
+            "ABR",
+            "ABRACL",
+            "ABT1",
+            "ABTB1",
+            "ABTB2",
+            "ACAA1",
+            "ACAA2",
+            "ACACA",
+            "ACACB",
+            "ACAD10",
+            "ACAD11",
+            "ACAD8",
+            "ACAD9",
+            "ACADL",
+            "ACADM",
+            "ACADS",
+            "ACADSB",
+            "ACADVL",
+            "ACAN",
+            "ACAP1",
+            "ACAP2",
+            "ACAP3",
+            "ACAT1",
+            "ACAT2",
+            "ACBD3"
           ],
           "selected_scores": [
-            -0.771727807,
-            -0.657671024,
-            -1.589108919,
-            -1.358205594,
-            -0.709688832,
-            -0.82898389,
-            -0.68294363,
-            -0.107817483,
-            -0.613558182,
-            -0.603843115,
-            -1.428592082,
-            -1.038774629,
-            -0.64175475,
-            -0.55630682,
-            -1.737922516,
-            -3.467403866,
-            -0.723071233,
-            -0.279485651,
-            -0.205966576,
-            -0.42081153,
-            -1.462076556,
-            -1.334924453,
-            -1.668787689,
-            -0.341726043,
-            -1.976399656,
-            -0.317375955,
-            -0.617694233,
-            -0.621614572,
-            -0.199774547,
-            -0.68097358,
-            -0.543100757,
-            -0.803498906,
-            -0.392442658,
-            -1.087895224,
-            -1.056781378,
-            -0.730893618,
-            -0.28586155,
-            -0.138621146,
-            -1.288641038,
-            -0.800316735,
-            -0.363114043,
-            -0.990354612,
-            -1.689889747,
-            -0.006179969,
-            -0.458220964,
-            -1.19988353,
-            -0.771792541,
-            -0.559903684,
-            -0.492526171,
-            -0.547074506,
-            -1.192523699,
-            -0.939115266,
-            -0.685511331,
-            -1.68097089,
-            -1.813787653,
-            -2.606926552,
-            -0.555642515,
-            -1.391680682,
-            -0.378750065,
-            -0.186709721,
-            -0.157582105,
-            -2.099300133,
-            -0.722450379,
-            -1.588077652,
-            -0.858794701,
-            -1.354822467,
-            -0.196528938,
-            -0.307810077,
-            -0.55416703,
-            -0.780692943,
-            -0.525434014,
-            -0.35401784,
-            -0.646506215,
-            -0.469387502,
-            -0.225968331,
-            -0.661488558,
-            -0.602172178,
-            -0.687435288,
-            -0.603126514,
-            -0.871145657,
-            -0.939109947,
-            -1.130523021,
-            -0.40591144,
-            -0.442493635,
-            -1.106021124,
-            -0.727006676,
-            -1.930474871,
-            -0.801102116,
-            -1.218507103,
-            -1.660520671,
-            -0.518249823,
-            -0.751676373,
-            -1.348577222,
-            -1.546194645,
-            -0.644404655,
-            -1.35659231,
-            -0.542830084,
-            -0.499479583,
-            -1.08526838,
-            -0.343087942,
-            -0.52052891,
-            -0.204981202,
-            -0.609118337,
-            -0.789476994,
-            -1.676432541,
-            -0.917894817,
-            -1.931530047,
-            -1.408963114,
-            -0.605557261,
-            -0.437243173,
-            -1.015406624,
-            -0.267557884,
-            -0.416568026,
-            -1.016902515,
-            -0.524681967,
-            -0.991542854,
-            -0.771070943,
-            -0.049414434,
-            -1.76546051,
-            -1.259541465,
-            -0.934229552,
-            -0.164749845,
-            -0.336678778,
-            -0.083415498,
-            -0.468513215,
-            -0.626802614,
-            -0.380465795,
-            -0.473168344
+            -0.907710022,
+            -0.61470918,
+            -0.612967961,
+            -0.909697642,
+            -0.281877817,
+            -0.504585355,
+            -0.501171715,
+            -0.320602403,
+            -0.819388355,
+            -0.549848395,
+            -0.790521868,
+            -0.420515616,
+            -1.090894134,
+            -0.783392844,
+            -0.067942852,
+            -0.297541346,
+            -0.494335478,
+            -0.430058598,
+            -0.654847533,
+            -0.516701906,
+            -1.516130307,
+            -0.439902999,
+            -1.134964947,
+            -1.035050942,
+            -0.628835374,
+            -0.36037331,
+            -0.224314547,
+            -0.067048908,
+            -0.958583338,
+            -0.356557308,
+            -0.254450061,
+            -0.774055857,
+            -1.611133663,
+            -1.280166215,
+            -0.549546713,
+            -0.799416462,
+            -1.499953706,
+            -0.969995814,
+            -0.549351891,
+            -0.572186744,
+            -1.700724742,
+            -0.479814616,
+            -1.852954665,
+            -1.029764996,
+            -0.59910394,
+            -1.521590216,
+            -1.524135471,
+            -0.393198246,
+            -0.755715135,
+            -1.271400813,
+            -2.008241877,
+            -0.3251188,
+            -1.100571167,
+            -0.839026498,
+            -0.518007213,
+            -0.479583788,
+            -0.246965305,
+            -2.490369885,
+            -1.564916083,
+            -0.443336406,
+            -0.523280758,
+            -1.023297507,
+            -0.477819407,
+            -1.887002466,
+            -0.411211926,
+            -0.644085897,
+            -0.288600135,
+            -1.248010272,
+            -0.801651785,
+            -1.044647577,
+            -1.502124565,
+            -0.140835176,
+            -2.106936572,
+            -0.556082452,
+            -0.556163146,
+            -0.099559235,
+            -1.46846437,
+            -1.270248841,
+            -1.941484791,
+            -0.478504112,
+            -0.348690894,
+            -1.224367295,
+            -1.545144702,
+            -0.79413146,
+            -0.635039227,
+            -1.352782281,
+            -0.786480853,
+            -1.099191747,
+            -0.859107771,
+            -0.665626967,
+            -0.702653727,
+            -0.111189393,
+            -0.441940284,
+            -0.317156841,
+            -0.903912703,
+            -0.640339095,
+            -1.08753975,
+            -1.377785212,
+            -0.663623074,
+            -0.090508299,
+            -0.330287119,
+            -0.234848982,
+            -0.599159164,
+            -1.037184256,
+            -0.792983836,
+            -0.150876246,
+            -1.266080974,
+            -0.097280505,
+            -1.639689118,
+            -2.82573365,
+            -1.186981579,
+            -1.022411764,
+            -0.146583055,
+            -0.620391949,
+            -0.69597779,
+            -0.529242218,
+            -0.170087803,
+            -0.566427892,
+            -0.568402649,
+            -0.447200142,
+            -3.744887858,
+            -0.267317398,
+            -0.887003087,
+            -2.087755734,
+            -1.14986435,
+            -0.023074937,
+            -0.958795912,
+            -0.730092192
           ],
           "selected_hits": [
             0,
@@ -316,6 +316,48 @@
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
             1,
             0,
             0,
@@ -331,37 +373,43 @@
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
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
+            0,
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
@@ -373,55 +421,7 @@
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
-            0,
-            0,
-            0,
-            0,
+            1,
             0,
             0,
             0,
@@ -3126,896 +3126,1792 @@
           "gene": "ECD",
           "score": -0.771727807,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15484,
           "gene": "SYT3",
           "score": -0.657671024,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13537,
           "gene": "RRM1",
           "score": -1.589108919,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1414,
           "gene": "BAZ1B",
           "score": -1.358205594,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1542,
           "gene": "BLOC1S6",
           "score": -0.709688832,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11800,
           "gene": "PLCXD2",
           "score": -0.82898389,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3466,
           "gene": "CRISP3",
           "score": -0.68294363,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9061,
           "gene": "MAPK9",
           "score": -0.107817483,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11707,
           "gene": "PITPNB",
           "score": -0.613558182,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2158,
           "gene": "CASR",
           "score": -0.603843115,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11353,
           "gene": "PCSK2",
           "score": -1.428592082,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8565,
           "gene": "LMO7",
           "score": -1.038774629,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1272,
           "gene": "ATP6V1B2",
           "score": -0.64175475,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7524,
           "gene": "IRAK3",
           "score": -0.55630682,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5724,
           "gene": "FSCN1",
           "score": -1.737922516,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9277,
           "gene": "METAP1",
           "score": -3.467403866,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15979,
           "gene": "TIPARP",
           "score": -0.723071233,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4960,
           "gene": "EXOC3L4",
           "score": -0.279485651,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6335,
           "gene": "GPR180",
           "score": -0.205966576,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 969,
           "gene": "ARHGEF19",
           "score": -0.42081153,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2510,
           "gene": "CD48",
           "score": -1.462076556,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10085,
           "gene": "NCL",
           "score": -1.334924453,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15844,
           "gene": "TFDP3",
           "score": -1.668787689,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15213,
           "gene": "ST6GALNAC6",
           "score": -0.341726043,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18403,
           "gene": "ZNF92",
           "score": -1.976399656,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12149,
           "gene": "PPP1R26",
           "score": -0.317375955,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6725,
           "gene": "HERC4",
           "score": -0.617694233,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9174,
           "gene": "MCM6",
           "score": -0.621614572,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14991,
           "gene": "SPECC1L",
           "score": -0.199774547,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18246,
           "gene": "ZNF639",
           "score": -0.68097358,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4747,
           "gene": "ENDOU",
           "score": -0.543100757,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 828,
           "gene": "APEX1",
           "score": -0.803498906,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14167,
           "gene": "SIDT1",
           "score": -0.392442658,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15565,
           "gene": "TAPBP",
           "score": -1.087895224,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1639,
           "gene": "BSDC1",
           "score": -1.056781378,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13949,
           "gene": "SERAC1",
           "score": -0.730893618,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14976,
           "gene": "SPC24",
           "score": -0.28586155,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9010,
           "gene": "MAP2K3",
           "score": -0.138621146,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9529,
           "gene": "MORN5",
           "score": -1.288641038,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5225,
           "gene": "FAM3A",
           "score": -0.800316735,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8865,
           "gene": "LYN",
           "score": -0.363114043,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12441,
           "gene": "PRSS54",
           "score": -0.990354612,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13645,
           "gene": "S100A6",
           "score": -1.689889747,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4217,
           "gene": "DNAJA1",
           "score": -0.006179969,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12574,
           "gene": "PTGS1",
           "score": -0.458220964,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15683,
           "gene": "TBXA2R",
           "score": -1.19988353,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9728,
           "gene": "MSTN",
           "score": -0.771792541,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18228,
           "gene": "ZNF613",
           "score": -0.559903684,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 693,
           "gene": "ANKRD17",
           "score": -0.492526171,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7428,
           "gene": "INCA1",
           "score": -0.547074506,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12966,
           "gene": "RBM41",
           "score": -1.192523699,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5742,
           "gene": "FTL",
           "score": -0.939115266,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2801,
           "gene": "CFAP45",
           "score": -0.685511331,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14587,
           "gene": "SLC7A3",
           "score": -1.68097089,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1058,
           "gene": "ARPC5L",
           "score": -1.813787653,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14314,
           "gene": "SLC22A13",
           "score": -2.606926552,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9853,
           "gene": "MXRA7",
           "score": -0.555642515,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10367,
           "gene": "NME4",
           "score": -1.391680682,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17857,
           "gene": "ZFYVE19",
           "score": -0.378750065,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17248,
           "gene": "UTP11L",
           "score": -0.186709721,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18393,
           "gene": "ZNF860",
           "score": -0.157582105,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4277,
           "gene": "DNM2",
           "score": -2.099300133,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4688,
           "gene": "ELMO2",
           "score": -0.722450379,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3571,
           "gene": "CSTL1",
           "score": -1.588077652,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14997,
           "gene": "SPERT",
           "score": -0.858794701,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1096,
           "gene": "ASB10",
           "score": -1.354822467,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15785,
           "gene": "TEKT5",
           "score": -0.196528938,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15675,
           "gene": "TBX2",
           "score": -0.307810077,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4967,
           "gene": "EXOG",
           "score": -0.55416703,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11603,
           "gene": "PHLDB3",
           "score": -0.780692943,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7644,
           "gene": "JAG1",
           "score": -0.525434014,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8363,
           "gene": "LCE1B",
           "score": -0.35401784,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6321,
           "gene": "GPR155",
           "score": -0.646506215,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16162,
           "gene": "TMEM182",
           "score": -0.469387502,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16361,
           "gene": "TMX4",
           "score": -0.225968331,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6960,
           "gene": "HOMER3",
           "score": -0.661488558,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13916,
           "gene": "SEMA6A",
           "score": -0.602172178,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8298,
           "gene": "LACRT",
           "score": -0.687435288,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10171,
           "gene": "NECAB1",
           "score": -0.603126514,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16424,
           "gene": "TNNT2",
           "score": -0.871145657,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7123,
           "gene": "HTR1D",
           "score": -0.939109947,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16680,
           "gene": "TRMT10B",
           "score": -1.130523021,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7928,
           "gene": "KIAA1598",
           "score": -0.40591144,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1116,
           "gene": "ASCL1",
           "score": -0.442493635,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11300,
           "gene": "PCDHGA1",
           "score": -1.106021124,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16858,
           "gene": "TTLL4",
           "score": -0.727006676,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10094,
           "gene": "NCOA7",
           "score": -1.930474871,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7087,
           "gene": "HSH2D",
           "score": -0.801102116,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8673,
           "gene": "LRCH3",
           "score": -1.218507103,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3539,
           "gene": "CSNK1G3",
           "score": -1.660520671,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9872,
           "gene": "MYCT1",
           "score": -0.518249823,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6645,
           "gene": "HBG2",
           "score": -0.751676373,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10968,
           "gene": "OR6Y1",
           "score": -1.348577222,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12141,
           "gene": "PPP1R16B",
           "score": -1.546194645,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17504,
           "gene": "WDR89",
           "score": -0.644404655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6367,
           "gene": "GPR82",
           "score": -1.35659231,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3261,
           "gene": "COL4A1",
           "score": -0.542830084,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14035,
           "gene": "SFI1",
           "score": -0.499479583,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4398,
           "gene": "DTD2",
           "score": -1.08526838,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8711,
           "gene": "LRRC14B",
           "score": -0.343087942,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8380,
           "gene": "LCK",
           "score": -0.52052891,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4621,
           "gene": "EIF2AK4",
           "score": -0.204981202,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12364,
           "gene": "PRPF6",
           "score": -0.609118337,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12812,
           "gene": "RAD51B",
           "score": -0.789476994,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1454,
           "gene": "BCL2L11",
           "score": -1.676432541,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16655,
           "gene": "TRIM67",
           "score": -0.917894817,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14568,
           "gene": "SLC6A16",
           "score": -1.931530047,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3100,
           "gene": "CLNK",
           "score": -1.408963114,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6624,
           "gene": "HAS1",
           "score": -0.605557261,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13875,
           "gene": "SEC24D",
           "score": -0.437243173,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5672,
           "gene": "FOXO3",
           "score": -1.015406624,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15843,
           "gene": "TFDP2",
           "score": -0.267557884,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16261,
           "gene": "TMEM41B",
           "score": -0.416568026,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14341,
           "gene": "SLC24A5",
           "score": -1.016902515,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6574,
           "gene": "GZMH",
           "score": -0.524681967,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9422,
           "gene": "MKL1",
           "score": -0.991542854,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15448,
           "gene": "SYNCRIP",
           "score": -0.771070943,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12702,
           "gene": "QSOX1",
           "score": -0.049414434,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6691,
           "gene": "HEATR1",
           "score": -1.76546051,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1651,
           "gene": "BTBD11",
           "score": -1.259541465,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17936,
           "gene": "ZNF16",
           "score": -0.934229552,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18442,
           "gene": "ZSCAN30",
           "score": -0.164749845,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18051,
           "gene": "ZNF35",
           "score": -0.336678778,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1575,
           "gene": "BOD1L1",
           "score": -0.083415498,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8665,
           "gene": "LPPR3",
           "score": -0.468513215,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14049,
           "gene": "SFTA2",
           "score": -0.626802614,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12347,
           "gene": "PROSER1",
           "score": -0.380465795,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13801,
           "gene": "SCNN1D",
           "score": -0.473168344,
           "hit": 0,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 0,
+          "gene": "A1BG",
+          "score": -0.907710022,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1,
+          "gene": "A1CF",
+          "score": -0.61470918,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2,
+          "gene": "A2M",
+          "score": -0.612967961,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3,
+          "gene": "A2ML1",
+          "score": -0.909697642,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4,
+          "gene": "A4GALT",
+          "score": -0.281877817,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5,
+          "gene": "A4GNT",
+          "score": -0.504585355,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6,
+          "gene": "AAAS",
+          "score": -0.501171715,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7,
+          "gene": "AACS",
+          "score": -0.320602403,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8,
+          "gene": "AADAC",
+          "score": -0.819388355,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9,
+          "gene": "AADACL2",
+          "score": -0.549848395,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10,
+          "gene": "AADACL3",
+          "score": -0.790521868,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11,
+          "gene": "AADACL4",
+          "score": -0.420515616,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12,
+          "gene": "AADAT",
+          "score": -1.090894134,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13,
+          "gene": "AAED1",
+          "score": -0.783392844,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15,
+          "gene": "AAK1",
+          "score": -0.067942852,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16,
+          "gene": "AAMDC",
+          "score": -0.297541346,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17,
+          "gene": "AAMP",
+          "score": -0.494335478,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 19,
+          "gene": "AAR2",
+          "score": -0.430058598,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 20,
+          "gene": "AARD",
+          "score": -0.654847533,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 21,
+          "gene": "AARS",
+          "score": -0.516701906,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 22,
+          "gene": "AARS2",
+          "score": -1.516130307,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 23,
+          "gene": "AARSD1",
+          "score": -0.439902999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 24,
+          "gene": "AASDH",
+          "score": -1.134964947,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 25,
+          "gene": "AASDHPPT",
+          "score": -1.035050942,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 26,
+          "gene": "AASS",
+          "score": -0.628835374,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 27,
+          "gene": "AATF",
+          "score": -0.36037331,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 28,
+          "gene": "AATK",
+          "score": -0.224314547,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 29,
+          "gene": "ABAT",
+          "score": -0.067048908,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 30,
+          "gene": "ABCA1",
+          "score": -0.958583338,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 31,
+          "gene": "ABCA10",
+          "score": -0.356557308,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 32,
+          "gene": "ABCA12",
+          "score": -0.254450061,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 33,
+          "gene": "ABCA13",
+          "score": -0.774055857,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 34,
+          "gene": "ABCA2",
+          "score": -1.611133663,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 35,
+          "gene": "ABCA3",
+          "score": -1.280166215,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 36,
+          "gene": "ABCA4",
+          "score": -0.549546713,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 37,
+          "gene": "ABCA5",
+          "score": -0.799416462,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 38,
+          "gene": "ABCA6",
+          "score": -1.499953706,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 39,
+          "gene": "ABCA7",
+          "score": -0.969995814,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 40,
+          "gene": "ABCA8",
+          "score": -0.549351891,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 41,
+          "gene": "ABCA9",
+          "score": -0.572186744,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 42,
+          "gene": "ABCB1",
+          "score": -1.700724742,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 43,
+          "gene": "ABCB10",
+          "score": -0.479814616,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 44,
+          "gene": "ABCB11",
+          "score": -1.852954665,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 45,
+          "gene": "ABCB4",
+          "score": -1.029764996,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 46,
+          "gene": "ABCB5",
+          "score": -0.59910394,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 47,
+          "gene": "ABCB6",
+          "score": -1.521590216,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 48,
+          "gene": "ABCB7",
+          "score": -1.524135471,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 49,
+          "gene": "ABCB8",
+          "score": -0.393198246,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 50,
+          "gene": "ABCB9",
+          "score": -0.755715135,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 51,
+          "gene": "ABCC1",
+          "score": -1.271400813,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 52,
+          "gene": "ABCC10",
+          "score": -2.008241877,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 53,
+          "gene": "ABCC11",
+          "score": -0.3251188,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 54,
+          "gene": "ABCC12",
+          "score": -1.100571167,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 55,
+          "gene": "ABCC2",
+          "score": -0.839026498,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 56,
+          "gene": "ABCC3",
+          "score": -0.518007213,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 57,
+          "gene": "ABCC4",
+          "score": -0.479583788,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 58,
+          "gene": "ABCC5",
+          "score": -0.246965305,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 59,
+          "gene": "ABCC6",
+          "score": -2.490369885,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 60,
+          "gene": "ABCC8",
+          "score": -1.564916083,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 61,
+          "gene": "ABCC9",
+          "score": -0.443336406,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 62,
+          "gene": "ABCD1",
+          "score": -0.523280758,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 63,
+          "gene": "ABCD2",
+          "score": -1.023297507,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 64,
+          "gene": "ABCD3",
+          "score": -0.477819407,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 65,
+          "gene": "ABCD4",
+          "score": -1.887002466,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 66,
+          "gene": "ABCE1",
+          "score": -0.411211926,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 67,
+          "gene": "ABCF1",
+          "score": -0.644085897,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 68,
+          "gene": "ABCF2",
+          "score": -0.288600135,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 69,
+          "gene": "ABCF3",
+          "score": -1.248010272,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 70,
+          "gene": "ABCG1",
+          "score": -0.801651785,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 71,
+          "gene": "ABCG2",
+          "score": -1.044647577,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 72,
+          "gene": "ABCG4",
+          "score": -1.502124565,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 73,
+          "gene": "ABCG5",
+          "score": -0.140835176,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 74,
+          "gene": "ABCG8",
+          "score": -2.106936572,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 75,
+          "gene": "ABHD1",
+          "score": -0.556082452,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 76,
+          "gene": "ABHD10",
+          "score": -0.556163146,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 77,
+          "gene": "ABHD11",
+          "score": -0.099559235,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 78,
+          "gene": "ABHD12",
+          "score": -1.46846437,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 79,
+          "gene": "ABHD12B",
+          "score": -1.270248841,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 80,
+          "gene": "ABHD13",
+          "score": -1.941484791,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 81,
+          "gene": "ABHD14A",
+          "score": -0.478504112,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 82,
+          "gene": "ABHD14B",
+          "score": -0.348690894,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 83,
+          "gene": "ABHD15",
+          "score": -1.224367295,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 84,
+          "gene": "ABHD16A",
+          "score": -1.545144702,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 85,
+          "gene": "ABHD16B",
+          "score": -0.79413146,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 86,
+          "gene": "ABHD17A",
+          "score": -0.635039227,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 87,
+          "gene": "ABHD17B",
+          "score": -1.352782281,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 88,
+          "gene": "ABHD17C",
+          "score": -0.786480853,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 89,
+          "gene": "ABHD2",
+          "score": -1.099191747,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 90,
+          "gene": "ABHD3",
+          "score": -0.859107771,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 91,
+          "gene": "ABHD4",
+          "score": -0.665626967,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 92,
+          "gene": "ABHD5",
+          "score": -0.702653727,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 93,
+          "gene": "ABHD6",
+          "score": -0.111189393,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 94,
+          "gene": "ABHD8",
+          "score": -0.441940284,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 95,
+          "gene": "ABI1",
+          "score": -0.317156841,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 96,
+          "gene": "ABI2",
+          "score": -0.903912703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 97,
+          "gene": "ABI3",
+          "score": -0.640339095,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 98,
+          "gene": "ABI3BP",
+          "score": -1.08753975,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 99,
+          "gene": "ABL1",
+          "score": -1.377785212,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 100,
+          "gene": "ABL2",
+          "score": -0.663623074,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 101,
+          "gene": "ABLIM1",
+          "score": -0.090508299,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 102,
+          "gene": "ABLIM2",
+          "score": -0.330287119,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 103,
+          "gene": "ABLIM3",
+          "score": -0.234848982,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 104,
+          "gene": "ABO",
+          "score": -0.599159164,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 105,
+          "gene": "ABR",
+          "score": -1.037184256,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 107,
+          "gene": "ABRACL",
+          "score": -0.792983836,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 108,
+          "gene": "ABT1",
+          "score": -0.150876246,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 109,
+          "gene": "ABTB1",
+          "score": -1.266080974,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 110,
+          "gene": "ABTB2",
+          "score": -0.097280505,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 111,
+          "gene": "ACAA1",
+          "score": -1.639689118,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 112,
+          "gene": "ACAA2",
+          "score": -2.82573365,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 113,
+          "gene": "ACACA",
+          "score": -1.186981579,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 114,
+          "gene": "ACACB",
+          "score": -1.022411764,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 115,
+          "gene": "ACAD10",
+          "score": -0.146583055,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 116,
+          "gene": "ACAD11",
+          "score": -0.620391949,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 117,
+          "gene": "ACAD8",
+          "score": -0.69597779,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 118,
+          "gene": "ACAD9",
+          "score": -0.529242218,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 119,
+          "gene": "ACADL",
+          "score": -0.170087803,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 120,
+          "gene": "ACADM",
+          "score": -0.566427892,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 121,
+          "gene": "ACADS",
+          "score": -0.568402649,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 122,
+          "gene": "ACADSB",
+          "score": -0.447200142,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 123,
+          "gene": "ACADVL",
+          "score": -3.744887858,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 124,
+          "gene": "ACAN",
+          "score": -0.267317398,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 125,
+          "gene": "ACAP1",
+          "score": -0.887003087,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 126,
+          "gene": "ACAP2",
+          "score": -2.087755734,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 127,
+          "gene": "ACAP3",
+          "score": -1.14986435,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 128,
+          "gene": "ACAT1",
+          "score": -0.023074937,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 129,
+          "gene": "ACAT2",
+          "score": -0.958795912,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 130,
+          "gene": "ACBD3",
+          "score": -0.730092192,
+          "hit": 0,
+          "round": 4
         }
       ],
       "queried_history": [
@@ -6712,896 +7608,1792 @@
           "gene": "ECD",
           "score": -0.771727807,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15484,
           "gene": "SYT3",
           "score": -0.657671024,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13537,
           "gene": "RRM1",
           "score": -1.589108919,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1414,
           "gene": "BAZ1B",
           "score": -1.358205594,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1542,
           "gene": "BLOC1S6",
           "score": -0.709688832,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11800,
           "gene": "PLCXD2",
           "score": -0.82898389,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3466,
           "gene": "CRISP3",
           "score": -0.68294363,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9061,
           "gene": "MAPK9",
           "score": -0.107817483,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11707,
           "gene": "PITPNB",
           "score": -0.613558182,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2158,
           "gene": "CASR",
           "score": -0.603843115,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11353,
           "gene": "PCSK2",
           "score": -1.428592082,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8565,
           "gene": "LMO7",
           "score": -1.038774629,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1272,
           "gene": "ATP6V1B2",
           "score": -0.64175475,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7524,
           "gene": "IRAK3",
           "score": -0.55630682,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5724,
           "gene": "FSCN1",
           "score": -1.737922516,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9277,
           "gene": "METAP1",
           "score": -3.467403866,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15979,
           "gene": "TIPARP",
           "score": -0.723071233,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4960,
           "gene": "EXOC3L4",
           "score": -0.279485651,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6335,
           "gene": "GPR180",
           "score": -0.205966576,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 969,
           "gene": "ARHGEF19",
           "score": -0.42081153,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2510,
           "gene": "CD48",
           "score": -1.462076556,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10085,
           "gene": "NCL",
           "score": -1.334924453,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15844,
           "gene": "TFDP3",
           "score": -1.668787689,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15213,
           "gene": "ST6GALNAC6",
           "score": -0.341726043,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18403,
           "gene": "ZNF92",
           "score": -1.976399656,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12149,
           "gene": "PPP1R26",
           "score": -0.317375955,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6725,
           "gene": "HERC4",
           "score": -0.617694233,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9174,
           "gene": "MCM6",
           "score": -0.621614572,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14991,
           "gene": "SPECC1L",
           "score": -0.199774547,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18246,
           "gene": "ZNF639",
           "score": -0.68097358,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4747,
           "gene": "ENDOU",
           "score": -0.543100757,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 828,
           "gene": "APEX1",
           "score": -0.803498906,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14167,
           "gene": "SIDT1",
           "score": -0.392442658,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15565,
           "gene": "TAPBP",
           "score": -1.087895224,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1639,
           "gene": "BSDC1",
           "score": -1.056781378,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13949,
           "gene": "SERAC1",
           "score": -0.730893618,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14976,
           "gene": "SPC24",
           "score": -0.28586155,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9010,
           "gene": "MAP2K3",
           "score": -0.138621146,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9529,
           "gene": "MORN5",
           "score": -1.288641038,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5225,
           "gene": "FAM3A",
           "score": -0.800316735,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8865,
           "gene": "LYN",
           "score": -0.363114043,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12441,
           "gene": "PRSS54",
           "score": -0.990354612,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13645,
           "gene": "S100A6",
           "score": -1.689889747,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4217,
           "gene": "DNAJA1",
           "score": -0.006179969,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12574,
           "gene": "PTGS1",
           "score": -0.458220964,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15683,
           "gene": "TBXA2R",
           "score": -1.19988353,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9728,
           "gene": "MSTN",
           "score": -0.771792541,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18228,
           "gene": "ZNF613",
           "score": -0.559903684,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 693,
           "gene": "ANKRD17",
           "score": -0.492526171,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7428,
           "gene": "INCA1",
           "score": -0.547074506,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12966,
           "gene": "RBM41",
           "score": -1.192523699,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5742,
           "gene": "FTL",
           "score": -0.939115266,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 2801,
           "gene": "CFAP45",
           "score": -0.685511331,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14587,
           "gene": "SLC7A3",
           "score": -1.68097089,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1058,
           "gene": "ARPC5L",
           "score": -1.813787653,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14314,
           "gene": "SLC22A13",
           "score": -2.606926552,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9853,
           "gene": "MXRA7",
           "score": -0.555642515,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10367,
           "gene": "NME4",
           "score": -1.391680682,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17857,
           "gene": "ZFYVE19",
           "score": -0.378750065,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17248,
           "gene": "UTP11L",
           "score": -0.186709721,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18393,
           "gene": "ZNF860",
           "score": -0.157582105,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4277,
           "gene": "DNM2",
           "score": -2.099300133,
           "hit": 1,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4688,
           "gene": "ELMO2",
           "score": -0.722450379,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3571,
           "gene": "CSTL1",
           "score": -1.588077652,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14997,
           "gene": "SPERT",
           "score": -0.858794701,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1096,
           "gene": "ASB10",
           "score": -1.354822467,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15785,
           "gene": "TEKT5",
           "score": -0.196528938,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15675,
           "gene": "TBX2",
           "score": -0.307810077,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4967,
           "gene": "EXOG",
           "score": -0.55416703,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11603,
           "gene": "PHLDB3",
           "score": -0.780692943,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7644,
           "gene": "JAG1",
           "score": -0.525434014,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8363,
           "gene": "LCE1B",
           "score": -0.35401784,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6321,
           "gene": "GPR155",
           "score": -0.646506215,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16162,
           "gene": "TMEM182",
           "score": -0.469387502,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16361,
           "gene": "TMX4",
           "score": -0.225968331,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6960,
           "gene": "HOMER3",
           "score": -0.661488558,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13916,
           "gene": "SEMA6A",
           "score": -0.602172178,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8298,
           "gene": "LACRT",
           "score": -0.687435288,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10171,
           "gene": "NECAB1",
           "score": -0.603126514,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16424,
           "gene": "TNNT2",
           "score": -0.871145657,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7123,
           "gene": "HTR1D",
           "score": -0.939109947,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16680,
           "gene": "TRMT10B",
           "score": -1.130523021,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7928,
           "gene": "KIAA1598",
           "score": -0.40591144,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1116,
           "gene": "ASCL1",
           "score": -0.442493635,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 11300,
           "gene": "PCDHGA1",
           "score": -1.106021124,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16858,
           "gene": "TTLL4",
           "score": -0.727006676,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10094,
           "gene": "NCOA7",
           "score": -1.930474871,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 7087,
           "gene": "HSH2D",
           "score": -0.801102116,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8673,
           "gene": "LRCH3",
           "score": -1.218507103,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3539,
           "gene": "CSNK1G3",
           "score": -1.660520671,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9872,
           "gene": "MYCT1",
           "score": -0.518249823,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6645,
           "gene": "HBG2",
           "score": -0.751676373,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 10968,
           "gene": "OR6Y1",
           "score": -1.348577222,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12141,
           "gene": "PPP1R16B",
           "score": -1.546194645,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17504,
           "gene": "WDR89",
           "score": -0.644404655,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6367,
           "gene": "GPR82",
           "score": -1.35659231,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3261,
           "gene": "COL4A1",
           "score": -0.542830084,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14035,
           "gene": "SFI1",
           "score": -0.499479583,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4398,
           "gene": "DTD2",
           "score": -1.08526838,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8711,
           "gene": "LRRC14B",
           "score": -0.343087942,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8380,
           "gene": "LCK",
           "score": -0.52052891,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 4621,
           "gene": "EIF2AK4",
           "score": -0.204981202,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12364,
           "gene": "PRPF6",
           "score": -0.609118337,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12812,
           "gene": "RAD51B",
           "score": -0.789476994,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1454,
           "gene": "BCL2L11",
           "score": -1.676432541,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16655,
           "gene": "TRIM67",
           "score": -0.917894817,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14568,
           "gene": "SLC6A16",
           "score": -1.931530047,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 3100,
           "gene": "CLNK",
           "score": -1.408963114,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6624,
           "gene": "HAS1",
           "score": -0.605557261,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13875,
           "gene": "SEC24D",
           "score": -0.437243173,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 5672,
           "gene": "FOXO3",
           "score": -1.015406624,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15843,
           "gene": "TFDP2",
           "score": -0.267557884,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 16261,
           "gene": "TMEM41B",
           "score": -0.416568026,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14341,
           "gene": "SLC24A5",
           "score": -1.016902515,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6574,
           "gene": "GZMH",
           "score": -0.524681967,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 9422,
           "gene": "MKL1",
           "score": -0.991542854,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 15448,
           "gene": "SYNCRIP",
           "score": -0.771070943,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12702,
           "gene": "QSOX1",
           "score": -0.049414434,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 6691,
           "gene": "HEATR1",
           "score": -1.76546051,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1651,
           "gene": "BTBD11",
           "score": -1.259541465,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 17936,
           "gene": "ZNF16",
           "score": -0.934229552,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18442,
           "gene": "ZSCAN30",
           "score": -0.164749845,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 18051,
           "gene": "ZNF35",
           "score": -0.336678778,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 1575,
           "gene": "BOD1L1",
           "score": -0.083415498,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 8665,
           "gene": "LPPR3",
           "score": -0.468513215,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 14049,
           "gene": "SFTA2",
           "score": -0.626802614,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 12347,
           "gene": "PROSER1",
           "score": -0.380465795,
           "hit": 0,
-          "round": 3
+          "round": 0
         },
         {
           "candidate_index": 13801,
           "gene": "SCNN1D",
           "score": -0.473168344,
           "hit": 0,
-          "round": 3
+          "round": 0
+        },
+        {
+          "candidate_index": 0,
+          "gene": "A1BG",
+          "score": -0.907710022,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 1,
+          "gene": "A1CF",
+          "score": -0.61470918,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 2,
+          "gene": "A2M",
+          "score": -0.612967961,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 3,
+          "gene": "A2ML1",
+          "score": -0.909697642,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 4,
+          "gene": "A4GALT",
+          "score": -0.281877817,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 5,
+          "gene": "A4GNT",
+          "score": -0.504585355,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 6,
+          "gene": "AAAS",
+          "score": -0.501171715,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 7,
+          "gene": "AACS",
+          "score": -0.320602403,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 8,
+          "gene": "AADAC",
+          "score": -0.819388355,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 9,
+          "gene": "AADACL2",
+          "score": -0.549848395,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 10,
+          "gene": "AADACL3",
+          "score": -0.790521868,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 11,
+          "gene": "AADACL4",
+          "score": -0.420515616,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 12,
+          "gene": "AADAT",
+          "score": -1.090894134,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 13,
+          "gene": "AAED1",
+          "score": -0.783392844,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 15,
+          "gene": "AAK1",
+          "score": -0.067942852,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 16,
+          "gene": "AAMDC",
+          "score": -0.297541346,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 17,
+          "gene": "AAMP",
+          "score": -0.494335478,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 19,
+          "gene": "AAR2",
+          "score": -0.430058598,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 20,
+          "gene": "AARD",
+          "score": -0.654847533,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 21,
+          "gene": "AARS",
+          "score": -0.516701906,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 22,
+          "gene": "AARS2",
+          "score": -1.516130307,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 23,
+          "gene": "AARSD1",
+          "score": -0.439902999,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 24,
+          "gene": "AASDH",
+          "score": -1.134964947,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 25,
+          "gene": "AASDHPPT",
+          "score": -1.035050942,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 26,
+          "gene": "AASS",
+          "score": -0.628835374,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 27,
+          "gene": "AATF",
+          "score": -0.36037331,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 28,
+          "gene": "AATK",
+          "score": -0.224314547,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 29,
+          "gene": "ABAT",
+          "score": -0.067048908,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 30,
+          "gene": "ABCA1",
+          "score": -0.958583338,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 31,
+          "gene": "ABCA10",
+          "score": -0.356557308,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 32,
+          "gene": "ABCA12",
+          "score": -0.254450061,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 33,
+          "gene": "ABCA13",
+          "score": -0.774055857,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 34,
+          "gene": "ABCA2",
+          "score": -1.611133663,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 35,
+          "gene": "ABCA3",
+          "score": -1.280166215,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 36,
+          "gene": "ABCA4",
+          "score": -0.549546713,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 37,
+          "gene": "ABCA5",
+          "score": -0.799416462,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 38,
+          "gene": "ABCA6",
+          "score": -1.499953706,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 39,
+          "gene": "ABCA7",
+          "score": -0.969995814,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 40,
+          "gene": "ABCA8",
+          "score": -0.549351891,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 41,
+          "gene": "ABCA9",
+          "score": -0.572186744,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 42,
+          "gene": "ABCB1",
+          "score": -1.700724742,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 43,
+          "gene": "ABCB10",
+          "score": -0.479814616,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 44,
+          "gene": "ABCB11",
+          "score": -1.852954665,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 45,
+          "gene": "ABCB4",
+          "score": -1.029764996,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 46,
+          "gene": "ABCB5",
+          "score": -0.59910394,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 47,
+          "gene": "ABCB6",
+          "score": -1.521590216,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 48,
+          "gene": "ABCB7",
+          "score": -1.524135471,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 49,
+          "gene": "ABCB8",
+          "score": -0.393198246,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 50,
+          "gene": "ABCB9",
+          "score": -0.755715135,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 51,
+          "gene": "ABCC1",
+          "score": -1.271400813,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 52,
+          "gene": "ABCC10",
+          "score": -2.008241877,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 53,
+          "gene": "ABCC11",
+          "score": -0.3251188,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 54,
+          "gene": "ABCC12",
+          "score": -1.100571167,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 55,
+          "gene": "ABCC2",
+          "score": -0.839026498,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 56,
+          "gene": "ABCC3",
+          "score": -0.518007213,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 57,
+          "gene": "ABCC4",
+          "score": -0.479583788,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 58,
+          "gene": "ABCC5",
+          "score": -0.246965305,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 59,
+          "gene": "ABCC6",
+          "score": -2.490369885,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 60,
+          "gene": "ABCC8",
+          "score": -1.564916083,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 61,
+          "gene": "ABCC9",
+          "score": -0.443336406,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 62,
+          "gene": "ABCD1",
+          "score": -0.523280758,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 63,
+          "gene": "ABCD2",
+          "score": -1.023297507,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 64,
+          "gene": "ABCD3",
+          "score": -0.477819407,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 65,
+          "gene": "ABCD4",
+          "score": -1.887002466,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 66,
+          "gene": "ABCE1",
+          "score": -0.411211926,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 67,
+          "gene": "ABCF1",
+          "score": -0.644085897,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 68,
+          "gene": "ABCF2",
+          "score": -0.288600135,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 69,
+          "gene": "ABCF3",
+          "score": -1.248010272,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 70,
+          "gene": "ABCG1",
+          "score": -0.801651785,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 71,
+          "gene": "ABCG2",
+          "score": -1.044647577,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 72,
+          "gene": "ABCG4",
+          "score": -1.502124565,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 73,
+          "gene": "ABCG5",
+          "score": -0.140835176,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 74,
+          "gene": "ABCG8",
+          "score": -2.106936572,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 75,
+          "gene": "ABHD1",
+          "score": -0.556082452,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 76,
+          "gene": "ABHD10",
+          "score": -0.556163146,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 77,
+          "gene": "ABHD11",
+          "score": -0.099559235,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 78,
+          "gene": "ABHD12",
+          "score": -1.46846437,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 79,
+          "gene": "ABHD12B",
+          "score": -1.270248841,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 80,
+          "gene": "ABHD13",
+          "score": -1.941484791,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 81,
+          "gene": "ABHD14A",
+          "score": -0.478504112,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 82,
+          "gene": "ABHD14B",
+          "score": -0.348690894,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 83,
+          "gene": "ABHD15",
+          "score": -1.224367295,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 84,
+          "gene": "ABHD16A",
+          "score": -1.545144702,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 85,
+          "gene": "ABHD16B",
+          "score": -0.79413146,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 86,
+          "gene": "ABHD17A",
+          "score": -0.635039227,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 87,
+          "gene": "ABHD17B",
+          "score": -1.352782281,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 88,
+          "gene": "ABHD17C",
+          "score": -0.786480853,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 89,
+          "gene": "ABHD2",
+          "score": -1.099191747,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 90,
+          "gene": "ABHD3",
+          "score": -0.859107771,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 91,
+          "gene": "ABHD4",
+          "score": -0.665626967,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 92,
+          "gene": "ABHD5",
+          "score": -0.702653727,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 93,
+          "gene": "ABHD6",
+          "score": -0.111189393,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 94,
+          "gene": "ABHD8",
+          "score": -0.441940284,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 95,
+          "gene": "ABI1",
+          "score": -0.317156841,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 96,
+          "gene": "ABI2",
+          "score": -0.903912703,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 97,
+          "gene": "ABI3",
+          "score": -0.640339095,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 98,
+          "gene": "ABI3BP",
+          "score": -1.08753975,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 99,
+          "gene": "ABL1",
+          "score": -1.377785212,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 100,
+          "gene": "ABL2",
+          "score": -0.663623074,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 101,
+          "gene": "ABLIM1",
+          "score": -0.090508299,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 102,
+          "gene": "ABLIM2",
+          "score": -0.330287119,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 103,
+          "gene": "ABLIM3",
+          "score": -0.234848982,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 104,
+          "gene": "ABO",
+          "score": -0.599159164,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 105,
+          "gene": "ABR",
+          "score": -1.037184256,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 107,
+          "gene": "ABRACL",
+          "score": -0.792983836,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 108,
+          "gene": "ABT1",
+          "score": -0.150876246,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 109,
+          "gene": "ABTB1",
+          "score": -1.266080974,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 110,
+          "gene": "ABTB2",
+          "score": -0.097280505,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 111,
+          "gene": "ACAA1",
+          "score": -1.639689118,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 112,
+          "gene": "ACAA2",
+          "score": -2.82573365,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 113,
+          "gene": "ACACA",
+          "score": -1.186981579,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 114,
+          "gene": "ACACB",
+          "score": -1.022411764,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 115,
+          "gene": "ACAD10",
+          "score": -0.146583055,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 116,
+          "gene": "ACAD11",
+          "score": -0.620391949,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 117,
+          "gene": "ACAD8",
+          "score": -0.69597779,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 118,
+          "gene": "ACAD9",
+          "score": -0.529242218,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 119,
+          "gene": "ACADL",
+          "score": -0.170087803,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 120,
+          "gene": "ACADM",
+          "score": -0.566427892,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 121,
+          "gene": "ACADS",
+          "score": -0.568402649,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 122,
+          "gene": "ACADSB",
+          "score": -0.447200142,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 123,
+          "gene": "ACADVL",
+          "score": -3.744887858,
+          "hit": 1,
+          "round": 4
+        },
+        {
+          "candidate_index": 124,
+          "gene": "ACAN",
+          "score": -0.267317398,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 125,
+          "gene": "ACAP1",
+          "score": -0.887003087,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 126,
+          "gene": "ACAP2",
+          "score": -2.087755734,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 127,
+          "gene": "ACAP3",
+          "score": -1.14986435,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 128,
+          "gene": "ACAT1",
+          "score": -0.023074937,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 129,
+          "gene": "ACAT2",
+          "score": -0.958795912,
+          "hit": 0,
+          "round": 4
+        },
+        {
+          "candidate_index": 130,
+          "gene": "ACBD3",
+          "score": -0.730092192,
+          "hit": 0,
+          "round": 4
         }
       ]
     }

```
