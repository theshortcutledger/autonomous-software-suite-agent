from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent / "memory"


def _bucket_path(bucket: str) -> Path:
    path = ROOT / bucket
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_record(bucket: str, name: str, data: dict[str, Any]) -> Path:
    path = _bucket_path(bucket) / f"{name}.json"
    payload = {"updated_at": datetime.now(timezone.utc).isoformat(), "data": data}
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_record(bucket: str, name: str) -> dict[str, Any] | None:
    path = _bucket_path(bucket) / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_records(bucket: str) -> list[str]:
    return sorted(p.stem for p in _bucket_path(bucket).glob("*.json"))
