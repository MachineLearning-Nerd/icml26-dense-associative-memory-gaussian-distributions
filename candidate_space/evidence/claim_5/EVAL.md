# Claim 5 evaluator guide

Verdict: **VERIFIED**.

Run the fixed command from the repository root:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

The command exits nonzero if any accepted claim regresses. Claim 5
downloads and hash-checks Text8 and the deleted executed author notebook,
trains `N=10000`, `d=50` spherical embeddings from the recovered author
configuration, and evaluates 100 queries for each of seeds 42, 43, and
44 on the author's 20-value beta grid.

The decisive transition rows are in `raw/phase_sweeps.csv`. At beta
7.85, the retrieval rates are 38%, 32%, and 30%, with Wilson 95% upper
bounds 47.8%, 41.7%, and 39.6%. At beta 16.24, all three rates are 100%,
with a 96.3% Wilson lower bound. The recovered executed author curve is
0%, 31%, and 98% at beta 7.85, 11.29, and 16.24.

The vectorized update agrees with an independent scalar loop to
`3.10e-15`. The beta-zero uniform-weight control retrieves 0%.

Primary files:

- `claim_contract.json`
- `source_audit.md`
- `method.md`
- `verifier.py`
- `raw/result.json`
- `raw/phase_sweeps.csv`
- `raw/query_results.csv`
- `independent_checker.json`
- `negative_control.json`
- `runtime.json`
- `limitations.md`
