# Claim-to-evidence ledger

Each verdict is produced by a machine-readable contract, an executable
verifier, saved raw evidence, an independent checker, and a negative control.
The detailed evaluator-facing pages are under
[`candidate_space/pages/current`](candidate_space/pages/current).

| Claim | Verdict | How the verdict is produced | Primary evidence |
| --- | --- | --- | --- |
| C1. Wasserstein LSE formulation | `VERIFIED_SCOPED` | Compare the Gaussian specialization, analytic mean gradient, stored-pattern ordering, and a sign-reversed control. | [Claim page](candidate_space/pages/current/claim-1.md) · [`reproduction/claims/claim_1`](reproduction/claims/claim_1) |
| C2. Exponential storage capacity | `VERIFIED_SCOPED` | Reconstruct the proof certificate and independently calibrate finite capacity without selecting the grid from the claimed formula. | [Claim page](candidate_space/pages/current/claim-2.md) · [`reproduction/claims/claim_2`](reproduction/claims/claim-2) |
| C3. Dimension-dependent retrieval decay | `VERIFIED_SCOPED` | Check the proof rate, log-domain certificate, dimension sweep, and long-double direct computations. | [Claim page](candidate_space/pages/current/claim-3.md) · [`reproduction/claims/claim_3`](reproduction/claims/claim_3) |
| C4. Synthetic temperature separation | `VERIFIED_SCOPED` | Reproduce the stated `N=10000`, `d=50`, beta `1` versus `0.1` experiment across fixed seeds and compare with a scalar implementation. | [Claim page](candidate_space/pages/current/claim-4.md) · [`reproduction/claims/claim_4`](reproduction/claims/claim_4) |
| C5. Text8 phase transition | `VERIFIED_SCOPED` | Recover the executed author notebook protocol and compare the author anchor with independent seeded runs across beta. | [Claim page](candidate_space/pages/current/claim-5.md) · [`reproduction/claims/claim_5`](reproduction/claims/claim_5) |
| C6. Non-commuting one-step convergence | `FALSIFIED_SCOPED_V1` | Test the exact v1 setup, independent checker, controls, and digitized Figure 8(b); the one-step error remains far above the claimed tolerance. | [Claim page](candidate_space/pages/current/claim-6.md) · [`reproduction/claims/claim_6`](reproduction/claims/claim_6) |

The cumulative run records the fixed command, software versions, hardware,
seeds, runtime, and raw outputs in
[`candidate_space/evidence/cumulative`](candidate_space/evidence/cumulative).

