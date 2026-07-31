# Claim 1 — Wasserstein LSE formulation: VERIFIED

Canonical source: arXiv:2509.23162v1, Section 2
([equation 1](https://ar5iv.labs.arxiv.org/html/2509.23162v1#S2.E1)).
Source HTML was retrieved `2026-07-30T07:22:13Z` and hashes to
`12972950e6f86841398b97457bbe3a8ee5c2e8a6cbdf0fd7eb319bbb6ebd1628`.

## Exact contract

For `beta > 0` and stored distributions `X_1,...,X_N` in
`P_2(R^d)`, the paper defines

```text
E(xi) = -(1/beta) log sum_i exp(-beta W_2^2(X_i, xi)).
```

This verifier tests the non-degenerate Gaussian specialization. It
requires an exact formula match, an analytic mean-gradient match to an
independent central finite difference, stored-pattern energies below a
deterministic fixture centroid, and rejection of a sign-reversed
gradient control.

The fixed command is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

The executable verifier is
`reproduction/claims/claim_1/verifier.py`; the machine-readable contract
is `reproduction/claims/claim_1/claim_contract.json`.

## Raw result

Run `4b824e0c-a9f3-4ace-b39c-706057da9992`, Git SHA
`3612f94158c9da860d7b09733266994176e098db`:

| Check | Observed | Threshold | Result |
| --- | ---: | ---: | --- |
| formula difference | 0 | `1e-12` | pass |
| gradient max absolute error | `8.703970877377287e-11` | `1e-6` | pass |
| maximum stored energy | `8.881784197001252e-16` | below centroid | pass |
| centroid energy | `8.142790314124024` | — | supporting evidence |
| sign-reversed control error | `14.227561462768701` | at least `0.1` | rejected as intended |

Analytic gradient:
`[-7.113780731352815, 1.081066567733659]`.

Independent finite-difference gradient:
`[-7.113780731415885, 1.0810665678206988]`.

Downloadable evidence:

- [raw result](../../../.openresearch/artifacts/claim_1/raw/result.json)
- [independent checker](../../../.openresearch/artifacts/claim_1/independent_checker.json)
- [negative control](../../../.openresearch/artifacts/claim_1/negative_control.json)
- [runtime and CPU record](../../../.openresearch/artifacts/claim_1/runtime.json)
- [exact command](../../../.openresearch/artifacts/claim_1/exact_command.txt)

HF `cpu-upgrade` exposed 64 logical/affinity CPUs; the verifier imposed a
one-thread numerical cap. Verifier runtime was `0.0967043 s`; total job
duration, including environment setup, was `42 s`; peak RSS was
`39,264 KiB`.

## Limitations

This verifies the mathematical formulation and Gaussian specialization,
not behavior for every distribution in `P_2(R^d)`. The decisive evidence
is the exact formula and independent derivative check; the separated
minimum fixture is supporting evidence.
