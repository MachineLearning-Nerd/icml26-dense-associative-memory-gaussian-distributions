# Claim 2 method

The proof certificate checks the exponential rate, the sphere-tail
union bound, the two Assumption 1 conditions, the contraction threshold,
and eventual disjointness of retrieval balls. It also finds a finite
numerical `d0`; this is independent of the finite experiment.

The full-scale experiment samples Algorithm 3 means uniformly on the
sphere and covariance eigenvalues on its bounded fixed-sum polytope.
The latter uses a pairwise Gibbs kernel whose invariant law is uniform
on the polytope. Exact invariants are checked for every sample. Exact
nearest-pair similarities are computed in blocks.

The main empirical scaling evidence does not select `N` from the theorem.
For five seeds and four dimensions it searches a fixed powers-of-two
grid, records the first separation failure, and fits log capacity
against dimension with a confidence interval. A separate theorem-sized
sweep reaches `d=260` and `N=9,390`.
