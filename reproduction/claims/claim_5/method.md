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

The checker independently evaluates Phi with scalar distance and weight
loops. The negative control sets beta to zero, forcing uniform weights.
