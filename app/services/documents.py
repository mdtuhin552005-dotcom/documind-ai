import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path

import fitz
from fastapi import HTTPException, UploadFile
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from starlette.concurrency import run_in_threadpool

from app.core.config import Settings
from app.database import DocumentDatabase

logger = logging.getLogger(__name__)


def normalize_filename(filename: str | None) -> str:
    normalized = (filename or "document.pdf").replace("\\", "/").rsplit("/", maxsplit=1)[-1]
    normalized = "".join(character for character in normalized if character.isprintable()).strip()
    return normalized[:180] or "document.pdf"


def extract_pdf_pages(content: bytes, max_pages: int) -> list[tuple[int, str]]:
    try:
        pdf = fitz.open(stream=content, filetype="pdf")
    except (fitz.FileDataError, fitz.EmptyFileError, ValueError) as error:
        raise HTTPException(status_code=422, detail="The uploaded file is not a readable PDF.") from error

    with pdf:
        if pdf.is_encrypted:
            raise HTTPException(status_code=422, detail="Password-protected PDFs are not supported.")
        if pdf.page_count > max_pages:
            raise HTTPException(
                status_code=413,
                detail=f"This PDF has {pdf.page_count} pages; the limit is {max_pages}.",
            )

        pages: list[tuple[int, str]] = []
        for page_index in range(pdf.page_count):
            try:
                text = pdf.load_page(page_index).get_text("text").strip()
            except (fitz.FileDataError, RuntimeError) as error:
                raise HTTPException(
                    status_code=422,
                    detail=f"Unable to read page {page_index + 1} of this PDF.",
                ) from error
            if text:
                pages.append((page_index + 1, text))

    if not pages:
        raise HTTPException(
            status_code=422,
            detail="No selectable text was found. Scanned PDFs need OCR before uploading.",
        )
    return pages


def chunk_pdf_pages(
    pages: list[tuple[int, str]],
    document_id: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks: list[Document] = []
    for page_number, page_text in pages:
        for chunk in splitter.create_documents(
            [page_text],
            metadatas=[{"document_id": document_id, "page": page_number}],
        ):
            if chunk.page_content.strip():
                chunks.append(chunk)
    return chunks


class DocumentService:
    def __init__(
        self,
        settings: Settings,
        database: DocumentDatabase,
        vector_store: Chroma,
    ) -> None:
        self.settings = settings
        self.database = database
        self.vector_store = vector_store

    async def list_documents(self, user_id: str) -> list[dict]:
        return await self.database.list_documents(user_id)

    async def upload_pdf(self, upload: UploadFile, user_id: str) -> dict:
        if not self.settings.gemini_api_key or not self.settings.gemini_api_key.get_secret_value():
            raise HTTPException(
                status_code=503,
                detail="Document indexing is unavailable until GEMINI_API_KEY is configured.",
            )

        content = await upload.read(self.settings.upload_limit_bytes + 1)
        if len(content) > self.settings.upload_limit_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"PDFs must be {self.settings.max_upload_mb} MiB or smaller.",
            )
        if b"%PDF-" not in content[:1024]:
            raise HTTPException(status_code=415, detail="Upload a valid PDF file.")

        pages = await run_in_threadpool(
            extract_pdf_pages,
            content,
            self.settings.max_pdf_pages,
        )
        document_id = str(uuid.uuid4())
        chunks = await run_in_threadpool(
            chunk_pdf_pages,
            pages,
            document_id,
            self.settings.chunk_size,
            self.settings.chunk_overlap,
        )
        if not chunks:
            raise HTTPException(status_code=422, detail="No searchable text could be extracted.")

        display_name = normalize_filename(upload.filename)
        title = Path(display_name).stem or "Untitled document"
        stored_file = self.settings.uploads_dir / f"{document_id}.pdf"
        temporary_file = stored_file.with_suffix(".tmp")
        self.settings.uploads_dir.mkdir(parents=True, exist_ok=True)

        try:
            await run_in_threadpool(temporary_file.write_bytes, content)
            await run_in_threadpool(temporary_file.replace, stored_file)
            await run_in_threadpool(
                self.vector_store.add_documents,
                chunks,
                ids=[f"{document_id}:{index}" for index in range(len(chunks))],
            )
            record = {
                "id": document_id,
                "filename": display_name,
                "title": title,
                "page_count": len(pages),
                "chunk_count": len(chunks),
                "created_at": datetime.now(UTC).isoformat(),
                "file_path": str(stored_file),
                "user_id": user_id,
            }
            await self.database.add_document(record)
        except Exception:
            logger.exception("Failed to index uploaded document %s", document_id)
            await run_in_threadpool(self._remove_vectors, document_id)
            for path in (temporary_file, stored_file):
                try:
                    await run_in_threadpool(path.unlink, missing_ok=True)
                except OSError:
                    logger.exception("Failed to clean up temporary upload %s", path)
            raise

        logger.info(
            "Indexed document id=%s pages=%d chunks=%d",
            document_id,
            len(pages),
            len(chunks),
        )
        return record

    async def delete_document(self, document_id: str, user_id: str) -> bool:
        record = await self.database.get_document(document_id, user_id)
        if record is None:
            return False

        await run_in_threadpool(self._remove_vectors, document_id)
        deleted = await self.database.delete_document(document_id, user_id)
        if deleted:
            file_path = Path(record["file_path"])
            try:
                await run_in_threadpool(file_path.unlink, missing_ok=True)
            except OSError:
                logger.exception("Could not remove stored PDF for document %s", document_id)
        return deleted

    def _remove_vectors(self, document_id: str) -> None:
        self.vector_store.delete(where={"document_id": document_id})
