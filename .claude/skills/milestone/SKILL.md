---
name: milestone
description: Start a build milestone from docs/PLAN.md (M0 to M5)
argument-hint: "[M0-M5]"
disable-model-invocation: true
---

Start milestone $ARGUMENTS.

1. Read `CLAUDE.md`, the $ARGUMENTS section of `docs/PLAN.md`, and `docs/PROGRESS.md`.
2. Check that previous milestones are marked done. If not, say so and stop.
3. Present a plan: files to create or change, tests to write, decisions that need an ADR,
   and any open question. Flag anything that is an OWNER TASK.
4. Wait for approval. Do not edit files before approval.
5. Implement in small steps. Run `make lint` and `make test` after each step.
6. When done, tell the owner to run `/close-milestone $ARGUMENTS`.
