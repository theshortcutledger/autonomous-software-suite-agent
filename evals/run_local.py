from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from policy import classify_action

CASES = Path(__file__).with_name("cases.jsonl")
RESULTS = Path(__file__).with_name("results")


def main() -> int:
    RESULTS.mkdir(exist_ok=True)
    failures = []
    results = []
    for line in CASES.read_text(encoding="utf-8").splitlines():
        case = json.loads(line)
        decision = classify_action(case["action"])
        passed = decision.level.name == case["expected_level"] and decision.allowed == case["expected_allowed"]
        item = {**case, "actual_level": decision.level.name, "actual_allowed": decision.allowed, "reason": decision.reason, "passed": passed}
        results.append(item)
        if not passed:
            failures.append(item)
    output = {"passed": not failures, "cases": results}
    (RESULTS / "latest.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
