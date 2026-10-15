from uuid import UUID

from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status

from app.schemas import DocumentListResponse, DocumentResponse, DocumentSummaryResponse
from app.api.routes.auth import require_authenticated_user
from app.services.documents import DocumentService

router = APIRouter(prefix="/api/documents", tags=["documents"])


def get_service(request: Request) -> DocumentService:
    return request.app.state.document_service


@router.get("", response_model=DocumentListResponse)
async def list_documents(request: Request) -> DocumentListResponse:
    user = await require_authenticated_user(request)
    documents = await get_service(request).list_documents(user["id"])
    return DocumentListResponse(documents=documents)


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
) -> DocumentResponse:
    user = await require_authenticated_user(request)
    try:
        result = await get_service(request).upload_pdf(file, user["id"])
        return DocumentResponse.model_validate(result)
    finally:
        await file.close()


@router.post("/{document_id}/summary", response_model=DocumentSummaryResponse)
async def summarize_document(request: Request, document_id: str) -> DocumentSummaryResponse:
    user = await require_authenticated_user(request)
    try:
        validated_id = str(UUID(document_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail="The selected document was not found.") from error
    chat_service = request.app.state.chat_service
    return await chat_service.generate_summary(validated_id, user["id"])


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(request: Request, document_id: str) -> None:
    user = await require_authenticated_user(request)
    try:
        validated_id = str(UUID(document_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail="The selected document was not found.") from error
    deleted = await get_service(request).delete_document(validated_id, user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="The selected document was not found.")
