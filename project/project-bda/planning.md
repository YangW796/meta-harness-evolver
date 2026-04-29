# Project-BDA Planning (Meta-Harness Evolver)

## Goal

Build a Meta-Harness Evolver project (`project-bda`) to compare against BioDiscoveryAgent on the same task + data:

- Task: `perturb-genes-brief`
- Dataset: `IFNG`
- Settings: `steps=5`, `num_genes=128`
- Optional tool: `gene_search=True` using Achilles features (`achilles.csv`)

Run the same closed-loop experimental design (choose genes in rounds, observe outcomes, choose next) but within the evolver runner so we can:

- Evaluate each candidate in a standardized way
- Record all decisions + outcomes as JSON artifacts
- Evolve only the strategy surface (policy) while keeping the runner stable

## Key Constraints

1. Do NOT use `.npy` for “selected genes” output. Record selection history in JSON (Project-3 style).
2. Strategy surface must mimic Project-3: evolve only `hoss-evolution/best/current/harness/model.py` (copied into each candidate), with a stable runner around it.
3. Design `gene_search` behavior explicitly (fair vs BioDiscoveryAgent, reproducible, no label leakage).

## Repository Layout (Target)

`meta-harness-evolver/project/project-bda/`

- `run_evolution.sh`
- `harness_run_script.sh`
- `evaluate.py`
- `proposer_prompt_prefix.txt` (optional, for NexAU prompt grounding)
- `hoss-evolution/`
  - `best/current/harness/model.py`  (baseline policy; evolvable surface)
  - `candidates/candidate_N/harness/model.py`
  - `candidates/candidate_N/harness/outputs/metrics.json`
  - `candidates/candidate_N/harness/outputs/bda_state.json` (resume state)

## Strategy Surface (Evolvable) — model.py

Follow Project-3’s selection-policy contract:

- Provide either:
  - `select(candidates, history, batch_size, seed) -> list[int]`, or
  - a class `SelectionPolicy` / `Policy` / `Model` exposing `.select(...)`.

Inputs semantics for BDA:

- `candidates`: list[dict] over the gene pool; each entry minimally includes:
  - `gene` (HGNC symbol)
  - optionally `candidate_index` (otherwise index in list is used)
- `history`: list[dict] containing already “queried” genes, each with:
  - `candidate_index`
  - `gene`
  - `score` (observed from ground truth)
  - optional `hit` (if we decide to show it; see “Fairness Boundary”)
- `batch_size`: typically 128
- `seed`: varies per round; used for reproducible exploration / tie-breaking

Runner must sanitize outputs exactly like Project-3:

- Filter invalid indices / duplicates / already-selected
- If < `batch_size`, fill remaining with random unseen indices (seeded)

## Outputs (No NPY) — metrics.json + state.json

Record everything in JSON, similar to Project-3:

### `harness/outputs/metrics.json`

`{"metrics": {"test": {...}}}` where `test` includes:

- `pool_size`
- `rounds` / `executed_rounds`
- `batch_size`
- `seed`
- `total_queries`
- `total_hits`
- `hit_curve`: `{ "queries": [...], "hits": [...] }`
- `round_details`: per-round breakdown (selected genes, hits, etc.)
- `queried_records`: compact, resume-friendly records, e.g.
  - `{ "candidate_index": int, "gene": str, "score": float, "hit": int, "round": int }`
- `queried_history`: readable rows (may be truncated fields if needed)

### `harness/outputs/bda_state.json`

Resume-only state, similar to `active_search_state.json` in Project-3:

- `completed_rounds`
- `queried_records` (the compact list)
- `total_queries`, `total_hits`
- (optional) `pool_size`, `batch_size`, `seed` for sanity checks

## Data / “Oracle” (Ground Truth)

To match BioDiscoveryAgent:

- Use `BioDiscoveryAgent/datasets/ground_truth_IFNG.csv` as the oracle score table.
- Optional “hits” definition:
  - If `topmovers_IFNG.npy` exists, it defines a “hit set” (BioDiscoveryAgent uses it in analysis).
  - Otherwise, define hits by a percentile threshold (e.g., top 10%) derived from ground-truth scores.

