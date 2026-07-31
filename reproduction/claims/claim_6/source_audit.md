# Claim 6 source audit

- Source: arXiv:2509.23162v2, Algorithm 1, Section 6.2.3, Figure 8.
- Retrieved: 2026-07-30T07:22:13Z.
- HTML SHA-256: `12972950e6f86841398b97457bbe3a8ee5c2e8a6cbdf0fd7eb319bbb6ebd1628`.
- PDF SHA-256: `3fc686f5cbc55b7ecb2f80dbb00c50adb3621c3645a100945e95a663983a5119`.

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
the prose claim at `1e-3` and reports the stricter plotted threshold
without using it to rewrite the statement.

The paper does not publish seeds, the law or normalization of the PSD
directions, a numerical binary-search tolerance, or raw Figure 8 data.
