## Project-4 是什么任务（Active Search）

这是一个“主动搜索（Active Search）”科学任务：在一个固定候选池（5000 条分子/抗体候选）里，用尽量少的查询找到尽量多的“好分子”（Top 1000）。

- 数据：大 CSV（每行一个候选分子/结构/序列等字段）
- 黑盒打分：`y = compute_x(row)`（见 [index.py](./index.py)）
- 真实标签（只用于评测，policy 不可见）：
  - 按 y 排序取 Top `top_ratio=0.2`（约 20%）→ `label=1`
  - 其余 → `label=0`
- 每轮行为：policy 从 5000 个候选中选 `batch_size=100` 个“没选过的”样本，oracle 揭示 label，history 增量更新
- 目标指标：在固定查询预算内最大化 `total_hits`（累计命中数），并输出 hit curve / Precision@100 / Recall / AUC（可选）

进化的对象仍然是 `hoss-evolution/best/current/harness/` 下的 harness 代码，核心是一个 [model.py](./hoss-evolution/best/current/harness/model.py)，但在 Project-4 中：

- `model.py` 不再是预测器
- 而是一个 **selection policy（选择策略）**

---

## Policy 接口（必须遵守）

`harness/model.py` 需要提供如下接口之一：

1) 模块级函数

```python
def select(candidates, history, batch_size, seed) -> list[int]:
    ...
```

2) 或一个带 `select(...)` 方法的类（类名可以是 `SelectionPolicy / Policy / Model`）

其中：
- `candidates`：list[dict]，长度为 5000，每个 dict 是一行（列名 -> 值）
- `history`：list[dict]，已查询的行；每行除原始字段外，还包含：
  - `candidate_index`：int（在 candidates 里的行号）
  - `label`：int（0/1）
- `batch_size`：本轮要选多少条（默认 100）
- `seed`：本轮随机种子（每轮变化）

注意：
- 不允许重复选；返回重复/已选 index 会被自动过滤并用随机补齐
- policy 不能调用 `compute_x` 或访问真实标签

---

## hoss-evolution 目录里会出现哪些文件

`project/project-4/hoss-evolution/` 是进化工作区，结构与 project-2 类似：

- `best/current/harness/model.py`
  - 当前最好 policy（默认每轮候选从这里复制一份作为起点；EXPLORE/RESTART 且设置 `EVOLVER_INITIAL_HARNESS_DIR` 时，从初始目录复制）
- `candidates/candidate_<N>/harness/outputs/metrics.json`
  - 本轮 active search 的指标（total_hits、hit_curve 等）
- `candidates/candidate_<N>/eval_scores.json`
  - 标准化评测分数（`final_score` 等，用于 best 更新）
- `candidates/candidate_<N>/traces/harness_run.log`
  - 每轮 harness 运行日志

---

## 主流程（白话版）

链路如下：  
`run_evolution.sh → harness_run_script.sh → main_fix_train_test_input_output.py → evaluate.py`

### 1) harness_run_script.sh：跑一轮 Active Search（给某个 candidate 打分）

文件：[harness_run_script.sh](./harness_run_script.sh)

可配置环境变量：
- `PROJECT4_TASK`：任务名（默认 `IL2`），用于从 `BioDiscoveryAgent/datasets` 自动选择数据
- `PROJECT4_DATASETS_DIR`：`BioDiscoveryAgent/datasets` 目录（默认自动定位到仓库内路径）
- `PROJECT4_DATA_CSV`：输入 CSV 路径（若不设置，则默认使用 `$PROJECT4_DATASETS_DIR/ground_truth_${PROJECT4_TASK}.csv`）
  - 可以是“任务 ground truth CSV”（例如 `ground_truth_IL2.csv`，通常包含 `Gene,Score`）
  - 也可以是大 CSV（每次按 seed 采样 5000 条）或“预生成候选池文件”（见下面 `compute_x_generate_fix_train_test.py`）
- `PROJECT4_FIXED_POOL`：=1 时强制把 `PROJECT4_DATA_CSV` 当作“固定候选池”（不再二次采样）
  - 典型场景：`PROJECT4_DATA_CSV` 指向 `compute_x_generate_fix_train_test.py` 预生成的 `candidate_pool_*.csv`（例如 `candidate_pool_labeled_*.csv`）
