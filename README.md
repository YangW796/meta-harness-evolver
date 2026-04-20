# Meta-Harness Evolver

一个面向 AI4S/科研代码任务的“外循环进化系统”：外循环不断生成候选 harness（代码/配置），运行任务脚本得到评分，再基于历史结果继续改进。

## 1. 项目概况

- 目标：让 LLM 作为“代码 proposer”，在**完整文件系统上下文**里迭代改 harness，从而提升任务分数。
- 进化对象（mutable surface）：`<workspace>/candidates/candidate_N/harness/` 下的文件（例如 `model.py`、`config.yaml`、脚本等）。
- 反馈信号：不是只给一个标量分数，而是保留每轮的 `eval_scores.json`、`harness_run.log`、`change_record.*`、`proposer_reasoning.md`，供后续轮次读取复盘。

## 2. 项目设计

### 2.1 总体设计（数据流）

一次迭代的主链路如下（目录均在 `EVOLVER_WORKSPACE` 下）：

1) Propose：proposer 读取历史 candidates 与 best，生成 `candidate_N/harness/*`  
2) Validate：轻量校验（语法/文件存在等）  
3) Harness Run：执行项目提供的 `HARNESS_RUN_SCRIPT`，产出 `candidate_N/harness/outputs/metrics.json`  
4) Evaluate：执行项目提供的 evaluate 脚本，把 metrics 映射成标准 `final_score` JSON  
5) Log：写 `candidate_N/eval_scores.json`、`candidate_N/change_record.*`、追加 `evolution_log.jsonl`  
6) Best Update：如果分数更好，用 candidate 覆盖 `best/current/harness/`  
7) Post（可选）：发 Feishu/Lark 通知

### 2.2 模块设计（scripts 侧）

scripts 的职责是“通用外循环”，与具体任务无关；任务差异通过环境变量和 project 的脚本注入。

- 主入口： [scripts/run_evolution.py](./scripts/run_evolution.py)
- 配置读取： [scripts/evolver_config.py](./scripts/evolver_config.py)（从 env 读取 `HARNESS_RUN_SCRIPT` 等）
- workspace 路径： [scripts/evolution_paths.py](./scripts/evolution_paths.py)
- 提示词调度（Exploit/Explore/Restart）： [scripts/evolution_prompting.py](./scripts/evolution_prompting.py)
- proposer 总控（含“改动幅度门槛”“新颖性约束”自动重提）： [scripts/proposer_runner.py](./scripts/proposer_runner.py)
- NexAU 子进程封装： [scripts/nexau_runner.py](./scripts/nexau_runner.py)
- Harness 执行与日志： [scripts/harness_runner.py](./scripts/harness_runner.py)
- Evaluate/Best/ChangeRecord/Feishu： [scripts/evaluation_runner.py](./scripts/evaluation_runner.py)
- Feishu 推送脚本： [scripts/post_to_research.py](./scripts/post_to_research.py)
- 工具函数： [scripts/shared.py](./scripts/shared.py)

### 2.3 模块设计（project 侧）

每个 `project/project-*` 提供一套“任务适配层”：

- `run_evolution.sh`：设置 workspace、脚本路径、超时、GPU/CPU 等，并启动外循环
- `harness_run_script.sh`：执行本任务的训练/搜索/推理逻辑，写出 `harness/outputs/metrics.json`
- `evaluate_project*.py` 或 `evaluate.py`：读取 metrics，输出标准 JSON（最后一行）给外循环
- `proposer_prompt_prefix.txt`：给 proposer 的任务背景与约束（通常限制“只能改 harness 下某些文件”）
- `hoss-evolution/best/current/harness/*`：baseline harness（默认外循环每轮从这里复制作为起点；EXPLORE/RESTART 且设置 `EVOLVER_INITIAL_HARNESS_DIR` 时，从初始目录复制）

## 3. 项目结构与文件说明（从主入口逐渐深入）

### 3.1 你通常从哪里启动

从某个 project 的 `run_evolution.sh` 启动，例如：

- [project-2/run_evolution.sh](./project/project-2/run_evolution.sh)
- [project-3/run_evolution.sh](./project/project-3/run_evolution.sh)

它们会：
- 读取仓库根目录 `.env`（如果存在）
- export 一组外循环需要的 env（workspace、harness 脚本路径、proposer 提示词前缀等）
- 调用 `python scripts/run_evolution.py ...`

