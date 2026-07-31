# Claim 5 source audit

The judged statement is from arXiv:2509.23162v1, Section 4.1.1 and
Figures 4–5. It states `N=10000`, `d=50`, spherical Gaussian word
embeddings trained for five epochs on Text8, ten retrieval iterations,
near-zero retrieval below beta 10, a sharp transition around beta 15,
and perfect retrieval above beta 30.

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
