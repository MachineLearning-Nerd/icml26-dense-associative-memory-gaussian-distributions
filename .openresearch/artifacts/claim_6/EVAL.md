# Claim 6 evaluator guide

Verdict: **FALSIFIED** for the exact arXiv v1 Section 6.2.3 assertion
that the `N=1000`, `d=10` non-commuting experiment converges in one
update at beta 1.

Start with `raw/result.json`. Every contract predicate is true. The
three `100r` seed means are 0.5650, 0.5954, and 0.5910 after one
update and 0.1736, 0.1839, and 0.1272 after five updates. No query is
below the paper figure's `1e-6` line after five updates.

The independent SciPy `sqrtm` implementation agrees to below `8e-15`.
The beta-zero control fails as intended. A rank-one PSD perturbation
law also contradicts one-step convergence. Finally, the verifier
retrieves the hash-pinned paper source and independently digitizes its
own Figure 8(b), which ends near W2 0.158 rather than zero.

The author repository's deleted executed notebook at commit
`d5346b69a778ad316c031a8e0f2f13b5f86e6e15` independently reports
`521/750` nearest-target recoveries and final mean W2 `0.157643` for
the same large-radius run. This agrees with the digitized paper figure
and the new three-seed experiment.
