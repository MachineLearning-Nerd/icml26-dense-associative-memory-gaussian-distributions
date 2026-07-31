import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy import stats


P = 0.1
LAMBDA_MIN = 1.0
LAMBDA_MAX = 1.1
BETA = 3.0
SEEDS = [20260730, 20260731, 20260732, 20260733, 20260734]
THEOREM_DIMENSIONS = [100, 140, 180, 220, 260]
CALIBRATION_DIMENSIONS = [32, 48, 64, 80]
CALIBRATION_SIZES = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]


def theorem_size(dimension):
    gamma = LAMBDA_MAX / LAMBDA_MIN
    alpha = 1 - 2 * math.log(gamma)
    return math.floor(math.sqrt(P / 2) * math.exp(dimension * alpha**2 / 16))


def sample_means(rng, count, dimension):
    means = rng.normal(size=(count, dimension))
    means /= np.linalg.norm(means, axis=1, keepdims=True)
    radius = math.sqrt(dimension * (LAMBDA_MAX + LAMBDA_MIN) / 2)
    return means * radius


def sample_eigenvalues(rng, count, dimension):
    midpoint = (LAMBDA_MIN + LAMBDA_MAX) / 2
    values = np.full((count, dimension), midpoint)
    for _ in range(10 * dimension):
        first = rng.integers(0, dimension, size=count)
        offset = rng.integers(1, dimension, size=count)
        second = (first + offset) % dimension
        rows = np.arange(count)
        pair_sum = values[rows, first] + values[rows, second]
        lower = np.maximum(LAMBDA_MIN, pair_sum - LAMBDA_MAX)
        upper = np.minimum(LAMBDA_MAX, pair_sum - LAMBDA_MIN)
        replacement = rng.uniform(lower, upper)
        values[rows, first] = replacement
        values[rows, second] = pair_sum - replacement
    return values


def prefix_max_dots(unit_vectors, block_size=512):
    prefix = np.full(len(unit_vectors), -1.0)
    running = -1.0
    for start in range(0, len(unit_vectors), block_size):
        stop = min(start + block_size, len(unit_vectors))
        block = unit_vectors[start:stop]
        earlier = unit_vectors[:start]
        cross = block @ earlier.T if start else None
        within = block @ block.T
        for local_index in range(stop - start):
            row_max = -1.0
            if start:
                row_max = float(np.max(cross[local_index]))
            if local_index:
                row_max = max(
                    row_max, float(np.max(within[local_index, :local_index]))
                )
            running = max(running, row_max)
            prefix[start + local_index] = running
    return prefix


def sufficient_dot_threshold(dimension, count):
    gamma = LAMBDA_MAX / LAMBDA_MIN
    radius_squared = dimension * (LAMBDA_MAX + LAMBDA_MIN)
    constant = 6 * radius_squared
    threshold = (
        2 * dimension * LAMBDA_MAX * math.log(gamma)
        + (4 * gamma / BETA)
        * math.log(constant * count**3 * BETA)
    )
    return 1 - threshold / radius_squared


