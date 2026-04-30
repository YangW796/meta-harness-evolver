# Change Record — candidate_2

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/IFNG/run-2/best/current/harness
Generated at: 2026-04-30T07:11:27.934990

## Files Changed

- model.py: modified (added=44, deleted=12, delta=32)
- outputs/metrics.json: modified (added=2159, deleted=367, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -51,12 +51,12 @@
     hit_indices = [h['candidate_index'] for h in history if h.get('hit', 0) == 1]
     hit_scores = [h['score'] for h in history if h.get('hit', 0) == 1]
     
-    # If we have hits, prioritize exploring similar genes
-    if hit_indices and len(hit_indices) > 0:
-        # Try to use gene search if available
-        try:
-            import bda_tools
-            
+    # Try to use gene search if available (for both exploitation and exploration)
+    try:
+        import bda_tools
+        
+        # If we have hits, prioritize exploring similar genes (exploitation)
+        if hit_indices and len(hit_indices) > 0:
             # Find the best hit (most negative score)
             best_hit_idx = hit_indices[np.argmin(hit_scores)]
             best_hit_gene = candidates[best_hit_idx].get('gene')
@@ -85,12 +85,44 @@
                     
                     rng.shuffle(selected)
                     return selected[:batch_size]
-        except ImportError:
-            # Gene search not available, fall back to pure Thompson Sampling
-            pass
-        except Exception:
-            # Gene search failed, fall back to pure Thompson Sampling
-            pass
+        else:
+            # No hits yet: use diverse gene search for proactive exploration
+            # Pick a random gene from history to start diverse search
+            if history:
+                # Select a random gene from those already explored
+                random_history_gene = rng.choice(history)
+                start_gene = candidates[random_history_gene['candidate_index']].get('gene')
+                
+                if start_gene:
+                    # Search for diverse genes to explore different gene families
+                    diverse_indices = bda_tools.gene_search(start_gene, k=30, diverse=True)
+                    
+                    # Filter to available indices only
+                    diverse_available = [idx for idx in diverse_indices if idx in available_indices]
+                    
+                    # If we found diverse genes, include some in the selection
+                    if diverse_available:
+                        # Take up to 40% of batch from diverse exploration
+                        num_diverse = min(len(diverse_available), batch_size * 2 // 5)
+                        selected = diverse_available[:num_diverse]
+                        remaining_batch = batch_size - len(selected)
+                        
+                        # Fill the rest using Thompson Sampling
+                        if remaining_batch > 0:
+                            thompson_selected = _thompson_sampling(
+                                candidates, history, available_indices, 
+                                selected, remaining_batch, rng
+                            )
+                            selected.extend(thompson_selected)
+                        
+                        rng.shuffle(selected)
+                        return selected[:batch_size]
+    except ImportError:
+        # Gene search not available, fall back to pure Thompson Sampling
+        pass
+    except Exception:
+        # Gene search failed, fall back to pure Thompson Sampling
+        pass
     
     # Use pure Thompson Sampling
     selected = _thompson_sampling(candidates, history, available_indices, [], batch_size, rng)

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,309 +9,299 @@
   "metrics": {
     "test": {
       "pool_size": 18418,
-      "rounds": 1,
+      "rounds": 2,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 0,
-      "baseline_total_hits": 0,
+      "baseline_total_queries": 128,
+      "baseline_total_hits": 2,
       "delta_queries": 128,
-      "delta_hits": 2,
-      "total_queries": 128,
-      "total_hits": 2,
+      "delta_hits": 8,
+      "total_queries": 256,
+      "total_hits": 10,
       "top_k": 920,
       "hit_curve": {
         "queries": [
-          0,
-          128
+          128,
+          256
         ],
         "hits": [
-          0,
-          2
+          2,
+          10
         ]
       },
-      "auc": 128.0,
-      "auc_normalized": 0.0010869565217391304,
-      "ncg": 0.10533733408464835,
+      "auc": 768.0,
+      "auc_normalized": 0.003260869565217391,
+      "ncg": 0.14926231786886981,
       "round_details": [
         {
-          "round": 0,
+          "round": 1,
           "selected_count": 128,
-          "hits": 2,
-          "cumulative_hits": 2,
-          "precision_at_batch": 0.015625,
+          "hits": 8,
+          "cumulative_hits": 10,
+          "precision_at_batch": 0.0625,
           "selected": [
-            "AADAC",
-            "ABHD5",
-            "ABLIM1",
-            "ABHD10",
-            "ABCB8",
-            "AAMDC",
-            "ABCD1",
-            "ABLIM2",
-            "ABLIM3",
-            "ABHD14B",
-            "ABCB6",
-            "AARS1",
-            "ABCA1",
-            "ACACB",
-            "ABCA12",
-            "ABCB9",
-            "ABCD2",
-            "ACADL",
-            "ABI2",
-            "AANAT",
-            "ABCG8",
-            "A2M",
-            "ABCE1",
-            "ABHD13",
-            "ABCA4",
-            "ABHD16B",
-            "AAAS",
-            "A1CF",
-            "ABHD17B",
-            "ABHD12B",
-            "AASS",
-            "ABL2",
-            "ABCC8",
-            "ABCG5",
-            "ABI1",
-            "ABCC6",
-            "ABCA7",
-            "ABCG4",
-            "ABCA2",
-            "ABCC1",
-            "ABCC9",
-            "ABCA6",
-            "ABT1",
-            "ABCA9",
-            "ABHD16A",
-            "ABHD12",
-            "ABCC3",
-            "ABCB1",
-            "ABL1",
-            "AARS2",
-            "ABCC10",
-            "ABCG1",
-            "AARSD1",
-            "ABI3",
-            "ABCA8",
-            "ABR",
-            "ACAD8",
-            "ABCF1",
-            "A4GNT",
-            "ABCC2",
-            "AAGAB",
-            "ABHD3",
-            "ABCD4",
-            "ABI3BP",
-            "ABRA",
-            "ACACA",
-            "AACS",
-            "AASDH",
-            "ABCB5",
-            "ABCA5",
-            "AADACL2",
-            "ABHD14A",
-            "AAK1",
-            "ABCF2",
-            "ABCC5",
-            "A4GALT",
-            "ABCA13",
-            "ABO",
-            "ABCB11",
-            "ABCB4",
-            "AADACL4",
-            "ABCB7",
-            "ABRAXAS1",
-            "ACAD10",
-            "ABHD17C",
-            "ABRACL",
-            "AAR2",
-            "ABHD6",
-            "ABCB10",
-            "ABTB1",
-            "ABITRAM",
-            "AARD",
-            "A1BG",
-            "ACADM",
-            "ABTB2",
-            "ABCC4",
-            "ACAD9",
-            "ABCC11",
-            "ACAA1",
-            "ABHD2",
-            "ABHD15",
-            "ABHD4",
-            "AASDHPPT",
-            "ABCG2",
-            "ABRAXAS2",
-            "ABHD11",
-            "ABCD3",
-            "ABAT",
-            "AATF",
-            "ACAA2",
-            "ACADSB",
-            "A3GALT2",
-            "ABCC12",
-            "ABHD1",
-            "AADACL3",
-            "ABCF3",
-            "ABTB3",
-            "ACAD11",
-            "ABHD17A",
-            "AADAT",
-            "ACADS",
-            "AAMP",
-            "ACADVL",
-            "ABCA10",
-            "ABCA3",
-            "ABHD8",
-            "A2ML1",
-            "AATK"
+            "GRB10",
+            "CHSY3",
+            "CDV3",
+            "TSEN54",
+            "MPZL3",
+            "STAT5A",
+            "LAMP1",
+            "TMCC1",
+            "GRPR",
+            "EPPIN",
+            "HM13",
+            "HOXA10",
+            "CACNA1B",
+            "HSPA1A",
+            "CELF3",
+            "PRDX4",
+            "HPD",
+            "GART",
+            "NDUFA4",
+            "PIMREG",
+            "FAM221B",
+            "ACTA2",
+            "NME6",
+            "MARCHF4",
+            "RAB11A",
+            "MMP1",
+            "LYRM4",
+            "CHRAC1",
+            "KCTD8",
+            "CEP97",
+            "ARSI",
+            "KCNQ5",
+            "OR9I1",
+            "ALYREF",
+            "ATP4A",
+            "EIF5A2",
+            "CACNA1A",
+            "GABRR3",
+            "EPB41L1",
+            "SEZ6",
+            "C3orf79",
+            "MRPL32",
+            "CMTM7",
+            "CRLF2",
+            "EDNRA",
+            "FAR2",
+            "PIEZO2",
+            "SLBP",
+            "B3GALNT2",
+            "GOLGA8O",
+            "AMOTL1",
+            "SERPINE3",
+            "RXFP4",
+            "ASIC3",
+            "CD207",
+            "GJB1",
+            "MAP3K21",
+            "FOXR2",
+            "PPA1",
+            "OXA1L",
+            "PCDHGB3",
+            "RIOX2",
+            "GABRG1",
+            "BBS12",
+            "KDM4C",
+            "RBM34",
+            "MRPL39",
+            "CRIP3",
+            "ZP3",
+            "FCMR",
+            "SP100",
+            "SAPCD2",
+            "ZPLD1",
+            "TOB2",
+            "OR10A4",
+            "MMP26",
+            "DAZAP1",
+            "BCKDHA",
+            "MS4A4E",
+            "COMMD5",
+            "TOGARAM2",
+            "PCDHB13",
+            "SLC35F5",
+            "CASP3",
+            "SNRPD3",
+            "RNASE10",
+            "CMPK2",
+            "CEACAM18",
+            "MTERF4",
+            "ZNF451",
+            "IQCN",
+            "FAM98B",
+            "DYRK1A",
+            "MSANTD3-TMEFF1",
+            "LUZP1",
+            "EXTL2",
+            "SPTB",
+            "POT1",
+            "KRTAP19-5",
+            "PTGFRN",
+            "EPM2A",
+            "ARHGEF38",
+            "ATMIN",
+            "CDH13",
+            "RPS26",
+            "NEK11",
+            "CARD18",
+            "PRDM10",
+            "FHIP2A",
+            "SRSF12",
+            "DSTN",
+            "SPON2",
+            "APOLD1",
+            "OLFM3",
+            "MARF1",
+            "RASGRP4",
+            "ERCC4",
+            "SDHC",
+            "OR2T4",
+            "ATP8A1",
+            "SLAIN2",
+            "COL7A1",
+            "PRR27",
+            "ERCC6L",
+            "CLEC14A",
+            "RSAD1",
+            "CCDC88A",
+            "LACTBL1"
           ],
           "selected_scores": [
-            0.09700375,
-            -0.123051,
-            -0.095673,
-            -0.083665,
-            -0.009105,
-            0.01205,
-            -0.0909125,
-            -0.220065,
-            0.131625,
-            0.025335,
-            -0.042354,
-            -0.40020835,
-            0.1342295,
-            0.018345,
-            -0.108835,
-            0.21014065,
-            0.00524,
-            0.147555,
-            -0.22205,
-            0.14409,
-            -0.038225,
-            -0.18934,
-            0.359895,
-            0.022985,
-            -0.159105,
-            -0.002058,
-            0.130627,
-            0.129081,
-            0.23368,
-            -0.01068,
-            -0.085326,
-            0.11353,
-            0.051595,
-            0.103443,
-            0.0107805,
-            0.307105,
-            -0.01946,
-            0.25585085,
-            -0.2907179,
-            -0.165605,
-            0.19773,
-            -0.1365005,
-            0.0858425,
-            0.27268896,
-            -0.1640935,
-            0.1263665,
-            -0.0762865,
-            -0.266345,
-            0.0765485,
-            0.03688,
-            -0.1349245,
-            0.04291255,
-            -0.007871,
-            -0.1086473,
-            0.0039675,
-            0.339915,
-            0.02707,
-            -0.105515,
-            0.029995,
-            -0.1535965,
-            -0.31044,
-            0.071691,
-            -0.04102,
-            -0.12602566,
-            0.031534,
-            0.035085,
-            0.19899,
-            0.140285,
-            0.0766415,
-            0.09411,
-            0.180098,
-            -0.0982965,
-            -0.144225,
-            -0.1052725,
-            0.16644,
-            0.15113,
-            -0.01498,
-            0.016455,
-            0.09610045,
-            0.2502,
-            -0.165411,
-            -0.505255,
-            0.02837,
-            0.037576,
-            -0.0872855,
-            -0.0995285,
-            0.17943,
-            -0.01869,
-            -0.091724,
-            0.0953785,
-            0.18748,
-            0.0074185,
-            -0.161214,
-            -0.17399,
-            -0.15948,
-            0.07494,
-            0.0464,
-            -0.1653245,
-            0.27926,
-            -0.033632,
-            0.054218,
-            -0.015138,
-            0.0825805,
-            -0.000475,
-            -0.240335,
-            0.178475,
-            -0.367169,
-            -0.01351,
-            0.3854245,
-            -0.0323105,
-            0.0369245,
-            0.183225,
-            -0.09262565,
-            0.09580065,
-            -0.217905,
-            0.0637145,
-            0.33209,
-            0.184825,
-            -0.35325,
-            0.23516,
-            0.243119,
-            0.1659475,
-            0.0484775,
-            -0.00779,
-            0.20382,
-            -0.239638,
-            0.005275,
-            -0.027445
+            -0.248375,
+            -0.412895,
+            -0.0747755,
+            -0.1799,
+            0.091062,
+            0.070219,
+            -0.250764,
+            -0.24566,
+            -0.34612,
+            0.1894457,
+            -0.1634025,
+            0.138547,
+            -0.018338,
+            -0.18896,
+            -0.209461,
+            -0.05254,
+            -0.0576055,
+            0.680965,
+            -0.0954025,
+            -0.067748,
+            0.15022,
+            0.0549595,
+            -0.143155,
+            -0.006445,
+            -0.36555,
+            -0.10929505,
+            -0.0324625,
+            0.0712425,
+            -0.149912,
+            0.151961,
+            -0.108513,
+            0.0243845,
+            -0.39658,
+            0.29792,
+            0.13117,
+            0.0379539,
+            -0.0910175,
+            0.01787,
+            0.11663,
+            0.30831,
+            0.029185,
+            -0.011175,
+            0.44058,
+            -0.05671,
+            0.313375,
+            -0.0430835,
+            0.113345,
+            0.31116,
+            -0.069145,
+            -0.21548,
+            -0.045733,
+            -0.20525,
+            -0.011635,
+            -0.08891,
+            0.082544,
+            -0.01148,
+            0.096635,
+            -0.077375,
+            0.037033,
+            -0.11009675,
+            0.0901975,
+            0.016995,
+            -0.1049975,
+            -0.09705,
+            -0.10772,
+            -0.088945,
+            0.096265,
+            0.156865,
+            0.179865,
+            -0.1574545,
+            0.35942,
+            -0.016528,
+            0.26673,
+            0.3595075,
+            -0.35446,
+            -0.447885,
+            0.058625,
+            0.0544845,
+            0.197935,
+            -0.170365,
+            0.0094185,
+            0.05577,
+            -0.009455,
+            -0.27373,
+            -0.0978905,
+            0.1520625,
+            0.338575,
+            -0.0762515,
+            -0.1273965,
+            -0.06424,
+            0.032715,
+            0.036453,
+            -0.53973,
+            -0.062495,
+            0.165695,
+            0.1882635,
+            0.1158745,
+            0.05799565,
+            -0.24164,
+            0.02096,
+            0.21128,
+            -0.1083765,
+            0.1215055,
+            -0.1230715,
+            -0.042948,
+            0.104762,
+            0.1253575,
+            0.054417,
+            -0.060856,
+            0.34673,
+            -0.121887,
+            -0.1191485,
+            0.1369725,
+            -0.001175,
+            -0.178513,
+            0.01226,
+            0.1543335,
+            0.5242,
+            -0.1580005,
+            -0.244146,
+            0.067428,
+            -0.268605,
+            0.210485,
+            0.07,
+            -0.20048,
+            0.400445,
+            0.162785,
+            0.080435
           ],
           "selected_hits": [
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
             1,
             0,
             0,
@@ -328,60 +318,6 @@
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
-            0,
-            0,
-            0,
-            0,
-            0,
             1,
             0,
             0,
@@ -397,36 +333,100 @@
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
+            1,
             0,
             0
           ]
@@ -1328,6 +1328,902 @@
           "score": -0.027445,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 6332,
+          "gene": "GRB10",
+          "score": -0.248375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2982,
+          "gene": "CHSY3",
+          "score": -0.412895,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2681,
+          "gene": "CDV3",
+          "score": -0.0747755,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16710,
+          "gene": "TSEN54",
+          "score": -0.1799,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9420,
+          "gene": "MPZL3",
+          "score": 0.091062,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15222,
+          "gene": "STAT5A",
+          "score": 0.070219,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8172,
+          "gene": "LAMP1",
+          "score": -0.250764,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16035,
+          "gene": "TMCC1",
+          "score": -0.24566,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6383,
+          "gene": "GRPR",
+          "score": -0.34612,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4863,
+          "gene": "EPPIN",
+          "score": 0.1894457,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6793,
+          "gene": "HM13",
+          "score": -0.1634025,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6870,
+          "gene": "HOXA10",
+          "score": 0.138547,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2035,
+          "gene": "CACNA1B",
+          "score": -0.018338,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6983,
+          "gene": "HSPA1A",
+          "score": -0.18896,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2715,
+          "gene": "CELF3",
+          "score": -0.209461,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12273,
+          "gene": "PRDX4",
+          "score": -0.05254,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6909,
+          "gene": "HPD",
+          "score": -0.0576055,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5825,
+          "gene": "GART",
+          "score": 0.680965,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 9984,
+          "gene": "NDUFA4",
+          "score": -0.0954025,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11718,
+          "gene": "PIMREG",
+          "score": -0.067748,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5171,
+          "gene": "FAM221B",
+          "score": 0.15022,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 198,
+          "gene": "ACTA2",
+          "score": 0.0549595,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10235,
+          "gene": "NME6",
+          "score": -0.143155,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8949,
+          "gene": "MARCHF4",
+          "score": -0.006445,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12715,
+          "gene": "RAB11A",
+          "score": -0.36555,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9318,
+          "gene": "MMP1",
+          "score": -0.10929505,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8751,
+          "gene": "LYRM4",
+          "score": -0.0324625,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2940,
+          "gene": "CHRAC1",
+          "score": 0.0712425,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7733,
+          "gene": "KCTD8",
+          "score": -0.149912,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2787,
+          "gene": "CEP97",
+          "score": 0.151961,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1064,
+          "gene": "ARSI",
+          "score": -0.108513,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7703,
+          "gene": "KCNQ5",
+          "score": 0.0243845,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11022,
+          "gene": "OR9I1",
+          "score": -0.39658,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 594,
+          "gene": "ALYREF",
+          "score": 0.29792,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1223,
+          "gene": "ATP4A",
+          "score": 0.13117,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4691,
+          "gene": "EIF5A2",
+          "score": 0.0379539,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2034,
+          "gene": "CACNA1A",
+          "score": -0.0910175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5760,
+          "gene": "GABRR3",
+          "score": 0.01787,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4825,
+          "gene": "EPB41L1",
+          "score": 0.11663,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14006,
+          "gene": "SEZ6",
+          "score": 0.30831,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1911,
+          "gene": "C3orf79",
+          "score": 0.029185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9475,
+          "gene": "MRPL32",
+          "score": -0.011175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3190,
+          "gene": "CMTM7",
+          "score": 0.44058,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3510,
+          "gene": "CRLF2",
+          "score": -0.05671,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4565,
+          "gene": "EDNRA",
+          "score": 0.313375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5251,
+          "gene": "FAR2",
+          "score": -0.0430835,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11671,
+          "gene": "PIEZO2",
+          "score": 0.113345,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14220,
+          "gene": "SLBP",
+          "score": 0.31116,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1327,
+          "gene": "B3GALNT2",
+          "score": -0.069145,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6158,
+          "gene": "GOLGA8O",
+          "score": -0.21548,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 617,
+          "gene": "AMOTL1",
+          "score": -0.045733,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13974,
+          "gene": "SERPINE3",
+          "score": -0.20525,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13614,
+          "gene": "RXFP4",
+          "score": -0.011635,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1117,
+          "gene": "ASIC3",
+          "score": -0.08891,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2484,
+          "gene": "CD207",
+          "score": 0.082544,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6000,
+          "gene": "GJB1",
+          "score": -0.01148,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8896,
+          "gene": "MAP3K21",
+          "score": 0.096635,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5611,
+          "gene": "FOXR2",
+          "score": -0.077375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12088,
+          "gene": "PPA1",
+          "score": 0.037033,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11100,
+          "gene": "OXA1L",
+          "score": -0.11009675,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11351,
+          "gene": "PCDHGB3",
+          "score": 0.0901975,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13216,
+          "gene": "RIOX2",
+          "score": 0.016995,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5753,
+          "gene": "GABRG1",
+          "score": -0.1049975,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1406,
+          "gene": "BBS12",
+          "score": -0.09705,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7747,
+          "gene": "KDM4C",
+          "score": -0.10772,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12956,
+          "gene": "RBM34",
+          "score": -0.088945,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9482,
+          "gene": "MRPL39",
+          "score": 0.096265,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3499,
+          "gene": "CRIP3",
+          "score": 0.156865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18367,
+          "gene": "ZP3",
+          "score": 0.179865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5368,
+          "gene": "FCMR",
+          "score": -0.1574545,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14863,
+          "gene": "SP100",
+          "score": 0.35942,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13690,
+          "gene": "SAPCD2",
+          "score": -0.016528,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18371,
+          "gene": "ZPLD1",
+          "score": 0.26673,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16408,
+          "gene": "TOB2",
+          "score": 0.3595075,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10662,
+          "gene": "OR10A4",
+          "score": -0.35446,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9333,
+          "gene": "MMP26",
+          "score": -0.447885,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3867,
+          "gene": "DAZAP1",
+          "score": 0.058625,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1427,
+          "gene": "BCKDHA",
+          "score": 0.0544845,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9545,
+          "gene": "MS4A4E",
+          "score": 0.197935,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3337,
+          "gene": "COMMD5",
+          "score": -0.170365,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16411,
+          "gene": "TOGARAM2",
+          "score": 0.0094185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11325,
+          "gene": "PCDHB13",
+          "score": 0.05577,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14448,
+          "gene": "SLC35F5",
+          "score": -0.009455,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2174,
+          "gene": "CASP3",
+          "score": -0.27373,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14768,
+          "gene": "SNRPD3",
+          "score": -0.0978905,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13246,
+          "gene": "RNASE10",
+          "score": 0.1520625,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3182,
+          "gene": "CMPK2",
+          "score": 0.338575,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2690,
+          "gene": "CEACAM18",
+          "score": -0.0762515,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9609,
+          "gene": "MTERF4",
+          "score": -0.1273965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18052,
+          "gene": "ZNF451",
+          "score": -0.06424,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7410,
+          "gene": "IQCN",
+          "score": 0.032715,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5231,
+          "gene": "FAM98B",
+          "score": 0.036453,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4498,
+          "gene": "DYRK1A",
+          "score": -0.53973,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 9552,
+          "gene": "MSANTD3-TMEFF1",
+          "score": -0.062495,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8713,
+          "gene": "LUZP1",
+          "score": 0.165695,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5020,
+          "gene": "EXTL2",
+          "score": 0.1882635,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15061,
+          "gene": "SPTB",
+          "score": 0.1158745,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12057,
+          "gene": "POT1",
+          "score": 0.05799565,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8077,
+          "gene": "KRTAP19-5",
+          "score": -0.24164,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12578,
+          "gene": "PTGFRN",
+          "score": 0.02096,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4856,
+          "gene": "EPM2A",
+          "score": 0.21128,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 964,
+          "gene": "ARHGEF38",
+          "score": -0.1083765,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1186,
+          "gene": "ATMIN",
+          "score": 0.1215055,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2599,
+          "gene": "CDH13",
+          "score": -0.1230715,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13475,
+          "gene": "RPS26",
+          "score": -0.042948,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10046,
+          "gene": "NEK11",
+          "score": 0.104762,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2150,
+          "gene": "CARD18",
+          "score": 0.1253575,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12256,
+          "gene": "PRDM10",
+          "score": 0.054417,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5456,
+          "gene": "FHIP2A",
+          "score": -0.060856,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15121,
+          "gene": "SRSF12",
+          "score": 0.34673,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4422,
+          "gene": "DSTN",
+          "score": -0.121887,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15024,
+          "gene": "SPON2",
+          "score": -0.1191485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 865,
+          "gene": "APOLD1",
+          "score": 0.1369725,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10624,
+          "gene": "OLFM3",
+          "score": -0.001175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8958,
+          "gene": "MARF1",
+          "score": -0.178513,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12899,
+          "gene": "RASGRP4",
+          "score": 0.01226,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4888,
+          "gene": "ERCC4",
+          "score": 0.1543335,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13825,
+          "gene": "SDHC",
+          "score": 0.5242,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 10798,
+          "gene": "OR2T4",
+          "score": -0.1580005,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1271,
+          "gene": "ATP8A1",
+          "score": -0.244146,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14214,
+          "gene": "SLAIN2",
+          "score": 0.067428,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3319,
+          "gene": "COL7A1",
+          "score": -0.268605,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12406,
+          "gene": "PRR27",
+          "score": 0.210485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4891,
+          "gene": "ERCC6L",
+          "score": 0.07,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3090,
+          "gene": "CLEC14A",
+          "score": -0.20048,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13530,
+          "gene": "RSAD1",
+          "score": 0.400445,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2357,
+          "gene": "CCDC88A",
+          "score": 0.162785,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8155,
+          "gene": "LACTBL1",
+          "score": 0.080435,
+          "hit": 0,
+          "round": 1
         }
       ],
       "queried_history": [
@@ -2226,6 +3122,902 @@
           "score": -0.027445,
           "hit": 0,
           "round": 0
+        },
+        {
+          "candidate_index": 6332,
+          "gene": "GRB10",
+          "score": -0.248375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2982,
+          "gene": "CHSY3",
+          "score": -0.412895,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2681,
+          "gene": "CDV3",
+          "score": -0.0747755,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16710,
+          "gene": "TSEN54",
+          "score": -0.1799,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9420,
+          "gene": "MPZL3",
+          "score": 0.091062,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15222,
+          "gene": "STAT5A",
+          "score": 0.070219,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8172,
+          "gene": "LAMP1",
+          "score": -0.250764,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16035,
+          "gene": "TMCC1",
+          "score": -0.24566,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6383,
+          "gene": "GRPR",
+          "score": -0.34612,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4863,
+          "gene": "EPPIN",
+          "score": 0.1894457,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6793,
+          "gene": "HM13",
+          "score": -0.1634025,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6870,
+          "gene": "HOXA10",
+          "score": 0.138547,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2035,
+          "gene": "CACNA1B",
+          "score": -0.018338,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6983,
+          "gene": "HSPA1A",
+          "score": -0.18896,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2715,
+          "gene": "CELF3",
+          "score": -0.209461,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12273,
+          "gene": "PRDX4",
+          "score": -0.05254,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6909,
+          "gene": "HPD",
+          "score": -0.0576055,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5825,
+          "gene": "GART",
+          "score": 0.680965,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 9984,
+          "gene": "NDUFA4",
+          "score": -0.0954025,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11718,
+          "gene": "PIMREG",
+          "score": -0.067748,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5171,
+          "gene": "FAM221B",
+          "score": 0.15022,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 198,
+          "gene": "ACTA2",
+          "score": 0.0549595,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10235,
+          "gene": "NME6",
+          "score": -0.143155,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8949,
+          "gene": "MARCHF4",
+          "score": -0.006445,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12715,
+          "gene": "RAB11A",
+          "score": -0.36555,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9318,
+          "gene": "MMP1",
+          "score": -0.10929505,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8751,
+          "gene": "LYRM4",
+          "score": -0.0324625,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2940,
+          "gene": "CHRAC1",
+          "score": 0.0712425,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7733,
+          "gene": "KCTD8",
+          "score": -0.149912,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2787,
+          "gene": "CEP97",
+          "score": 0.151961,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1064,
+          "gene": "ARSI",
+          "score": -0.108513,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7703,
+          "gene": "KCNQ5",
+          "score": 0.0243845,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11022,
+          "gene": "OR9I1",
+          "score": -0.39658,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 594,
+          "gene": "ALYREF",
+          "score": 0.29792,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1223,
+          "gene": "ATP4A",
+          "score": 0.13117,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4691,
+          "gene": "EIF5A2",
+          "score": 0.0379539,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2034,
+          "gene": "CACNA1A",
+          "score": -0.0910175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5760,
+          "gene": "GABRR3",
+          "score": 0.01787,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4825,
+          "gene": "EPB41L1",
+          "score": 0.11663,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14006,
+          "gene": "SEZ6",
+          "score": 0.30831,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1911,
+          "gene": "C3orf79",
+          "score": 0.029185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9475,
+          "gene": "MRPL32",
+          "score": -0.011175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3190,
+          "gene": "CMTM7",
+          "score": 0.44058,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3510,
+          "gene": "CRLF2",
+          "score": -0.05671,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4565,
+          "gene": "EDNRA",
+          "score": 0.313375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5251,
+          "gene": "FAR2",
+          "score": -0.0430835,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11671,
+          "gene": "PIEZO2",
+          "score": 0.113345,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14220,
+          "gene": "SLBP",
+          "score": 0.31116,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1327,
+          "gene": "B3GALNT2",
+          "score": -0.069145,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6158,
+          "gene": "GOLGA8O",
+          "score": -0.21548,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 617,
+          "gene": "AMOTL1",
+          "score": -0.045733,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13974,
+          "gene": "SERPINE3",
+          "score": -0.20525,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13614,
+          "gene": "RXFP4",
+          "score": -0.011635,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1117,
+          "gene": "ASIC3",
+          "score": -0.08891,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2484,
+          "gene": "CD207",
+          "score": 0.082544,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 6000,
+          "gene": "GJB1",
+          "score": -0.01148,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8896,
+          "gene": "MAP3K21",
+          "score": 0.096635,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5611,
+          "gene": "FOXR2",
+          "score": -0.077375,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12088,
+          "gene": "PPA1",
+          "score": 0.037033,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11100,
+          "gene": "OXA1L",
+          "score": -0.11009675,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11351,
+          "gene": "PCDHGB3",
+          "score": 0.0901975,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13216,
+          "gene": "RIOX2",
+          "score": 0.016995,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5753,
+          "gene": "GABRG1",
+          "score": -0.1049975,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1406,
+          "gene": "BBS12",
+          "score": -0.09705,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7747,
+          "gene": "KDM4C",
+          "score": -0.10772,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12956,
+          "gene": "RBM34",
+          "score": -0.088945,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9482,
+          "gene": "MRPL39",
+          "score": 0.096265,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3499,
+          "gene": "CRIP3",
+          "score": 0.156865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18367,
+          "gene": "ZP3",
+          "score": 0.179865,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5368,
+          "gene": "FCMR",
+          "score": -0.1574545,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14863,
+          "gene": "SP100",
+          "score": 0.35942,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13690,
+          "gene": "SAPCD2",
+          "score": -0.016528,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18371,
+          "gene": "ZPLD1",
+          "score": 0.26673,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16408,
+          "gene": "TOB2",
+          "score": 0.3595075,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10662,
+          "gene": "OR10A4",
+          "score": -0.35446,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9333,
+          "gene": "MMP26",
+          "score": -0.447885,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 3867,
+          "gene": "DAZAP1",
+          "score": 0.058625,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1427,
+          "gene": "BCKDHA",
+          "score": 0.0544845,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9545,
+          "gene": "MS4A4E",
+          "score": 0.197935,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3337,
+          "gene": "COMMD5",
+          "score": -0.170365,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 16411,
+          "gene": "TOGARAM2",
+          "score": 0.0094185,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 11325,
+          "gene": "PCDHB13",
+          "score": 0.05577,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14448,
+          "gene": "SLC35F5",
+          "score": -0.009455,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2174,
+          "gene": "CASP3",
+          "score": -0.27373,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14768,
+          "gene": "SNRPD3",
+          "score": -0.0978905,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13246,
+          "gene": "RNASE10",
+          "score": 0.1520625,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3182,
+          "gene": "CMPK2",
+          "score": 0.338575,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2690,
+          "gene": "CEACAM18",
+          "score": -0.0762515,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 9609,
+          "gene": "MTERF4",
+          "score": -0.1273965,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 18052,
+          "gene": "ZNF451",
+          "score": -0.06424,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 7410,
+          "gene": "IQCN",
+          "score": 0.032715,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5231,
+          "gene": "FAM98B",
+          "score": 0.036453,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4498,
+          "gene": "DYRK1A",
+          "score": -0.53973,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 9552,
+          "gene": "MSANTD3-TMEFF1",
+          "score": -0.062495,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8713,
+          "gene": "LUZP1",
+          "score": 0.165695,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5020,
+          "gene": "EXTL2",
+          "score": 0.1882635,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15061,
+          "gene": "SPTB",
+          "score": 0.1158745,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12057,
+          "gene": "POT1",
+          "score": 0.05799565,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8077,
+          "gene": "KRTAP19-5",
+          "score": -0.24164,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12578,
+          "gene": "PTGFRN",
+          "score": 0.02096,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4856,
+          "gene": "EPM2A",
+          "score": 0.21128,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 964,
+          "gene": "ARHGEF38",
+          "score": -0.1083765,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1186,
+          "gene": "ATMIN",
+          "score": 0.1215055,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2599,
+          "gene": "CDH13",
+          "score": -0.1230715,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13475,
+          "gene": "RPS26",
+          "score": -0.042948,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10046,
+          "gene": "NEK11",
+          "score": 0.104762,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 2150,
+          "gene": "CARD18",
+          "score": 0.1253575,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12256,
+          "gene": "PRDM10",
+          "score": 0.054417,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 5456,
+          "gene": "FHIP2A",
+          "score": -0.060856,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15121,
+          "gene": "SRSF12",
+          "score": 0.34673,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4422,
+          "gene": "DSTN",
+          "score": -0.121887,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 15024,
+          "gene": "SPON2",
+          "score": -0.1191485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 865,
+          "gene": "APOLD1",
+          "score": 0.1369725,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 10624,
+          "gene": "OLFM3",
+          "score": -0.001175,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8958,
+          "gene": "MARF1",
+          "score": -0.178513,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12899,
+          "gene": "RASGRP4",
+          "score": 0.01226,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4888,
+          "gene": "ERCC4",
+          "score": 0.1543335,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13825,
+          "gene": "SDHC",
+          "score": 0.5242,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 10798,
+          "gene": "OR2T4",
+          "score": -0.1580005,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 1271,
+          "gene": "ATP8A1",
+          "score": -0.244146,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 14214,
+          "gene": "SLAIN2",
+          "score": 0.067428,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3319,
+          "gene": "COL7A1",
+          "score": -0.268605,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 12406,
+          "gene": "PRR27",
+          "score": 0.210485,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 4891,
+          "gene": "ERCC6L",
+          "score": 0.07,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 3090,
+          "gene": "CLEC14A",
+          "score": -0.20048,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 13530,
+          "gene": "RSAD1",
+          "score": 0.400445,
+          "hit": 1,
+          "round": 1
+        },
+        {
+          "candidate_index": 2357,
+          "gene": "CCDC88A",
+          "score": 0.162785,
+          "hit": 0,
+          "round": 1
+        },
+        {
+          "candidate_index": 8155,
+          "gene": "LACTBL1",
+          "score": 0.080435,
+          "hit": 0,
+          "round": 1
         }
       ]
     }

```
