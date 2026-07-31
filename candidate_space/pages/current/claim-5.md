# Claim 5 — Text8 phase transition: VERIFIED

Canonical source: arXiv:2509.23162v1, Section 4.1.1 and Figures 4–5.
The later v2 removes this experiment; this page tests the exact v1
claim scored by the live judge.

## Exact contract

Use the canonical 17,005,207-token Text8 corpus and the recovered
executed author configuration: a top-10,000 vocabulary, 50-dimensional
spherical Gaussian embeddings, five training epochs, and ten retrieval
updates over 20 log-spaced beta values.

The paper does not define “sharp” numerically. Before the accepted child
run, the contract required:

- at most 5% retrieval through beta 5.46;
- at most 50% retrieval at beta 7.85;
- at least 95% retrieval at beta 16.24 and thereafter;
- a first 50% crossing in `[11, 16.5]`;
- Wilson 95% separation of the beta 7.85 and 16.24 endpoints for all
  three deterministic query seeds.

The fixed command is:

```bash
uv sync --frozen && uv run python -m reproduction.run
```

The cumulative runner exits nonzero if this verifier rejects any
predicate.

## Source and data audit

The Text8 archive SHA-256 is
`a6640522afe85d1963ad56c05b0ede0a0c000dddc9671758a6cc09b7a38e5232`;
the uncompressed corpus MD5 is `3bea1919949baf155f99411df5fada7e`.
It contains 17,005,207 tokens and 253,854 types. The top-10,000
vocabulary hash is
`d4e1f58f89a7ad0b89a479b79fdd9559f9ea2d9575ad79ce7556da736675f923`.

The authors' deleted executed notebook is retrieved at immutable commit
`d5346b69a778ad316c031a8e0f2f13b5f86e6e15` and SHA-256
`4720167b74eb84cb35ec853863ab1f23eabcf837ccfe1b5e41d4496872e2ce3e`.
It reveals a material paper/code discrepancy: although the paper says
Text8, the executed run trains on only the first 100,000 corpus tokens.
The reproduction follows and discloses that executable configuration.

## Result

The recovered author output and independent reconstruction both show
the claimed transition:

| Evidence | beta 7.85 | beta 11.29 | beta 16.24 |
| --- | ---: | ---: | ---: |
| executed author notebook | 0% | 31% | 98% |
| independent seed 42 | 38% | 83% | 100% |
| independent seed 43 | 32% | 83% | 100% |
| independent seed 44 | 30% | 79% | 100% |

Each independent cell contains 100 queries. At beta 7.85, the Wilson
95% upper bounds are 47.8%, 41.7%, and 39.6%. At beta 16.24, all three
Wilson lower bounds are 96.3%. Every seed remains at 100% for all larger
beta values.

The scalar-loop Wasserstein update agrees with the vectorized
implementation to `3.0982161280945775e-15`. The beta-zero
uniform-weight control retrieves 0%.

Downloadable evidence:

- [verifier source](../../evidence/claim_5/verifier.py)
- [claim contract](../../evidence/claim_5/claim_contract.json)
- [source audit](../../evidence/claim_5/source_audit.md)
- [raw result](../../evidence/claim_5/raw/result.json)
- [phase sweep CSV](../../evidence/claim_5/raw/phase_sweeps.csv)
- [6,000 per-query rows](../../evidence/claim_5/raw/query_results.csv)
- [independent checker](../../evidence/claim_5/independent_checker.json)
- [negative control](../../evidence/claim_5/negative_control.json)
- [runtime and CPU record](../../evidence/claim_5/runtime.json)
- [evaluator guide](../../evidence/claim_5/EVAL.md)

Successful cumulative run `52ab44ba-6855-4d43-a90c-33b50fdf0b79`
used HF `cpu-upgrade`, documented as 8 vCPUs and 32 GB. The container
exposed 64 logical/affinity CPUs. Suite runtime was `945.208 s`, job
duration `16m24s`, peak RSS `1,539,864 KiB`, and estimated job cost
`$0.0082`.

## Limitations

The independent trainer preserves the historical objective,
initialization, sampling, clipping, constraints, and AdaGrad rule but
batches 2,048 ranking pairs instead of applying the abandoned Cython
implementation sequentially. The immutable executed notebook separately
anchors the exact author run. The 100,000-token cap is an undisclosed
deviation in the paper's own experiment, not a reproduction substitution.