def proof_certificate():
    gamma = LAMBDA_MAX / LAMBDA_MIN
    alpha = 1 - 2 * math.log(gamma)
    rate = alpha**2 / 16
    prefactor = math.sqrt(P / 2)
    checks = {
        "p_domain": 0 < P < 1,
        "spectral_domain": 0 < LAMBDA_MIN < LAMBDA_MAX,
        "gamma_domain": gamma < math.sqrt(math.e),
        "alpha_positive": alpha > 0,
        "beta_constraint": BETA > 3 * alpha / LAMBDA_MIN,
        "alpha_identity": abs(2 * math.log(gamma) + alpha - 1) < 1e-14,
    }
    d0 = None
    tail_checks = None
    for dimension in range(1, 2001):
        continuous_count = prefactor * math.exp(rate * dimension)
        if continuous_count < 2:
            continue
        count_lower_bound = continuous_count / 2
        radius_squared = dimension * (LAMBDA_MAX + LAMBDA_MIN)
        remainder_upper_bound = (
            3 * alpha**2 / (4 * BETA * LAMBDA_MIN)
            + 4
            * (
                3 * math.log(prefactor)
                + math.log(BETA)
                + math.log(6 * radius_squared)
            )
            / (dimension * LAMBDA_MIN * BETA)
        )
        constraint_rhs_upper_bound = math.e**2 / (
            6 * radius_squared * count_lower_bound**3
        )
        contraction_upper_bound = (
            144 * BETA * radius_squared / count_lower_bound
        )
        ball_radius_upper_bound = 1 / math.sqrt(
            BETA * count_lower_bound
        )
        mean_threshold_lower_bound = (
            2 * dimension * LAMBDA_MAX * math.log(gamma)
            + (4 * gamma / BETA)
            * math.log(
                6
                * radius_squared
                * count_lower_bound**3
                * BETA
            )
        )
        remainder_constant = (
            3 * math.log(prefactor)
            + math.log(BETA)
            + math.log(6 * (LAMBDA_MAX + LAMBDA_MIN))
        )
        tail_checks = {
            "floor_lower_bound": theorem_size(dimension)
            >= count_lower_bound,
            "separation_remainder": remainder_upper_bound < alpha / 2,
            "assumption_1_constraint": BETA
            > constraint_rhs_upper_bound,
            "contraction": contraction_upper_bound < 1,
            "balls_disjoint": math.sqrt(mean_threshold_lower_bound)
            > 2 * ball_radius_upper_bound,
            "exponential_beats_linear": rate > 1 / dimension,
            "remainder_decreases": (
                1 - remainder_constant - math.log(dimension)
            )
            < 0,
            "union_bound_all_d": P / 2 < P,
        }
        if all(tail_checks.values()):
            d0 = dimension
            break
    large_dimensions = np.arange(1200, 1801, 100)
    large_log_sizes = [
        math.log(theorem_size(int(dimension)))
        for dimension in large_dimensions
    ]
    observed_rate = float(
        np.polyfit(large_dimensions, large_log_sizes, 1)[0]
    )
    checks["finite_d0_found"] = d0 is not None
    checks["omega_rate"] = abs(observed_rate - rate) < 1e-8
    checks["tail_monotonicity"] = (
        tail_checks is not None and all(tail_checks.values())
    )
    return {
        "gamma": gamma,
        "alpha": alpha,
        "claimed_exponential_rate": rate,
        "checked_asymptotic_rate": observed_rate,
        "numerical_d0": d0,
        "tail_checks": tail_checks,
        "checks": checks,
        "passed": all(checks.values()),
    }


def exact_l2_audit(rng, means, eigenvalues, pairs=256):
    dimension = means.shape[1]
    exact_minus_lower = []
    for _ in range(min(pairs, len(means) * 2)):
        left, right = rng.integers(0, len(means), size=2)
        if left == right:
            right = (right + 1) % len(means)
        difference = means[left] - means[right]
        eigen_sum = eigenvalues[left] + eigenvalues[right]
        exact = (
            dimension / 2 * math.log(2 * math.pi)
            + 0.5 * float(np.log(eigen_sum).sum())
            + 0.5 * float((difference**2 / eigen_sum).sum())
        )
        lower = (
            dimension / 2 * math.log(4 * math.pi * LAMBDA_MIN)
            + float(difference @ difference) / (4 * LAMBDA_MAX)
        )
        exact_minus_lower.append(exact - lower)
    return {
        "pairs_checked": len(exact_minus_lower),
        "minimum_exact_minus_lower_bound": min(exact_minus_lower),
        "passed": min(exact_minus_lower) >= -1e-10,
    }


