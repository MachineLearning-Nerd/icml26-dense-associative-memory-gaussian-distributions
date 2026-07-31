import hashlib
import io
import json
import math
import tarfile
import urllib.request

import numpy as np
import torch
from PIL import Image
from scipy.linalg import sqrtm


COUNT = 1_000
DIMENSION = 10
QUERY_COUNT = 750
BETAS = [1.0, 0.1]
RADIUS_MULTIPLIERS = [1, 100]
TEXT_THRESHOLD = 1e-3
PLOT_THRESHOLD = 1e-6
SEEDS = [20260730, 20260731, 20260732]
BATCH_SIZE = 8
SOURCE_URL = "https://export.arxiv.org/e-print/2509.23162v1"
SOURCE_SHA256 = "a88a9b572b0d3c28b62de7f9419885cd3367d25e8b453bf4ffeba36a68f1f6ee"
FIGURE_NAME = (
    "retrieval_dynamics_general,N_1000,d_10,"
    "beta_1,perturb100x.png"
)
FIGURE_SHA256 = "58cab4d6ad088d862eb892d5eee30389d77cf23d8434185e9f692b27f3bebd18"


def matrix_power(matrix, power):
    eigenvalues, eigenvectors = torch.linalg.eigh(
        (matrix + matrix.transpose(-1, -2)) / 2
    )
    eigenvalues = eigenvalues.clamp_min(1e-14)
    scaled = eigenvectors * eigenvalues.pow(power).unsqueeze(-2)
    return scaled @ eigenvectors.transpose(-1, -2)


def bures_covariance_squared(left, right, left_sqrt=None):
    if left_sqrt is None:
        left_sqrt = matrix_power(left, 0.5)
    middle = left_sqrt @ right @ left_sqrt
    eigenvalues = torch.linalg.eigvalsh(
        (middle + middle.transpose(-1, -2)) / 2
    ).clamp_min(0)
    distance = (
        torch.diagonal(left, dim1=-2, dim2=-1).sum(-1)
        + torch.diagonal(right, dim1=-2, dim2=-1).sum(-1)
        - 2 * eigenvalues.sqrt().sum(-1)
    )
    return distance.clamp_min(0)


def sample_patterns(rng):
    means = rng.normal(size=(COUNT, DIMENSION))
    means /= np.linalg.norm(means, axis=1, keepdims=True)
    means *= math.sqrt(DIMENSION)

    factors = rng.normal(size=(COUNT, DIMENSION, DIMENSION))
    covariances = factors @ factors.transpose(0, 2, 1)
    covariances += 0.01 * np.eye(DIMENSION)[None]
    covariances *= (
        DIMENSION
        / np.trace(covariances, axis1=1, axis2=2)
    )[:, None, None]

    audit_pairs = [
        (index, index + 1)
        for index in range(min(100, COUNT - 1))
    ]
    commutators = [
        float(
            np.linalg.norm(
                covariances[i] @ covariances[j]
                - covariances[j] @ covariances[i],
                ord="fro",
            )
        )
        for i, j in audit_pairs
    ]
    invariants = {
        "count": len(means) == COUNT,
        "dimension": means.shape[1] == DIMENSION,
        "maximum_mean_norm_squared_error": float(
            np.max(np.abs(np.sum(means**2, axis=1) - DIMENSION))
        ),
        "maximum_trace_error": float(
            np.max(
                np.abs(
                    np.trace(covariances, axis1=1, axis2=2)
                    - DIMENSION
                )
            )
        ),
        "minimum_covariance_eigenvalue": float(
            np.min(np.linalg.eigvalsh(covariances))
        ),
        "minimum_commutator_frobenius_norm": min(commutators),
        "median_commutator_frobenius_norm": float(
            np.median(commutators)
        ),
    }
    return (
        torch.from_numpy(means),
        torch.from_numpy(covariances),
        invariants,
    )


