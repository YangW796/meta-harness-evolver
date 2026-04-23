# Active Search（统一版）

`project/active-search/` 是统一的 Active Search 任务实现与运行入口。给定一个候选池 CSV（通常 5000 行），selection policy（`harness/model.py`）每轮选择一批未查询候选，oracle 揭示 label，累积命中并输出可用于进化日志的指标与状态文件。

这个目录整合了此前 `project-3 / project-4` 的共性逻辑，目标是：**只需要知道 CSV 路径**（以及可选的标签生成方式），即可灵活跑不同输入格式的数据。

---

## 目录与入口

- 运行 Active Search 主程序：[active_search.py](./project/active-search/active_search.py)
- 评测脚本（供 evolver 写入 evolution_log.jsonl）：[evaluate.py](./project/active-search/evaluate.py)
- evolver 运行入口（单任务）：[run_evolution.sh](./project/active-search/run_evolution.sh)
- evolver 运行入口（扫全任务）：[run_evolution_all_tasks.sh](./project/active-search/run_evolution_all_tasks.sh)
- harness 执行脚本（evolver 调用）：[harness_run_script.sh](./project/active-search/harness_run_script.sh)
- 手工生成 Score+label 的候选池数据（带难度）：[manual_score_data_generation.py](./project/active-search/manual_score_data_generation.py)
- proposer prompt 前缀（统一）：[proposer_prompt_prefix.txt](./project/active-search/proposer_prompt_prefix.txt)

---

## Policy 接口（必须遵守）

你的 harness 代码位于候选目录的：

`<candidate_dir>/harness/model.py`

需要提供如下接口之一：

1) 模块级函数：

`select(candidates, history, batch_size, seed) -> list[int]`

2) 或一个带 `select(...)` 方法的类（类名可为 `SelectionPolicy / Policy / Model`）。

输入语义：

- `candidates`：候选池 row dict 列表（不含 label；可能会剥离 score 列，避免 policy “偷看”）
- `history`：已查询样本 row dict 列表，每条包含原始字段 + `candidate_index` + `label`

---

## 数据输入与标签来源（灵活）

运行时只要求 `--csv` 指向一个 CSV（大表或已固定候选池都可）。label 的生成/加载按优先级自动选择：

1) CSV 自带 `label` 列：直接使用（传给 policy 前会剥离 label）
2) `--ground_truth_csv`：提供 `candidate_index,label`
3) 与 CSV 同目录的 `topmovers_<TASK>.npy` + CSV 含 `Gene` 列：`Gene` 在 topmovers 中则 label=1
4) 数值列（默认列名 `Score`，可用 `--score_column` 改名）：按 `top_ratio` 取 `abs(Score)` Top-k 为 label=1
5) `--compute_x_py /path/to/compute_x.py`：该文件需提供 `compute_x(pool_rows)->scores`，内部据 `top_ratio` 取 Top-k 为 label=1（policy 不可调用它）

---

## 输出（metrics.json / state / evolution log）

运行结束会写：

- `harness/outputs/metrics.json`：包含 `metrics.test.*`
- `ACTIVE_SEARCH_STATE_PATH` 指定的 state json：用于断点续跑

关键字段（`metrics.test`）：

- `total_hits / total_queries / top_k / delta_hits / delta_queries / auc_normalized`
- `ncg / ncg_k / ncg_selected_sum / ncg_topk_sum`
- `queried_records`：`[{candidate_index,label}, ...]`
- `queried_history`：每条历史包含该候选的原始字段 + `candidate_index,label`（用于复盘“选了什么”）

`evaluate.py` 会把这些字段（尤其 `total_hits`、`ncg` 等）带入 `scenario_scores`，随后由 evolver 写进 `evolution_log.jsonl` 的每一条记录里。

---

## 运行方式

### 1) 直接跑一次 Active Search（不进化）

```bash
python project/active-search/active_search.py \
  --csv /path/to/data.csv \
  --model_dir /path/to/candidate_dir/harness/model.py \
  --pool_size 5000 \
  --top_ratio 0.2 \
  --batch_size 100 \
  --rounds 1 \
  --seed 42
```

如果需要 `compute_x` 来生成标签：

```bash
python project/active-search/active_search.py \
  --csv /path/to/data.csv \
  --model_dir /path/to/candidate_dir/harness/model.py \
  --top_ratio 0.2 \
  --compute_x_py /path/to/compute_x_impl.py
```

### 2) 跑 evolver（单任务）

`run_evolution.sh` 会自动：

- 生成/选择 workspace：`hoss-evolution_${RUN_TAG}_${TASK}`
- 准备 baseline model 到 `<workspace>/best/current/harness/model.py`
- 通过 `harness_run_script.sh` 执行 Active Search
- 调用 `evaluate.py` 输出标准 JSON，写入 `evolution_log.jsonl`

```bash
TASK=IL2 bash project/active-search/run_evolution.sh
```

常用参数（环境变量）：

- `ITERATIONS`：进化迭代次数（默认 20）
- `RUN_TAG`：运行 tag（默认 evo）
- `WORKSPACE_ROOT`：workspace 根目录（默认 active-search 目录）
- `ACTIVE_SEARCH_DATA_CSV`：数据 CSV 路径（不设则用 datasets 下 `ground_truth_${TASK}.csv`）
- `ACTIVE_SEARCH_DATASETS_DIR`：datasets 目录（默认仓库内 `BioDiscoveryAgent/datasets`）

### 3) 跑 evolver（扫全任务）

自动扫描 `ACTIVE_SEARCH_DATASETS_DIR` 下 `ground_truth_*.csv`：

```bash
bash project/active-search/run_evolution_all_tasks.sh
```

---

## 生成可控难度的 Score+label 数据（可选）

当你的 CSV 没有 `label/Score/topmovers`，又不想依赖项目内的 `compute_x`，可以用：

```bash
python project/active-search/manual_score_data_generation.py \
  --csv /path/to/merged_results.csv \
  --pool_size 5000 \
  --top_ratio 0.2 \
  --difficulty 1 \
  --out /path/to/out_dir
```

`--difficulty`：

- 1：线性
- 2：非线性
- 3：高度非线性

输出 CSV 会新增：

- `Score`（或 `--score_column` 指定列名）
- `label`
- 可选 `split`（若开启 `--split_train_test`）

