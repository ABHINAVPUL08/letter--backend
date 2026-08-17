from __future__ import annotations

import json
import logging
import re
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import OUTPUT_DIR
from app.content import LETTERS
from app.letter_builder import build_combined_letter_docx
from app.pdf_export import convert_docx_to_pdf
from app.translator import transliterate_client_name

logger = logging.getLogger(__name__)

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


def generate_package(data: dict[str, Any], job_dir: Path) -> Path:
    payload = normalize_payload(data)
    job_dir.mkdir(parents=True, exist_ok=True)

    english_name = payload["clientName"]
    language = payload["language"]
    native_name = transliterate_client_name(english_name, language)

    stem = f"{payload['lastName']}_{payload['firstName']}_A_{payload['aNumber']}_unable_to_reach"
    docx_path = job_dir / f"{stem}.docx"
    pdf_path = job_dir / f"{stem}.pdf"

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

    zip_path = job_dir / f"{payload['firstName']}_A_{payload['aNumber']}_unable_to_reach_letter.zip"
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


def output_dir_for(job_id: str) -> Path:
    path = OUTPUT_DIR / job_id
    path.mkdir(parents=True, exist_ok=True)
    return path


# Keep import used for language validation at runtime.
assert "english" in LETTERS and "hindi" in LETTERS and "punjabi" in LETTERS
