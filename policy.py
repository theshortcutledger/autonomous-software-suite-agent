from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class ApprovalLevel(IntEnum):
    L0 = 0
    L1 = 1
    L2 = 2
    L3 = 3


@dataclass(frozen=True)
class Decision:
    level: ApprovalLevel
    allowed: bool
    reason: str


KEYWORDS: dict[ApprovalLevel, tuple[str, ...]] = {
    ApprovalLevel.L3: (
        "destroy production", "delete production", "expose secret", "bypass security",
        "transfer money", "disable security", "delete core infrastructure",
    ),
    ApprovalLevel.L2: (
        "deploy production", "production deployment", "breaking api", "break compatibility",
        "production migration", "change authentication", "change authorization", "major infrastructure",
    ),
    ApprovalLevel.L1: (
        "dependency upgrade", "staging deployment", "deploy staging", "schema addition", "moderate refactor",
    ),
}


def classify_action(action: str) -> Decision:
    normalized = action.lower().strip()
    for level in (ApprovalLevel.L3, ApprovalLevel.L2, ApprovalLevel.L1):
        for phrase in KEYWORDS[level]:
            if phrase in normalized:
                if level == ApprovalLevel.L3:
                    return Decision(level, False, f"Blocked by default: {phrase}")
                return Decision(level, False, f"Explicit approval required: {phrase}")
    return Decision(ApprovalLevel.L0, True, "Autonomous action permitted")
