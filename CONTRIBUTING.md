# Contributing

All meaningful changes use the GitHub control plane.

## Development loop

Issue → discovery → proposal → branch → implementation → tests → pull request → review → merge.

Keep changes small and reversible. Preserve compatibility. Never commit secrets.

## Autonomous work

The agent may open issues, create branches, implement code in its sandbox, run tests, and open draft PRs within its configured permissions. High-impact changes remain subject to the approval policy in `docs/approval-policy.md`.

## Pull requests

Every PR should explain the problem, the change, evidence, tests, risks, rollback, and approval level. Do not mark a PR ready for review until automated checks pass and the author has verified the diff.
