# Scripts 使用说明

本目录说明 `scripts/` 下几个脚本如何执行，以及各参数/环境变量的含义。

## 统一约定：Evolution Workspace

所有脚本默认把进化数据写到同一个 workspace 目录中：

- 默认：`~/hoss-evolution`
- 可通过环境变量覆盖：`EVOLVER_WORKSPACE=/path/to/hoss-evolution`
- 或通过脚本参数覆盖：`--workspace /path/to/hoss-evolution`（`run_evolution.py` / `evaluate.py` / `post_to_research.py` 都支持）

workspace 目录结构（示例）：

```
~/hoss-evolution/
├── candidates/
│   └── candidate_N/
│       ├── harness/
│       ├── eval_scores.json
│       ├── traces/
│       └── proposer_reasoning.md
├── best/
│   └── current/
│       ├── harness/
│       └── eval_scores.json
└── evolution_log.jsonl
```

## run_evolution.py（主入口：完整外循环）

作用：执行一次完整的“提案 -> 校验 -> 评测 -> 记录 -> 推送”外循环。

执行：

```bash
python3 scripts/run_evolution.py
```

常用参数：

- `--workspace <DIR>`：进化 workspace 目录（默认：`$EVOLVER_WORKSPACE` 或 `~/hoss-evolution`）
- `--candidate-num <N>`：指定本次候选编号；不传则自动取 `candidates/` 下最大编号 + 1
- `--iterations <K>`：连续执行 K 轮外循环（默认：`$EVOLVER_ITERATIONS` 或 `1`）。若同时指定了 `--candidate-num N`，将依次运行 `candidate_N, candidate_{N+1}, ...` 共 K 轮
- `--evaluate-script <PATH>`：指定评测脚本/可执行文件（默认从环境变量 `EVALUATE_SCRIPT` 读取；若也未设置则使用 `scripts/evaluate.py`）
  - 该程序必须接受一个参数 `<candidate_dir>`
  - 且最后一行 stdout 必须输出 JSON（`run_evolution.py` 读取最后一行并 `json.loads`）

相关环境变量（提案器 / NexAU）：

- `EVOLVER_TEST_MODE=1`：跳过真实 proposer，直接在 candidate 的 `harness/config.yaml` 里写入一个最小改动，并生成 `proposer_reasoning.md`（用于本地联调）
- `NEXAU_HOME`：NexAU 仓库路径（默认：`/home/wy/Documents/NexAU`）
- `LLM_MODEL` / `LLM_API_KEY`：NexAU proposer 运行所需（缺失会报错）
- `LLM_BASE_URL` / `LLM_API_TYPE` / `LLM_TEMPERATURE` / `LLM_MAX_TOKENS`：透传给 NexAU 的 LLM 配置（可选）
- `PROPOSER_MAX_ITERATIONS`：NexAU agent 最大迭代次数（默认：`20`）
- `PROPOSER_TIMEOUT_SECONDS`：NexAU proposer 超时时间（秒，默认：`300`）
- `EVOLVER_ITERATIONS`：`run_evolution.py --iterations` 的默认值（默认：`1`）

说明：

- `run_evolution.py` / `evaluate.py` / `post_to_research.py` 启动时都会自动读取 `meta-harness-evolver/.env`（若存在）并将其中的键值加载到环境变量（不会覆盖已经在 shell 中设置的变量）

退出码：

- `0`：成功完成一次评测
- `1`：跳过/失败（例如 proposer 失败、校验失败、评测失败）
- `2`：内部错误（例如 child mode 参数不足）

## evaluate.py（评测器：对单个 candidate 打分）

作用：对某个 `candidate_dir` 执行 benchmark，最后一行输出 JSON（供 `run_evolution.py` 解析）。

执行：

```bash
python3 scripts/evaluate.py /path/to/hoss-evolution/candidates/candidate_7
```

参数：

- `--workspace <DIR>`：进化 workspace 目录（用于定位 `runtime_workspace`；默认同上）
- `<candidate_dir>`：候选目录，内部应包含 `harness/`

说明：

- 评测过程中会把 `candidate_dir/harness/` 下的文件拷贝到 `<workspace>/runtime_workspace/`，并在 `candidate_dir/backup/` 做备份，结束后会恢复备份。

## post_to_research.py（推送到飞书 Feishu/Lark）

作用：把一次迭代结果汇总为文本消息，并通过 `lark-oapi` 发送到飞书。

执行（最小参数）：

```bash
python3 scripts/post_to_research.py 7 /path/to/candidate_7 72.3 1
```

参数：

- `candidate_num`：候选编号（整数）
- `candidate_dir`：候选目录路径
- `score`：本次得分（float）
- `proposer_success`：`1`=success，`0`=failed
- `--workspace <DIR>`：进化 workspace（默认同上）
- `--prev-best-score <FLOAT>`：本次迭代开始前的 best 分数，用于正确计算 “vs best 的增量”（不传则用当前 best 文件计算）

相关环境变量（飞书）：

- `FEISHU_APP_ID`：飞书应用 App ID
- `FEISHU_APP_SECRET`：飞书应用 App Secret
- `FEISHU_RECEIVE_ID`：接收人/群的 id（例如 user open_id / chat_id 等）
- `FEISHU_RECEIVE_ID_TYPE`：接收 id 类型（默认：`open_id`）
- `FEISHU_DRY_RUN=1`：不真正发送，只打印消息

依赖：

- `pip install -U lark-oapi`

## validate.sh（可选：shell 版轻量校验）

作用：对 `candidate_dir/harness/` 做一些快速规则检查（例如必须文件是否存在、是否包含禁用规则等）。

执行：

```bash
bash scripts/validate.sh /path/to/hoss-evolution/candidates/candidate_7
```
