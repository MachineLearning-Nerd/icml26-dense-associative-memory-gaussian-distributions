import json
import os
import platform
import resource
import subprocess
import time
from pathlib import Path

from reproduction.claims.claim_1.verifier import verify


def cpu_affinity_count():
    if not hasattr(os, "sched_getaffinity"):
        return None
    return len(os.sched_getaffinity(0))


def command_output(command):
    return subprocess.check_output(command, text=True).strip()


def main():
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    started = time.perf_counter()
    output_dir = Path(".openresearch/generated/claim_1")
    result = verify(output_dir)
    runtime = time.perf_counter() - started
    evidence = {
        "suite": "baseline-claim-1",
        "fixed_command": "uv sync --frozen && uv run python -m reproduction.run",
        "git_sha": command_output(["git", "rev-parse", "HEAD"]),
        "uv": command_output(["uv", "--version"]),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "logical_cpu_allocation": os.cpu_count(),
        "affinity_cpu_allocation": cpu_affinity_count(),
        "thread_limit": 1,
        "runtime_seconds": runtime,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "claims": [result],
    }
    (output_dir / "suite.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print("BEGIN_REPRODUCTION_EVIDENCE")
    print(json.dumps(evidence, indent=2))
    print("END_REPRODUCTION_EVIDENCE")


if __name__ == "__main__":
    main()
