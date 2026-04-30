# Project PU Learning 实现规划

## 目标

在 `meta-harness-evolver/project/project-3` 的 Active Search 框架基础上，实现一个同样面向固定候选池、有限查询预算、演化 selection policy 的任务版本，但标签来源改为 **Positive-Unlabeled learning (PU learning)**：

- 用户提供一个正例 CSV 路径，记为 `positive_csv`。
- 搜索候选池来自一个大 CSV 或预生成 candidate pool，记为 `unlabeled_csv` / `candidate_pool_csv`。
- 评测时只有能和 `positive_csv` 匹配上的候选视为 `label=1`，其余候选为 unlabeled / unknown，在 oracle 反馈和指标里按 `label=0` 处理。
- policy 不可见完整正例集合，只能看到已查询样本被 oracle 揭示后的 `label`。
- 演化目标仍然是：在预算内尽量多地从候选池中找到正例。

这不是普通二分类：未命中的样本不是可靠负例，而是“未标注”。因此默认策略、prompt 和文档都要明确禁止把 U 集合当作干净负类。

## 与 Project-3 的主要差异

Project-3 当前逻辑：

- 通过 `compute_x(row)` 对候选池排序。
- 取 Top `top_ratio` 作为隐藏正例。
- `top_k = pool_size * top_ratio`。
- proposer 被提示不能读 `index.py` / `compute_x`。

PU 版本应改为：

- 删除对 `compute_x` 的运行时依赖，评测标签由 `positive_csv` 和候选池匹配得到。
- `top_k = 候选池中可匹配到的 positive 数量`。
- `PROJECT_PU_POSITIVE_CSV` 是必需配置，除非输入候选池已包含评测用 `label` 列。
- 不再暴露/强调 `top_ratio`，因为正例比例由 positive CSV 与候选池交集决定。
- prompt 中强调 PU 约束：`history.label=0` 只代表“查询后未命中 positive set”，不代表化学/生物学意义上的真负例。

## 建议目录结构

从 `project-3` 复制并改名保留相同执行链路：

```text
meta-harness-evolver/project/project-pu-learning/
  README.md
  evaluate.py
  harness_run_script.sh
  main_fix_train_test_input_output.py
  prepare_candidate_pool.py
  proposer_prompt_prefix.txt
  run_evolution.sh
  hoss-evolution/best/current/harness/model.py
```

文件职责：

- `main_fix_train_test_input_output.py`：PU active search 主逻辑，替换 Project-3 的 label 构造部分。
- `prepare_candidate_pool.py`：可选的候选池预生成工具，负责采样固定 pool，并可把 `label` 列写入离线 pool 方便复现实验。
- `evaluate.py`：可基本复用 Project-3 版本，但建议把字段名/错误信息改为 PU task。
- `harness_run_script.sh`：改用 `PROJECT_PU_*` 环境变量。
- `proposer_prompt_prefix.txt`：改写任务说明，重点说明 PU 语义和可用接口。
- `README.md`：给出最小运行方式、正例 CSV 格式、匹配键配置、断点续跑说明。

## 数据输入与配置

建议环境变量命名：

```bash
PROJECT_PU_DATA_CSV=/path/to/unlabeled_or_pool.csv
PROJECT_PU_POSITIVE_CSV=/path/to/positive.csv
PROJECT_PU_FIXED_POOL=0
PROJECT_PU_POOL_SIZE=5000
PROJECT_PU_BATCH_SIZE=100
PROJECT_PU_ROUNDS=1
PROJECT_PU_SEED=42
PROJECT_PU_SEED_QUERIES=0
PROJECT_PU_RESUME_STATE=1
PROJECT_PU_STATE_PATH=
PROJECT_PU_MATCH_COLUMNS=
PROJECT_PU_ID_COLUMN=
```

匹配策略优先级：

1. 如果设置 `PROJECT_PU_ID_COLUMN`，用该列做精确匹配。
2. 如果设置 `PROJECT_PU_MATCH_COLUMNS`，用逗号分隔的多列 tuple 做精确匹配，例如 `sequence,chain_id`。
3. 如果候选池和正例 CSV 都有明显 ID 列，可自动探测：`id`, `ID`, `candidate_id`, `sequence_id`, `name`。
4. 如果没有 ID，则退化为整行规范化匹配：取两边共有列，按列名排序，把数值和字符串规范化后组成 tuple。

建议实现一个明确函数：

