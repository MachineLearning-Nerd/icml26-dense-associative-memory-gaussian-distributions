import json
import math

import numpy as np
from scipy import stats


COUNT = 10_000
DIMENSION = 50
QUERY_COUNT = 7_500
LAMBDA_MIN = 1.0
LAMBDA_MAX = 1.1
BETAS = [1.0, 0.1]
RADIUS_MULTIPLIERS = [1, 100]
ITERATIONS = 3
THRESHOLD = 1e-6
SEEDS = [20260730, 20260731, 20260732]


def sample_algorithm_2(rng):
    target_sum = DIMENSION * (LAMBDA_MIN + LAMBDA_MAX) / 2
    eigenvalues = np.empty((COUNT, DIMENSION))
    pending = np.arange(COUNT)
    while len(pending):
        proposed = rng.uniform(
            LAMBDA_MIN,
            LAMBDA_MAX,
            size=(len(pending), DIMENSION - 1),
        )
        final = target_sum - proposed.sum(axis=1)
        accepted = (final >= LAMBDA_MIN) & (final <= LAMBDA_MAX)
        accepted_rows = pending[accepted]
        eigenvalues[accepted_rows, :-1] = proposed[accepted]
        eigenvalues[accepted_rows, -1] = final[accepted]
        pending = pending[~accepted]
    permutations = np.argsort(rng.random(size=eigenvalues.shape), axis=1)
    eigenvalues = np.take_along_axis(eigenvalues, permutations, axis=1)

    means = rng.normal(size=(COUNT, DIMENSION))
    means /= np.linalg.norm(means, axis=1, keepdims=True)
    means *= math.sqrt(target_sum)
    patterns = np.concatenate([means, np.sqrt(eigenvalues)], axis=1)
    invariants = {
        "count": len(patterns) == COUNT,
        "dimension": means.shape[1] == DIMENSION,
        "eigenvalue_bounds": float(eigenvalues.min()) >= LAMBDA_MIN
        and float(eigenvalues.max()) <= LAMBDA_MAX,
        "trace": float(
            np.max(np.abs(eigenvalues.sum(axis=1) - target_sum))
        )
        < 1e-10,
        "mean_radius": float(
            np.max(np.abs(np.sum(means**2, axis=1) - target_sum))
        )
        < 1e-10,
        "commuting_identity_basis": True,
    }
    return patterns, invariants


def perturb_queries(rng, patterns, targets, radius):
    mean_directions = rng.normal(size=(len(targets), DIMENSION))
    mean_directions /= np.linalg.norm(
        mean_directions, axis=1, keepdims=True
    )
    covariance_directions = rng.normal(size=(len(targets), DIMENSION))
    covariance_directions /= np.linalg.norm(
        covariance_directions, axis=1, keepdims=True
    )
    amplitude = radius / math.sqrt(2)
    covariance_start = patterns[targets, DIMENSION:]
    invalid = np.any(
        covariance_start + amplitude * covariance_directions <= 0.01,
        axis=1,
    )
    while np.any(invalid):
        replacement = rng.normal(size=(int(invalid.sum()), DIMENSION))
        replacement /= np.linalg.norm(replacement, axis=1, keepdims=True)
        covariance_directions[invalid] = replacement
        invalid = np.any(
            covariance_start + amplitude * covariance_directions <= 0.01,
            axis=1,
        )
    queries = patterns[targets].copy()
    queries[:, :DIMENSION] += amplitude * mean_directions
    queries[:, DIMENSION:] += amplitude * covariance_directions
    actual = np.linalg.norm(queries - patterns[targets], axis=1)
    if float(np.max(np.abs(actual - radius))) > 1e-10:
        raise AssertionError("query radius mismatch")
    return queries


def algorithm_1_update(queries, patterns, beta):
    query_norms = np.sum(queries**2, axis=1, keepdims=True)
    pattern_norms = np.sum(patterns**2, axis=1)
    logits = query_norms + pattern_norms - 2 * queries @ patterns.T
    np.maximum(logits, 0, out=logits)
    logits *= -beta
    logits -= np.max(logits, axis=1, keepdims=True)
    np.exp(logits, out=logits)
    normalizers = np.sum(logits, axis=1, keepdims=True)
    return (logits @ patterns) / normalizers


def summarize(errors, iteration):
    mean = float(np.mean(errors))
    standard_deviation = float(np.std(errors, ddof=1))
    half_width = 1.96 * standard_deviation / math.sqrt(len(errors))
    successes = int(np.sum(errors < THRESHOLD))
    proportion = successes / len(errors)
    proportion_half_width = 1.96 * math.sqrt(
        max(proportion * (1 - proportion), 0) / len(errors)
    )
    return {
        "iteration": iteration,
        "mean_w2_error": mean,
        "standard_deviation": standard_deviation,
        "mean_95_ci": [max(0.0, mean - half_width), mean + half_width],
        "convergence_rate": proportion,
        "convergence_95_ci": [
            max(0.0, proportion - proportion_half_width),
            min(1.0, proportion + proportion_half_width),
        ],
    }


