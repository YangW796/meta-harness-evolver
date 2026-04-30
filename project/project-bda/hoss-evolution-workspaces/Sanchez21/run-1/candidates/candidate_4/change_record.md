# Change Record — candidate_4

Compared against: /inspire/qb-ilm/project/cq-scientific-cooperation-zone/public/ywang/meta-harness-evolver/project/test/project-bda/hoss-evolution-workspaces/Sanchez21/run-1/best/current/harness
Generated at: 2026-04-30T06:56:05.122749

## Files Changed

- model.py: modified (added=67, deleted=17, delta=50)
- outputs/metrics.json: modified (added=2394, deleted=602, delta=1792)

## Diffs

### model.py

```diff
--- best/model.py
+++ candidate/model.py
@@ -73,8 +73,16 @@
             # Try to use gene search if available
             try:
                 import bda_tools
-                # Sample from top performers and find similar genes
-                num_to_sample = min(5, len(top_performers))
+                
+                # If hit information is available, prioritize actual hits over just high absolute scores
+                if any('hit' in h for h in history):
+                    hit_indices = [h['candidate_index'] for h in history if h.get('hit') == 1]
+                    if hit_indices:
+                        # Prioritize genes that are actual hits
+                        top_performers = hit_indices[:min(len(hit_indices), top_k)]
+                
+                # Sample more aggressively from top performers
+                num_to_sample = min(10, len(top_performers))
                 sampled_top = rng.sample(top_performers, num_to_sample)
                 
                 for top_idx in sampled_top:
@@ -85,7 +93,8 @@
                     gene = candidate.get('gene') or candidate.get('gene_a')
                     if gene:
                         try:
-                            similar = bda_tools.gene_search(gene, k=min(20, num_exploit), diverse=False)
+                            # Search for similar genes with higher k
+                            similar = bda_tools.gene_search(gene, k=min(30, num_exploit * 2), diverse=False)
                             for idx in similar:
                                 if idx in remaining_avail and idx not in exploit_candidates:
                                     exploit_candidates.add(idx)
@@ -93,28 +102,69 @@
                                         break
                         except:
                             pass
+                
+                # If we still need candidates, also try diverse search around top performers
+                if len(exploit_candidates) < num_exploit:
+                    for top_idx in sampled_top:
+                        if len(exploit_candidates) >= num_exploit:
+                            break
+                        candidate = candidates[top_idx]
+                        gene = candidate.get('gene') or candidate.get('gene_a')
+                        if gene:
+                            try:
+                                # Try diverse search for broader coverage
+                                diverse_similar = bda_tools.gene_search(gene, k=min(20, num_exploit - len(exploit_candidates)), diverse=True)
+                                for idx in diverse_similar:
+                                    if idx in remaining_avail and idx not in exploit_candidates:
+                                        exploit_candidates.add(idx)
+                                        if len(exploit_candidates) >= num_exploit:
+                                            break
+                            except:
+                                pass
             except ImportError:
                 # bda_tools not available, fall back to other strategies
                 pass
             
-            # If we still need more candidates, use weighted sampling
+            # If we still need more candidates, use weighted sampling based on score patterns
             if len(exploit_candidates) < num_exploit:
                 needed = num_exploit - len(exploit_candidates)
-                # Use stratified sampling for diversity: divide remaining into buckets
-                num_buckets = min(10, len(remaining_avail))
-                bucket_size = len(remaining_avail) // num_buckets
                 
-                sampled = set()
-                for bucket in range(num_buckets):
-                    if len(sampled) >= needed:
-                        break
-                    start = bucket * bucket_size
-                    end = start + bucket_size if bucket < num_buckets - 1 else len(remaining_avail)
-                    bucket_items = remaining_avail[start:end]
-                    if bucket_items:
-                        sampled.add(rng.choice(bucket_items))
+                # Analyze score distribution to target both extremes
+                scores = [h['score'] for h in history]
+                if scores:
+                    # Target both very negative and near-zero regions
+                    extreme_negative = [h['candidate_index'] for h in history if h['score'] < -2.0]
+                    near_zero = [h['candidate_index'] for h in history if abs(h['score']) < 0.1]
+                    
+                    # Sample from both regions if available
+                    if extreme_negative and needed > 1:
+                        idx = rng.choice(extreme_negative)
+                        if idx in remaining_avail and idx not in exploit_candidates:
+                            exploit_candidates.add(idx)
+                            needed -= 1
+                    
+                    if near_zero and needed > 0:
+                        idx = rng.choice(near_zero)
+                        if idx in remaining_avail and idx not in exploit_candidates:
+                            exploit_candidates.add(idx)
+                            needed -= 1
                 
-                exploit_candidates.update(sampled)
+                # Use stratified sampling for remaining diversity
+                if needed > 0:
+                    num_buckets = min(10, len(remaining_avail))
+                    bucket_size = len(remaining_avail) // num_buckets
+                    
+                    sampled = set()
+                    for bucket in range(num_buckets):
+                        if len(sampled) >= needed:
+                            break
+                        start = bucket * bucket_size
+                        end = start + bucket_size if bucket < num_buckets - 1 else len(remaining_avail)
+                        bucket_items = remaining_avail[start:end]
+                        if bucket_items:
+                            sampled.add(rng.choice(bucket_items))
+                    
+                    exploit_candidates.update(sampled)
         
         selected_indices = list(explore_indices) + list(exploit_candidates)[:num_exploit]
     else:

```

### outputs/metrics.json

