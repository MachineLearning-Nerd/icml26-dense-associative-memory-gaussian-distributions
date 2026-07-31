# Claim 6 — non-commuting one-step convergence: FALSIFIED

Canonical source: arXiv:2509.23162v1, Section 6.2.3 and Figure 8.
The later v2 removes this experiment; this page tests the exact v1
claim scored by the live judge.

## Exact contract

Sample `N=1000` Gaussian measures in `d=10` on the stated
Bures-Wasserstein sphere with full-rank, non-commuting SPD
covariances. Perturb 750 stored measures at radii
`1/sqrt(beta N)` and `100/sqrt(beta N)`, then apply Algorithm 1.
The paper text says suitable beta gives one-step convergence.

Falsification requires more than observing nonzero error: all sphere,
SPD, non-commutation, scale, and radius assumptions must pass; both
the paper's full-rank perturbation law and an alternative rank-one PSD
law must contradict one-step convergence; an independent
implementation and a failing beta-zero control must pass; and the
paper's own figure must independently contradict the prose.

## Result

All predicates passed across deterministic seeds `20260730`,
`20260731`, and `20260732`.

| condition | seed-level mean W2 after one update |
| --- | --- |
| beta 1, `r` | `0.001847`, `0.002001`, `0.002039` |
| beta 1, `100r` | `0.5650`, `0.5954`, `0.5910` |
| beta 0.1, `r` | `2.8659`, `2.8632`, `2.8646` |
| beta 0.1, `100r` | `3.2971`, `3.3173`, `3.3395` |
| beta 1, `100r`, rank-one PSD law | `0.3660`, `0.3581`, `0.3773` |

For beta 1 at `100r`, mean W2 after five updates is `0.1736`,
`0.1839`, and `0.1272`. Across all 2,250 queries, 0% reach `1e-6`;
only 26.1–31.7% reach `1e-3`. Nearest-target identity is much weaker:
94.4–96.3% is not convergence to the stored Gaussian.

The hash-pinned v1 Figure 8(b) independently digitizes to:

```text
iteration: 0       1       2       3       4       5
mean W2:   3.1538  0.6205  0.2257  0.1658  0.1580  0.1580
```

That plot and the authors' deleted executed notebook (final mean
`0.157643`, 521/750 nearest targets) agree with this falsification.
The paper's empirical data therefore contradict its one-step prose.
This does not falsify the broader update rule or every possible
non-commuting distribution.

The fixed command is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

The cumulative runner exits nonzero unless this assumption-satisfying
counterexample and every supporting predicate pass.

Downloadable evidence:

- [verifier source](../../evidence/claim_6/verifier.py)
- [raw result](../../evidence/claim_6/raw/result.json)
- [trajectory CSV](../../evidence/claim_6/raw/trajectories.csv)
- [claim contract](../../evidence/claim_6/claim_contract.json)
- [source audit](../../evidence/claim_6/source_audit.md)
- [paper-figure audit](../../evidence/claim_6/source_figure_audit.json)
- [independent checker](../../evidence/claim_6/independent_checker.json)
- [negative control](../../evidence/claim_6/negative_control.json)
- [runtime](../../evidence/claim_6/runtime.json)
- [evaluator guide](../../evidence/claim_6/EVAL.md)

Run `eb085eac-056a-4005-add9-816058a8eab0` at Git SHA
`11f0d0dafdbf612f997d383fb6e92345f334df20` on HF
`cpu-upgrade`, provisioned as 8 vCPUs and 32 GB. The container exposed
64 logical/affinity CPUs and used a 64-thread limit. Verifier runtime
was `3389.079 s`; total job `57m25s`; peak RSS `1,543,072 KiB`.

## Limitations

This is a valid counterexample to the exact empirical one-step claim:
the tested generators satisfy the source assumptions and the paper's
own plotted run supplies an independent counterexample. It is not a
claim that every non-commuting distribution fails to retrieve.