def covariance_perturbations(base, directions, target_distance):
    base_sqrt = matrix_power(base, 0.5)
    low = torch.zeros(len(base), dtype=torch.float64)
    high = torch.ones(len(base), dtype=torch.float64)
    target_squared = target_distance**2

    for _ in range(32):
        proposals = base + high[:, None, None] * directions
        distances = bures_covariance_squared(
            base, proposals, base_sqrt
        )
        unresolved = distances < target_squared
        if not bool(unresolved.any()):
            break
        high[unresolved] *= 2
    if bool((distances < target_squared).any()):
        raise AssertionError("failed to bracket covariance perturbation")

    for _ in range(64):
        middle = (low + high) / 2
        proposals = base + middle[:, None, None] * directions
        distances = bures_covariance_squared(
            base, proposals, base_sqrt
        )
        below = distances < target_squared
        low[below] = middle[below]
        high[~below] = middle[~below]

    scale = (low + high) / 2
    perturbed = base + scale[:, None, None] * directions
    actual_squared = bures_covariance_squared(
        base, perturbed, base_sqrt
    )
    return perturbed, actual_squared.sqrt()


def perturb_queries(
    rng,
    means,
    covariances,
    targets,
    radius,
    direction_law="wishart",
):
    mean_directions = rng.normal(size=(len(targets), DIMENSION))
    mean_directions /= np.linalg.norm(
        mean_directions, axis=1, keepdims=True
    )
    mean_offset = torch.from_numpy(
        mean_directions * (radius / math.sqrt(2))
    )

    if direction_law == "wishart":
        factors = rng.normal(
            size=(len(targets), DIMENSION, DIMENSION)
        )
        directions = factors @ factors.transpose(0, 2, 1)
    elif direction_law == "rank_one":
        factors = rng.normal(size=(len(targets), DIMENSION, 1))
        directions = factors @ factors.transpose(0, 2, 1)
    else:
        raise ValueError(f"unknown direction law: {direction_law}")
    directions /= np.trace(
        directions, axis1=1, axis2=2
    )[:, None, None]
    directions = torch.from_numpy(directions)

    target_covariances = covariances[targets]
    query_covariances, covariance_distances = covariance_perturbations(
        target_covariances,
        directions,
        radius / math.sqrt(2),
    )
    query_means = means[targets] + mean_offset
    full_distances = torch.sqrt(
        torch.sum(mean_offset**2, dim=1) + covariance_distances**2
    )
    return query_means, query_covariances, full_distances


def algorithm_1_update(
    query_means,
    query_covariances,
    pattern_means,
    pattern_covariances,
    beta,
):
    pattern_sqrt = matrix_power(pattern_covariances, 0.5)
    pattern_norms = torch.sum(pattern_means**2, dim=1)
    pattern_traces = torch.diagonal(
        pattern_covariances, dim1=-2, dim2=-1
    ).sum(-1)
    output_means = []
    output_covariances = []

    for start in range(0, len(query_means), BATCH_SIZE):
        stop = start + BATCH_SIZE
        means = query_means[start:stop]
        covariances = query_covariances[start:stop]
        mean_squared = (
            torch.sum(means**2, dim=1, keepdim=True)
            + pattern_norms[None]
            - 2 * means @ pattern_means.T
        ).clamp_min(0)

        middle = (
            pattern_sqrt[None]
            @ covariances[:, None]
            @ pattern_sqrt[None]
        )
        middle = (middle + middle.transpose(-1, -2)) / 2
        eigenvalues, eigenvectors = torch.linalg.eigh(middle)
        eigenvalues = eigenvalues.clamp_min(1e-14)
        covariance_squared = (
            pattern_traces[None]
            + torch.diagonal(
                covariances, dim1=-2, dim2=-1
            ).sum(-1)[:, None]
            - 2 * eigenvalues.sqrt().sum(-1)
        ).clamp_min(0)
        weights = torch.softmax(
            -beta * (mean_squared + covariance_squared),
            dim=1,
        )

        inverse_root = (
            eigenvectors * eigenvalues.rsqrt().unsqueeze(-2)
        ) @ eigenvectors.transpose(-1, -2)
        transport = (
            pattern_sqrt[None]
            @ inverse_root
            @ pattern_sqrt[None]
        )
        average_transport = torch.einsum(
            "bn,bnij->bij", weights, transport
        )
        updated_covariances = (
            average_transport
            @ covariances
            @ average_transport.transpose(-1, -2)
        )
        output_means.append(weights @ pattern_means)
        output_covariances.append(
            (
                updated_covariances
                + updated_covariances.transpose(-1, -2)
            )
            / 2
        )
    return torch.cat(output_means), torch.cat(output_covariances)


