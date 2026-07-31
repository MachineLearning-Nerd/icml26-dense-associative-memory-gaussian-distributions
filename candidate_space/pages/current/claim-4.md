# Claim 4 — exact synthetic temperature separation: VERIFIED

Canonical source: arXiv:2509.23162v1,
[Section 4.1](https://ar5iv.labs.arxiv.org/html/2509.23162v1#S4.SS1),
Figure 3, Algorithm 2, and Appendix Figure 6.

## Exact contract

Generate `N=10000` commuting Gaussian memories in `d=50` with
`lambda_min=1` and `lambda_max=1.1`. Perturb 7,500 memories at each
radius

```text
1/sqrt(beta N), 100/sqrt(beta N)
```

and apply Algorithm 1. At the plotted `1e-6` threshold, beta 1 should
retrieve the targets while beta 0.1 should not.

Algorithm 2 specifies `R^2=d(lambda_min+lambda_max)`, which this
verification follows. Section 4.1 prints `R` rather than `R^2`; the
source audit records that ambiguity. The paper does not state how to
divide the query perturbation between mean and covariance, so squared
Wasserstein distance is split equally.

## Result

The verifier used the exact paper scale with three deterministic
seeds (`20260730`, `20260731`, `20260732`). Each table cell contains
7,500 queries.

| beta | radius | seed-level retrieval after one update | mean W2 error after three updates |
| ---: | ---: | ---: | ---: |
| `1` | `r=0.01` | `100%, 100%, 100%` | `2.55e-18, 1.18e-16, 2.58e-18` |
| `1` | `100r=1` | `100%, 100%, 100%` | `2.55e-18, 1.18e-16, 2.58e-18` |
| `0.1` | `r=0.0316228` | `0%, 0%, 0%` | `6.97151, 6.97128, 6.97143` |
| `0.1` | `100r=3.16228` | `0%, 0%, 0%` | `6.98013, 6.97719, 6.97928` |

All Algorithm 2 count, dimension, spectrum, trace, mean-radius, and
commuting-basis invariants passed. A scalar-loop implementation agreed
with the vectorized update within `1.0130785099704553e-15`. A beta-zero
uniform-weight control retrieved 0% for every seed.

The fixed command is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

The cumulative runner exits nonzero if this verifier rejects any
predicate.

Downloadable evidence:

- [verifier source](../../evidence/claim_4/verifier.py)
- [raw per-query result](../../evidence/claim_4/raw/result.json)
- [trajectory CSV](../../evidence/claim_4/raw/trajectories.csv)
- [claim contract](../../evidence/claim_4/claim_contract.json)
- [source audit](../../evidence/claim_4/source_audit.md)
- [independent checker](../../evidence/claim_4/independent_checker.json)
- [negative control](../../evidence/claim_4/negative_control.json)
- [runtime](../../evidence/claim_4/runtime.json)
- [evaluator guide](../../evidence/claim_4/EVAL.md)

Run `1da1893a-85e4-42f7-9085-541596e0b322` at Git SHA
`5ad638648cfdf45e7a5ea2d82c6b9ae28ffb61aa` on HF
`cpu-upgrade`, provisioned as 8 vCPUs and 32 GB. The container exposed
64 logical/affinity CPUs and used a 64-thread limit. Verifier runtime was
`513.4822568770032 s`; total job runtime `568 s`; peak RSS
`1,372,860 KiB`.

## Limitations

This verifies the reported synthetic experiment, not every possible
perturbation decomposition. The covariances commute exactly as required
by Section 4.1; non-commuting covariances are tested separately by
Claim 6.
