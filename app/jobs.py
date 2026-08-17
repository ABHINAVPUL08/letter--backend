from __future__ import annotations

import threading
from typing import Any

_lock = threading.Lock()
_jobs: dict[str, dict[str, Any]] = {}


def create_job(job_id: str) -> dict[str, Any]:
    job = {"status": "queued", "progress": 0, "message": "Queued", "error": None, "zip_path": None}
    with _lock:
        _jobs[job_id] = job
    return job


def update_job(job_id: str, **fields: Any) -> None:
    with _lock:
        job = _jobs.get(job_id)
        if not job:
            return
        job.update(fields)


def get_job(job_id: str) -> dict[str, Any] | None:
    with _lock:
        job = _jobs.get(job_id)
        return dict(job) if job else None
