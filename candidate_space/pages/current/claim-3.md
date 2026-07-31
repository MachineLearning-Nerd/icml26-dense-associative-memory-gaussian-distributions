# Claim 3 — retrieval error decays in dimension: VERIFIED

Canonical source: arXiv:2509.23162v2,
[Theorem 3](https://ar5iv.labs.arxiv.org/html/2509.23162#Thmtheorem3)
and [Corollary 2](https://ar5iv.labs.arxiv.org/html/2509.23162#Thmcorollary2).

## Exact contract

For Algorithm 3 memories satisfying the inherited commuting,
separation, spectral, self-map, and contraction assumptions, a query
strictly inside

```text
r = 1/sqrt(beta N)
```

must satisfy the one-step bound

```text
W2(Phi(query), X_i) <= 3/sqrt(beta N).
```

Substituting Theorem 1's
`N=Omega(exp(d alpha^2/16))` gives log-error slope at most
`-alpha^2/32` in dimension. This is dimension decay—not decay merely
over retrieval iterations.

## Result

The proof certificate derives the claimed log-error rate
`-0.020471731321250977` for the audited fixture. The experiment varied
`d=100,140,180,220,260`, with `N=13,69,354,1825,9390`, five seeds,
and up to 64 distinct queries per memory. All 1,345 queries were placed
at exactly `0.9/sqrt(beta N)`, preserving the commuting covariance and
spectral assumptions.

| Quantity | Observed |
| --- | ---: |
| mean fitted log-error/dimension slope | `-4.482669200983174` |
| 95% upper confidence bound | `-4.425165805007219` |
| required bound rate | `-0.020471731321250977` |
| smallest margin below Theorem 3 log bound | `414.9609530701211` |

Ordinary double precision rounds these extremely small errors to zero.
The primary result therefore uses a log-domain triangle-inequality
certificate. Fifteen independent long-double direct computations
matched it within `1.14e-13` in log error. Reversing the Gibbs-logit
sign caused all 25 controls to violate the theorem bound.

The fixed command is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

Downloadable evidence:

- [raw result](../../../.openresearch/artifacts/claim_3/raw/result.json)
- [dimension sweep](../../../.openresearch/artifacts/claim_3/raw/dimension_sweep.csv)
- [proof certificate](../../../.openresearch/artifacts/claim_3/proof_certificate.json)
- [independent checker](../../../.openresearch/artifacts/claim_3/independent_checker.json)
- [negative control](../../../.openresearch/artifacts/claim_3/negative_control.json)
- [runtime](../../../.openresearch/artifacts/claim_3/runtime.json)

Run `3bd0e1d9-ab67-44d1-801d-022c6d3df992` used HF
`cpu-upgrade`: estimated 64 cores; actual allocation 64 logical and
affinity CPUs; thread limit 64; verifier runtime `470.3710075530689 s`;
total job runtime `523 s`; peak RSS `304,704 KiB`.

## Limitations

The finite sweep calibrates the proof but does not replace its
quantifiers. At theorem scale, a log-domain certificate is necessary
to avoid presenting floating-point zeros as evidence.