```python
def _build_positive_key_set(positive_rows, candidate_fieldnames, id_column, match_columns) -> set[tuple]:
    ...

def _make_pu_labels(pool_rows, positive_key_set, key_columns_or_mode) -> np.ndarray:
    ...
```

注意事项：

- 对浮点列做匹配时要谨慎。优先推荐用户提供稳定 ID 或序列列。
- 如果自动匹配后 `top_k == 0`，应直接报错并提示设置 `PROJECT_PU_ID_COLUMN` 或 `PROJECT_PU_MATCH_COLUMNS`。
- 如果 `positive_csv` 中有重复正例 key，应去重并在日志/metrics 中记录去重数量。
- policy 输入的 `candidates` 必须剥离 `label`，不能泄漏完整正例集合。

## 主流程设计

`main_fix_train_test_input_output.py` 可沿用 Project-3 主流程的大部分代码：

1. 读取候选 CSV。
2. 如果不是 fixed pool，则按 seed 采样 `pool_size` 条。
3. 读取/构造 labels：
   - 若候选池自带 `label` 列：提取 labels 并从传给 policy 的 rows 中删除 `label`。
   - 否则读取 `positive_csv`，按匹配键构造 labels。
4. 加载 `harness/model.py` 的 `select(candidates, history, batch_size, seed)`。
5. 支持 `active_search_state.json` 断点续跑。
6. 每轮调用 policy 选未查询 index。
7. oracle 按 labels 揭示 `label` 并追加到 history。
8. 写出 `harness/outputs/metrics.json` 和 state。

Project-3 中这些函数可直接复用或轻改：

- `_load_selection_policy`
- `_parse_cell`
- `_read_csv_rows`
- `_make_candidate_pool`
- `_extract_inline_labels`
- `_sanitize_selected_indices`
- `_jsonify_row`
- `run_active_search`
- `_build_history_from_records`
- `_load_state`
- `_save_state`

需要替换/新增：

- 删除 `_make_ground_truth_labels` 中对 `compute_x` 的依赖。
- 删除 `_load_ground_truth_csv` 或保留为 debug/兼容入口，命名改为 `_load_label_csv`。
- 新增 positive CSV 匹配与 PU labels 构造逻辑。
- CLI 参数改为 `--positive_csv`, `--id_column`, `--match_columns`。

## 评估指标

`evaluate.py` 建议先保持 Project-3 的 scoring 形式，减少 evolver 集成风险：

```python
delta_precision = delta_hits / max(1, delta_queries)
final_score = clamp(delta_precision, 0, 1) * 100
```

同时在 `metrics.json` 中保留更多 PU 诊断字段：

- `total_hits`
- `delta_hits`
- `total_queries`
- `delta_queries`
- `top_k`
- `recall = total_hits / top_k`
- `hit_curve`
- `auc_normalized`
- `positive_csv`
- `positive_rows`
- `positive_unique_keys`
- `positive_in_pool`
- `match_mode`
- `match_columns`

如果后续希望更偏向“累计发现总数”，可以把 `final_score` 改回 Project-3 README 描述里的 `total_hits / top_k * 100`；但当前 Project-3 的实际 `evaluate.py` 是按本轮 delta precision 打分。PU 版本初期建议先复制实际行为，避免改变演化压力。

## 默认 baseline policy

`hoss-evolution/best/current/harness/model.py` 建议提供一个不依赖外部包的稳健 baseline：

- history 为空：随机选择，或按数值特征做简单 farthest/diverse sampling。
- history 只有正例或只有未标注：结合正例邻近度和随机探索。
- history 同时有 P 和 U：训练轻量 PU-aware scoring。

可实现思路：

1. 从 candidates/history 中提取数值列，跳过 `candidate_index`, `label` 和明显非数值列。
2. 做 median/IQR 或 mean/std 标准化。
3. 把 `history.label=1` 当 P，把 `history.label=0` 当 U，不宣称 U 是真负。
4. 分数由三部分组成：
   - 与已发现 P 的相似度/近邻距离：越接近 P 越高。
   - 与已查询样本的距离：适度鼓励覆盖未探索区域。
   - 随机扰动：避免 deterministic trap。
5. 当 P 数量足够时，可用 logistic/ridge 风格的线性模型，把 U 作为 noisy negative 并降低权重，例如 `weight_U = 0.1 ~ 0.3`。
6. 每轮 top score 中加入 diversity rerank，避免 100 条都挤在同一局部区域。

prompt 中允许 proposer 继续改进这些策略，但要禁止：

- 读取 positive CSV。
- 读取 outputs/state 之外的隐藏标签文件。
- 把未标注样本当作可信负例做过强惩罚。

