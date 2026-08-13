# Branch audit

This repository began with OpenResearch-style `orx/` branch names. The
branches below were renamed to make their purpose clear while preserving
their commit history and evidence lineage. `main` is the publication
surface.

| Historical branch | Clean branch | Purpose and evidence scope |
| --- | --- | --- |
| `main` | `main` | Publication surface, cumulative runner, reports, and evaluator-facing evidence. |
| `orx/baseline-judged-claim-1-regression` | `audit/baseline-claim-1-regression` | Freezes the judged baseline and regresses the Claim 1 formulation. |
| `orx/claim-2-calibrated-capacity-scaling` | `experiment/claim-2-capacity-scaling` | Reconstructs the exponential capacity certificate and performs independent finite-size calibration. |
| `orx/claim-3-dimension-decay-retrieval` | `experiment/claim-3-dimension-decay` | Tests the dimension-dependent retrieval-error rate with log-domain and long-double checks. |
| `orx/claim-4-exact-synthetic-phase-separation` | `experiment/claim-4-temperature-separation` | Reproduces the exact `N=10000`, `d=50`, beta `1` versus `0.1` synthetic experiment. |
| `orx/claim-5-author-code-text8-phase-transition` | `experiment/claim-5-author-text8` | Preserves the author-notebook Text8 protocol and its phase-transition output. |
| `orx/claim-5-source-faithful-transition-band-verifier` | `audit/claim-5-text8-transition-band` | Verifies the source-faithful Text8 transition contract across independent seeds. |
| `orx/claim-6-exact-non-commuting-covariance-retrieval` | `audit/claim-6-noncommuting-retrieval` | Checks non-commuting covariance retrieval trajectories and scale behavior. |
| `orx/claim-6-source-consistent-falsification-audit` | `audit/claim-6-falsification` | Combines the assumption checks, independent checker, negative control, and v1 Figure 8(b) contradiction for Claim 6. |
| `orx/evaluator-visible-claim-1-evidence` | `audit/evaluator-claim-1` | Keeps the evaluator-visible Claim 1 evidence surface. |
| `orx/evaluator-visible-release-candidate` | `release/evaluator-visible-candidate` | Assembles the evaluator-facing release candidate and publication artifacts. |

## Branch hygiene

- No `orx/` branch is part of the cleaned public namespace.
- Branch names describe evidence role (`audit`), experiment (`experiment`),
  or publication surface (`release`).
- A branch is not an independent paper version; the v1/v2 scope is tracked
  in [`candidate_space/pages/current/version-audit.md`](candidate_space/pages/current/version-audit.md).
- Claim verdicts come from the contracts and verifiers, not from branch
  names or commit messages.
