## Project-2 是什么任务

这是一个“蛋白序列/结构 → 打分”的科学任务：给定每条样本的 `Sequence`（氨基酸序列）和 `Structure`（对应结构文件路径线索），我们构造一个目标分数 `x`，训练/进化一个模型去预测 `x`。最终评价不是回归误差，而是“能不能把真正的 Top-k 样本挑出来”。

- 输入：`merged_results.csv` 中的样本（至少包含 `Sequence / Structure / iptm / DDG / SAP Score / FV Charge`）
- 目标：用特征预测 `x = compute_x(df)`（见 [index.py](./index.py)）
- 评价：在测试集上把 `x` 和预测值各自取 Top-k（由 `top_ratio` 决定），计算二分类 F1（Top-k F1），再乘 100 作为 `final_score`（见 [evaluate_project2.py](./evaluate_project2.py)）

任务难度可以理解成两档：
- 基础版：`x = compute_x(df)`（默认使用）
- 进阶版：把标签替换为 `x0 = compute_x0(df)`（更复杂的非线性组合，更难拟合）

模型默认用：
- 序列特征：ESM2 embedding（见 [main_fix_train_test_input_output.py](./main_fix_train_test_input_output.py) 的 `load_esm/_encode_sequences`）
- 结构特征：从 cif 文本里非常粗糙地统计 `ATOM` 数量与 residue 数量（见 `parse_cif`）

进化的对象是 `hoss-evolution/best/current/harness/` 下的“harness 代码”，当前核心就是一个 [model.py](./hoss-evolution/best/current/harness/model.py)（提供 `train_model/predict_model/save_model/load_model` 四个函数接口）。

---

## hoss-evolution 目录里会出现哪些文件（以及它们是干什么的）

`project/project-2/hoss-evolution/` 是本项目的“进化工作区”。现在可能只看到一小部分文件；当你运行进化后，会陆续自动生成下面这些：

- `best/current/harness/`
  - 目前已存在：`model.py`：当前“最好”的模型实现（每轮候选都会从这里复制一份作为起点）
  - 可能新增：其他脚本/配置（如果 proposer 认为需要）
- `best/current/eval_scores.json`
  - 当前 best 的打分结果（`final_score` 等）
- `best/current/winner_note.md`
  - 记录是哪一个 `candidate_N` 成为 best 以及分数变化
- `candidates/candidate_<N>/harness/`
  - 第 N 轮候选的 harness 代码（从 best 复制后做“一处小改动”）
- `candidates/candidate_<N>/proposer_reasoning.md`
  - LLM 这轮改动的简短说明（改了什么、为什么）
- `candidates/candidate_<N>/traces/harness_run.log`
  - 这轮训练脚本（`harness_run_script.sh`）的运行日志（stdout/stderr 都会在这里）
- `candidates/candidate_<N>/harness/outputs/metrics.json`
  - 训练脚本产出的指标文件（test 的 F1、top_ratio 等），评测脚本会读取它
- `candidates/candidate_<N>/eval_scores.json`
  - 评测脚本输出的标准化成绩（`final_score` 等），用于更新 best
- `candidates/candidate_<N>/change_record.json` / `change_record.md`
  - 自动对比“candidate harness vs best harness”的 diff 记录（方便回看每轮改了什么）
- `evolution_log.jsonl`
  - 每轮一个 JSON 行：候选编号、分数、是否成功、改动摘要等（用于全局追踪）

---

## 从数据准备到进化评测的一整套流程（白话版）

下面按你给的顺序把链路串起来：  
`compute_x_generate_fix_train_test.py → run_evolution.sh → harness_run_script.sh → main_fix_train_test_input_output.py → evaluate_project2.py`

### 1) compute_x_generate_fix_train_test.py：先把数据“打上分”和“固定划分”

文件：[compute_x_generate_fix_train_test.py](./compute_x_generate_fix_train_test.py)

它干两件事：
- 读取 `merged_results.csv`，用 `compute_x(df)` 算一个分数 `x`（线性组合，见 [index.py](./index.py) 的 `compute_x`）
- 用随机种子生成一个固定的 `train/test` 列（写到 split 文件里），避免每次训练划分都变

同时它还能把样本按 `x` 排序后，导出 Top 比例或阈值筛选后的子集 CSV（一般用于你自己做快速实验/筛数据；进化主流程不强依赖这个子集）。

注意：
- 训练主脚本默认用的是 `compute_x(df)` 作为真实标签；如果你想把任务调成“进阶版”，可以把训练脚本里的 `compute_x` 改成 `compute_x0`。
- 训练时需要一个带 `split` 列的 split CSV；默认期望文件名是 `train_test_split.csv`，如果你生成的是带参数的文件名，需要自行复制/改名，或通过环境变量指定（见后面）。

