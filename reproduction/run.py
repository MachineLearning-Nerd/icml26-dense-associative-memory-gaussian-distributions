import json
import os
import platform
import resource
import subprocess
import time
from pathlib import Path

THREAD_LIMIT = min(64, os.cpu_count() or 1)
os.environ["OMP_NUM_THREADS"] = str(THREAD_LIMIT)
os.environ["OPENBLAS_NUM_THREADS"] = str(THREAD_LIMIT)
os.environ["MKL_NUM_THREADS"] = str(THREAD_LIMIT)

from reproduction.claims.claim_1.verifier import verify as verify_claim_1
from reproduction.claims.claim_2.verifier import verify as verify_claim_2
from reproduction.claims.claim_3.verifier import verify as verify_claim_3
from reproduction.claims.claim_4.verifier import verify as verify_claim_4
from reproduction.claims.claim_5.verifier import verify as verify_claim_5
from reproduction.claims.claim_6.verifier import verify as verify_claim_6


def cpu_affinity_count():
    if not hasattr(os, "sched_getaffinity"):
        return None
    return len(os.sched_getaffinity(0))


def command_output(command):
    return subprocess.check_output(command, text=True).strip()


def main():
    started = time.perf_counter()
    output_root = Path(".openresearch/generated")
    claim_1 = verify_claim_1(output_root / "claim_1")
    claim_2 = verify_claim_2(output_root / "claim_2")
    claim_3 = verify_claim_3(output_root / "claim_3")
    claim_4 = verify_claim_4(output_root / "claim_4")
    claim_5 = verify_claim_5(output_root / "claim_5")
    claim_6 = verify_claim_6(output_root / "claim_6")
    runtime = time.perf_counter() - started
    evidence = {
        "suite": "cumulative-claims-1-through-6",
        "fixed_command": "uv sync --frozen && uv run python -m reproduction.run",
        "git_sha": command_output(["git", "rev-parse", "HEAD"]),
        "uv": command_output(["uv", "--version"]),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "logical_cpu_allocation": os.cpu_count(),
        "affinity_cpu_allocation": cpu_affinity_count(),
        "estimated_required_cores": 64,
        "selected_compute_flavor": "cpu-upgrade",
        "thread_limit": THREAD_LIMIT,
        "runtime_seconds": runtime,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "claims": [
            claim_1,
            claim_2,
            claim_3,
            claim_4,
            claim_5,
            claim_6,
        ],
    }
    (output_root / "suite.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print("BEGIN_REPRODUCTION_EVIDENCE")
    print(json.dumps(evidence, indent=2))
    print("END_REPRODUCTION_EVIDENCE")


if __name__ == "__main__":
    main()
