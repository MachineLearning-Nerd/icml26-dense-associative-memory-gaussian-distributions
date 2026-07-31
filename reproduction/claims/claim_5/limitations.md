# Claim 5 limitations

The recovered author run trained on only 100,000 of Text8's 17,005,207
tokens. The paper does not disclose this cap. The independent trainer
uses the same data slice and objective but batches ranking updates, so
its learned parameters need not be bitwise identical to the notebook's
sequential Cython run. The immutable notebook output separately anchors
the exact author execution; the new sweeps test whether the reported
phase survives an independently implemented full-scale reconstruction.
