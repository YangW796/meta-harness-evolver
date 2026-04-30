# Change Record — candidate_2

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21_down/run-1/best/current/harness
Generated at: 2026-04-30T06:59:40.015361

## Files Changed

- model.py: modified (added=88, deleted=42, delta=46)
- outputs/metrics.json: modified (added=2098, deleted=306, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -79,7 +79,9 @@
         
         return selected_indices[:batch_size]
     
-    # Thompson Sampling with Gene Cluster Priors
+    # Enhanced Thompson Sampling with Continuous Score Modeling
+    # Use Gaussian-Gamma model for continuous scores instead of Beta for binary hits
+    
     # Group candidates into clusters based on gene similarity
     clusters = defaultdict(list)
     candidate_to_cluster = {}
@@ -141,68 +143,112 @@
             candidate_to_cluster[idx] = prefix
             clusters[prefix].append(idx)
     
-    # Compute cluster statistics (empirical Bayes priors)
-    cluster_successes = defaultdict(int)
-    cluster_trials = defaultdict(int)
+    # Compute cluster statistics using continuous scores
+    cluster_sums = defaultdict(float)
+    cluster_sums_sq = defaultdict(float)
+    cluster_counts = defaultdict(int)
     
     for h in history:
         idx = h['candidate_index']
         cluster_id = candidate_to_cluster[idx]
-        cluster_trials[cluster_id] += 1
-        if h.get('hit') == 1:
-            cluster_successes[cluster_id] += 1
-    
-    # Compute global prior from all history
-    total_hits = sum(1 for h in history if h.get('hit') == 1)
-    global_alpha = total_hits + 1
-    global_beta = len(history) - total_hits + 1
+        score = h['score']
+        
+        cluster_sums[cluster_id] += score
+        cluster_sums_sq[cluster_id] += score * score
+        cluster_counts[cluster_id] += 1
+    
+    # Compute global statistics for empirical Bayes prior
+    all_scores = [h['score'] for h in history]
+    global_mean = np.mean(all_scores) if all_scores else 0.0
+    global_var = np.var(all_scores) if len(all_scores) > 1 else 1.0
+    
+    # Gaussian-Gamma prior parameters (uninformative but centered at global stats)
+    mu_0 = global_mean  # Prior mean
+    lambda_0 = 1.0      # Prior precision scaling
+    alpha_0 = 1.0       # Prior shape for precision
+    beta_0 = global_var if global_var > 0 else 1.0  # Prior rate for precision
     
     # For each cluster, compute posterior parameters
-    cluster_alpha = {}
-    cluster_beta = {}
+    cluster_posterior = {}
     
     for cluster_id in clusters:
-        successes = cluster_successes.get(cluster_id, 0)
-        trials = cluster_trials.get(cluster_id, 0)
-        
-        # Use global prior with cluster observations
-        # This is empirical Bayes: use global distribution as prior
-        cluster_alpha[cluster_id] = successes + global_alpha
-        cluster_beta[cluster_id] = (trials - successes) + global_beta
+        n = cluster_counts.get(cluster_id, 0)
+        
+        if n == 0:
+            # No observations, use prior
+            cluster_posterior[cluster_id] = {
+                'mu_n': mu_0,
+                'lambda_n': lambda_0,
+                'alpha_n': alpha_0,
+                'beta_n': beta_0
+            }
+        else:
+            # Update posterior with cluster observations
+            sum_x = cluster_sums[cluster_id]
+            sum_x_sq = cluster_sums_sq[cluster_id]
+            mean_x = sum_x / n
+            
+            # Gaussian-Gamma posterior update
+            lambda_n = lambda_0 + n
+            mu_n = (lambda_0 * mu_0 + sum_x) / lambda_n
+            alpha_n = alpha_0 + n / 2.0
+            beta_n = beta_0 + 0.5 * (sum_x_sq - (sum_x * sum_x) / n) + \
+                     (lambda_0 * n * (mean_x - mu_0) ** 2) / (2 * lambda_n)
+            
+            cluster_posterior[cluster_id] = {
+                'mu_n': mu_n,
+                'lambda_n': lambda_n,
+                'alpha_n': alpha_n,
+                'beta_n': beta_n
+            }
     
     # For candidates with direct observations, compute posterior
-    candidate_alpha = {}
-    candidate_beta = {}
+    candidate_posterior = {}
     
     for h in history:
         idx = h['candidate_index']
-        hit = h.get('hit', 0)
+        score = h['score']
         cluster_id = candidate_to_cluster[idx]
-        
-        # Start with cluster prior, update with direct observation
-        candidate_alpha[idx] = hit + cluster_alpha[cluster_id]
-        candidate_beta[idx] = (1 - hit) + cluster_beta[cluster_id]
-    
-    # Thompson Sampling: sample theta for each candidate and select top ones
-    sampled_probs = {}
+        cluster_post = cluster_posterior[cluster_id]
+        
+        # Update from cluster prior with single observation
+        lambda_n = cluster_post['lambda_n'] + 1
+        mu_n = (cluster_post['lambda_n'] * cluster_post['mu_n'] + score) / lambda_n
+        alpha_n = cluster_post['alpha_n'] + 0.5
+        beta_n = cluster_post['beta_n'] + 0.5 * (score - cluster_post['mu_n']) ** 2 * \
+                 cluster_post['lambda_n'] / lambda_n
+        
+        candidate_posterior[idx] = {
+            'mu_n': mu_n,
+            'lambda_n': lambda_n,
+            'alpha_n': alpha_n,
+            'beta_n': beta_n
+        }
+    
+    # Thompson Sampling: sample from posterior predictive (Student-t)
+    sampled_scores = {}
     
     for idx in available:
         cluster_id = candidate_to_cluster[idx]
         
-        if idx in candidate_alpha:
+        if idx in candidate_posterior:
             # Candidate has been observed, use its posterior
-            alpha = candidate_alpha[idx]
-            beta = candidate_beta[idx]
+            post = candidate_posterior[idx]
         else:
             # Candidate not observed, use cluster posterior
-            alpha = cluster_alpha[cluster_id]
-            beta = cluster_beta[cluster_id]
-        
-        # Sample from Beta distribution
-        sampled_probs[idx] = np.random.beta(alpha, beta)
-    
-    # Select top candidates by sampled probability
-    sorted_by_sample = sorted(available, key=lambda x: sampled_probs[x], reverse=True)
+            post = cluster_posterior[cluster_id]
+        
+        # Sample precision from Gamma
+        tau = np.random.gamma(post['alpha_n'], 1.0 / post['beta_n'])
+        
+        # Sample mean from Gaussian given precision
+        mean_sample = np.random.normal(post['mu_n'], 1.0 / np.sqrt(post['lambda_n'] * tau))
+        
+        # Store sampled score (we want more negative = better for this task)
+        sampled_scores[idx] = mean_sample
+    
+    # Select top candidates by sampled score (prioritize more negative values)
+    sorted_by_sample = sorted(available, key=lambda x: sampled_scores[x])
     selected_indices = sorted_by_sample[:batch_size]
     
     return selected_indices
```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,301 +9,306 @@
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
+      "baseline_total_hits": 5,
       "delta_queries": 128,
       "delta_hits": 5,
-      "total_queries": 128,
-      "total_hits": 5,
+      "total_queries": 256,
+      "total_hits": 10,
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
-          5
+          5,
+          10
         ]
       },
-      "auc": 320.0,
-      "auc_normalized": 0.0027056277056277055,
-      "ncg": 0.1683378563733971,
+      "auc": 960.0,
+      "auc_normalized": 0.004058441558441558,
+      "ncg": 0.2031925200173379,
       "round_details": [
         {
-          "round": 0,
+          "round": 1,
           "selected_count": 128,
           "hits": 5,
-          "cumulative_hits": 5,
+          "cumulative_hits": 10,
           "precision_at_batch": 0.0390625,
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
+            "DDI2",
+            "LONRF2",
+            "ZNF559-ZNF177",
+            "TSSC4",
+            "LDLRAD4",
+            "CDK15",
+            "DPPA2",
+            "CDC5L",
+            "KDM3B",
+            "P2RX4",
+            "HTR3C",
+            "BRE",
+            "BRWD1",
+            "TNFSF8",
+            "ARL6IP4",
+            "AAGAB",
+            "TCL1A",
+            "ZKSCAN7",
+            "AMOTL2",
+            "GRID2IP",
+            "ERP27",
+            "ZNF83",
+            "IL36RN",
+            "CHD6",
+            "CCDC122",
+            "MTA2",
+            "FOXE1",
+            "RND2",
+            "TRIM58",
+            "ETFDH",
+            "ENOPH1",
+            "PKM",
+            "CAPZA2",
+            "ACTR1B",
+            "CLASP2",
+            "GTF2A1",
+            "IL31",
+            "NAPB",
+            "SPINT1",
+            "BBS10",
+            "VDR",
+            "TCEB3CL2",
+            "B4GALNT3",
+            "TAC4",
+            "CLPX",
+            "TEX40",
+            "IMPA2",
+            "LRRTM1",
+            "UBL7",
+            "TP73",
+            "RTN1",
+            "SPATS2",
+            "ZWILCH",
+            "RS1",
+            "SLC30A6",
+            "TAS2R20",
+            "C4orf29",
+            "GMFB",
+            "SDHC",
+            "RABAC1",
+            "FSTL1",
+            "CRCP",
+            "AIF1L",
+            "HNRNPR",
+            "PUM2",
+            "VASP",
+            "TMEM238",
+            "XAB2",
+            "HS6ST1",
+            "MUC3A",
+            "SPATA31A6",
+            "UTP20",
+            "SSR1",
+            "FOXA2",
+            "ANGPTL4",
+            "COL24A1",
+            "NUDT15",
+            "GDF6",
+            "ME2",
+            "ZBTB8B",
+            "RAET1G",
+            "SYCE1",
+            "FAM160B1",
+            "RNF167",
+            "AXIN1",
+            "CD164L2",
+            "TP63",
+            "CINP",
+            "CDK2AP1",
+            "NCAM2",
+            "DIS3L2",
+            "PGBD1",
+            "ING2",
+            "PFN2",
+            "MYO19",
+            "MAGEB17",
+            "FAM114A1",
+            "SPCS3",
+            "DCAF8L2",
+            "IL36A",
+            "PARD3",
+            "MAP3K7",
+            "CDK16",
+            "BMPR2",
+            "PLXNA1",
+            "NAV1",
+            "RPP40",
+            "CRHBP",
+            "ZNF568",
+            "POMGNT1",
+            "TNR",
+            "PTPRK",
+            "LMBRD1",
+            "LGALS2",
+            "CNTNAP3",
+            "SGSH",
+            "COX7A2L",
+            "RAD54L2",
+            "PARP9",
+            "BTN3A1",
+            "AMACR",
+            "PPP1R17",
+            "TMEM8C",
+            "NPW",
+            "SYT2",
+            "JAK1",
+            "SLC25A17",
+            "GDPD1"
           ],
           "selected_scores": [
-            -0.440718299,
-            -0.211908354,
-            -0.453119592,
-            -4.965011117,
-            -1.083120102,
-            -0.482325554,
-            -0.426778306,
-            -0.572145006,
-            -0.600054381,
-            -1.638094938,
-            -1.479928967,
-            -0.531641773,
-            -2.501769779,
-            -0.53460571,
-            -1.655053509,
-            -0.316263145,
-            -1.841883456,
-            -0.467002565,
-            -1.382644681,
-            -0.349429341,
-            -0.338453236,
-            -0.303647301,
-            -1.12269276,
-            -0.676953445,
-            -3.015036203,
-            -0.355781568,
-            -0.567475521,
-            -0.233841029,
-            -0.115840676,
-            -0.761357564,
-            -0.507730569,
-            -0.727924428,
-            -0.799337128,
-            -0.853079197,
-            -1.414528018,
-            -0.624452994,
-            -0.37051967,
-            -1.103645237,
-            -0.528293503,
-            -0.626249194,
-            -0.538715688,
-            -1.361523575,
-            -0.493907098,
-            -0.359608657,
-            -0.319706721,
-            -1.665457326,
-            -1.108543714,
-            -1.283785665,
-            -0.483560745,
-            -0.168391389,
-            -0.212794819,
-            -1.01708101,
-            -1.555198412,
-            -3.846843544,
-            -0.314854751,
-            -0.687615875,
-            -0.887118123,
-            -1.785320636,
-            -1.11090559,
-            -1.474057418,
-            -0.454534112,
-            -0.473458847,
-            -0.353922365,
-            -1.169893979,
-            -1.080713719,
-            -0.463768342,
-            -0.893653613,
-            -0.500746844,
-            -0.05541296,
-            -2.292532726,
-            -1.065641167,
-            -0.458249888,
-            -0.248697989,
-            -1.723707673,
-            -1.248742525,
-            -0.606074539,
-            -1.616315535,
-            -0.625833814,
-            -1.887446516,
-            -0.760030351,
-            -0.790477636,
-            -1.498557032,
-            -0.45372378,
-            -1.619798825,
-            -1.139585963,
-            -1.069497046,
-            -1.000614035,
-            -0.600012888,
-            -0.990899065,
-            -0.512726259,
-            -1.179428663,
-            -0.979729795,
-            -0.686840974,
-            -0.625917622,
-            -1.421392615,
-            -1.585646831,
-            -0.312904766,
-            -1.139817189,
-            -0.556111904,
-            -1.445795344,
-            -0.450441631,
-            -0.520950282,
-            -1.158650374,
-            -0.544454627,
-            -0.748603479,
-            -0.06859385,
-            -0.694079177,
-            -0.173578048,
-            -0.185874668,
-            -0.899583631,
-            -0.59555894,
-            -0.547705879,
-            -1.129825101,
-            -0.480012617,
-            -0.569548136,
-            -1.087354143,
-            -0.449956719,
-            -0.530776837,
-            -0.49094761,
-            -0.60240636,
-            -1.725716417,
-            -0.772827818,
-            -1.783244708,
-            -0.83255635,
-            -0.313176705,
-            -1.076033352,
-            -0.909825102,
-            -0.61144655
+            -0.306600558,
+            -0.942059951,
+            -0.512561534,
+            -0.434762436,
+            -0.515691564,
+            -0.543954085,
+            -0.231849981,
+            -1.30631225,
+            -2.123302384,
+            -0.895888332,
+            -0.893999647,
+            -0.719399047,
+            -1.369489525,
+            -1.580145467,
+            -0.383464419,
+            -0.669472472,
+            -0.313284927,
+            -0.801952387,
+            -0.597616552,
+            -0.112350676,
+            -0.60564137,
+            -0.323889734,
+            -0.539854908,
+            -0.269144461,
+            -0.477657619,
+            -1.753059275,
+            -0.126096573,
+            -0.456952444,
+            -1.107643035,
+            -1.005968912,
+            -1.039459342,
+            -0.566469921,
+            -0.547647084,
+            -2.676961105,
+            -0.720196739,
+            -0.560837764,
+            -0.48859985,
+            -0.504563953,
+            -0.876782278,
+            -0.555709322,
+            -0.684824516,
+            -0.381023993,
+            -0.347115866,
+            -0.828933135,
+            -0.140477532,
+            -0.422164937,
+            -0.461318003,
+            -2.592523477,
+            -0.764022397,
+            -0.566748018,
+            -0.69771725,
+            -0.378330042,
+            -0.934061114,
+            -0.235661351,
+            -1.244838015,
+            -0.307960534,
+            -0.415325668,
+            -0.854138764,
+            -0.656352894,
+            -1.180092247,
+            -0.963236266,
+            -1.080601987,
+            -0.762862387,
+            -0.682290269,
+            -0.755236631,
+            -1.133624527,
+            -0.695619006,
+            -1.307671029,
+            -0.943631679,
+            -1.01937299,
+            -0.906503046,
+            -2.077461957,
+            -1.577564116,
+            -0.295863731,
+            -0.804895793,
+            -1.335594247,
+            -1.575994641,
+            -1.153146511,
+            -0.7198085,
+            -1.738619696,
+            -0.557222438,
+            -1.083570349,
+            -0.513260184,
+            -1.127926173,
+            -1.109688797,
+            -0.329972028,
+            -0.350176452,
+            -0.934284081,
+            -0.44125141,
+            -2.197398787,
+            -0.27799242,
+            -0.935941336,
+            -3.745862679,
+            -2.022894031,
+            -0.359967096,
+            -0.401092105,
+            -0.582838656,
+            -0.313799055,
+            -0.828336324,
+            -0.565361589,
+            -1.438277915,
+            -0.441209211,
+            -0.453217512,
+            -0.046077773,
+            -0.680411001,
+            -0.740697779,
+            -1.098501412,
+            -1.013220548,
+            -0.239185293,
+            -1.252663599,
+            -0.745389295,
+            -1.573596014,
+            -1.485285374,
+            -0.774989349,
+            -1.119232109,
+            -0.996524308,
+            -1.898013587,
+            -0.8352701,
+            -0.376506713,
+            -0.713514398,
+            -2.001973503,
+            -0.708628462,
+            -0.289417769,
+            -0.138030494,
+            -0.823101552,
+            -1.801116994,
+            -0.567387603,
+            -0.384405013
           ],
           "selected_hits": [
             0,
             0,
             0,
+            0,
+            0,
+            0,
+            0,
+            0,
             1,
             0,
             0,
@@ -313,6 +318,22 @@
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
             1,
             0,
             0,
@@ -325,6 +346,8 @@
             0,
             0,
             0,
+            0,
+            0,
             1,
             0,
             0,
@@ -354,46 +377,23 @@
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
             1,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
-            0,
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
           "score": -0.61144655,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 3918,
+          "gene": "DDI2",
+          "score": -0.306600558,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8636,
+          "gene": "LONRF2",
+          "score": -0.942059951,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18180,
+          "gene": "ZNF559-ZNF177",
+          "score": -0.512561534,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16793,
+          "gene": "TSSC4",
+          "score": -0.434762436,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8412,
+          "gene": "LDLRAD4",
+          "score": -0.515691564,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2621,
+          "gene": "CDK15",
+          "score": -0.543954085,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4342,
+          "gene": "DPPA2",
+          "score": -0.231849981,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2572,
+          "gene": "CDC5L",
+          "score": -1.30631225,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7843,
+          "gene": "KDM3B",
+          "score": -2.123302384,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 11075,
+          "gene": "P2RX4",
+          "score": -0.895888332,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7131,
+          "gene": "HTR3C",
+          "score": -0.893999647,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1616,
+          "gene": "BRE",
+          "score": -0.719399047,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1636,
+          "gene": "BRWD1",
+          "score": -1.369489525,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16404,
+          "gene": "TNFSF8",
+          "score": -1.580145467,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1022,
+          "gene": "ARL6IP4",
+          "score": -0.383464419,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14,
+          "gene": "AAGAB",
+          "score": -0.669472472,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15730,
+          "gene": "TCL1A",
+          "score": -0.313284927,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17885,
+          "gene": "ZKSCAN7",
+          "score": -0.801952387,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 627,
+          "gene": "AMOTL2",
+          "score": -0.597616552,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6428,
+          "gene": "GRID2IP",
+          "score": -0.112350676,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4885,
+          "gene": "ERP27",
+          "score": -0.60564137,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18377,
+          "gene": "ZNF83",
+          "score": -0.323889734,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7390,
+          "gene": "IL36RN",
+          "score": -0.539854908,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2867,
+          "gene": "CHD6",
+          "score": -0.269144461,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2232,
+          "gene": "CCDC122",
+          "score": -0.477657619,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9744,
+          "gene": "MTA2",
+          "score": -1.753059275,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5650,
+          "gene": "FOXE1",
+          "score": -0.126096573,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13272,
+          "gene": "RND2",
+          "score": -0.456952444,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16645,
+          "gene": "TRIM58",
+          "score": -1.107643035,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4919,
+          "gene": "ETFDH",
+          "score": -1.005968912,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4758,
+          "gene": "ENOPH1",
+          "score": -1.039459342,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11737,
+          "gene": "PKM",
+          "score": -0.566469921,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2113,
+          "gene": "CAPZA2",
+          "score": -0.547647084,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 215,
+          "gene": "ACTR1B",
+          "score": -2.676961105,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3001,
+          "gene": "CLASP2",
+          "score": -0.720196739,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6510,
+          "gene": "GTF2A1",
+          "score": -0.560837764,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7382,
+          "gene": "IL31",
+          "score": -0.48859985,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10022,
+          "gene": "NAPB",
+          "score": -0.504563953,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15026,
+          "gene": "SPINT1",
+          "score": -0.876782278,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1421,
+          "gene": "BBS10",
+          "score": -0.555709322,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17307,
+          "gene": "VDR",
+          "score": -0.684824516,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15709,
+          "gene": "TCEB3CL2",
+          "score": -0.381023993,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1364,
+          "gene": "B4GALNT3",
+          "score": -0.347115866,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15510,
+          "gene": "TAC4",
+          "score": -0.828933135,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3111,
+          "gene": "CLPX",
+          "score": -0.140477532,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15828,
+          "gene": "TEX40",
+          "score": -0.422164937,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7418,
+          "gene": "IMPA2",
+          "score": -0.461318003,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8791,
+          "gene": "LRRTM1",
+          "score": -2.592523477,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 17031,
+          "gene": "UBL7",
+          "score": -0.764022397,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16495,
+          "gene": "TP73",
+          "score": -0.566748018,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13587,
+          "gene": "RTN1",
+          "score": -0.69771725,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14974,
+          "gene": "SPATS2",
+          "score": -0.378330042,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18459,
+          "gene": "ZWILCH",
+          "score": -0.934061114,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13551,
+          "gene": "RS1",
+          "score": -0.235661351,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14435,
+          "gene": "SLC30A6",
+          "score": -1.244838015,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15584,
+          "gene": "TAS2R20",
+          "score": -0.307960534,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1864,
+          "gene": "C4orf29",
+          "score": -0.415325668,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6154,
+          "gene": "GMFB",
+          "score": -0.854138764,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13844,
+          "gene": "SDHC",
+          "score": -0.656352894,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12783,
+          "gene": "RABAC1",
+          "score": -1.180092247,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5735,
+          "gene": "FSTL1",
+          "score": -0.963236266,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3436,
+          "gene": "CRCP",
+          "score": -1.080601987,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 466,
+          "gene": "AIF1L",
+          "score": -0.762862387,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6953,
+          "gene": "HNRNPR",
+          "score": -0.682290269,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12644,
+          "gene": "PUM2",
+          "score": -0.755236631,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17283,
+          "gene": "VASP",
+          "score": -1.133624527,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16219,
+          "gene": "TMEM238",
+          "score": -0.695619006,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17587,
+          "gene": "XAB2",
+          "score": -1.307671029,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7052,
+          "gene": "HS6ST1",
+          "score": -0.943631679,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9825,
+          "gene": "MUC3A",
+          "score": -1.01937299,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14957,
+          "gene": "SPATA31A6",
+          "score": -0.906503046,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17253,
+          "gene": "UTP20",
+          "score": -2.077461957,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15171,
+          "gene": "SSR1",
+          "score": -1.577564116,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5635,
+          "gene": "FOXA2",
+          "score": -0.295863731,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 660,
+          "gene": "ANGPTL4",
+          "score": -0.804895793,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3254,
+          "gene": "COL24A1",
+          "score": -1.335594247,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10629,
+          "gene": "NUDT15",
+          "score": -1.575994641,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5976,
+          "gene": "GDF6",
+          "score": -1.153146511,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9205,
+          "gene": "ME2",
+          "score": -0.7198085,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17742,
+          "gene": "ZBTB8B",
+          "score": -1.738619696,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12824,
+          "gene": "RAET1G",
+          "score": -0.557222438,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15430,
+          "gene": "SYCE1",
+          "score": -1.083570349,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5108,
+          "gene": "FAM160B1",
+          "score": -0.513260184,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13310,
+          "gene": "RNF167",
+          "score": -1.127926173,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1333,
+          "gene": "AXIN1",
+          "score": -1.109688797,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2460,
+          "gene": "CD164L2",
+          "score": -0.329972028,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16494,
+          "gene": "TP63",
+          "score": -0.350176452,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2973,
+          "gene": "CINP",
+          "score": -0.934284081,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2628,
+          "gene": "CDK2AP1",
+          "score": -0.44125141,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10062,
+          "gene": "NCAM2",
+          "score": -2.197398787,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 4136,
+          "gene": "DIS3L2",
+          "score": -0.27799242,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11533,
+          "gene": "PGBD1",
+          "score": -0.935941336,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7432,
+          "gene": "ING2",
+          "score": -3.745862679,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 11520,
+          "gene": "PFN2",
+          "score": -2.022894031,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9918,
+          "gene": "MYO19",
+          "score": -0.359967096,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8941,
+          "gene": "MAGEB17",
+          "score": -0.401092105,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5053,
+          "gene": "FAM114A1",
+          "score": -0.582838656,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14980,
+          "gene": "SPCS3",
+          "score": -0.313799055,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3865,
+          "gene": "DCAF8L2",
+          "score": -0.828336324,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7387,
+          "gene": "IL36A",
+          "score": -0.565361589,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11187,
+          "gene": "PARD3",
+          "score": -1.438277915,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9028,
+          "gene": "MAP3K7",
+          "score": -0.441209211,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2622,
+          "gene": "CDK16",
+          "score": -0.453217512,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1563,
+          "gene": "BMPR2",
+          "score": -0.046077773,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11878,
+          "gene": "PLXNA1",
+          "score": -0.680411001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10044,
+          "gene": "NAV1",
+          "score": -0.740697779,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13470,
+          "gene": "RPP40",
+          "score": -1.098501412,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3455,
+          "gene": "CRHBP",
+          "score": -1.013220548,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18189,
+          "gene": "ZNF568",
+          "score": -0.239185293,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12011,
+          "gene": "POMGNT1",
+          "score": -1.252663599,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16431,
+          "gene": "TNR",
+          "score": -0.745389295,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12621,
+          "gene": "PTPRK",
+          "score": -1.573596014,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8551,
+          "gene": "LMBRD1",
+          "score": -1.485285374,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8446,
+          "gene": "LGALS2",
+          "score": -0.774989349,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3212,
+          "gene": "CNTNAP3",
+          "score": -1.119232109,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14080,
+          "gene": "SGSH",
+          "score": -0.996524308,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3360,
+          "gene": "COX7A2L",
+          "score": -1.898013587,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12818,
+          "gene": "RAD54L2",
+          "score": -0.8352701,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11210,
+          "gene": "PARP9",
+          "score": -0.376506713,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1675,
+          "gene": "BTN3A1",
+          "score": -0.713514398,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 602,
+          "gene": "AMACR",
+          "score": -2.001973503,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12142,
+          "gene": "PPP1R17",
+          "score": -0.708628462,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16312,
+          "gene": "TMEM8C",
+          "score": -0.289417769,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10493,
+          "gene": "NPW",
+          "score": -0.138030494,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15483,
+          "gene": "SYT2",
+          "score": -0.823101552,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7647,
+          "gene": "JAK1",
+          "score": -1.801116994,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14350,
+          "gene": "SLC25A17",
+          "score": -0.567387603,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5982,
+          "gene": "GDPD1",
+          "score": -0.384405013,
+          "hit": 0,
+          "round": 1
         }
       ],
       "queried_history": [
@@ -2226,6 +3122,902 @@
           "score": -0.61144655,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 3918,
+          "gene": "DDI2",
+          "score": -0.306600558,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8636,
+          "gene": "LONRF2",
+          "score": -0.942059951,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18180,
+          "gene": "ZNF559-ZNF177",
+          "score": -0.512561534,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16793,
+          "gene": "TSSC4",
+          "score": -0.434762436,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8412,
+          "gene": "LDLRAD4",
+          "score": -0.515691564,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2621,
+          "gene": "CDK15",
+          "score": -0.543954085,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4342,
+          "gene": "DPPA2",
+          "score": -0.231849981,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2572,
+          "gene": "CDC5L",
+          "score": -1.30631225,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7843,
+          "gene": "KDM3B",
+          "score": -2.123302384,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 11075,
+          "gene": "P2RX4",
+          "score": -0.895888332,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7131,
+          "gene": "HTR3C",
+          "score": -0.893999647,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1616,
+          "gene": "BRE",
+          "score": -0.719399047,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1636,
+          "gene": "BRWD1",
+          "score": -1.369489525,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16404,
+          "gene": "TNFSF8",
+          "score": -1.580145467,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1022,
+          "gene": "ARL6IP4",
+          "score": -0.383464419,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14,
+          "gene": "AAGAB",
+          "score": -0.669472472,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15730,
+          "gene": "TCL1A",
+          "score": -0.313284927,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17885,
+          "gene": "ZKSCAN7",
+          "score": -0.801952387,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 627,
+          "gene": "AMOTL2",
+          "score": -0.597616552,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6428,
+          "gene": "GRID2IP",
+          "score": -0.112350676,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4885,
+          "gene": "ERP27",
+          "score": -0.60564137,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18377,
+          "gene": "ZNF83",
+          "score": -0.323889734,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7390,
+          "gene": "IL36RN",
+          "score": -0.539854908,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2867,
+          "gene": "CHD6",
+          "score": -0.269144461,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2232,
+          "gene": "CCDC122",
+          "score": -0.477657619,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9744,
+          "gene": "MTA2",
+          "score": -1.753059275,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5650,
+          "gene": "FOXE1",
+          "score": -0.126096573,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13272,
+          "gene": "RND2",
+          "score": -0.456952444,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16645,
+          "gene": "TRIM58",
+          "score": -1.107643035,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4919,
+          "gene": "ETFDH",
+          "score": -1.005968912,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4758,
+          "gene": "ENOPH1",
+          "score": -1.039459342,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11737,
+          "gene": "PKM",
+          "score": -0.566469921,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2113,
+          "gene": "CAPZA2",
+          "score": -0.547647084,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 215,
+          "gene": "ACTR1B",
+          "score": -2.676961105,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3001,
+          "gene": "CLASP2",
+          "score": -0.720196739,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6510,
+          "gene": "GTF2A1",
+          "score": -0.560837764,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7382,
+          "gene": "IL31",
+          "score": -0.48859985,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10022,
+          "gene": "NAPB",
+          "score": -0.504563953,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15026,
+          "gene": "SPINT1",
+          "score": -0.876782278,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1421,
+          "gene": "BBS10",
+          "score": -0.555709322,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17307,
+          "gene": "VDR",
+          "score": -0.684824516,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15709,
+          "gene": "TCEB3CL2",
+          "score": -0.381023993,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1364,
+          "gene": "B4GALNT3",
+          "score": -0.347115866,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15510,
+          "gene": "TAC4",
+          "score": -0.828933135,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3111,
+          "gene": "CLPX",
+          "score": -0.140477532,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15828,
+          "gene": "TEX40",
+          "score": -0.422164937,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7418,
+          "gene": "IMPA2",
+          "score": -0.461318003,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8791,
+          "gene": "LRRTM1",
+          "score": -2.592523477,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 17031,
+          "gene": "UBL7",
+          "score": -0.764022397,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16495,
+          "gene": "TP73",
+          "score": -0.566748018,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13587,
+          "gene": "RTN1",
+          "score": -0.69771725,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14974,
+          "gene": "SPATS2",
+          "score": -0.378330042,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18459,
+          "gene": "ZWILCH",
+          "score": -0.934061114,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13551,
+          "gene": "RS1",
+          "score": -0.235661351,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14435,
+          "gene": "SLC30A6",
+          "score": -1.244838015,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15584,
+          "gene": "TAS2R20",
+          "score": -0.307960534,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1864,
+          "gene": "C4orf29",
+          "score": -0.415325668,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6154,
+          "gene": "GMFB",
+          "score": -0.854138764,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13844,
+          "gene": "SDHC",
+          "score": -0.656352894,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12783,
+          "gene": "RABAC1",
+          "score": -1.180092247,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5735,
+          "gene": "FSTL1",
+          "score": -0.963236266,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3436,
+          "gene": "CRCP",
+          "score": -1.080601987,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 466,
+          "gene": "AIF1L",
+          "score": -0.762862387,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6953,
+          "gene": "HNRNPR",
+          "score": -0.682290269,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12644,
+          "gene": "PUM2",
+          "score": -0.755236631,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17283,
+          "gene": "VASP",
+          "score": -1.133624527,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16219,
+          "gene": "TMEM238",
+          "score": -0.695619006,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17587,
+          "gene": "XAB2",
+          "score": -1.307671029,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7052,
+          "gene": "HS6ST1",
+          "score": -0.943631679,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9825,
+          "gene": "MUC3A",
+          "score": -1.01937299,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14957,
+          "gene": "SPATA31A6",
+          "score": -0.906503046,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17253,
+          "gene": "UTP20",
+          "score": -2.077461957,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15171,
+          "gene": "SSR1",
+          "score": -1.577564116,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5635,
+          "gene": "FOXA2",
+          "score": -0.295863731,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 660,
+          "gene": "ANGPTL4",
+          "score": -0.804895793,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3254,
+          "gene": "COL24A1",
+          "score": -1.335594247,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10629,
+          "gene": "NUDT15",
+          "score": -1.575994641,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5976,
+          "gene": "GDF6",
+          "score": -1.153146511,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9205,
+          "gene": "ME2",
+          "score": -0.7198085,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 17742,
+          "gene": "ZBTB8B",
+          "score": -1.738619696,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12824,
+          "gene": "RAET1G",
+          "score": -0.557222438,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15430,
+          "gene": "SYCE1",
+          "score": -1.083570349,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5108,
+          "gene": "FAM160B1",
+          "score": -0.513260184,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13310,
+          "gene": "RNF167",
+          "score": -1.127926173,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1333,
+          "gene": "AXIN1",
+          "score": -1.109688797,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2460,
+          "gene": "CD164L2",
+          "score": -0.329972028,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16494,
+          "gene": "TP63",
+          "score": -0.350176452,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2973,
+          "gene": "CINP",
+          "score": -0.934284081,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2628,
+          "gene": "CDK2AP1",
+          "score": -0.44125141,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10062,
+          "gene": "NCAM2",
+          "score": -2.197398787,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 4136,
+          "gene": "DIS3L2",
+          "score": -0.27799242,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11533,
+          "gene": "PGBD1",
+          "score": -0.935941336,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7432,
+          "gene": "ING2",
+          "score": -3.745862679,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 11520,
+          "gene": "PFN2",
+          "score": -2.022894031,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9918,
+          "gene": "MYO19",
+          "score": -0.359967096,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8941,
+          "gene": "MAGEB17",
+          "score": -0.401092105,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5053,
+          "gene": "FAM114A1",
+          "score": -0.582838656,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14980,
+          "gene": "SPCS3",
+          "score": -0.313799055,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3865,
+          "gene": "DCAF8L2",
+          "score": -0.828336324,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7387,
+          "gene": "IL36A",
+          "score": -0.565361589,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11187,
+          "gene": "PARD3",
+          "score": -1.438277915,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9028,
+          "gene": "MAP3K7",
+          "score": -0.441209211,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2622,
+          "gene": "CDK16",
+          "score": -0.453217512,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1563,
+          "gene": "BMPR2",
+          "score": -0.046077773,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11878,
+          "gene": "PLXNA1",
+          "score": -0.680411001,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10044,
+          "gene": "NAV1",
+          "score": -0.740697779,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13470,
+          "gene": "RPP40",
+          "score": -1.098501412,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3455,
+          "gene": "CRHBP",
+          "score": -1.013220548,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18189,
+          "gene": "ZNF568",
+          "score": -0.239185293,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12011,
+          "gene": "POMGNT1",
+          "score": -1.252663599,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16431,
+          "gene": "TNR",
+          "score": -0.745389295,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12621,
+          "gene": "PTPRK",
+          "score": -1.573596014,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8551,
+          "gene": "LMBRD1",
+          "score": -1.485285374,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8446,
+          "gene": "LGALS2",
+          "score": -0.774989349,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3212,
+          "gene": "CNTNAP3",
+          "score": -1.119232109,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14080,
+          "gene": "SGSH",
+          "score": -0.996524308,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3360,
+          "gene": "COX7A2L",
+          "score": -1.898013587,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12818,
+          "gene": "RAD54L2",
+          "score": -0.8352701,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11210,
+          "gene": "PARP9",
+          "score": -0.376506713,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1675,
+          "gene": "BTN3A1",
+          "score": -0.713514398,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 602,
+          "gene": "AMACR",
+          "score": -2.001973503,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12142,
+          "gene": "PPP1R17",
+          "score": -0.708628462,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16312,
+          "gene": "TMEM8C",
+          "score": -0.289417769,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10493,
+          "gene": "NPW",
+          "score": -0.138030494,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15483,
+          "gene": "SYT2",
+          "score": -0.823101552,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7647,
+          "gene": "JAK1",
+          "score": -1.801116994,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14350,
+          "gene": "SLC25A17",
+          "score": -0.567387603,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5982,
+          "gene": "GDPD1",
+          "score": -0.384405013,
+          "hit": 0,
+          "round": 1
         }
       ]
     }

```
