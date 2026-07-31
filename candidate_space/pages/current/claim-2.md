# Claim 2 — exponential storage capacity: VERIFIED

Canonical source: arXiv:2509.23162v1,
[Theorem 1](https://ar5iv.labs.arxiv.org/html/2509.23162v1#Thmtheorem1)
and [Algorithm 3](https://ar5iv.labs.arxiv.org/html/2509.23162v1#alg3).

## Exact contract

For `0<p<1`, positive spectral bounds with
`gamma=lambda_max/lambda_min<sqrt(e)`,
`alpha=1-2 log(gamma)`, and
`beta>3 alpha/lambda_min`, the theorem asserts that some `d0` exists
such that for every `d>d0`,

```text
N = floor(sqrt(p/2) exp(d alpha^2/16))
```

Algorithm 3 samples `N` pairwise-commuting Gaussians on the stated
Wasserstein sphere and the energy stores `Omega(N)` patterns with
probability at least `1-p`.

The fixed command is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

The executable [verifier](../../evidence/claim_2/verifier.py),
[contract](../../evidence/claim_2/claim_contract.json), and
[source audit](../../evidence/claim_2/source_audit.md) are visible here.
The cumulative runner exits nonzero if this verifier rejects any
predicate.

## Proof-level result

The independent certificate used `p=0.1`, `lambda_min=1`,
`lambda_max=1.1`, and `beta=3`. It checked every domain assumption,
reconstructed the union bound and contraction implications, verified
the rate

```text
alpha^2/16 = 0.040943462642501954,
```

and found a conservative numerical `d0=364`. Tail monotonicity checks
show that the certified sufficient inequalities persist for all larger
dimensions. All sweeps use deterministic seeds `20260730` through
`20260734`.

The paper HTML has two documented transcription inconsistencies: one
proof sentence writes `/8` where the theorem and union-bound algebra
require `/16`, and another equality drops a factor `d` from `R^2`.
The certificate checks the theorem statement and corrected algebra
explicitly.

## Independent empirical calibration

The primary scaling calibration did not choose sample sizes from the
claimed formula. It searched the fixed grid
`N=8,16,...,8192` at `d=32,48,64,80`, with five deterministic seeds,
and recorded the first separation failure.

| Quantity | Observed |
| --- | ---: |
| mean fitted `log(capacity)/d` slope | `0.12390005852509015` |
| 95% lower confidence bound | `0.11574225041692215` |
| claimed sufficient exponent | `0.040943462642501954` |

The separate theorem-sized sweep ran 25 complete Algorithm 3 samples
at `d=100,140,180,220,260`, reaching `N=9,390`. Every sample satisfied
the sphere, trace, spectral, and commutativity invariants and the
separation condition. The worst separation margin was
`0.4505864872109182`.

An independent checker evaluated 6,400 exact Gaussian `L2` overlaps;
the minimum exact separation minus the proof lower bound was
`4.0341059584373795`. A duplicated-pattern control was rejected because
its minimum mean distance is zero.

Downloadable evidence:

- [raw result](../../evidence/claim_2/raw/result.json)
- [theorem-sized sweep](../../evidence/claim_2/raw/theorem_sweep.csv)
- [independent calibration](../../evidence/claim_2/raw/calibration_sweep.csv)
- [proof certificate](../../evidence/claim_2/proof_certificate.json)
- [independent checker](../../evidence/claim_2/independent_checker.json)
- [negative control](../../evidence/claim_2/negative_control.json)
- [runtime](../../evidence/claim_2/runtime.json)
- [evaluator guide](../../evidence/claim_2/EVAL.md)

Run `a2f67dbf-8aaf-4e90-9d38-4b7a1d51c50d` used HF
`cpu-upgrade`, provisioned as 8 vCPUs and 32 GB. The container exposed
64 logical/affinity CPUs and used a 64-thread limit. Verifier runtime was
`385.97424927703105 s`; total job runtime `433 s`; peak RSS
`274,332 KiB`. Git SHA:
`9fa3d8d77b71276c8a78450038ec9e0da8c2ec7b`.

## Limitations

The empirical trials alone do not establish universal quantifiers; the
verdict relies on the proof certificate. The finite-length pairwise
Gibbs kernel used for covariance-polytope sampling has the correct
uniform invariant law, but its finite-time uniformity remains a
numerical approximation.
