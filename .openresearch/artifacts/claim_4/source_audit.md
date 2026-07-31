# Claim 4 source audit

- Source: arXiv:2509.23162v1, Section 4.1, Figure 3, Algorithm 2,
  and Appendix Figure 6.
- Retrieved: 2026-07-30T07:22:13Z.
- HTML SHA-256: `12972950e6f86841398b97457bbe3a8ee5c2e8a6cbdf0fd7eb319bbb6ebd1628`.
- PDF SHA-256: `3fc686f5cbc55b7ecb2f80dbb00c50adb3621c3645a100945e95a663983a5119`.

The main experiment fixes `N=10000`, `d=50`, 7,500 queries,
`lambda_min=1`, `lambda_max=1.1`, beta values 1 and 0.1, and radii
`1/sqrt(beta N)` and `100/sqrt(beta N)`. The plotted convergence
threshold is `1e-6`.

Section 4.1 prints `R=d(lambda_max+lambda_min)`, while Algorithm 2
unambiguously sets `R^2=d(lambda_min+lambda_max)`. The asset names and
the sphere definition also support the Algorithm 2 interpretation.
This verifier follows Algorithm 2 and records the textual ambiguity.
The paper does not specify how perturbation is divided between mean and
covariance; the verifier splits squared Wasserstein budget equally.
