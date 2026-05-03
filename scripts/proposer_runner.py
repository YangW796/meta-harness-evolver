from __future__ import annotations

import os
import json
import difflib
from pathlib import Path

from evolver_config import EvolverConfig
from evolution_paths import EvolverPaths, get_best_candidate
from evolution_prompting import choose_prompt_mode
from nexau_runner import run_proposer_with_nexau
from shared import iter_effective_files, iter_effective_files_recursive


def _load_prompt_context_provider(paths: EvolverPaths):
    style = str(os.environ.get("EVOLVER_PROMPT_STYLE", "")).strip()
    if style != "bda_like":
        return None

    raw_path = str(os.environ.get("EVOLVER_PROMPT_CONTEXT_FILE", "")).strip()
    if not raw_path:
        return None

    p = Path(raw_path).expanduser()
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()
    else:
        p = p.resolve()
    if not p.exists():
        print(f"[PROPOSER] EVOLVER_PROMPT_CONTEXT_FILE not found: {p}")
        return None

    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("evolver_prompt_context", str(p))
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fn = getattr(module, "build_prompt_context", None)
        if callable(fn):
            return fn
    except Exception as e:
        print(f"[PROPOSER] Failed to load prompt context provider: {e}")
        return None
    return None


def _extract_tags(text: str) -> set[str]:
    t = (text or "").lower()
    tags: set[str] = set()
    patterns: dict[str, list[str]] = {
        "linear": ["ridge", "lasso", "linear", "elasticnet"],
        "svm_kernel": ["svm", "rbf", "kernel"],
        "tree_boost": ["xgboost", "lightgbm", "catboost", "gbdt", "gradientboost", "randomforest", "extra trees"],
        "nn": ["mlp", "dropout", "batchnorm", "layernorm", "adam", "sgd"],
        "feature": ["standard", "normalize", "scaler", "pca", "feature"],
        "calibration": ["calibration", "isotonic", "platt"],
        "objective_rank": ["pairwise", "listwise", "ranking", "rank"],
        "objective_quantile": ["quantile", "pinball"],
        "objective_classification": ["classification", "logistic", "sigmoid", "softmax", "crossentropy"],
        "objective_regression": ["regression", "mse", "mae", "huber"],
        "uncertainty": ["uncertainty", "ensemble", "bootstrap", "thompson"],
    }
    for tag, keys in patterns.items():
        if any(k in t for k in keys):
            tags.add(tag)
    return tags


def _load_recent_change_texts(candidates_dir: Path, k: int) -> list[str]:
    items: list[tuple[int, Path]] = []
    for d in candidates_dir.iterdir():
        if not d.is_dir() or not d.name.startswith("candidate_"):
            continue
        try:
            n = int(d.name.split("_", 1)[1])
        except Exception:
            continue
        items.append((n, d))
    items.sort(key=lambda x: x[0])
    texts: list[str] = []
    for _, d in items[-k:]:
        p = d / "change_record.json"
        if p.exists():
            try:
                payload = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                payload = {}
            diffs = payload.get("diffs", [])
            if isinstance(diffs, list):
                for it in diffs:
                    if isinstance(it, dict) and isinstance(it.get("diff"), str):
                        texts.append(it["diff"])
        else:
            md = d / "change_record.md"
            if md.exists():
                try:
                    texts.append(md.read_text(encoding="utf-8", errors="replace"))
                except Exception:
                    pass
    return texts


def _recent_tags(candidates_dir: Path, k: int) -> set[str]:
    tags: set[str] = set()
    for txt in _load_recent_change_texts(candidates_dir, k=k):
        tags |= _extract_tags(txt)
    return tags


