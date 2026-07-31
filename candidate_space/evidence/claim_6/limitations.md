# Claim 6 limitations and deviations

The paper omits seeds and the exact PSD direction distribution. This
verifier uses three documented seeds and two valid laws:
trace-normalized full-rank Wishart directions and random rank-one PSD
directions. Scaling is immaterial because binary search fixes the exact
covariance distance.

Figure 8 raw data is unavailable. Pixel digitization is therefore an
approximation, but it is hash-pinned, independently axis-calibrated,
and separated from the numerical rerun. Its margins are two to three
orders of magnitude larger than the `1e-3` prose level.

This is a falsification of the finite v1 empirical statement, not a
claim that no non-commuting memory instance can ever retrieve. The
current v2 paper removed the experiment; that version change is
disclosed rather than treated as evidence.
