"""Export the combined Word letter to a single PDF."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def convert_docx_to_pdf(docx_path: Path, pdf_path: Path) -> Path | None:
    docx_path = docx_path.resolve()
    pdf_path = pdf_path.resolve()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        import pythoncom
        import win32com.client
    except ImportError:
        logger.warning("pywin32 is not installed; cannot convert to PDF via Word/WPS")
        return None

    pythoncom.CoInitialize()
    app = None
    doc = None
    try:
        for prog_id in ("Word.Application", "Kwps.Application", "wps.Application"):
            try:
                app = win32com.client.DispatchEx(prog_id)
            except Exception:
                app = None
                continue
            try:
                app.Visible = False
                app.DisplayAlerts = 0
            except Exception:
                pass
            try:
                doc = app.Documents.Open(str(docx_path), ReadOnly=True)
                exported = False
                try:
                    doc.ExportAsFixedFormat(OutputFileName=str(pdf_path), ExportFormat=17)
                    exported = True
                except Exception:
                    try:
                        doc.SaveAs(str(pdf_path), FileFormat=17)
                        exported = True
                    except Exception:
                        logger.exception("PDF export failed with %s", prog_id)
                try:
                    doc.Close(False)
                except Exception:
                    pass
                doc = None
                try:
                    app.Quit()
                except Exception:
                    pass
                app = None
                if exported and pdf_path.exists() and pdf_path.stat().st_size > 0:
                    logger.info("Created PDF with %s: %s", prog_id, pdf_path)
                    return pdf_path
            except Exception:
                logger.exception("Could not convert using %s", prog_id)
                try:
                    if doc is not None:
                        doc.Close(False)
                except Exception:
                    pass
                try:
                    if app is not None:
                        app.Quit()
                except Exception:
                    pass
                app = None
                doc = None
        return None
    finally:
        pythoncom.CoUninitialize()
