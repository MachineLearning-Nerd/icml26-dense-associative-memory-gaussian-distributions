# Claim 5 method

The verifier downloads and hashes canonical Text8, reconstructs its
top-10,000 frequency vocabulary, and trains 50-dimensional spherical
Gaussian embeddings for five epochs from the exact first-100,000-token
author configuration. It preserves the historical initialization,
KL-ranking objective, context-pair construction, negative-sampling
law, gradient clipping, covariance bounds, mean-norm bound, AdaGrad
rule, and even the historical Cython raw-index variance lookup.

To keep the locked environment unchanged, the independent implementation
batches 2,048 ranking-pair updates rather than compiling the abandoned
Cython extension. Retrieval itself is an exact Euclidean representation
of spherical Bures-Wasserstein geometry:
`[mu, sqrt(d) * sqrt(variance)]`. Three deterministic 100-word sweeps
use the author's 20-beta grid and ten-update rule.

The paper does not define “sharp” numerically. Before the child run, the
contract operationalizes it on the author's own log-spaced grid: at most
5% retrieval through beta 5.46, at most 50% at beta 7.85, at least 95%
at beta 16.24, the first 50% crossing in [11, 16.5], and a plateau of at
least 95% from beta 16.24 onward. This two-grid-interval
transition band covers the stated beta approximately 15 without adding
the rejected baseline's unstated requirement that one adjacent jump be
at least 50 percentage points. The independent sweeps additionally
require the Wilson 95% upper bound at beta 7.85 to be below 50% and the
lower bound at beta 16.24 to be above 95%.

The checker independently evaluates Phi with scalar distance and weight
loops. The negative control sets beta to zero, forcing uniform weights.
