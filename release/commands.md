# Reproduction and release commands

Every experiment node inherited this exact scientific command:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

Every long or uncertain CPU run was submitted through OpenResearch to
the configured Hugging Face backend:

```bash
orx exp run <experiment-id> --flavor cpu-upgrade --timeout <bound> --image ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim
orx exp wait <experiment-id> --timeout 480
orx logs <run-id>
```

The accepted cumulative run used:

```bash
orx exp run 8afda98b-e400-49fa-9661-68a9122a9be5 --flavor cpu-upgrade --timeout 6h --image ghcr.io/astral-sh/uv:0.11.32-python3.12-trixie-slim
orx exp wait 8afda98b-e400-49fa-9661-68a9122a9be5 --timeout 480
orx logs 52ab44ba-6855-4d43-a90c-33b50fdf0b79 --range 0:4004291
```

Short local, one-core validation and presentation commands:

```bash
UV_NO_SYNC=1 uv run python -m py_compile reproduction/claims/claim_5/verifier.py
jq empty reproduction/claims/claim_5/claim_contract.json
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 UV_NO_SYNC=1 uv run python reports/reproduction/make_figures.py
/opt/homebrew/bin/marimo check notebooks/ddam_reproduction.py
xmllint --noout reports/reproduction/images/*.svg
UV_NO_SYNC=1 uv run python release/validate_candidate.py <fresh-candidate-root>
```

Tree, source, and evidence inspection used `orx projects`, `orx runs`,
`orx exp status`, `orx exp desc`, `orx logs`, `git status`,
`git rev-parse`, `git branch -a`, `git ls-remote`, `rg`, `jq`, `find`,
`shasum -a 256`, `file`, and `du`. Paper retrieval used explicit
`OpenResearch-Reproduction/1.0` HTTP User-Agent requests.

The publication action, after the final gate, is a text-only API upload
of every path in `upload-allowlist.txt` to the existing Space
`DineshAI/uPHdNikfdo`, followed by fresh download, hash comparison, and
the same traversal command.
