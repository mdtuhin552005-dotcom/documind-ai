import json
import time
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Request
from app.api.routes.auth import require_authenticated_user

from app.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationCreateRequest,
    ConversationDetail,
    ConversationListResponse,
    ConversationMessage,
    ConversationSummary,
)
from app.services.chat import ChatService

router = APIRouter(prefix="/api/chat", tags=["chat"])
conversations_router = APIRouter(prefix="/api/chats", tags=["chat history"])


@router.post("", response_model=ChatResponse)
async def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    user = await require_authenticated_user(request)
    service: ChatService = request.app.state.chat_service
    start_time = time.time()
    result = await service.answer(payload, user["id"])
    duration_ms = round((time.time() - start_time) * 1000, 2)
    try:
        chunks_count = len(result.sources) if getattr(result, "sources", None) else 0
        await request.app.state.database.log_query(
            query_text=payload.message,
            response_time_ms=duration_ms,
            user_id=user["id"],
            document_id=payload.document_id,
            retrieved_chunks=chunks_count,
        )
        ip = request.client.host if request.client else None
        preview = payload.message[:50] + ("..." if len(payload.message) > 50 else "")
        await request.app.state.database.log_activity(
            "ASK_QUERY",
            f"Query: {preview} ({duration_ms}ms)",
            user_id=user["id"],
            ip_address=ip,
        )
    except Exception:
        pass
    return result


@conversations_router.get("", response_model=ConversationListResponse)
async def list_conversations(request: Request) -> ConversationListResponse:
    user = await require_authenticated_user(request)
    database = request.app.state.database
    conversations = await database.list_conversations(user_id=user["id"])
    return ConversationListResponse(conversations=conversations)


@conversations_router.post("", response_model=ConversationSummary, status_code=201)
async def create_conversation(
    request: Request,
    payload: ConversationCreateRequest,
) -> ConversationSummary:
    user = await require_authenticated_user(request)
    database = request.app.state.database
    document = await database.get_document(payload.document_id, user["id"])
    if document is None:
        raise HTTPException(status_code=404, detail="The selected document was not found.")
    now = datetime.now(UTC).isoformat()
    conversation = {
        "id": str(uuid.uuid4()),
        "document_id": payload.document_id,
        "title": "New chat",
        "created_at": now,
        "updated_at": now,
        "user_id": user["id"],
    }
    await database.create_conversation(conversation)
    return ConversationSummary(
        **conversation,
        document_filename=document["filename"],
        last_message=None,
    )


@conversations_router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(request: Request, conversation_id: str) -> ConversationDetail:
    user = await require_authenticated_user(request)
    try:
        conversation_id = str(uuid.UUID(conversation_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Chat was not found.") from error

    database = request.app.state.database
    conversation = await database.get_conversation(conversation_id, user["id"])
    if conversation is None:
        raise HTTPException(status_code=404, detail="Chat was not found.")

    messages = []
    for message in await database.get_conversation_messages(conversation_id):
        try:
            sources = json.loads(message["sources"])
        except (TypeError, json.JSONDecodeError) as error:
            raise RuntimeError("Saved chat contains invalid source references.") from error
        messages.append(
            ConversationMessage(
                role=message["role"],
                content=message["content"],
                sources=sources,
                created_at=message["created_at"],
            )
        )
    return ConversationDetail(**conversation, messages=messages)


@conversations_router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(request: Request, conversation_id: str) -> None:
    user = await require_authenticated_user(request)
    try:
        conversation_id = str(uuid.UUID(conversation_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Chat was not found.") from error
    database = request.app.state.database
    if not await database.delete_conversation(conversation_id, user["id"]):
        raise HTTPException(status_code=404, detail="Chat was not found.")

