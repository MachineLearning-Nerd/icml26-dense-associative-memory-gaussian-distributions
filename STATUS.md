# Reproduction status

## Paper

**Dense associative memory for Gaussian distributions** by Chandan Tankala
and Krishnakumar Balasubramanian. The canonical judged scope is arXiv
`2509.23162v1`; the current v2 source is tracked separately because it
removes or materially changes Claims 5 and 6.

## Overall verdict

`PARTIAL_CLAIMS_1_TO_5_VERIFIED_CLAIM_6_FALSIFIED`

Claims 1–5 pass their explicit contracts. Claim 6 is falsified for the exact
finite v1 one-step non-commuting convergence statement under its stated
setup. The result is narrow: it does not invalidate the broader update rule
or imply that every non-commuting Gaussian memory fails.

## Claim boundary

`C1_TO_C5_SCOPED_V1_VERIFIED_C6_EXACT_V1_ONE_STEP_NONCOMMUTING_FALSIFIED_V2_SCOPE_DIFFERENCE`

| Item | Status |
| --- | --- |
| Current score claim | `false` |
| Publication gate | `false` |
| Official author endorsement | `false` |
| Last historical live judge | `6/12` |
| Release forecast | `10/12–12/12`, forecast only |

The forecast is retained as historical context, never as a current score.

## Verification

The cumulative evidence bundle was produced with:

```bash
uv sync --frozen
uv run python -m reproduction.run
```

The exact claim contracts, raw outputs, independent checkers, negative
controls, and limitations are linked from [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md).