### 2) run_evolution.sh：启动“外循环进化”（提案→训练→评测→更新 best）

文件：[run_evolution.sh](./run_evolution.sh)

它做的事情很朴素：
- 设置一堆环境变量：workspace 路径、训练脚本路径、超时、batch size、是否用 GPU 等
- 检测机器有没有 GPU；如果 `USE_GPU=1` 且确实有 GPU，就设置 `HARNESS_DEVICE=cuda` 并导出 `EVOLVER_NUM_GPUS=<数量>`，否则走 CPU
- 调用仓库根目录的 `scripts/run_evolution.py` 开始跑 N 轮（默认 `ITERATIONS=20`）

### 3) harness_run_script.sh：对某个 candidate 真的“跑训练”

文件：[harness_run_script.sh](./harness_run_script.sh)

进化每轮会生成一个 `candidates/candidate_N/`，然后外循环会调用这个脚本：

- 输入：`<candidate_dir>`
- 它会把 `candidate_dir/harness/model.py` 当成“模型实现”
- 它会调用 `main_fix_train_test_input_output.py --mode train ...` 去训练并写出指标

你最需要关心的可配置环境变量（不改代码也能跑）：
- `PROJECT2_DATA_ROOT`：结构文件根目录（默认是一个内部路径）
- `PROJECT2_DATA_CSV`：`merged_results.csv` 的路径
- `PROJECT2_SPLIT_FILE`：固定 split 文件路径（必须存在并包含 `split` 列）
- `PROJECT2_TOP_RATIO`：Top-k 的比例
- `HARNESS_DEVICE`：`cpu/cuda/auto`（通常由 `run_evolution.sh` 设好）
- `HARNESS_BATCH_SIZE`：ESM 编码 batch size

### 4) main_fix_train_test_input_output.py：训练、保存模型、产出 metrics.json

文件：[main_fix_train_test_input_output.py](./main_fix_train_test_input_output.py)

训练（`--mode train`）的主逻辑是：
- 读取 `merged_results.csv`
- 读取 split 文件，并拿 `Structure` 做 merge，把 `split=train/test` 拼回到原始 df
- 计算真实标签 `x = compute_x(df)`（见 [index.py](./index.py) 的 `compute_x`）
- 用 ESM 把 `Sequence` 编成向量，再拼上 cif 的两个结构统计特征，得到 `X`
- 调用 `candidate_dir/harness/model.py` 里的：
  - `train_model(X_train, y_train, ...)` 得到模型对象
  - `predict_model(model, X_test, ...)` 得到测试集预测
  - 计算 Top-k F1
  - `save_model(model, model_path)` 把模型保存到 `candidate_dir/harness/iptm_model.pt`（默认）
- 写出 `candidate_dir/harness/outputs/metrics.json`，里面包含 test 的 F1、top_ratio、样本数等

其中 `_load_model_api()` 会用 importlib 动态加载 `model.py`，让每个 candidate 可以带着自己修改后的模型代码跑训练。

### 5) evaluate_project2.py：把 metrics.json 翻译成“最终分数”

文件：[evaluate_project2.py](./evaluate_project2.py)

它只做一件事：
- 读 `candidate_dir/harness/outputs/metrics.json` 的 `test.f1`
- `final_score = clamp(f1,0,1) * 100`，并输出标准 JSON（`run_evolution.py` 会读取最后一行 JSON）

---

## 最小可运行方式（只跑一轮训练，不进化）

只要你已经准备好：
- `merged_results.csv`
- 固定 split 文件（带 `split` 列）
- 结构根目录（包含 `.../<pdb_id>/af3_output/<structure>/<structure>_model.cif` 这样的层级）

你可以直接跑：

```bash
bash project/project-2/harness_run_script.sh project/project-2/hoss-evolution/best/current
```

如果你的数据路径不同，推荐用环境变量覆盖：

```bash
PROJECT2_DATA_ROOT=/path/to/root \
PROJECT2_DATA_CSV=/path/to/merged_results.csv \
PROJECT2_SPLIT_FILE=/path/to/train_test_split.csv \
HARNESS_DEVICE=cpu \
bash project/project-2/harness_run_script.sh project/project-2/hoss-evolution/best/current
```

---

## 建议：完整跑实验时先复制整个 project-2

如果你要“跑完整项目 + 保存结果/日志”，建议先复制一份整个 `project/project-2/` 到新的目录里再运行（例如 `project/project-2-run/`），不要直接在原始 `project-2` 里反复迭代：

- 进化会持续写入 `hoss-evolution/`、生成大量候选目录与日志
- 复制一份单独跑，可以避免把源码目录搞乱，保证主分支的 `project-2` 始终保持“干净可复现”的基准状态
