# Claim 6 source audit

- Judged source: arXiv:2509.23162v1, Algorithm 1, Section 6.2.3,
  Figure 8.
- Retrieved with an explicit OpenResearch browser User-Agent:
  2026-07-31.
- v1 PDF SHA-256:
  `58b2f5125c77f256aacff39fb6a479867b786565e393c1b6cb8f014248045ba9`.
- v1 source archive SHA-256:
  `a88a9b572b0d3c28b62de7f9419885cd3367d25e8b453bf4ffeba36a68f1f6ee`.
- Figure 8 panel (b) SHA-256:
  `58cab4d6ad088d862eb892d5eee30389d77cf23d8434185e9f692b27f3bebd18`.

Section 6.2.3 fixes `N=1000`, `d=10`, 750 queries, sphere radius
`R=sqrt(2d)`, beta values 1 and 0.1, and perturbation radii
`1/sqrt(beta N)` and `100/sqrt(beta N)`. Means satisfy
`||mu_i||^2=d`. Covariances are sampled as `WW^T+0.01I` and rescaled
to trace `d`, without a shared eigenbasis.

The query assigns half of squared W2 distance to the mean and half to
the covariance. A random PSD covariance direction is scaled by binary
search to hit the requested distance. Algorithm 1 computes exact
Bures-Wasserstein distances and transport maps.

The Figure 8 caption draws a `1e-6` threshold. The following prose says
beta 1 converges in one step but reaches a `1e-3` level, rather than the
`1e-6` reached by commuting covariances. The contract therefore tests
the prose claim at `1e-3`.

The source figure contradicts that prose for the 100-fold radius.
Hash-pinned pixel calibration gives average W2 errors of approximately
`3.154, 0.621, 0.226, 0.166, 0.158, 0.158` at iterations zero through
five. The panel therefore neither converges in one step nor approaches
`1e-3`.

The paper does not publish seeds, the law or normalization of the PSD
directions, a numerical binary-search tolerance, or raw Figure 8 data.

The current arXiv v2 source removed this non-commuting experiment. The
live judge and protected Space revision explicitly assess the v1 claim,
so this contract names v1 and does not attribute the statement to v2.
