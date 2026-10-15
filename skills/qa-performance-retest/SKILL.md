---
name: qa-performance-retest
description: "Plan and evaluate regression/performance retests of approved fixes against comparable baselines and stability criteria."
---

# qa-performance-retest

Read `references/CONTRACT.md` and `references/ENGINEERING.md`. Read approved proposal, change receipt, workload/profile and baseline. Check comparability of build/config/data/environment capacity/transaction mix/collection windows and record confounders. Confirm a new complete run profile before invoking the appropriate executor.
Evaluate original reproduction/mechanism, latency distributions/percentiles with sample counts, throughput/errors/saturation, negative/regression checks and sustained stability. Record before/after values with units, not unsupported percentage promises. Unavailable or incomparable measurements remain unknown/inconclusive. Retesting does not itself authorize deployment/rollback. Write engineering/retests with acceptance outcomes, evidence and remaining RCA-source gaps; hand to RCA/reporting for conclusion updates.
