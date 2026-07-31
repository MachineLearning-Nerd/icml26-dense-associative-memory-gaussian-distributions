# Evaluator-blind red team — round 1

Candidate root was assembled fresh by overlaying the protected judged
revision `5d96031f01d2b0e83e0e8cbdd3ad9baadb26ce45` with candidate text.
The reviewer started only from:

- `README.md`
- `logbook.json`
- `pages/index.md`

The machine record `red-team-round-1.json` lists all 77 files opened.
No repository paths, OpenResearch logs, dashboards, or unpublished
branches were used to complete the review.

All six claim rows exposed the exact contract and source anchor,
assumption/numerical audit, executable verifier, fixed command, raw
numbers inline, raw JSON/CSV links, independent checker, negative
control, limitations, Git SHA, seeds, CPU/runtime record, and nonzero
failure behavior. The historical overview was reachable and labeled
exactly **Historical rejected baseline**. No local link was broken.

Reviewer conclusions:

| Claim | Located current verifier | Evidence conclusion |
| --- | --- | --- |
| 1 | yes | VERIFIED |
| 2 | yes | VERIFIED |
| 3 | yes | VERIFIED |
| 4 | yes | VERIFIED |
| 5 | yes | VERIFIED |
| 6 | yes | FALSIFIED |

Conclusion that could not be verified: none.

Fix requested before round 2: replace placeholder `logbook.json`
revision and timestamp with the winning scientific SHA and actual UTC
time.
