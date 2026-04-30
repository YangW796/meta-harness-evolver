### A. 先补齐诊断数据（确认到底比随机差多少、差在哪里）
在evaluate时：
1. 从每次 run 的 best/current 或 candidate 的 harness/outputs/metrics.json 抽关键统计
   - pool_size、top_k、total_queries、total_hits、hit_curve、round_details
2. 计算随机基线期望 （每个数据集一条）
   - expected_hits ≈ total_queries * (top_k/pool_size)
   - 如果显著低于期望：优先查“策略是否在重复/无效选择”（例如大量被 runner sanitize 掉导致随机填充、或策略偏向某些无关模式）。

### B. 将每个project的proposer_prompt_prefix.txt改造成python代码
将每个project的proposer_prompt_prefix.txt改造成python代码，用于在meta-harness-evolver/scripts/proposer_runner.py中注入调用。

### C
- 把“必须使用该摘要”的要求写进流程
 在 proposer_task 的“你必须做什么”里加一条（对 project-bda 生效）：
- “先读/利用 summary，再决定要改的 policy；在 proposer_reasoning 里引用 summary 的具体证据（例如某些 hit gene 家族/通路、gene_search anchor 等）。”
- 增加“反模式警告” （专治低命中）
 明确告诉 proposer：
- candidate_index 没有几何意义，不要做“index proximity 扩散”当相似性（除非确认 candidates 排序本身有生物学结构）。
- 若无 Achilles：用“基因名/家族/通路邻居”做扩张策略比 index 距离靠谱；若有 Achilles：优先 gene_search。

### D。
Builder with MCP

在工作区搜索 'step_*_log.log'

step_0_log.log

step_1_log.log

meta-harness-evolver\scripts\proposer_runner.py

meta-harness-evolver\project\project-bda\proposer_prompt_prefix.txt

Thought

1）现阶段命中率偏低的“直接原因”判断（基于你贴的 Sanchez21_down 结果）

- 你这条链路里 top_k=924 很大概率对应 hit_set 大小（约占全库的 ~5%），而 total_queries=128/256/384/512 说明每轮 128、共 4 轮。
- 以常见单基因库规模 pool_size≈18939 粗估，随机命中率期望约 924/18939≈4.9% ：
  - 512 次查询随机期望 hits ≈ 25
  - 你现在 512 次 hits=19（≈3.7%）→ 略低于随机 ，属于“策略没有有效利用反馈/相似性信号，甚至在某些轮次把预算浪费在无关区域”的典型表现。
- 结合我们当前 project-bda 的现实约束：如果 没启用 Achilles gene_search ，策略只能看到 (gene, score[, hit]) ，而 candidate_index 本身没有生物学结构（大概率只是文件顺序/字母序），这会导致很多候选策略（比如“按 index proximity 扩散”）本质上接近随机或更差。
- 所以最可能的根因是： 策略层面缺少“可泛化的相似性/特征”，但提示词又没有强约束 proposer 去利用已有的 gene_search 或者从历史 hit/高分基因做系统性扩张 ，导致进化出来的 policy 经常在“看起来聪明的启发式”上打转，实际提升有限。
2）对照 BioDiscoveryAgent 的 step_0/step_1 提示词：它做对了什么 从你给的 step_0_log.log / step_1_log.log 可以总结 BDA 的提示词框架有几个关键点：

- 强制把“实验反馈”喂给模型 ：Step 1 直接给了“全部已测基因 + 分数表”，再给“hits 列表 + 分数”，这等于给了明确的监督信号与可解释锚点。
- 强制一个可控工具循环 ：明确要求 “Gene Search: 选一个 gene 作为锚点 → 返回相似基因”，并把工具返回结果拼到上下文里。
- 强制输出格式 + 不重复约束 ：模型输出必须可解析、可直接执行，且不能包含已测基因。
相较之下，project-bda 的 proposer 提示词（ proposer_runner.py + project-bda/proposer_prompt_prefix.txt ）更偏“代码演化流程”，没有把“基因层面的反馈摘要”作为强制输入结构，因此 proposer 很容易只根据候选差分/抽象算法描述做改动，错过最关键的任务信号。

## 3）详细改造计划（不写代码版）：怎么改提示词框架，同时不影响其他 project
下面按“先诊断→再改 prompt 注入→再改 project-bda 专属提示→再做验证”的顺序列。

