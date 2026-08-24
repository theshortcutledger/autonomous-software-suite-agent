# Autonomous Suite Agent

A supervised autonomous software-evolution agent built for the OpenAI Agents SDK. V1 uses the SDK SandboxAgent with a bounded `repo/` workspace so the agent can inspect and modify software, run verification, and preserve state across sandbox sessions.

## What it does

- reasons about software-suite improvements;
- checks intended actions against approval policy;
- works inside a bounded sandbox;
- runs safe verification commands;
- retains structured memory outside secrets;
- exposes a small HTTP interface with `/health` and `/run`;
- includes a local policy evaluation harness.

## Install

This project requires network access to install `openai-agents` and the other declared dependencies:

```bash
uv sync
```

Then configure `OPENAI_API_KEY` in the environment. Never commit it. Set `SUITE_WORKSPACE=/absolute/path/to/your/software-suite` to point the agent at a real repo; otherwise it works in the local `sandbox/workspace` directory.

## Run

CLI:

```bash
uv run python main.py "Inspect the sandbox and propose the highest-value improvement."
```

HTTP:

```bash
PORT=8000 uv run python main.py
curl http://127.0.0.1:8000/health
```

## Evaluate

```bash
python evals/run_local.py
```

## Safety

Production actions, destructive operations, auth/security changes, and other high-impact changes require explicit approval. V1's tool surface is intentionally narrow; production deployment and external side effects are not exposed to the agent yet.
