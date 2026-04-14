---
name: meta-harness-evolver
description: Meta-Harness-style evolution loop for AI4S / agentic codebases. Reads prior candidates from $EVOLVER_WORKSPACE, proposes one targeted code/config edit via NexAU, evaluates via a user-provided evaluate program, logs results, and posts a summary to Feishu.
---

# Meta-Harness Evolver

## What This Does

Implements a **Meta-Harness**-style outer loop. Each run:

1. **Reads** the current best + all prior candidates in the evolution workspace
2. **Proposes** one targeted modification via a NexAU coding agent
3. **Evaluates** the candidate via `--evaluate-script` (bash/py/executable) which prints JSON as the last line
4. **Logs** the candidate harness + scores + execution traces to the evolution filesystem
5. **Posts** a summary report to Feishu (Lark)

## The Meta-Harness Loop

```
Proposer Agent ──(filesystem access)──► Hoss Workspace
      ▲                                   │
      │                          propose harness
      │                                   ▼
      │                          Evaluate on benchmark
      │                                   ▼
log ───┴── store: code + scores + traces ──► $EVOLVER_WORKSPACE/
```

## Quick Start

Run from repo root:

```bash
bash meta-harness-evolver/scripts/example_run_evolution.sh
```

## Directory Structure

```
$EVOLVER_WORKSPACE/
├── best/                  # Best harness found so far
│   └── current/
├── candidates/            # All evaluated harnesses
│   └── candidate_N/       # One dir per candidate
│       ├── harness/      # The proposed config files (SOUL.md, etc.)
│       ├── eval_scores.json
│       └── traces/        # Execution traces
├── benchmark/             # Evaluation tasks + scorer
│   └── scenarios/         # ~20 diverse task scenarios
├── proposer/              # Proposer's workspace
│   └── logs/              # Proposer's own reasoning traces
└── evolution_log.jsonl    # Full run history
```

## What Can Be Evolved

Any files inside `candidate_N/harness/` (e.g., `model.py`, `train.py`, `config.yaml`). Do not commit secrets into this workspace.

## The Evolution Algorithm

1. **Seed**: Start with Hoss's current configs as iteration 0
2. **Propose**: Proposer reads full history from `$EVOLVER_WORKSPACE/candidates/`, identifies failure patterns, proposes 1 targeted edit
3. **Validate**: Lightweight import/syntax check before running full benchmark
4. **Evaluate**: Run proposed harness against all 20 benchmark scenarios, score each
5. **Log**: Store candidate harness + scores + proposer reasoning traces
6. **Select**: Pareto frontier over (performance, simplicity) — proposer decides which candidates to keep exploring from
7. **Repeat**: Next night's proposer can read ALL prior candidates to build on good ideas

### Key Insight from the Paper
The **skill text is the strongest lever** — it steers the proposer. Iterating on the proposer's prompt/role description had more effect than changing iteration count or population size.

## Evaluation

Evaluation is delegated to a user-provided program via `--evaluate-script`. It must accept `<candidate_dir>` and print JSON as the last stdout line.

Default benchmark has **20 scenarios** across categories:
- **Memory**: Recall, update, synthesize from memory files
- **Code**: Write, review, debug code tasks
- **Coordination**: Spawn sub-agents, synthesize results
- **Research**: Web search, fetch, summarize, synthesize
- **Communication**: Draft emails, Feishu messages
- **Quality**: Spot errors, inconsistencies, broken links

Each scenario has:
- A concrete task description
- Expected outcome criteria
- A scoring rubric (0-3 per scenario: fail / partial / pass / excellent)

## The Proposer Agent

The proposer is a **coding-agent sub-agent** (default: coder) that:
- Reads all prior candidates from `~/hoss-evolution/candidates/` via filesystem ops
- Identifies patterns in failed/succeeded candidates
- Proposes targeted, specific edits (NOT wholesale rewrites)
- Writes proposed configs to the new candidate directory
- Logs its reasoning trace so future iterations can build on it

### Proposer Prompt

The proposer's role is defined by the task prompt in `scripts/run_evolution.py` and should prefer targeted edits over full rewrites.

## Workflow Steps

### Step 1: Read Prior Candidates
```bash
# List all prior candidates
ls "$EVOLVER_WORKSPACE/candidates/"

# Read best candidate
cat ~/hoss-evolution/best/current/eval_scores.json

# Read history log
tail -20 "$EVOLVER_WORKSPACE/evolution_log.jsonl"
```

### Step 2: Run Proposer
```bash
# The sub-agent proposer reads ~/hoss-evolution/ and proposes
# This is triggered by openclaw run with this skill loaded
```

### Step 3: Validate Before Benchmark
```bash
# Quick syntax check
bash ~/hoss-evolution/scripts/validate.sh <candidate_dir>
```

### Step 4: Run Evaluation
```bash
python3 meta-harness-evolver/scripts/run_evolution.py --evaluate-script /path/to/evaluate.sh
```

### Step 5: Log Results
```bash
# Scores + traces written to candidate dir automatically
# Evolution log updated
```

### Step 6: Post to Feishu
```bash
python3 meta-harness-evolver/scripts/post_to_research.py <candidate_num> <candidate_dir> <score> <proposer_success>
```

## Scoring

Final score = weighted average across scenarios:
- Memory tasks: 25%
- Code tasks: 25%
- Coordination: 15%
- Research: 20%
- Communication: 10%
- Quality: 5%

Results are tracked as a Pareto frontier: for each candidate, log both score and "complexity" (size/diff of changes). Simpler harnesses that score equally get priority.

## Resources

- [references/harness-spec.md](references/harness-spec.md) — Full spec of what constitutes Hoss's harness, what can/cannot be modified
- [references/benchmark-design.md](references/benchmark-design.md) — How to design benchmark scenarios, scoring rubrics, how to add new scenarios
- [references/evolution-logic.md](references/evolution-logic.md) — Detailed evolution algorithm, parent selection, Pareto frontier logic
- [scripts/run_evolution.py](scripts/run_evolution.py) — Main entry point, runs the full loop
- [scripts/propose_harness.py](scripts/propose_harness.py) — The proposer sub-agent task definition
- [scripts/evaluate-example.py](scripts/evaluate-example.py) — Benchmark runner (example)
- [scripts/post_to_research.py](scripts/post_to_research.py) — Feishu reporter

## Notes

- If the proposer fails to produce a valid candidate, the iteration is skipped
- Keep evaluation scenarios diverse enough that no single strategy can game all of them