### A. 先补齐诊断数据（确认到底比随机差多少、差在哪里）
1. 从每次 run 的 best/current 或 candidate 的 harness/outputs/metrics.json 抽关键统计
   - pool_size、top_k、total_queries、total_hits、hit_curve、round_details
2. 计算随机基线期望 （每个数据集一条）
   - expected_hits ≈ total_queries * (top_k/pool_size)
   - 如果显著低于期望：优先查“策略是否在重复/无效选择”（例如大量被 runner sanitize 掉导致随机填充、或策略偏向某些无关模式）。
3. 确认 gene_search 是否真正可用 （这是提升的分水岭）
   - 是否设置 BDA_GENE_SEARCH=1 ， BDA_CSV_PATH 是否有完整 achilles.csv
   - 如果多数 run 没开 gene_search：后续 prompt 改造要明确引导“没有 gene_search 时不要用 candidate_index 距离当相似性”。
### B. 在 proposer_runner 侧增加“可选的任务态摘要注入”（核心改造点）
目标：让 proposer 像 BDA Step 1 一样，默认就能看到结构化反馈，而不是“靠它自己想起来去读文件”。

计划做法（保持对其他 project 零影响的关键是“默认关闭/按 project 开关启用”）：

1. 定义一个“Prompt Context 注入开关” （仅计划，不改代码）：
   - 方案 1：环境变量开关，例如 EVOLVER_PROMPT_STYLE=bda_like
   - 方案 2：workspace 里存在某个文件才启用，例如 <workspace>/.prompt_profile=bda
   - 方案 3：仅对 project-bda 的 run_evolution.sh 设置一个 env var，让 proposer_runner 识别到才启用
2. 注入内容设计（token 受控，强结构）
    给 proposer_task 增加一个区块，例如 ## Experiment Feedback Summary ，内容建议是 JSON/表格混合，且限制长度：
   - data_name, pool_size, top_k, hit_rate, total_queries, total_hits, ncg
   - top_hits : top N（例如 20）个 hit 基因（带 score、round）
   - top_scores : top N 个绝对值最大的 score 基因（带 score、round）
   - recent_rounds : 最近 1-2 轮的 selected list + hits count
   - sanitization_stats （如果能拿到）：策略返回的无效/重复比例（帮助发现“模型返回重复→被随机填充→等于随机”的问题）
3. 把“必须使用该摘要”的要求写进流程
    在 proposer_task 的“你必须做什么”里加一条（对 project-bda 生效）：
   - “先读/利用 summary，再决定要改的 policy；在 proposer_reasoning 里引用 summary 的具体证据（例如某些 hit gene 家族/通路、gene_search anchor 等）。”
4. 增加“反模式警告” （专治低命中）
    明确告诉 proposer：
   - candidate_index 没有几何意义，不要做“index proximity 扩散”当相似性（除非确认 candidates 排序本身有生物学结构）。
   - 若无 Achilles：用“基因名/家族/通路邻居”做扩张策略比 index 距离靠谱；若有 Achilles：优先 gene_search。
### C. project-bda 专属提示词（proposer_prompt_prefix.txt）强化为“BDA-like 合同”
这个文件是 project-bda 自己的，不会影响其他 project，是最安全的定制点。

计划修改方向：

1. 加一个“强制读取输出”的指令
   - 明确要求 proposer 必须查看 best/current/harness/outputs/metrics.json （或 candidate 的同名文件），并基于其中 queried_history / round_details 做决策。
2. 加一个“建议的策略骨架（可进化，但必须覆盖）”
   - Round 0：探索（随机或多样化）
   - Round ≥1：从 history 里选若干 anchor（比如 top score / hit）
     - 若 gene_search 可用：对每个 anchor 调 bda_tools.gene_search(anchor, k=BDA_GENE_SEARCH_K, diverse=BDA_GENE_SEARCH_DIVERSE) 得到候选池
     - 若不可用：用“家族/通路邻居 + 多样化填充”的启发式（强调不要用 index 距离）
   - 最终 selection：去重、过滤已选、不足则随机补齐（runner 也会补齐，但策略自己做能减少被动随机填充）
3. 把目标函数写清楚
   - final_score = ncg * 100 ，强调优先提升 ncg ，同时兼顾 cumulative_hits 。
4. 把“输出必须鲁棒”的工程约束写清楚
   - 不能引入新依赖；gene_search 不可用时要降级；pair dataset 时不要调用 gene_search（并提示如何处理 pair：用 gene_a/gene_b 的历史聚合等）。