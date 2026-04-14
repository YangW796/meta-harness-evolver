# ⚡ Meta-Harness Evolver

**A Meta-Harness-style outer-loop runner for AI4S / agentic codebases.**

> *"The harness around a fixed LLM can produce a 6× performance gap on the same benchmark."* — [Meta-Harness Paper](https://yoonholee.com/meta-harness/)

This project runs an outer-loop optimization — reading prior candidates, proposing targeted code/config modifications, evaluating against a benchmark, logging results, and iterating.

---

## What Is This?

Meta-Harness is an outer-loop system that searches over **harness code** — the configuration files that wrap an LLM (prompts, context management, memory, tools). Unlike text optimizers that compress feedback to scalar scores, Meta-Harness gives a coding agent **full filesystem access** to all prior candidates' source, scores, and execution traces.

**Key insight:** The richest signal isn't a score — it's the **execution trace**. The proposer reads what actually happened, traces failures to root causes, and proposes targeted edits.

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│  Proposer Agent ──(filesystem access)──► $EVOLVER_WORKSPACE/
│         ▲                                           │
│         │                               propose harness
│         │                                           ▼
│         │                               Evaluate on benchmark
│         │                                           ▼
│  log ───┴── store: code + scores + traces ──► candidates/
└─────────────────────────────────────────────────────────┘
```

Each run:

1. **Read** — Proposer reads all prior candidates from the evolution filesystem
2. **Propose** — Identifies failure patterns, proposes 1 targeted edit (any file types)
3. **Validate** — Lightweight syntax/constraint check
4. **Evaluate** — Run benchmark (~20 diverse scenarios)
5. **Log** — Store candidate + scores + proposer reasoning traces
6. **Post** — Summary posted to Feishu (Lark)

---

## What Can Be Evolved

The evolver treats `candidate_N/harness/` as the "mutable surface". It can contain any files relevant to your AI4S task (e.g. `model.py`, `train.py`, `config.yaml`).

---

## Quick Start

1. Create and configure `meta-harness-evolver/.env` (not committed). At minimum:
   - `EVOLVER_WORKSPACE=./hoss-evolution`
   - `NEXAU_HOME=/path/to/NexAU`
   - `LLM_MODEL / LLM_BASE_URL / LLM_API_KEY` (for the NexAU proposer)
   - `FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_RECEIVE_ID(_TYPE)` (for Feishu posting)

2. Seed the workspace:
   - Put your baseline code/config into: `$EVOLVER_WORKSPACE/best/current/harness/`
   - Optional baseline candidate: `$EVOLVER_WORKSPACE/candidates/candidate_0/harness/`

3. Run:

```bash
bash meta-harness-evolver/scripts/example_run_evolution.sh
```

---

## Directory Structure

```
$EVOLVER_WORKSPACE/
├── candidates/              # All evaluated candidates
│   └── candidate_N/
│       ├── harness/          # Proposed config files
│       ├── eval_scores.json # Benchmark scores
│       ├── traces/           # Execution traces
│       └── proposer_reasoning.md
├── best/
│   └── current/              # Best harness found so far
│       ├── harness/
│       └── eval_scores.json
├── benchmark/
│   └── scenarios/            # ~20 diverse eval scenarios
└── evolution_log.jsonl       # Full run history
```

---

## Benchmark

The default benchmark has **20 scenarios** across 6 categories:

| Category | Weight | Examples |
|----------|--------|---------|
| Memory | 25% | Recall from logs, update MEMORY.md, synthesize across files |
| Code | 25% | Write scripts, debug, security review |
| Research | 20% | Web search + synthesize, fetch and summarize |
| Coordination | 15% | Spawn sub-agents, handle failures |
| Communication | 10% | Draft messages, handle pushback |
| Quality | 5% | Spot broken links, catch inconsistencies |

Each scenario is scored 0-3 (fail / partial / pass / excellent). Final score = weighted average × 100.

---

## The Proposer Agent

The proposer is a **coding-agent sub-agent** that:
- Reads all prior candidates via filesystem ops (grep, cat)
- Identifies patterns in success/failure
- Proposes **1 targeted edit** — not a wholesale rewrite
- Logs its reasoning trace for next iteration

Key constraint: **the skill text is the strongest lever**. Iterating on the proposer's role description had more effect than iteration count or population size.

---

## The Meta-Harness Paper

> *"Meta-Harness improves over Agentic Context Engineering (ACE) by 7.7 points while using 4× fewer context tokens."*

This skill implements the core ideas from:

**Meta-Harness: End-to-End Optimization of Model Harnesses**  
Yoonho Lee, Roshen Nair, Qizheng Zhang, Omar Khattab, Kangwook Lee, Chelsea Finn  
Stanford / MIT / KRAFTON  

- [Paper](https://yoonholee.com/meta-harness/paper.pdf)
- [Project Page](https://yoonholee.com/meta-harness/)
- [Artifact](https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact)

---

## Adapting for Your Task

This runner is agent/task-agnostic:

1. **Update `references/harness-spec.md`** — define what files constitute your mutable surface
2. **Replace evaluation** — point `--evaluate-script` to your own benchmark program
3. **Adjust weights** — if coordination matters more than code for your use case
4. **Update proposer prompt** — `scripts/run_evolution.py` proposer_task — describe your task and constraints

---

## Example Feishu Output

```
Meta-Harness Evolution — Report

Candidate: candidate_7
Score: 72.3/100 🔺 +3.1 vs best
Proposer: SUCCESS

What Changed:
  ~ model.py (+12 lines)
  ~ config.yaml (+3 lines)

Proposer's Reasoning:
  "candidate_5 and candidate_6 both failed on memory_2
   (updating MEMORY.md). Their HEARTBEAT.md didn't prioritize
   memory health checks. Added memory consistency validation."

Recent History:
  • candidate_6: 69.2
  • candidate_5: 68.1
  • candidate_4: 71.0
```

---

## References

- [Harness Spec](references/harness-spec.md) — What files make up an agent's harness
- [Benchmark Design](references/benchmark-design.md) — How to build/extend the eval suite
- [Evolution Logic](references/evolution-logic.md) — Algorithm details, Pareto frontier, proposer patterns

---

## Contributing

Issues and PRs welcome. If you adapt this for a different agent framework, we'd love to hear about it — open an issue or drop a note in the discussion.

---

## License

MIT — do what you want with it.
