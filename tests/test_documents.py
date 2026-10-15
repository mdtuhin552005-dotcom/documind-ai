import fitz
import pytest
from fastapi import HTTPException

from app.services.documents import chunk_pdf_pages, extract_pdf_pages, normalize_filename


def make_pdf(*page_texts: str) -> bytes:
    pdf = fitz.open()
    for text in page_texts:
        page = pdf.new_page()
        page.insert_text((72, 72), text)
    content = pdf.tobytes()
    pdf.close()
    return content


def test_extract_pdf_pages_preserves_original_page_numbers() -> None:
    content = make_pdf("First page", "", "Third page")

    pages = extract_pdf_pages(content, max_pages=5)

    assert pages == [(1, "First page"), (3, "Third page")]


def test_extract_pdf_pages_rejects_page_limit() -> None:
    with pytest.raises(HTTPException) as error:
        extract_pdf_pages(make_pdf("one", "two"), max_pages=1)

    assert error.value.status_code == 413


def test_extract_pdf_pages_rejects_scanned_or_empty_documents() -> None:
    with pytest.raises(HTTPException) as error:
        extract_pdf_pages(make_pdf(""), max_pages=5)

    assert error.value.status_code == 422


def test_chunk_pdf_pages_keeps_document_and_page_metadata() -> None:
    chunks = chunk_pdf_pages(
        [(7, "A reliable finding. " * 40)],
        document_id="document-123",
        chunk_size=120,
        chunk_overlap=20,
    )

    assert len(chunks) > 1
    assert all(chunk.metadata["document_id"] == "document-123" for chunk in chunks)
    assert all(chunk.metadata["page"] == 7 for chunk in chunks)


def test_normalize_filename_removes_path_and_control_characters() -> None:
    assert normalize_filename("..\\private\\report.pdf\n") == "report.pdf"


def test_summarize_endpoint_handles_missing_document(tmp_path) -> None:
    import uuid
    from fastapi.testclient import TestClient
    from app.core.config import Settings
    from app.main import create_app

    test_settings = Settings(data_dir=tmp_path / "data", gemini_api_key=None)
    application = create_app(test_settings)
    with TestClient(application) as client:
        res = client.post(f"/api/documents/{uuid.uuid4()}/summary")
        assert res.status_code == 401
