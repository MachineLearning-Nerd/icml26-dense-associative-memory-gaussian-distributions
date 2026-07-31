import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
IMAGES = Path(__file__).resolve().parent / "images"
IMAGES.mkdir(exist_ok=True)

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#15803d"
PURPLE = "#7e22ce"
GRAY = "#64748b"

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "svg.hashsalt": "openresearch-ddam",
    }
)


def read_csv(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def save(figure, name):
    figure.tight_layout()
    figure.savefig(
        IMAGES / name,
        format="svg",
        bbox_inches="tight",
        metadata={"Date": None},
    )
    plt.close(figure)


def headline():
    claim5 = json.loads(
        (ARTIFACTS / "claim_5" / "raw" / "result.json").read_text()
    )
    claim6 = read_csv(ARTIFACTS / "claim_6" / "raw" / "trajectories.csv")
    figure, axes = plt.subplots(1, 2, figsize=(11, 4.1))

    author = claim5["author_notebook_audit"]["phase_curve"]
    axes[0].plot(
        [row["beta"] for row in author],
        [row["retrieval_rate"] for row in author],
        color="black",
        linewidth=2.4,
        marker="o",
        markersize=3,
        label="executed author notebook",
    )
    for color, sweep in zip([BLUE, ORANGE, GREEN], claim5["phase_sweeps"]):
        axes[0].plot(
            [row["beta"] for row in sweep["curve"]],
            [row["retrieval_rate"] for row in sweep["curve"]],
            color=color,
            linewidth=1.7,
            marker=".",
            label=f"independent seed {sweep['seed']}",
        )
    axes[0].axvspan(7.8476, 16.2378, color=PURPLE, alpha=0.1)
    axes[0].axvline(15, color=PURPLE, linestyle="--", linewidth=1)
    axes[0].set_xscale("log")
    axes[0].set_ylim(-0.03, 1.05)
    axes[0].set_xlabel(r"temperature parameter $\beta$")
    axes[0].set_ylabel("retrieval success")
    axes[0].set_title("Text8: the phase transition is reproducible")
    axes[0].legend(fontsize=7, loc="lower right")

    by_iteration = defaultdict(list)
    for row in claim6:
        if (
            row["kind"].strip('"') == "large_radius_trajectory"
            and float(row["beta"]) == 1
        ):
            by_iteration[int(row["iteration"])].append(
                float(row["mean_w2_error"])
            )
    iterations = sorted(by_iteration)
    means = np.array([np.mean(by_iteration[i]) for i in iterations])
    lows = np.array([np.min(by_iteration[i]) for i in iterations])
    highs = np.array([np.max(by_iteration[i]) for i in iterations])
    paper_audit = json.loads(
        (ARTIFACTS / "claim_6" / "source_figure_audit.json").read_text()
    )
    paper_values = paper_audit["digitized_mean_w2_by_iteration"]
    axes[1].plot(
        iterations,
        means,
        marker="o",
        color=ORANGE,
        linewidth=2,
        label="reproduction, 3 seeds",
    )
    axes[1].fill_between(iterations, lows, highs, color=ORANGE, alpha=0.15)
    axes[1].plot(
        range(len(paper_values)),
        paper_values,
        marker="s",
        color="black",
        linestyle="--",
        label="digitized paper Figure 8(b)",
    )
    axes[1].set_yscale("log")
    axes[1].set_xlabel("retrieval update")
    axes[1].set_ylabel("mean Wasserstein error")
    axes[1].set_title("Non-commuting: the paper's own curve refutes one step")
    axes[1].legend(fontsize=7)
    save(figure, "headline-results.svg")


def capacity():
    rows = read_csv(
        ARTIFACTS / "claim_2" / "raw" / "calibration_sweep.csv"
    )
    groups = defaultdict(list)
    for row in rows:
        groups[(int(row["seed"]), int(row["dimension"]))].append(row)
    figure, axis = plt.subplots(figsize=(7.4, 4.3))
    for seed in sorted({key[0] for key in groups}):
        dimensions = []
        last_passes = []
        first_failures = []
        for dimension in sorted({key[1] for key in groups if key[0] == seed}):
            group = groups[(seed, dimension)]
            passed = [int(row["count"]) for row in group if row["passed"] == "True"]
            failed = [int(row["count"]) for row in group if row["passed"] == "False"]
            dimensions.append(dimension)
            last_passes.append(max(passed))
            first_failures.append(min(failed) if failed else np.nan)
        axis.plot(
            dimensions,
            last_passes,
            marker="o",
            linewidth=1,
            alpha=0.65,
            label=f"seed {seed}",
        )
        axis.scatter(dimensions, first_failures, marker="x", alpha=0.5)
    axis.set_yscale("log", base=2)
    axis.set_xlabel("dimension")
    axis.set_ylabel("pattern count")
    axis.set_title("Capacity calibration: last pass (●), first failure (×)")
    axis.legend(ncol=2, fontsize=7)
    axis.grid(axis="y", alpha=0.2)
    save(figure, "capacity-scaling.svg")


def dimension_decay():
    rows = read_csv(ARTIFACTS / "claim_3" / "raw" / "dimension_sweep.csv")
    by_dimension = defaultdict(list)
    bounds = {}
    for row in rows:
        dimension = int(row["dimension"])
        by_dimension[dimension].append(float(row["log_error_upper"]))
        bounds[dimension] = float(row["log_theorem_bound"])
    dimensions = sorted(by_dimension)
    medians = np.array([np.median(by_dimension[d]) for d in dimensions])
    q1 = np.array([np.quantile(by_dimension[d], 0.25) for d in dimensions])
    q3 = np.array([np.quantile(by_dimension[d], 0.75) for d in dimensions])
    figure, axis = plt.subplots(figsize=(7.4, 4.3))
    axis.plot(dimensions, medians, color=BLUE, marker="o", label="observed median")
    axis.fill_between(dimensions, q1, q3, color=BLUE, alpha=0.15, label="IQR")
    axis.plot(
        dimensions,
        [bounds[d] for d in dimensions],
        color=ORANGE,
        linestyle="--",
        marker="s",
        label="Theorem 3 upper bound",
    )
    axis.set_xlabel("dimension")
    axis.set_ylabel("log one-step Wasserstein error")
    axis.set_title("Retrieval error decays with dimension, not just iteration")
    axis.legend(fontsize=8)
    axis.grid(alpha=0.2)
    save(figure, "dimension-decay.svg")


def temperature_separation():
    rows = read_csv(ARTIFACTS / "claim_4" / "raw" / "trajectories.csv")
    groups = defaultdict(list)
    for row in rows:
        key = (
            float(row["beta"]),
            int(row["radius_multiplier"]),
            int(row["iteration"]),
        )
        groups[key].append(float(row["mean_w2_error"]))
    figure, axis = plt.subplots(figsize=(7.4, 4.3))
    styles = {
        (1.0, 1): (BLUE, "-", r"$\beta=1$, radius $r$"),
        (1.0, 100): (GREEN, "-", r"$\beta=1$, radius $100r$"),
        (0.1, 1): (ORANGE, "--", r"$\beta=0.1$, radius $r$"),
        (0.1, 100): (PURPLE, "--", r"$\beta=0.1$, radius $100r$"),
    }
    for (beta, radius), (color, style, label) in styles.items():
        iterations = sorted(
            key[2]
            for key in groups
            if key[0] == beta and key[1] == radius
        )
        values = [
            max(np.mean(groups[(beta, radius, iteration)]), 1e-18)
            for iteration in iterations
        ]
        axis.plot(
            iterations,
            values,
            color=color,
            linestyle=style,
            marker="o",
            label=label,
        )
    axis.set_yscale("log")
    axis.set_xlabel("retrieval update")
    axis.set_ylabel("mean Wasserstein error")
    axis.set_title(r"Exact $N=10{,}000$, $d=50$ temperature separation")
    axis.legend(fontsize=8)
    axis.grid(alpha=0.2)
    save(figure, "temperature-separation.svg")


headline()
capacity()
dimension_decay()
temperature_separation()
