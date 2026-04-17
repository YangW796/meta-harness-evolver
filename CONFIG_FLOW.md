## 配置与运行流程（从零到跑通）

本文把整个仓库从“装环境”到“新建一个 project 并跑进化”串起来，按步骤走即可。

---

## 1) 安装环境（conda + pip）

建议使用 conda，和项目脚本默认的环境名保持一致（`meta-harness-evolver0`）：

```bash
conda create -n meta-harness-evolver0 python=3.12 -y
conda activate meta-harness-evolver0
pip install -U pip
pip install -r requirements.txt
```

说明：
- `requirements.txt` 里包含：numpy/pandas/sklearn、torch、fair-esm、以及 NexAU（用于 proposer）。
- torch/fair-esm 可能需要根据你的机器（CPU/CUDA）自行选择合适版本；如果你已经有可用的 torch 环境，也可以直接复用。

---

## 2) NexAU 代码下载（用于 code-agent 资源目录）

运行 proposer 时不只需要安装 `nexau` 这个 Python 包，还需要一套“code agent 资源目录”（里面有 `system-workflow.md`、tool 定义等）。本仓库通过环境变量 `NEXAU_CODE_AGENT_DIR` 指向它。

推荐做法：把 NexAU 仓库 clone 到本机任意目录：

```bash
git clone https://github.com/nex-agi/NexAU.git
cd NexAU
git checkout v0.4.1
```

然后在 `.env` 里把 `NEXAU_CODE_AGENT_DIR` 指到：

```
NEXAU_CODE_AGENT_DIR=/path/to/NexAU/examples/code_agent
```

补充：
- `requirements.txt` 里 NexAU 默认是 `git+ssh` 安装方式；如果你的机器没配 GitHub SSH Key，可以把那一行改成 `git+https`，或者先配置 SSH Key 再安装。

---

## 3) 配置 .env（需要设置哪些字段、各自含义）

在仓库根目录创建 `.env`（不提交到 git）。项目内的 `project/*/run_evolution.sh` 会 source 它；`scripts/post_to_research.py` 也会读取它。

### 3.1 必选（能跑 proposer 的最小集合）

```
LLM_MODEL=...
LLM_API_KEY=...
NEXAU_CODE_AGENT_DIR=/path/to/NexAU/examples/code_agent
```

- `LLM_MODEL`：proposer 使用的模型名（例如 OpenAI / 兼容接口的模型名）。
- `LLM_API_KEY`：对应的 key。
- `NEXAU_CODE_AGENT_DIR`：NexAU code agent 资源目录（必须存在）。

### 3.2 常用可选（建议配上）

```
LLM_BASE_URL=...
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096
```

- `LLM_BASE_URL`：如果你用的是兼容 OpenAI 的自建/代理接口，在这里填 base url；不需要就留空。
- `LLM_TEMPERATURE` / `LLM_MAX_TOKENS`：控制 proposer 的采样温度与单次最大输出 token。

### 3.3 进化工作区相关（可选）

```
EVOLVER_WORKSPACE=...
```

- `EVOLVER_WORKSPACE`：外循环写数据的 workspace 目录。很多 project 会在各自的 `run_evolution.sh` 里显式设置为 `project/<name>/hoss-evolution`，所以你也可以不在 `.env` 配它。

### 3.4 Feishu 推送（可选，不配也能跑）

```
FEISHU_POST_ENABLED=0
FEISHU_APP_ID=...
FEISHU_APP_SECRET=...
FEISHU_RECEIVE_ID=...
FEISHU_RECEIVE_ID_TYPE=open_id
FEISHU_DRY_RUN=1
```

- `FEISHU_POST_ENABLED`：是否推送（1=推送，0=不推送）。
- `FEISHU_*`：Feishu/Lark 机器人所需配置。
- `FEISHU_DRY_RUN=1`：只打印不发送，方便先验证流程。

### 3.5 训练/运行相关（通常由每个 project 的 run_evolution.sh 设置）

这些变量会被 `scripts/run_evolution.py` 与每个 project 的 `harness_run_script.sh` 用到：

