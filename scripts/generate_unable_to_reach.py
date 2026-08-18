#!/usr/bin/env python3
"""Generate the Unable to Reach letter PDF/Word package for one queued job.

The API server only creates a job. This script does the work:

    python scripts/generate_unable_to_reach.py --job-id <id>
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import traceback
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.jobs import get_payload, job_dir, update_job
from generator.letter_builder import build_combined_letter_docx
from generator.pdf_export import convert_docx_to_pdf
from generator.translator import transliterate_client_name

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("generate_unable_to_reach")

SUPPORTED_LANGUAGES = {"hindi", "punjabi"}


def format_a_number(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) != 9:
        raise ValueError("A-number must be exactly 9 digits")
    return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"


def format_letter_date(raw: str | None) -> str:
    if raw and str(raw).strip() and str(raw).strip().lower() not in {"unknown", "n/a"}:
        text = str(raw).strip()
        for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(text, fmt).strftime("%m/%d/%Y")
            except ValueError:
                continue
        return text
    return datetime.now().strftime("%m/%d/%Y")


def normalize_payload(data: dict[str, Any]) -> dict[str, Any]:
    first = str(data.get("firstName") or "").strip().upper()
    last = str(data.get("lastName") or "").strip().upper()
    client_name = str(data.get("clientName") or "").strip().upper()
    if not client_name:
        client_name = ", ".join(p for p in (last, first) if p)
    if not first or not last:
        raise ValueError("firstName and lastName are required")

    language = str(data.get("language") or "").strip().lower()
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError("language must be hindi or punjabi")

    a_digits = re.sub(r"\D", "", str(data.get("aNumber") or ""))
    a_formatted = format_a_number(a_digits)
    addr_code = str(data.get("addr_code") or data.get("addrCode") or "add1").strip().lower()
    if addr_code not in {"add1", "add2", "add3"}:
        addr_code = "add1"

    return {
        "firstName": first,
        "lastName": last,
        "clientName": client_name,
        "aNumber": a_digits,
        "aNumberFormatted": a_formatted,
        "language": language,
        "addr_code": addr_code,
        "date": format_letter_date(data.get("date") or data.get("letterDate")),
    }


def generate_package(data: dict[str, Any], out_dir: Path) -> Path:
    payload = normalize_payload(data)
    out_dir.mkdir(parents=True, exist_ok=True)

    english_name = payload["clientName"]
    language = payload["language"]
    native_name = transliterate_client_name(english_name, language)

    stem = f"{payload['lastName']}_{payload['firstName']}_A_{payload['aNumber']}_unable_to_reach"
    docx_path = out_dir / f"{stem}.docx"
    pdf_path = out_dir / f"{stem}.pdf"

    build_combined_letter_docx(
        native_language=language,
        english_name=english_name,
        native_name=native_name,
        a_number_formatted=payload["aNumberFormatted"],
        native_a_number=payload["aNumberFormatted"],
        letter_date=payload["date"],
        native_date=payload["date"],
        dest_path=docx_path,
    )
    pdf_file = convert_docx_to_pdf(docx_path, pdf_path)

    zip_path = out_dir / f"{payload['firstName']}_A_{payload['aNumber']}_unable_to_reach_letter.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        if pdf_file and pdf_file.exists():
            zf.write(pdf_file, pdf_file.name)
        zf.write(docx_path, docx_path.name)
        zf.writestr(
            "payload.json",
            json.dumps(
                {
                    **payload,
                    "nativeName": native_name,
                    "languages": ["english", payload["language"]],
                    "note": "One file: English first, then the translated letter.",
                },
                indent=2,
                ensure_ascii=False,
            ),
        )
    logger.info("Created letter package %s", zip_path)
    return zip_path


def run_job(job_id: str) -> None:
    payload = get_payload(job_id)
    if payload is None:
        raise FileNotFoundError(f"No payload found for job {job_id}")

    update_job(job_id, status="processing", progress=10, message="Generating letters")
    zip_path = generate_package(payload, job_dir(job_id))
    update_job(
        job_id,
        status="completed",
        progress=100,
        message="Unable to Reach letter generated",
        zip_path=str(zip_path),
        error=None,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Unable to Reach letter for a job")
    parser.add_argument("--job-id", required=True, help="Job id created by the API server")
    args = parser.parse_args()
    job_id = args.job_id.strip()
    try:
        run_job(job_id)
        return 0
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
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
