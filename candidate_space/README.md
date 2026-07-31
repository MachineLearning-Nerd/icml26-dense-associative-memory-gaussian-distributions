---
title: "Gaussian Dense Associative Memory (uPHdNikfdo)"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-uPHdNikfdo
---

# Gaussian Dense Associative Memory — current verification

The current candidate tests every judged claim from arXiv
`2509.23162v1`: Claims 1–5 are **VERIFIED** and Claim 6 is
**FALSIFIED**.

Start with the [current verification index](pages/index.md), then read
the [illustrated report](pages/current/report.md) or any individual
claim page. The previous judged `overview` is preserved verbatim and
reachable as **Historical rejected baseline**; its toy verifier is not
the current verifier.

Fixed command:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

Successful cumulative run:
`52ab44ba-6855-4d43-a90c-33b50fdf0b79` at Git
`856fea8914ea9289e565c5e7e58ce3d55936a377`.

The previous live judge score remains `6/12`. Any higher total is a
forecast until the live judge evaluates this revision.
