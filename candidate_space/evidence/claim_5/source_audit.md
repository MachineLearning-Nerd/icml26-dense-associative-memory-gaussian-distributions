# Claim 5 source audit

The judged statement is from arXiv:2509.23162v1, Section 4.1.1 and
Figures 4–5. It states `N=10000`, `d=50`, spherical Gaussian word
embeddings trained for five epochs on Text8, ten retrieval iterations,
and a sharp transition around beta 15. Figures 4–5 show the low- and
high-temperature plateaus but the prose does not quantify “sharp.”

The authors' repository briefly contained an executed `DDAM.ipynb` at
commit `d5346b69a778ad316c031a8e0f2f13b5f86e6e15`; it was deleted 51
minutes later. The verifier retrieves that immutable revision and
requires SHA-256
`4720167b74eb84cb35ec853863ab1f23eabcf837ccfe1b5e41d4496872e2ce3e`.
It exposes the otherwise unstated phase-plot protocol: 100 words,
seed 42, 20 log-spaced betas, and the exact Word2Gauss implementation.

Material discrepancy: although the paper describes the 17,005,207-token
Text8 corpus, the author notebook sets `corpus_sample=100000`, so only
the first 100,000 tokens are used for training. This verifier reproduces
the executable author configuration and reports that cap explicitly.
The later arXiv v2 removes this experiment; it is not silently substituted
for the v1 claim judged by OpenResearch.

The historical rejected baseline required at most 5% retrieval at every
beta below 10 and a 50-percentage-point jump between one adjacent pair of
grid values. Those quantifiers are not in the paper. The current contract
instead declares a transition band using the actual plotted grid: beta
7.85 must be at most 50%, beta 16.24 must be at least 95%, the first 50%
crossing must lie in [11, 16.5], and the high-retrieval plateau must
persist thereafter. Independent sweeps must separate the two endpoints
at Wilson 95% confidence. The contract also requires a near-zero
pre-transition plateau through beta 5.46.
