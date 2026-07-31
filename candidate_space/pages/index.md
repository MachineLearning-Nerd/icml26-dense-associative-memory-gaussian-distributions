# Current verification

This candidate starts from the immutable judged revision
`5d96031f01d2b0e83e0e8cbdd3ad9baadb26ce45`. Current verification is
listed first; the historical judged page will remain reachable and
unchanged in the release candidate.

Current verifier: Git
`856fea8914ea9289e565c5e7e58ce3d55936a377`, successful cumulative run
`52ab44ba-6855-4d43-a90c-33b50fdf0b79`, fixed command
`uv sync --frozen && uv run python -m reproduction.run`. It supersedes
the historical toy verifier as the only current verification run.

| Claim | Current page | Status |
| --- | --- | --- |
| 1 | [Wasserstein LSE formulation](current/claim-1.md) | VERIFIED |
| 2 | [Exponential storage capacity](current/claim-2.md) | VERIFIED |
| 3 | [Dimension-decay retrieval](current/claim-3.md) | VERIFIED |
| 4 | [Exact synthetic temperature separation](current/claim-4.md) | VERIFIED |
| 5 | [Text8 phase transition](current/claim-5.md) | VERIFIED |
| 6 | [Non-commuting one-step convergence](current/claim-6.md) | FALSIFIED |

Read the [paper version audit](current/version-audit.md) before comparing
claims against the current arXiv source. The [illustrated reproduction
report](current/report.md) explains the implementation and evidence.
The [release forecast](current/release-report.md) separates the previous
live score from projected points, and the
[marimo tutorial](../notebooks/ddam_reproduction.py) embeds the compact
accepted evidence.

The previous `overview` page is preserved verbatim and remains reachable
as **Historical rejected baseline**. Its toy verifier is superseded by
the fixed command and current claim pages above.

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pages/current/claim-1.md` | yes, excerpt and source path | yes | yes | finite difference | sign reversal rejected | yes | VERIFIED |
| 2 | `pages/current/claim-2.md` | yes, source path | yes | yes | proof + exact L2 | duplicate rejected | yes | VERIFIED |
| 3 | `pages/current/claim-3.md` | yes, source path | yes | yes | long double | reversed logits rejected | yes | VERIFIED |
| 4 | `pages/current/claim-4.md` | yes, linked verifier | yes | yes | scalar loop | beta-zero rejected | yes | VERIFIED |
| 5 | `pages/current/claim-5.md` | yes, linked verifier | yes | yes | scalar loop | beta-zero rejected | yes | VERIFIED |
| 6 | `pages/current/claim-6.md` | yes, linked verifier | yes | yes | SciPy `sqrtm` | beta-zero rejected | yes | FALSIFIED |
