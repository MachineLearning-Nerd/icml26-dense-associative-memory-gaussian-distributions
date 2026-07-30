import json
from pathlib import Path

import numpy as np

from reproduction import core


def fixture():
    rng = np.random.default_rng(20260730)
    patterns = []
    for _ in range(5):
        mean = rng.normal(0, 5, size=2)
        matrix = rng.normal(size=(2, 2))
        covariance = matrix @ matrix.T + np.eye(2)
        patterns.append((mean, covariance))
    return patterns


def finite_difference(query, patterns, beta, step=1e-5):
    gradient = np.zeros_like(query[0])
    for coordinate in range(len(gradient)):
        plus_mean = query[0].copy()
        minus_mean = query[0].copy()
        plus_mean[coordinate] += step
        minus_mean[coordinate] -= step
        plus = core.energy((plus_mean, query[1]), patterns, beta)
        minus = core.energy((minus_mean, query[1]), patterns, beta)
        gradient[coordinate] = (plus - minus) / (2 * step)
    return gradient


def verify(output_dir):
    patterns = fixture()
    beta = 8.0
    query = (np.array([0.5, -0.3]), np.eye(2))
    distances = np.array([core.wasserstein_squared(pattern, query) for pattern in patterns])
    direct_energy = float(-np.log(np.exp(-beta * distances).sum()) / beta)
    implemented_energy = core.energy(query, patterns, beta)
    analytic_gradient = core.mean_gradient(query, patterns, beta)
    numerical_gradient = finite_difference(query, patterns, beta)
    gradient_error = float(np.max(np.abs(analytic_gradient - numerical_gradient)))

    stored_energies = [core.energy(pattern, patterns, beta) for pattern in patterns]
    centroid = (
        np.mean(np.stack([mean for mean, _ in patterns]), axis=0),
        np.mean(np.stack([covariance for _, covariance in patterns]), axis=0),
    )
    centroid_energy = core.energy(centroid, patterns, beta)

    reversed_gradient_error = float(
        np.max(np.abs(-analytic_gradient - numerical_gradient))
    )
    checks = {
        "formula_matches": abs(implemented_energy - direct_energy) <= 1e-12,
        "gradient_matches": gradient_error <= 1e-6,
        "stored_below_centroid": max(stored_energies) < centroid_energy,
        "negative_control_rejected": reversed_gradient_error >= 0.1,
    }
    result = {
        "claim_id": 1,
        "verdict": "VERIFIED" if all(checks.values()) else "BLOCKED",
        "beta": beta,
        "seed": 20260730,
        "implemented_energy": implemented_energy,
        "direct_energy": direct_energy,
        "analytic_gradient": analytic_gradient.tolist(),
        "finite_difference_gradient": numerical_gradient.tolist(),
        "gradient_max_abs_error": gradient_error,
        "stored_energies": stored_energies,
        "centroid_energy": centroid_energy,
        "negative_control": {
            "name": "sign-reversed gradient",
            "max_abs_error": reversed_gradient_error,
            "rejected": checks["negative_control_rejected"],
        },
        "checks": checks,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    if result["verdict"] != "VERIFIED":
        raise SystemExit(json.dumps(result, indent=2))
    return result

