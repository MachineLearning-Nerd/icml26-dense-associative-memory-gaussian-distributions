# Claim 6 method

Three deterministic replicas implement Section 6.2.3. Each covariance
is generated from a fresh 10 by 10 standard-normal matrix, regularized
by `0.01I`, and rescaled to trace 10. Commutator norms audit that the
covariances do not share an eigenbasis.

For each query, a unit mean direction receives distance
`r/sqrt(2)`. A fresh PSD covariance direction receives the other half
of squared distance. Vectorized bracketing and binary search select its
scale until the exact Bures covariance distance is within `1e-9`.

Algorithm 1 is evaluated in float64 batches. Symmetric eigendecomposition
computes all Bures distances, inverse square roots, and transport maps;
no diagonal or commuting shortcut is used. A separate scalar SciPy
implementation based on `sqrtm` checks a small fixture.

The result reports W2 error, standard deviation, confidence intervals,
nearest-target retrieval, and both `1e-3` and `1e-6` threshold rates.
The beta-zero control uses the mean component as a rigorous lower bound
on full W2 error.
