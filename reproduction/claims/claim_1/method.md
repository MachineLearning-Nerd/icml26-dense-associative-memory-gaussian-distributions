# Claim 1 method

The verifier creates five deterministic, separated two-dimensional
Gaussians. It evaluates the Wasserstein log-sum-exp energy with a stable
log-sum-exp calculation, compares it with an independently written
direct expression, and checks the analytic mean gradient against central
finite differences. The checker also compares stored-pattern energies
with the energy at their centroid.

The negative control reverses the analytic gradient sign. It must exceed
the contract's error threshold; otherwise the verifier exits nonzero.

