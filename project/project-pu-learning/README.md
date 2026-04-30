# Project PU Learning

This project is a Positive-Unlabeled (PU) version of `project-3`.

The execution shape is the same Active Search loop:

- A policy receives a fixed candidate pool.
- Each round it selects new candidate indices.
- An oracle reveals labels only for selected candidates.
- The goal is to discover as many known positives as possible under the query budget.

The difference is label construction. Instead of computing hidden labels with `compute_x`, this project builds labels by matching the candidate pool against a user-provided positive CSV.

## Policy Interface

`harness/model.py` must provide:

```python
def select(candidates, history, batch_size, seed) -> list[int]:
    ...
```

Where:

- `candidates`: list of row dicts. It never includes the full hidden label column.
- `history`: queried rows only, each with `candidate_index` and oracle-revealed `label`.
- `label=1`: the queried candidate matched the positive set.
- `label=0`: the queried candidate did not match the positive set. In PU learning this is an unlabeled miss/noisy negative, not a guaranteed true negative.

## Required Data

Set a candidate CSV:

```bash
PROJECT_PU_DATA_CSV=/path/to/candidates.csv
```

Set a positive CSV unless the candidate CSV already has an inline `label` column:

```bash
PROJECT_PU_POSITIVE_CSV=/path/to/positives.csv
```

Recommended: provide a stable matching key:

```bash
PROJECT_PU_ID_COLUMN=sequence_id
```

Or multiple matching columns:

```bash
PROJECT_PU_MATCH_COLUMNS=sequence,chain_id
```

If neither is provided, the runner tries common ID columns (`id`, `ID`, `candidate_id`, `sequence_id`, `name`) and then falls back to all common columns.

## Run One Harness Evaluation

```bash
PROJECT_PU_DATA_CSV=/path/to/candidates.csv \
PROJECT_PU_POSITIVE_CSV=/path/to/positives.csv \
PROJECT_PU_ID_COLUMN=sequence_id \
PROJECT_PU_POOL_SIZE=5000 \
PROJECT_PU_BATCH_SIZE=100 \
PROJECT_PU_ROUNDS=1 \
PROJECT_PU_SEED=42 \
bash project/project-pu-learning/harness_run_script.sh project/project-pu-learning/hoss-evolution/best/current
```

Or call Python directly for debugging. Prefer passing the positive CSV through the environment so it can be scrubbed before `model.py` is imported:

```bash
PROJECT_PU_POSITIVE_CSV=/path/to/positives.csv \
python project/project-pu-learning/main_fix_train_test_input_output.py \
  --csv /path/to/candidates.csv \
  --id_column sequence_id \
  --model_dir project/project-pu-learning/hoss-evolution/best/current/harness/model.py \
  --pool_size 5000 \
  --batch_size 100 \
  --rounds 1 \
  --seed 42
```

## Prepare A Fixed Pool

For reproducible evolution runs, pre-generate a fixed labeled pool:

```bash
python project/project-pu-learning/prepare_candidate_pool.py \
  --csv /path/to/candidates.csv \
  --positive_csv /path/to/positives.csv \
  --id_column sequence_id \
  --pool_size 5000 \
  --seed 42 \
  --out /path/to/out_dir
```

Then run with:

```bash
PROJECT_PU_DATA_CSV=/path/to/out_dir/candidate_pool_pu_labeled_n5000_seed42.csv \
PROJECT_PU_FIXED_POOL=1 \
bash project/project-pu-learning/harness_run_script.sh project/project-pu-learning/hoss-evolution/best/current
```

## Metrics

The runner writes `harness/outputs/metrics.json`.

Important fields:

- `top_k`: positives present in the candidate pool.
- `positive_in_pool`: same count from PU matching diagnostics.
- `total_hits`: cumulative positives discovered.
- `delta_hits`: positives discovered in this run.
- `delta_precision`: emitted by `evaluate.py` as the final score basis.
- `match_mode` and `match_columns`: how positives were matched.

State is saved to `harness/outputs/active_search_state.json` by default so repeated one-round runs continue the same search.

## Evolution

```bash
PROJECT_PU_DATA_CSV=/path/to/candidates.csv \
PROJECT_PU_POSITIVE_CSV=/path/to/positives.csv \
PROJECT_PU_ID_COLUMN=sequence_id \
bash project/project-pu-learning/run_evolution.sh
```

Only `harness/model.py` should be changed by proposer candidates.
