from __future__ import annotations

import bda_tools

def select(candidates, history, batch_size, seed) -> list[int]:
    """
    Project-BDA 的选点策略。

    接口约定（必须严格保持不变）：
        select(candidates, history, batch_size, seed) -> list[int]

    输入：
    - candidates: list[dict]
        - 单基因数据集：每项形如 {"gene": "<HGNC>"}。
        - 基因对数据集：每项形如 {"gene_a": "<HGNC>", "gene_b": "<HGNC>"}。
        - Gene Search（可选工具）：当 runner 启用时，你可以调用：
          - bda_tools.gene_search(query_gene: str, k: int = 10, diverse: bool = False) -> list[int]
    - history: list[dict]
        - 每项至少包含：
          - candidate_index: int（在 candidates 里的索引）
          - score: float（oracle 返回的分数）
          - hit: int（0/1；runner 允许时才会提供）
    - batch_size: int
    - seed: int

    输出：
    - list[int]：本轮要选择的“新”的候选索引列表（不要重复；已选/重复会被 runner 过滤并随机补齐）。

    你可以实现任何合适的算法/模型（传统算法、机器学习、深度学习、生物学启发式、数学模型等）。

    当你实现 select(...) 时必须调用 gene_search（在 gene_search 可用时）。
    原因：单基因筛选里每个基因只出现一次，单纯基于“已测基因的统计”无法泛化到未测基因；
    Achilles gene_search 用 embedding 的邻域扩展，把已观测到的强信号迁移到未测基因。

    如何调用 gene_search（API 说明）：

    - 函数签名：
        bda_tools.gene_search(query_gene: str, k: int = 10, diverse: bool = False) -> list[int]

    - 参数含义：
        - query_gene: 锚点基因（HGNC symbol），建议从 history 里选 hit=1 或 |score| 较大的基因。
        - k: 返回多少个邻居（最多 k 个）。
        - diverse:
            - False：返回“最相似”的邻居（利用相似性做 exploit）。
            - True：返回“最不相似”的邻居（做 diverse exploration）。

    - 返回值含义：
        - list[int]：候选的 index（直接用于返回 select 的结果；索引对应 candidates 列表）。

    """
    pass
