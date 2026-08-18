from __future__ import annotations

import json
import logging
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Form, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.config import AUTH_DISABLED, CORS_ORIGINS, PORT, ROOT_DIR
from app.jobs import create_job, get_job, update_job

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

JOB_SCRIPT = ROOT_DIR / "scripts" / "generate_unable_to_reach.py"

app = FastAPI(title="Unable to Reach Letter Backend", version="1.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LetterPayload(BaseModel):
    firstName: str
    lastName: str
    clientName: str | None = None
    aNumber: str
    language: str = "hindi"
    addr_code: str = "add1"
    date: str | None = None


def _require_auth(authorization: str | None) -> None:
    if AUTH_DISABLED:
        return
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")


def _parse_data_json(data_json: str) -> dict[str, Any]:
    try:
        data = json.loads(data_json)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid data_json: {exc}") from exc
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="data_json must be an object")
    return data


def _start_pdf_job(job_id: str) -> None:
    if not JOB_SCRIPT.exists():
        update_job(job_id, status="failed", progress=100, error="PDF generation script is missing")
        raise HTTPException(status_code=500, detail="PDF generation script is missing")

    log_path = ROOT_DIR / "output" / job_id / "worker.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_file = open(log_path, "ab")
    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    try:
        subprocess.Popen(
            [sys.executable, str(JOB_SCRIPT), "--job-id", job_id],
            cwd=str(ROOT_DIR),
            stdout=log_file,
            stderr=subprocess.STDOUT,
            creationflags=creationflags,
        )
    except Exception as exc:
        log_file.close()
        update_job(job_id, status="failed", progress=100, error=str(exc))
        raise HTTPException(status_code=500, detail="Could not start PDF job") from exc
    logger.info("Started PDF job script for %s", job_id)


def _queue_job(payload: dict[str, Any]) -> dict[str, str]:
    job_id = uuid.uuid4().hex
    create_job(job_id, payload)
    _start_pdf_job(job_id)
    return {"job_id": job_id, "status": "queued"}


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "unable-to-reach-letter",
        "try_these": {
            "health": "http://localhost:8000/health",
            "docs": "http://localhost:8000/docs",
        },
        "endpoints": {
            "POST": "/api/unable-to-reach-letter",
            "GET_status": "/api/job-status/{job_id}",
            "GET_download": "/api/download/{job_id}",
        },
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "unable-to-reach-letter"}


@app.post("/api/unable-to-reach-letter")
async def unable_to_reach_letter(
    authorization: str | None = Header(default=None),
    data_json: str = Form(
        ...,
        description="JSON with firstName, lastName, aNumber, language, addr_code, date",
    ),
) -> dict[str, str]:
    _require_auth(authorization)
    payload = _parse_data_json(data_json)
    return _queue_job(payload)


@app.post("/api/generate")
def generate_letter_json(
    payload: LetterPayload,
    authorization: str | None = Header(default=None),
) -> dict[str, str]:
    _require_auth(authorization)
    return _queue_job(payload.model_dump())


@app.get("/api/job-status/{job_id}")
def job_status(job_id: str, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    _require_auth(authorization)
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "status": job["status"],
        "progress": job.get("progress", 0),
        "message": job.get("message"),
        "error": job.get("error"),
        "job_id": job_id,
    }


@app.get("/api/download/{job_id}")
def download(job_id: str, authorization: str | None = Header(default=None)):
    _require_auth(authorization)
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    zip_path = job.get("zip_path")
    if job["status"] != "completed" or not zip_path:
        raise HTTPException(status_code=409, detail="Job is not ready for download")
    path = Path(zip_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Generated file not found")
    return FileResponse(
        path,
        media_type="application/zip",
        filename=f"{job_id}_unable_to_reach_letter.zip",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
