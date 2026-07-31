# Claim 4 method

Algorithm 2 is implemented directly: the first `d-1` eigenvalues are
uniform on the stated interval, the final eigenvalue enforces the trace,
rejected samples are redrawn, and coordinates are randomly permuted.
Means are uniform on their sphere.

Because all covariances share the identity basis, each Gaussian is
represented by its mean concatenated with square-root eigenvalues.
This makes the Wasserstein metric exactly Euclidean and Algorithm 1 an
exact Gibbs-weighted coordinate average. Each query splits its squared
perturbation budget equally between mean and covariance coordinates.

Three independent memories are tested. Every iteration reports mean,
standard deviation, 95% interval, convergence rate, and nearest-target
rate. Final query errors are retained in the raw result. A scalar-loop
softmax implementation is the independent checker.
