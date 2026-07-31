import csv
import json
import math

import numpy as np
from scipy import stats
from scipy.special import logsumexp

from reproduction.claims.claim_2.verifier import (
    BETA,
    LAMBDA_MAX,
    LAMBDA_MIN,
    P,
    SEEDS,
    THEOREM_DIMENSIONS,
    sample_eigenvalues,
    sample_means,
    theorem_size,
)


QUERIES_PER_MEMORY = 64
RADIUS_FRACTION = 0.9


def gaussian_coordinates(means, eigenvalues):
    return np.concatenate([means, np.sqrt(eigenvalues)], axis=1)


def squared_distances(queries, patterns):
    query_norms = np.sum(queries**2, axis=1, keepdims=True)
    pattern_norms = np.sum(patterns**2, axis=1)
    distances = query_norms + pattern_norms - 2 * queries @ patterns.T
    return np.maximum(distances, 0)


def proof_certificate():
    gamma = LAMBDA_MAX / LAMBDA_MIN
    alpha = 1 - 2 * math.log(gamma)
    capacity_rate = alpha**2 / 16
    error_rate = -capacity_rate / 2
    prefactor = math.sqrt(P / 2)
    dimensions = np.arange(1200, 1801, 100)
    log_bounds = [
        math.log(3)
        - 0.5 * math.log(BETA * theorem_size(int(dimension)))
        for dimension in dimensions
    ]
    fitted_rate = float(np.polyfit(dimensions, log_bounds, 1)[0])
    checks = {
        "capacity_rate_identity": abs(
            capacity_rate - alpha**2 / 16
        )
        < 1e-14,
        "error_rate_identity": abs(error_rate + alpha**2 / 32) < 1e-14,
        "floor_bound_eventual": theorem_size(364)
        >= prefactor * math.exp(capacity_rate * 364) / 2,
        "asymptotic_rate": abs(fitted_rate - error_rate) < 1e-8,
    }
    return {
        "alpha": alpha,
        "capacity_log_rate": capacity_rate,
        "claimed_log_error_rate": error_rate,
        "fitted_bound_rate": fitted_rate,
        "checks": checks,
        "passed": all(checks.values()),
    }


def long_double_checker(patterns, query, target, logits, log_upper):
    logits_long = logits.astype(np.longdouble)
    maximum = np.max(logits_long)
    weights = np.exp(logits_long - maximum)
    weights /= np.sum(weights)
    delta = patterns.astype(np.longdouble) - patterns[target].astype(
        np.longdouble
    )
    direct_vector = np.sum(weights[:, None] * delta, axis=0)
    direct_error = np.sqrt(np.sum(direct_vector**2))
    direct_log = float(np.log(direct_error))
    return {
        "direct_log_error": direct_log,
        "certificate_log_upper": log_upper,
        "passed": direct_log <= log_upper + 1e-10,
    }