### 3.2 scripts/run_evolution.py（外循环主控）

见 [run_evolution.py](./scripts/run_evolution.py)：

- `--workspace`：指定本次 workspace（默认来自 `EVOLVER_WORKSPACE`）
- `--iterations`：本进程内要跑多少个 candidate
- `--evaluate-script`：评测脚本路径（project 提供）

每轮 candidate 的子流程：
- Propose： [proposer_runner.py](./scripts/proposer_runner.py)
- Validate/Harness： [harness_runner.py](./scripts/harness_runner.py)
- Evaluate/Log/Best/Post： [evaluation_runner.py](./scripts/evaluation_runner.py)

### 3.3 workspace 结构（运行后生成）

```
<EVOLVER_WORKSPACE>/
  candidates/
    candidate_N/
      harness/                  # 本轮候选 harness（proposer 生成）
      traces/                   # proposer/harness 日志
      proposer_reasoning.md
      eval_scores.json          # 标准化后的分数（final_score 等）
      change_record.json/md     # candidate vs best 的差异
  best/current/
    harness/                    # 当前最好 harness
    eval_scores.json
    winner_note.md
  evolution_log.jsonl           # 逐轮汇总日志
```

## 4. 环境变量总表（按功能分类）

说明：
- 仓库会在多个脚本中读取 `.env`（根目录），你可以把常用 env 放在 `.env` 里。
- 各 `project/*/run_evolution.sh` 也会 export 一些默认值（可覆盖）。

### 4.1 外循环入口（run_evolution.py）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `EVOLVER_WORKSPACE` | `~/hoss-evolution` | workspace 根目录（候选/最佳/日志都写这里）。 |
| `EVOLVER_ITERATIONS` | `1` | `--iterations` 未显式传参时的默认值。 |
| `EVALUATE_SCRIPT` | 空 | `--evaluate-script` 未显式传参时的默认值。 |
| `EVOLVER_TEST_MODE` | `0` | =1 时 proposer 会写最小改动用于 dry-run（由 project 脚本常设/可覆盖）。 |

### 4.2 Proposer（NexAU/LLM）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `LLM_MODEL` | 无（必填） | NexAU proposer 使用的模型名。 |
| `LLM_API_KEY` | 无（必填） | NexAU proposer 使用的 API key。 |
| `LLM_BASE_URL` | 空 | 可选：OpenAI-compatible endpoint。 |
| `LLM_TEMPERATURE` | `0.7` | proposer 采样温度。 |
| `LLM_MAX_TOKENS` | `4096` | proposer 最大输出 tokens。 |
| `NEXAU_CODE_AGENT_DIR` | `examples/code_agent` | NexAU agent 资源目录。 |
| `PROPOSER_PROMPT_PREFIX` | 空 | project 注入的任务背景/约束前缀（通常由 `proposer_prompt_prefix.txt` 读入）。 |
| `PROPOSER_MAX_ITERATIONS` | `20` | NexAU agent 最大 tool iterations（project 往往设更大）。 |
| `PROPOSER_TIMEOUT_SECONDS` | `300` | proposer 子进程超时（秒）。 |

### 4.3 Harness 执行（训练/搜索脚本）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `HARNESS_RUN_SCRIPT` | 空 | 每轮候选生成后执行的 bash 脚本：`bash <script> <candidate_dir>`。 |
| `REQUIRE_HARNESS_RUN_SCRIPT` | `0` | =1 时必须提供 `HARNESS_RUN_SCRIPT`，否则该轮失败。 |
| `HARNESS_RUN_TIMEOUT_SECONDS` | `600` | harness_run_script 超时（秒）。 |
| `HARNESS_RUN_LOG_HEARTBEAT_SECONDS` | `5` | harness 运行期间的心跳写日志间隔（秒）。 |
| `HARNESS_DEVICE` | 空（由 project 设） | 运行设备提示（常见：cpu/cuda/auto）。 |
| `HARNESS_BATCH_SIZE` | 空（由 project 设） | 任务脚本内部 batch size（例如 embedding 编码 batch）。 |
| `EVOLVER_NUM_GPUS` | `0` | 可用 GPU 数（project 探测后 export，用于在 prompt 里提示硬件）。 |

外循环调用 `HARNESS_RUN_SCRIPT` 时会注入（若未设置则 setdefault）：

