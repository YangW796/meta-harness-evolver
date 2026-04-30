from __future__ import annotations


def select(
    candidates: list[dict[str, object]],
    history: list[dict[str, object]],
    batch_size: int,
    seed: int,
) -> list[int]:
    """
    Positive-Unlabeled Active Search 选择策略接口。

    输入：
    - candidates: list[dict]，固定候选池；每个 dict 是一行候选（列名 -> 值）
      - 不包含完整隐藏标签 label
      - 不包含 positive CSV 路径
    - history: list[dict]，已查询过的样本；每个 dict 除原始字段外，还包含：
      - candidate_index: int（在 candidates 中的行号）
      - label: int（oracle 揭示的标签；1 表示匹配已知正例，0 表示未标注/未命中）
    - batch_size: int，本轮要选择的新样本数量
    - seed: int，本轮随机种子

    输出：
    - list[int]：从 candidates 中选择的 candidate_index

    注意：
    - 不要返回重复 index。
    - 不要返回 history 里已经查询过的 index。
    - PU learning 中 label=0 不是可靠真负例，只代表该样本未匹配已知正例集合。
    """

    pass