def independent_checker():
    rng = np.random.default_rng(404)
    patterns = rng.normal(size=(32, 12))
    queries = rng.normal(size=(3, 12))
    beta = 0.7
    vectorized = algorithm_1_update(queries, patterns, beta)
    loop_outputs = []
    for query in queries:
        distances = np.array(
            [float(np.sum((query - pattern) ** 2)) for pattern in patterns]
        )
        logits = -beta * distances
        weights = np.exp(logits - np.max(logits))
        weights /= weights.sum()
        loop_outputs.append(
            np.sum(weights[:, None] * patterns, axis=0)
        )
    maximum_error = float(
        np.max(np.abs(vectorized - np.stack(loop_outputs)))
    )
    return {
        "name": "scalar-loop Algorithm 1 update",
        "maximum_absolute_error": maximum_error,
        "tolerance": 1e-11,
        "passed": maximum_error < 1e-11,
    }


def verify(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    configurations = []
    raw_final_errors = {}
    uniform_control_rates = []
    all_invariants = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        patterns, invariants = sample_algorithm_2(rng)
        all_invariants.append(invariants)
        targets = rng.choice(COUNT, size=QUERY_COUNT, replace=False)
        uniform_output = np.mean(patterns, axis=0)
        uniform_errors = np.linalg.norm(
            uniform_output - patterns[targets], axis=1
        )
        uniform_control_rates.append(
            float(np.mean(uniform_errors < THRESHOLD))
        )
        for beta in BETAS:
            for multiplier in RADIUS_MULTIPLIERS:
                radius = multiplier / math.sqrt(beta * COUNT)
                queries = perturb_queries(
                    rng, patterns, targets, radius
                )
                trajectory = [
                    summarize(
                        np.linalg.norm(
                            queries - patterns[targets], axis=1
                        ),
                        0,
                    )
                ]
                current = queries
                for iteration in range(1, ITERATIONS + 1):
                    current = algorithm_1_update(
                        current, patterns, beta
                    )
                    errors = np.linalg.norm(
                        current - patterns[targets], axis=1
                    )
                    trajectory.append(summarize(errors, iteration))
                label = f"seed_{seed}_beta_{beta}_radius_{multiplier}r"
                raw_final_errors[label] = errors.tolist()
                configurations.append(
                    {
                        "seed": seed,
                        "N": COUNT,
                        "d": DIMENSION,
                        "queries": QUERY_COUNT,
                        "beta": beta,
                        "radius_multiplier": multiplier,
                        "radius": radius,
                        "iterations": ITERATIONS,
                        "trajectory": trajectory,
                    }
                )
    checker = independent_checker()
    positive = [
        config["trajectory"][-1]
        for config in configurations
        if config["beta"] == 1.0
    ]
    negative = [
        config["trajectory"][-1]
        for config in configurations
        if config["beta"] == 0.1
    ]
    negative_control = {
        "name": "beta=0 uniform weights",
        "per_seed_convergence_rates": uniform_control_rates,
        "rejected": max(uniform_control_rates) <= 0.01,
    }
    checks = {
        "exact_scale": all(
            config["N"] == 10_000
            and config["d"] == 50
            and config["queries"] == 7_500
            for config in configurations
        ),
        "algorithm_2_invariants": all(
            all(invariants.values()) for invariants in all_invariants
        ),
        "beta_1_converges": min(
            result["convergence_95_ci"][0] for result in positive
        )
        >= 0.999,
        "beta_0_1_fails": max(
            result["convergence_95_ci"][1] for result in negative
        )
        <= 0.01,
        "independent_checker": checker["passed"],
        "negative_control_rejected": negative_control["rejected"],
    }
    result = {
        "claim_id": 4,
        "verdict": "VERIFIED" if all(checks.values()) else "BLOCKED",
        "parameters": {
            "N": COUNT,
            "d": DIMENSION,
            "queries": QUERY_COUNT,
            "lambda_min": LAMBDA_MIN,
            "lambda_max": LAMBDA_MAX,
            "betas": BETAS,
            "radius_multipliers": RADIUS_MULTIPLIERS,
            "iterations": ITERATIONS,
            "threshold": THRESHOLD,
            "seeds": SEEDS,
        },
        "algorithm_2_invariants": all_invariants,
        "configurations": configurations,
        "raw_final_errors": raw_final_errors,
        "independent_checker": checker,
        "negative_control": negative_control,
        "checks": checks,
    }
    (output_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    if result["verdict"] != "VERIFIED":
        raise SystemExit(json.dumps(result, indent=2))
    return result