- `PROJECT4_POOL_SIZE`：候选池大小（默认 5000；仅在输入是大 CSV 且未 fixed_pool 时生效）
- `PROJECT4_TOP_RATIO`：好分子比例（默认 0.2；仅在输入 CSV 不含 label 且未提供 ground_truth 时生效）
- `PROJECT4_BATCH_SIZE`：每轮查询数（默认 100）
- `PROJECT4_ROUNDS`：本次运行执行的轮数（默认 1）
- `PROJECT4_SEED`：采样与随机种子（默认 42）
- `PROJECT4_SEED_QUERIES`：可选的初始随机 seed queries（默认 0；仅在第一次运行且历史为空时生效）
- `PROJECT4_RESUME_STATE`：是否从 state 断点续跑（默认 1）
- `PROJECT4_STATE_PATH`：自定义 state 文件路径（默认空；空则写到 `harness/outputs/active_search_state.json`）
- `PROJECT4_GROUND_TRUTH_CSV`：可选的 ground truth CSV（candidate_index,label）；如果输入 CSV 自带 `label` 列则不需要
  - 仅当输入 CSV 不含 `label` 且你不想用 `compute_x + top_ratio` 在运行时现场生成标签时才需要

### 2) main_fix_train_test_input_output.py：执行 Active Search 并写 metrics.json

文件：[main_fix_train_test_input_output.py](./main_fix_train_test_input_output.py)

它会：
- 读入候选池：
  - 输入是大 CSV：按 seed 采样 5000 条
  - 输入是候选池 CSV：直接使用（可配合 `--fixed_pool` / 文件名前缀自动识别）
- 读入 ground truth label：
  - 若输入 CSV 自带 `label` 列：直接使用，并在传给 policy 前剥离 `label`（policy 看不到）
  - 否则：使用 `compute_x` 计算 y 并构造 top-k 标签（评测内部使用），或从 `--ground_truth_csv` 读取
- 多轮调用 `harness/model.py` 的 `select(...)` 选择未选过的样本
- oracle 揭示 label，更新 history，并记录每轮命中与累计命中
- 写出 `harness/outputs/metrics.json`
- 断点续跑：默认会读写 `harness/outputs/active_search_state.json`，跨多次运行累积历史并保证不重复选

### 3) evaluate.py：把 metrics.json 翻译成最终分数

文件：[evaluate.py](./evaluate.py)

它读取 `test.total_hits` 与 `test.top_k`，并输出：
- `final_score = clamp(total_hits / top_k, 0, 1) * 100`

---

## 最小可运行方式（不进化，只跑一次）

```bash
PROJECT4_TASK=IL2 \
PROJECT4_POOL_SIZE=5000 \
PROJECT4_TOP_RATIO=0.2 \
PROJECT4_BATCH_SIZE=100 \
PROJECT4_ROUNDS=1 \
PROJECT4_SEED=42 \
bash project/project-4/harness_run_script.sh project/project-4/hoss-evolution/best/current
```

或直接跑主脚本：

```bash
python project/project-4/main_fix_train_test_input_output.py \
  --csv /path/to/merged_results.csv \
  --model_dir project/project-4/hoss-evolution/best/current/harness/model.py \
  --pool_size 5000 \
  --top_ratio 0.2 \
  --batch_size 100 \
  --rounds 1 \
  --seed 42
```

---

## 推荐：先预生成“带 label 的候选池文件”（单文件）

文件：[compute_x_generate_fix_train_test.py](./compute_x_generate_fix_train_test.py)

它会从大 CSV 采样 5000 条，并把 `label`（top-1000）直接写回同一个 CSV 文件：

```bash
python project/project-4/compute_x_generate_fix_train_test.py \
  --csv /path/to/merged_results.csv \
  --pool_size 5000 \
  --top_ratio 0.2 \
  --seed 42 \
  --out /path/to/out_dir
```

输出文件示例：
- `candidate_pool_labeled_all_top0p2_n5000_seed42.csv`（包含原始列 + `label` 列）

然后用这个文件跑 active search（不需要 `PROJECT4_GROUND_TRUTH_CSV`）：

```bash
PROJECT4_DATA_CSV=/path/to/out_dir/candidate_pool_labeled_all_top0p2_n5000_seed42.csv \
PROJECT4_FIXED_POOL=1 \
PROJECT4_ROUNDS=1 \
PROJECT4_RESUME_STATE=1 \
bash project/project-4/harness_run_script.sh project/project-4/hoss-evolution/best/current
```