def _extract_json_payload(text: str) -> object | None:
    if not isinstance(text, str):
        return None
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    for ln in reversed(lines[-50:]):
        if not (ln.startswith("[") or ln.startswith("{")):
            continue
        try:
            return json.loads(ln)
        except Exception:
            continue
    t = text.strip()
    candidates: list[str] = []
    b0, b1 = t.rfind("["), t.rfind("]")
    if 0 <= b0 < b1:
        candidates.append(t[b0 : b1 + 1])
    o0, o1 = t.rfind("{"), t.rfind("}")
    if 0 <= o0 < o1:
        candidates.append(t[o0 : o1 + 1])
    for cand in candidates:
        try:
            return json.loads(cand)
        except Exception:
            pass
    return None


def plan_attempts(
    paths: EvolverPaths,
    cfg: EvolverConfig,
    candidate_num: int,
    attempts: int,
    candidate_dir_override: Path | None = None,
) -> list[dict]:
    import uuid

    attempts = max(1, int(attempts))
    if attempts <= 1:
        return []

    candidate_dir = candidate_dir_override or (paths.candidates_dir / f"candidate_{candidate_num}")
    candidate_dir.mkdir(parents=True, exist_ok=True)
    (candidate_dir / "traces").mkdir(exist_ok=True)

    best = get_best_candidate(paths)
    novelty_k = int(os.environ.get("EVOLVER_NOVELTY_LOOKBACK", "10"))
    novelty_k = max(1, novelty_k)
    recent_tag_set = _recent_tags(paths.candidates_dir, k=novelty_k)

    best_harness_dir = paths.best_dir / "harness"
    if best_harness_dir.exists():
        files = [f.relative_to(best_harness_dir).as_posix() for f in iter_effective_files_recursive(best_harness_dir)]
        target_files_str = "\n".join([f"   - {f}" for f in sorted(files)])
    else:
        target_files_str = "   - (No files found)"

    prefix_parts: list[str] = []
    script_raw = str(getattr(cfg, "harness_run_script", "") or "").strip()
    if script_raw:
        script_path = Path(script_raw).expanduser()
        candidates = []
        if script_path.is_absolute():
            candidates.append(script_path)
        else:
            candidates.append((Path.cwd() / script_path).resolve())
            candidates.append((Path(__file__).resolve().parents[1] / script_path).resolve())
        for sp in candidates:
            p = sp.parent / "proposer_prompt_prefix.txt"
            if p.exists():
                try:
                    txt = p.read_text(encoding="utf-8", errors="replace").strip()
                except Exception:
                    txt = ""
                if txt:
                    prefix_parts.append(txt)
                break
    if not prefix_parts:
        default_prefix = Path(__file__).resolve().parents[1] / "project" / "project-bda" / "proposer_prompt_prefix.txt"
        if default_prefix.exists():
            try:
                txt = default_prefix.read_text(encoding="utf-8", errors="replace").strip()
            except Exception:
                txt = ""
            if txt:
                prefix_parts.append(txt)
    extra_prefix = str(getattr(cfg, "proposer_prompt_prefix", "") or "").strip()
    if extra_prefix:
        prefix_parts.append(extra_prefix)
    injected_prefix = ("\n\n".join(prefix_parts).strip() + "\n\n") if prefix_parts else ""

    planner_task = "\n".join(
        [
            "You are the Attempt Planner for an evolution run.",
            "",
            f"Goal: produce {attempts} distinct attempt directions for candidate_{candidate_num}.",
            "Each attempt should be meaningfully different in algorithmic direction and not a trivial variant.",
            "",
            "Constraints:",
            "- Attempts should avoid repeating these recently used strategy tags where possible:",
            f"{sorted(recent_tag_set)}",
            "- Each attempt must specify what to change and why.",
            "- The edit should be compatible with the project harness run script.",
            "",
            "Allowed files include:",
            f"{target_files_str}",
            "",
            "Output requirement:",
            "- Output ONLY a JSON array on a single line (no markdown).",
            "- JSON schema: [{attempt:int, title:str, strategy_tags:list[str], hypothesis:str, implementation_outline:str}].",
            "- attempt values must be 1..N.",
            "",
            f"Best score so far: {best['final_score'] if best else 'N/A'}",
            "",
            "Now plan the attempts and output the JSON array.",
        ]
    )
    if injected_prefix:
        planner_task = injected_prefix + planner_task

    agent_session_id = str(uuid.uuid4())[:8]
    result = run_proposer_with_nexau(
        task=planner_task,
        label=f"evolver-attempt-planner-{agent_session_id}",
        work_dir=paths.workspace,
        timeout_seconds=int(os.environ.get("PROPOSER_ATTEMPT_PLANNER_TIMEOUT_SECONDS", "120") or "120"),
        log_dir=candidate_dir / "traces",
        max_iterations_override=min(max(int(os.environ.get("PROPOSER_MAX_ITERATIONS", "20")) // 2, 10), 40),
    )

    output_text = result.get("output", "")
    payload = _extract_json_payload(output_text if isinstance(output_text, str) else "")
    if isinstance(payload, list):
        plans = [p for p in payload if isinstance(p, dict)]
        normalized: list[dict] = []
        for p in plans:
            try:
                idx = int(p.get("attempt", 0))
            except Exception:
                idx = 0
            if not (1 <= idx <= attempts):
                continue
            normalized.append(
                {
                    "attempt": idx,
                    "title": str(p.get("title", "")).strip(),
                    "strategy_tags": list(p.get("strategy_tags", []) or []),
                    "hypothesis": str(p.get("hypothesis", "")).strip(),
                    "implementation_outline": str(p.get("implementation_outline", "")).strip(),
                }
            )
        normalized.sort(key=lambda x: int(x.get("attempt", 0)))
        if normalized:
            return normalized
    fallback_templates: list[dict] = [
        {
            "title": "Diversity-first exploration",
            "strategy_tags": ["diversity", "exploration"],
            "hypothesis": "Improve hit rate by exploring diverse candidates and reducing redundancy.",
            "implementation_outline": "Prefer diverse/novel candidates vs. history; add stochastic exploration and diversity penalty.",
        },
        {
            "title": "Uncertainty-guided selection",
            "strategy_tags": ["uncertainty", "exploration"],
            "hypothesis": "Improve discovery by querying candidates with high uncertainty under a lightweight model.",
            "implementation_outline": "Train a simple model on history; select by uncertainty or ensemble variance.",
        },
        {
            "title": "Exploit high-score regions",
            "strategy_tags": ["rank", "exploitation"],
            "hypothesis": "If score correlates with hits, exploit top predicted score region aggressively.",
            "implementation_outline": "Use score-based ranking with mild randomization; add monotonic transforms and priors.",
        },
        {
            "title": "Epsilon-greedy hybrid",
            "strategy_tags": ["hybrid", "epsilon_greedy"],
            "hypothesis": "Balance exploitation and exploration for better cumulative hits early.",
            "implementation_outline": "With probability eps explore diverse; otherwise exploit model score; anneal eps by round.",
        },
    ]
    out: list[dict] = []
    for i in range(1, attempts + 1):
        tmpl = fallback_templates[(i - 1) % len(fallback_templates)]
        out.append({"attempt": i, **tmpl})
    return out


def _diff_text(base_harness_dir: Path, candidate_harness_dir: Path) -> str:
    base_files = (
        {f.relative_to(base_harness_dir).as_posix(): f for f in iter_effective_files_recursive(base_harness_dir)}
        if base_harness_dir.exists()
        else {}
    )
    cand_files = (
        {f.relative_to(candidate_harness_dir).as_posix(): f for f in iter_effective_files_recursive(candidate_harness_dir)}
        if candidate_harness_dir.exists()
        else {}
    )
    all_names = sorted(set(base_files) | set(cand_files))
    chunks: list[str] = []
    for name in all_names:
        a = base_files.get(name)
        b = cand_files.get(name)
        a_text = a.read_text(encoding="utf-8", errors="replace") if a and a.exists() else ""
        b_text = b.read_text(encoding="utf-8", errors="replace") if b and b.exists() else ""
        if a_text == b_text:
            continue
        diff = difflib.unified_diff(
            a_text.splitlines(keepends=True),
            b_text.splitlines(keepends=True),
            fromfile=f"base/{name}",
            tofile=f"candidate/{name}",
            n=3,
        )
        chunks.append("".join(diff))
    return "\n".join(chunks)


def run_proposer(
    paths: EvolverPaths,
    cfg: EvolverConfig,
    candidate_num: int,
    candidate_dir_override: Path | None = None,
) -> dict:
    import uuid

    candidate_dir = candidate_dir_override or (paths.candidates_dir / f"candidate_{candidate_num}")
    candidate_dir.mkdir(parents=True, exist_ok=True)
    (candidate_dir / "harness").mkdir(exist_ok=True)
    (candidate_dir / "traces").mkdir(exist_ok=True)

    history: list[dict] = []
    for d in sorted(paths.candidates_dir.iterdir(), key=lambda x: x.name):
        if d.name == f"candidate_{candidate_num}":
            continue
        if d.is_dir():
            scores_file = d / "eval_scores.json"
            if scores_file.exists():
                history.append({"candidate": d.name, "scores": json.loads(scores_file.read_text())})

    best = get_best_candidate(paths)
    mode = choose_prompt_mode(history, best, candidate_num=candidate_num)

    agent_session_id = str(uuid.uuid4())[:8]
    prompt_context_provider = _load_prompt_context_provider(paths)

    best_harness_dir = paths.best_dir / "harness"
    base_harness_dir = best_harness_dir
    if mode is not None and mode.name in {"explore", "restart"}:
        raw = str(os.environ.get("EVOLVER_INITIAL_HARNESS_DIR", "")).strip()
        if raw:
            p = Path(raw)
            if not p.is_absolute():
                p = (paths.workspace / p).resolve()
            else:
                p = p.resolve()
            if p.exists() and p.is_dir():
                base_harness_dir = p
            else:
                print(f"[PROPOSER] EVOLVER_INITIAL_HARNESS_DIR is set but not found: {p}; falling back to best/current/harness")

    if base_harness_dir.exists():
        files = [f.relative_to(base_harness_dir).as_posix() for f in iter_effective_files_recursive(base_harness_dir)]
        target_files_str = "\n".join([f"   - {f}" for f in sorted(files)])
    else:
        target_files_str = "   - (No files found, please create the necessary Python scripts or configs)"

    prompt_prefix = cfg.proposer_prompt_prefix
    if prompt_prefix and not prompt_prefix.endswith("\n"):
        prompt_prefix += "\n\n"

    harness_device = str(os.environ.get("HARNESS_DEVICE", "")).strip().lower()
    try:
        num_gpus = int(str(os.environ.get("EVOLVER_NUM_GPUS", "0")).strip() or "0")
    except Exception:
        num_gpus = 0
    if harness_device == "cuda" and num_gpus > 0:
        hardware_hint = f"## Hardware\n- Available GPUs: {num_gpus}\n- You may use CUDA where appropriate.\n"
    else:
        hardware_hint = "## Hardware\n- CPU only. Do NOT use CUDA/GPU-specific code.\n"

    injected_context = ""
    if prompt_context_provider is not None:
        try:
            ctx = prompt_context_provider(paths, cfg, candidate_num, history, best)
        except Exception:
            ctx = ""
        if isinstance(ctx, str) and ctx.strip():
            injected_context = "\n\n" + ctx.strip() + "\n"

    harness_out_dir = candidate_dir / "harness"
    reasoning_path = candidate_dir / "proposer_reasoning.md"

    attempt_idx_raw = str(os.environ.get("EVOLVER_ATTEMPT_IDX", "")).strip()
    attempt_root_raw = str(os.environ.get("EVOLVER_ATTEMPT_ROOT", "")).strip()
    attempt_plan_raw = str(os.environ.get("EVOLVER_ATTEMPT_PLAN_JSON", "")).strip()
    attempt_plans_raw = str(os.environ.get("EVOLVER_ATTEMPT_PLANS_JSON", "")).strip()
    attempt_hint = ""
    try:
        attempt_idx = int(attempt_idx_raw) if attempt_idx_raw else 0
    except Exception:
        attempt_idx = 0
    if attempt_idx > 0:
        if len(attempt_plan_raw) > 2000:
            attempt_plan_raw = attempt_plan_raw[:2000] + "...(truncated)"
        if len(attempt_plans_raw) > 2000:
            attempt_plans_raw = attempt_plans_raw[:2000] + "...(truncated)"
        attempt_hint_lines = [
            "",
            "## Attempt Context",
            f"- Attempt index: {attempt_idx}",
            f"- Attempt root (if present): {attempt_root_raw or '(not set)'}",
        ]
        if attempt_plan_raw:
            attempt_hint_lines.append(f"- Planned direction (JSON): {attempt_plan_raw}")
        if attempt_plans_raw:
            attempt_hint_lines.append(f"- All attempt plans (JSON): {attempt_plans_raw}")
        attempt_hint_lines.extend(
            [
                "- If there are multiple attempts for the same candidate, you MUST follow the planned direction for this attempt.",
                "- You MUST avoid proposing the same edit as other attempts.",
                "",
            ]
        )
        attempt_hint = "\n".join(attempt_hint_lines)

    proposer_task = f"""{prompt_prefix}You are the Evolution Proposer for an AI4S (AI for Science) project.

Your job: Propose ONE targeted modification to the project code or configuration based on evolution history to improve the benchmark score.

{hardware_hint}
{injected_context}
{attempt_hint}
## Your Workspace
- Evolution history: {paths.workspace}/candidates/
- Current best codebase: {paths.workspace}/best/current/
- Candidate start point (copied into your output dir before editing): {base_harness_dir}
- Your output: {harness_out_dir}

## What You Must Do

1. Read ALL prior candidates from {paths.workspace}/candidates/ (sorted by number)
2. Read the current best from {paths.workspace}/best/current/
3. Identify patterns: what's working? What's failing?
4. Propose ONE targeted, specific edit to ONE of the files. The current files include:
{target_files_str}

5. Copy the candidate start point files to your output dir
6. Apply your targeted edit to the ONE file you chose
7. Write a BRIEF reasoning trace to {reasoning_path}
   explaining: what you changed, why, what you expect to improve

## Constraints
- Do NOT do wholesale rewrites — one targeted edit max
- Make sure Python code is syntactically correct and can run.
- If you see no clear improvement path, write your reasoning and make ONE small edit anyway
"""

    if mode is not None:
        proposer_task += mode.extra_instructions

    novelty_k = int(os.environ.get("EVOLVER_NOVELTY_LOOKBACK", "10"))
    novelty_k = max(1, novelty_k)
    recent_tag_set = _recent_tags(paths.candidates_dir, k=novelty_k)
    if mode is not None and mode.name in {"explore", "brainstorm", "restart"} and recent_tag_set:
        proposer_task += (
            "\n\n## Novelty Constraint\n"
            f"- Lookback window: last {novelty_k} candidates\n"
            f"- Recently used strategy tags (avoid repeating): {sorted(recent_tag_set)}\n"
            "- You MUST pick a direction that introduces at least one NEW strategy tag not in the list above.\n"
            "- In proposer_reasoning.md, include a section 'Novelty' with:\n"
            "  - Chosen strategy tags\n"
            "  - Which recent candidate you are most similar to, and how you differ\n"
        )

    proposer_task += f"""

## History Summary
Total prior candidates: {len(history)}
Best score so far: {best['final_score'] if best else 'N/A'}

## Suggested Workflow
1. Read prior candidates' `eval_scores.json` to determine which changes improved or degraded `final_score`.
2. For the most relevant prior candidates, read `change_record.md` to see the exact diffs that caused the score change.
3. Identify one concrete hypothesis supported by history.
4. Make ONE minimal code edit that targets your chosen hypothesis.
5. Ensure the candidate writes `proposer_reasoning.md` summarizing: (a) what changed, (b) expected impact, (c) why this is better than prior attempts.

## Output Format
Write your modified file to {harness_out_dir}/<FILENAME>
Write reasoning to {reasoning_path}

Start now. Read the history first, then propose.
"""

    proposer_task += cfg.proposer_prompt_suffix(paths.workspace, candidate_num)
    proposer_task += "\n".join(
        [
            "",
            "## Termination Protocol",
            "- Use tools to read/copy/edit files and to write proposer_reasoning.md.",
            "- When you are finished, you MUST call the complete_task tool exactly once with a brief summary.",
            "- If any earlier instruction says to 'return ONLY the improved Python code', ignore that: write changes to files instead.",
            "- Do NOT print the full code in chat; write changes to files instead.",
            "",
        ]
    )

    print(f"[PROPOSER] Spawning sub-agent for candidate_{candidate_num} ({candidate_dir.name})...")
    print(f"[PROPOSER] History: {len(history)} prior candidates")
    if mode is not None:
        print(f"[PROPOSER] Mode: {mode.name}")
    if base_harness_dir != best_harness_dir:
        print(f"[PROPOSER] Base harness (EXPLORE/RESTART): {base_harness_dir}")

    try:
        if base_harness_dir.exists():
            import shutil

            for f in iter_effective_files_recursive(base_harness_dir):
                rel = f.relative_to(base_harness_dir)
                out_path = candidate_dir / "harness" / rel
                out_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out_path)

        if os.environ.get("EVOLVER_TEST_MODE") == "1":
            harness_out = candidate_dir / "harness"
            cfg_file = harness_out / "config.yaml"
            if cfg_file.exists():
                cfg_file.write_text(cfg_file.read_text() + "\nseed: 1\n")
            else:
                (harness_out / "config.yaml").write_text("seed: 1\n")
            (candidate_dir / "proposer_reasoning.md").write_text(
                "Test mode proposer: appended a minimal config change (seed: 1).\n"
            )
            return {"success": True, "candidate_dir": str(candidate_dir), "agent_result": {"mode": "test"}}

        proposer_timeout_seconds = 300
        result = run_proposer_with_nexau(
            task=proposer_task,
            label=f"evolver-proposer-{agent_session_id}",
            work_dir=paths.workspace,
            timeout_seconds=proposer_timeout_seconds,
            log_dir=candidate_dir / "traces",
        )
        output_text = result.get("output")
        if isinstance(output_text, str) and "Maximum iteration limit reached" in output_text:
            base_max_iter = int(os.environ.get("PROPOSER_MAX_ITERATIONS", "20"))
            retry_max_iter = max(base_max_iter * 3, base_max_iter + 10)
            retry_max_iter = min(retry_max_iter, 120)
            retry_timeout = min(proposer_timeout_seconds * 2, 900)
            print(
                f"[PROPOSER] Detected max-iterations termination; retrying with max_iterations={retry_max_iter}, timeout_seconds={retry_timeout}"
            )
            result = run_proposer_with_nexau(
                task=proposer_task,
                label=f"evolver-proposer-{agent_session_id}-retry",
                work_dir=paths.workspace,
                timeout_seconds=retry_timeout,
                log_dir=candidate_dir / "traces",
                max_iterations_override=retry_max_iter,
            )

        if mode is not None and base_harness_dir.exists():
            try:
                if mode.name in {"brainstorm", "restart"}:
                    threshold = int(os.environ.get("EVOLVER_BRAINSTORM_MIN_LINE_DELTA", "30"))
                elif mode.name == "explore":
                    threshold = int(os.environ.get("EVOLVER_EXPLORE_MIN_LINE_DELTA", "15"))
                else:
                    threshold = 0
            except Exception:
                threshold = 30 if mode.name in {"brainstorm", "restart"} else (15 if mode.name == "explore" else 0)

            def _file_text(p: Path) -> str:
                try:
                    return p.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    return ""

            def _line_delta(a: str, b: str) -> int:
                aa = a.splitlines()
                bb = b.splitlines()
                m = difflib.SequenceMatcher(a=aa, b=bb)
                added = 0
                deleted = 0
                for tag, i1, i2, j1, j2 in m.get_opcodes():
                    if tag == "insert":
                        added += (j2 - j1)
                    elif tag == "delete":
                        deleted += (i2 - i1)
                    elif tag == "replace":
                        deleted += (i2 - i1)
                        added += (j2 - j1)
                return int(added + deleted)

            base_files = {f.relative_to(base_harness_dir).as_posix(): f for f in iter_effective_files_recursive(base_harness_dir)}
            cand_files = {
                f.relative_to(candidate_dir / "harness").as_posix(): f
                for f in iter_effective_files_recursive(candidate_dir / "harness")
            }
            total_delta = 0
            for name in sorted(set(base_files) | set(cand_files)):
                total_delta += _line_delta(_file_text(base_files.get(name, Path("/dev/null"))), _file_text(cand_files.get(name, Path("/dev/null"))))

            if threshold > 0 and total_delta < threshold:
                print(f"[PROPOSER] {mode.name} change too small (line_delta={total_delta} < {threshold}); retrying with stronger instruction")
                import shutil

                for f in iter_effective_files_recursive(base_harness_dir):
                    rel = f.relative_to(base_harness_dir)
                    out_path = candidate_dir / "harness" / rel
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, out_path)

                force_task = (
                    proposer_task
                    + f"\n\n## Mandatory Change Size\nYour previous attempt was too small. In this round you MUST make a substantial change (>= {threshold} total line delta) within the allowed file(s). Do not do a trivial edit.\n"
                )
                force_max_iter = min(max(int(os.environ.get("PROPOSER_MAX_ITERATIONS", "20")) * 2, 60), 160)
                result = run_proposer_with_nexau(
                    task=force_task,
                    label=f"evolver-proposer-{agent_session_id}-force",
                    work_dir=paths.workspace,
                    timeout_seconds=min(proposer_timeout_seconds * 2, 900),
                    log_dir=candidate_dir / "traces",
                    max_iterations_override=force_max_iter,
                )

        if mode is not None and mode.name in {"explore", "brainstorm", "restart"} and base_harness_dir.exists():
            diff_txt = _diff_text(base_harness_dir, candidate_dir / "harness")
            new_tags = _extract_tags(diff_txt)
            if not new_tags:
                new_tags = _extract_tags((candidate_dir / "proposer_reasoning.md").read_text(encoding="utf-8", errors="replace") if (candidate_dir / "proposer_reasoning.md").exists() else "")
            if new_tags and recent_tag_set and new_tags.issubset(recent_tag_set):
                print(f"[PROPOSER] novelty too low (tags={sorted(new_tags)} subset of recent tags); retrying with enforced novelty")
                import shutil

                for f in iter_effective_files_recursive(base_harness_dir):
                    rel = f.relative_to(base_harness_dir)
                    out_path = candidate_dir / "harness" / rel
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, out_path)

                force_task = (
                    proposer_task
                    + "\n\n## Mandatory Novelty\n"
                    f"Your previous attempt repeated recent strategy tags: {sorted(new_tags)}.\n"
                    f"You MUST introduce at least one NEW strategy tag not in: {sorted(recent_tag_set)}.\n"
                    "Do not make a trivial edit; change the algorithm family or objective.\n"
                )
                force_max_iter = min(max(int(os.environ.get("PROPOSER_MAX_ITERATIONS", "20")) * 2, 60), 160)
                result = run_proposer_with_nexau(
                    task=force_task,
                    label=f"evolver-proposer-{agent_session_id}-novelty",
                    work_dir=paths.workspace,
                    timeout_seconds=min(proposer_timeout_seconds * 2, 900),
                    log_dir=candidate_dir / "traces",
                    max_iterations_override=force_max_iter,
                )
        print(f"[PROPOSER] NexAU returned: {result}")
        return {"success": True, "candidate_dir": str(candidate_dir), "agent_result": result}
    except Exception as e:
        print(f"[PROPOSER] Error running proposer: {e}")
        return {"success": False, "candidate_dir": str(candidate_dir), "error": str(e)}