| 变量 | 默认值 | 说明 |
|---|---|---|
| `CANDIDATE_DIR` | 自动注入 | 当前 candidate 目录（同 argv[1]）。 |
| `CANDIDATE_NUM` | 自动注入 | 当前 candidate 编号。 |

### 4.4 探索性调度与约束（Explore/Exploit/Restart）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `EVOLVER_EXPLOIT_WINDOW` | `5` | 最近多少轮内 best 有更新则进入 Exploit（偏小改）。 |
| `EVOLVER_EXPLORE_EVERY` | `5` | 每 N 个 candidate 强制一次 Explore（定期探索）。 |
| `EVOLVER_EXPLORE_WINDOW` | `10` | 连续 N 个 candidate 无提升则触发一次自适应 Explore（并在 10/20/30… 节点触发）。 |
| `EVOLVER_RESTART_WINDOW` | `30` | 连续 N 个 candidate 无提升则触发 Restart（强换方向）。 |
| `EVOLVER_BRAINSTORM_ENABLED` | `1` | 是否启用“停滞触发探索/重启”逻辑。 |
| `EVOLVER_BRAINSTORM_MIN_DELTA` | `1e-12` | 判定“提升”的最小分数差。 |
| `EVOLVER_NOVELTY_LOOKBACK` | `10` | 新颖性约束的回看窗口（读取最近 K 个 `change_record.*`）。 |
| `EVOLVER_INITIAL_HARNESS_DIR` | 空 | EXPLORE/RESTART 模式下的候选起始 harness 目录；支持相对路径（相对 `EVOLVER_WORKSPACE`）。为空则沿用 `best/current/harness`。 |
| `EVOLVER_EXPLORE_MIN_LINE_DELTA` | `15` | Explore 轮的最小改动幅度门槛（行变更量不足会自动重提）。 |
| `EVOLVER_BRAINSTORM_MIN_LINE_DELTA` | `30` | Brainstorm/Restart 的最小改动幅度门槛（行变更量不足会自动重提）。 |

### 4.5 Feishu/Lark 推送（可选）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `FEISHU_POST_ENABLED` | `1` | =1 才会发送推送。 |
| `FEISHU_POST_TIMEOUT_SECONDS` | `30` | 推送超时（秒）。 |
| `FEISHU_DRY_RUN` | 空 | =1 时只打印不发送。 |
| `FEISHU_APP_ID` | 空 | Feishu 应用 ID。 |
| `FEISHU_APP_SECRET` | 空 | Feishu 应用密钥。 |
| `FEISHU_RECEIVE_ID` | 空 | 接收方 ID（open_id/chat_id 等）。 |
| `FEISHU_RECEIVE_ID_TYPE` | `open_id` | 接收方 ID 类型。 |

### 4.6 Project 环境变量

project 的 `harness_run_script.sh` 通常会提供任务级变量（可在 `.env` 或 shell 中覆盖）。

**Project-1**（见 [project-1/harness_run_script.sh](./project/project-1/harness_run_script.sh)）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `PYTHON_BIN` | `python` | python 可执行文件。 |
| `PROJECT1_DATA_CSV` | `<固定默认路径>/merged_results.csv` | 输入 CSV。 |
| `PROJECT1_MODEL_PATH` | `<candidate>/harness/iptm_model.pt` | 保存模型路径。 |
| `HARNESS_DEVICE` | `cpu` | 设备。 |
| `HARNESS_BATCH_SIZE` | `16` | batch。 |

**Project-2**（见 [project-2/harness_run_script.sh](./project/project-2/harness_run_script.sh)）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `PYTHON_BIN` | `python` | python 可执行文件。 |
| `PROJECT2_DATA_ROOT` | 项目脚本内置路径 | 结构根目录。 |
| `PROJECT2_DATA_CSV` | `$PROJECT2_DATA_ROOT/merged_results.csv` | 输入 CSV。 |
| `PROJECT2_SPLIT_FILE` | `<csv_dir>/train_test_split.csv` | 固定 train/test split。 |
| `PROJECT2_TOP_RATIO` | `0.1` | Top-k 比例。 |
| `PROJECT2_MODEL_PATH` | `<candidate>/harness/iptm_model.pt` | 保存模型路径。 |
| `HARNESS_DEVICE` | `cpu` | 设备。 |
| `HARNESS_BATCH_SIZE` | `16` | batch。 |

