# Dense associative memory for Gaussian distributions — reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-uPHdNikfdo-dense-associative-memory-for-gaussian-distributions/blob/main/notebooks/ddam_reproduction.py)

This repository reproduces all six OpenResearch claims for
[arXiv:2509.23162v1](https://arxiv.org/abs/2509.23162v1). The successful
cumulative suite finds Claims 1–5 **VERIFIED** and the exact
non-commuting one-step Claim 6 **FALSIFIED**.

The strongest new result is the previously deferred Text8 experiment:
the executed author notebook rises from 31% retrieval at beta 11.29 to
98% at 16.24; three independent 100-query seeds rise from 79–83% to
100% over the same interval. At exact `N=1000,d=10`, the paper's
non-commuting one-step claim is contradicted by both new runs and its
own archived Figure 8.

The fixed reproduction command is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

All formal runs used Hugging Face `cpu-upgrade`, provisioned as 8 vCPUs
and 32 GB. The winning cumulative job took 16m24s and cost approximately
`$0.0082`. No GPU was used.

Read the [illustrated technical report](reports/reproduction/report.md),
[release forecast](reports/reproduction/release-report.md), or
[self-contained marimo tutorial](notebooks/ddam_reproduction.py).

## Claim summary

| Claim | Paper result | Observed result | Assessment | Substitution or limitation |
| --- | --- | --- | --- | --- |
| 1 | Wasserstein LSE energy | exact formula; gradient error `8.70e-11` | VERIFIED | Gaussian specialization |
| 2 | `Omega(exp(d alpha²/16))` capacity | proof certificate; calibrated slope `0.12390` | VERIFIED | empirical sweep supports but does not replace proof |
| 3 | error decays exponentially in dimension | certified rate; fitted slope `-4.4827` | VERIFIED | log-domain certificate avoids floating-point zero |
| 4 | `N=10000,d=50`, beta 1 vs 0.1 | 100% vs 0% over 90,000 query-cells | VERIFIED | paper leaves perturbation decomposition ambiguous |
| 5 | Text8 transition near beta 15 | author 31→98%; new seeds 79–83→100% | VERIFIED | author trained on only 100,000 tokens; reconstruction batches updates |
| 6 | non-commuting one-step convergence | one-step error 0.565–0.595 at `100r` | FALSIFIED | exact empirical claim only, not the broader model |

The best-supported `12/12` is a forecast, not a new judge result. The
last live judge score remains `6/12` until it evaluates the published
Hugging Face revision.

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | publication surface | Not run as an experiment (publication surface) | reader-facing artifacts | — |
| [`orx/baseline-judged-claim-1-regression`](https://github.com/MachineLearning-Nerd/icml26-repro-uPHdNikfdo-dense-associative-memory-for-gaussian-distributions/tree/orx/baseline-judged-claim-1-regression) | freeze judged baseline and regress Claim 1 | `uv sync --frozen && uv run python -m reproduction.run` | Claim 1 VERIFIED | HF `cpu-upgrade` |
| [`orx/claim-2-calibrated-capacity-scaling`](https://github.com/MachineLearning-Nerd/icml26-repro-uPHdNikfdo-dense-associative-memory-for-gaussian-distributions/tree/orx/claim-2-calibrated-capacity-scaling) | theorem certificate and non-circular capacity search | `uv sync --frozen && uv run python -m reproduction.run` | Claims 1–2 VERIFIED | HF `cpu-upgrade` |
| [`orx/claim-3-dimension-decay-retrieval`](https://github.com/MachineLearning-Nerd/icml26-repro-uPHdNikfdo-dense-associative-memory-for-gaussian-distributions/tree/orx/claim-3-dimension-decay-retrieval) | test decay in dimension | `uv sync --frozen && uv run python -m reproduction.run` | Claims 1–3 VERIFIED | HF `cpu-upgrade` |
| [`orx/claim-4-exact-synthetic-phase-separation`](https://github.com/MachineLearning-Nerd/icml26-repro-uPHdNikfdo-dense-associative-memory-for-gaussian-distributions/tree/orx/claim-4-exact-synthetic-phase-separation) | exact `N=10000,d=50` beta comparison | `uv sync --frozen && uv run python -m reproduction.run` | Claims 1–4 VERIFIED | HF `cpu-upgrade` |
| [`orx/claim-6-source-consistent-falsification-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-uPHdNikfdo-dense-associative-memory-for-gaussian-distributions/tree/orx/claim-6-source-consistent-falsification-audit) | exact-scale non-commuting counterexample | `uv sync --frozen && uv run python -m reproduction.run` | Claim 6 FALSIFIED | HF `cpu-upgrade` |
| [`orx/claim-5-source-faithful-transition-band-verifier`](https://github.com/MachineLearning-Nerd/icml26-repro-uPHdNikfdo-dense-associative-memory-for-gaussian-distributions/tree/orx/claim-5-source-faithful-transition-band-verifier) | recover Text8 protocol and verify transition | `uv sync --frozen && uv run python -m reproduction.run` | Claims 1–5 VERIFIED; Claim 6 FALSIFIED | HF `cpu-upgrade`, 16m24s |

## Local reading

The notebook opens with embedded accepted evidence; expensive experiments
are optional:

```bash
marimo edit notebooks/ddam_reproduction.py
marimo run notebooks/ddam_reproduction.py
```

Raw JSON/CSV, claim contracts, checkers, controls, source audits, and
runtime records live under `.openresearch/artifacts/`. Evaluator-facing
copies are assembled under `candidate_space/evidence/`.
