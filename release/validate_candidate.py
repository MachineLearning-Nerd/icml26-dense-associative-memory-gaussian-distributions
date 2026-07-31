import json
import re
import sys
from collections import deque
from pathlib import Path


root = Path(sys.argv[1]).resolve()
links_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
sha_pattern = re.compile(r"`[0-9a-f]{40}`")

queue = deque(
    [
        root / "README.md",
        root / "logbook.json",
        root / "pages" / "index.md",
    ]
)
opened = set()
broken = []


def enqueue(path):
    resolved = path.resolve()
    if root not in resolved.parents and resolved != root:
        broken.append({"path": str(path), "reason": "escapes candidate root"})
        return
    if not resolved.is_file():
        broken.append({"path": str(path), "reason": "missing"})
        return
    if resolved not in opened:
        queue.append(resolved)


while queue:
    path = queue.popleft()
    if path in opened:
        continue
    if not path.is_file():
        broken.append({"path": str(path), "reason": "missing entrypoint"})
        continue
    opened.add(path)
    if path.suffix.lower() not in {".md", ".json"}:
        continue
    text = path.read_text()
    if path.name == "logbook.json":
        logbook = json.loads(text)
        nodes = [logbook["root"]]
        while nodes:
            node = nodes.pop()
            enqueue(root / node["file"])
            nodes.extend(node.get("children", []))
    if path.suffix.lower() == ".md":
        for target in links_pattern.findall(text):
            if (
                "://" in target
                or target.startswith("#")
                or target.startswith("mailto:")
            ):
                continue
            enqueue(path.parent / target.split("#", 1)[0])


claim_results = {}
for claim_id in range(1, 7):
    relative = Path("pages") / "current" / f"claim-{claim_id}.md"
    path = root / relative
    text = path.read_text() if path.is_file() else ""
    links = links_pattern.findall(text)

    def linked(fragment):
        return any(fragment in target for target in links)

    checks = {
        "reachable": path.resolve() in opened,
        "exact_contract_inline": "## Exact contract" in text,
        "source_anchor_inline": "Canonical source:" in text,
        "assumptions_numerical_audit_inline": (
            bool(re.search(r"\d", text))
            and (
                "assumption" in text.lower()
                or "contract" in text.lower()
                or "domain" in text.lower()
            )
        ),
        "verifier_link": linked("verifier.py"),
        "contract_link": linked("claim_contract.json"),
        "source_audit_link": linked("source_audit.md"),
        "raw_link": linked("/raw/"),
        "checker_link": linked("independent_checker.json"),
        "control_link": linked("negative_control.json"),
        "runtime_link": linked("runtime.json"),
        "eval_link": linked("EVAL.md"),
        "raw_numbers_inline": "|" in text and bool(re.search(r"\d", text)),
        "fixed_command_inline": (
            "uv sync --frozen && uv run python -m reproduction.run" in text
        ),
        "nonzero_failure_inline": "exits nonzero" in text,
        "limitations_inline": "## Limitations" in text,
        "git_sha_inline": bool(sha_pattern.search(text)),
        "seeds_inline": "seed" in text.lower(),
        "cpu_runtime_inline": (
            "cpu-upgrade" in text
            and ("runtime" in text.lower() or "duration" in text.lower())
        ),
        "verdict_inline": (
            "VERIFIED" in text.splitlines()[0]
            or "FALSIFIED" in text.splitlines()[0]
        ),
    }
    claim_results[str(claim_id)] = {
        "page": str(relative),
        "checks": checks,
        "complete": all(checks.values()),
    }

historical = (root / "pages" / "overview" / "page.md").resolve()
index_text = (root / "pages" / "index.md").read_text()
summary = {
    "candidate_root": str(root),
    "entrypoints": ["README.md", "logbook.json", "pages/index.md"],
    "opened_files": sorted(str(path.relative_to(root)) for path in opened),
    "broken_links": broken,
    "historical_rejected_baseline_reachable": historical in opened,
    "historical_label_exact": "Historical rejected baseline" in index_text,
    "claims": claim_results,
}
summary["passed"] = (
    not broken
    and summary["historical_rejected_baseline_reachable"]
    and summary["historical_label_exact"]
    and all(row["complete"] for row in claim_results.values())
)
print(json.dumps(summary, indent=2))
raise SystemExit(0 if summary["passed"] else 1)
