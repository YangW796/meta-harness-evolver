#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EVOLVER_DIR="$ROOT_DIR/meta-harness-evolver"
# --- 环境变量文件加载 ---
# 如果存在 .env 文件，自动加载其中的环境变量
ENV_FILE="$EVOLVER_DIR/.env"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

# --- 核心运行配置（请根据实际情况手动修改） ---

# Conda 虚拟环境名称
CONDA_ENV="meta-harness-evolver"

# 进化数据的统一工作空间目录（包含 candidates、best、evolution_log.jsonl）
WORKSPACE_DIR="$ROOT_DIR/hoss-evolution"

# 打分评测脚本路径（负责根据 candidate 跑 AI4S 任务并输出带 final_score 的 JSON）
EVALUATE_SCRIPT_PATH="$EVOLVER_DIR/scripts/evaluate-example.py"

# 本次运行的候选方案编号（留空则自动取当前 candidates 目录下最大编号 + 1）
CANDIDATE_NUM=""

# 连续执行的迭代轮数（外循环执行次数）
ITERATIONS="1"

# --- 调试开关 ---

# 飞书推送开关：1=仅打印不真实发送，0=真实发送
export FEISHU_DRY_RUN="1"

# 测试模式开关：1=跳过真实 NexAU Proposer 的大模型调用（只在 config.yaml 里加一行内容用于快速测试全流程），0=真实调用
export EVOLVER_TEST_MODE="0"

# --- 组装命令并执行 ---

ARGS=(python "$EVOLVER_DIR/scripts/run_evolution.py" --workspace "$WORKSPACE_DIR" --iterations "$ITERATIONS" --evaluate-script "$EVALUATE_SCRIPT_PATH")
if [[ -n "$CANDIDATE_NUM" ]]; then
  ARGS+=(--candidate-num "$CANDIDATE_NUM")
fi

cd "$ROOT_DIR"
conda run -n "$CONDA_ENV" "${ARGS[@]}"


