---
name: eval
description: Run the eval suite, compare with the last run and thresholds, and explain the results
argument-hint: "[smoke|full]"
disable-model-invocation: true
---

Run the $ARGUMENTS eval suite (default: smoke).

1. Run `make eval-smoke` for smoke, `make eval` for full.
2. Compare with the most recent previous file in `evals/results/`.
3. Report a table: metric, previous, current, threshold, pass/fail. Split by language.
4. For every regression or missed threshold, give the likely cause and a concrete fix to the
   system (retrieval, chunking, prompt, refusal logic).
5. Never edit `evals/thresholds.yaml` or `evals/golden_set.jsonl`.
