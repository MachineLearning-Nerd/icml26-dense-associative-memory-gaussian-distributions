# Claim 2 source audit

- Source: arXiv:2509.23162v1, Theorem 1 and Appendix 6.4.
- HTML anchor: `Thmtheorem1`; sampler: `alg3`.
- Retrieved: 2026-07-30T07:22:13Z.
- HTML SHA-256: `12972950e6f86841398b97457bbe3a8ee5c2e8a6cbdf0fd7eb319bbb6ebd1628`.
- PDF SHA-256: `3fc686f5cbc55b7ecb2f80dbb00c50adb3621c3645a100945e95a663983a5119`.

The theorem quantifies over `0<p<1`, positive eigenvalue bounds with
`gamma=lambda_max/lambda_min<sqrt(e)`, and
`beta>3(1-2 log(gamma))/lambda_min`. It is asymptotic: a finite `d0`
may depend on these parameters, and the conclusion applies to every
integer `d>d0`. Covariances must commute pairwise, their spectra must
remain within the stated interval, and means/covariance traces each use
half of `R^2=d(lambda_max+lambda_min)`.

The HTML proof contains two transcription inconsistencies: the union
bound paragraph displays `/8` for `N` once although the theorem and the
following algebra require `/16`; and a later displayed equality drops a
factor `d` from `R^2`. The verifier reconstructs the chain from the
theorem statement and checks the corrected identities rather than
silently using either typo.
