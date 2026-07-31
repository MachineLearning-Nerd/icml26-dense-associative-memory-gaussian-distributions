# Claim 4 evaluation

Verdict: **VERIFIED**

Run the cumulative verifier with:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

The exact-scale run used `N=10000`, `d=50`, 7,500 queries, three
deterministic seeds, beta values 1 and 0.1, and perturbation radii
`1/sqrt(beta N)` and `100/sqrt(beta N)`. At beta 1, all 45,000
seed/radius queries were below `1e-6` after one update. At beta 0.1,
none of the 45,000 queries were below `1e-6` after three updates.

Review `raw/result.json` for every final query error and
`raw/trajectories.csv` for the compact iteration summaries. The
independent scalar-loop update agreed within
`1.0130785099704553e-15`; the beta-zero uniform-weight control retrieved
zero queries.

The verifier exits nonzero when any claim check fails because the
cumulative runner propagates verifier assertions. Current code is
`verifier.py`; no earlier toy verifier is current evidence.