```diff
--- best/outputs/metrics.json
+++ candidate/outputs/metrics.json
@@ -9,296 +9,296 @@
   "metrics": {
     "test": {
       "pool_size": 18469,
-      "rounds": 3,
+      "rounds": 4,
       "executed_rounds": 1,
       "batch_size": 128,
       "seed": 42,
-      "baseline_total_queries": 256,
-      "baseline_total_hits": 15,
+      "baseline_total_queries": 384,
+      "baseline_total_hits": 18,
       "delta_queries": 128,
-      "delta_hits": 3,
-      "total_queries": 384,
-      "total_hits": 18,
+      "delta_hits": 11,
+      "total_queries": 512,
+      "total_hits": 29,
       "top_k": 924,
       "hit_curve": {
         "queries": [
-          256,
-          384
+          384,
+          512
         ],
         "hits": [
-          15,
-          18
+          18,
+          29
         ]
       },
-      "auc": 2112.0,
-      "auc_normalized": 0.005952380952380952,
-      "ncg": 0.24958945340405878,
+      "auc": 3008.0,
+      "auc_normalized": 0.006358225108225108,
+      "ncg": 0.2690165741423913,
       "round_details": [
         {
-          "round": 2,
+          "round": 3,
           "selected_count": 128,
-          "hits": 3,
-          "cumulative_hits": 18,
-          "precision_at_batch": 0.0234375,
+          "hits": 11,
+          "cumulative_hits": 29,
+          "precision_at_batch": 0.0859375,
           "selected": [
-            "RTEL1",
-            "VAPB",
-            "ZNF280A",
-            "DCPS",
-            "GANAB",
-            "PTPRN",
-            "IPP",
-            "MRPL43",
-            "ARHGEF11",
-            "INTS8",
-            "ADAT2",
-            "CORT",
-            "FAM26E",
-            "UCN3",
-            "NCKAP1",
-            "PTMA",
-            "RPP25L",
-            "OR1N2",
-            "PNLIPRP1",
-            "CCT7",
-            "PCDH7",
-            "MIR432",
-            "FAM96B",
-            "CYP1A1",
-            "UBC",
-            "CCDC77",
-            "CMYA5",
-            "MAN2B1",
-            "NPTX2",
-            "CTC1",
-            "MRPL48",
-            "ATAD2",
-            "PDZD4",
-            "RALB",
-            "CNPY3",
-            "TGFB1",
-            "TEX33",
-            "GPR32",
-            "GPD1",
-            "DPP4",
-            "LOC100506127",
-            "KRTAP4-7",
-            "BRSK1",
-            "BCDIN3D",
-            "SLC39A6",
-            "ATP5O",
-            "OR52N2",
-            "PRKAG1",
-            "TBCC",
-            "SPTAN1",
-            "ZNF208",
-            "FABP3",
-            "KCNJ2",
-            "TMED3",
-            "SRSF3",
-            "PEX5",
-            "BCL11A",
-            "MEGF6",
-            "FAM49A",
-            "ADCY9",
-            "INCENP",
-            "AK2",
-            "ZNF345",
-            "MICU2",
-            "PLK5",
-            "HAS3",
-            "RPL3L",
-            "CYBB",
-            "POLR3G",
-            "PCDHGA8",
-            "CYP2A13",
-            "INPP4B",
-            "C9orf85",
-            "SLC27A2",
-            "BPIFB3",
-            "TDG",
-            "C4A",
-            "F2R",
-            "KLF1",
-            "PASD1",
-            "C17orf67",
-            "SPANXC",
-            "TRIM42",
-            "HMGB3",
-            "NT5DC3",
-            "RPS4Y2",
-            "SLC4A5",
-            "MCF2L2",
-            "GDF15",
-            "WDR60",
-            "GRK5",
-            "CADM4",
-            "MGAM",
-            "TMEM156",
-            "LRRFIP2",
-            "CAV2",
-            "UGT2B7",
-            "OSR2",
-            "ZNF627",
-            "TMEM59",
-            "CBWD2",
-            "MOB3B",
-            "TNFSF13",
-            "NAPRT",
-            "RPGRIP1",
-            "RPP40",
-            "NCS1",
-            "ZNF671",
-            "SPINK6",
-            "CCRL2",
-            "NTS",
-            "LEO1",
-            "DUOXA1",
-            "DUSP26",
-            "DUSP28",
-            "CD300E",
-            "SMURF2",
-            "RIT1",
-            "PGBD3",
-            "SNX10",
-            "CFC1",
-            "MCIDAS",
-            "DYSF",
-            "MFAP3L",
-            "ZDHHC5",
-            "TSTA3",
-            "PPID",
-            "KRI1"
+            "MATN1",
+            "SERPINB8",
+            "TMOD3",
+            "LOC728763",
+            "CEP126",
+            "NDUFS1",
+            "PCNXL3",
+            "ANKRD35",
+            "CCPG1",
+            "TMEM220",
+            "ADORA3",
+            "DCAF4L1",
+            "MOGAT3",
+            "DDX42",
+            "NOP56",
+            "ATG4C",
+            "CCDC124",
+            "EDN2",
+            "MASP1",
+            "FAM19A5",
+            "HSD17B4",
+            "SLC24A4",
+            "CD53",
+            "SACM1L",
+            "EPB42",
+            "C7orf73",
+            "ARSB",
+            "FXYD5",
+            "ODF2",
+            "LETM1",
+            "POC1B-GALNT4",
+            "OAZ1",
+            "CMTM4",
+            "SCHIP1",
+            "CLCN2",
+            "ANKRD27",
+            "OS9",
+            "NUCB2",
+            "RBM23",
+            "ZC3H15",
+            "ZNF214",
+            "LIN52",
+            "CACFD1",
+            "TP53INP2",
+            "PSMD9",
+            "HPS6",
+            "PLA2G4B",
+            "FAM46D",
+            "ALG13",
+            "LCE1B",
+            "TSC22D1",
+            "SIPA1L1",
+            "MVK",
+            "HRASLS5",
+            "SEC61B",
+            "RASGRP3",
+            "RAB1B",
+            "PABPC5",
+            "KCNH3",
+            "SULT1A1",
+            "GNB2L1",
+            "BRF1",
+            "TRPV4",
+            "DRP2",
+            "CD163L1",
+            "MRPL37",
+            "SLAMF8",
+            "RPS20",
+            "CRISP2",
+            "ABI3",
+            "PPP2R5D",
+            "MIA3",
+            "STKLD1",
+            "SNAI3",
+            "HEY1",
+            "P2RX2",
+            "MAST4",
+            "KRT23",
+            "VWF",
+            "ITFG1",
+            "TREX1",
+            "ARGLU1",
+            "F9",
+            "ANO8",
+            "LTK",
+            "TMEM133",
+            "CNTN6",
+            "GAPT",
+            "IFIH1",
+            "CARD18",
+            "CLK1",
+            "CBL",
+            "DYNC2LI1",
+            "RHOV",
+            "FGFR4",
+            "CERS5",
+            "SPIN4",
+            "RETSAT",
+            "MFSD12",
+            "RANBP6",
+            "RPUSD3",
+            "PYHIN1",
+            "FGF11",
+            "YEATS4",
+            "ARL14",
+            "CCR7",
+            "OPRL1",
+            "SEPT9",
+            "KIAA0100",
+            "OR10G3",
+            "PRDM9",
+            "SMIM24",
+            "IFT52",
+            "RHOA",
+            "WDR48",
+            "ZNF432",
+            "ABCA3",
+            "SEC24D",
+            "ASCL1",
+            "TCEAL2",
+            "C7orf60",
+            "KDELR2",
+            "KBTBD3",
+            "ITGAE",
+            "CAMTA1",
+            "BTBD17",
+            "CHI3L2",
+            "PRY"
           ],
           "selected_scores": [
-            -1.4855187669999999,
-            -1.2703910729999999,
-            -0.7558665640000001,
-            -1.195998507,
-            -0.63300024,
-            -0.9694214790000001,
-            -0.29513096,
-            -0.815280817,
-            -0.657764427,
-            -2.515189464,
-            -0.181357057,
-            -0.140774507,
-            -1.0365657959999999,
-            -2.0068613999999996,
-            -0.614692695,
-            -1.038748139,
-            -1.405789679,
-            -0.63151199,
-            -0.519566309,
-            -0.704492129,
-            -0.779044927,
-            -0.047927155,
-            -0.890342008,
-            -0.246907181,
-            -1.242476262,
-            -1.112939553,
-            -0.648189609,
-            -0.9480956159999999,
-            -2.401567439,
-            -0.278952628,
-            -0.373296909,
-            -0.534442847,
-            -1.689643157,
-            -0.827657419,
-            -0.22900884300000002,
-            -0.323883879,
-            -1.320435759,
-            -0.491993019,
-            -2.039463539,
-            -0.6797851090000001,
-            -1.118812634,
-            -3.346861492,
-            -0.236795593,
-            -0.8460896000000001,
-            -0.32367678,
-            -1.1252520990000001,
-            -0.842105975,
-            -1.2557984759999998,
-            -1.462807671,
-            -0.28914351,
-            -1.4629832409999999,
-            -0.6001938529999999,
-            -0.685301266,
-            -1.895656615,
-            -1.1955252440000002,
-            -1.004241742,
-            -0.608515755,
-            -0.441613959,
-            -0.45734107399999996,
-            -0.494880649,
-            -0.411976677,
-            -0.43550246600000003,
-            -0.7923046420000001,
-            -0.48885202,
-            -0.285187163,
-            -0.366737059,
-            -1.973648408,
-            -1.4469121919999999,
-            -0.34459338799999994,
-            -1.08085994,
-            -0.7921534929999999,
-            -0.576914143,
-            -0.9804685870000001,
-            -0.111658109,
-            -2.264809504,
-            -0.066540241,
-            -0.298375674,
-            -0.382332281,
-            -0.291552926,
-            -0.37730578200000003,
-            -1.124229479,
-            -0.608521103,
-            -1.022118105,
-            -1.0863716190000001,
-            -0.61964227,
-            -0.48291109299999996,
-            -2.063871355,
-            -0.420416412,
-            -1.127234176,
-            -0.40373960299999995,
-            -0.342649714,
-            -0.66884535,
-            -0.32805284,
-            -1.398034435,
-            -1.549298755,
-            -0.404721396,
-            -0.353900724,
-            -0.612890566,
-            -0.315584109,
-            -0.226062235,
-            -1.26286739,
-            -1.154290228,
-            -0.593435607,
-            -0.43343086700000005,
-            -1.242310251,
-            -1.092353034,
-            -0.167400781,
-            -1.530213681,
-            -0.235857347,
-            -2.039709218,
-            -0.349507898,
-            -1.901654728,
-            -1.175281715,
-            -0.354934275,
-            -0.212464882,
-            -0.416952297,
-            -1.7582445430000002,
-            -0.79174172,
-            -0.128372143,
-            -0.774897576,
-            -1.932787094,
-            -0.118253991,
-            -1.499861251,
-            -1.064490566,
-            -1.040591794,
-            -0.156054917,
-            -0.384717194,
-            -1.111219665
+            -0.4104380999999999,
+            -0.329490148,
+            -0.22175702600000002,
+            -1.1886534709999999,
+            -0.156549957,
+            -0.5231745529999999,
+            -1.567926415,
+            -0.519084251,
+            -0.461368483,
+            -1.182195947,
+            -1.2535028959999999,
+            -1.23915844,
+            -0.702892028,
+            -1.368088589,
+            -3.12504232,
+            -1.294710559,
+            -1.3287066109999999,
+            -0.223556442,
+            -0.966823482,
+            -1.176611027,
+            -0.9546285259999999,
+            -0.662405857,
+            -1.053278716,
+            -2.148767173,
+            -0.061137486,
+            -0.396462735,
+            -0.5009418520000001,
+            -0.33476787399999997,
+            -0.469909029,
+            -0.559237908,
+            -0.11615138300000001,
+            -0.32720166300000003,
+            -0.716024876,
+            -1.139779623,
+            -1.1597699479999999,
+            -0.7868462820000001,
+            -0.23046398,
+            -0.628037608,
+            -0.743159424,
+            -4.642818375,
+            -0.434667445,
+            -3.093945923,
+            -0.6513169289999999,
+            -0.47062887600000003,
+            -0.604428159,
+            -1.890446505,
+            -0.477295927,
+            -0.070973971,
+            -2.780068955,
+            -0.664128853,
+            -2.02432083,
+            -0.8523889179999999,
+            -0.33314050100000003,
+            -0.17696316399999998,
+            -0.732267441,
+            -2.396689074,
+            -0.590366287,
+            -0.775620894,
+            -0.504159483,
+            -1.1862740440000001,
+            -1.769044294,
+            -1.374109684,
+            -0.72425143,
+            -1.152236536,
+            -1.4734528830000002,
+            -2.2005796159999997,
+            -0.646016172,
+            -1.065640001,
+            -0.481033955,
+            -0.18754147399999999,
+            -0.370238175,
+            -0.6449656570000001,
+            -0.166186834,
+            -0.774750712,
+            -2.094411689,
+            -0.58233107,
+            -1.059639734,
+            -0.09050302199999999,
+            -0.584625911,
+            -1.19117938,
+            -0.342036268,
+            -3.2208133180000003,
+            -0.644513575,
+            -1.947826808,
+            -0.7503026909999999,
+            -2.072937505,
+            -0.812852122,
+            -0.663318773,
+            -0.5536093000000001,
+            -0.6228774029999999,
+            -0.270706545,
+            -0.204112658,
+            -0.47467650899999997,
+            -0.392412264,
+            -0.593319123,
+            -0.19005876800000002,
+            -0.023098108,
+            -1.03093522,
+            -3.015320243,
+            -0.542753612,
+            -1.2502314829999999,
+            -0.548085777,
+            -2.175442962,
+            -1.1739566909999999,
+            -0.496439061,
+            -0.32461639800000003,
+            -0.746379056,
+            -0.326716425,
+            -0.580674799,
+            -0.823717975,
+            -0.669017746,
+            -0.29737308100000004,
+            -1.4153385,
+            -2.9459395660000003,
+            -0.528011775,
+            -1.8124296130000002,
+            -0.21133955100000001,
+            -0.7292541159999999,
+            -0.18055578100000003,
+            -0.8765485590000001,
+            -0.546959614,
+            -0.487717731,
+            -1.066628225,
+            -0.215583203,
+            -0.456741119,
+            -0.126790438,
+            -0.885074315,
+            -0.83277222
           ],
           "selected_hits": [
             0,
@@ -315,13 +315,6 @@
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
             1,
             0,
             0,
@@ -332,16 +325,6 @@
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
             1,
             0,
             0,
@@ -357,64 +340,81 @@
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
             1,
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
+            1,
+            0,
+            0,
+            0,
+            0,
+            0,
+            1,
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
+            1,
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
             0,
             0,
             0,
@@ -2230,896 +2230,1792 @@
           "gene": "RTEL1",
           "score": -1.4855187669999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17277,
           "gene": "VAPB",
           "score": -1.2703910729999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18007,
           "gene": "ZNF280A",
           "score": -0.7558665640000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3889,
           "gene": "DCPS",
           "score": -1.195998507,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5884,
           "gene": "GANAB",
           "score": -0.63300024,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12623,
           "gene": "PTPRN",
           "score": -0.9694214790000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7497,
           "gene": "IPP",
           "score": -0.29513096,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9635,
           "gene": "MRPL43",
           "score": -0.815280817,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 963,
           "gene": "ARHGEF11",
           "score": -0.657764427,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7481,
           "gene": "INTS8",
           "score": -2.515189464,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 291,
           "gene": "ADAT2",
           "score": -0.181357057,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3338,
           "gene": "CORT",
           "score": -0.140774507,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5221,
           "gene": "FAM26E",
           "score": -1.0365657959999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17069,
           "gene": "UCN3",
           "score": -2.0068613999999996,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10080,
           "gene": "NCKAP1",
           "score": -0.614692695,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12585,
           "gene": "PTMA",
           "score": -1.038748139,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13467,
           "gene": "RPP25L",
           "score": -1.405789679,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10843,
           "gene": "OR1N2",
           "score": -0.63151199,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11912,
           "gene": "PNLIPRP1",
           "score": -0.519566309,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2447,
           "gene": "CCT7",
           "score": -0.704492129,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11266,
           "gene": "PCDH7",
           "score": -0.779044927,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9408,
           "gene": "MIR432",
           "score": -0.047927155,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5300,
           "gene": "FAM96B",
           "score": -0.890342008,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3735,
           "gene": "CYP1A1",
           "score": -0.246907181,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16980,
           "gene": "UBC",
           "score": -1.242476262,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2331,
           "gene": "CCDC77",
           "score": -1.112939553,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3151,
           "gene": "CMYA5",
           "score": -0.648189609,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8986,
           "gene": "MAN2B1",
           "score": -0.9480956159999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10490,
           "gene": "NPTX2",
           "score": -2.401567439,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3590,
           "gene": "CTC1",
           "score": -0.278952628,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9640,
           "gene": "MRPL48",
           "score": -0.373296909,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1160,
           "gene": "ATAD2",
           "score": -0.534442847,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11455,
           "gene": "PDZD4",
           "score": -1.689643157,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12833,
           "gene": "RALB",
           "score": -0.827657419,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3193,
           "gene": "CNPY3",
           "score": -0.22900884300000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15861,
           "gene": "TGFB1",
           "score": -0.323883879,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15823,
           "gene": "TEX33",
           "score": -1.320435759,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6347,
           "gene": "GPR32",
           "score": -0.491993019,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6281,
           "gene": "GPD1",
           "score": -2.039463539,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4336,
           "gene": "DPP4",
           "score": -0.6797851090000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8594,
           "gene": "LOC100506127",
           "score": -1.118812634,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8253,
           "gene": "KRTAP4-7",
           "score": -3.346861492,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1634,
           "gene": "BRSK1",
           "score": -0.236795593,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1442,
           "gene": "BCDIN3D",
           "score": -0.8460896000000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14505,
           "gene": "SLC39A6",
           "score": -0.32367678,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1255,
           "gene": "ATP5O",
           "score": -1.1252520990000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10927,
           "gene": "OR52N2",
           "score": -0.842105975,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12285,
           "gene": "PRKAG1",
           "score": -1.2557984759999998,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15651,
           "gene": "TBCC",
           "score": -1.462807671,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15079,
           "gene": "SPTAN1",
           "score": -0.28914351,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17960,
           "gene": "ZNF208",
           "score": -1.4629832409999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5017,
           "gene": "FABP3",
           "score": -0.6001938529999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7766,
           "gene": "KCNJ2",
           "score": -0.685301266,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16063,
           "gene": "TMED3",
           "score": -1.895656615,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15144,
           "gene": "SRSF3",
           "score": -1.1955252440000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11500,
           "gene": "PEX5",
           "score": -1.004241742,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1448,
           "gene": "BCL11A",
           "score": -0.608515755,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9252,
           "gene": "MEGF6",
           "score": -0.441613959,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5241,
           "gene": "FAM49A",
           "score": -0.45734107399999996,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 307,
           "gene": "ADCY9",
           "score": -0.494880649,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7429,
           "gene": "INCENP",
           "score": -0.411976677,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 482,
           "gene": "AK2",
           "score": -0.43550246600000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18048,
           "gene": "ZNF345",
           "score": -0.7923046420000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9375,
           "gene": "MICU2",
           "score": -0.48885202,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11858,
           "gene": "PLK5",
           "score": -0.285187163,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6626,
           "gene": "HAS3",
           "score": -0.366737059,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13450,
           "gene": "RPL3L",
           "score": -1.973648408,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3719,
           "gene": "CYBB",
           "score": -1.4469121919999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12001,
           "gene": "POLR3G",
           "score": -0.34459338799999994,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11310,
           "gene": "PCDHGA8",
           "score": -1.08085994,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3747,
           "gene": "CYP2A13",
           "score": -0.7921534929999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7450,
           "gene": "INPP4B",
           "score": -0.576914143,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1968,
           "gene": "C9orf85",
           "score": -0.9804685870000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14402,
           "gene": "SLC27A2",
           "score": -0.111658109,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1593,
           "gene": "BPIFB3",
           "score": -2.264809504,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15752,
           "gene": "TDG",
           "score": -0.066540241,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1859,
           "gene": "C4A",
           "score": -0.298375674,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4999,
           "gene": "F2R",
           "score": -0.382332281,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8011,
           "gene": "KLF1",
           "score": -0.291552926,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11216,
           "gene": "PASD1",
           "score": -0.37730578200000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1745,
           "gene": "C17orf67",
           "score": -1.124229479,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14929,
           "gene": "SPANXC",
           "score": -0.608521103,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16629,
           "gene": "TRIM42",
           "score": -1.022118105,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6905,
           "gene": "HMGB3",
           "score": -1.0863716190000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10587,
           "gene": "NT5DC3",
           "score": -0.61964227,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13503,
           "gene": "RPS4Y2",
           "score": -0.48291109299999996,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14540,
           "gene": "SLC4A5",
           "score": -2.063871355,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9162,
           "gene": "MCF2L2",
           "score": -0.420416412,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5972,
           "gene": "GDF15",
           "score": -1.127234176,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17482,
           "gene": "WDR60",
           "score": -0.40373960299999995,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6447,
           "gene": "GRK5",
           "score": -0.342649714,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2035,
           "gene": "CADM4",
           "score": -0.66884535,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9342,
           "gene": "MGAM",
           "score": -0.32805284,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16132,
           "gene": "TMEM156",
           "score": -1.398034435,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8780,
           "gene": "LRRFIP2",
           "score": -1.549298755,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2172,
           "gene": "CAV2",
           "score": -0.404721396,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17102,
           "gene": "UGT2B7",
           "score": -0.353900724,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11022,
           "gene": "OSR2",
           "score": -0.612890566,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18241,
           "gene": "ZNF627",
           "score": -0.315584109,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16281,
           "gene": "TMEM59",
           "score": -0.226062235,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2190,
           "gene": "CBWD2",
           "score": -1.26286739,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9502,
           "gene": "MOB3B",
           "score": -1.154290228,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16398,
           "gene": "TNFSF13",
           "score": -0.593435607,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10025,
           "gene": "NAPRT",
           "score": -0.43343086700000005,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13405,
           "gene": "RPGRIP1",
           "score": -1.242310251,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13470,
           "gene": "RPP40",
           "score": -1.092353034,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10101,
           "gene": "NCS1",
           "score": -0.167400781,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18267,
           "gene": "ZNF671",
           "score": -1.530213681,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15022,
           "gene": "SPINK6",
           "score": -0.235857347,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2435,
           "gene": "CCRL2",
           "score": -2.039709218,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10607,
           "gene": "NTS",
           "score": -0.349507898,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8431,
           "gene": "LEO1",
           "score": -1.901654728,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4414,
           "gene": "DUOXA1",
           "score": -1.175281715,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4435,
           "gene": "DUSP26",
           "score": -0.354934275,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4437,
           "gene": "DUSP28",
           "score": -0.212464882,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2488,
           "gene": "CD300E",
           "score": -0.416952297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14751,
           "gene": "SMURF2",
           "score": -1.7582445430000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13234,
           "gene": "RIT1",
           "score": -0.79174172,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11535,
           "gene": "PGBD3",
           "score": -0.128372143,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14811,
           "gene": "SNX10",
           "score": -0.774897576,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2816,
           "gene": "CFC1",
           "score": -1.932787094,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9166,
           "gene": "MCIDAS",
           "score": -0.118253991,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4473,
           "gene": "DYSF",
           "score": -1.499861251,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9316,
           "gene": "MFAP3L",
           "score": -1.064490566,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17807,
           "gene": "ZDHHC5",
           "score": -1.040591794,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16800,
           "gene": "TSTA3",
           "score": -0.156054917,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12097,
           "gene": "PPID",
           "score": -0.384717194,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8133,
           "gene": "KRI1",
           "score": -1.111219665,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 9109,
+          "gene": "MATN1",
+          "score": -0.4104380999999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13984,
+          "gene": "SERPINB8",
+          "score": -0.329490148,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16328,
+          "gene": "TMOD3",
+          "score": -0.22175702600000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8629,
+          "gene": "LOC728763",
+          "score": -1.1886534709999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2744,
+          "gene": "CEP126",
+          "score": -0.156549957,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10158,
+          "gene": "NDUFS1",
+          "score": -0.5231745529999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11344,
+          "gene": "PCNXL3",
+          "score": -1.567926415,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 716,
+          "gene": "ANKRD35",
+          "score": -0.519084251,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2424,
+          "gene": "CCPG1",
+          "score": -0.461368483,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16204,
+          "gene": "TMEM220",
+          "score": -1.182195947,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 366,
+          "gene": "ADORA3",
+          "score": -1.2535028959999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3858,
+          "gene": "DCAF4L1",
+          "score": -1.23915844,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9513,
+          "gene": "MOGAT3",
+          "score": -0.702892028,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3954,
+          "gene": "DDX42",
+          "score": -1.368088589,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10418,
+          "gene": "NOP56",
+          "score": -3.12504232,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 1190,
+          "gene": "ATG4C",
+          "score": -1.294710559,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2233,
+          "gene": "CCDC124",
+          "score": -1.3287066109999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4534,
+          "gene": "EDN2",
+          "score": -0.223556442,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9098,
+          "gene": "MASP1",
+          "score": -0.966823482,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5172,
+          "gene": "FAM19A5",
+          "score": -1.176611027,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7069,
+          "gene": "HSD17B4",
+          "score": -0.9546285259999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14340,
+          "gene": "SLC24A4",
+          "score": -0.662405857,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2513,
+          "gene": "CD53",
+          "score": -1.053278716,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13666,
+          "gene": "SACM1L",
+          "score": -2.148767173,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4794,
+          "gene": "EPB42",
+          "score": -0.061137486,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 1912,
+          "gene": "C7orf73",
+          "score": -0.396462735,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1071,
+          "gene": "ARSB",
+          "score": -0.5009418520000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5777,
+          "gene": "FXYD5",
+          "score": -0.33476787399999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10738,
+          "gene": "ODF2",
+          "score": -0.469909029,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8436,
+          "gene": "LETM1",
+          "score": -0.559237908,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11941,
+          "gene": "POC1B-GALNT4",
+          "score": -0.11615138300000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10717,
+          "gene": "OAZ1",
+          "score": -0.32720166300000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3144,
+          "gene": "CMTM4",
+          "score": -0.716024876,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13775,
+          "gene": "SCHIP1",
+          "score": -1.139779623,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3010,
+          "gene": "CLCN2",
+          "score": -1.1597699479999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 704,
+          "gene": "ANKRD27",
+          "score": -0.7868462820000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10999,
+          "gene": "OS9",
+          "score": -0.23046398,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10617,
+          "gene": "NUCB2",
+          "score": -0.628037608,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12954,
+          "gene": "RBM23",
+          "score": -0.743159424,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17756,
+          "gene": "ZC3H15",
+          "score": -4.642818375,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17964,
+          "gene": "ZNF214",
+          "score": -0.434667445,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8515,
+          "gene": "LIN52",
+          "score": -3.093945923,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 2000,
+          "gene": "CACFD1",
+          "score": -0.6513169289999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16487,
+          "gene": "TP53INP2",
+          "score": -0.47062887600000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12517,
+          "gene": "PSMD9",
+          "score": -0.604428159,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7024,
+          "gene": "HPS6",
+          "score": -1.890446505,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11762,
+          "gene": "PLA2G4B",
+          "score": -0.477295927,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5235,
+          "gene": "FAM46D",
+          "score": -0.070973971,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 560,
+          "gene": "ALG13",
+          "score": -2.780068955,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 8363,
+          "gene": "LCE1B",
+          "score": -0.664128853,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16731,
+          "gene": "TSC22D1",
+          "score": -2.02432083,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14194,
+          "gene": "SIPA1L1",
+          "score": -0.8523889179999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9844,
+          "gene": "MVK",
+          "score": -0.33314050100000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7032,
+          "gene": "HRASLS5",
+          "score": -0.17696316399999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13880,
+          "gene": "SEC61B",
+          "score": -0.732267441,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12900,
+          "gene": "RASGRP3",
+          "score": -2.396689074,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12728,
+          "gene": "RAB1B",
+          "score": -0.590366287,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11107,
+          "gene": "PABPC5",
+          "score": -0.775620894,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7748,
+          "gene": "KCNH3",
+          "score": -0.504159483,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15367,
+          "gene": "SULT1A1",
+          "score": -1.1862740440000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6184,
+          "gene": "GNB2L1",
+          "score": -1.769044294,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1617,
+          "gene": "BRF1",
+          "score": -1.374109684,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16722,
+          "gene": "TRPV4",
+          "score": -0.72425143,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4376,
+          "gene": "DRP2",
+          "score": -1.152236536,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2458,
+          "gene": "CD163L1",
+          "score": -1.4734528830000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9628,
+          "gene": "MRPL37",
+          "score": -2.2005796159999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14238,
+          "gene": "SLAMF8",
+          "score": -0.646016172,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13490,
+          "gene": "RPS20",
+          "score": -1.065640001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3465,
+          "gene": "CRISP2",
+          "score": -0.481033955,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 97,
+          "gene": "ABI3",
+          "score": -0.18754147399999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12181,
+          "gene": "PPP2R5D",
+          "score": -0.370238175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9363,
+          "gene": "MIA3",
+          "score": -0.6449656570000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15293,
+          "gene": "STKLD1",
+          "score": -0.166186834,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14759,
+          "gene": "SNAI3",
+          "score": -0.774750712,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6743,
+          "gene": "HEY1",
+          "score": -2.094411689,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11073,
+          "gene": "P2RX2",
+          "score": -0.58233107,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9103,
+          "gene": "MAST4",
+          "score": -1.059639734,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8149,
+          "gene": "KRT23",
+          "score": -0.09050302199999999,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17417,
+          "gene": "VWF",
+          "score": -0.584625911,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7573,
+          "gene": "ITFG1",
+          "score": -1.19117938,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16587,
+          "gene": "TREX1",
+          "score": -0.342036268,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 923,
+          "gene": "ARGLU1",
+          "score": -3.2208133180000003,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 5010,
+          "gene": "F9",
+          "score": -0.644513575,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 756,
+          "gene": "ANO8",
+          "score": -1.947826808,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8833,
+          "gene": "LTK",
+          "score": -0.7503026909999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16109,
+          "gene": "TMEM133",
+          "score": -2.072937505,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3209,
+          "gene": "CNTN6",
+          "score": -0.812852122,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5889,
+          "gene": "GAPT",
+          "score": -0.663318773,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7213,
+          "gene": "IFIH1",
+          "score": -0.5536093000000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2121,
+          "gene": "CARD18",
+          "score": -0.6228774029999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3088,
+          "gene": "CLK1",
+          "score": -0.270706545,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2177,
+          "gene": "CBL",
+          "score": -0.204112658,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4461,
+          "gene": "DYNC2LI1",
+          "score": -0.47467650899999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13190,
+          "gene": "RHOV",
+          "score": -0.392412264,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5519,
+          "gene": "FGFR4",
+          "score": -0.593319123,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2786,
+          "gene": "CERS5",
+          "score": -0.19005876800000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15015,
+          "gene": "SPIN4",
+          "score": -0.023098108,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 13079,
+          "gene": "RETSAT",
+          "score": -1.03093522,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9330,
+          "gene": "MFSD12",
+          "score": -3.015320243,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 12853,
+          "gene": "RANBP6",
+          "score": -0.542753612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13524,
+          "gene": "RPUSD3",
+          "score": -1.2502314829999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12684,
+          "gene": "PYHIN1",
+          "score": -0.548085777,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5491,
+          "gene": "FGF11",
+          "score": -2.175442962,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17649,
+          "gene": "YEATS4",
+          "score": -1.1739566909999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1004,
+          "gene": "ARL14",
+          "score": -0.496439061,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2432,
+          "gene": "CCR7",
+          "score": -0.32461639800000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10796,
+          "gene": "OPRL1",
+          "score": -0.746379056,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13947,
+          "gene": "SEPT9",
+          "score": -0.326716425,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7872,
+          "gene": "KIAA0100",
+          "score": -0.580674799,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10804,
+          "gene": "OR10G3",
+          "score": -0.823717975,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12252,
+          "gene": "PRDM9",
+          "score": -0.669017746,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14717,
+          "gene": "SMIM24",
+          "score": -0.29737308100000004,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7260,
+          "gene": "IFT52",
+          "score": -1.4153385,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13175,
+          "gene": "RHOA",
+          "score": -2.9459395660000003,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17473,
+          "gene": "WDR48",
+          "score": -0.528011775,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18095,
+          "gene": "ZNF432",
+          "score": -1.8124296130000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 35,
+          "gene": "ABCA3",
+          "score": -0.21133955100000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13875,
+          "gene": "SEC24D",
+          "score": -0.7292541159999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1116,
+          "gene": "ASCL1",
+          "score": -0.18055578100000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15694,
+          "gene": "TCEAL2",
+          "score": -0.8765485590000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1904,
+          "gene": "C7orf60",
+          "score": -0.546959614,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7836,
+          "gene": "KDELR2",
+          "score": -0.487717731,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7710,
+          "gene": "KBTBD3",
+          "score": -1.066628225,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7589,
+          "gene": "ITGAE",
+          "score": -0.215583203,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2082,
+          "gene": "CAMTA1",
+          "score": -0.456741119,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1653,
+          "gene": "BTBD17",
+          "score": -0.126790438,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2879,
+          "gene": "CHI3L2",
+          "score": -0.885074315,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12453,
+          "gene": "PRY",
+          "score": -0.83277222,
+          "hit": 0,
+          "round": 3
         }
       ],
       "queried_history": [
@@ -4920,896 +5816,1792 @@
           "gene": "RTEL1",
           "score": -1.4855187669999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17277,
           "gene": "VAPB",
           "score": -1.2703910729999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18007,
           "gene": "ZNF280A",
           "score": -0.7558665640000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3889,
           "gene": "DCPS",
           "score": -1.195998507,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5884,
           "gene": "GANAB",
           "score": -0.63300024,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12623,
           "gene": "PTPRN",
           "score": -0.9694214790000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7497,
           "gene": "IPP",
           "score": -0.29513096,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9635,
           "gene": "MRPL43",
           "score": -0.815280817,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 963,
           "gene": "ARHGEF11",
           "score": -0.657764427,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7481,
           "gene": "INTS8",
           "score": -2.515189464,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 291,
           "gene": "ADAT2",
           "score": -0.181357057,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3338,
           "gene": "CORT",
           "score": -0.140774507,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5221,
           "gene": "FAM26E",
           "score": -1.0365657959999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17069,
           "gene": "UCN3",
           "score": -2.0068613999999996,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10080,
           "gene": "NCKAP1",
           "score": -0.614692695,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12585,
           "gene": "PTMA",
           "score": -1.038748139,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13467,
           "gene": "RPP25L",
           "score": -1.405789679,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10843,
           "gene": "OR1N2",
           "score": -0.63151199,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11912,
           "gene": "PNLIPRP1",
           "score": -0.519566309,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2447,
           "gene": "CCT7",
           "score": -0.704492129,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11266,
           "gene": "PCDH7",
           "score": -0.779044927,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9408,
           "gene": "MIR432",
           "score": -0.047927155,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5300,
           "gene": "FAM96B",
           "score": -0.890342008,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3735,
           "gene": "CYP1A1",
           "score": -0.246907181,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16980,
           "gene": "UBC",
           "score": -1.242476262,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2331,
           "gene": "CCDC77",
           "score": -1.112939553,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3151,
           "gene": "CMYA5",
           "score": -0.648189609,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8986,
           "gene": "MAN2B1",
           "score": -0.9480956159999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10490,
           "gene": "NPTX2",
           "score": -2.401567439,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3590,
           "gene": "CTC1",
           "score": -0.278952628,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9640,
           "gene": "MRPL48",
           "score": -0.373296909,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1160,
           "gene": "ATAD2",
           "score": -0.534442847,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11455,
           "gene": "PDZD4",
           "score": -1.689643157,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12833,
           "gene": "RALB",
           "score": -0.827657419,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3193,
           "gene": "CNPY3",
           "score": -0.22900884300000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15861,
           "gene": "TGFB1",
           "score": -0.323883879,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15823,
           "gene": "TEX33",
           "score": -1.320435759,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6347,
           "gene": "GPR32",
           "score": -0.491993019,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6281,
           "gene": "GPD1",
           "score": -2.039463539,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4336,
           "gene": "DPP4",
           "score": -0.6797851090000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8594,
           "gene": "LOC100506127",
           "score": -1.118812634,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8253,
           "gene": "KRTAP4-7",
           "score": -3.346861492,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1634,
           "gene": "BRSK1",
           "score": -0.236795593,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1442,
           "gene": "BCDIN3D",
           "score": -0.8460896000000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14505,
           "gene": "SLC39A6",
           "score": -0.32367678,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1255,
           "gene": "ATP5O",
           "score": -1.1252520990000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10927,
           "gene": "OR52N2",
           "score": -0.842105975,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12285,
           "gene": "PRKAG1",
           "score": -1.2557984759999998,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15651,
           "gene": "TBCC",
           "score": -1.462807671,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15079,
           "gene": "SPTAN1",
           "score": -0.28914351,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17960,
           "gene": "ZNF208",
           "score": -1.4629832409999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5017,
           "gene": "FABP3",
           "score": -0.6001938529999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7766,
           "gene": "KCNJ2",
           "score": -0.685301266,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16063,
           "gene": "TMED3",
           "score": -1.895656615,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15144,
           "gene": "SRSF3",
           "score": -1.1955252440000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11500,
           "gene": "PEX5",
           "score": -1.004241742,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1448,
           "gene": "BCL11A",
           "score": -0.608515755,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9252,
           "gene": "MEGF6",
           "score": -0.441613959,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5241,
           "gene": "FAM49A",
           "score": -0.45734107399999996,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 307,
           "gene": "ADCY9",
           "score": -0.494880649,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7429,
           "gene": "INCENP",
           "score": -0.411976677,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 482,
           "gene": "AK2",
           "score": -0.43550246600000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18048,
           "gene": "ZNF345",
           "score": -0.7923046420000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9375,
           "gene": "MICU2",
           "score": -0.48885202,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11858,
           "gene": "PLK5",
           "score": -0.285187163,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6626,
           "gene": "HAS3",
           "score": -0.366737059,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13450,
           "gene": "RPL3L",
           "score": -1.973648408,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3719,
           "gene": "CYBB",
           "score": -1.4469121919999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12001,
           "gene": "POLR3G",
           "score": -0.34459338799999994,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11310,
           "gene": "PCDHGA8",
           "score": -1.08085994,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 3747,
           "gene": "CYP2A13",
           "score": -0.7921534929999999,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 7450,
           "gene": "INPP4B",
           "score": -0.576914143,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1968,
           "gene": "C9orf85",
           "score": -0.9804685870000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14402,
           "gene": "SLC27A2",
           "score": -0.111658109,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1593,
           "gene": "BPIFB3",
           "score": -2.264809504,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15752,
           "gene": "TDG",
           "score": -0.066540241,
           "hit": 1,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1859,
           "gene": "C4A",
           "score": -0.298375674,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4999,
           "gene": "F2R",
           "score": -0.382332281,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8011,
           "gene": "KLF1",
           "score": -0.291552926,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11216,
           "gene": "PASD1",
           "score": -0.37730578200000003,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 1745,
           "gene": "C17orf67",
           "score": -1.124229479,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14929,
           "gene": "SPANXC",
           "score": -0.608521103,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16629,
           "gene": "TRIM42",
           "score": -1.022118105,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6905,
           "gene": "HMGB3",
           "score": -1.0863716190000001,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10587,
           "gene": "NT5DC3",
           "score": -0.61964227,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13503,
           "gene": "RPS4Y2",
           "score": -0.48291109299999996,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14540,
           "gene": "SLC4A5",
           "score": -2.063871355,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9162,
           "gene": "MCF2L2",
           "score": -0.420416412,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 5972,
           "gene": "GDF15",
           "score": -1.127234176,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17482,
           "gene": "WDR60",
           "score": -0.40373960299999995,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 6447,
           "gene": "GRK5",
           "score": -0.342649714,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2035,
           "gene": "CADM4",
           "score": -0.66884535,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9342,
           "gene": "MGAM",
           "score": -0.32805284,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16132,
           "gene": "TMEM156",
           "score": -1.398034435,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8780,
           "gene": "LRRFIP2",
           "score": -1.549298755,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2172,
           "gene": "CAV2",
           "score": -0.404721396,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17102,
           "gene": "UGT2B7",
           "score": -0.353900724,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11022,
           "gene": "OSR2",
           "score": -0.612890566,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18241,
           "gene": "ZNF627",
           "score": -0.315584109,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16281,
           "gene": "TMEM59",
           "score": -0.226062235,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2190,
           "gene": "CBWD2",
           "score": -1.26286739,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9502,
           "gene": "MOB3B",
           "score": -1.154290228,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16398,
           "gene": "TNFSF13",
           "score": -0.593435607,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10025,
           "gene": "NAPRT",
           "score": -0.43343086700000005,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13405,
           "gene": "RPGRIP1",
           "score": -1.242310251,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13470,
           "gene": "RPP40",
           "score": -1.092353034,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10101,
           "gene": "NCS1",
           "score": -0.167400781,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 18267,
           "gene": "ZNF671",
           "score": -1.530213681,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 15022,
           "gene": "SPINK6",
           "score": -0.235857347,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2435,
           "gene": "CCRL2",
           "score": -2.039709218,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 10607,
           "gene": "NTS",
           "score": -0.349507898,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8431,
           "gene": "LEO1",
           "score": -1.901654728,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4414,
           "gene": "DUOXA1",
           "score": -1.175281715,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4435,
           "gene": "DUSP26",
           "score": -0.354934275,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4437,
           "gene": "DUSP28",
           "score": -0.212464882,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2488,
           "gene": "CD300E",
           "score": -0.416952297,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14751,
           "gene": "SMURF2",
           "score": -1.7582445430000002,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 13234,
           "gene": "RIT1",
           "score": -0.79174172,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 11535,
           "gene": "PGBD3",
           "score": -0.128372143,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 14811,
           "gene": "SNX10",
           "score": -0.774897576,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 2816,
           "gene": "CFC1",
           "score": -1.932787094,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9166,
           "gene": "MCIDAS",
           "score": -0.118253991,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 4473,
           "gene": "DYSF",
           "score": -1.499861251,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 9316,
           "gene": "MFAP3L",
           "score": -1.064490566,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 17807,
           "gene": "ZDHHC5",
           "score": -1.040591794,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 16800,
           "gene": "TSTA3",
           "score": -0.156054917,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 12097,
           "gene": "PPID",
           "score": -0.384717194,
           "hit": 0,
-          "round": 2
+          "round": 0
         },
         {
           "candidate_index": 8133,
           "gene": "KRI1",
           "score": -1.111219665,
           "hit": 0,
-          "round": 2
+          "round": 0
+        },
+        {
+          "candidate_index": 9109,
+          "gene": "MATN1",
+          "score": -0.4104380999999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13984,
+          "gene": "SERPINB8",
+          "score": -0.329490148,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16328,
+          "gene": "TMOD3",
+          "score": -0.22175702600000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8629,
+          "gene": "LOC728763",
+          "score": -1.1886534709999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2744,
+          "gene": "CEP126",
+          "score": -0.156549957,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10158,
+          "gene": "NDUFS1",
+          "score": -0.5231745529999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11344,
+          "gene": "PCNXL3",
+          "score": -1.567926415,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 716,
+          "gene": "ANKRD35",
+          "score": -0.519084251,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2424,
+          "gene": "CCPG1",
+          "score": -0.461368483,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16204,
+          "gene": "TMEM220",
+          "score": -1.182195947,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 366,
+          "gene": "ADORA3",
+          "score": -1.2535028959999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3858,
+          "gene": "DCAF4L1",
+          "score": -1.23915844,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9513,
+          "gene": "MOGAT3",
+          "score": -0.702892028,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3954,
+          "gene": "DDX42",
+          "score": -1.368088589,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10418,
+          "gene": "NOP56",
+          "score": -3.12504232,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 1190,
+          "gene": "ATG4C",
+          "score": -1.294710559,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2233,
+          "gene": "CCDC124",
+          "score": -1.3287066109999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4534,
+          "gene": "EDN2",
+          "score": -0.223556442,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9098,
+          "gene": "MASP1",
+          "score": -0.966823482,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5172,
+          "gene": "FAM19A5",
+          "score": -1.176611027,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7069,
+          "gene": "HSD17B4",
+          "score": -0.9546285259999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14340,
+          "gene": "SLC24A4",
+          "score": -0.662405857,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2513,
+          "gene": "CD53",
+          "score": -1.053278716,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13666,
+          "gene": "SACM1L",
+          "score": -2.148767173,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4794,
+          "gene": "EPB42",
+          "score": -0.061137486,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 1912,
+          "gene": "C7orf73",
+          "score": -0.396462735,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1071,
+          "gene": "ARSB",
+          "score": -0.5009418520000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5777,
+          "gene": "FXYD5",
+          "score": -0.33476787399999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10738,
+          "gene": "ODF2",
+          "score": -0.469909029,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8436,
+          "gene": "LETM1",
+          "score": -0.559237908,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11941,
+          "gene": "POC1B-GALNT4",
+          "score": -0.11615138300000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10717,
+          "gene": "OAZ1",
+          "score": -0.32720166300000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3144,
+          "gene": "CMTM4",
+          "score": -0.716024876,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13775,
+          "gene": "SCHIP1",
+          "score": -1.139779623,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3010,
+          "gene": "CLCN2",
+          "score": -1.1597699479999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 704,
+          "gene": "ANKRD27",
+          "score": -0.7868462820000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10999,
+          "gene": "OS9",
+          "score": -0.23046398,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10617,
+          "gene": "NUCB2",
+          "score": -0.628037608,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12954,
+          "gene": "RBM23",
+          "score": -0.743159424,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17756,
+          "gene": "ZC3H15",
+          "score": -4.642818375,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17964,
+          "gene": "ZNF214",
+          "score": -0.434667445,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8515,
+          "gene": "LIN52",
+          "score": -3.093945923,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 2000,
+          "gene": "CACFD1",
+          "score": -0.6513169289999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16487,
+          "gene": "TP53INP2",
+          "score": -0.47062887600000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12517,
+          "gene": "PSMD9",
+          "score": -0.604428159,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7024,
+          "gene": "HPS6",
+          "score": -1.890446505,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11762,
+          "gene": "PLA2G4B",
+          "score": -0.477295927,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5235,
+          "gene": "FAM46D",
+          "score": -0.070973971,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 560,
+          "gene": "ALG13",
+          "score": -2.780068955,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 8363,
+          "gene": "LCE1B",
+          "score": -0.664128853,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16731,
+          "gene": "TSC22D1",
+          "score": -2.02432083,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14194,
+          "gene": "SIPA1L1",
+          "score": -0.8523889179999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9844,
+          "gene": "MVK",
+          "score": -0.33314050100000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7032,
+          "gene": "HRASLS5",
+          "score": -0.17696316399999998,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13880,
+          "gene": "SEC61B",
+          "score": -0.732267441,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12900,
+          "gene": "RASGRP3",
+          "score": -2.396689074,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12728,
+          "gene": "RAB1B",
+          "score": -0.590366287,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11107,
+          "gene": "PABPC5",
+          "score": -0.775620894,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7748,
+          "gene": "KCNH3",
+          "score": -0.504159483,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15367,
+          "gene": "SULT1A1",
+          "score": -1.1862740440000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6184,
+          "gene": "GNB2L1",
+          "score": -1.769044294,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1617,
+          "gene": "BRF1",
+          "score": -1.374109684,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16722,
+          "gene": "TRPV4",
+          "score": -0.72425143,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4376,
+          "gene": "DRP2",
+          "score": -1.152236536,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2458,
+          "gene": "CD163L1",
+          "score": -1.4734528830000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9628,
+          "gene": "MRPL37",
+          "score": -2.2005796159999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14238,
+          "gene": "SLAMF8",
+          "score": -0.646016172,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13490,
+          "gene": "RPS20",
+          "score": -1.065640001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3465,
+          "gene": "CRISP2",
+          "score": -0.481033955,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 97,
+          "gene": "ABI3",
+          "score": -0.18754147399999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12181,
+          "gene": "PPP2R5D",
+          "score": -0.370238175,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9363,
+          "gene": "MIA3",
+          "score": -0.6449656570000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15293,
+          "gene": "STKLD1",
+          "score": -0.166186834,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14759,
+          "gene": "SNAI3",
+          "score": -0.774750712,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 6743,
+          "gene": "HEY1",
+          "score": -2.094411689,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 11073,
+          "gene": "P2RX2",
+          "score": -0.58233107,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9103,
+          "gene": "MAST4",
+          "score": -1.059639734,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8149,
+          "gene": "KRT23",
+          "score": -0.09050302199999999,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17417,
+          "gene": "VWF",
+          "score": -0.584625911,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7573,
+          "gene": "ITFG1",
+          "score": -1.19117938,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16587,
+          "gene": "TREX1",
+          "score": -0.342036268,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 923,
+          "gene": "ARGLU1",
+          "score": -3.2208133180000003,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 5010,
+          "gene": "F9",
+          "score": -0.644513575,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 756,
+          "gene": "ANO8",
+          "score": -1.947826808,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 8833,
+          "gene": "LTK",
+          "score": -0.7503026909999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 16109,
+          "gene": "TMEM133",
+          "score": -2.072937505,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3209,
+          "gene": "CNTN6",
+          "score": -0.812852122,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5889,
+          "gene": "GAPT",
+          "score": -0.663318773,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7213,
+          "gene": "IFIH1",
+          "score": -0.5536093000000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2121,
+          "gene": "CARD18",
+          "score": -0.6228774029999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 3088,
+          "gene": "CLK1",
+          "score": -0.270706545,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2177,
+          "gene": "CBL",
+          "score": -0.204112658,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 4461,
+          "gene": "DYNC2LI1",
+          "score": -0.47467650899999997,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13190,
+          "gene": "RHOV",
+          "score": -0.392412264,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5519,
+          "gene": "FGFR4",
+          "score": -0.593319123,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2786,
+          "gene": "CERS5",
+          "score": -0.19005876800000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15015,
+          "gene": "SPIN4",
+          "score": -0.023098108,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 13079,
+          "gene": "RETSAT",
+          "score": -1.03093522,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 9330,
+          "gene": "MFSD12",
+          "score": -3.015320243,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 12853,
+          "gene": "RANBP6",
+          "score": -0.542753612,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13524,
+          "gene": "RPUSD3",
+          "score": -1.2502314829999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12684,
+          "gene": "PYHIN1",
+          "score": -0.548085777,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 5491,
+          "gene": "FGF11",
+          "score": -2.175442962,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 17649,
+          "gene": "YEATS4",
+          "score": -1.1739566909999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1004,
+          "gene": "ARL14",
+          "score": -0.496439061,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2432,
+          "gene": "CCR7",
+          "score": -0.32461639800000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10796,
+          "gene": "OPRL1",
+          "score": -0.746379056,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13947,
+          "gene": "SEPT9",
+          "score": -0.326716425,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7872,
+          "gene": "KIAA0100",
+          "score": -0.580674799,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 10804,
+          "gene": "OR10G3",
+          "score": -0.823717975,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12252,
+          "gene": "PRDM9",
+          "score": -0.669017746,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 14717,
+          "gene": "SMIM24",
+          "score": -0.29737308100000004,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7260,
+          "gene": "IFT52",
+          "score": -1.4153385,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13175,
+          "gene": "RHOA",
+          "score": -2.9459395660000003,
+          "hit": 1,
+          "round": 3
+        },
+        {
+          "candidate_index": 17473,
+          "gene": "WDR48",
+          "score": -0.528011775,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 18095,
+          "gene": "ZNF432",
+          "score": -1.8124296130000002,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 35,
+          "gene": "ABCA3",
+          "score": -0.21133955100000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 13875,
+          "gene": "SEC24D",
+          "score": -0.7292541159999999,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1116,
+          "gene": "ASCL1",
+          "score": -0.18055578100000003,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 15694,
+          "gene": "TCEAL2",
+          "score": -0.8765485590000001,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1904,
+          "gene": "C7orf60",
+          "score": -0.546959614,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7836,
+          "gene": "KDELR2",
+          "score": -0.487717731,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7710,
+          "gene": "KBTBD3",
+          "score": -1.066628225,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 7589,
+          "gene": "ITGAE",
+          "score": -0.215583203,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2082,
+          "gene": "CAMTA1",
+          "score": -0.456741119,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 1653,
+          "gene": "BTBD17",
+          "score": -0.126790438,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 2879,
+          "gene": "CHI3L2",
+          "score": -0.885074315,
+          "hit": 0,
+          "round": 3
+        },
+        {
+          "candidate_index": 12453,
+          "gene": "PRY",
+          "score": -0.83277222,
+          "hit": 0,
+          "round": 3
         }
       ]
     }

```