- `HARNESS_RUN_SCRIPT`：每轮 candidate 生成后、evaluate 前要执行的训练脚本路径。
- `REQUIRE_HARNESS_RUN_SCRIPT`：是否强制必须提供 run script（1=强制）。
- `HARNESS_RUN_TIMEOUT_SECONDS`：训练脚本的超时。
- `HARNESS_DEVICE`：cpu/cuda/auto（很多 project 会在 run_evolution.sh 里自动检测 GPU 再决定）。
- `HARNESS_BATCH_SIZE`：训练脚本里用到的 batch size（例如 ESM embedding 的 batch）。
- `PROPOSER_MAX_ITERATIONS` / `PROPOSER_TIMEOUT_SECONDS`：控制 proposer 的迭代次数与超时。

---

## 4) 如何新建一个 project（需要哪些文件、各自做什么）

建议参考现有的 `project/project-1/`、`project/project-2/` 的结构，新建一个目录：

```
project/project-<N>/
  run_evolution.sh
  harness_run_script.sh
  evaluate_project<N>.py
  proposer_prompt_prefix.txt
  input_output.py
  hoss-evolution/
    best/current/harness/
      ... baseline harness files ...
```

下面解释每个“必须文件”的职责（这是最小闭环）：

### 4.1 run_evolution.sh（外循环入口）

职责：设置本 project 的 workspace、训练脚本、评测脚本、超时、是否用 GPU，然后调用仓库根目录的 `scripts/run_evolution.py`。

关键点：
- `WORKSPACE_DIR` 一般设为 `"$PROJECT_DIR/hoss-evolution"`
- `EVALUATE_SCRIPT_PATH` 指向本 project 的 `evaluate_project<N>.py`
- `HARNESS_RUN_SCRIPT` 指向本 project 的 `harness_run_script.sh`
- `PROPOSER_PROMPT_PREFIX` 通常从 `proposer_prompt_prefix.txt` 读取并 export

### 4.2 proposer_prompt_prefix.txt（告诉 proposer：你这是个什么科学任务）

职责：给 proposer 一个“项目背景 + 规则 + 约束”，让它知道：
- 任务输入/输出是什么（数据在哪里来、metrics 写到哪里去）
- 哪些文件允许改（通常是 `candidate_dir/harness/` 下）
- 评测看什么指标（metrics.json 的格式、final_score 的逻辑）
- 不要做什么（比如别改大范围、别写死绝对路径、别引入私密信息）

### 4.3 input_output.py（训练/推理主程序）

职责：真正完成你的科学任务“输入→训练→输出指标”。常见形态：
- `--mode train`：读数据、训练模型、保存模型、写 `harness/outputs/metrics.json`
- `--mode predict`：加载模型、对单条样本预测（可选）

你可以把“模型实现”放在 `candidate_dir/harness/model.py`，然后 `input_output.py` 动态加载它（project-2 就是这么做的）。

### 4.4 harness_run_script.sh（每轮 candidate 的训练脚本）

职责：外循环每轮会把 `candidate_dir` 传进来，这个脚本要：
- 找到 `candidate_dir/harness/` 下的 harness 文件（例如 `model.py`、配置等）
- 调用 `input_output.py --mode train ...`
- 确保最终产出：`candidate_dir/harness/outputs/metrics.json`

外循环会把一些环境变量注入给它（例如 `EVOLVER_WORKSPACE / CANDIDATE_NUM / CANDIDATE_DIR`），你也可以在脚本里增加项目自己的 `PROJECT*_DATA_*` 变量。

### 4.5 evaluate_project<N>.py（评测脚本）

职责：只做“读 candidate 的产出 → 打分 → print 一行 JSON”：
- 输入参数：`candidate_dir`
- 读取：`candidate_dir/harness/outputs/metrics.json`
- 输出：最后一行 `json.dumps({final_score: ..., ...})`

外循环 `scripts/run_evolution.py` 会把评测脚本 stdout 的最后一行当作 JSON 解析。

---

## 5) 运行（并把日志保存到文件）

每个 project 都有自己的入口脚本，建议在仓库根目录运行：

```bash
bash project/<project-name>/run_evolution.sh > project/<project-name>/log.txt 2>&1
```

如果你想批量跑多个 project（谨慎，注意资源占用），可以用：

```bash
bash project/*/run_evolution.sh > run_all.log 2>&1
```

---

## 建议：要跑“完整项目并长期保存结果”，先复制一份 project 目录

外循环会持续写入 workspace（通常在 `project/<name>/hoss-evolution/`）并生成大量候选与日志。为了保证源码目录长期保持干净可复现，建议：
- 复制整个 `project/<name>/` 到一个新目录再跑（例如 `project/<name>-run/`）
- 把数据路径/环境变量配置在新目录对应的 `run_evolution.sh` 里

