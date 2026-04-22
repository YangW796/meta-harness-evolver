from __future__ import annotations


def select(
    candidates: list[dict[str, object]],
    history: list[dict[str, object]],
    batch_size: int,
    seed: int,
) -> list[int]:
    """
    Active Search 选择策略（selection policy）。

    输入：
    - candidates: list[dict]，长度约为 5000；每个 dict 是一行候选（列名 -> 值）
      - 不包含隐藏标签 label
      - 不包含黑盒分数
    - history: list[dict]，已查询过的样本（每个 dict 是一行），并额外包含：
      - candidate_index: int（在 candidates 中的行号）
      - label: int（0/1，oracle 揭示的真实标签）
    - batch_size: int，本轮要选择的“新样本”数量（默认 100）
    - seed: int，本轮随机种子（每轮变化）

    输出：
    - list[int]：从 candidates 中选择的行号（长度应尽量为 batch_size，且不要重复/不要选 history 里已选过的）
    """

    pass
