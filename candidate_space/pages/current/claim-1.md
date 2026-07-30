# Claim 1 — Wasserstein LSE formulation

Canonical source: arXiv:2509.23162v2, Section 2, equation 1.

The fixed command is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

The verifier is `reproduction/claims/claim_1/verifier.py`; its exact
contract is `reproduction/claims/claim_1/claim_contract.json`. Raw
baseline output will be added from the immutable OpenResearch run log on
the first child, after the baseline branch is frozen.

