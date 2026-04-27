## Project-Mobius 是什么任务（Reranking）

这是一个“抗体候选 reranking”任务：用 Mobius 训练一个轻量的序列+结构 surrogate 模型，在固定的 train/val/test split 上预测 oracle ranking score，并在 test 集上评估排序相关指标（例如 NDCG@K、Spearman）。

主程序：
- mobius/scripts/run_mobius_lightning.py

进化的对象是 `hoss-evolution/best/current/harness/model/` 下的模型包（对 Mobius 的 `mobius/reranking/model/` 的替代实现），核心文件是：
- [architecture.py](./hoss-evolution/best/current/harness/model/architecture.py)

---

## 模型接口（必须遵守）

Mobius 的 Lightning 代码会 import 并使用以下符号：
- `from mobius.reranking.model.architecture import RerankingModelConfig, MobiusReranker`

并要求：
- `MobiusReranker.forward(batch) -> dict`
- 返回 dict 至少包含：
  - `pred_utility`
  - `pred_score_direct`
  - `confidence_logits`
  - `ddg_status_logits`

---

## hoss-evolution 目录里会出现哪些文件

`project/project-mobius/hoss-evolution/` 是进化工作区，结构与 project-2 类似：

- `best/current/harness/model/`
  - 当前最好模型实现（默认每轮候选从这里复制一份作为起点）
- `candidates/candidate_<N>/harness/outputs/metrics.json`
  - 本轮 reranking 的指标（从 Lightning 的 CSV logger 解析出来）
- `candidates/candidate_<N>/eval_scores.json`
  - 标准化评测分数（`final_score` 等，用于 best 更新）
- `candidates/candidate_<N>/traces/harness_run.log`
  - 每轮 harness 运行日志

---

## 主流程（白话版）

链路如下：  
`run_evolution.sh → harness_run_script.sh → mobius/scripts/run_mobius_lightning.py → evaluate.py`

### 1) harness_run_script.sh：跑一次 Mobius reranking 训练 + test（给某个 candidate 打分）

文件：[harness_run_script.sh](./harness_run_script.sh)

可配置环境变量：
- `MOBIUS_HOME`：mobius 代码根目录（默认取仓库内 `mobius/`）
- `MOBIUS_CONFIG`：Mobius 的 YAML 配置路径（默认 `mobius/configs/reranker_demo.yaml`）
- `MOBIUS_OUTPUT_DIR`：一次运行输出目录（默认 `harness/outputs/mobius_run`）
- `MOBIUS_DEVICES / MOBIUS_ACCELERATOR / MOBIUS_STRATEGY / MOBIUS_MAX_ROWS / MOBIUS_RESUME_FROM`：透传给 `run_mobius_lightning.py` 的可选参数
- `MOBIUS_DATA_ROOT / MOBIUS_ORACLE_CSV / MOBIUS_NORMALIZATION_JSON / MOBIUS_TARGET / MOBIUS_METHOD / MOBIUS_BATCH_SIZE / MOBIUS_NUM_WORKERS / MOBIUS_SEED`：覆盖 config.yaml 中的 `data.*`

### 3) evaluate.py：把 metrics.json 翻译成最终分数

文件：[evaluate.py](./evaluate.py)

它读取 `harness/outputs/metrics.json` 中的 reranking 指标，并输出 `final_score`。

---

## 最小可运行方式（不进化，只跑一次训练+评测）

```bash
MOBIUS_HOME=/path/to/mobius \
MOBIUS_CONFIG=/path/to/mobius/configs/reranker_demo.yaml \
bash project/project-mobius/harness_run_script.sh project/project-mobius/hoss-evolution/best/current
```