The policy must never read ground truth directly; only the runner uses it to reveal outcomes for queried genes.

## Multi-Dataset Workspaces (workspace-index)

Goal: each dataset under `BioDiscoveryAgent/datasets/` maps to a distinct evolver workspace index so we can:

- run a single dataset (e.g. `IFNG`) or
- run `all` datasets in a batch
- keep results isolated per dataset (separate `best/current`, candidates, and `evolution_log.jsonl`)

### Dataset Sources

Datasets are defined by the intersection of:

- task prompt: `BioDiscoveryAgent/datasets/task_prompts/<DATA>.json`
- oracle table: `BioDiscoveryAgent/datasets/ground_truth_<DATA>.csv`
- optional hit set: `BioDiscoveryAgent/datasets/topmovers_<DATA>.npy`

Examples observed in the repo:

- IFNG, IL2, Carnevale22_Adenosine, Horlbeck, Sanchez21, Sanchez21_down, Scharenberg22, Steinhart_crispra_GD2_D22

### Workspace Indexing Convention

Define a stable mapping from `<DATA>` to a workspace directory, e.g.:

- `project-bda/hoss-evolution/workspaces/<DATA>/`
  - contains `best/current/`, `candidates/`, and `evolution_log.jsonl`

The evolver entry script should accept:

- `--data_name <DATA>` to select one dataset, or
- `--data_name all` to iterate over all datasets that have both `task_prompts/<DATA>.json` and `ground_truth_<DATA>.csv`.

### Run Semantics for `all`

For `all`, you still run only one top-level command/script once.
That single run iterates over datasets internally, and for each dataset writes to its own workspace:

- isolated workspace per dataset
- identical hyperparameters (steps/batch_size/seed policy) unless explicitly overridden
- aggregate summary can be printed to stdout, but per-dataset truth is always in each workspace’s `evolution_log.jsonl`.

## Evaluation (final_score)

`evaluate.py` reads `metrics.json` and outputs JSON on stdout last line, including:

- `final_score`: single scalar for evolver best-update
- also include raw metrics for analysis (e.g., `total_hits`, `ncg`, `auc_normalized`)

To align with BioDiscoveryAgent’s `analyze.py`:

- compute `cumulative_hits`
- compute `ncg` (normalized cumulative gain)
- recommended: `final_score = ncg * 100` (and store both `ncg` and `cumulative_hits`)

## gene_search Design

Objective: replicate BioDiscoveryAgent’s “Gene Search tool” effect but within the policy framework.

### Tool semantics (must be stable across candidates unless intentionally evolved)

- Input: `query_gene`
- Output: `k` genes either:
  - `similar` (top-k by cosine similarity in Achilles feature space), or
  - `dissimilar/diverse` (bottom-k or novelty-biased selection)

### Data source / caching

- Use `achilles.csv` under a configured directory, e.g. `BDA_CSV_PATH`.
- Prefer runner-side preparation/caching to avoid large downloads during evaluation.

### Usage protocol (baseline policy)

- Each round chooses an anchor gene:
  - If history non-empty: pick a high-score gene from history (e.g., top-1 or top-m).
  - Cold start: pick a seeded random gene.
- Query `gene_search(anchor, k=10, mode="similar")` to expand candidates.
- Selection combines:
  - exploit from gene_search results (unseen first)
  - explore by random fill for remaining slots
- Optional: switch to `dissimilar` when hit-curve stalls.

## Fairness Boundary

For a fair comparison to BioDiscoveryAgent:

- Policy can only access what BioDiscoveryAgent effectively sees:
  - Previously queried genes and their measured scores.
- No peeking into unqueried ground truth scores/labels.
- If we include `hit` in history:
  - It should be derived from the same hit definition used in evaluation, and documented.

## Integration with Meta-Harness Evolver

Workflow matches existing projects:

`run_evolution.sh → harness_run_script.sh → (BDA runner main) → evaluate.py`

The evolver then:

- writes `candidate_N/eval_scores.json`
- computes `candidate_N/change_record.*`
- appends to `<workspace>/evolution_log.jsonl`
