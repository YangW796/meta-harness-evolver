## Project-3 是什么任务（Active Search）

这是一个“主动搜索（Active Search）”科学任务：在一个固定候选池（5000 条分子/抗体候选）里，用尽量少的查询找到尽量多的“好分子”（Top 1000）。

- 数据：大 CSV（每行一个候选分子/结构/序列等字段）
- 黑盒打分：`y = compute_x(row)`（见 [index.py](./index.py)）
- 真实标签（只用于评测，policy 不可见）：
  - 按 y 排序取 Top `top_k=1000` → `label=1`
  - 其余 → `label=0`
- 每轮行为：policy 从 5000 个候选中选 `batch_size=100` 个“没选过的”样本，oracle 揭示 label，history 增量更新
- 目标指标：在固定查询预算内最大化 `total_hits`（累计命中数），并输出 hit curve / Precision@100 / Recall / AUC（可选）

进化的对象仍然是 `hoss-evolution/best/current/harness/` 下的 harness 代码，核心是一个 [model.py](./hoss-evolution/best/current/harness/model.py)，但在 Project-3 中：

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

`project/project-3/hoss-evolution/` 是进化工作区，结构与 project-2 类似：

- `best/current/harness/model.py`
  - 当前最好 policy（每轮候选从这里复制一份作为起点）
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
- `PROJECT3_DATA_ROOT`：数据根目录（默认指向内部路径）
- `PROJECT3_DATA_CSV`：大 CSV 的路径（默认 `$PROJECT3_DATA_ROOT/merged_results.csv`）
- `PROJECT3_POOL_SIZE`：候选池大小（默认 5000）
- `PROJECT3_TOP_K`：好分子数量（默认 1000）
- `PROJECT3_BATCH_SIZE`：每轮查询数（默认 100）
- `PROJECT3_ROUNDS`：轮数（默认 10，总查询 = rounds * batch_size）
- `PROJECT3_SEED`：采样与随机的种子（默认 42）
- `PROJECT3_SEED_QUERIES`：可选的初始随机 seed queries（默认 0）

### 2) main_fix_train_test_input_output.py：执行 Active Search 并写 metrics.json

文件：[main_fix_train_test_input_output.py](./main_fix_train_test_input_output.py)

它会：
- 从大 CSV 采样出固定的 5000 条候选池
- 用 `compute_x` 计算 y 并构造 ground truth top-1000 标签（评测内部使用）
- 多轮调用 `harness/model.py` 的 `select(...)` 选择未选过的样本
- oracle 揭示 label，更新 history，并记录每轮命中与累计命中
- 写出 `harness/outputs/metrics.json`

### 3) evaluate.py：把 metrics.json 翻译成最终分数

文件：[evaluate.py](./evaluate.py)

它读取 `test.total_hits` 与 `test.top_k`，并输出：
- `final_score = clamp(total_hits / top_k, 0, 1) * 100`

---

## 最小可运行方式（不进化，只跑一次）

```bash
PROJECT3_DATA_CSV=/path/to/merged_results.csv \
PROJECT3_POOL_SIZE=5000 \
PROJECT3_TOP_K=1000 \
PROJECT3_BATCH_SIZE=100 \
PROJECT3_ROUNDS=10 \
PROJECT3_SEED=42 \
bash project/project-3/harness_run_script.sh project/project-3/hoss-evolution/best/current
```

或直接跑主脚本：

```bash
python project/project-3/main_fix_train_test_input_output.py \
  --csv /path/to/merged_results.csv \
  --model_dir project/project-3/hoss-evolution/best/current/harness/model.py \
  --pool_size 5000 \
  --top_k 1000 \
  --batch_size 100 \
  --rounds 10 \
  --seed 42
```
