import hashlib
import io
import json
import math
import re
import urllib.request
import zipfile
from collections import Counter

import numpy as np
import torch


TEXT8_URL = "https://mattmahoney.net/dc/text8.zip"
TEXT8_SHA256 = "a6640522afe85d1963ad56c05b0ede0a0c000dddc9671758a6cc09b7a38e5232"
TEXT8_MD5 = "3bea1919949baf155f99411df5fada7e"
TEXT8_TOKENS = 17_005_207
TEXT8_TYPES = 253_854
VOCABULARY_SHA256 = "d4e1f58f89a7ad0b89a479b79fdd9559f9ea2d9575ad79ce7556da736675f923"

AUTHOR_NOTEBOOK_URL = (
    "https://raw.githubusercontent.com/chandantankala/DDAM/"
    "d5346b69a778ad316c031a8e0f2f13b5f86e6e15/DDAM.ipynb"
)
AUTHOR_NOTEBOOK_SHA256 = "4720167b74eb84cb35ec853863ab1f23eabcf837ccfe1b5e41d4496872e2ce3e"
AUTHOR_COMMIT = "d5346b69a778ad316c031a8e0f2f13b5f86e6e15"
WORD2GAUSS_COMMIT = "cdf5e7f5d0c8c7582fdf92e4599bd8efda5b98bc"

COUNT = 10_000
DIMENSION = 50
TRAINING_TOKENS = 100_000
EPOCHS = 5
WINDOW = 5
NEGATIVE_SAMPLES = 2
TRAIN_BATCH_SIZE = 2_048
QUERY_COUNT = 100
QUERY_SEEDS = [42, 43, 44]
BETAS = np.logspace(-1, 2, 20)
MAX_ITERATIONS = 10
CONVERGENCE_THRESHOLD = 1e-6


