# GitHub Control Plane

GitHub is the source of truth for the Autonomous Software Evolution Agent.

## Lifecycle

1. **Intake** — work enters through an Issue.
2. **Discovery** — the agent gathers evidence and identifies affected systems.
3. **Proposal** — the agent records objective, value, architecture, risks, tests, rollback, and required approval level.
4. **Implementation** — approved L0/L1 work is developed on a feature branch; L2/L3 work cannot proceed to production side effects without explicit approval.
5. **Verification** — CI runs syntax and policy/eval checks. The agent must report actual test results.
6. **Pull Request** — every meaningful code change lands through a PR.
7. **Human review** — required for the approval levels defined in `docs/approval-policy.md`.
8. **Merge** — only after required checks and review requirements pass.
9. **Release** — staging/production actions remain separately gated.
10. **Learning** — durable decisions and operational lessons are written to memory.

## GitHub as state

Issues represent work and discovery. Pull requests represent implementation. PR comments represent review decisions. CI represents automated verification. The repository history is the audit trail.

## Branch model

- `main` — release-ready code and the only production source branch.
- `chore/*` — repository maintenance.
- `feature/*` — autonomous or human feature work.
- `fix/*` — defect fixes.
- `experiment/*` — reversible research and prototypes.

## Approval gates

- **L0:** autonomous.
- **L1:** review recommended; no production side effect.
- **L2:** explicit human approval required before high-impact execution.
- **L3:** blocked by default; explicit authorization is required even to prepare certain actions.

## Agent behavior

The agent may create Issues, branches, commits, tests, documentation, and draft PRs within its tool permissions. It must not merge production-impacting changes merely because CI passes. Human approval remains the authority for high-impact actions.
