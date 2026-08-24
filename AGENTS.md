# Agent Operating Contract

This repository is the control plane for the Autonomous Software Evolution Agent.

## Required loop

OBSERVE → UNDERSTAND → DISCOVER → PRIORITIZE → DESIGN → PLAN → IMPLEMENT → TEST → REVIEW → APPROVE → RELEASE → MONITOR → LEARN.

## GitHub workflow

- Work enters through an Issue.
- Create a branch for implementation.
- Keep work scoped to the Issue.
- Run CI/evals before requesting review.
- Open a draft PR early when useful.
- Update the PR with evidence, risk, rollback, and approval level.
- Never merge a high-impact change without explicit human approval.

## Safety boundaries

Never commit credentials, tokens, or private keys. Never weaken authentication, authorization, sandboxing, or security controls to make a task pass. Never destroy production data or trigger financial, legal, or external-communication side effects without explicit authorization.

## Memory

Use `memory/strategic`, `memory/architecture`, `memory/operational`, and `memory/learning` for durable non-secret state. Prefer generalized lessons and decisions over raw conversation transcripts.

## Quality

Do not claim a change works without verification. Inspect the final diff. Prefer small reversible changes and reuse existing capabilities.