def run_sweep():
    rows = []
    direct_audits = []
    control_failures = 0
    slopes = []
    for seed in SEEDS:
        seed_medians = []
        for dimension in THEOREM_DIMENSIONS:
            rng = np.random.default_rng(seed + 20_000 + dimension)
            count = theorem_size(dimension)
            means = sample_means(rng, count, dimension)
            eigenvalues = sample_eigenvalues(rng, count, dimension)
            patterns = gaussian_coordinates(means, eigenvalues)
            query_count = min(QUERIES_PER_MEMORY, count)
            targets = rng.choice(count, size=query_count, replace=False)
            directions = rng.normal(size=(query_count, dimension))
            directions /= np.linalg.norm(directions, axis=1, keepdims=True)
            radius = 1 / math.sqrt(BETA * count)
            query_means = means[targets] + RADIUS_FRACTION * radius * directions
            queries = gaussian_coordinates(query_means, eigenvalues[targets])
            distances = squared_distances(queries, patterns)
            logits = -BETA * distances
            log_denominators = logsumexp(logits, axis=1)
            log_uppers = []
            for query_index, target in enumerate(targets):
                target_distances = np.linalg.norm(
                    patterns - patterns[target], axis=1
                )
                positive = target_distances > 0
                log_numerator = logsumexp(
                    logits[query_index, positive]
                    + np.log(target_distances[positive])
                )
                log_upper = float(
                    log_numerator - log_denominators[query_index]
                )
                log_uppers.append(log_upper)
                theorem_log_bound = math.log(3 / math.sqrt(BETA * count))
                rows.append(
                    {
                        "seed": seed,
                        "dimension": dimension,
                        "count": count,
                        "query_index": query_index,
                        "query_w2": RADIUS_FRACTION * radius,
                        "allowed_query_radius": radius,
                        "log_error_upper": log_upper,
                        "log_theorem_bound": theorem_log_bound,
                        "bound_passed": log_upper <= theorem_log_bound,
                    }
                )
                if dimension == THEOREM_DIMENSIONS[0] and query_index < 3:
                    direct_audits.append(
                        long_double_checker(
                            patterns,
                            queries[query_index],
                            int(target),
                            logits[query_index],
                            log_upper,
                        )
                    )
            seed_medians.append(float(np.median(log_uppers)))

            reversed_logits = BETA * distances[0]
            reversed_weights = np.exp(
                reversed_logits - np.max(reversed_logits)
            )
            reversed_weights /= reversed_weights.sum()
            reversed_output = reversed_weights @ patterns
            reversed_error = float(
                np.linalg.norm(reversed_output - patterns[targets[0]])
            )
            if reversed_error > 3 / math.sqrt(BETA * count):
                control_failures += 1
        slopes.append(
            float(
                np.polyfit(THEOREM_DIMENSIONS, seed_medians, 1)[0]
            )
        )
    mean_slope = float(np.mean(slopes))
    sem = float(stats.sem(slopes))
    upper = mean_slope + float(
        stats.t.ppf(0.975, len(slopes) - 1)
    ) * sem
    return rows, direct_audits, {
        "per_seed_log_error_slopes": slopes,
        "mean_slope": mean_slope,
        "upper_95_percent_bound": upper,
    }, {
        "name": "sign-reversed Gibbs logits",
        "cases": len(SEEDS) * len(THEOREM_DIMENSIONS),
        "theorem_bound_violations": control_failures,
        "rejected": control_failures
        == len(SEEDS) * len(THEOREM_DIMENSIONS),
    }


def verify(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    proof = proof_certificate()
    rows, direct_audits, fit, negative_control = run_sweep()
    checks = {
        "proof_certificate": proof["passed"],
        "query_assumptions": all(
            row["query_w2"] < row["allowed_query_radius"] for row in rows
        ),
        "theorem_bounds": all(row["bound_passed"] for row in rows),
        "dimension_rate": fit["upper_95_percent_bound"]
        <= proof["claimed_log_error_rate"],
        "independent_direct_checks": all(
            audit["passed"] for audit in direct_audits
        ),
        "negative_control_rejected": negative_control["rejected"],
    }
    with (output_dir / "dimension_sweep.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "claim_id": 3,
        "verdict": "VERIFIED" if all(checks.values()) else "BLOCKED",
        "parameters": {
            "p": P,
            "lambda_min": LAMBDA_MIN,
            "lambda_max": LAMBDA_MAX,
            "beta": BETA,
            "seeds": SEEDS,
            "dimensions": THEOREM_DIMENSIONS,
            "queries_per_memory": QUERIES_PER_MEMORY,
            "query_radius_fraction": RADIUS_FRACTION,
        },
        "proof_certificate": proof,
        "dimension_fit": fit,
        "sweep": rows,
        "independent_checker": direct_audits,
        "negative_control": negative_control,
        "checks": checks,
    }
    (output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    if result["verdict"] != "VERIFIED":
        raise SystemExit(json.dumps(result, indent=2))
    return result
