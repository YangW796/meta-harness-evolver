import argparse
import csv
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np

_INDEX_IMPORT_PATH: str | None = None
try:
    _INDEX_IMPORT_PATH = str(Path(__file__).resolve().parents[4])
except IndexError:
    _INDEX_IMPORT_PATH = None

if _INDEX_IMPORT_PATH is not None:
    sys.path.insert(0, _INDEX_IMPORT_PATH)
else:
    for p in Path(__file__).resolve().parents:
        if (p / "index.py").exists():
            _INDEX_IMPORT_PATH = str(p)
            sys.path.insert(0, _INDEX_IMPORT_PATH)
            break

from index import compute_x

_SCRIPT_DIR = str(Path(__file__).resolve().parent)
for _p in [_INDEX_IMPORT_PATH, _SCRIPT_DIR, ""]:
    if _p and _p in sys.path:
        while _p in sys.path:
            sys.path.remove(_p)
sys.modules.pop("index", None)


def _load_selection_policy(model_file: str):
    model_path = Path(model_file).expanduser().resolve()
    if not model_path.exists():
        raise ValueError(f"model file does not exist: {model_path}")

    spec = importlib.util.spec_from_file_location("candidate_policy_module", str(model_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load policy module from: {model_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    if callable(getattr(module, "select", None)):
        return module.select

    for cls_name in ["SelectionPolicy", "Policy", "Model"]:
        cls = getattr(module, cls_name, None)
        if cls is None:
            continue
        inst = cls()
        if callable(getattr(inst, "select", None)):
            return inst.select

    raise ValueError("model file missing required callable: select(candidates, history, batch_size, seed) -> list[int]")


def _parse_cell(v: str) -> object:
    s = (v or "").strip()
    if s == "":
        return ""
    try:
        x = float(s)
    except Exception:
        return s
    if not np.isfinite(x):
        return 0.0
    return x


def _read_csv_rows(csv_path: str) -> list[dict[str, object]]:
    path = Path(csv_path).expanduser().resolve()
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV missing header: {path}")
        rows: list[dict[str, object]] = []
        for r in reader:
            row: dict[str, object] = {}
            for k in reader.fieldnames:
                row[k] = _parse_cell(r.get(k, ""))
            rows.append(row)
    return rows


def _make_candidate_pool(rows: list[dict[str, object]], pool_size: int, seed: int) -> list[dict[str, object]]:
    if pool_size <= 0:
        raise ValueError(f"pool_size must be positive, got: {pool_size}")
    if pool_size >= len(rows):
        return list(rows)
    rng = np.random.default_rng(int(seed))
    keep_idx = rng.choice(len(rows), size=int(pool_size), replace=False).tolist()
    return [rows[i] for i in keep_idx]


def _make_ground_truth_labels(pool_rows: list[dict[str, object]], top_ratio: float) -> np.ndarray:
    if not pool_rows:
        return np.zeros((0,), dtype=np.int8)
    r = float(top_ratio)
    if not (0.0 < r < 1.0):
        raise ValueError(f"top_ratio must be in (0, 1), got: {r}")
    k = int(max(1, int(round(len(pool_rows) * r))))
    k = int(min(k, len(pool_rows)))
    y = np.asarray(compute_x(pool_rows), dtype=np.float64).reshape(-1)
    order = np.argsort(-y, kind="mergesort")
    labels = np.zeros((len(pool_rows),), dtype=np.int8)
    if k > 0:
        labels[order[:k]] = 1
    return labels


def _load_ground_truth_csv(path: str, n: int) -> np.ndarray:
    p = Path(path).expanduser().resolve()
    with p.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"ground_truth CSV missing header: {p}")
        required = {"candidate_index", "label"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise ValueError(f"ground_truth CSV missing columns {sorted(missing)}: {p}")
        labels = np.zeros((n,), dtype=np.int8)
        seen = 0
        for r in reader:
            try:
                i = int(float(str(r.get("candidate_index", "")).strip()))
                lab = int(float(str(r.get("label", "")).strip()))
            except Exception:
                continue
            if 0 <= i < n:
                labels[i] = 1 if lab != 0 else 0
                seen += 1
        if seen == 0:
            raise ValueError(f"ground_truth CSV contains no valid rows: {p}")
    return labels


def _extract_inline_labels(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], np.ndarray | None]:
    if not rows:
        return rows, None
    if "label" not in rows[0]:
        return rows, None
    labels = np.zeros((len(rows),), dtype=np.int8)
    stripped: list[dict[str, object]] = []
    for i, r in enumerate(rows):
        rr = dict(r)
        v = rr.pop("label", 0)
        try:
            labels[i] = 1 if int(float(str(v).strip())) != 0 else 0
        except Exception:
            labels[i] = 0
        stripped.append(rr)
    return stripped, labels


def _sanitize_selected_indices(
    selected: object,
    n: int,
    already_selected: set[int],
    batch_size: int,
    seed: int,
) -> list[int]:
    out: list[int] = []
    seen: set[int] = set()

    if selected is None:
        selected_list: list[object] = []
    elif isinstance(selected, (list, tuple, np.ndarray)):
        selected_list = list(selected)
    else:
        selected_list = [selected]

    for v in selected_list:
        try:
            idx = int(v)
        except Exception:
            continue
        if idx < 0 or idx >= n:
            continue
        if idx in already_selected or idx in seen:
            continue
        out.append(idx)
        seen.add(idx)
        if len(out) >= batch_size:
            break

    if len(out) < batch_size:
        remaining = [i for i in range(n) if i not in already_selected and i not in seen]
        if remaining:
            rng = np.random.default_rng(int(seed))
            fill_n = min(batch_size - len(out), len(remaining))
            fill = rng.choice(np.asarray(remaining, dtype=np.int64), size=int(fill_n), replace=False).tolist()
            out.extend(int(x) for x in fill)

    return out


def run_active_search(
    pool_rows: list[dict[str, object]],
    labels: np.ndarray,
    select_fn,
    rounds: int,
    batch_size: int,
    seed: int,
    seed_queries: int,
    initial_history: list[dict[str, object]] | None = None,
    initial_already_selected: set[int] | None = None,
    start_round: int = 0,
) -> dict:
    # Active Search 核心循环：
    # - pool_rows: 固定候选池（长度通常为 5000）
    # - labels: oracle 的真实标签（policy 不可见）
    # - select_fn: policy 的 select(...)，负责给出本轮要查询的 candidate_index 列表
    # - initial_history/initial_already_selected/start_round: 用于断点续跑（从历史状态继续跑）
    n = int(len(pool_rows))
    # already_selected：全局已查询过的 candidate_index 集合（确保跨轮不重复选）
    already_selected: set[int] = set(initial_already_selected or set())
    # history：已查询过的样本记录（行内容 + candidate_index + label），会作为 policy 输入
    history: list[dict[str, object]] = [dict(r) for r in (initial_history or [])]

    # seed_queries：可选的“冷启动”随机查询（仅在历史为空时生效）
    rng = np.random.default_rng(int(seed) + int(start_round))
    if seed_queries > 0 and n > 0 and not history:
        seed_queries = int(min(seed_queries, n))
        seed_idx = rng.choice(n, size=seed_queries, replace=False).tolist()
        seed_idx = _sanitize_selected_indices(seed_idx, n=n, already_selected=already_selected, batch_size=seed_queries, seed=seed)
        for i in seed_idx:
            # oracle：把真实 label 写入 history（policy 的下一轮可见）
            r = dict(pool_rows[i])
            r["candidate_index"] = int(i)
            r["label"] = int(labels[int(i)])
            history.append(r)
        already_selected.update(int(i) for i in seed_idx)

    # per_round：每轮的统计；hit_curve：累计命中曲线（x=累计查询数，y=累计 hits）
    per_round: list[dict] = []
    cumulative_hits = int(sum(int(r.get("label", 0)) for r in history))
    total_queries = int(len(history))
    hit_curve_queries: list[int] = [total_queries]
    hit_curve_hits: list[int] = [cumulative_hits]

    # 主循环：每次执行 rounds 轮（默认 1），每轮查询 batch_size 个新样本
    executed_rounds = 0
    for t in range(int(rounds)):
        # 候选池耗尽则提前结束
        if len(already_selected) >= n:
            break
        # global_round：从 start_round 起累加，用于续跑时保证每轮 seed 不同
        global_round = int(start_round) + int(t)
        # policy 输出：期望是 list[int] 的 candidate_index（可能包含重复/越界/已选）
        selected_raw = select_fn(pool_rows, history, int(batch_size), int(seed) + global_round)
        # 统一清洗：去重、去已选、裁剪到 batch_size，不足则随机补齐（也保证不重复）
        selected = _sanitize_selected_indices(
            selected_raw,
            n=n,
            already_selected=already_selected,
            batch_size=int(batch_size),
            seed=int(seed) + 10_000 + global_round,
        )
        # oracle 揭示：本轮命中数（hits_t）
        hits_t = int(labels[np.asarray(selected, dtype=np.int64)].sum()) if selected else 0

        # 将本轮查询结果写入 history（带 label），并更新已选集合
        for i in selected:
            r = dict(pool_rows[int(i)])
            r["candidate_index"] = int(i)
            r["label"] = int(labels[int(i)])
            history.append(r)
        already_selected.update(int(i) for i in selected)

        # 更新累计统计与曲线
        cumulative_hits += hits_t
        total_queries += int(len(selected))
        hit_curve_queries.append(total_queries)
        hit_curve_hits.append(cumulative_hits)
        executed_rounds += 1

        # 记录本轮指标（Precision@batch_size 等）
        per_round.append(
            {
                "round": int(global_round + 1),
                "queried": int(len(selected)),
                "hits": int(hits_t),
                "cumulative_hits": int(cumulative_hits),
                "precision_at_batch": float(hits_t / max(1, int(len(selected)))),
            }
        )
        # 已找到全部好分子（labels.sum()）则提前结束
        if cumulative_hits >= int(labels.sum()):
            break

    # top_k：本次 ground truth 中好分子总数（由 labels 决定，通常约为 pool_size * top_ratio）
    top_k = int(labels.sum())
    # recall：累计找到的好分子 / 全部好分子
    recall = float(cumulative_hits / max(1, top_k))

    # AUC：对 hit curve 做梯形积分（越大表示越早找到更多好分子）
    area = 0.0
    for i in range(1, len(hit_curve_queries)):
        x0, x1 = float(hit_curve_queries[i - 1]), float(hit_curve_queries[i])
        y0, y1 = float(hit_curve_hits[i - 1]), float(hit_curve_hits[i])
        area += (x1 - x0) * (y0 + y1) / 2.0
    # 归一化 AUC：除以 (总查询数 * top_k)，便于不同设置间对比
    auc_norm = float(area / max(1.0, float(hit_curve_queries[-1]) * float(max(1, top_k))))

    # 将 history 压缩成可序列化的 queried_records（用于 state 持久化/断点续跑）
    queried_records: list[dict[str, int]] = []
    for r in history:
        try:
            queried_records.append({"candidate_index": int(r["candidate_index"]), "label": int(r["label"])})
        except Exception:
            continue

    return {
        "pool_size": int(n),
        "top_k": int(top_k),
        "rounds": int(start_round + executed_rounds),
        "executed_rounds": int(executed_rounds),
        "batch_size": int(batch_size),
        "seed": int(seed),
        "seed_queries": int(seed_queries),
        "total_queries": int(total_queries),
        "total_hits": int(cumulative_hits),
        "recall": recall,
        "auc": float(area),
        "auc_normalized": auc_norm,
        "hit_curve": {"queries": hit_curve_queries, "hits": hit_curve_hits},
        "round_details": per_round,
        "queried_records": queried_records,
    }


def _build_history_from_records(
    pool_rows: list[dict[str, object]],
    records: list[dict[str, int]],
) -> tuple[list[dict[str, object]], set[int], int]:
    history: list[dict[str, object]] = []
    already_selected: set[int] = set()
    total_hits = 0
    n = len(pool_rows)
    for rec in records:
        try:
            i = int(rec.get("candidate_index", -1))
            lab = int(rec.get("label", 0))
        except Exception:
            continue
        if i < 0 or i >= n or i in already_selected:
            continue
        row = dict(pool_rows[i])
        row["candidate_index"] = i
        row["label"] = 1 if lab != 0 else 0
        history.append(row)
        already_selected.add(i)
        total_hits += int(row["label"])
    return history, already_selected, total_hits


def _load_state(path: str) -> dict:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return {}
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


def _save_state(path: str, payload: dict) -> None:
    p = Path(path).expanduser().resolve()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["active_search"], default="active_search")
    parser.add_argument("--csv", required=True, help="large CSV path or prebuilt candidate_pool CSV path")
    parser.add_argument("--model_dir", default="model.py", help="selection policy implementation file")
    parser.add_argument("--pool_size", type=int, default=int(os.environ.get("PROJECT3_POOL_SIZE", "5000")))
    parser.add_argument("--top_ratio", type=float, default=float(os.environ.get("PROJECT3_TOP_RATIO", "0.2")))
    parser.add_argument("--batch_size", type=int, default=int(os.environ.get("PROJECT3_BATCH_SIZE", "100")))
    parser.add_argument("--rounds", type=int, default=int(os.environ.get("PROJECT3_ROUNDS", "1")))
    parser.add_argument("--seed", type=int, default=int(os.environ.get("PROJECT3_SEED", "42")))
    parser.add_argument("--seed_queries", type=int, default=int(os.environ.get("PROJECT3_SEED_QUERIES", "0")))
    parser.add_argument("--fixed_pool", action="store_true")
    parser.add_argument("--ground_truth_csv", default=os.environ.get("PROJECT3_GROUND_TRUTH_CSV", ""))
    parser.add_argument("--state_path", default=os.environ.get("PROJECT3_STATE_PATH", ""))
    parser.add_argument("--resume_state", type=int, default=int(os.environ.get("PROJECT3_RESUME_STATE", "1")))
    args = parser.parse_args()

    rows = _read_csv_rows(args.csv)
    csv_name = Path(args.csv).name
    use_fixed = bool(args.fixed_pool) or csv_name.startswith("candidate_pool_")
    pool_rows = list(rows) if use_fixed else _make_candidate_pool(rows, pool_size=int(args.pool_size), seed=int(args.seed))

    pool_rows, inline_labels = _extract_inline_labels(pool_rows)
    if inline_labels is not None:
        labels = inline_labels
    elif args.ground_truth_csv:
        labels = _load_ground_truth_csv(args.ground_truth_csv, n=len(pool_rows))
    else:
        labels = _make_ground_truth_labels(pool_rows, top_ratio=float(args.top_ratio))
    select_fn = _load_selection_policy(args.model_dir)

    default_state_path = str(Path(args.model_dir).expanduser().resolve().parent / "outputs" / "active_search_state.json")
    state_path = args.state_path if args.state_path else default_state_path
    state = _load_state(state_path) if int(args.resume_state) != 0 else {}
    record_list: list[dict[str, int]] = []
    completed_rounds = 0
    if state:
        record_list = state.get("queried_records", [])
        if not isinstance(record_list, list):
            record_list = []
        try:
            completed_rounds = int(state.get("completed_rounds", 0))
        except Exception:
            completed_rounds = 0

    history, already_selected, _ = _build_history_from_records(pool_rows, record_list)
    seed_queries = int(args.seed_queries) if not history else 0
    metrics = run_active_search(
        pool_rows=pool_rows,
        labels=labels,
        select_fn=select_fn,
        rounds=int(args.rounds),
        batch_size=int(args.batch_size),
        seed=int(args.seed),
        seed_queries=seed_queries,
        initial_history=history,
        initial_already_selected=already_selected,
        start_round=int(completed_rounds),
    )

    output_dir = Path(args.model_dir).expanduser().resolve().parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"metrics": {"test": metrics}}
    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    state_payload = {
        "completed_rounds": int(metrics.get("rounds", completed_rounds)),
        "pool_size": int(len(pool_rows)),
        "top_k": int(labels.sum()),
        "batch_size": int(args.batch_size),
        "seed": int(args.seed),
        "queried_records": metrics.get("queried_records", []),
        "total_queries": int(metrics.get("total_queries", 0)),
        "total_hits": int(metrics.get("total_hits", 0)),
    }
    _save_state(state_path, state_payload)
    print(f"Metrics saved to {metrics_path}")
    print(f"State saved to {state_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
