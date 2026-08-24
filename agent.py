from __future__ import annotations

import os
from pathlib import Path

from policy import classify_action

try:
    from agents import Runner
    from agents.run import RunConfig
    from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
    from agents.sandbox.entries import LocalDir
    from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False

ROOT = Path(__file__).resolve().parent
DEFAULT_WORKSPACE = ROOT / "sandbox" / "workspace"
DEFAULT_WORKSPACE.mkdir(parents=True, exist_ok=True)
INSTRUCTIONS = (ROOT / "docs" / "prompt.md").read_text(encoding="utf-8")


def _require_sdk() -> None:
    if not SDK_AVAILABLE:
        raise RuntimeError(
            "OpenAI Agents SDK is not installed in this environment. "
            "Run `uv sync` where network/package access is available."
        )


def workspace_path() -> Path:
    configured = os.getenv("SUITE_WORKSPACE")
    path = Path(configured).expanduser().resolve() if configured else DEFAULT_WORKSPACE.resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_agent():
    _require_sdk()
    workspace = workspace_path()
    return SandboxAgent(
        name="Autonomous Software Evolution Agent",
        model=os.getenv("MODEL", "gpt-5.6"),
        instructions=INSTRUCTIONS + "\n\nWorkspace is mounted at `repo/`. Never assume files outside `repo/` are available. Before any consequential action, call the approval policy tool if exposed by the runtime; high-impact actions must be escalated.",
        default_manifest=Manifest(entries={"repo": LocalDir(src=workspace)}),
    )


async def run_agent(prompt: str) -> str:
    _require_sdk()
    result = await Runner.run(
        build_agent(),
        prompt,
        run_config=RunConfig(
            sandbox=SandboxRunConfig(client=UnixLocalSandboxClient()),
            workflow_name="Autonomous Software Evolution Agent",
        ),
    )
    return str(result.final_output)


class PolicyTool:
    @staticmethod
    def evaluate(action: str) -> str:
        decision = classify_action(action)
        return f"level={decision.level.name}; allowed={decision.allowed}; reason={decision.reason}"