**Project-3（Active Search）**（见 [project-3/harness_run_script.sh](./project/project-3/harness_run_script.sh)）

| 变量 | 默认值 | 说明 |
|---|---|---|
| `PYTHON_BIN` | `python` | python 可执行文件。 |
| `PROJECT3_DATA_ROOT` | 项目脚本内置路径 | 数据根目录。 |
| `PROJECT3_DATA_CSV` | `$PROJECT3_DATA_ROOT/merged_results.csv` | 输入 CSV（大 CSV 或预生成候选池 CSV）。 |
| `PROJECT3_FIXED_POOL` | `0` | =1 时把 `PROJECT3_DATA_CSV` 当作固定候选池，不采样。 |
| `PROJECT3_POOL_SIZE` | `5000` | 候选池大小（仅大 CSV 且未 fixed_pool 时生效）。 |
| `PROJECT3_TOP_RATIO` | `0.2` | 好分子比例（输入 CSV 不含 label 且未提供 ground truth 时生效）。 |
| `PROJECT3_GROUND_TRUTH_CSV` | 空 | 可选：外部 ground truth（candidate_index,label）。若输入 CSV 自带 label 列则不需要。 |
| `PROJECT3_BATCH_SIZE` | `100` | 每轮查询数。 |
| `PROJECT3_ROUNDS` | `1` | 本次运行轮数（默认 1）。 |
| `PROJECT3_SEED` | `42` | 随机种子。 |
| `PROJECT3_SEED_QUERIES` | `0` | 冷启动随机查询数（仅历史为空时生效）。 |
| `PROJECT3_RESUME_STATE` | `1` | 是否从 state 断点续跑。 |
| `PROJECT3_STATE_PATH` | 空 | 自定义 state 文件路径；空则默认写到 `harness/outputs/active_search_state.json`。 |

## 5. 如何自己编写一个新 Project（流程）

下面是一个最小可复用的“新项目模板流程”（建议从 project-2/3 复制改起）。

### 5.1 新建目录与文件

1) 建目录：`project/project-<N>/`  
2) 至少包含：
- `run_evolution.sh`
- `harness_run_script.sh`
- `evaluate_project<N>.py`（或 `evaluate.py`）
- `proposer_prompt_prefix.txt`
- `hoss-evolution/best/current/harness/`（baseline harness 文件）

### 5.2 定义 harness 的“可变面”

把你希望 LLM 修改的文件放到：

`project/project-<N>/hoss-evolution/best/current/harness/`

并在 `proposer_prompt_prefix.txt` 明确：
- 允许修改哪些文件（强烈建议只允许修改 harness 下的少数文件）
- 必须保留哪些函数签名/输出格式
- 禁止修改哪些 IO/评测逻辑

### 5.3 编写 harness_run_script.sh（产生 metrics.json）

要求：
- 脚本签名：`bash harness_run_script.sh <candidate_dir>`
- 读取 `<candidate_dir>/harness/` 下的代码/配置
- 运行你的训练/推理/搜索流程
- 写出：`<candidate_dir>/harness/outputs/metrics.json`

`metrics.json` 的内容由你自定义，但 evaluate 脚本必须能从中读取并输出最终分数。

### 5.4 编写 evaluate 脚本（输出标准 JSON）

外循环只要求：evaluate 脚本对 `<candidate_dir>` 做评测，并在 stdout 最后一行输出 JSON，例如：

```json
{"final_score": 73.2, "category_scores": {...}, "scenario_scores": {...}}
```

### 5.5 编写 run_evolution.sh（把任务挂到外循环）

典型做法（参考 project-2/3）：
- export `EVOLVER_WORKSPACE` 指向 `project/project-<N>/hoss-evolution`
- export `HARNESS_RUN_SCRIPT` 指向 `project/project-<N>/harness_run_script.sh`
- export `HARNESS_RUN_TIMEOUT_SECONDS`、`PROPOSER_MAX_ITERATIONS`、`PROPOSER_TIMEOUT_SECONDS`
- export `PROPOSER_PROMPT_PREFIX="$(cat proposer_prompt_prefix.txt)"$'\n'`
- 调用 `python scripts/run_evolution.py --workspace ... --evaluate-script ...`

完成以上步骤后，你就可以像运行现有项目一样启动：

```bash
bash project/project-<N>/run_evolution.sh
```
