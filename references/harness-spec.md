# Harness Spec — What Constitutes the Evolvable Surface

This document defines what files make up the evolvable surface for this runner.

## Core Harness Files

### Default Convention

The evolver reads and writes files under:

- Current best: `$EVOLVER_WORKSPACE/best/current/harness/`
- Candidate output: `$EVOLVER_WORKSPACE/candidates/candidate_N/harness/`

Files inside `harness/` can be any types needed for your AI4S task (for example: `.py`, `.yaml`, `.json`, `.txt`).

## Non-Harness Files (NOT Evolution Targets)

These files are typically not part of the evolvable surface:
- The workspace log files (`evolution_log.jsonl`, `candidate_N/traces/`, `candidate_N/backup/`)
- Any secret material (API keys, tokens, passwords)

## What Makes a Good Harness

From the Meta-Harness paper, a good harness:
1. **Gives the model rich, selective access to experience** — not compressed summaries
2. **Is executable code, not just text** — structured configs that the agent can reason about
3. **Has coherent algorithmic structure** — not hard-coded brittle solutions
4. **Exposes what matters for downstream decisions** — traces of failure modes

For AI4S tasks:
- Keep changes small and targeted (one file per iteration) to preserve attribution
- Make configs explicit and machine-readable (e.g., YAML/JSON) when possible
- Prefer reproducible changes (seed, hyperparameters, model wiring) over ad-hoc edits

## File Naming & Location Convention

When the proposer creates a new candidate harness:
```
$EVOLVER_WORKSPACE/candidates/candidate_N/harness/
  <task files...>
```

## Anti-Patterns (What NOT to Propose)

1. **Large refactors** that change many files at once
2. **Adding secrets** into the workspace or configs
3. **Overfitting** to a single benchmark script output format or scenario wording