## `prepare_candidate_pool.py`

为了复现实验，建议提供一个离线工具：

```bash
python project/project-pu-learning/prepare_candidate_pool.py \
  --csv /path/to/unlabeled.csv \
  --positive_csv /path/to/positive.csv \
  --pool_size 5000 \
  --seed 42 \
  --id_column sequence_id \
  --out /path/to/out_dir
```

输出：

```text
candidate_pool_pu_labeled_n5000_seed42.csv
```

该文件包含原始候选列 + `label`。运行 active search 时：

```bash
PROJECT_PU_DATA_CSV=/path/to/candidate_pool_pu_labeled_n5000_seed42.csv \
PROJECT_PU_FIXED_POOL=1 \
bash project/project-pu-learning/harness_run_script.sh project/project-pu-learning/hoss-evolution/best/current
```

预生成 labeled pool 的好处：

- 正例匹配只做一次。
- 多个演化 candidate 使用完全相同 pool 和 labels。
- 方便调试 `top_k == 0` 或匹配列不对的问题。

## run_evolution 集成

`run_evolution.sh` 从 Project-3 复制后做这些修改：

- 工作区变量改名为 `PROJECT_PU_WORKSPACE_DIR` / `PROJECT_PU_SEED_BEST_DIR`。
- `HARNESS_RUN_SCRIPT` 指向 PU 目录。
- deny 规则不再需要特别针对 `index.py`，但仍建议禁止读取显式标签/positive 文件：
  - `NEXAU_DENY_RUN_SHELL_SUBSTRINGS` 增加 `PROJECT_PU_POSITIVE_CSV` 指向文件名或目录片段时需谨慎，避免 proposer 直接 cat 正例 CSV。
  - 更稳的方式是在 prompt 和 harness 运行权限中限制只能改 `model.py`，并且 model 运行时不传 positive path。
- `PROPOSER_PROMPT_PREFIX_PATH` 指向 PU prompt。

## README 需要写清楚的点

- 这是 PU active search，不是监督二分类。
- 用户必须提供正例 CSV，除非 fixed pool 已带 `label`。
- 推荐提供稳定 ID 或序列列作为匹配键。
- `history.label=0` 在策略设计里应视作 unlabeled miss/noisy negative。
- policy 接口与 Project-3 完全相同。
- 最小运行命令、预生成 pool 命令、断点续跑行为。

## 实施步骤

1. 复制 Project-3 文件到 `project-pu-learning`。
2. 改 `main_fix_train_test_input_output.py`：
   - 移除 `compute_x` import。
   - 增加 positive CSV 参数和 key matching。
   - 记录 PU diagnostics。
3. 改 `harness_run_script.sh` 的环境变量前缀。
4. 改 `evaluate.py` 的名称/错误信息，保持 scoring 兼容。
5. 新增 `prepare_candidate_pool.py`。
6. 写 PU 版 `README.md`。
7. 写 PU 版 `proposer_prompt_prefix.txt`。
8. 准备默认 `hoss-evolution/best/current/harness/model.py`。
9. 用一个小型临时 CSV 做 smoke test：
   - 正例能匹配。
   - `top_k > 0`。
   - policy 看不到 `label`。
   - metrics/state 正常写出。
   - evaluate 输出 `final_score`。

## 边界情况

- `positive_csv` 中的正例不在候选池：只影响 `positive_in_pool`，不应计入 `top_k`。
- 候选池中重复 key：建议全部标为正例；metrics 记录 duplicate candidate keys 数。
- 正例过少：`recall` 仍可用，但 `delta_precision` 波动大；可在 README 中建议增大 pool 或 rounds。
- 正例过多：任务接近普通 active search，但仍应保持 U 语义。
- 无数值特征：baseline policy 退回随机和字符串 hash 特征，或者只随机。
- fixed pool 自带 `label` 且同时传 positive CSV：优先使用 inline label，并在日志中说明。

## 验收标准

- `PROJECT_PU_DATA_CSV + PROJECT_PU_POSITIVE_CSV` 可直接跑通一次 harness。
- `candidate_pool_pu_labeled_*.csv` 可作为 fixed pool 跑通。
- `metrics.json` 中 `top_k == positive_in_pool`。
- `queried_history` 中只有已查询样本带 `label`，完整 `candidates` 不含 `label`。
- `evaluate.py` 能读取 metrics 并输出 JSON。
- evolver 仍然只要求 candidate 修改 `harness/model.py`。