def download(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "OpenResearch-Reproduction/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def audit_author_notebook():
    raw = download(AUTHOR_NOTEBOOK_URL)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != AUTHOR_NOTEBOOK_SHA256:
        raise AssertionError("author notebook hash mismatch")
    notebook = json.loads(raw)
    training_source = ""
    training_output = ""
    phase_source = ""
    phase_output = ""
    for cell in notebook["cells"]:
        source = "".join(cell.get("source", []))
        outputs = []
        for output in cell.get("outputs", []):
            text = output.get("text", [])
            if isinstance(text, str):
                outputs.append(text)
            else:
                outputs.append("".join(text))
        rendered = "\n".join(outputs)
        if "def train_word2gauss" in source and "'corpus_sample': 100000" in source:
            training_source = source
            training_output = rendered
        if (
            "def compute_retrieval_fraction_vs_beta" in source
            and "sample_size=100" in source
            and "Beta = " in rendered
        ):
            phase_source = source
            phase_output = rendered
    if not all([training_source, training_output, phase_source, phase_output]):
        raise AssertionError("author notebook cells not found")

    epoch_matches = re.findall(
        r"Epoch (\d)/5: [0-9.]+s, mean_norm=([0-9.]+), "
        r"mean_sigma=([0-9.]+)",
        training_output,
    )
    curve_matches = re.findall(
        r"Beta = ([0-9.]+): ([0-9.]+)% retrieval rate",
        phase_output,
    )
    training = [
        {
            "epoch": int(epoch),
            "mean_norm": float(mean_norm),
            "mean_sigma": float(mean_sigma),
        }
        for epoch, mean_norm, mean_sigma in epoch_matches
    ]
    curve = [
        {
            "beta": float(beta),
            "retrieval_rate": float(percent) / 100,
        }
        for beta, percent in curve_matches
    ]
    source_checks = {
        "N_10000": "'max_vocab': 10000" in training_source,
        "d_50": "'embed_dim': 50" in training_source,
        "five_epochs": "'num_epochs': 5" in training_source,
        "spherical": "covariance_type='spherical'" in training_source,
        "KL_energy": "energy_type='KL'" in training_source,
        "window_5": "'window_size': 5" in training_source,
        "two_negative_samples": "nsamples=2" in training_source,
        "first_100000_tokens": "'corpus_sample': 100000" in training_source,
        "phase_100_queries": "sample_size=100" in phase_source,
        "phase_seed_42": "seed=42" in phase_source,
        "twenty_log_betas": "np.logspace(-1, 2, 20)" in phase_source,
        "ten_updates": "max_iterations=10" in phase_source,
    }
    return {
        "url": AUTHOR_NOTEBOOK_URL,
        "commit": AUTHOR_COMMIT,
        "sha256": digest,
        "word2gauss_commit": WORD2GAUSS_COMMIT,
        "source_checks": source_checks,
        "training_output": training,
        "phase_curve": curve,
    }


def load_text8():
    archive_bytes = download(TEXT8_URL)
    archive_hash = hashlib.sha256(archive_bytes).hexdigest()
    if archive_hash != TEXT8_SHA256:
        raise AssertionError("Text8 archive hash mismatch")
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        corpus = archive.read("text8")
    corpus_md5 = hashlib.md5(corpus).hexdigest()
    if corpus_md5 != TEXT8_MD5:
        raise AssertionError("Text8 corpus hash mismatch")
    tokens = corpus.split()
    counts = Counter(tokens)
    vocabulary_rows = counts.most_common(COUNT)
    vocabulary_bytes = b"\n".join(
        word + b"\t" + str(count).encode()
        for word, count in vocabulary_rows
    )
    vocabulary_hash = hashlib.sha256(vocabulary_bytes).hexdigest()
    words = [word for word, _ in vocabulary_rows]
    word_to_id = {word: index for index, word in enumerate(words)}
    probabilities = np.array(
        [count for _, count in vocabulary_rows],
        dtype=np.float64,
    )
    probabilities **= 0.75
    probabilities /= probabilities.sum()
    audit = {
        "archive_url": TEXT8_URL,
        "archive_sha256": archive_hash,
        "uncompressed_md5": corpus_md5,
        "uncompressed_bytes": len(corpus),
        "token_count": len(tokens),
        "type_count": len(counts),
        "vocabulary_size": len(words),
        "vocabulary_sha256": vocabulary_hash,
        "vocabulary_cutoff_count": vocabulary_rows[-1][1],
        "first_words": [word.decode() for word in words[:5]],
    }
    return tokens[:TRAINING_TOKENS], word_to_id, probabilities, audit


def positive_pairs(training_tokens, word_to_id):
    out_of_vocabulary = -1
    ids = np.array(
        [word_to_id.get(word, out_of_vocabulary) for word in training_tokens],
        dtype=np.int64,
    )
    left = []
    right = []
    for document_start in range(0, len(ids), 1_000):
        document = ids[document_start : document_start + 1_000]
        for i in range(len(document)):
            if document[i] == out_of_vocabulary:
                continue
            for j in range(i + 1, min(i + WINDOW + 1, len(document))):
                if document[j] != out_of_vocabulary:
                    left.append(document[i])
                    right.append(document[j])
    return np.asarray(left, dtype=np.int64), np.asarray(right, dtype=np.int64)


def initialize_embeddings():
    np.random.seed(5)
    means = 0.1 * np.random.randn(2 * COUNT, DIMENSION).astype(np.float32)
    variances = np.random.randn(2 * COUNT, 1).astype(np.float32)
    variances += 0.5
    np.clip(variances, 0.7, 1.5, out=variances)
    return (
        torch.from_numpy(means),
        torch.from_numpy(variances),
        torch.zeros_like(torch.from_numpy(means)),
        torch.zeros_like(torch.from_numpy(variances)),
    )


def energy(means, variances, i_rows, j_rows):
    mean_i = means[i_rows]
    mean_j = means[j_rows]
    variance_i = variances[i_rows]
    variance_j = variances[j_rows]
    ratio = variance_j / variance_i
    squared = torch.sum((mean_i - mean_j) ** 2, dim=1, keepdim=True)
    return -0.5 * (
        DIMENSION * ratio
        + squared / variance_i
        - DIMENSION
        - DIMENSION * torch.log(ratio)
    )


def energy_gradient(
    means,
    variances,
    i_rows,
    j_rows,
    raw_j,
):
    mean_i = means[i_rows]
    mean_j = means[j_rows]
    variance_i = variances[i_rows]
    variance_j = variances[j_rows]
    delta = (mean_i - mean_j) / variance_i
    gradient_mean_i = -delta
    gradient_mean_j = delta
    # This raw-j lookup intentionally preserves the historical Cython
    # implementation used by the author notebook.
    raw_variance_j = variances[raw_j]
    gradient_variance_i = 0.5 * (
        DIMENSION * raw_variance_j / variance_i**2
        + torch.sum(delta**2, dim=1, keepdim=True)
        - DIMENSION / variance_i
    )
    gradient_variance_j = (
        0.5
        * DIMENSION
        * (1 / variance_j - 1 / variance_i)
    )
    return (
        gradient_mean_i,
        gradient_variance_i,
        gradient_mean_j,
        gradient_variance_j,
    )


def aggregate_update(
    values,
    accumulated,
    row_groups,
    gradient_groups,
):
    rows = torch.cat(row_groups)
    gradients = torch.cat(gradient_groups)
    gradients.clamp_(-10, 10)
    unique_rows, inverse = torch.unique(rows, return_inverse=True)
    combined = torch.zeros(
        (len(unique_rows), gradients.shape[1]),
        dtype=gradients.dtype,
    )
    combined_squares = torch.zeros_like(combined)
    combined.index_add_(0, inverse, gradients)
    combined_squares.index_add_(0, inverse, gradients**2)
    accumulated[unique_rows] += combined_squares
    values[unique_rows] -= (
        0.1
        * combined
        / (torch.sqrt(accumulated[unique_rows]) + 1)
    )
    return unique_rows


def train_embeddings(training_tokens, word_to_id, probabilities):
    means, variances, accumulated_means, accumulated_variances = (
        initialize_embeddings()
    )
    left, right = positive_pairs(training_tokens, word_to_id)
    expanded_count = 4 * len(left)
    centers = np.tile(np.array([0, 1, 0, 1]), len(left))
    positive_i = np.repeat(left, 4)
    positive_j = np.repeat(right, 4)
    epoch_summaries = []
    for epoch in range(1, EPOCHS + 1):
        allocated_random_count = (
            2 * len(training_tokens) * WINDOW * NEGATIVE_SAMPLES
        )
        random_ids = np.random.choice(
            COUNT,
            size=allocated_random_count,
            p=probabilities,
        )[:expanded_count]
        negative_i = np.where(centers == 0, positive_i, random_ids)
        negative_j = np.where(centers == 0, random_ids, positive_j)

        for start in range(0, expanded_count, TRAIN_BATCH_SIZE):
            stop = min(start + TRAIN_BATCH_SIZE, expanded_count)
            center = torch.from_numpy(centers[start:stop])
            pos_i = torch.from_numpy(positive_i[start:stop])
            pos_j = torch.from_numpy(positive_j[start:stop])
            neg_i = torch.from_numpy(negative_i[start:stop])
            neg_j = torch.from_numpy(negative_j[start:stop])
            pos_i_rows = pos_i + center * COUNT
            pos_j_rows = pos_j + (1 - center) * COUNT
            neg_i_rows = neg_i + center * COUNT
            neg_j_rows = neg_j + (1 - center) * COUNT

            positive_energy = energy(
                means, variances, pos_i_rows, pos_j_rows
            )
            negative_energy = energy(
                means, variances, neg_i_rows, neg_j_rows
            )
            active = (
                0.1 - positive_energy + negative_energy > 1e-14
            ).squeeze(1)
            if not bool(active.any()):
                continue
            positive_gradients = energy_gradient(
                means,
                variances,
                pos_i_rows,
                pos_j_rows,
                pos_j,
            )
            negative_gradients = energy_gradient(
                means,
                variances,
                neg_i_rows,
                neg_j_rows,
                neg_j,
            )
            active_pos_i = pos_i_rows[active]
            active_pos_j = pos_j_rows[active]
            active_neg_i = neg_i_rows[active]
            active_neg_j = neg_j_rows[active]
            mean_rows = [
                active_pos_i,
                active_pos_j,
                active_neg_i,
                active_neg_j,
            ]
            mean_gradients = [
                -positive_gradients[0][active],
                -positive_gradients[2][active],
                negative_gradients[0][active],
                negative_gradients[2][active],
            ]
            touched_means = aggregate_update(
                means,
                accumulated_means,
                mean_rows,
                mean_gradients,
            )
            norms = torch.linalg.vector_norm(means[touched_means], dim=1)
            outside = norms > 2
            outside_rows = touched_means[outside]
            means[outside_rows] = means[outside_rows] * (
                2 / norms[outside, None]
            )

            variance_rows = mean_rows
            variance_gradients = [
                -positive_gradients[1][active],
                -positive_gradients[3][active],
                negative_gradients[1][active],
                negative_gradients[3][active],
            ]
            touched_variances = aggregate_update(
                variances,
                accumulated_variances,
                variance_rows,
                variance_gradients,
            )
            variances[touched_variances] = variances[
                touched_variances
            ].clamp(0.7, 1.5)

        epoch_summaries.append(
            {
                "epoch": epoch,
                "mean_norm": float(
                    torch.linalg.vector_norm(means, dim=1).mean()
                ),
                "mean_sigma": float(variances.mean()),
            }
        )
    training_audit = {
        "positive_context_pairs_per_epoch": len(left),
        "ranking_pairs_per_epoch": expanded_count,
        "batch_size": TRAIN_BATCH_SIZE,
        "epochs": EPOCHS,
        "optimizer": (
            "batched reconstruction of historical per-coordinate "
            "AdaGrad, including the Cython raw-j variance lookup"
        ),
        "epoch_summaries": epoch_summaries,
        "minimum_variance": float(variances.min()),
        "maximum_variance": float(variances.max()),
        "maximum_mean_norm": float(
            torch.linalg.vector_norm(means, dim=1).max()
        ),
    }
    return means[:COUNT].double(), variances[:COUNT, 0].double(), training_audit


def squared_distances(queries, patterns):
    distances = (
        torch.sum(queries**2, dim=1, keepdim=True)
        + torch.sum(patterns**2, dim=1)[None]
        - 2 * queries @ patterns.T
    )
    return distances.clamp_min_(0)


def phi(queries, patterns, beta):
    distances = squared_distances(queries, patterns)
    relative = distances - distances.min(dim=1, keepdim=True).values
    if beta <= 50:
        weights = torch.softmax(-beta * relative, dim=1)
        return weights @ patterns
    positive = torch.where(
        relative > 0,
        relative,
        torch.full_like(relative, torch.inf),
    )
    hard = beta * positive.min(dim=1).values > 100
    output = torch.empty_like(queries)
    if bool(hard.any()):
        nearest = distances[hard].argmin(dim=1)
        output[hard] = patterns[nearest]
    if bool((~hard).any()):
        weights = torch.softmax(-beta * relative[~hard], dim=1)
        output[~hard] = weights @ patterns
    return output


def retrieve(patterns, targets, beta, sign=1):
    radius = 1 / math.sqrt(beta * COUNT)
    originals = patterns[targets]
    radii = torch.linalg.vector_norm(originals, dim=1)
    current = originals * (1 + radius / radii)[:, None]
    previous = None
    active = torch.ones(len(targets), dtype=torch.bool)
    update_counts = torch.zeros(len(targets), dtype=torch.int64)
    for _ in range(MAX_ITERATIONS):
        if previous is not None:
            state_change = torch.linalg.vector_norm(
                current[:, :DIMENSION] - previous[:, :DIMENSION],
                dim=1,
            )
            active &= state_change >= CONVERGENCE_THRESHOLD
            if not bool(active.any()):
                break
        previous = current.clone()
        if sign == 1:
            current[active] = phi(current[active], patterns, beta)
        else:
            distances = squared_distances(current[active], patterns)
            current[active] = (
                torch.softmax(beta * distances, dim=1) @ patterns
            )
        update_counts[active] += 1
    nearest = squared_distances(current, patterns).argmin(dim=1)
    return nearest, update_counts


def phase_curve(patterns, seed):
    random = np.random.RandomState(seed)
    targets = random.choice(
        np.arange(100, COUNT),
        size=QUERY_COUNT,
        replace=False,
    )
    target_tensor = torch.from_numpy(targets)
    curve = []
    query_rows = []
    for beta in BETAS:
        nearest, updates = retrieve(patterns, target_tensor, float(beta))
        successes = nearest == target_tensor
        curve.append(
            {
                "beta": float(beta),
                "retrieval_rate": float(successes.double().mean()),
                "successes": int(successes.sum()),
                "queries": QUERY_COUNT,
                "mean_updates": float(updates.double().mean()),
            }
        )
        query_rows.extend(
            {
                "seed": seed,
                "beta": float(beta),
                "target": int(target),
                "nearest": int(found),
                "success": bool(success),
                "updates": int(update_count),
            }
            for target, found, success, update_count in zip(
                targets,
                nearest.tolist(),
                successes.tolist(),
                updates.tolist(),
            )
        )
    return curve, query_rows


def independent_checker(patterns):
    subset = patterns[:32]
    queries = patterns[100:103] * 1.01
    beta = 3.7
    vectorized = phi(queries, subset, beta)
    scalar = []
    for query in queries:
        distances = torch.tensor(
            [
                float(torch.sum((query - pattern) ** 2))
                for pattern in subset
            ],
            dtype=torch.float64,
        )
        weights = torch.exp(-beta * (distances - distances.min()))
        weights /= weights.sum()
        scalar.append(
            torch.sum(weights[:, None] * subset, dim=0)
        )
    maximum_error = float(
        torch.max(torch.abs(vectorized - torch.stack(scalar)))
    )
    return {
        "name": "scalar-loop spherical-Wasserstein Phi",
        "maximum_absolute_error": maximum_error,
        "tolerance": 1e-11,
        "passed": maximum_error < 1e-11,
    }


def curve_checks(curve):
    low = [
        row["retrieval_rate"]
        for row in curve
        if row["beta"] < 10
    ]
    above_30 = [
        row["retrieval_rate"]
        for row in curve
        if row["beta"] > 30
    ]
    rates = np.array([row["retrieval_rate"] for row in curve])
    betas = np.array([row["beta"] for row in curve])
    transition_indices = np.flatnonzero(rates >= 0.5)
    transition_beta = (
        float(betas[transition_indices[0]])
        if len(transition_indices)
        else None
    )
    return {
        "below_10_near_zero": max(low) <= 0.05,
        "above_30_near_perfect": min(above_30) >= 0.95,
        "sharp_adjacent_jump": float(np.max(np.diff(rates))) >= 0.5,
        "transition_beta": transition_beta,
        "transition_near_15": (
            transition_beta is not None
            and 11 <= transition_beta <= 24
        ),
    }


def verify(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    author = audit_author_notebook()
    training_tokens, word_to_id, probabilities, text8 = load_text8()
    means, variances, training = train_embeddings(
        training_tokens,
        word_to_id,
        probabilities,
    )
    patterns = torch.cat(
        [
            means,
            math.sqrt(DIMENSION) * torch.sqrt(variances)[:, None],
        ],
        dim=1,
    )
    curves = []
    raw_queries = []
    for seed in QUERY_SEEDS:
        curve, queries = phase_curve(patterns, seed)
        curves.append({"seed": seed, "curve": curve, "checks": curve_checks(curve)})
        raw_queries.extend(queries)

    checker = independent_checker(patterns)
    control_targets = torch.from_numpy(
        np.random.RandomState(42).choice(
            np.arange(100, COUNT),
            size=QUERY_COUNT,
            replace=False,
        )
    )
    control_queries = patterns[control_targets] * (
        1 + 1 / math.sqrt(15 * COUNT)
        / torch.linalg.vector_norm(patterns[control_targets], dim=1)
    )[:, None]
    uniform_output = phi(control_queries, patterns, 0)
    uniform_nearest = squared_distances(
        uniform_output, patterns
    ).argmin(dim=1)
    negative_control = {
        "name": "beta=0 uniform-weight retrieval",
        "retrieval_rate": float(
            (uniform_nearest == control_targets).double().mean()
        ),
        "rejected": bool(
            float((uniform_nearest == control_targets).double().mean())
            <= 0.01
        ),
        "query_radius": 1 / math.sqrt(15 * COUNT),
        "query_count": QUERY_COUNT,
    }

    author_rates = [
        row["retrieval_rate"] for row in author["phase_curve"]
    ]
    expected_author_rates = (
        [0.0] * 13
        + [0.31, 0.98]
        + [1.0] * 5
    )
    checks = {
        "author_source_contract": all(
            author["source_checks"].values()
        ),
        "author_executed_curve": (
            len(author_rates) == 20
            and np.allclose(author_rates, expected_author_rates)
        ),
        "text8_exact": (
            text8["token_count"] == TEXT8_TOKENS
            and text8["type_count"] == TEXT8_TYPES
            and text8["vocabulary_sha256"] == VOCABULARY_SHA256
        ),
        "training_exact_scale": (
            len(word_to_id) == COUNT
            and means.shape == (COUNT, DIMENSION)
            and len(training_tokens) == TRAINING_TOKENS
            and len(training["epoch_summaries"]) == EPOCHS
        ),
        "embedding_constraints": (
            training["minimum_variance"] >= 0.7 - 1e-6
            and training["maximum_variance"] <= 1.5 + 1e-6
            and training["maximum_mean_norm"] <= 2 + 1e-6
        ),
        "author_seed_phase": all(
            curves[0]["checks"][name]
            for name in [
                "below_10_near_zero",
                "above_30_near_perfect",
                "sharp_adjacent_jump",
                "transition_near_15",
            ]
        ),
        "validation_seed_phase": all(
            all(
                row["checks"][name]
                for name in [
                    "below_10_near_zero",
                    "above_30_near_perfect",
                    "sharp_adjacent_jump",
                    "transition_near_15",
                ]
            )
            for row in curves[1:]
        ),
        "independent_checker": checker["passed"],
        "negative_control_rejected": negative_control["rejected"],
    }
    result = {
        "claim_id": 5,
        "verdict": "VERIFIED" if all(checks.values()) else "BLOCKED",
        "parameters": {
            "N": COUNT,
            "d": DIMENSION,
            "text8_total_tokens": TEXT8_TOKENS,
            "author_training_token_cap": TRAINING_TOKENS,
            "epochs": EPOCHS,
            "window": WINDOW,
            "negative_samples": NEGATIVE_SAMPLES,
            "query_count_per_seed": QUERY_COUNT,
            "query_seeds": QUERY_SEEDS,
            "betas": BETAS.tolist(),
            "maximum_updates": MAX_ITERATIONS,
        },
        "text8_audit": text8,
        "author_notebook_audit": author,
        "training": training,
        "phase_sweeps": curves,
        "raw_query_results": raw_queries,
        "independent_checker": checker,
        "negative_control": negative_control,
        "checks": checks,
        "deviation": (
            "The paper describes Text8 as a 17-million-token corpus, but "
            "the recovered author notebook trains on only its first 100,000 "
            "tokens. The independent trainer preserves the historical "
            "objective, initialization, pair construction, Cython gradient "
            "lookup, and AdaGrad rule, but batches independent updates in "
            f"groups of {TRAIN_BATCH_SIZE} instead of applying every ranking "
            "pair sequentially."
        ),
    }
    (output_dir / "result.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    if result["verdict"] != "VERIFIED":
        raise SystemExit(json.dumps(result, indent=2))
    return result
