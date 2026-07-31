# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "marimo==0.23.15",
#   "matplotlib==3.10.9",
#   "numpy==2.2.6",
# ]
# ///

import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # Dense associative memory for Gaussian distributions

    **A self-contained reproduction of all six judged claims.**
    Claims 1–5 are VERIFIED; the exact non-commuting one-step claim
    is FALSIFIED. The evidence below is embedded, so opening this
    notebook does not rerun the expensive experiments.
    """)
    return


@app.cell
def _(np, plt):
    evidence_betas = np.logspace(-1, 2, 20)
    evidence_author = np.array(
        [0] * 13 + [0.31, 0.98] + [1] * 5,
        dtype=float,
    )
    evidence_seeds = {
        42: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.38, 0.83, 1, 1, 1, 1, 1, 1],
        43: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.32, 0.83, 1, 1, 1, 1, 1, 1],
        44: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.01, 0.30, 0.79, 1, 1, 1, 1, 1, 1],
    }
    evidence_claim6_reproduction = np.array(
        [3.1623, 0.5838, 0.225, 0.161, 0.151, 0.162]
    )
    evidence_claim6_paper = np.array(
        [3.1538, 0.6205, 0.2257, 0.1658, 0.1580, 0.1580]
    )

    headline_fig, headline_axes = plt.subplots(1, 2, figsize=(10, 3.6))
    headline_axes[0].plot(
        evidence_betas,
        evidence_author,
        color="black",
        linewidth=2.2,
        marker="o",
        markersize=3,
        label="executed author notebook",
    )
    for evidence_seed, evidence_curve in evidence_seeds.items():
        headline_axes[0].plot(
            evidence_betas,
            evidence_curve,
            marker=".",
            label=f"independent seed {evidence_seed}",
        )
    headline_axes[0].axvspan(7.8476, 16.2378, color="#7e22ce", alpha=0.1)
    headline_axes[0].axvline(15, color="#7e22ce", linestyle="--")
    headline_axes[0].set_xscale("log")
    headline_axes[0].set_ylim(-0.03, 1.05)
    headline_axes[0].set_title("Text8 phase transition")
    headline_axes[0].set_xlabel(r"$\beta$")
    headline_axes[0].set_ylabel("retrieval success")
    headline_axes[0].legend(fontsize=6)

    evidence_iterations = np.arange(6)
    headline_axes[1].plot(
        evidence_iterations,
        evidence_claim6_reproduction,
        marker="o",
        label="reproduction",
    )
    headline_axes[1].plot(
        evidence_iterations,
        evidence_claim6_paper,
        marker="s",
        linestyle="--",
        color="black",
        label="paper Figure 8(b)",
    )
    headline_axes[1].set_yscale("log")
    headline_axes[1].set_title("Non-commuting error persists")
    headline_axes[1].set_xlabel("retrieval update")
    headline_axes[1].set_ylabel("mean Wasserstein error")
    headline_axes[1].legend(fontsize=7)
    headline_fig.tight_layout()
    headline_fig
    return evidence_betas, evidence_seeds


@app.cell
def _(mo):
    mo.md(r"""
    ## Central idea

    A memory stores Gaussian measures \(X_i\) using the log-sum-exp
    Wasserstein energy

    \[
    E(\xi)=-\frac{1}{\beta}\log\sum_i
    \exp\{-\beta W_2^2(X_i,\xi)\}.
    \]

    The Gibbs weights favor nearby stored measures. The retrieval
    operator takes their Wasserstein barycenter. Large \(\beta\)
    creates sharp local basins; small \(\beta\) averages broadly.

    The formal reproduction command is:

    ```bash
    uv sync --frozen && uv run python -m reproduction.run
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## What the evidence establishes

    | Claim | Direct evidence | Verdict |
    | --- | --- | --- |
    | Energy and gradient | formula exact; finite-difference error `8.70e-11` | VERIFIED |
    | Exponential capacity | proof certificate; calibrated slope `0.12390` | VERIFIED |
    | Dimension decay | proof certificate; fitted slope `-4.4827` | VERIFIED |
    | Synthetic temperature | exact `N=10000,d=50`: 100% vs 0% | VERIFIED |
    | Text8 transition | author 31→98%; new seeds 79–83→100% | VERIFIED |
    | Non-commuting one step | new and archived errors remain nonzero | FALSIFIED |

    Finite experiments are not used as proofs of universal
    quantifiers. Claims 2 and 3 therefore include independently
    reconstructed symbolic/numerical certificates.
    """)
    return


@app.cell
def _(mo):
    beta_slider = mo.ui.slider(
        start=0,
        stop=19,
        step=1,
        value=14,
        label="Explore a measured beta-grid index",
        show_value=True,
    )
    beta_slider
    return (beta_slider,)


@app.cell
def _(beta_slider, evidence_betas, evidence_seeds, mo, np):
    explorer_index = int(beta_slider.value)
    explorer_rates = np.array(
        [curve[explorer_index] for curve in evidence_seeds.values()]
    )
    mo.md(
        f"""
        **Illustrative explorer — not additional formal evidence.**

        At measured beta `{evidence_betas[explorer_index]:.4g}`, the
        three independent retrieval rates are
        `{", ".join(f"{rate:.0%}" for rate in explorer_rates)}`.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Reproducibility notes

    The canonical Text8 archive and deleted executed author notebook
    are hash-pinned. Every claim has a machine-readable contract,
    raw JSON/CSV, an independent checker, a negative control,
    deterministic seeds, and a nonzero exit on rejection.

    The successful cumulative run used HF `cpu-upgrade`
    (8 provisioned vCPUs, 32 GB), completed in 16m24s, and cost about
    `$0.0082`. This notebook intentionally embeds only the compact
    accepted results; see the repository report and claim pages for
    complete raw evidence and limitations.
    """)
    return


if __name__ == "__main__":
    app.run()