def paired_w2(means, covariances, target_means, target_covariances):
    covariance_squared = bures_covariance_squared(
        target_covariances,
        covariances,
        matrix_power(target_covariances, 0.5),
    )
    mean_squared = torch.sum((means - target_means) ** 2, dim=1)
    return torch.sqrt((mean_squared + covariance_squared).clamp_min(0))


def summarize(errors, nearest_target_rate):
    values = errors.numpy()
    mean = float(np.mean(values))
    standard_deviation = float(np.std(values, ddof=1))
    half_width = 1.96 * standard_deviation / math.sqrt(len(values))
    return {
        "mean_w2_error": mean,
        "standard_deviation": standard_deviation,
        "mean_95_ci": [max(0.0, mean - half_width), mean + half_width],
        "below_1e-3_rate": float(np.mean(values < TEXT_THRESHOLD)),
        "below_1e-6_rate": float(np.mean(values < PLOT_THRESHOLD)),
        "nearest_target_rate": nearest_target_rate,
    }


def nearest_mean_target_rate(means, pattern_means, targets):
    selected = []
    for start in range(0, len(means), 64):
        batch = means[start : start + 64]
        squared = (
            torch.sum(batch**2, dim=1, keepdim=True)
            + torch.sum(pattern_means**2, dim=1)[None]
            - 2 * batch @ pattern_means.T
        )
        selected.extend(torch.argmin(squared, dim=1).tolist())
    return float(np.mean(np.asarray(selected) == targets))


def scipy_update(query_mean, query_covariance, means, covariances, beta):
    distances = []
    transports = []
    for mean, covariance in zip(means, covariances):
        covariance_sqrt = np.real_if_close(sqrtm(covariance))
        middle = covariance_sqrt @ query_covariance @ covariance_sqrt
        middle_sqrt = np.real_if_close(sqrtm(middle))
        distance = (
            np.sum((mean - query_mean) ** 2)
            + np.trace(covariance + query_covariance - 2 * middle_sqrt)
        )
        distances.append(float(distance))
        transports.append(
            covariance_sqrt
            @ np.linalg.inv(middle_sqrt)
            @ covariance_sqrt
        )
    logits = -beta * np.asarray(distances)
    weights = np.exp(logits - np.max(logits))
    weights /= weights.sum()
    updated_mean = weights @ means
    average_transport = np.einsum(
        "n,nij->ij", weights, np.asarray(transports)
    )
    updated_covariance = (
        average_transport
        @ query_covariance
        @ average_transport.T
    )
    return updated_mean, updated_covariance


def independent_checker():
    rng = np.random.default_rng(606)
    count = 7
    dimension = 3
    means = rng.normal(size=(count, dimension))
    factors = rng.normal(size=(count, dimension, dimension))
    covariances = factors @ factors.transpose(0, 2, 1)
    covariances += 0.2 * np.eye(dimension)[None]
    query_mean = rng.normal(size=dimension)
    query_factor = rng.normal(size=(dimension, dimension))
    query_covariance = query_factor @ query_factor.T
    query_covariance += 0.2 * np.eye(dimension)
    beta = 0.7

    torch_mean, torch_covariance = algorithm_1_update(
        torch.from_numpy(query_mean[None]),
        torch.from_numpy(query_covariance[None]),
        torch.from_numpy(means),
        torch.from_numpy(covariances),
        beta,
    )
    scipy_mean, scipy_covariance = scipy_update(
        query_mean,
        query_covariance,
        means,
        covariances,
        beta,
    )
    mean_error = float(
        np.max(np.abs(torch_mean[0].numpy() - scipy_mean))
    )
    covariance_error = float(
        np.max(
            np.abs(torch_covariance[0].numpy() - scipy_covariance)
        )
    )
    return {
        "name": "SciPy sqrtm scalar Algorithm 1",
        "mean_maximum_absolute_error": mean_error,
        "covariance_maximum_absolute_error": covariance_error,
        "tolerance": 1e-9,
        "passed": max(mean_error, covariance_error) < 1e-9,
    }


