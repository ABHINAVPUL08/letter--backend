from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config import OUTPUT_DIR


def job_dir(job_id: str) -> Path:
    path = OUTPUT_DIR / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def _job_path(job_id: str) -> Path:
    return job_dir(job_id) / "job.json"


def _payload_path(job_id: str) -> Path:
    return job_dir(job_id) / "payload.json"


def _write_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def create_job(job_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    job = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0,
        "message": "Queued",
        "error": None,
        "zip_path": None,
    }
    _write_json(_job_path(job_id), job)
    _write_json(_payload_path(job_id), payload)
    return job


def update_job(job_id: str, **fields: Any) -> None:
    job = _read_json(_job_path(job_id))
    if not job:
        return
    job.update(fields)
    _write_json(_job_path(job_id), job)


def get_job(job_id: str) -> dict[str, Any] | None:
    return _read_json(_job_path(job_id))


def get_payload(job_id: str) -> dict[str, Any] | None:
    return _read_json(_payload_path(job_id))
