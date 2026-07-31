Previous live judged score: `6/12`

Conservative projected score range after the proposed change: `10/12–12/12`

Best-supported possible new score: `12/12` **forecast, not a judge result**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 2 | 2 | HIGH | VERIFIED | Existing full-credit formulation evidence passes unchanged in the cumulative suite. |
| 2 | 1 | 2 | HIGH | VERIFIED | Exact theorem assumptions, proof certificate, non-circular calibration, independent checker, and failing control; evaluator may scrutinize the reconstructed proof transcription. |
| 3 | 1 | 2 | HIGH | VERIFIED | Exact dimension quantifier is handled by a proof certificate and five-dimension sweep; log-domain arithmetic is clearly disclosed. |
| 4 | 1 | 2 | HIGH | VERIFIED | Exact `N=10000,d=50`, both beta values and radii, 90,000 query-cells, three seeds, checker, and control. |
| 5 | 0 | 2 | HIGH | VERIFIED | Hash-pinned Text8 and executed author notebook plus an independent full-scale reconstruction and Wilson-separated transition on three seeds; risk is the recovered author's undisclosed 100,000-token cap and batched trainer. |
| 6 | 1 | 2 | HIGH | FALSIFIED | Assumption-satisfying exact-scale counterexample, alternate perturbation law, independent checker, control, and the paper's own digitized curve; risk is interpretation of “one-step” prose. |

Current total score: `6/12` from the last live judge.

Conservative projected total score range: `10/12–12/12`.

Best-supported possible total score: `12/12`, forecast only.

Claims changed since the previous judge result: Claims 2–5 now have
full-scale or proof-level VERIFIED evidence; Claim 6 now has a
source-consistent FALSIFIED result. Claim 1 is preserved and regressed.

Claims remaining BLOCKED: none.

Exact publication action after all gates pass: upload the text allowlist
to the existing `DineshAI/uPHdNikfdo` Space through the Hugging Face API,
verify the returned revision by fresh download and SHA-256 traversal,
then mirror the same reader-facing text paths to GitHub `main`.

## Experiment tree

The tree starts from the immutable judged Claim 1 regression, descends
through Claims 2–4, branches Claim 6 source interpretation, descends to
the valid falsification, and then branches Claim 5 verifier semantics.
Winning scientific SHA:
`856fea8914ea9289e565c5e7e58ce3d55936a377`.

The fixed command on every node is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

Successful cumulative run:
`52ab44ba-6855-4d43-a90c-33b50fdf0b79`.
HF `cpu-upgrade` is provisioned as 8 vCPUs and 32 GB. The successful job
ran for 16m24s and cost approximately `$0.0082`; a separate timeout
attempt ran 4h05m and cost approximately `$0.12` without producing
scientific evidence.
