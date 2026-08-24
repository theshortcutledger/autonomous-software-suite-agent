# V1 Architecture

The V1 is intentionally a single orchestrator agent with narrow tools. The agent is backed by structured approval policy, a small file-based memory layout, a sandbox workspace boundary, and an evaluation harness. Specialist handoffs are deferred until the workflow demonstrates a need for them.

## Runtime Components

- `agent.py`: agent definition, instructions, tools, runner helper.
- `policy.py`: risk classification and approval rules.
- `memory.py`: structured memory operations.
- `main.py`: CLI + HTTP health endpoint.
- `evals/`: policy evaluation harness.

## Data boundaries

- `memory/`: persistent non-secret knowledge.
- `sandbox/`: autonomous workspace.
- credentials: environment only; never persisted by the application.