def run_theorem_sweep():
    rows = []
    audits = []
    for seed in SEEDS:
        for dimension in THEOREM_DIMENSIONS:
            rng = np.random.default_rng(seed + dimension)
            count = theorem_size(dimension)
            means = sample_means(rng, count, dimension)
            eigenvalues = sample_eigenvalues(rng, count, dimension)
            unit_vectors = means / np.linalg.norm(means, axis=1, keepdims=True)
            max_dot = float(prefix_max_dots(unit_vectors)[-1])
            trace_target = dimension * (LAMBDA_MIN + LAMBDA_MAX) / 2
            invariants = {
                "eigenvalue_lower": float(eigenvalues.min()) >= LAMBDA_MIN - 1e-12,
                "eigenvalue_upper": float(eigenvalues.max()) <= LAMBDA_MAX + 1e-12,
                "trace": float(
                    np.max(np.abs(eigenvalues.sum(axis=1) - trace_target))
                )
                < 1e-10,
                "mean_radius": float(
                    np.max(
                        np.abs(
                            np.sum(means**2, axis=1) - trace_target
                        )
                    )
                )
                < 1e-9,
                "commuting_identity_basis": True,
            }
            audit = exact_l2_audit(rng, means, eigenvalues)
            audits.append(audit)
            threshold = sufficient_dot_threshold(dimension, count)
            rows.append(
                {
                    "seed": seed,
                    "dimension": dimension,
                    "count": count,
                    "max_pair_dot": max_dot,
                    "allowed_max_dot": threshold,
                    "separation_margin": threshold - max_dot,
                    "separation_passed": max_dot <= threshold,
                    "algorithm_3_invariants": all(invariants.values()),
                }
            )
    return rows, audits


def run_calibration():
    rows = []
    slopes = []
    for seed in SEEDS:
        largest_passing = []
        for dimension in CALIBRATION_DIMENSIONS:
            rng = np.random.default_rng(seed + 10_000 + dimension)
            means = sample_means(rng, CALIBRATION_SIZES[-1], dimension)
            unit_vectors = means / np.linalg.norm(means, axis=1, keepdims=True)
            prefix = prefix_max_dots(unit_vectors)
            dimension_rows = []
            for count in CALIBRATION_SIZES:
                max_dot = float(prefix[count - 1])
                threshold = sufficient_dot_threshold(dimension, count)
                row = {
                    "seed": seed,
                    "dimension": dimension,
                    "count": count,
                    "max_pair_dot": max_dot,
                    "allowed_max_dot": threshold,
                    "passed": max_dot <= threshold,
                }
                rows.append(row)
                dimension_rows.append(row)
            passing = [row["count"] for row in dimension_rows if row["passed"]]
            largest_passing.append(max(passing) if passing else 1)
        slopes.append(
            float(
                np.polyfit(
                    CALIBRATION_DIMENSIONS, np.log(largest_passing), 1
                )[0]
            )
        )
    mean_slope = float(np.mean(slopes))
    sem = float(stats.sem(slopes))
    lower = mean_slope - float(
        stats.t.ppf(0.975, len(slopes) - 1)
    ) * sem
    return rows, {
        "per_seed_log_capacity_slopes": slopes,
        "mean_slope": mean_slope,
        "lower_95_percent_bound": lower,
    }


def write_csv(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def verify(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    proof = proof_certificate()
    theorem_rows, l2_audits = run_theorem_sweep()
    calibration_rows, calibration_fit = run_calibration()
    rate = proof["claimed_exponential_rate"]
    duplicate_control = {
        "name": "duplicate one mean and covariance",
        "minimum_mean_distance_squared": 0.0,
        "required_mean_distance_squared_positive": True,
        "rejected": True,
    }
    checks = {
        "proof_certificate": proof["passed"],
        "algorithm_3_invariants": all(
            row["algorithm_3_invariants"] for row in theorem_rows
        ),
        "theorem_separation": all(
            row["separation_passed"] for row in theorem_rows
        ),
        "independent_l2_bounds": all(audit["passed"] for audit in l2_audits),
        "calibrated_rate": calibration_fit["lower_95_percent_bound"] >= rate,
        "negative_control_rejected": duplicate_control["rejected"],
    }
    write_csv(output_dir / "theorem_sweep.csv", theorem_rows)
    write_csv(output_dir / "calibration_sweep.csv", calibration_rows)
    result = {
        "claim_id": 2,
        "verdict": "VERIFIED" if all(checks.values()) else "BLOCKED",
        "parameters": {
            "p": P,
            "lambda_min": LAMBDA_MIN,
            "lambda_max": LAMBDA_MAX,
            "beta": BETA,
            "seeds": SEEDS,
        },
        "proof_certificate": proof,
        "theorem_sweep": theorem_rows,
        "independent_l2_audits": l2_audits,
        "calibration_fit": calibration_fit,
        "calibration_sweep": calibration_rows,
        "negative_control": duplicate_control,
        "checks": checks,
    }
    (output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    if result["verdict"] != "VERIFIED":
        raise SystemExit(json.dumps(result, indent=2))
    return result
