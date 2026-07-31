# Claim 3 method

For commuting Gaussians, concatenate the mean and square roots of the
covariance eigenvalues. Squared Euclidean distance in this `2d`
coordinate is exactly squared Wasserstein distance, and Algorithm 1 is
the Gibbs-weighted average of stored coordinates.

Queries perturb only the mean by `0.9r`, so covariance assumptions are
preserved exactly. The verifier computes a log-domain certificate

```text
error <= sum_j w_j W2(X_j, X_i)
```

without underflow. It compares every certificate to Theorem 3, fits
log error against dimension for five seeds, and reports a confidence
interval. A separate long-double loop directly sums
`w_j (X_j-X_i)` for small cases. Reversing the Gibbs sign is the
negative control.