def source_figure_audit():
    request = urllib.request.Request(
        SOURCE_URL,
        headers={
            "User-Agent": (
                "OpenResearch-Reproduction/1.0 "
                "(https://github.com/MachineLearning-Nerd/"
                "icml26-repro-uPHdNikfdo-dense-associative-"
                "memory-for-gaussian-distributions)"
            )
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        source = response.read()
    source_hash = hashlib.sha256(source).hexdigest()
    if source_hash != SOURCE_SHA256:
        raise AssertionError(
            f"unexpected arXiv v1 source hash: {source_hash}"
        )

    with tarfile.open(fileobj=io.BytesIO(source), mode="r:*") as archive:
        members = [
            member
            for member in archive.getmembers()
            if member.name.endswith(FIGURE_NAME)
        ]
        if len(members) != 1:
            raise AssertionError("Figure 8 panel (b) is missing")
        figure = archive.extractfile(members[0]).read()
    figure_hash = hashlib.sha256(figure).hexdigest()
    if figure_hash != FIGURE_SHA256:
        raise AssertionError(
            f"unexpected Figure 8 panel hash: {figure_hash}"
        )

    pixels = np.asarray(Image.open(io.BytesIO(figure)).convert("RGBA"))
    if pixels.shape != (1764, 2956, 4):
        raise AssertionError(f"unexpected figure shape: {pixels.shape}")

    calibration_rows = []
    column = pixels[:, 250, :3]
    grid_rows = np.flatnonzero(np.all(column == 231, axis=1))
    for row in grid_rows:
        if 100 <= row <= 1400 and (
            not calibration_rows or row > calibration_rows[-1][-1] + 1
        ):
            calibration_rows.append([int(row)])
        elif calibration_rows and row == calibration_rows[-1][-1] + 1:
            calibration_rows[-1].append(int(row))
    grid_centers = np.asarray(
        [np.mean(group) for group in calibration_rows]
    )
    grid_values = np.arange(3.0, 0.49, -0.5)
    if len(grid_centers) != len(grid_values):
        raise AssertionError(
            f"could not calibrate y-axis: {grid_centers.tolist()}"
        )
    slope, intercept = np.polyfit(grid_values, grid_centers, 1)
    residual = np.max(
        np.abs(grid_centers - (slope * grid_values + intercept))
    )

    blue = (
        (pixels[:, :, 0] < 40)
        & (pixels[:, :, 1] < 40)
        & (pixels[:, :, 2] > 220)
        & (pixels[:, :, 3] > 200)
    )
    x_positions = np.rint(
        np.linspace(318, 2805, num=6)
    ).astype(int)
    curve_rows = []
    for x_position in x_positions:
        y, x = np.where(blue)
        selected = y[np.abs(x - x_position) <= 4]
        if len(selected) < 20:
            raise AssertionError(
                f"missing blue curve at x={x_position}"
            )
        curve_rows.append(float(np.median(selected)))
    digitized = [
        float((row - intercept) / slope) for row in curve_rows
    ]
    return {
        "source_url": SOURCE_URL,
        "source_sha256": source_hash,
        "figure": FIGURE_NAME,
        "figure_sha256": figure_hash,
        "figure_shape": list(pixels.shape),
        "calibration_grid_pixel_rows": grid_centers.tolist(),
        "calibration_grid_values": grid_values.tolist(),
        "calibration_maximum_pixel_residual": float(residual),
        "curve_pixel_rows": curve_rows,
        "digitized_mean_w2_by_iteration": digitized,
        "checks": {
            "axis_calibration": bool(residual < 1.0),
            "one_step_above_0_1": bool(digitized[1] > 0.1),
            "five_steps_above_0_05": bool(digitized[5] > 0.05),
        },
    }


def verify(output_dir):
    torch.set_default_dtype(torch.float64)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_audit = source_figure_audit()
    configurations = []
    raw_errors = {}
    invariants = []
    query_radius_errors = []
    uniform_lower_bounds = []
    multistep_trajectories = []
    alternative_direction_results = []

    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        means, covariances, pattern_invariants = sample_patterns(rng)
        invariants.append(pattern_invariants)
        targets = rng.choice(COUNT, size=QUERY_COUNT, replace=False)
        target_means = means[targets]
        target_covariances = covariances[targets]
        uniform_mean = torch.mean(means, dim=0)
        uniform_lower_bounds.append(
            torch.linalg.vector_norm(
                target_means - uniform_mean, dim=1
            ).numpy().tolist()
        )

        for beta in BETAS:
            for multiplier in RADIUS_MULTIPLIERS:
                radius = multiplier / math.sqrt(beta * COUNT)
                query_means, query_covariances, actual_radii = (
                    perturb_queries(
                        rng,
                        means,
                        covariances,
                        targets,
                        radius,
                    )
                )
                query_radius_errors.append(
                    float(torch.max(torch.abs(actual_radii - radius)))
                )
                updated_means, updated_covariances = algorithm_1_update(
                    query_means,
                    query_covariances,
                    means,
                    covariances,
                    beta,
                )
                errors = paired_w2(
                    updated_means,
                    updated_covariances,
                    target_means,
                    target_covariances,
                )
                nearest_rate = nearest_mean_target_rate(
                    updated_means, means, targets
                )
                label = (
                    f"seed_{seed}_beta_{beta}_radius_{multiplier}r"
                )
                raw_errors[label] = errors.numpy().tolist()
                configurations.append(
                    {
                        "seed": seed,
                        "N": COUNT,
                        "d": DIMENSION,
                        "queries": QUERY_COUNT,
                        "beta": beta,
                        "radius_multiplier": multiplier,
                        "radius": radius,
                        "initial_mean_w2_error": float(
                            torch.mean(actual_radii)
                        ),
                        "one_step": summarize(errors, nearest_rate),
                    }
                )
                if beta == 1.0 and multiplier == 100:
                    trajectory = [
                        {
                            "iteration": 0,
                            "mean_w2_error": float(
                                torch.mean(actual_radii)
                            ),
                        },
                        {
                            "iteration": 1,
                            **summarize(errors, nearest_rate),
                        },
                    ]
                    current_means = updated_means
                    current_covariances = updated_covariances
                    for iteration in range(2, 6):
                        current_means, current_covariances = (
                            algorithm_1_update(
                                current_means,
                                current_covariances,
                                means,
                                covariances,
                                beta,
                            )
                        )
                        current_errors = paired_w2(
                            current_means,
                            current_covariances,
                            target_means,
                            target_covariances,
                        )
                        current_nearest_rate = (
                            nearest_mean_target_rate(
                                current_means, means, targets
                            )
                        )
                        trajectory.append(
                            {
                                "iteration": iteration,
                                **summarize(
                                    current_errors,
                                    current_nearest_rate,
                                ),
                            }
                        )
                    multistep_trajectories.append(
                        {
                            "seed": seed,
                            "beta": beta,
                            "radius_multiplier": multiplier,
                            "trajectory": trajectory,
                        }
                    )

        rank_one_rng = np.random.default_rng(seed + 6_000)
        rank_one_means, rank_one_covariances, rank_one_radii = (
            perturb_queries(
                rank_one_rng,
                means,
                covariances,
                targets,
                100 / math.sqrt(COUNT),
                direction_law="rank_one",
            )
        )
        query_radius_errors.append(
            float(
                torch.max(
                    torch.abs(
                        rank_one_radii - 100 / math.sqrt(COUNT)
                    )
                )
            )
        )
        rank_one_updated_means, rank_one_updated_covariances = (
            algorithm_1_update(
                rank_one_means,
                rank_one_covariances,
                means,
                covariances,
                1.0,
            )
        )
        rank_one_errors = paired_w2(
            rank_one_updated_means,
            rank_one_updated_covariances,
            target_means,
            target_covariances,
        )
        alternative_direction_results.append(
            {
                "seed": seed,
                "direction_law": "rank-one PSD",
                "beta": 1.0,
                "radius_multiplier": 100,
                "initial_mean_w2_error": float(
                    torch.mean(rank_one_radii)
                ),
                "one_step": summarize(
                    rank_one_errors,
                    nearest_mean_target_rate(
                        rank_one_updated_means,
                        means,
                        targets,
                    ),
                ),
            }
        )

    checker = independent_checker()
    positive = [
        row["one_step"]
        for row in configurations
        if row["beta"] == 1.0
    ]
    negative = [
        row["one_step"]
        for row in configurations
        if row["beta"] == 0.1
    ]
    flat_uniform = np.concatenate(uniform_lower_bounds)
    negative_control = {
        "name": "beta=0 uniform-weight mean lower bound",
        "minimum_w2_lower_bound": float(np.min(flat_uniform)),
        "below_1e-3_rate_upper_bound": float(
            np.mean(flat_uniform < TEXT_THRESHOLD)
        ),
        "rejected": float(np.min(flat_uniform)) > TEXT_THRESHOLD,
    }
    large_radius_positive = [
        row["one_step"]
        for row in configurations
        if row["beta"] == 1.0 and row["radius_multiplier"] == 100
    ]
    final_large_radius = [
        row["trajectory"][-1]
        for row in multistep_trajectories
    ]
    alternative_positive = [
        row["one_step"] for row in alternative_direction_results
    ]
    checks = {
        "exact_scale": all(
            row["N"] == COUNT
            and row["d"] == DIMENSION
            and row["queries"] == QUERY_COUNT
            for row in configurations
        ),
        "sphere_invariants": all(
            row["maximum_mean_norm_squared_error"] < 1e-10
            and row["maximum_trace_error"] < 1e-10
            and row["minimum_covariance_eigenvalue"] > 0
            for row in invariants
        ),
        "non_commuting": min(
            row["minimum_commutator_frobenius_norm"]
            for row in invariants
        )
        > 1e-6,
        "query_radii": max(query_radius_errors) < 1e-9,
        "beta_1_one_step_claim_rejected": min(
            row["mean_95_ci"][0] for row in positive
        )
        > TEXT_THRESHOLD,
        "large_radius_one_step_claim_rejected": min(
            row["mean_95_ci"][0] for row in large_radius_positive
        )
        > 0.1,
        "large_radius_five_step_claim_rejected": min(
            row["mean_95_ci"][0] for row in final_large_radius
        )
        > 0.05,
        "alternative_psd_direction_rejects_one_step": min(
            row["mean_95_ci"][0] for row in alternative_positive
        )
        > 0.1,
        "source_figure_rejects_one_step": all(
            figure_audit["checks"].values()
        ),
        "beta_0_1_non_convergence": max(
            row["below_1e-3_rate"] for row in negative
        )
        <= 0.01,
        "independent_checker": checker["passed"],
        "negative_control_rejected": negative_control["rejected"],
    }
    result = {
        "claim_id": 6,
        "verdict": "FALSIFIED" if all(checks.values()) else "BLOCKED",
        "parameters": {
            "N": COUNT,
            "d": DIMENSION,
            "queries": QUERY_COUNT,
            "sphere_radius": math.sqrt(2 * DIMENSION),
            "betas": BETAS,
            "radius_multipliers": RADIUS_MULTIPLIERS,
            "updates": 5,
            "paper_text_threshold": TEXT_THRESHOLD,
            "paper_plot_threshold": PLOT_THRESHOLD,
            "seeds": SEEDS,
            "batch_size": BATCH_SIZE,
        },
        "pattern_invariants": invariants,
        "maximum_query_radius_error": max(query_radius_errors),
        "configurations": configurations,
        "multistep_large_radius_trajectories": multistep_trajectories,
        "alternative_psd_direction": alternative_direction_results,
        "raw_one_step_errors": raw_errors,
        "source_figure_audit": figure_audit,
        "independent_checker": checker,
        "negative_control": negative_control,
        "checks": checks,
    }
    (output_dir / "result.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    if result["verdict"] != "FALSIFIED":
        raise SystemExit(json.dumps(result, indent=2))
    return result
