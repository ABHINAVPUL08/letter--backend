from __future__ import annotations

import json
import logging
import traceback
import uuid
from typing import Any

from fastapi import BackgroundTasks, FastAPI, Form, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.config import AUTH_DISABLED, CORS_ORIGINS, PORT
from app.jobs import create_job, get_job, update_job
from app.service import generate_package, output_dir_for

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Unable to Reach Letter Backend", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LetterPayload(BaseModel):
    firstName: str = "ABHINAV"
    lastName: str = "PULYANI"
    clientName: str = "PULYANI, ABHINAV"
    aNumber: str = "251566057"
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


def _run_job(job_id: str, payload: dict[str, Any]) -> None:
    try:
        update_job(job_id, status="processing", progress=10, message="Generating letters")
        zip_path = generate_package(payload, output_dir_for(job_id))
        update_job(
            job_id,
            status="completed",
            progress=100,
            message="Unable to Reach letter generated",
            zip_path=str(zip_path),
            error=None,
        )
    except Exception as exc:
        logger.exception("Job %s failed", job_id)
        update_job(
            job_id,
            status="failed",
            progress=100,
            message="Processing failed",
            error=str(exc),
            traceback=traceback.format_exc(),
        )


def _queue_job(background_tasks: BackgroundTasks, payload: dict[str, Any]) -> dict[str, str]:
    job_id = uuid.uuid4().hex
    create_job(job_id)
    background_tasks.add_task(_run_job, job_id, payload)
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
        "generate_letter": "POST /api/unable-to-reach-letter with form field data_json",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "unable-to-reach-letter"}


@app.post("/api/unable-to-reach-letter")
async def unable_to_reach_letter(
    background_tasks: BackgroundTasks,
    authorization: str | None = Header(default=None),
    data_json: str = Form(
        default=(
            '{"firstName":"ABHINAV","lastName":"PULYANI","clientName":"PULYANI, ABHINAV",'
            '"aNumber":"251566057","language":"hindi","addr_code":"add1"}'
        ),
        description="JSON with firstName, lastName, aNumber, language, addr_code, date",
    ),
) -> dict[str, str]:
    _require_auth(authorization)
    payload = _parse_data_json(data_json)
    return _queue_job(background_tasks, payload)


@app.post("/api/generate")
def generate_letter_json(
    payload: LetterPayload,
    background_tasks: BackgroundTasks,
    authorization: str | None = Header(default=None),
) -> dict[str, str]:
    _require_auth(authorization)
    return _queue_job(background_tasks, payload.model_dump())


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
    if job["status"] != "completed" or not job.get("zip_path"):
        raise HTTPException(status_code=409, detail="Job is not ready for download")
    return FileResponse(
        job["zip_path"],
        media_type="application/zip",
        filename=f"{job_id}_unable_to_reach_letter.zip",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
