import numpy as np


def symmetric_sqrt(matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    if np.min(eigenvalues) <= 0:
        raise ValueError("covariance must be positive definite")
    return (eigenvectors * np.sqrt(eigenvalues)) @ eigenvectors.T


def wasserstein_squared(left, right):
    left_mean, left_covariance = left
    right_mean, right_covariance = right
    left_sqrt = symmetric_sqrt(left_covariance)
    cross_sqrt = symmetric_sqrt(left_sqrt @ right_covariance @ left_sqrt)
    mean_term = np.sum((left_mean - right_mean) ** 2)
    covariance_term = np.trace(left_covariance + right_covariance - 2 * cross_sqrt)
    return float(mean_term + covariance_term)


def energy(query, patterns, beta):
    distances = np.array([wasserstein_squared(pattern, query) for pattern in patterns])
    logits = -beta * distances
    maximum = float(np.max(logits))
    return float(-(maximum + np.log(np.exp(logits - maximum).sum())) / beta)


def weights(query, patterns, beta):
    distances = np.array([wasserstein_squared(pattern, query) for pattern in patterns])
    logits = -beta * distances
    exponentials = np.exp(logits - np.max(logits))
    return exponentials / exponentials.sum()


def mean_gradient(query, patterns, beta):
    query_mean, _ = query
    coefficients = weights(query, patterns, beta)
    pattern_means = np.stack([mean for mean, _ in patterns])
    return 2 * np.sum(coefficients[:, None] * (query_mean - pattern_means), axis=0)

