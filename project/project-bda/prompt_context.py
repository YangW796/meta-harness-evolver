from __future__ import annotations

import json
import math
from pathlib import Path


def _safe_float(x: object, default: float | None = None) -> float | None:
    if x is None:
        return default
    try:
        v = float(x)
    except Exception:
        return default
    if not math.isfinite(v):
        return default
    return v


def _safe_int(x: object, default: int = 0) -> int:
    if x is None:
        return default
    try:
        return int(x)
    except Exception:
        return default


def _read_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _pick_metrics_path(workspace: Path) -> Path | None:
    best_path = workspace / "best" / "current" / "harness" / "outputs" / "metrics.json"
    if best_path.exists():
        return best_path

    candidates_dir = workspace / "candidates"
    if not candidates_dir.exists():
        return None

    best_n = -1
    best_candidate_metrics: Path | None = None
    for d in candidates_dir.iterdir():
        if not d.is_dir() or not d.name.startswith("candidate_"):
            continue
        try:
            n = int(d.name.split("_", 1)[1])
        except Exception:
            continue
        p = d / "harness" / "outputs" / "metrics.json"
        if p.exists() and n > best_n:
            best_n = n
            best_candidate_metrics = p
    return best_candidate_metrics


def extract_key_stats(metrics_payload: dict) -> dict:
    test = ((metrics_payload.get("metrics") or {}).get("test") or {}) if isinstance(metrics_payload, dict) else {}
    pool_size = _safe_int(test.get("pool_size"), 0)
    top_k = _safe_int(test.get("top_k"), 0)
    total_queries = _safe_int(test.get("total_queries"), 0)
    total_hits = _safe_int(test.get("total_hits"), 0)
    hit_curve = test.get("hit_curve") if isinstance(test.get("hit_curve"), dict) else {}
    round_details = test.get("round_details") if isinstance(test.get("round_details"), list) else []
    ncg = _safe_float(test.get("ncg"), None)

    expected_hit_rate = (float(top_k) / float(pool_size)) if pool_size > 0 and top_k > 0 else 0.0
    actual_hit_rate = (float(total_hits) / float(total_queries)) if total_queries > 0 else 0.0
    expected_hits = float(total_queries) * expected_hit_rate

    ratio = None
    if expected_hit_rate > 0:
        ratio = actual_hit_rate / expected_hit_rate

    return {
        "data_name": metrics_payload.get("data_name"),
        "task": metrics_payload.get("task"),
        "pool_size": pool_size,
        "top_k": top_k,
        "total_queries": total_queries,
        "total_hits": total_hits,
        "hit_curve": hit_curve,
        "round_details": round_details,
        "ncg": ncg,
        "expected_hit_rate": expected_hit_rate,
        "actual_hit_rate": actual_hit_rate,
        "expected_hits": expected_hits,
        "hit_rate_ratio_vs_random": ratio,
    }


def _format_gene_list(items: list[str], limit: int) -> str:
    trimmed = [str(x).strip() for x in items if str(x).strip()]
    if len(trimmed) <= limit:
        return ", ".join(trimmed)
    head = trimmed[:limit]
    return ", ".join(head) + f", ... (+{len(trimmed) - limit})"


def _top_records(metrics_payload: dict, *, n_hits: int = 20, n_scores: int = 20) -> dict[str, list[dict]]:
    test = ((metrics_payload.get("metrics") or {}).get("test") or {}) if isinstance(metrics_payload, dict) else {}
    records = test.get("queried_records", [])
    if not isinstance(records, list):
        return {"top_hits": [], "top_scores": []}

    norm: list[dict] = []
    for r in records:
        if not isinstance(r, dict):
            continue
        gene = str(r.get("gene", "")).strip()
        score = _safe_float(r.get("score"), 0.0) or 0.0
        hit = _safe_int(r.get("hit"), 0)
        rr = _safe_int(r.get("round"), 0)
        norm.append({"gene": gene, "score": float(score), "abs_score": float(abs(score)), "hit": int(hit), "round": int(rr)})

    top_hits = [x for x in norm if int(x.get("hit", 0)) == 1]
    top_hits.sort(key=lambda x: float(x.get("score", 0.0)), reverse=True)
    top_scores = list(norm)
    top_scores.sort(key=lambda x: float(x.get("score", 0.0)), reverse=True)
    return {"top_hits": top_hits[: max(0, int(n_hits))], "top_scores": top_scores[: max(0, int(n_scores))]}


def build_prompt_context(paths, cfg, candidate_num: int, history, best) -> str:
    workspace = Path(getattr(paths, "workspace", "")).expanduser().resolve()
    metrics_path = _pick_metrics_path(workspace)
    if metrics_path is None:
        return ""

    payload = _read_json(metrics_path)
    stats = extract_key_stats(payload)
    tops = _top_records(payload, n_hits=20, n_scores=20)

    warnings: list[str] = []
    ratio = stats.get("hit_rate_ratio_vs_random")
    if isinstance(ratio, float) and math.isfinite(ratio) and ratio < 0.8 and stats.get("total_queries", 0) >= 128:
        warnings.append(
            "Actual hit rate is significantly below the random baseline. This often means the policy is returning many invalid/duplicate indices (runner then fills randomly), or using a non-informative heuristic (e.g., candidate_index proximity)."
        )

    round_details = stats.get("round_details") if isinstance(stats.get("round_details"), list) else []
    recent_rounds = []
    for rd in round_details[-2:]:
        if not isinstance(rd, dict):
            continue
        selected = rd.get("selected", [])
        if not isinstance(selected, list):
            selected = []
        recent_rounds.append(
            {
                "round": _safe_int(rd.get("round"), 0),
                "hits": _safe_int(rd.get("hits"), 0),
                "precision_at_batch": _safe_float(rd.get("precision_at_batch"), 0.0) or 0.0,
                "selected_preview": _format_gene_list([str(x) for x in selected], 20),
            }
        )

    ctx = {
        "source_metrics_path": str(metrics_path),
        "data_name": stats.get("data_name"),
        "task": stats.get("task"),
        "pool_size": stats.get("pool_size"),
        "top_k": stats.get("top_k"),
        "total_queries": stats.get("total_queries"),
        "total_hits": stats.get("total_hits"),
        "ncg": stats.get("ncg"),
        "actual_hit_rate": stats.get("actual_hit_rate"),
        "expected_hit_rate_random": stats.get("expected_hit_rate"),
        "expected_hits_random": stats.get("expected_hits"),
        "hit_rate_ratio_vs_random": stats.get("hit_rate_ratio_vs_random"),
        "recent_rounds": recent_rounds,
        "top_hits_by_abs_score": tops.get("top_hits", []),
        "top_scores_by_abs_score": tops.get("top_scores", []),
        "warnings": warnings,
    }

    return (
        "## Experiment Feedback Summary (MANDATORY)\n"
        "You MUST use this summary when deciding what to change, and cite at least one concrete item from it in proposer_reasoning.md.\n"
        "Do NOT assume candidate_index has biological meaning.\n"
        "\n"
        + "```json\n"
        + json.dumps(ctx, ensure_ascii=False, indent=2)
        + "\n```\n"
    )
