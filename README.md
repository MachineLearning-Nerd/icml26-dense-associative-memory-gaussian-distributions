# Dense associative memory for Gaussian distributions — independent reproduction

[![Open in Molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-dense-associative-memory-gaussian-distributions/blob/main/notebooks/ddam_reproduction.py)

Independent reproduction and claim audit for **Dense associative memory for Gaussian distributions** by Chandan Tankala and Krishnakumar Balasubramanian.

- Paper: [arXiv:2509.23162](https://arxiv.org/abs/2509.23162)
- Exact judged scope: [arXiv:2509.23162v1](https://arxiv.org/abs/2509.23162v1)
- Clean repository: [MachineLearning-Nerd/icml26-dense-associative-memory-gaussian-distributions](https://github.com/MachineLearning-Nerd/icml26-dense-associative-memory-gaussian-distributions)
- Reproduction command: `uv sync --frozen && uv run python -m reproduction.run`

## What the paper does

The paper extends dense associative memory from vectors to Gaussian
distributions. It uses Wasserstein/Bures–Wasserstein geometry, a
log-sum-exp energy, and Gibbs barycentric retrieval to study energy
landscapes, storage capacity, retrieval error, synthetic phase
separation, and Text8 embeddings.

## Reproduction status

The release bundle verifies five claims and finds one narrow empirical
claim contradicted by both the new experiments and the paper's own
archived evidence.

Overall status: `PARTIAL_CLAIMS_1_TO_5_VERIFIED_CLAIM_6_FALSIFIED`.
This is a scoped v1 audit, not a claim that every theorem or experiment in
every paper revision has been reproduced. `publication_allowed=false`,
`score_claim=false`, and `official_author_endorsement=false` until an
independent evaluator judges the public revision.

| Release result | Meaning |
| --- | --- |
| Claims 1–5: **VERIFIED** | Every contract predicate, checker, and required control passed. |
| Claim 6: **FALSIFIED** | The exact one-step non-commuting convergence claim is contradicted under its stated setup. |
| Blocked claims: none | The release contains an explicit verdict for every claim. |
| Historical live judge: `6/12` | This is the last judged score, not a new judge result. |
| Release forecast: `10–12/12` | Forecast only; it becomes a score only after the evaluator judges the published revision. |

The live judge evaluated **v1**. The current arXiv **v2** removes or
materially changes Claims 5 and 6, so this repository keeps v1 as the
canonical evidence scope instead of silently substituting v2. See the
[paper-version audit](candidate_space/pages/current/version-audit.md).

## Claim-to-evidence map

Each claim is produced by a machine-readable contract and an executable
verifier. The verifier writes raw results and is accompanied by an
independent checker, a negative control, a source audit, and a limitations
record. The evaluator-facing summaries are under
[`candidate_space/pages/current`](candidate_space/pages/current).

| Claim | Paper statement and reproduction | Verdict | Primary evidence |
| --- | --- | --- | --- |
| 1. Wasserstein LSE formulation | Checks the exact Gaussian specialization, analytic mean gradient against an independent central finite difference, stored-pattern energy ordering, and a sign-reversed control. Gradient error: `8.70e-11`. | **VERIFIED** | [Claim page](candidate_space/pages/current/claim-1.md) · [`reproduction/claims/claim_1`](reproduction/claims/claim_1) |
| 2. Exponential storage capacity | Reconstructs the theorem certificate with `p=0.1`, `lambda_min=1`, `lambda_max=1.1`, `beta=3`, and conservative `d0=364`; independently calibrates capacity without choosing the search grid from the claimed formula. | **VERIFIED** | [Claim page](candidate_space/pages/current/claim-2.md) · [`reproduction/claims/claim_2`](reproduction/claims/claim_2) |
| 3. Dimension-dependent retrieval decay | Checks the proof rate `-alpha²/32`, a log-domain certificate, 1,345 queries across dimensions, and 15 long-double direct computations. Fitted slope: `-4.4827`; required upper rate: `-0.02047`. | **VERIFIED** | [Claim page](candidate_space/pages/current/claim-3.md) · [`reproduction/claims/claim_3`](reproduction/claims/claim_3) |
| 4. Synthetic temperature separation | Reproduces `N=10000`, `d=50`, three seeds, both radii, and beta `1` versus `0.1`; beta `1` retrieves `100%`, while beta `0.1` retrieves `0%`. A scalar implementation agrees within `1.01e-15`. | **VERIFIED** | [Claim page](candidate_space/pages/current/claim-4.md) · [`reproduction/claims/claim_4`](reproduction/claims/claim_4) |
| 5. Text8 phase transition | Recovers the executed author notebook protocol and checks the transition over 20 beta values. Author output goes from `31%` to `98%`; independent seeds go from `79–83%` to `100%`. | **VERIFIED** | [Claim page](candidate_space/pages/current/claim-5.md) · [`reproduction/claims/claim_5`](reproduction/claims/claim_5) |
| 6. Non-commuting one-step convergence | Tests `N=1000`, `d=10`, full-rank non-commuting Gaussians, both radii, an alternative rank-one PSD law, independent checks, controls, and the v1 Figure 8(b) audit. At `100r`, one-step error remains `0.565–0.595`; no query reaches `1e-6`. | **FALSIFIED** | [Claim page](candidate_space/pages/current/claim-6.md) · [`reproduction/claims/claim_6`](reproduction/claims/claim_6) |

### How a verdict is produced

1. The claim contract fixes the source section, assumptions, quantifiers,
   thresholds, and verdict rule.
2. The source audit records the paper version, hashes, ambiguities, and
   any recovered author artifact used by the test.
3. The verifier executes the experiment or proof-level certificate and
   writes JSON/CSV results under `.openresearch/artifacts/`.
4. An independent checker recomputes key values from the saved evidence;
   a negative control must fail or separate as specified.
5. `reproduction.run` executes the cumulative suite and returns a nonzero
   status if any required predicate fails.

For Claims 2 and 3, the decisive evidence is a reconstructed proof
certificate; finite experiments are calibration. For Claim 6,
**FALSIFIED** means an assumption-satisfying counterexample passed every
required predicate. It does not mean that every non-commuting Gaussian
memory fails or that the broader update rule is invalid.

## Branches

`main` is the publication surface. The complete old-to-clean branch
mapping and each branch's purpose are documented in
[branch-audit.md](branch-audit.md).

| Clean branch | Purpose |
| --- | --- |
| `audit/baseline-claim-1-regression` | Preserve the judged baseline and regress Claim 1. |
| `experiment/claim-2-capacity-scaling` | Reconstruct and calibrate the capacity claim. |
| `experiment/claim-3-dimension-decay` | Test dimension-dependent retrieval decay. |
| `experiment/claim-4-temperature-separation` | Run the exact-scale synthetic beta comparison. |
| `experiment/claim-5-author-text8` | Reproduce the recovered author Text8 protocol. |
| `audit/claim-5-text8-transition-band` | Audit the source-faithful Text8 transition band. |
| `audit/claim-6-noncommuting-retrieval` | Check exact non-commuting retrieval trajectories. |
| `audit/claim-6-falsification` | Audit the source-consistent Claim 6 falsification. |
| `audit/evaluator-claim-1` | Keep evaluator-visible Claim 1 evidence. |
| `release/evaluator-visible-candidate` | Assemble the evaluator-facing release candidate. |

Branch names describe the work they contain; they are not separate paper
versions or competing final results. Historical `orx/` names are retained
only in the audit for provenance.

## Repository map

| Path | Role |
| --- | --- |
| `reproduction/claims/claim_{1..6}` | Claim contracts, methods, source audits, verifiers, and limitations. |
| `candidate_space/pages/current` | Self-contained evaluator-facing claim pages and version audit. |
| `candidate_space/evidence` | Published claim evidence, raw outputs, controls, and runtime records. |
| `reports/reproduction` | Illustrated technical report and release forecast. |
| `notebooks/ddam_reproduction.py` | Self-contained marimo reading/tutorial surface. |
| `.openresearch/artifacts` | Machine-readable run artifacts produced by the cumulative suite. |

## Reproduce locally

```bash
uv sync --frozen
uv run python -m reproduction.run
```

The accepted cumulative run used Hugging Face `cpu-upgrade`, provisioned
with 8 vCPUs and 32 GB. It completed in `16m24s`, used no GPU, peaked at
about `1.47 GiB` RSS, and cost approximately `$0.0082`. Text8 uses the
canonical 17,005,207-token corpus but follows the recovered executed
author configuration, which trains on only the first 100,000 tokens; that
material paper/code discrepancy is disclosed in the Claim 5 page.

To read the artifacts without rerunning the expensive suite:

```bash
marimo edit notebooks/ddam_reproduction.py
marimo run notebooks/ddam_reproduction.py
```

## Scope and limitations

- The mathematical claims are checked for the stated Gaussian fixtures
  and assumptions, not for every distribution in `P_2(R^d)`.
- A proof certificate is an executable reconstruction, not a formal proof
  checked by a proof assistant.
- Claim 4 leaves the paper's mean/covariance perturbation split ambiguous;
  this reproduction documents and fixes an equal split.
- Claim 5 preserves the historical author run as a separate anchor; the
  independent trainer batches ranking pairs instead of reproducing the
  abandoned sequential Cython implementation byte-for-byte.
- Claim 6 is a narrow falsification of the v1 one-step empirical statement,
  not a universal negative result about non-commuting retrieval.
- This repository is an independent reproduction and is not author-
  endorsed.

## Citation

```bibtex
@article{tankala2025dense,
  title={Dense associative memory for Gaussian distributions},
  author={Tankala, Chandan and Balasubramanian, Krishnakumar},
  journal={arXiv preprint arXiv:2509.23162},
  year={2025},
  doi={10.48550/arXiv.2509.23162}
}
```

Machine-readable citation metadata is also available in
[`CITATION.cff`](CITATION.cff), and the author note is kept separately in
[`AUTHOR_THANK_YOU.md`](AUTHOR_THANK_YOU.md).

## Thank you

Thank you to Chandan Tankala and Krishnakumar Balasubramanian for
developing and sharing this work, its mathematical formulation, and the
artifacts that made an independent audit possible. Their paper and
publicly recoverable experiment traces made it possible to separate
theorem-level evidence, empirical reproduction, and falsification checks
instead of treating every reported number as a single undifferentiated
result.

Documentation and cleanup in this repository are maintained by
[MachineLearning-Nerd](https://github.com/MachineLearning-Nerd). The
attribution applies to this reproduction work and does not change the
provenance of the paper or the authors' artifacts.
