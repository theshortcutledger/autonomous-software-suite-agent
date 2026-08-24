from __future__ import annotations

import argparse
import asyncio
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent import SDK_AVAILABLE, run_agent, workspace_path

app = FastAPI(title="Autonomous Suite Agent", version="0.1.0")


class RunRequest(BaseModel):
    prompt: str


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "agents_sdk_available": SDK_AVAILABLE, "workspace": str(workspace_path())}


@app.post("/run")
async def run_endpoint(request: RunRequest) -> dict[str, str]:
    try:
        return {"output": await run_agent(request.prompt)}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def cli() -> None:
    parser = argparse.ArgumentParser(description="Autonomous Software Evolution Agent")
    parser.add_argument("prompt", nargs="?", default="Inspect the workspace and propose the highest-value safe improvement.")
    args = parser.parse_args()
    print(asyncio.run(run_agent(args.prompt)))


if __name__ == "__main__":
    if os.getenv("PORT"):
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=int(os.environ["PORT"]))
    else:
        cli()
