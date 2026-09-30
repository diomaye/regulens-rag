---
name: close-milestone
description: Verify a milestone's definition of done and governance checklist, then commit
argument-hint: "[M0-M5]"
disable-model-invocation: true
---

Close milestone $ARGUMENTS.

## Definition of done
Check every "Done when" item for $ARGUMENTS in `docs/PLAN.md`. Show evidence (command output
or file path) for each. If any item fails, list it and stop without committing.

## Quality
- `make lint` and `make test` pass.
- New public functions have type hints and docstrings.

## Governance checklist
- No secrets in the diff or working tree (keys, tokens, connection strings with passwords).
- No client, employer or personal data added.
- `evals/golden_set.jsonl` and `evals/thresholds.yaml` unchanged by Claude.
- New downloaded sources recorded in `data/manifest.csv` with SHA-256.
- Logging includes version fields where generation code changed.
- ADRs written for decisions made in this milestone.

## Wrap-up
1. Update `docs/PROGRESS.md` (status, notes, open questions).
2. Summarize: what was built, key trade-offs and why, what the owner should learn or review.
3. Propose a conventional commit message and commit after approval.
